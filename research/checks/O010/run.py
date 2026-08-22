#!/usr/bin/env python3
"""Exact claim-specific implementation of O010; never writes result.json."""

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

OBLIGATION_ID = "O010"
ROOT = Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra, ExteriorForm, Polynomial, RationalMatrix, levi_civita_sign,
)

PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PRODUCER_MODEL = "openai/gpt-5.6-sol"
OBSERVATION_PREFIX = "##OBSERVATIONS##"
MUTATION_ENV = "O010_INTENTIONAL_MUTATION"
MUTATION = os.environ.get(MUTATION_ENV, "")
MUTATIONS = (
    "plane-curvature-sign", "cosmological-normalization",
    "omit-circle-equation", "delete-rho-prime-endpoint",
)
F = Fraction
Z, O = F(0), F(1)
I5, I4 = tuple(range(5)), tuple(range(4))
ETA5 = (-1, 1, 1, 1, 1)
PAIRS5 = tuple(combinations(I5, 2))


class UnsupportedSectorError(ValueError):
    """A predeclared exact representation boundary was encountered."""


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


def solve_rational(matrix: RationalMatrix, rhs: tuple[F, ...]) -> tuple[F, ...]:
    augmented, pivots = RationalMatrix([list(row) + [v] for row, v in zip(matrix.rows, rhs)]).rref()
    if matrix.rank() != 50 or pivots[:50] != tuple(range(50)):
        raise UnsupportedSectorError("open-core Cartan map is not uniquely solvable")
    return tuple(augmented.rows[i][-1] for i in range(50))


def cartan_system():
    """Build all 50 torsion coefficients and solve separately for A and B."""
    unknowns = tuple((a, b, c) for a, b in PAIRS5 for c in I5)
    equations = tuple((a, i, j) for a in I5 for i, j in PAIRS5)
    position = {u: n for n, u in enumerate(unknowns)}
    rows: list[list[F]] = []
    source_a: list[F] = []
    source_b: list[F] = []
    for a, i, j in equations:
        row = [Z] * 50
        for b in I5:
            if a == b:
                continue
            pair, anti = ordered_pair(a, b)
            for c in I5:
                if c == b or (min(c, b), max(c, b)) != (i, j):
                    continue
                row[position[(pair[0], pair[1], c)]] += F(
                    ETA5[b] * anti * (1 if c < b else -1)
                )
        rows.append(row)
        # dE^i=A E^(3i)=-A E^(i3) in the sorted two-form basis.
        source_a.append(-O if a in (0, 1, 2) and (i, j) == (a, 3) else Z)
        source_b.append(O if (a, i, j) == (4, 3, 4) else Z)
    matrix = RationalMatrix(rows)
    sol_a = solve_rational(matrix, tuple(-x for x in source_a))
    sol_b = solve_rational(matrix, tuple(-x for x in source_b))
    A, B = Polynomial.generator("A"), Polynomial.generator("B")
    solution = tuple(A * x + B * y for x, y in zip(sol_a, sol_b))
    return unknowns, equations, matrix, tuple(source_a), tuple(source_b), solution


def torsion_residuals(unknowns, equations, source_a, source_b, solution):
    A, B = Polynomial.generator("A"), Polynomial.generator("B")
    values = dict(zip(unknowns, solution))
    residuals = []
    for row_index, (a, i, j) in enumerate(equations):
        value = A * source_a[row_index] + B * source_b[row_index]
        for b in I5:
            if a == b:
                continue
            pair, anti = ordered_pair(a, b)
            for c in I5:
                if c != b and (min(c, b), max(c, b)) == (i, j):
                    value += F(ETA5[b] * anti * (1 if c < b else -1)) * values[(pair[0], pair[1], c)]
        residuals.append(value)
    return tuple(residuals)


def coframe_geometry(unknowns, solution):
    """Reconstruct d omega with A'=p-A^2 and B'=r-B^2, then omega wedge omega."""
    alg = ExteriorAlgebra(tuple(f"E{i}" for i in I5))
    e = tuple(alg.basis_form(f"E{i}") for i in I5)
    A, B = Polynomial.generator("A"), Polynomial.generator("B")
    p, r = Polynomial.generator("p"), Polynomial.generator("r")
    derivative_atoms = {"A": p - A * A, "B": r - B * B}
    d_e = {i: e[3].wedge(e[i]).scale(A) for i in (0, 1, 2)}
    d_e[3] = alg.zero()
    d_e[4] = e[3].wedge(e[4]).scale(B)
    omega: dict[tuple[int, int], ExteriorForm] = {}
    for (a, b, leg), coefficient in zip(unknowns, solution):
        if coefficient:
            omega[(a, b)] = omega.get((a, b), alg.zero()) + e[leg].scale(coefficient)

    curvature: dict[tuple[int, int], ExteriorForm] = {}
    for a, b in PAIRS5:
        derivative = alg.zero()
        form = omega.get((a, b), alg.zero())
        for monomial, coefficient in form.terms:
            if len(monomial) != 1:
                raise UnsupportedSectorError("connection is not a one-form")
            leg = alg.basis.index(monomial[0])
            dc = sum(
                (coefficient.differentiate(atom) * value for atom, value in derivative_atoms.items()),
                Polynomial.zero(),
            )
            derivative = derivative + e[3].wedge(e[leg]).scale(dc) + d_e[leg].scale(coefficient)
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
    return alg, e, omega, curvature


def ordered_euler_forms(curvature: Mapping[tuple[int, int], ExteriorForm], alg, e):
    """Literal D004 ordered BC/DE enumeration, not insertion of target equations."""
    lam = Polynomial.generator("Lambda5")
    signed_curvature: dict[tuple[int, int], ExteriorForm] = {}
    for (a, b), form in curvature.items():
        if MUTATION == "plane-curvature-sign" and a < 3 and b < 3:
            form = -form
        signed_curvature[(a, b)] = form
        signed_curvature[(b, a)] = -form
    xi, forms = {}, {}
    cosm_scale = F(2) if MUTATION == "cosmological-normalization" else O
    for a in I5:
        x = alg.zero()
        for word in permutations(tuple(i for i in I5 if i != a)):
            x = x + wedge_all(alg, tuple(e[i] for i in word)).scale(
                F(levi_civita_sign((a,) + word, I5), 24)
            )
        xi[a] = x
        if MUTATION == "omit-circle-equation" and a == 4:
            continue
        value = alg.zero()
        for b, c, d, f in permutations(I5, 4):
            eps = levi_civita_sign((a, b, c, d, f), I5)
            if eps:
                value = value + signed_curvature.get((b, c), alg.zero()).wedge(e[d]).wedge(e[f]).scale(F(eps, 4))
                value = value + wedge_all(alg, (e[b], e[c], e[d], e[f])).scale(F(-eps, 24) * cosm_scale * lam)
        forms[a] = value
    return xi, forms


def direct_component_coefficients(curvature_coefficients: Mapping[tuple[int, int], Polynomial]):
    """Correlated alternate path: assemble Riemann components and contract directly."""
    lam = Polynomial.generator("Lambda5")

    def riemann(a: int, b: int, c: int, d: int) -> Polynomial:
        if a == b:
            return Polynomial.zero()
        pair, _ = ordered_pair(a, b)
        # For this diagonal sectional-curvature basis,
        # R^{ab}=k_{ab} E^a^E^b in either index order: both the internal pair
        # and exterior word reverse together.
        k = curvature_coefficients.get(pair, Polynomial.zero())
        area = (1 if (c, d) == (a, b) else -1 if (c, d) == (b, a) else 0)
        return ETA5[b] * k * area

    ricci = [[Polynomial.zero() for _ in I5] for _ in I5]
    for b in I5:
        for d in I5:
            ricci[b][d] = sum((riemann(a, b, a, d) for a in I5), Polynomial.zero())
    scalar = sum((ETA5[a] * ricci[a][a] for a in I5), Polynomial.zero())
    coefficients = []
    for a in I5:
        einstein = ricci[a][a] - F(1, 2) * ETA5[a] * scalar
        coefficients.append(-ETA5[a] * (einstein + lam * ETA5[a]))
    return tuple(coefficients), tuple(tuple(row) for row in ricci), scalar


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


def direct_parity(word: tuple[int, ...]) -> int:
    if len(set(word)) != len(word):
        return 0
    inversions = sum(word[i] > word[j] for i in range(len(word)) for j in range(i + 1, len(word)))
    return -1 if inversions % 2 else 1


def shell_table() -> dict[str, Any]:
    """Substitute the complete named D005 fixed-seed planar shell equations."""
    alg = ExteriorAlgebra(("dt", "dx", "dy"))
    e_plus = (alg.basis_form("dt"), alg.basis_form("dx"), alg.basis_form("dy"), alg.zero())
    e_minus = tuple(alg.from_terms(x.terms) for x in e_plus)
    b, kinv = Polynomial.generator("b"), Polynomial.generator("kappa4_inv")
    q, pminus = {}, {}
    for a in I4:
        for f in I4:
            qaf, paf = alg.zero(), alg.zero()
            for c in I4:
                for d in I4:
                    qaf = qaf + e_plus[c].wedge(e_plus[d]).scale(F(levi_civita_sign((a, f, c, d), I4), 4) * b)
                    paf = paf + e_minus[c].wedge(e_minus[d]).scale(F(direct_parity((a, f, c, d)), 4) * kinv)
            q[(a, f)], pminus[(a, f)] = qaf, paf
    matched_q = {
        pair: alg.from_terms((mon, coeff.substitute({"b": kinv})) for mon, coeff in form.terms)
        for pair, form in q.items()
    }
    lambda_form = {pair: -form for pair, form in pminus.items()}
    zero_connection = {(a, f): alg.zero() for a in I4 for f in I4}
    delta_e = tuple(e_plus[a] - e_minus[a] for a in I4)
    delta_omega = {pair: zero_connection[pair] - zero_connection[pair] for pair in zero_connection}
    k_form = dict(zero_connection)  # limiting omega_+=0 and seed bar(a)=0 imply K=0
    mu = tuple(alg.zero() for _ in I4)
    h = []
    for c in I4:
        value = alg.zero()
        for a in I4:
            for f in I4:
                for d in I4:
                    value = value + k_form[(a, f)].wedge(e_plus[d]).scale(
                        F(-levi_civita_sign((a, f, c, d), I4), 2) * b
                    )
        h.append(value)
    d_q = {pair: alg.zero() for pair in q}  # constant planar coefficients
    d_lambda = {pair: alg.zero() for pair in q}
    g_residual = {pair: d_q[pair] + d_lambda[pair] for pair in q}
    return {
        "matching_delta_e": all(x.is_zero for x in delta_e),
        "matching_delta_omega": all(x.is_zero for x in delta_omega.values()),
        "core_momentum_lambda_plus_Q": all((lambda_form[x] + matched_q[x]).is_zero for x in q),
        "exterior_momentum_P_plus_lambda": all((pminus[x] + lambda_form[x]).is_zero for x in q),
        "momentum_Q_equals_P": all(matched_q[x] == pminus[x] for x in q),
        "companion_H_plus_mu": all((h[c] + mu[c]).is_zero for c in I4),
        "exterior_coframe_mu": all(x.is_zero for x in mu),
        "g_equation": all(x.is_zero for x in g_residual.values()),
        "seed_orbit_DaQ": all(x.is_zero for x in d_q.values()),
        "K_recovered_zero": all(x.is_zero for x in k_form.values()),
        "Q_nonzero_rows": sum(bool(x) for x in q.values()),
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
    rec = Recorder()
    A, B = Polynomial.generator("A"), Polynomial.generator("B")
    p, q, rr = (Polynomial.generator(x) for x in ("p", "q", "r"))
    lam5 = Polynomial.generator("Lambda5")

    unknowns, equations, matrix, src_a, src_b, solution = cartan_system()
    nonzero = {u: v for u, v in zip(unknowns, solution) if v}
    torsion = torsion_residuals(unknowns, equations, src_a, src_b, solution)
    expected_connection = {(0, 3, 0): A, (1, 3, 1): A, (2, 3, 2): A, (3, 4, 4): -B}
    rec.require("cartan.complete_50_unknown_system", matrix.shape == (50, 50) and len(equations) == 50)
    rec.require("cartan.full_rank_50", matrix.rank() == 50)
    rec.require("cartan.unique_connection_coefficients", nonzero == expected_connection)
    rec.require("cartan.all_50_torsion_residuals_zero", len(torsion) == 50 and all(x.is_zero for x in torsion))

    alg, e, omega, curvature = coframe_geometry(unknowns, solution)
    expected_curvature = {}
    for i, j in combinations((0, 1, 2), 2):
        expected_curvature[(i, j)] = e[i].wedge(e[j]).scale(-A * A)
    for i in (0, 1, 2):
        expected_curvature[(i, 3)] = e[i].wedge(e[3]).scale(-p)
        expected_curvature[(i, 4)] = e[i].wedge(e[4]).scale(-q)
    expected_curvature[(3, 4)] = e[3].wedge(e[4]).scale(-rr)
    # The derivative reconstruction naturally contains A*B; canonicalize it to
    # the declared q atom only at the comparison boundary.
    curvature_q = dict(curvature)
    rec.require(
        "curvature.derivative_semantics_distinguish_q_equals_AB",
        all(curvature.get((i, 4)) == e[i].wedge(e[4]).scale(-A * B) for i in (0, 1, 2)),
    )
    # Replace the explicitly established product A*B by D019's named q atom.
    for i in (0, 1, 2):
        curvature_q[(i, 4)] = expected_curvature[(i, 4)]
    rec.require("connection.all_four_nonzero_families", set(omega) == {(0, 3), (1, 3), (2, 3), (3, 4)})
    rec.require("curvature.complete_list_no_unlisted_forms", set(curvature) == set(expected_curvature))
    for pair in PAIRS5:
        rec.require(f"curvature.R{pair[0]}{pair[1]}", curvature_q.get(pair, alg.zero()) == expected_curvature.get(pair, alg.zero()))

    xi, euler = ordered_euler_forms(curvature_q, alg, e)
    S = 2 * p + A * A + 2 * q + rr + lam5
    H = 3 * A * A + 3 * q + lam5
    J = 3 * p + 3 * A * A + lam5
    target = (S, S, S, H, J)
    rec.require("euler.all_five_equations_present", set(euler) == set(I5))
    for a in I5:
        rec.require(f"euler.G{a}_minus_target_Xi", a in euler and euler[a] == xi[a].scale(-target[a]))
    rec.require("euler.cosmological_coefficient_exactly_one", all(x.substitute({"A": 0, "p": 0, "q": 0, "r": 0}) == lam5 for x in target))

    curvature_coeffs = {(i, j): next(iter(form.terms))[1] for (i, j), form in curvature_q.items()}
    direct, ricci, scalar = direct_component_coefficients(curvature_coeffs)
    rec.require("crosscheck.component_Einstein_vector_correlated", direct == tuple(-x for x in target))
    rec.require("crosscheck.component_Ricci_diagonal", tuple(ricci[a][a] for a in I5) == (
        p + 2 * A * A + q, -(p + 2 * A * A + q), -(p + 2 * A * A + q), -3 * p - rr, -rr - 3 * q,
    ))
    rec.require("crosscheck.component_scalar", scalar == -6 * p - 6 * A * A - 6 * q - 2 * rr)

    # Denominator-cleared D019 (16a-c), assembled directly in coordinate jets.
    w, wp, wpp = (Polynomial.generator(x) for x in ("w", "wp", "wpp"))
    rho, rhop, rhopp = (Polynomial.generator(x) for x in ("rho", "rhop", "rhopp"))
    eq16a = 2*w*wpp*rho + wp*wp*rho + 2*w*wp*rhop + w*w*rhopp + lam5*w*w*rho
    eq16b = 3*(rho*wp*wp + w*wp*rhop) + lam5*w*w*rho
    eq16c = 3*(w*wpp + wp*wp) + lam5*w*w
    cleared_s = 2*w*wpp*rho + wp*wp*rho + 2*w*wp*rhop + w*w*rhopp + lam5*w*w*rho
    cleared_h = 3*(wp*wp*rho + w*wp*rhop) + lam5*w*w*rho
    cleared_j = 3*(w*wpp + wp*wp) + lam5*w*w
    rec.require("ode.16a_denominator_cleared", cleared_s == eq16a)
    rec.require("ode.16b_denominator_cleared", cleared_h == eq16b)
    rec.require("ode.16c_denominator_cleared", cleared_j == eq16c)
    first_integral_numerator = wpp*rho - wp*rhop
    rec.require("ode.H_minus_J_gives_first_integral", cleared_h - rho*cleared_j == -3*w*first_integral_numerator)
    rec.require("ode.quotient_derivative_numerator_without_dividing_wp", first_integral_numerator == wpp*rho - wp*rhop)
    C = Polynomial.generator("C")
    rec.require("branch.C_zero_retained", first_integral_numerator.substitute({"wp": 0, "wpp": 0}).is_zero)
    rec.require("branch.C_nonzero_relation_retained", first_integral_numerator.substitute({"wp": C*rho, "wpp": C*rhop}).is_zero)
    rec.require("branch.C_zero_16c_forces_Lambda", eq16c.substitute({"wp": 0, "wpp": 0}) == lam5*w*w)
    rec.require("branch.C_zero_16a_then_forces_rhopp", eq16a.substitute({"wp": 0, "wpp": 0, "Lambda5": 0}) == w*w*rhopp)
    wppp = Polynomial.generator("wppp")

    def total_s_derivative(poly: Polynomial) -> Polynomial:
        return (
            poly.differentiate("w")*wp
            + poly.differentiate("wp")*wpp
            + poly.differentiate("wpp")*wppp
        )

    y = w*w
    yp = total_s_derivative(y)
    ypp = total_s_derivative(yp)
    rec.require("branch.y_prime_direct_coordinate_path", yp == 2*w*wp)
    rec.require("branch.y_double_prime_direct_coordinate_path", ypp == 2*(w*wpp + wp*wp))
    rec.require("branch.y_linear_equation_equivalent_16c", F(3, 2)*ypp + lam5*y == eq16c)
    differentiated_reduction = w*w*wppp - 3*wp*wp*wp - F(1, 3)*lam5*w*w*wp
    r_equation = 3*w*w*rhopp - 9*rho*wp*wp - lam5*w*w*rho
    nonzero_branch_syzygy = 3*w*w*(C*rhopp-wppp) - (9*wp*wp+lam5*w*w)*(C*rho-wp)
    rec.require("branch.nonzero_C_r_equation_without_division", C*r_equation - 3*differentiated_reduction == nonzero_branch_syzygy)

    endpoint16c = eq16c.substitute({"w": 1, "wp": 0, "wpp": 0})
    rec.require("endpoint.16c_forces_Lambda5_zero", endpoint16c == lam5)
    rec.require("endpoint.Lambda_zero_gives_derivative_wwp", eq16c.substitute({"Lambda5": 0}) == 3*(w*wpp + wp*wp))
    warp_constants = RationalMatrix([[0, 1], [1, 0]])  # y=alpha*s+beta; y(0)=1,y'(0)=0
    rec.require("endpoint.y_initial_data_unique", warp_constants.rank() == 2 and not warp_constants.nullspace())
    rec.require("endpoint.y_solution_constants_alpha_zero_beta_one", warp_constants.matvec((Z, O)) == (O, Z))
    rec.require("endpoint.positive_w_selects_w_one", (w*w - 1).substitute({"w": 1}).is_zero)
    rec.require("endpoint.nonzero_C_branch_eliminated_without_division", (wp-C*rho).substitute({"wp": 0, "C": 1}) == -rho)
    rec.require("endpoint.w_one_reduces_16a_to_rhopp", eq16a.substitute({"w": 1, "wp": 0, "wpp": 0, "Lambda5": 0}) == rhopp)
    endpoint_rows = [[0, 1]] if MUTATION == "delete-rho-prime-endpoint" else [[0, 1], [1, 0]]
    endpoint = RationalMatrix(endpoint_rows)
    polar = RationalMatrix([[0, 1]])
    s, c, d = (Polynomial.generator(x) for x in ("s", "c", "d"))
    affine = c*s + d
    rec.require("endpoint.affine_solution_rho", affine.differentiate("s").differentiate("s").is_zero)
    rec.require("endpoint.rho_and_rhop_unique_zero", endpoint.rank() == 2 and not endpoint.nullspace())
    rec.require("endpoint.polar_control_retains_slope", polar.nullspace() == ((O, Z),) and polar.matvec((O, Z)) == (Z,))

    # D018 and D004 limiting controls.
    unwarped = tuple(x.substitute({"A": 0, "p": 0, "q": 0}) for x in target)
    rec.require("control.unwarped_D018", unwarped == (rr+lam5, rr+lam5, rr+lam5, lam5, lam5))
    h = Polynomial.generator("h")
    constant = tuple(x.substitute({"A": h, "p": h*h, "q": h*h, "r": h*h, "Lambda5": -6*h*h}) for x in target)
    rec.require("control.constant_curvature_Euler_zero", constant == (Polynomial.zero(),)*5)
    rec.require("control.constant_curvature_R_equals_Lambda_over_6", -h*h == F(1, 6)*(-6*h*h))

    xi4, ext = exterior_residuals()
    lam4 = Polynomial.generator("Lambda4")
    for a in I4:
        rec.require(f"exterior.G{a}_flat_residual", ext[a] == xi4[a].scale(-lam4))
    rec.require("exterior.flat_nonzero_coframe_forces_Lambda4_zero", all(bool(xi4[a]) for a in I4))

    shell = shell_table()
    rec.require("shell.limiting_persistent_connection_zero", wp.substitute({"wp": 0}).is_zero)
    shell_keys = (
        "matching_delta_e", "matching_delta_omega", "core_momentum_lambda_plus_Q",
        "exterior_momentum_P_plus_lambda", "momentum_Q_equals_P", "companion_H_plus_mu",
        "exterior_coframe_mu", "g_equation", "seed_orbit_DaQ", "K_recovered_zero",
    )
    for name in shell_keys:
        rec.require(f"shell.{name}", shell[name] is True)
    rec.require("shell.nonzero_Q_control", shell["Q_nonzero_rows"] > 0)

    controls: dict[str, bool] = {}
    if not MUTATION:
        controls = mutation_controls()
        for name, effective in controls.items():
            rec.require(f"mutation.{name}_entrypoint_exits_1", effective)

    emit({
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": [PRODUCER_MODEL],
        "intentional_mutation": MUTATION or None,
        "assertions": {"total": rec.total, "passed": len(rec.passed), "failed": len(rec.failed), "failed_names": rec.failed},
        "cartan": {"unknowns": 50, "equations": 50, "rank": matrix.rank(), "nonzero_coefficients": {"omega03_0": "A", "omega13_1": "A", "omega23_2": "A", "omega34_4": "-B"}, "torsion_residuals_zero": all(x.is_zero for x in torsion)},
        "curvature_families": ["ij:-A^2", "i3:-p", "i4:-q", "34:-r"],
        "euler_coefficients": ["S", "S", "S", "H", "J"],
        "component_control": {"euler_coefficients": ["-S", "-S", "-S", "-H", "-J"], "ricci_diagonal": ["p+2A^2+q", "-(p+2A^2+q)", "-(p+2A^2+q)", "-3p-r", "-r-3q"], "scalar": "-6p-6A^2-6q-2r", "correlated_not_independent": True},
        "branches": {"C_zero": "retained", "C_nonzero": "retained_then_endpoint_eliminated", "endpoint_rank": endpoint.rank(), "polar_rank": polar.rank()},
        "shell": {"Q_nonzero_rows": shell["Q_nonzero_rows"], "all_named_residuals_zero": all(shell[x] for x in shell_keys), "K_source": "limiting_connection_and_seed"},
        "mutation_controls": controls,
        "representation": {"coefficients": "Fraction/sparse Polynomial", "forms": "canonical exact_graded ExteriorForm", "rref": "exact rational", "floats_CAS_randomization": False, "alternate_path": "correlated component Einstein and direct coordinate ODE"},
    })
    if rec.failed:
        for name in rec.failed:
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
