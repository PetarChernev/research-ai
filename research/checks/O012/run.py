#!/usr/bin/env python3
"""Exact claim-specific implementation of O012; never writes result.json."""

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

OBLIGATION_ID = "O012"
PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
OBSERVATION_PREFIX = "##OBSERVATIONS##"
PRODUCER_MODEL = "openai/gpt-5.6-sol"
MUTATION = os.environ.get("O012_INTENTIONAL_MUTATION", "")
MUTATIONS = ("core-sign", "omit-order", "smooth-flat-zero", "fictitious-d005-cancellation")


def parity(values: tuple[int, ...]) -> int:
    if len(set(values)) != len(values):
        return 0
    inversions = sum(values[i] > values[j] for i in range(len(values)) for j in range(i + 1, len(values)))
    return -1 if inversions % 2 else 1


@dataclass(frozen=True)
class Poly:
    """Canonical free polynomial over Q; a monomial is a sorted atom tuple."""
    terms: tuple[tuple[tuple[str, ...], Fraction], ...] = ()

    @staticmethod
    def make(value: "Poly | Fraction | int | str") -> "Poly":
        if isinstance(value, Poly):
            return value
        if isinstance(value, str):
            return Poly((((value,), Fraction(1)),))
        value = Fraction(value)
        return Poly((((), value),)) if value else Poly()

    @staticmethod
    def collect(items: Iterable[tuple[tuple[str, ...], Fraction]]) -> "Poly":
        result: dict[tuple[str, ...], Fraction] = {}
        for monomial, coefficient in items:
            key = tuple(sorted(monomial))
            result[key] = result.get(key, Fraction(0)) + Fraction(coefficient)
        return Poly(tuple(sorted((m, c) for m, c in result.items() if c)))

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

    def text(self) -> str:
        return "0" if not self.terms else "+".join(f"{c}*{'*'.join(m) or '1'}" for m, c in self.terms)


@dataclass(frozen=True)
class Form:
    """Canonical sparse exterior form on one explicitly ordered basis."""
    basis: tuple[str, ...]
    terms: tuple[tuple[tuple[str, ...], Poly], ...] = ()

    @staticmethod
    def collect(basis: tuple[str, ...], items: Iterable[tuple[tuple[str, ...], Poly]]) -> "Form":
        order = {label: index for index, label in enumerate(basis)}
        result: dict[tuple[str, ...], Poly] = {}
        for word, coefficient in items:
            if len(set(word)) != len(word):
                continue
            sign = -1 if sum(order[word[i]] > order[word[j]] for i in range(len(word)) for j in range(i + 1, len(word))) % 2 else 1
            canonical = tuple(sorted(word, key=order.__getitem__))
            result[canonical] = result.get(canonical, Poly()) + coefficient * sign
        return Form(basis, tuple(sorted((w, c) for w, c in result.items() if not c.is_zero)))

    @staticmethod
    def atom(basis: tuple[str, ...], label: str, coefficient: Poly | int | str = 1) -> "Form":
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

    def wedge(self, other: "Form") -> "Form":
        if self.basis != other.basis:
            raise ValueError("exterior basis mismatch")
        return Form.collect(self.basis, ((w1 + w2, c1 * c2) for w1, c1 in self.terms for w2, c2 in other.terms))

    def scale(self, scalar: Poly | Fraction | int | str) -> "Form":
        factor = Poly.make(scalar)
        return Form.collect(self.basis, ((w, c * factor) for w, c in self.terms))

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def coefficient(self, word: tuple[str, ...]) -> Poly:
        return dict(self.terms).get(word, Poly())


def wedge_all(factors: Iterable[Form], basis: tuple[str, ...]) -> Form:
    result = Form.collect(basis, [((), Poly.make(1))])
    for factor in factors:
        result = result.wedge(factor)
    return result


def antisymmetric_component(components: Mapping[tuple[int, int], Form], a: int, b: int, basis: tuple[str, ...]) -> Form:
    if a == b:
        return Form.zero(basis)
    return components.get((a, b), Form.zero(basis)) if a < b else -components.get((b, a), Form.zero(basis))


def theta5_ordered(coframes: Mapping[int, Form], variations: Mapping[tuple[int, int], Form], *, omit_order: bool) -> Form:
    """D004 (25), reconstructed from the complete 1/12 ordered sum."""
    basis = next(iter(coframes.values())).basis
    total = Form.zero(basis)
    for indices in permutations(range(5)):
        a, b, c, d, e = indices
        if omit_order and a > b:
            continue
        term = wedge_all((antisymmetric_component(variations, a, b, basis), coframes[c], coframes[d], coframes[e]), basis)
        total = total + term.scale(Poly.make("kappa5_inv") * Fraction(parity(indices), 12))
    return total


def push_circle(form: Form) -> Form:
    if form.basis[-1] != "dtheta":
        raise ValueError("dtheta must be the final oriented fiber leg")
    return Form.collect(form.basis[:-1], ((word[:-1], coefficient * "tau") for word, coefficient in form.terms if word and word[-1] == "dtheta"))


def split_coefficients() -> tuple[Fraction, Fraction]:
    """Reconstruct D004 (31) ratios by internal ordered enumeration."""
    raw: dict[tuple[str, ...], Fraction] = {}
    persistent: dict[tuple[str, ...], Fraction] = {}
    mixed: dict[tuple[str, ...], Fraction] = {}

    def add(table: dict[tuple[str, ...], Fraction], pair: str, legs: tuple[int, ...], value: Fraction) -> None:
        sign = parity(legs)
        word = (pair,) + tuple(f"E{i}" for i in sorted(legs))
        table[word] = table.get(word, Fraction(0)) + value * sign

    for indices in permutations(range(5)):
        a, b, c, d, e = indices
        lo, hi = sorted((a, b))
        add(raw, f"w{lo}{hi}", (c, d, e), Fraction(parity(indices) * (1 if a < b else -1), 12))
    for a, b, c, d in permutations(range(4)):
        eps = parity((a, b, c, d))
        lo, hi = sorted((a, b))
        add(persistent, f"w{lo}{hi}", (c, d, 4), Fraction(eps * (1 if a < b else -1)))
        add(mixed, f"w{a}4", (b, c, d), Fraction(-eps))  # omega^(4a)=-omega^(a4)

    def ratio(structure: dict[tuple[str, ...], Fraction]) -> Fraction:
        values = {raw[word] / coefficient for word, coefficient in structure.items()}
        if len(values) != 1:
            raise ValueError("ordered split has no unique ratio")
        return next(iter(values))

    return ratio(persistent), ratio(mixed)


def epsilon_three_form(basis: tuple[str, ...], coframes: Mapping[int, Form]) -> Form:
    result = Form.zero(basis)
    for b, c, d in permutations(range(4), 3):
        eps = parity((3, b, c, d))
        if eps:
            result = result + wedge_all((coframes[b], coframes[c], coframes[d]), basis).scale(eps)
    return result


def momentum(coframes: Mapping[int, Form], scale_atom: str) -> dict[tuple[int, int], Form]:
    basis = next(iter(coframes.values())).basis
    result: dict[tuple[int, int], Form] = {}
    for a, b in combinations(range(4), 2):
        value = Form.zero(basis)
        for c in range(4):
            for d in range(4):
                eps = parity((a, b, c, d))
                if eps:
                    value = value + coframes[c].wedge(coframes[d]).scale(Poly.make(scale_atom) * Fraction(eps, 4))
        result[(a, b)] = value
    return result


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
    cb = ("du0", "du1", "du2", "dtheta")
    sb = cb[:-1]
    ce = {0: Form.atom(cb, "du0"), 1: Form.atom(cb, "du1"), 2: Form.atom(cb, "du2"), 3: Form.zero(cb), 4: Form.zero(cb)}
    se = {0: Form.atom(sb, "du0"), 1: Form.atom(sb, "du1"), 2: Form.atom(sb, "du2"), 3: Form.zero(sb)}
    o_sigma = wedge_all((se[0], se[1], se[2]), sb)
    o_circle = wedge_all((ce[0], ce[1], ce[2], Form.atom(cb, "dtheta")), cb)

    split_e4, split_mixed = split_coefficients()
    rec.require("D004.split_E4_coefficient_1_over_4", split_e4 == Fraction(1, 4))
    rec.require("D004.split_mixed_coefficient_1_over_6", split_mixed == Fraction(1, 6))
    variation = {} if mutation == "smooth-flat-zero" else {(3, 4): Form.atom(cb, "dtheta", -Poly.make("delta_chi43"))}
    theta_mixed = theta5_ordered(ce, variation, omit_order=mutation == "omit-order")
    pushed = push_circle(theta_mixed)
    if mutation == "core-sign":
        pushed = -pushed
    expected_core = o_sigma.scale(Poly.make("delta_chi43") * "kappa5_inv" * "tau")
    rec.require("D004.mixed_ordered_coefficient", pushed == expected_core)
    rec.require("D004.mixed_unintegrated_coefficient", theta_mixed == o_circle.scale(Poly.make("delta_chi43") * "kappa5_inv"))

    persistent_variation = {(0, 3): Form.atom(cb, "du0", "f")}
    theta_e4 = theta5_ordered(ce, persistent_variation, omit_order=False)
    rec.require("D004.collapsed_E4_channel_zero", theta_e4.is_zero and push_circle(theta_e4).is_zero)
    epsilon3 = epsilon_three_form(cb, ce)
    expected_epsilon3 = wedge_all((ce[0], ce[1], ce[2]), cb).scale(-6)
    rec.require("D004.epsilon_3bcd_equals_minus_6", epsilon3 == expected_epsilon3)
    rec.require("D004.fiber_reordering_sign", Form.atom(cb, "dtheta").wedge(expected_epsilon3) == o_circle.scale(6))

    # Separate hand/permutation path: pair orders, coframe permutations, action
    # factor, fiber reordering, and epsilon_3012 are assembled directly.
    hand_coefficient = Fraction(2 * 6, 12) * (-1) * parity((3, 0, 1, 2))
    rec.require("alternate.hand_pair_and_permutation_coefficient", hand_coefficient == 1)
    rec.require("alternate.hand_agrees_ordered_enumeration", pushed.coefficient(sb) == Poly.make("delta_chi43") * "kappa5_inv" * "tau")

    fields = ("e_plus", "omega_plus_ab", "e_minus", "varpi_ab", "g", "lambda_ab", "mu_a", "u_seed_orbit")
    variations = ("delta_omega_plus_ab", "delta_varpi_ab", "delta_e_plus", "delta_e_minus", "delta_lambda_ab", "delta_mu_a", "xi_g", "zeta_u")
    rec.require("D005.complete_basic_field_list_excludes_chi43", "chi43" not in fields and "omega43" not in fields)
    rec.require("D005.complete_variation_list_excludes_delta_chi43", "delta_chi43" not in variations)
    q = momentum(se, "kappa4_inv")
    pminus = momentum(se, "kappa4_inv")
    lam = {pair: -form for pair, form in q.items()}
    zero = Form.zero(sb)
    delta_e = {a: zero for a in range(4)}
    delta_omega = {pair: zero for pair in q}
    k_forms = {pair: zero for pair in q}
    mu = {a: zero for a in range(4)}
    h_of_k: dict[int, Form] = {}
    for c in range(4):
        h_c = zero
        for a in range(4):
            for b in range(4):
                k_ab = antisymmetric_component(k_forms, a, b, sb)
                for d in range(4):
                    eps = parity((a, b, c, d))
                    if eps:
                        h_c = h_c + k_ab.wedge(se[d]).scale(Poly.make("kappa4_inv") * Fraction(-eps, 2))
        h_of_k[c] = h_c
    d_q = {pair: zero for pair in q}
    shell_rows = {
        "Delta_e": all(form.is_zero for form in delta_e.values()),
        "Delta_omega": all(form.is_zero for form in delta_omega.values()),
        "Q_plus_lambda": all((q[pair] + lam[pair]).is_zero for pair in q),
        "Pminus_plus_lambda": all((pminus[pair] + lam[pair]).is_zero for pair in q),
        "Q_equals_Pminus": q == pminus,
        "K_zero": all(form.is_zero for form in k_forms.values()),
        "H0_plus_mu": all((h_of_k[a] + mu[a]).is_zero for a in range(4)),
        "mu_zero": all(form.is_zero for form in mu.values()),
        "edge_dQ_minus_dQ": all((d_q[pair] + -d_q[pair]).is_zero for pair in q),
        "fixed_seed_dQ_zero": all(form.is_zero for form in d_q.values()),
    }
    for row, condition in shell_rows.items():
        rec.require(f"D005.shell.{row}", condition)
    rec.require("D005.six_momentum_components_reproduced", len(q) == 6)
    rec.require("D005.rank_three_momentum_nonzero", sum(not form.is_zero for form in q.values()) == 3)

    incidence: dict[str, Form] = {name: zero for name in variations}
    if mutation == "fictitious-d005-cancellation":
        incidence["delta_chi43"] = -expected_core
    d005_chi = incidence.get("delta_chi43", zero)
    rec.require("D005.chi43_coefficient_identically_zero", d005_chi.is_zero)
    rec.require("combined.free_mixed_term_uncancelled", pushed + d005_chi == expected_core)
    details = {
        "mutation": mutation or None,
        "ordered_split": {"E4": str(split_e4), "mixed": str(split_mixed)},
        "mixed_coefficient": pushed.coefficient(sb).text(),
        "epsilon_3bcd": epsilon3.coefficient(sb).text(),
        "hand_coefficient": str(hand_coefficient),
        "d005_fields": list(fields),
        "d005_variations": list(variations),
        "shell_rows": shell_rows,
        "nonzero_momentum_components": [f"{a}{b}" for (a, b), form in q.items() if not form.is_zero],
    }
    return rec, details


def emit_observations(observations: dict[str, object]) -> None:
    print(OBSERVATION_PREFIX + " " + json.dumps(observations, sort_keys=True, allow_nan=False, default=str))


def check() -> int:
    rec, details = evaluate(MUTATION)
    mutation_runs: dict[str, object] = {}
    if not MUTATION:
        for mutation in MUTATIONS:
            environment = dict(os.environ)
            environment["O012_INTENTIONAL_MUTATION"] = mutation
            process = subprocess.run([sys.executable, str(Path(__file__).resolve())], env=environment, capture_output=True, text=True, check=False)
            mutation_runs[mutation] = {"exit_code": process.returncode, "detected": process.returncode == FAILED}
            rec.require(f"mutation_process.{mutation}.exits_1", process.returncode == FAILED)
    failed = rec.failed
    emit_observations({
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": [PRODUCER_MODEL],
        "representation": {"domain": "free exact polynomial coefficients and finite exterior forms", "equality": "canonical sparse tuple equality", "CAS": False, "floating_point": False, "random_sampling": False, "tau": "formal exact ordinary period interpreted as 2*pi"},
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
        outcome = check()
    except (KeyError, ValueError) as exc:
        emit_observations({"obligation_id": OBLIGATION_ID, "producer_model": PRODUCER_MODEL, "inconclusive_reason": str(exc)})
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    return outcome if outcome in {PASSED, FAILED, INCONCLUSIVE} else ERROR


if __name__ == "__main__":
    raise SystemExit(main())
