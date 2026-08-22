#!/usr/bin/env python3
"""Claim-specific exact implementation of O007; never writes result.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import permutations
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence


OBLIGATION_ID = "O007"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra,
    ExteriorForm,
    Polynomial,
    levi_civita_sign,
)


PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PRODUCER_MODEL = "openai/gpt-5.6-sol"
OBSERVATION_PREFIX = "##OBSERVATIONS##"
MUTATION = os.environ.get("O007_INTENTIONAL_MUTATION", "")
SUPPORTED_MUTATIONS = {"", "exterior-sign", "lambda-sign", "dressing-omit", "dressing-invert"}
INTERNAL4 = (0, 1, 2, 3)
INTERNAL5 = (0, 1, 2, 3, 4)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
ETA = (-1, 1, 1, 1)
ZERO, ONE = Fraction(0), Fraction(1)


class UnsupportedSectorError(ValueError):
    """A requested object is outside the predeclared finite exact sector."""


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


def emit_observations(data: Mapping[str, Any]) -> None:
    print(OBSERVATION_PREFIX + " " + json.dumps(data, sort_keys=True, default=str, allow_nan=False))


def wedge_all(algebra: ExteriorAlgebra, factors: Sequence[ExteriorForm]) -> ExteriorForm:
    result = algebra.unit()
    for factor in factors:
        result = result.wedge(factor)
    return result


def substitute_form(form: ExteriorForm, replacements: Mapping[str, Polynomial | int | Fraction]) -> ExteriorForm:
    return form.algebra.from_terms(
        (word, coefficient.substitute(replacements)) for word, coefficient in form.terms
    )


def antisymmetric_component(
    components: Mapping[tuple[int, int], ExteriorForm], a: int, b: int, algebra: ExteriorAlgebra
) -> ExteriorForm:
    if a == b:
        return algebra.zero()
    return components.get((a, b), algebra.zero()) if a < b else -components.get((b, a), algebra.zero())


def palatini_component(
    dimension: int,
    a: int,
    b: int,
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    kappa_inverse: Polynomial,
) -> ExteriorForm:
    """Direct ordered definition P_IJ=[2 kappa (D-2)!]^-1 epsilon_IJ...E...."""
    orientation = tuple(range(dimension))
    remaining = tuple(index for index in orientation if index not in (a, b))
    if len(remaining) != dimension - 2 or a == b:
        raise UnsupportedSectorError("Palatini component requires distinct in-range indices")
    prefactor = Fraction(1, 2 * factorial(dimension - 2))
    result = algebra.zero()
    for tail in permutations(remaining):
        epsilon = levi_civita_sign((a, b) + tail, orientation)
        result = result + wedge_all(algebra, tuple(coframes[index] for index in tail)).scale(
            kappa_inverse * prefactor * epsilon
        )
    return result


def displayed_persistent_component(
    a: int,
    b: int,
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    kappa_inverse: Polynomial,
    *,
    five_dimensional: bool,
) -> ExteriorForm:
    result = algebra.zero()
    for c in INTERNAL4:
        for d in INTERNAL4:
            epsilon = levi_civita_sign((a, b, c, d), INTERNAL4)
            if epsilon:
                factors = [coframes[c], coframes[d]]
                if five_dimensional:
                    factors.append(coframes[4])
                result = result + wedge_all(algebra, tuple(factors)).scale(
                    kappa_inverse * Fraction(epsilon, 4)
                )
    return result


def factorial(value: int) -> int:
    result = 1
    for factor in range(2, value + 1):
        result *= factor
    return result


def inversion_sign(word: tuple[int, ...]) -> int:
    inversions = sum(
        word[left] > word[right]
        for left in range(len(word))
        for right in range(left + 1, len(word))
    )
    return -1 if inversions % 2 else 1


def dense_hand_component(dimension: int, a: int, b: int) -> dict[tuple[int, ...], Fraction]:
    """Alternate local permutation/word assembly, independent of kernel epsilon/wedge."""
    remaining = tuple(index for index in range(dimension) if index not in (a, b))
    prefactor = Fraction(1, 2 * factorial(dimension - 2))
    result: dict[tuple[int, ...], Fraction] = {}
    for tail in permutations(remaining):
        epsilon = inversion_sign((a, b) + tail)
        wedge_sign = inversion_sign(tail)
        canonical = tuple(sorted(tail))
        result[canonical] = result.get(canonical, ZERO) + prefactor * epsilon * wedge_sign
    return {word: coefficient for word, coefficient in result.items() if coefficient}


def fiber_pushforward(
    form: ExteriorForm, target: ExteriorAlgebra, tau: Polynomial, *, normalized: bool
) -> ExteriorForm:
    if form.algebra.basis != target.basis + ("dtheta",):
        raise UnsupportedSectorError("fiber source must be target basis followed by dtheta")
    terms = []
    for word, coefficient in form.terms:
        if "dtheta" not in word:
            continue
        if word[-1] != "dtheta":
            raise UnsupportedSectorError("fiber leg is not rightmost")
        terms.append((word[:-1], coefficient if normalized else coefficient * tau))
    return target.from_terms(terms)


def transpose(matrix: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix[0])))


def matmul(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> tuple[tuple[Fraction, ...], ...]:
    right_t = transpose(right)
    return tuple(
        tuple(sum((x * y for x, y in zip(row, column)), ZERO) for column in right_t)
        for row in left
    )


def identity(size: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ONE if i == j else ZERO for j in range(size)) for i in range(size))


def lorentz_inverse(g: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    metric = tuple(tuple(Fraction(ETA[i]) if i == j else ZERO for j in INTERNAL4) for i in INTERNAL4)
    return matmul(matmul(metric, transpose(g)), metric)


def generator_matrix(pair: tuple[int, int]) -> tuple[tuple[Fraction, ...], ...]:
    a, b = pair
    rows = [[ZERO for _ in INTERNAL4] for _ in INTERNAL4]
    rows[b][a] = Fraction(ETA[a])
    rows[a][b] = Fraction(-ETA[b])
    return tuple(tuple(row) for row in rows)


def adjoint_matrix(g: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    inverse = lorentz_inverse(g)
    columns = []
    for pair in PAIRS:
        transformed = matmul(matmul(g, generator_matrix(pair)), inverse)
        columns.append(tuple(transformed[b][a] / ETA[a] for a, b in PAIRS))
    return tuple(tuple(columns[column][row] for column in range(6)) for row in range(6))


def form_vector_scale(vector: Sequence[ExteriorForm], scalar: int | Fraction) -> tuple[ExteriorForm, ...]:
    return tuple(entry.scale(scalar) for entry in vector)


def form_vector_add(left: Sequence[ExteriorForm], right: Sequence[ExteriorForm]) -> tuple[ExteriorForm, ...]:
    return tuple(a + b for a, b in zip(left, right))


def form_matvec(
    matrix: Sequence[Sequence[Fraction]], vector: Sequence[ExteriorForm]
) -> tuple[ExteriorForm, ...]:
    algebra = vector[0].algebra
    return tuple(
        sum((vector[column].scale(entry) for column, entry in enumerate(row)), algebra.zero())
        for row in matrix
    )


def vector_zero(vector: Sequence[ExteriorForm]) -> bool:
    return all(entry.is_zero for entry in vector)


def total_residual(
    p: Sequence[ExteriorForm],
    q: Sequence[ExteriorForm],
    ad_g: Sequence[Sequence[Fraction]],
    ad_g_inverse: Sequence[Sequence[Fraction]],
    mutation: str = "",
) -> tuple[ExteriorForm, ...]:
    lam = q if mutation == "lambda-sign" else form_vector_scale(q, -1)
    exterior = p if mutation == "exterior-sign" else form_vector_scale(p, -1)
    if mutation == "dressing-omit":
        dressed_lambda = lam
    elif mutation == "dressing-invert":
        dressed_lambda = form_matvec(ad_g, lam)
    else:
        dressed_lambda = form_matvec(ad_g_inverse, lam)
    return form_vector_add(exterior, form_vector_scale(dressed_lambda, -1))


def check() -> int:
    if MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(f"unsupported O007_INTENTIONAL_MUTATION={MUTATION!r}")
    record = Recorder()
    tau = Polynomial.generator("tau")
    rho = Polynomial.generator("rho")
    radius = Polynomial.generator("R")
    k4 = Polynomial.generator("kappa4_inv")
    k5 = Polynomial.generator("kappa5_inv")

    # Universal ordered Palatini coefficient reconstruction.
    alg4 = ExteriorAlgebra(("E0", "E1", "E2", "E3"))
    e4 = {i: alg4.basis_form(f"E{i}") for i in INTERNAL4}
    raw4 = palatini_component(4, 0, 3, alg4, e4, k4)
    shown4 = displayed_persistent_component(0, 3, alg4, e4, k4, five_dimensional=False)
    expected4 = e4[1].wedge(e4[2]).scale(k4 * Fraction(1, 2))
    record.require("palatini.4d_ordered_coefficient_one_quarter", raw4 == shown4 == expected4)
    record.require(
        "palatini.4d_all_six_components_match_displayed_formula",
        all(
            palatini_component(4, a, b, alg4, e4, k4)
            == displayed_persistent_component(a, b, alg4, e4, k4, five_dimensional=False)
            for a, b in PAIRS
        ),
    )

    alg5 = ExteriorAlgebra(("E0", "E1", "E2", "E3", "E4"))
    e5 = {i: alg5.basis_form(f"E{i}") for i in INTERNAL5}
    raw5 = palatini_component(5, 0, 3, alg5, e5, k5)
    shown5 = displayed_persistent_component(0, 3, alg5, e5, k5, five_dimensional=True)
    expected5 = e5[1].wedge(e5[2]).wedge(e5[4]).scale(k5 * Fraction(1, 2))
    record.require("palatini.5d_persistent_coefficient_one_quarter", raw5 == shown5 == expected5)
    record.require(
        "palatini.5d_all_six_persistent_components_match_displayed_formula",
        all(
            palatini_component(5, a, b, alg5, e5, k5)
            == displayed_persistent_component(a, b, alg5, e5, k5, five_dimensional=True)
            for a, b in PAIRS
        ),
    )
    hand4 = dense_hand_component(4, 0, 3)
    hand5 = dense_hand_component(5, 0, 3)
    record.require("crosscheck.dense_4d_component", hand4 == {(1, 2): Fraction(1, 2)})
    record.require("crosscheck.dense_5d_component", hand5 == {(1, 2, 4): Fraction(1, 2)})

    # Adapted planar core and exact circle pushforwards.
    circle = ExteriorAlgebra(("dx1", "dx2", "dtheta"))
    cut = ExteriorAlgebra(("dx1", "dx2"))
    dx1, dx2, dtheta = (circle.basis_form(label) for label in circle.basis)
    core_coframes = {0: circle.zero(), 1: dx1, 2: dx2, 3: circle.zero(), 4: dtheta.scale(rho)}
    core = tuple(
        displayed_persistent_component(a, b, circle, core_coframes, k5, five_dimensional=True)
        for a, b in PAIRS
    )
    ordinary = tuple(fiber_pushforward(form, cut, tau, normalized=False) for form in core)
    normalized = tuple(fiber_pushforward(form, cut, tau, normalized=True) for form in core)
    area = cut.basis_form("dx1").wedge(cut.basis_form("dx2"))
    expected_ordinary03 = area.scale(tau * rho * k5 * Fraction(1, 2))
    expected_normalized03 = area.scale(rho * k5 * Fraction(1, 2))
    record.require("core.ordinary_proportional_rho", ordinary[PAIR_INDEX[(0, 3)]] == expected_ordinary03)
    record.require("core.normalized_proportional_rho", normalized[PAIR_INDEX[(0, 3)]] == expected_normalized03)
    record.require("core.only_planar_03_component", all(form.is_zero for i, form in enumerate(ordinary) if i != PAIR_INDEX[(0, 3)]))
    collapsed_ordinary = tuple(substitute_form(form, {"rho": 0}) for form in ordinary)
    collapsed_normalized = tuple(substitute_form(form, {"rho": 0}) for form in normalized)
    record.require("core.ordinary_exact_zero_at_rho_zero", vector_zero(collapsed_ordinary))
    record.require("core.normalized_exact_zero_at_rho_zero", vector_zero(collapsed_normalized))

    fixed_ordinary = tuple(substitute_form(form, {"rho": radius}) for form in ordinary)
    fixed_normalized = tuple(substitute_form(form, {"rho": radius}) for form in normalized)
    exterior_cut_coframes = {
        0: cut.zero(),
        1: cut.basis_form("dx1"),
        2: cut.basis_form("dx2"),
        3: cut.zero(),
    }
    exterior_p = tuple(
        displayed_persistent_component(
            a, b, cut, exterior_cut_coframes, k4, five_dimensional=False
        )
        for a, b in PAIRS
    )
    record.require(
        "exterior.planar_P03_exact",
        exterior_p[PAIR_INDEX[(0, 3)]] == area.scale(k4 * Fraction(1, 2)),
    )
    fixed_ordinary_matched = tuple(
        substitute_form(form, {"kappa4_inv": tau * radius * k5})
        for form in form_vector_add(fixed_ordinary, form_vector_scale(exterior_p, -1))
    )
    fixed_normalized_matched = tuple(
        substitute_form(form, {"kappa4_inv": radius * k5})
        for form in form_vector_add(fixed_normalized, form_vector_scale(exterior_p, -1))
    )
    record.require("fixed_radius.ordinary_nonzero", not vector_zero(fixed_ordinary))
    record.require("fixed_radius.normalized_nonzero", not vector_zero(fixed_normalized))
    record.require("fixed_radius.ordinary_normalization_matches_4d", vector_zero(fixed_ordinary_matched))
    record.require("fixed_radius.normalized_normalization_matches_4d", vector_zero(fixed_normalized_matched))

    # Exact shell cancellation and dressing-sensitive witnesses.
    identity4 = identity(4)
    boost = (
        (Fraction(5, 3), Fraction(4, 3), ZERO, ZERO),
        (Fraction(4, 3), Fraction(5, 3), ZERO, ZERO),
        (ZERO, ZERO, ONE, ZERO),
        (ZERO, ZERO, ZERO, ONE),
    )
    p = exterior_p
    id_ad = adjoint_matrix(identity4)
    boost_inverse = lorentz_inverse(boost)
    boost_ad = adjoint_matrix(boost)
    boost_ad_inverse = adjoint_matrix(boost_inverse)
    record.require("lorentz.identity_adjoint", id_ad == identity(6))
    record.require("lorentz.boost_inverse_exact", matmul(boost, boost_inverse) == identity4)
    record.require("lorentz.adjoint_inverse_exact", matmul(boost_ad, boost_ad_inverse) == identity(6))
    q_identity = form_matvec(id_ad, p)
    q_boost = form_matvec(boost_ad, p)
    q_boost_unit = tuple(substitute_form(form, {"kappa4_inv": 1}) for form in q_boost)
    record.require("crosscheck.boost_Q03_hand_value_5_over_6", q_boost_unit[PAIR_INDEX[(0, 3)]] == area.scale(Fraction(5, 6)))
    record.require("crosscheck.boost_Q13_hand_value_2_over_3", q_boost_unit[PAIR_INDEX[(1, 3)]] == area.scale(Fraction(2, 3)))

    identity_residual = total_residual(p, q_identity, id_ad, id_ad, MUTATION)
    boost_residual = total_residual(p, q_boost, boost_ad, boost_ad_inverse, MUTATION)
    record.require("cancellation.identity_exact_zero", vector_zero(identity_residual))
    record.require("cancellation.nonidentity_exact_zero", vector_zero(boost_residual))
    reversed_p = form_vector_scale(p, -1)
    reversed_q = form_matvec(boost_ad, reversed_p)
    reversed_residual = total_residual(reversed_p, reversed_q, boost_ad, boost_ad_inverse, MUTATION)
    record.require("cancellation.common_orientation_reversal_zero", vector_zero(reversed_residual))

    mutation_effective = {}
    for name in ("exterior-sign", "lambda-sign", "dressing-omit", "dressing-invert"):
        witness_q = q_identity if name in {"exterior-sign", "lambda-sign"} else q_boost
        witness_ad = id_ad if name in {"exterior-sign", "lambda-sign"} else boost_ad
        witness_inverse = id_ad if name in {"exterior-sign", "lambda-sign"} else boost_ad_inverse
        mutation_effective[name] = not vector_zero(total_residual(p, witness_q, witness_ad, witness_inverse, name))
        record.require(f"mutation.{name}_discriminating", mutation_effective[name])

    observations = {
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": ["openai/gpt-5.6-sol"],
        "intentional_mutation": MUTATION or None,
        "assertions": {
            "total": record.total,
            "passed": len(record.passed),
            "failed": len(record.failed),
            "failed_names": record.failed,
        },
        "representation": {
            "coefficients": "Fraction and free sparse Polynomial over Fraction",
            "forms": "canonical exact_graded sparse exterior maps",
            "lorentz_pairs": [f"{a}{b}" for a, b in PAIRS],
            "float_tolerance_random_cas": False,
        },
        "palatini": {"hand_4d": str(hand4), "hand_5d": str(hand5)},
        "core": {
            "ordinary_03": ordinary[PAIR_INDEX[(0, 3)]].to_data(),
            "normalized_03": normalized[PAIR_INDEX[(0, 3)]].to_data(),
            "collapsed_ordinary_zero": vector_zero(collapsed_ordinary),
            "collapsed_normalized_zero": vector_zero(collapsed_normalized),
        },
        "boost_hand_control": {"Q03": "5/6", "Q13": "2/3"},
        "mutation_controls": mutation_effective,
    }
    emit_observations(observations)
    if record.failed:
        for name in record.failed:
            print(f"FAILED: {name}", file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        outcome = check()
    except UnsupportedSectorError as exc:
        emit_observations({"obligation_id": OBLIGATION_ID, "inconclusive_reason": str(exc)})
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    return outcome if outcome in {PASSED, FAILED, INCONCLUSIVE} else ERROR


if __name__ == "__main__":
    raise SystemExit(main())
