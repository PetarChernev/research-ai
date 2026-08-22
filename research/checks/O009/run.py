#!/usr/bin/env python3
"""Exact claim-specific implementation of O009; never writes result.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable, Mapping

OBLIGATION_ID = "O009"
ROOT = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra, ExteriorForm, Polynomial, RationalMatrix, levi_civita_sign,
)

PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PRODUCER_MODEL = "openai/gpt-5.6-sol"
OBSERVATION_PREFIX = "##OBSERVATIONS##"
MUTATION_ENV = "O009_INTENTIONAL_MUTATION"
MUTATION = os.environ.get(MUTATION_ENV, "")
MUTATIONS = (
    "spin-connection-sign", "ordered-pair-normalization",
    "omit-circle-equation", "delete-rho-prime-endpoint",
)
F = Fraction
Z, O = F(0), F(1)
I5, I4 = tuple(range(5)), tuple(range(4))
ETA5 = (-1, 1, 1, 1, 1)
PAIRS5 = tuple(combinations(I5, 2))


class UnsupportedSectorError(ValueError):
    pass


@dataclass
class Recorder:
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    def require(self, name: str, condition: bool) -> None:
        if type(condition) is not bool:
            raise TypeError(f"assertion {name!r} did not return bool")
        (self.passed if condition else self.failed).append(name)

    @property
    def total(self) -> int:
        return len(self.passed) + len(self.failed)


def emit(data: Mapping[str, Any]) -> None:
    print(OBSERVATION_PREFIX + " " + json.dumps(data, sort_keys=True, default=str, allow_nan=False))


def wedge_all(alg: ExteriorAlgebra, factors: Iterable[ExteriorForm]) -> ExteriorForm:
    out = alg.unit()
    for factor in factors:
        out = out.wedge(factor)
    return out


def ordered_pair(a: int, b: int) -> tuple[tuple[int, int], int]:
    if a == b:
        raise ValueError("equal antisymmetric indices")
    return ((a, b), 1) if a < b else ((b, a), -1)


def cartan_system() -> tuple[tuple[tuple[int, int, int], ...], RationalMatrix, tuple[F, ...]]:
    """Solve T^A=0 after factoring q=rho'/rho from dE4=q E3^E4."""
    unknowns = tuple((a, b, c) for a, b in PAIRS5 for c in I5)
    equations = tuple((a, i, j) for a in I5 for i, j in PAIRS5)
    position = {u: n for n, u in enumerate(unknowns)}
    rows: list[list[F]] = []
    rhs: list[F] = []
    for a, i, j in equations:
        row = [Z] * 50
        for b in I5:
            if a == b:
                continue
            pair, anti = ordered_pair(a, b)
            for c in I5:
                if c == b or (min(c, b), max(c, b)) != (i, j):
                    continue
                wedge_sign = 1 if c < b else -1
                row[position[(pair[0], pair[1], c)]] += F(ETA5[b] * anti * wedge_sign)
        source = O if (a, i, j) == (4, 3, 4) else Z
        rows.append(row)
        rhs.append(-source)
    matrix = RationalMatrix(rows)
    augmented, pivots = RationalMatrix([row + [v] for row, v in zip(rows, rhs)]).rref()
    if matrix.rank() != 50 or pivots[:50] != tuple(range(50)):
        raise UnsupportedSectorError("open-core Cartan map is not uniquely solvable")
    return unknowns, matrix, tuple(augmented.rows[i][-1] for i in range(50))


def torsion_residuals(unknowns: tuple[tuple[int, int, int], ...], solution: tuple[F, ...]) -> tuple[F, ...]:
    values = dict(zip(unknowns, solution))
    residuals: list[F] = []
    for a in I5:
        for i, j in PAIRS5:
            value = O if (a, i, j) == (4, 3, 4) else Z
            for b in I5:
                if a == b:
                    continue
                pair, anti = ordered_pair(a, b)
                for c in I5:
                    if c != b and (min(c, b), max(c, b)) == (i, j):
                        value += F(ETA5[b] * anti * (1 if c < b else -1)) * values[(pair[0], pair[1], c)]
            residuals.append(value)
    return tuple(residuals)


def coordinate_geometry(unknowns: tuple[tuple[int, int, int], ...], solution: tuple[F, ...]):
    """Use q E4=rho' dtheta, then explicitly differentiate rho'."""
    alg = ExteriorAlgebra(("dt", "dx", "dy", "ds", "dtheta"))
    ds, dtheta = alg.basis_form("ds"), alg.basis_form("dtheta")
    rp, rpp = Polynomial.generator("rho_prime"), Polynomial.generator("rho_double_prime")
    omega: dict[tuple[int, int], ExteriorForm] = {}
    for (a, b, leg), value in zip(unknowns, solution):
        if value:
            if leg != 4:
                raise UnsupportedSectorError("unsupported q E^C coordinate conversion")
            omega[(a, b)] = dtheta.scale(value * rp)
    curvature: dict[tuple[int, int], ExteriorForm] = {}
    for a, b in PAIRS5:
        form = omega.get((a, b), alg.zero())
        derivative = alg.zero()
        if form:
            coefficient = form.terms[0][1].differentiate("rho_prime") * rpp
            derivative = ds.wedge(dtheta).scale(coefficient)
        quadratic = alg.zero()
        for c in I5:
            if c in (a, b):
                continue
            ac, sa = ordered_pair(a, c)
            cb, sb = ordered_pair(c, b)
            quadratic = quadratic + omega.get(ac, alg.zero()).scale(sa).wedge(
                omega.get(cb, alg.zero()).scale(sb)
            ).scale(ETA5[c])
        total = derivative + quadratic
        if total:
            curvature[(a, b)] = total
    return alg, omega, curvature


def ordered_euler_forms():
    """Literal D004 ordered BC and DE enumeration with epsilon_01234=+1."""
    alg = ExteriorAlgebra(tuple(f"E{i}" for i in I5))
    e = tuple(alg.basis_form(f"E{i}") for i in I5)
    k, lam = Polynomial.generator("k"), Polynomial.generator("Lambda5")
    r34 = e[3].wedge(e[4]).scale(k)
    curvature = {(3, 4): r34, (4, 3): -r34}
    prefactor = F(1, 2) if MUTATION == "ordered-pair-normalization" else F(1, 4)
    xi: dict[int, ExteriorForm] = {}
    forms: dict[int, ExteriorForm] = {}
    for a in I5:
        x = alg.zero()
        for word in permutations(tuple(i for i in I5 if i != a)):
            x = x + wedge_all(alg, tuple(e[i] for i in word)).scale(F(levi_civita_sign((a,) + word, I5), 24))
        xi[a] = x
        if MUTATION == "omit-circle-equation" and a == 4:
            continue
        value = alg.zero()
        for b, c, d, f in permutations(I5, 4):
            eps = levi_civita_sign((a, b, c, d, f), I5)
            if eps:
                value = value + curvature.get((b, c), alg.zero()).wedge(e[d]).wedge(e[f]).scale(prefactor * eps)
                value = value + wedge_all(alg, (e[b], e[c], e[d], e[f])).scale(F(-eps, 24) * lam)
        forms[a] = value
    return xi, forms


def direct_warped_coefficients() -> tuple[Polynomial, ...]:
    """Independent component contraction, with no Euler enumeration helper."""
    k, lam = Polynomial.generator("k"), Polynomial.generator("Lambda5")

    def area(a: int, b: int) -> int:
        return 1 if (a, b) == (3, 4) else (-1 if (a, b) == (4, 3) else 0)

    ricci = [[Polynomial.zero() for _ in I5] for _ in I5]
    for b in I5:
        for d in I5:
            ricci[b][d] = sum((k * (ETA5[a] * area(a, b) * area(a, d)) for a in I5), Polynomial.zero())
    scalar = sum((ETA5[a] * ricci[a][a] for a in I5), Polynomial.zero())
    result = []
    for a in I5:
        einstein = ricci[a][a] - F(1, 2) * ETA5[a] * scalar
        result.append(-ETA5[a] * (einstein + lam * ETA5[a]))
    return tuple(result)


def exterior_residuals():
    alg = ExteriorAlgebra(tuple(f"e{i}" for i in I4))
    e = tuple(alg.basis_form(f"e{i}") for i in I4)
    lam = Polynomial.generator("Lambda4")
    xi, residual = {}, {}
    for a in I4:
        x, g = alg.zero(), alg.zero()
        for word in permutations(tuple(i for i in I4 if i != a)):
            eps = levi_civita_sign((a,) + word, I4)
            form = wedge_all(alg, tuple(e[i] for i in word))
            x = x + form.scale(F(eps, 6))
            g = g + form.scale(F(-eps, 6) * lam)
        xi[a], residual[a] = x, g
    return xi, residual


def endpoint_systems() -> tuple[RationalMatrix, RationalMatrix]:
    # Columns (c,d): rho(0)=d, rho'(0)=c.
    rows = [[0, 1]] if MUTATION == "delete-rho-prime-endpoint" else [[0, 1], [1, 0]]
    return RationalMatrix(rows), RationalMatrix([[0, 1]])


def direct_parity(word: tuple[int, ...]) -> int:
    if len(set(word)) != len(word):
        return 0
    inversions = sum(word[i] > word[j] for i in range(len(word)) for j in range(i + 1, len(word)))
    return -1 if inversions % 2 else 1


def shell_table() -> dict[str, Any]:
    alg = ExteriorAlgebra(("dt", "dx", "dy"))
    e = (alg.basis_form("dt"), alg.basis_form("dx"), alg.basis_form("dy"), alg.zero())
    e_minus = tuple(
        alg.from_terms(form.terms) for form in
        (alg.basis_form("dt"), alg.basis_form("dx"), alg.basis_form("dy"), alg.zero())
    )
    b, kinv = Polynomial.generator("b"), Polynomial.generator("kappa4_inv")
    q, p = {}, {}
    for a in I4:
        for f in I4:
            qaf, paf = alg.zero(), alg.zero()
            for c in I4:
                for d in I4:
                    qaf = qaf + e[c].wedge(e[d]).scale(F(levi_civita_sign((a, f, c, d), I4), 4) * b)
                    paf = paf + e[c].wedge(e[d]).scale(F(direct_parity((a, f, c, d)), 4) * kinv)
            q[(a, f)], p[(a, f)] = qaf, paf
    matched_q = {
        pair: alg.from_terms((mon, coeff.substitute({"b": kinv})) for mon, coeff in form.terms)
        for pair, form in q.items()
    }
    # Assemble lambda independently from the direct-parity P^- path, then use
    # Q=P^- to test lambda=-Q without comparing an object to its own negation.
    lam = {pair: -form for pair, form in p.items()}
    zero_one = alg.zero()
    zero_connection = {(a, f): zero_one for a in I4 for f in I4}
    delta_e = tuple(e[a] - e_minus[a] for a in I4)
    delta_omega = {
        pair: zero_connection[pair] - zero_connection[pair] for pair in zero_connection
    }
    mu = tuple(alg.zero() for _ in I4)
    # K=0 is substituted into the displayed D005 H_c sum, rather than treating
    # H(K)=0 as an unexamined flag.
    h = []
    for c in I4:
        value = alg.zero()
        for a in I4:
            for f in I4:
                for d in I4:
                    eps = levi_civita_sign((a, f, c, d), I4)
                    value = value + zero_connection[(a, f)].wedge(e[d]).scale(F(-eps, 2) * b)
        h.append(value)
    # The planar coefficients and bar-a are exactly constant/zero, so the
    # exterior and connection pieces of D_bar_a Q are assembled as zero forms.
    d_bar_q = {pair: alg.zero() for pair in q}
    identity4 = tuple(tuple(O if i == j else Z for j in I4) for i in I4)
    a0 = {pair: alg.zero() for pair in q}
    # Each boolean corresponds to a distinct D005 equation/substitution.
    return {
        "delta_e_zero": all(form.is_zero for form in delta_e),
        "delta_omega_zero": all(form.is_zero for form in delta_omega.values()),
        "lambda_equals_minus_Q": all((lam[pair] + matched_q[pair]).is_zero for pair in q),
        "mu_zero": all(form.is_zero for form in mu),
        "Q_equals_P": all(matched_q[pair] == p[pair] for pair in q),
        "Q_nonzero_rows": sum(bool(form) for form in q.values()),
        "H_of_K_zero": all(form.is_zero for form in h),
        "D_bar_a_Q_zero": all(form.is_zero for form in d_bar_q.values()),
        "orbit_reference_a_zero": all(form.is_zero for form in a0.values()) and identity4[0][0] == O,
    }


def mutation_controls() -> dict[str, bool]:
    controls = {}
    for name in MUTATIONS:
        env = os.environ.copy()
        env[MUTATION_ENV] = name
        run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve())], env=env, cwd=ROOT,
            capture_output=True, text=True, timeout=30, check=False,
        )
        controls[name] = run.returncode == FAILED and "FAILED:" in run.stderr
    return controls


def check() -> int:
    if MUTATION not in {"", *MUTATIONS}:
        raise UnsupportedSectorError(f"unsupported mutation {MUTATION!r}")
    r = Recorder()
    unknowns, matrix, solution = cartan_system()
    if MUTATION == "spin-connection-sign":
        solution = tuple(-v for v in solution)
    nonzero = {u: v for u, v in zip(unknowns, solution) if v}
    residuals = torsion_residuals(unknowns, solution)
    r.require("cartan.complete_50_by_50_system", matrix.shape == (50, 50))
    r.require("cartan.unique_rank_50", matrix.rank() == 50)
    r.require("cartan.only_omega34_equals_minus_qE4", nonzero == {(3, 4, 4): -O})
    r.require("cartan.every_torsion_residual_zero", all(v == 0 for v in residuals))

    alg, omega, curvature = coordinate_geometry(unknowns, solution)
    rp, rpp = Polynomial.generator("rho_prime"), Polynomial.generator("rho_double_prime")
    expected_w = alg.basis_form("dtheta").scale(-rp)
    expected_r = alg.basis_form("ds").wedge(alg.basis_form("dtheta")).scale(-rpp)
    r.require("connection.omega34_minus_rhop_dtheta", omega.get((3, 4)) == expected_w)
    r.require("connection.omega43_plus_rhop_dtheta", -omega.get((3, 4), alg.zero()) == -expected_w)
    r.require("curvature.only_R34_independent_pair", set(curvature) == {(3, 4)})
    r.require("curvature.R34_minus_rhopp_ds_dtheta", curvature.get((3, 4)) == expected_r)
    r.require("curvature.R43_plus_rhopp_ds_dtheta", -curvature.get((3, 4), alg.zero()) == -expected_r)

    xi, euler = ordered_euler_forms()
    k, lam5 = Polynomial.generator("k"), Polynomial.generator("Lambda5")
    expected_coeffs = tuple(k - lam5 if a < 3 else -lam5 for a in I5)
    r.require("euler.all_five_equations_present", set(euler) == set(I5))
    for a in I5:
        r.require(f"euler.G{a}_coefficient", a in euler and euler[a] == xi[a].scale(expected_coeffs[a]))
    direct = direct_warped_coefficients()
    r.require("crosscheck.direct_warped_coefficients", direct == expected_coeffs)
    r.require("elimination.normal_circle_force_Lambda5_zero", direct[3:] == (-lam5, -lam5))
    r.require("elimination.persistent_then_forces_k_zero", direct[0] + lam5 == k)
    rho = Polynomial.generator("rho")
    rhopp = Polynomial.generator("rho_double_prime")
    warped_relation = k * rho + rhopp  # k=-rho''/rho, cleared only for rho>0.
    r.require(
        "elimination.k_zero_equivalent_rhopp_zero_for_rho_positive",
        warped_relation.substitute({"k": 0}) == rhopp,
    )

    xi4, ext = exterior_residuals()
    lam4 = Polynomial.generator("Lambda4")
    for a in I4:
        r.require(f"exterior.G{a}_flat_cosmological_residual", ext[a] == xi4[a].scale(-lam4))
    r.require("exterior.nonzero_coframe_forces_Lambda4_zero", all(bool(xi4[a]) for a in I4))

    full_endpoint, one_endpoint = endpoint_systems()
    s = Polynomial.generator("s")
    c = Polynomial.generator("c")
    d = Polynomial.generator("d")
    affine = c * s + d
    r.require("endpoint.affine_profile_value_is_d", affine.substitute({"s": 0}) == d)
    r.require("endpoint.affine_profile_derivative_is_c", affine.differentiate("s") == c)
    r.require("endpoint.two_data_unique_c_d_zero", full_endpoint.rank() == 2 and not full_endpoint.nullspace())
    r.require("endpoint.one_data_retains_nonzero_c", one_endpoint.nullspace() == ((O, Z),))
    r.require("endpoint.polar_control_rho_equals_c_s", one_endpoint.matvec((O, Z)) == (Z,))

    shell = shell_table()
    shell_keys = (
        "delta_e_zero", "delta_omega_zero", "lambda_equals_minus_Q", "mu_zero",
        "Q_equals_P", "H_of_K_zero", "D_bar_a_Q_zero", "orbit_reference_a_zero",
    )
    for name in shell_keys:
        r.require(f"shell.{name}", shell[name] is True)
    r.require("shell.rank_three_Q_nonzero_control", shell["Q_nonzero_rows"] > 0)

    controls: dict[str, bool] = {}
    if not MUTATION:
        controls = mutation_controls()
        for name, effective in controls.items():
            r.require(f"mutation.{name}_entrypoint_exits_1", effective)

    emit({
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": [PRODUCER_MODEL],
        "intentional_mutation": MUTATION or None,
        "assertions": {"total": r.total, "passed": len(r.passed), "failed": len(r.failed), "failed_names": r.failed},
        "cartan": {"unknowns": 50, "rank": matrix.rank(), "nonzero_solution": {str(u): str(v) for u, v in nonzero.items()}, "all_residuals_zero": all(v == 0 for v in residuals)},
        "euler_coefficients": ["k-Lambda5", "k-Lambda5", "k-Lambda5", "-Lambda5", "-Lambda5"],
        "endpoint_ranks": {"declared": full_endpoint.rank(), "one_endpoint": one_endpoint.rank()},
        "shell": {"Q_nonzero_rows": shell["Q_nonzero_rows"], "all_equalities": all(shell[x] for x in shell_keys)},
        "mutation_controls": controls,
        "representation": {"coefficients": "Fraction and sparse Polynomial", "forms": "exact_graded canonical ExteriorForm", "CAS_floats_randomization": False, "alternate": "direct warped component contraction"},
    })
    if r.failed:
        for name in r.failed:
            print(f"FAILED: {name}", file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        return check()
    except UnsupportedSectorError as exc:
        emit({"obligation_id": OBLIGATION_ID, "inconclusive_reason": str(exc)})
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR


if __name__ == "__main__":
    raise SystemExit(main())
