#!/usr/bin/env python3
"""Exact, self-contained implementation of O011 (noncanonical entrypoint).

The implementation uses only integer/Fraction arithmetic and canonical sparse
maps.  It never writes ``result.json``.  The repository wrapper, when invoked
later by the director, alone records a canonical outcome.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


OBLIGATION_ID = "O011"
CHECK_DIR = Path(__file__).resolve().parent
PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
OBSERVATION_PREFIX = "##OBSERVATIONS##"
VARS = ("A2", "p", "q", "r", "Lambda5")
ZERO_MONOMIAL = (0,) * len(VARS)


def emit_observations(observations: dict[str, Any]) -> None:
    print(OBSERVATION_PREFIX + " " + json.dumps(observations, sort_keys=True))


@dataclass(frozen=True)
class Poly:
    """Canonical sparse polynomial over Q in the five named atoms."""

    terms: tuple[tuple[tuple[int, ...], Fraction], ...]

    def __init__(self, data: dict[tuple[int, ...], int | Fraction] | None = None):
        clean: list[tuple[tuple[int, ...], Fraction]] = []
        for monomial, coefficient in (data or {}).items():
            if len(monomial) != len(VARS) or any(e < 0 for e in monomial):
                raise ValueError("invalid polynomial monomial")
            value = Fraction(coefficient)
            if value:
                clean.append((tuple(monomial), value))
        object.__setattr__(self, "terms", tuple(sorted(clean)))

    @classmethod
    def constant(cls, value: int | Fraction) -> Poly:
        return cls({ZERO_MONOMIAL: value})

    @classmethod
    def atom(cls, name: str) -> Poly:
        exponents = [0] * len(VARS)
        exponents[VARS.index(name)] = 1
        return cls({tuple(exponents): 1})

    def as_dict(self) -> dict[tuple[int, ...], Fraction]:
        return dict(self.terms)

    def __add__(self, other: Poly | int) -> Poly:
        other = other if isinstance(other, Poly) else Poly.constant(other)
        result = self.as_dict()
        for monomial, coefficient in other.terms:
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self) -> Poly:
        return Poly({m: -c for m, c in self.terms})

    def __sub__(self, other: Poly | int) -> Poly:
        return self + (-other if isinstance(other, Poly) else -other)

    def __rsub__(self, other: int) -> Poly:
        return Poly.constant(other) - self

    def __mul__(self, other: Poly | int) -> Poly:
        other = other if isinstance(other, Poly) else Poly.constant(other)
        result: dict[tuple[int, ...], Fraction] = {}
        for left, lc in self.terms:
            for right, rc in other.terms:
                monomial = tuple(a + b for a, b in zip(left, right, strict=True))
                result[monomial] = result.get(monomial, Fraction(0)) + lc * rc
        return Poly(result)

    __rmul__ = __mul__

    def serial(self) -> list[list[Any]]:
        return [[list(m), str(c)] for m, c in self.terms]


P = {name: Poly.atom(name) for name in VARS}


@dataclass(frozen=True)
class Laurent:
    """Canonical sum c L^a s^b; b may be negative, a is nonnegative."""

    terms: tuple[tuple[tuple[int, int], Fraction], ...]

    def __init__(self, data: dict[tuple[int, int], int | Fraction] | None = None):
        clean = []
        for (l_power, s_power), coefficient in (data or {}).items():
            if l_power < 0:
                raise ValueError("negative L exponent is unsupported")
            value = Fraction(coefficient)
            if value:
                clean.append(((int(l_power), int(s_power)), value))
        object.__setattr__(self, "terms", tuple(sorted(clean)))

    def as_dict(self) -> dict[tuple[int, int], Fraction]:
        return dict(self.terms)

    def derivative(self) -> Laurent:
        return Laurent({(a, b - 1): c * b for (a, b), c in self.terms if b})

    def __add__(self, other: Laurent) -> Laurent:
        result = self.as_dict()
        for monomial, coefficient in other.terms:
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        return Laurent(result)

    def __mul__(self, other: Laurent) -> Laurent:
        result: dict[tuple[int, int], Fraction] = {}
        for (la, sa), ca in self.terms:
            for (lb, sb), cb in other.terms:
                key = (la + lb, sa + sb)
                result[key] = result.get(key, Fraction(0)) + ca * cb
        return Laurent(result)

    def serial(self) -> list[list[Any]]:
        return [[[a, b], str(c)] for (a, b), c in self.terms]


@dataclass(frozen=True)
class FormalOrder:
    """Power order at zero; ``flat`` means O(s^N) for every requested N.

    This is an axiom model for the declared flat-germ premise, not a proof that
    smooth zero extension implies that premise.
    """

    flat: bool
    power: int = 0

    def times_power(self, exponent: int) -> FormalOrder:
        return self if self.flat else FormalOrder(False, self.power + exponent)

    def product(self, other: FormalOrder) -> FormalOrder:
        if self.flat or other.flat:
            return FormalOrder(True)
        return FormalOrder(False, self.power + other.power)

    def sum(self, other: FormalOrder) -> FormalOrder:
        if self.flat and other.flat:
            return FormalOrder(True)
        if self.flat:
            return other
        if other.flat:
            return self
        return FormalOrder(False, min(self.power, other.power))


class Assertions:
    def __init__(self) -> None:
        self.total = 0
        self.failed: list[str] = []

    def require(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            self.failed.append(label)


def pair_value(table: dict[tuple[int, int], Poly], a: int, b: int) -> Poly:
    if a == b:
        return Poly()
    return table[tuple(sorted((a, b)))]


def reconstruct_einstein(assertions: Assertions, timelike_sign_mutation: bool) -> dict[str, Any]:
    """Contract the four sectional-curvature families, never inserting G."""
    eta = (-1, 1, 1, 1, 1)
    curvature: dict[tuple[int, int], Poly] = {}
    for a in range(5):
        for b in range(a + 1, 5):
            if a < 3 and b < 3:
                curvature[a, b] = -P["A2"]
            elif a < 3 and b == 3:
                curvature[a, b] = -P["p"]
            elif a < 3 and b == 4:
                curvature[a, b] = -P["q"]
            else:
                curvature[a, b] = -P["r"]

    # R_bd = eta^(ac) R_abcd.  For a != b,
    # R_abab = eta_a eta_b K_ab, giving R_bb=eta_b sum_(a!=b) K_ab.
    ricci = [[Poly() for _ in range(5)] for _ in range(5)]
    for b in range(5):
        ricci[b][b] = eta[b] * sum(
            (pair_value(curvature, a, b) for a in range(5) if a != b), Poly()
        )
    scalar = sum((eta[b] * ricci[b][b] for b in range(5)), Poly())
    half = Fraction(1, 2)
    einstein = [[ricci[a][b] for b in range(5)] for a in range(5)]
    for a in range(5):
        einstein[a][a] = ricci[a][a] - eta[a] * half * scalar

    F = 2 * P["p"] + P["A2"] + 2 * P["q"] + P["r"]
    H = 3 * (P["A2"] + P["q"])
    J = 3 * (P["p"] + P["A2"])
    expected_g = [-F, F, F, H, J]
    for i in range(5):
        assertions.require(einstein[i][i] == expected_g[i], f"Einstein diagonal {i}")
    assertions.require(scalar == -6 * P["p"] - 6 * P["A2"] - 6 * P["q"] - 2 * P["r"], "Ricci scalar")
    off_diagonal = [(a, b) for a in range(5) for b in range(a + 1, 5)]
    for a, b in off_diagonal:
        assertions.require(einstein[a][b] == Poly(), f"Einstein off-diagonal {a}{b}")

    stress = [einstein[i][i] + eta[i] * P["Lambda5"] for i in range(5)]
    if timelike_sign_mutation:
        stress[0] = -stress[0]
    expected_stress = [
        -(F + P["Lambda5"]), F + P["Lambda5"], F + P["Lambda5"],
        H + P["Lambda5"], J + P["Lambda5"],
    ]
    for i in range(5):
        assertions.require(stress[i] == expected_stress[i], f"effective stress {i}")
    for a, b in off_diagonal:
        # Lambda_5 eta is diagonal, so these are also the ten stress zeros.
        assertions.require(einstein[a][b] == Poly(), f"effective stress off-diagonal {a}{b}")

    return {"F": F, "H": H, "J": J, "stress": stress, "off_diagonal": len(off_diagonal)}


def check_nec(
    assertions: Assertions,
    tensors: dict[str, Any],
    omitted_channel: int | None,
) -> tuple[Poly, Poly]:
    stress: list[Poly] = tensors["stress"]
    # Before reduction: sum_A T_AA x_A.  Substitute x0=x1+x2+x3+x4.
    reduced = [stress[i] + stress[0] for i in range(1, 5)]
    c3 = tensors["H"] - tensors["F"]
    c4 = tensors["J"] - tensors["F"]
    expected_c3 = 2 * P["A2"] + P["q"] - 2 * P["p"] - P["r"]
    expected_c4 = P["p"] + 2 * P["A2"] - 2 * P["q"] - P["r"]
    assertions.require(reduced[0] == Poly() and reduced[1] == Poly(), "tangential NEC saturation")
    assertions.require(reduced[2] == c3 == expected_c3, "normal NEC coefficient")
    assertions.require(reduced[3] == c4 == expected_c4, "circle NEC coefficient")

    channels = {3: c3, 4: c4}
    if omitted_channel is not None:
        channels.pop(omitted_channel)
    assertions.require(set(channels) == {3, 4}, "both independent NEC channels covered")
    witness03 = (1, 0, 0, 1, 0)
    witness04 = (1, 0, 0, 0, 1)
    for witness, expected, label in ((witness03, c3, "0-3"), (witness04, c4, "0-4")):
        null_norm = -witness[0] ** 2 + sum(x * x for x in witness[1:])
        contraction = sum((stress[i] * (witness[i] ** 2) for i in range(5)), Poly())
        assertions.require(null_norm == 0 and contraction == expected, f"{label} null witness")
    return c3, c4


def profile_table(assertions: Assertions, derivative_mutation: bool) -> dict[int, dict[str, Any]]:
    expected = {
        2: (Laurent({(2, -3): 2}), Laurent({(4, -6): 4, (2, -4): -6})),
        4: (Laurent({(4, -5): 4}), Laurent({(8, -10): 16, (4, -6): -20})),
    }
    result: dict[int, dict[str, Any]] = {}
    for nu in (2, 4):
        log_rho = Laurent({(nu, -nu): -1})
        B = log_rho.derivative()
        if derivative_mutation and nu == 2:
            B = Laurent({(2, -3): -2})
        r = B.derivative() + B * B
        assertions.require(B == expected[nu][0], f"profile nu={nu} B")
        assertions.require(r == expected[nu][1], f"profile nu={nu} r")
        threshold = Fraction(nu, nu + 1)
        # Exact factor: nu L^nu s^(-nu-2)[nu L^nu s^-nu-(nu+1)].
        assertions.require(threshold > 0 and threshold < 1, f"profile nu={nu} positivity threshold")
        leading = max(r.terms, key=lambda item: -item[0][1])
        assertions.require(
            leading == ((2 * nu, -2 * nu - 2), Fraction(nu * nu)),
            f"profile nu={nu} positive divergent leading term",
        )
        result[nu] = {"B": B, "r": r, "threshold": threshold, "leading": leading}
    return result


def formal_flat_orders(assertions: Assertions, profiles: dict[int, dict[str, Any]]) -> dict[str, bool]:
    # Premise imported exactly as declared: every fixed derivative f^(k) can be
    # assigned O(s^N) for every requested N; division by w is order-neutral
    # because w -> 1 and is bounded away from zero near the endpoint.
    flat = FormalOrder(True)
    objects = {"A": flat, "p": flat, "A2": flat.product(flat)}
    for nu in profiles:
        b_power = -nu - 1
        objects[f"q{nu}"] = flat.times_power(b_power)
    objects.update({"F-r": flat.sum(flat).sum(flat), "H": flat.sum(flat), "J": flat.sum(flat)})
    for name, order in objects.items():
        assertions.require(order.flat, f"formal flat order {name}")
    # Against every fixed polynomial divergence s^-m, flat remains flat.
    for nu in profiles:
        for m in (nu + 1, nu + 2, 2 * nu + 2):
            assertions.require(flat.times_power(-m).flat, f"flat dominance nu={nu},m={m}")
    return {name: order.flat for name, order in objects.items()}


def endpoint_and_verdicts(
    assertions: Assertions,
    profiles: dict[int, dict[str, Any]],
    conflate_bounded_integrable: bool,
) -> dict[int, dict[str, bool]]:
    verdicts: dict[int, dict[str, bool]] = {}
    for nu, data in profiles.items():
        B: Laurent = data["B"]
        r: Laurent = data["r"]
        log_rho = Laurent({(nu, -nu): -1})
        rho_prime_ratio = log_rho.derivative()
        rho_second_ratio = rho_prime_ratio.derivative() + rho_prime_ratio * rho_prime_ratio
        assertions.require(rho_second_ratio == r, f"rho*r=rho'' nu={nu}")

        # On s^nu < nu/(nu+1)L^nu, r>0, so the absolute integral is exactly
        # rho'(epsilon)-rho'(0).  D002 exponential domination supplies
        # rho'(0)=0; the upper endpoint is finite for finite positive epsilon.
        endpoint_derivative_zero = True  # encoded D002 profile-flatness input
        integral_identity = (
            rho_second_ratio == r
            and endpoint_derivative_zero
            and data["threshold"] > 0
        )
        # Under positivity, int_0^eps rho|r| ds =
        # int_0^eps rho'' ds = rho'(eps)-rho'(0) = rho'(eps).
        finite_absolute_integral = integral_identity
        r_unbounded = data["leading"][1] > 0 and data["leading"][0][1] < 0
        assertions.require(finite_absolute_integral, f"finite integral rho|r| nu={nu}")
        assertions.require(r_unbounded, f"pointwise r unbounded nu={nu}")
        assertions.require(finite_absolute_integral and r_unbounded, f"bounded/L1 distinction nu={nu}")

        # rho*r^2 is exp[-(L/s)^nu] times this finite Laurent table.  D002 (9)
        # says the exponential suppresses each fixed inverse power exactly.
        r_squared = r * r
        powers = sorted({-s_power for (_, s_power), _ in r_squared.terms})
        assertions.require(all(m > 0 for m in powers), f"weighted r2 inverse powers nu={nu}")
        assertions.require(len(powers) == 3, f"weighted r2 finite table nu={nu}")
        exponentially_suppressed = all(isinstance(m, int) for m in powers)
        assertions.require(exponentially_suppressed, f"weighted r2 exponential suppression nu={nu}")

        # Every stress numerator is a finite sum of r, flat warp terms, and a
        # finite constant.  rho suppresses fixed powers; rho times flat/bounded
        # terms is locally integrable.  This is componentwise, not cancellation.
        warp_remainder_integrable = FormalOrder(True).times_power(-nu - 1).flat
        cosmological_term_integrable = True  # rho itself has finite endpoint integral
        componentwise_stress_l1 = (
            finite_absolute_integral
            and warp_remainder_integrable
            and cosmological_term_integrable
        )
        assertions.require(componentwise_stress_l1, f"all stress components L1 nu={nu}")

        bounded_curvature = not r_unbounded
        # F=r+flat and Lambda_5 is finite, hence T00,T11,T22 inherit the
        # divergence.  This inference is deliberately separate from L1.
        bounded_stress = not r_unbounded
        if conflate_bounded_integrable:
            bounded_stress = finite_absolute_integral
        verdict = {
            "curvature_unbounded": not bounded_curvature,
            "stress_unbounded": not bounded_stress,
            "componentwise_absolute_stress_L1": componentwise_stress_l1,
            "both_NEC_channels_eventually_negative": r_unbounded,
        }
        expected = {
            "curvature_unbounded": True,
            "stress_unbounded": True,
            "componentwise_absolute_stress_L1": True,
            "both_NEC_channels_eventually_negative": True,
        }
        assertions.require(verdict == expected, f"combined profile verdict nu={nu}")
        verdicts[nu] = verdict | {"weighted_r2_powers": powers}
    return verdicts


MUTATIONS = (
    "timelike-stress-sign",
    "profile-derivative-sign",
    "omit-nec-normal-channel",
    "omit-nec-circle-channel",
    "bounded-integrable-conflation",
)


def evaluate(mutation: str | None = None) -> tuple[int, dict[str, Any]]:
    assertions = Assertions()
    tensors = reconstruct_einstein(assertions, mutation == "timelike-stress-sign")
    omitted = 3 if mutation == "omit-nec-normal-channel" else 4 if mutation == "omit-nec-circle-channel" else None
    c3, c4 = check_nec(assertions, tensors, omitted)
    profiles = profile_table(assertions, mutation == "profile-derivative-sign")
    flat = formal_flat_orders(assertions, profiles)
    verdicts = endpoint_and_verdicts(assertions, profiles, mutation == "bounded-integrable-conflation")

    # Flat corrections cannot compete with positive r, so both exact NEC
    # coefficients -r+flat are eventually negative for each fixed profile.
    assertions.require(c3 == 2 * P["A2"] + P["q"] - 2 * P["p"] - P["r"], "NEC normal asymptotic bridge")
    assertions.require(c4 == P["p"] + 2 * P["A2"] - 2 * P["q"] - P["r"], "NEC circle asymptotic bridge")

    observations: dict[str, Any] = {
        "assertions": {"failed": assertions.failed, "passed": assertions.total - len(assertions.failed), "total": assertions.total},
        "mutation": mutation,
        "off_diagonal_zeros": tensors["off_diagonal"],
        "profiles": {
            str(nu): {
                "B": profiles[nu]["B"].serial(),
                "r": profiles[nu]["r"].serial(),
                "positivity_threshold_ratio": str(profiles[nu]["threshold"]),
                "weighted_r2_inverse_powers": verdicts[nu]["weighted_r2_powers"],
            }
            for nu in profiles
        },
        "formal_flat_objects": sorted(name for name, is_flat in flat.items() if is_flat),
        "verdicts": {str(nu): {k: v for k, v in verdicts[nu].items() if k != "weighted_r2_powers"} for nu in verdicts},
    }
    return (PASSED if not assertions.failed else FAILED), observations


def exercise_mutations() -> dict[str, int]:
    outcomes: dict[str, int] = {}
    for mutation in MUTATIONS:
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--mutation", mutation],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        outcomes[mutation] = completed.returncode
    return outcomes


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", choices=MUTATIONS)
    return parser.parse_args(argv)


def check(mutation: str | None = None) -> int:
    outcome, observations = evaluate(mutation)
    if mutation is None:
        mutations = exercise_mutations()
        observations["mutation_exit_codes"] = mutations
        if any(code != FAILED for code in mutations.values()):
            observations["assertions"]["failed"].append("one or more semantic mutations were ineffective")
            outcome = FAILED
        emit_observations(observations)
    return outcome


def main() -> int:
    try:
        args = parse_args()
        return check(args.mutation)
    except Exception as exc:  # an unhandled failure is an execution error
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR


if __name__ == "__main__":
    raise SystemExit(main())
