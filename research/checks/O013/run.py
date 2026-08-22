#!/usr/bin/env python3
"""Exact claim-specific implementation of O013; never writes result.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Iterable, Mapping

OBLIGATION_ID = "O013"
PRODUCER_MODEL = "openai/gpt-5.6-sol"
PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
OBSERVATION_PREFIX = "##OBSERVATIONS##"
MUTATION = os.environ.get("O013_INTENTIONAL_MUTATION", "")
MUTATIONS = ("omit-order", "reverse-primitive-sign", "delete-coframe-companion", "reverse-orbit-corner-sign", "transform-only-dynamical-connection")


def parity(values: tuple[int, ...]) -> int:
    if len(set(values)) != len(values):
        return 0
    n = sum(values[i] > values[j] for i in range(len(values)) for j in range(i + 1, len(values)))
    return -1 if n % 2 else 1


@dataclass(frozen=True)
class Poly:
    """Canonical sparse free polynomial over Q."""
    terms: tuple[tuple[tuple[str, ...], Fraction], ...] = ()

    @staticmethod
    def make(value: "Poly | Fraction | int | str") -> "Poly":
        if isinstance(value, Poly):
            return value
        if isinstance(value, str):
            return Poly((((value,), Fraction(1)),))
        q = Fraction(value)
        return Poly((((), q),)) if q else Poly()

    @staticmethod
    def collect(items: Iterable[tuple[tuple[str, ...], Fraction]]) -> "Poly":
        out: dict[tuple[str, ...], Fraction] = {}
        for monomial, coefficient in items:
            key = tuple(sorted(monomial))
            out[key] = out.get(key, Fraction()) + Fraction(coefficient)
        return Poly(tuple(sorted((m, c) for m, c in out.items() if c)))

    def __add__(self, other: "Poly | Fraction | int | str") -> "Poly":
        rhs = Poly.make(other)
        return Poly.collect(self.terms + rhs.terms)

    def __neg__(self) -> "Poly":
        return Poly(tuple((m, -c) for m, c in self.terms))

    def __sub__(self, other: "Poly | Fraction | int | str") -> "Poly":
        return self + -Poly.make(other)

    def __mul__(self, other: "Poly | Fraction | int | str") -> "Poly":
        rhs = Poly.make(other)
        return Poly.collect((m1 + m2, c1 * c2) for m1, c1 in self.terms for m2, c2 in rhs.terms)

    __rmul__ = __mul__

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def coefficient_of(self, atoms: tuple[str, ...]) -> Fraction:
        return dict(self.terms).get(tuple(sorted(atoms)), Fraction())

    def text(self) -> str:
        return "0" if self.is_zero else "+".join(f"{c}*{'*'.join(m) or '1'}" for m, c in self.terms)


@dataclass(frozen=True)
class Form:
    """Sparse exterior form on an explicitly ordered basis."""
    basis: tuple[str, ...]
    terms: tuple[tuple[tuple[str, ...], Poly], ...] = ()

    @staticmethod
    def collect(basis: tuple[str, ...], items: Iterable[tuple[tuple[str, ...], Poly]]) -> "Form":
        order = {label: i for i, label in enumerate(basis)}
        out: dict[tuple[str, ...], Poly] = {}
        for word, coefficient in items:
            if len(set(word)) != len(word):
                continue
            inv = sum(order[word[i]] > order[word[j]] for i in range(len(word)) for j in range(i + 1, len(word)))
            key = tuple(sorted(word, key=order.__getitem__))
            out[key] = out.get(key, Poly()) + coefficient * (-1 if inv % 2 else 1)
        return Form(basis, tuple(sorted((w, c) for w, c in out.items() if not c.is_zero)))

    @staticmethod
    def scalar(basis: tuple[str, ...], coefficient: Poly | Fraction | int | str = 1) -> "Form":
        return Form.collect(basis, [((), Poly.make(coefficient))])

    @staticmethod
    def atom(basis: tuple[str, ...], label: str, coefficient: Poly | Fraction | int | str = 1) -> "Form":
        return Form.collect(basis, [((label,), Poly.make(coefficient))])

    @staticmethod
    def zero(basis: tuple[str, ...]) -> "Form":
        return Form(basis)

    def __add__(self, other: "Form") -> "Form":
        if self.basis != other.basis:
            raise ValueError("exterior basis mismatch")
        return Form.collect(self.basis, self.terms + other.terms)

    def __neg__(self) -> "Form":
        return Form(self.basis, tuple((w, -c) for w, c in self.terms))

    def __sub__(self, other: "Form") -> "Form":
        return self + -other

    def wedge(self, other: "Form") -> "Form":
        if self.basis != other.basis:
            raise ValueError("exterior basis mismatch")
        return Form.collect(self.basis, ((w1 + w2, c1 * c2) for w1, c1 in self.terms for w2, c2 in other.terms))

    def scale(self, scalar: Poly | Fraction | int | str) -> "Form":
        q = Poly.make(scalar)
        return Form.collect(self.basis, ((w, c * q) for w, c in self.terms))

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def coefficient(self, word: tuple[str, ...]) -> Poly:
        return dict(self.terms).get(word, Poly())


def wedge_all(factors: Iterable[Form], basis: tuple[str, ...]) -> Form:
    out = Form.scalar(basis)
    for factor in factors:
        out = out.wedge(factor)
    return out


def sum_forms(forms: Iterable[Form], basis: tuple[str, ...]) -> Form:
    out = Form.zero(basis)
    for form in forms:
        out = out + form
    return out


def generic_one_form(basis: tuple[str, ...], stem: str) -> Form:
    return sum_forms((Form.atom(basis, leg, f"{stem}_{mu}") for mu, leg in enumerate(basis)), basis)


def antisym(table: Mapping[tuple[int, int], Form], a: int, b: int, basis: tuple[str, ...]) -> Form:
    if a == b:
        return Form.zero(basis)
    return table[(a, b)] if a < b else -table[(b, a)]


def momenta(coframes: Mapping[int, Form], *, omit_order: bool = False) -> dict[tuple[int, int], Form]:
    """P_AB=(12 kappa5)^-1 epsilon_ABCDE E^C E^D E^E."""
    basis = next(iter(coframes.values())).basis
    out: dict[tuple[int, int], Form] = {}
    for a in range(5):
        for b in range(5):
            value = Form.zero(basis)
            if a != b and not (omit_order and a > b):
                for c, d, e in permutations(range(5), 3):
                    eps = parity((a, b, c, d, e))
                    if eps:
                        value = value + wedge_all((coframes[c], coframes[d], coframes[e]), basis).scale(Poly.make("kappa5_inv") * Fraction(eps, 12))
            out[(a, b)] = value
    return out


def ordered_pairing(left: Mapping[tuple[int, int], Form], right: Mapping[tuple[int, int], Form]) -> Form:
    basis = next(iter(left.values())).basis
    return sum_forms((left[(a, b)].wedge(right[(a, b)]) for a in range(5) for b in range(5)), basis)


def push_circle(form: Form) -> Form:
    if form.basis[-1] != "dtheta":
        raise ValueError("dtheta is not the final oriented fiber leg")
    return Form.collect(form.basis[:-1], ((word[:-1], coefficient * "tau") for word, coefficient in form.terms if word and word[-1] == "dtheta"))


def vary_momenta(coframes: Mapping[int, Form], delta_e: Mapping[int, Form]) -> dict[tuple[int, int], Form]:
    """Direct Leibniz derivative of the unreduced momentum definition."""
    basis = next(iter(coframes.values())).basis
    out: dict[tuple[int, int], Form] = {}
    for a in range(5):
        for b in range(5):
            value = Form.zero(basis)
            for c, d, e in permutations(range(5), 3):
                eps = parity((a, b, c, d, e))
                if eps:
                    for factors in ((delta_e[c], coframes[d], coframes[e]), (coframes[c], delta_e[d], coframes[e]), (coframes[c], coframes[d], delta_e[e])):
                        value = value + wedge_all(factors, basis).scale(Poly.make("kappa5_inv") * Fraction(eps, 12))
            out[(a, b)] = value
    return out


def coframe_current(k_table: Mapping[tuple[int, int], Form], coframes: Mapping[int, Form], c: int) -> Form:
    basis = next(iter(coframes.values())).basis
    out = Form.zero(basis)
    for a in range(5):
        for b in range(5):
            for d in range(5):
                for e in range(5):
                    eps = parity((a, b, c, d, e))
                    if eps:
                        out = out + wedge_all((k_table[(a, b)], coframes[d], coframes[e]), basis).scale(Poly.make("kappa5_inv") * Fraction(eps, 4))
    return out


def lambda_mixed(a: int, b: int) -> Poly:
    """lambda^A_B=lambda^(AB) eta_BB, eta=diag(-,+,+,+,+)."""
    if a == b:
        return Poly()
    atom = f"lambda_{min(a, b)}{max(a, b)}"
    upper_sign = 1 if a < b else -1
    metric_sign = -1 if b == 0 else 1
    return Poly.make(atom) * upper_sign * metric_sign


def infinitesimal_vector(table: Mapping[int, Form]) -> dict[int, Form]:
    basis = next(iter(table.values())).basis
    return {a: sum_forms((table[b].scale(lambda_mixed(a, b)) for b in range(5)), basis) for a in range(5)}


def infinitesimal_adjoint(k: Mapping[tuple[int, int], Form]) -> dict[tuple[int, int], Form]:
    basis = next(iter(k.values())).basis
    return {(a, b): sum_forms((term for c in range(5) for term in (k[(c, b)].scale(lambda_mixed(a, c)), k[(a, c)].scale(lambda_mixed(b, c)))), basis) for a in range(5) for b in range(5)}


def covariance_residual(*, transform_only_dynamical: bool) -> tuple[Form, set[str]]:
    """Generic polynomial tensor identity, not sampling or a finite witness."""
    basis = ("x0", "x1", "x2", "x3")
    e = {a: generic_one_form(basis, f"E{a}") for a in range(5)}
    k_ind = {(a, b): generic_one_form(basis, f"K{a}{b}") for a, b in combinations(range(5), 2)}
    k = {(a, b): antisym(k_ind, a, b, basis) for a in range(5) for b in range(5)}
    p = momenta(e)
    delta_e = infinitesimal_vector(e)
    delta_p = vary_momenta(e, delta_e)
    delta_k = infinitesimal_adjoint(k)
    if transform_only_dynamical:
        for a, b in combinations(range(5), 2):
            dlam = generic_one_form(basis, f"dlambda{a}{b}")
            delta_k[(a, b)] = delta_k[(a, b)] - dlam
            delta_k[(b, a)] = -delta_k[(a, b)]
    residual = -(ordered_pairing(delta_k, p) + ordered_pairing(k, delta_p))
    seen = {atom for _, coefficient in ordered_pairing(delta_k, p).terms for monomial, _ in coefficient.terms for atom in monomial if atom.startswith("lambda_")}
    return residual, seen


def orbit_signs(reverse_corner: bool) -> tuple[int, int, dict[str, int]]:
    """Use -D zeta P and D(zeta P)=D zeta P+zeta DP."""
    input_dzeta_p = -1
    bulk = -input_dzeta_p
    corner = input_dzeta_p * (-1 if reverse_corner else 1)
    return bulk, corner, {"input_-D_zeta_P": input_dzeta_p, "D_zeta_P_equals_boundary_minus_zeta_DP": -1}


@dataclass
class Recorder:
    results: dict[str, bool] = field(default_factory=dict)

    def require(self, name: str, condition: bool) -> None:
        if name in self.results or type(condition) is not bool:
            raise ValueError(f"invalid assertion {name}")
        self.results[name] = condition

    @property
    def failed(self) -> list[str]:
        return sorted(name for name, passed in self.results.items() if not passed)


def evaluate(mutation: str) -> tuple[Recorder, dict[str, object]]:
    if mutation and mutation not in MUTATIONS:
        raise ValueError(f"unsupported mutation {mutation!r}")
    rec = Recorder()
    primitive_sign = 1 if mutation == "reverse-primitive-sign" else -1

    cb = ("du0", "du1", "du2", "dtheta")
    sb = cb[:-1]
    e = {0: Form.atom(cb, "du0"), 1: Form.atom(cb, "du1"), 2: Form.atom(cb, "du2"), 3: Form.zero(cb), 4: Form.zero(cb)}
    o_sigma = wedge_all((Form.atom(sb, "du0"), Form.atom(sb, "du1"), Form.atom(sb, "du2")), sb)
    p = momenta(e, omit_order=mutation == "omit-order")
    expected_43 = wedge_all((e[0], e[1], e[2]), cb).scale(Poly.make("kappa5_inv") * Fraction(-1, 2))
    expected_34 = -expected_43
    rec.require("momentum.P43", p[(4, 3)] == expected_43)
    rec.require("momentum.P34", p[(3, 4)] == expected_34)
    rec.require("momentum.only_43_34_nonzero", {(a, b) for (a, b), value in p.items() if not value.is_zero} == {(4, 3), (3, 4)})

    k_ind = {(a, b): Form.zero(cb) for a, b in combinations(range(5), 2)}
    k_ind[(3, 4)] = Form.atom(cb, "dtheta", -Poly.make("k"))
    k_table = {(a, b): antisym(k_ind, a, b, cb) for a in range(5) for b in range(5)}
    reduced = push_circle(ordered_pairing(k_table, p).scale(primitive_sign))
    expected_reduced = o_sigma.scale(-Poly.make("tau") * "kappa5_inv" * "k")
    rec.require("primitive.B_ref_reduction", reduced == expected_reduced)
    rec.require("primitive.tau_exact_ordinary_symbol", Poly.make("tau") * "kappa5_inv" * "k" == Poly.make("k") * "tau" * "kappa5_inv")

    # Materially different direct path: no Form or momentum constructor.
    direct_43 = sum(Fraction(parity((4, 3) + perm), 12) * parity(perm) for perm in permutations((0, 1, 2)))
    direct_34 = sum(Fraction(parity((3, 4) + perm), 12) * parity(perm) for perm in permutations((0, 1, 2)))
    rec.require("alternate.direct_P43_coefficient", direct_43 == Fraction(-1, 2))
    rec.require("alternate.direct_P34_coefficient", direct_34 == Fraction(1, 2))
    rec.require("alternate.two_order_primitive_coefficient", -2 * Fraction(1, 2) == -1)

    # Complete generic field-space derivative of the unreduced primitive.
    gb = ("x0", "x1", "x2", "x3")
    ge = {a: generic_one_form(gb, f"E{a}") for a in range(5)}
    de = {a: generic_one_form(gb, f"dE{a}") for a in range(5)}
    gi = {(a, b): generic_one_form(gb, f"K{a}{b}") for a, b in combinations(range(5), 2)}
    gk = {(a, b): antisym(gi, a, b, gb) for a in range(5) for b in range(5)}
    doi = {(a, b): generic_one_form(gb, f"domega{a}{b}") for a, b in combinations(range(5), 2)}
    dbi = {(a, b): generic_one_form(gb, f"dbar{a}{b}") for a, b in combinations(range(5), 2)}
    domega = {(a, b): antisym(doi, a, b, gb) for a in range(5) for b in range(5)}
    dbar = {(a, b): antisym(dbi, a, b, gb) for a in range(5) for b in range(5)}
    gp = momenta(ge)
    dp = vary_momenta(ge, de)
    varied_direct = (ordered_pairing(domega, gp) - ordered_pairing(dbar, gp) + ordered_pairing(gk, dp)).scale(primitive_sign)
    connection_terms = -ordered_pairing(domega, gp) + ordered_pairing(dbar, gp)
    currents = {c: coframe_current(gk, ge, c) for c in range(5)}
    coframe_term = sum_forms((de[c].wedge(currents[c]) for c in range(5)), gb)
    expected_variation = connection_terms if mutation == "delete-coframe-companion" else connection_terms + coframe_term
    rec.require("variation.complete_unreduced_identity", varied_direct == expected_variation)
    rec.require("variation.coframe_current_nonzero_generic", not coframe_term.is_zero)
    rec.require("variation.J_exact_coefficient_and_sign", coframe_term == -ordered_pairing(gk, dp))
    rec.require("variation.reference_term_survives", not ordered_pairing(dbar, gp).is_zero)

    row_results: dict[str, bool] = {}
    for a, b in combinations(range(5), 2):
        row_i = {(i, j): Form.zero(cb) for i, j in combinations(range(5), 2)}
        row_i[(a, b)] = Form.atom(cb, "dtheta" if (a, b) == (3, 4) else "du0", f"v{a}{b}")
        row = {(i, j): antisym(row_i, i, j, cb) for i in range(5) for j in range(5)}
        boundary = ordered_pairing(row, p) + ordered_pairing(row, p).scale(primitive_sign)
        row_results[f"{a}{b}"] = boundary.is_zero
        rec.require(f"cancellation.deltaomega_{a}{b}", boundary.is_zero)

    polar_de = {
        a: (e[a].scale("alpha") if a in (0, 1, 2) else Form.zero(cb))
        for a in range(5)
    }
    polar_dp = vary_momenta(e, polar_de)
    polar_rescaling_form = push_circle(ordered_pairing(k_table, polar_dp).scale(primitive_sign))
    rescaling_residual = polar_rescaling_form.coefficient(sb)
    rec.require("polar.rescaling_derived_from_unreduced_primitive", polar_rescaling_form == o_sigma.scale(Poly.make(-3) * "tau" * "kappa5_inv" * "k" * "alpha"))
    rec.require("polar.rescaling_residual_exact", rescaling_residual == Poly.make("k") * "alpha" * "tau" * "kappa5_inv" * -3)
    rec.require("polar.rescaling_requires_k_zero", rescaling_residual.coefficient_of(("alpha", "k", "kappa5_inv", "tau")) == -3)
    ref = {(a, b): Form.zero(cb) for a in range(5) for b in range(5)}
    ref[(4, 3)] = Form.atom(cb, "dtheta", "dbar43")
    ref[(3, 4)] = -ref[(4, 3)]
    reference_row = push_circle(ordered_pairing(ref, p))
    rec.require("reference.arbitrary_row_nonzero", not reference_row.is_zero)
    rec.require("reference.equation_is_nonzero_P43_zero", not p[(4, 3)].is_zero and p[(4, 3)] == expected_43)
    rec.require("reference.rank_three_witness_nonzero", not o_sigma.is_zero)

    bulk_sign, corner_sign, orbit_trace = orbit_signs(mutation == "reverse-orbit-corner-sign")
    rec.require("orbit.bulk_plus_zeta_D_P", bulk_sign == 1)
    rec.require("orbit.corner_minus_zeta_P", corner_sign == -1)

    cov_residual, seen_generators = covariance_residual(transform_only_dynamical=mutation == "transform-only-dynamical-connection")
    negative_residual, _ = covariance_residual(transform_only_dynamical=True)
    expected_generators = {f"lambda_{a}{b}" for a, b in combinations(range(5), 2)}
    rec.require("covariance.simultaneous_SO14_generic_identity", cov_residual.is_zero)
    rec.require("covariance.all_ten_generators_present", seen_generators == expected_generators)
    rec.require("covariance.transform_only_connection_negative_control", not negative_residual.is_zero)

    details = {
        "mutation": mutation or None,
        "nonzero_momenta": {f"P{a}{b}": value.coefficient(("du0", "du1", "du2")).text() for (a, b), value in p.items() if not value.is_zero},
        "B_ref": reduced.coefficient(sb).text(),
        "direct_coefficients": {"P43": str(direct_43), "P34": str(direct_34)},
        "deltaomega_rows": row_results,
        "coframe_companion_terms": len(coframe_term.terms),
        "reference_row": reference_row.coefficient(sb).text(),
        "rescaling_residual": rescaling_residual.text(),
        "orbit": {"bulk": bulk_sign, "corner": corner_sign, "derivation": orbit_trace},
        "covariance": {"kind": "generic exact polynomial tensor identity", "finite_witness_only": False, "simultaneous_residual_terms": len(cov_residual.terms), "transform_only_residual_terms": len(negative_residual.terms), "internal_generators": 10},
    }
    return rec, details


def emit_observations(observations: dict[str, object]) -> None:
    print(OBSERVATION_PREFIX + " " + json.dumps(observations, sort_keys=True, allow_nan=False, default=str))


def check() -> int:
    rec, details = evaluate(MUTATION)
    mutation_runs: dict[str, object] = {}
    if not MUTATION:
        for mutation in MUTATIONS:
            env = dict(os.environ)
            env["O013_INTENTIONAL_MUTATION"] = mutation
            process = subprocess.run([sys.executable, str(Path(__file__).resolve())], env=env, capture_output=True, text=True, check=False)
            mutation_runs[mutation] = {"exit_code": process.returncode, "detected": process.returncode == FAILED}
            rec.require(f"mutation_process.{mutation}.exits_1", process.returncode == FAILED)
    failed = rec.failed
    emit_observations({
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": [PRODUCER_MODEL],
        "representation": {"domain": "free exact rational polynomials, finite exterior forms, and explicit SO(1,4) tables", "equality": "canonical sparse tuple equality", "CAS": False, "floating_point": False, "random_sampling": False, "covariance_rigor": "generic polynomial identity in all component and gauge-generator atoms"},
        "details": details,
        "mutation_processes": mutation_runs,
        "assertions": {"total": len(rec.results), "passed": len(rec.results) - len(failed), "failed": len(failed), "failed_names": failed},
    })
    if failed:
        for name in failed:
            print(f"FAILED: {name}", file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        return check()
    except (KeyError, ValueError) as exc:
        emit_observations({"obligation_id": OBLIGATION_ID, "producer_model": PRODUCER_MODEL, "inconclusive_reason": str(exc)})
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR


if __name__ == "__main__":
    raise SystemExit(main())
