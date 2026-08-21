#!/usr/bin/env python3
"""Executable implementation of machine-check obligation O002.

Run this only through the deterministic wrapper:

    uv run --locked python scripts/run_check.py O002

This file decides nothing canonical. It performs the declared test and reports
the process exit status; `scripts/run_check.py` records the canonical outcome in
`result.json`. Do not write `result.json` from here.

Exit protocol:

    0 -> the declared acceptance criterion was met
    1 -> the declared acceptance criterion was not met
    2 -> the check could not decide (inconclusive)
    3 -> execution error

Optional structured observations may be emitted with `emit_observations({...})`.
The wrapper stores them as data; they never choose the outcome.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from fractions import Fraction
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import sys
from typing import Any


OBLIGATION_ID = "O002"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]

# Keep the fingerprinted infrastructure directory byte-for-byte stable while
# this process imports it.  The complete directory, including any pre-existing
# caches, is declared in spec.yaml.
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra,
    ExteriorForm,
    Polynomial,
    levi_civita_sign,
)

PASSED = 0
FAILED = 1
INCONCLUSIVE = 2
ERROR = 3

OBSERVATION_PREFIX = "##OBSERVATIONS##"

PRODUCER_MODEL = "openai/gpt-5.6-sol"
INTERNAL_MUTATION = os.environ.get("O002_INTERNAL_MUTATION", "")
SUPPORTED_INTERNAL_MUTATIONS = {"", "total-sign"}


class UnsupportedSectorError(ValueError):
    """A requested object is outside the predeclared regular bare sector."""


def wedge_all(algebra: ExteriorAlgebra, factors: Iterable[ExteriorForm]) -> ExteriorForm:
    """Wedge factors from left to right in one declared algebra."""

    result = algebra.unit()
    for factor in factors:
        result = result.wedge(factor)
    return result


def substitute_form(
    form: ExteriorForm,
    replacements: Mapping[str, Polynomial | int | Fraction],
) -> ExteriorForm:
    """Apply an exact simultaneous substitution to every form coefficient."""

    return form.algebra.from_terms(
        (monomial, coefficient.substitute(replacements))
        for monomial, coefficient in form.terms
    )


def coordinate_pullback(
    form: ExteriorForm,
    target: ExteriorAlgebra,
    *,
    zero_generators: frozenset[str],
) -> ExteriorForm:
    """Pull back coordinate one-forms, sending declared normal legs to zero."""

    source = form.algebra
    images: dict[str, ExteriorForm] = {}
    for label in source.basis:
        if label in zero_generators:
            images[label] = target.zero()
        elif label in target.basis:
            images[label] = target.basis_form(label)
        else:
            raise UnsupportedSectorError(f"no pullback image declared for {label!r}")
    return form.pullback(target, images)


def fiber_pushforward(
    form: ExteriorForm,
    target: ExteriorAlgebra,
    *,
    normalized_haar: bool,
    tau: Polynomial,
) -> ExteriorForm:
    """Extract a rightmost dtheta and apply ordinary or normalized circle mass."""

    source = form.algebra
    if not source.basis or source.basis[-1] != "dtheta":
        raise UnsupportedSectorError("fiber source must declare dtheta as its final basis leg")
    if target.basis != source.basis[:-1]:
        raise UnsupportedSectorError("fiber target must be the source basis with dtheta removed")

    terms: list[tuple[tuple[str, ...], Polynomial]] = []
    for monomial, coefficient in form.terms:
        if "dtheta" not in monomial:
            continue
        if monomial[-1] != "dtheta":
            raise UnsupportedSectorError("fiber leg is not in the declared rightmost convention")
        pushed = coefficient if normalized_haar else coefficient * tau
        terms.append((monomial[:-1], pushed))
    return target.from_terms(terms)


def constant_coefficient(coefficient: Polynomial) -> Fraction:
    if coefficient.is_zero:
        return Fraction(0)
    if len(coefficient.terms) != 1 or coefficient.terms[0][0] != ():
        raise ValueError("a rational proportionality check received a nonconstant coefficient")
    return coefficient.terms[0][1]


def constant_form_ratio(actual: ExteriorForm, template: ExteriorForm) -> Fraction:
    """Return the unique exact rational r with actual=r*template."""

    if actual.algebra != template.algebra or actual.is_zero or template.is_zero:
        raise ValueError("proportional forms must be nonzero members of one algebra")
    actual_map = dict(actual.terms)
    template_map = dict(template.terms)
    if actual_map.keys() != template_map.keys():
        raise ValueError("proportional forms have different canonical supports")
    ratios = {
        constant_coefficient(actual_map[monomial])
        / constant_coefficient(template_map[monomial])
        for monomial in actual_map
    }
    if len(ratios) != 1:
        raise ValueError("no unique rational proportionality coefficient exists")
    return next(iter(ratios))


def antisymmetric_component(
    components: Mapping[tuple[int, int], ExteriorForm],
    first: int,
    second: int,
    algebra: ExteriorAlgebra,
) -> ExteriorForm:
    if first == second:
        return algebra.zero()
    if first < second:
        return components.get((first, second), algebra.zero())
    return -components.get((second, first), algebra.zero())


def ordered_theta5(
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    variations: Mapping[tuple[int, int], ExteriorForm],
    kappa5_inv: Polynomial,
) -> ExteriorForm:
    """Evaluate D004 (24) by its complete ordered five-index sum."""

    result = algebra.zero()
    for indices in permutations(range(5)):
        first, second, third, fourth, fifth = indices
        epsilon = levi_civita_sign(indices, (0, 1, 2, 3, 4))
        term = wedge_all(
            algebra,
            (
                antisymmetric_component(variations, first, second, algebra),
                coframes[third],
                coframes[fourth],
                coframes[fifth],
            ),
        )
        result = result + term.scale(kappa5_inv * Fraction(epsilon, 12))
    return result


def ordered_theta4(
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    variations: Mapping[tuple[int, int], ExteriorForm],
    kappa4_inv: Polynomial,
) -> ExteriorForm:
    """Evaluate D004 (26) by its complete ordered four-index sum."""

    result = algebra.zero()
    for indices in permutations(range(4)):
        first, second, third, fourth = indices
        epsilon = levi_civita_sign(indices, (0, 1, 2, 3))
        term = wedge_all(
            algebra,
            (
                antisymmetric_component(variations, first, second, algebra),
                coframes[third],
                coframes[fourth],
            ),
        )
        result = result + term.scale(kappa4_inv * Fraction(epsilon, 4))
    return result


def parity(indices: tuple[int, ...]) -> int:
    """Independent inversion-parity implementation for the dense cross-check."""

    inversions = sum(
        indices[left] > indices[right]
        for left in range(len(indices))
        for right in range(left + 1, len(indices))
    )
    return -1 if inversions % 2 else 1


def dense_contract_word(
    word: tuple[str, ...], label: str, normal_coefficient: int
) -> tuple[Fraction, tuple[str, ...]]:
    """Independent left contraction of one dense exterior word."""

    if label not in word:
        return Fraction(0), ()
    position = word.index(label)
    sign = -1 if position % 2 else 1
    return Fraction(normal_coefficient * sign), word[:position] + word[position + 1 :]


DenseForm = dict[tuple[str, ...], Fraction]


def canonical_dense_word(
    word: tuple[str, ...], order: Mapping[str, int]
) -> tuple[int, tuple[str, ...]]:
    if len(set(word)) != len(word):
        return 0, ()
    inversions = sum(
        order[word[left]] > order[word[right]]
        for left in range(len(word))
        for right in range(left + 1, len(word))
    )
    return (-1 if inversions % 2 else 1), tuple(sorted(word, key=order.__getitem__))


def dense_add_term(
    target: DenseForm,
    word: tuple[str, ...],
    coefficient: Fraction,
    order: Mapping[str, int],
) -> None:
    sign, canonical = canonical_dense_word(word, order)
    if not sign or not coefficient:
        return
    updated = target.get(canonical, Fraction(0)) + sign * coefficient
    if updated:
        target[canonical] = updated
    else:
        target.pop(canonical, None)


def dense_scale(form: DenseForm, scalar: Fraction) -> DenseForm:
    return {
        word: coefficient * scalar
        for word, coefficient in form.items()
        if coefficient * scalar
    }


def dense_sum(*forms: DenseForm) -> DenseForm:
    result: DenseForm = {}
    for form in forms:
        for word, coefficient in form.items():
            updated = result.get(word, Fraction(0)) + coefficient
            if updated:
                result[word] = updated
            else:
                result.pop(word, None)
    return result


def dense_atom_substitute(
    polynomial: DenseForm,
    atom: str,
    replacement: tuple[str, ...],
) -> DenseForm:
    """Substitute one commuting atom in a tiny exact dense polynomial map."""

    result: DenseForm = {}
    for monomial, coefficient in polynomial.items():
        expanded: list[str] = []
        for factor in monomial:
            expanded.extend(replacement if factor == atom else (factor,))
        canonical = tuple(sorted(expanded))
        updated = result.get(canonical, Fraction(0)) + coefficient
        if updated:
            result[canonical] = updated
        else:
            result.pop(canonical, None)
    return result


def dense_ratio(actual: DenseForm, template: DenseForm) -> Fraction:
    if not actual or not template or actual.keys() != template.keys():
        raise ValueError("dense proportionality supports differ or are empty")
    ratios = {actual[word] / template[word] for word in actual}
    if len(ratios) != 1:
        raise ValueError("dense objects have no unique proportionality coefficient")
    return next(iter(ratios))


def form_as_constant_dense(form: ExteriorForm) -> DenseForm:
    return {word: constant_coefficient(coefficient) for word, coefficient in form.terms}


def form_data(form: ExteriorForm) -> dict[str, Any]:
    return form.to_data()


def emit_observations(observations: dict[str, Any]) -> None:
    """Emit one structured, machine-readable observation record to stdout."""
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


def check() -> int:
    """Execute every exact assertion and declared sensitivity control."""

    if INTERNAL_MUTATION not in SUPPORTED_INTERNAL_MUTATIONS:
        raise ValueError(f"unsupported O002_INTERNAL_MUTATION={INTERNAL_MUTATION!r}")

    assertions: dict[str, bool] = {}

    def expect(name: str, condition: bool) -> None:
        if name in assertions:
            raise RuntimeError(f"duplicate assertion name {name!r}")
        assertions[name] = bool(condition)

    # Exact coefficient atoms.  tau is a formal period interpreted as 2*pi.
    tau = Polynomial.generator("tau")
    radius = Polynomial.generator("R")
    rho0 = Polynomial.generator("rho0")
    chi0 = Polynomial.generator("chi0")
    f = Polynomial.generator("f")
    a = Polynomial.generator("a")
    b0 = Polynomial.generator("b0")
    kappa4_inv = Polynomial.generator("kappa4_inv")
    kappa5_inv = Polynomial.generator("kappa5_inv")

    # D003 orientations reconstructed by outward-normal-first contraction.
    core_bulk = ExteriorAlgebra(("du0", "du1", "du2", "ds", "dtheta"))
    exterior_bulk = ExteriorAlgebra(("du0", "du1", "du2", "ds"))
    circle_boundary = ExteriorAlgebra(("du0", "du1", "du2", "dtheta"))
    sigma = ExteriorAlgebra(("du0", "du1", "du2"))

    core_o_sigma = wedge_all(
        core_bulk,
        (core_bulk.basis_form("du0"), core_bulk.basis_form("du1"), core_bulk.basis_form("du2")),
    )
    o5 = core_o_sigma.wedge(core_bulk.basis_form("ds")).wedge(
        core_bulk.basis_form("dtheta")
    )
    core_boundary_orientation = -o5.contract(core_bulk.basis_vector("ds"))
    expected_core_orientation = core_o_sigma.wedge(core_bulk.basis_form("dtheta"))

    exterior_o_sigma = wedge_all(
        exterior_bulk,
        (
            exterior_bulk.basis_form("du0"),
            exterior_bulk.basis_form("du1"),
            exterior_bulk.basis_form("du2"),
        ),
    )
    o4 = exterior_o_sigma.wedge(exterior_bulk.basis_form("ds"))
    exterior_boundary_orientation = o4.contract(exterior_bulk.basis_vector("ds"))
    expected_exterior_orientation = -exterior_o_sigma

    expect("P01.core_boundary_orientation", core_boundary_orientation == expected_core_orientation)
    expect(
        "P01.exterior_boundary_orientation",
        exterior_boundary_orientation == expected_exterior_orientation,
    )
    expect(
        "P01.opposite_incidence_signs",
        not core_boundary_orientation.is_zero and not exterior_boundary_orientation.is_zero,
    )
    dense_core_sign, dense_core_word = dense_contract_word(
        ("du0", "du1", "du2", "ds", "dtheta"), "ds", -1
    )
    dense_exterior_sign, dense_exterior_word = dense_contract_word(
        ("du0", "du1", "du2", "ds"), "ds", 1
    )
    expect(
        "P01.dense_core_boundary_orientation",
        dense_core_sign == 1 and dense_core_word == ("du0", "du1", "du2", "dtheta"),
    )
    expect(
        "P01.dense_exterior_boundary_orientation",
        dense_exterior_sign == -1 and dense_exterior_word == ("du0", "du1", "du2"),
    )
    expect("S01.epsilon_01234", levi_civita_sign((0, 1, 2, 3, 4), (0, 1, 2, 3, 4)) == 1)
    expect("S01.epsilon_0123", levi_civita_sign((0, 1, 2, 3), (0, 1, 2, 3)) == 1)
    expect(
        "S01.epsilon_abcd_equals_abcd4",
        all(
            levi_civita_sign(indices, (0, 1, 2, 3))
            == levi_civita_sign(indices + (4,), (0, 1, 2, 3, 4))
            for indices in permutations(range(4))
        ),
    )

    # Generic boundary-relevant alpha4.  Pullback kills a4 and descent sets b0=0.
    alpha4 = (
        core_o_sigma.wedge(core_bulk.basis_form("ds")).scale(a)
        + core_o_sigma.wedge(core_bulk.basis_form("dtheta")).scale(b0)
    )
    generic_trace = coordinate_pullback(
        alpha4,
        circle_boundary,
        zero_generators=frozenset({"ds"}),
    )
    descended_trace = substitute_form(generic_trace, {"b0": 0})
    ordinary_generic = fiber_pushforward(
        generic_trace, sigma, normalized_haar=False, tau=tau
    )
    haar_generic = fiber_pushforward(generic_trace, sigma, normalized_haar=True, tau=tau)
    ordinary_descended = fiber_pushforward(
        descended_trace, sigma, normalized_haar=False, tau=tau
    )
    haar_descended = fiber_pushforward(
        descended_trace, sigma, normalized_haar=True, tau=tau
    )
    sigma_o = wedge_all(
        sigma,
        (sigma.basis_form("du0"), sigma.basis_form("du1"), sigma.basis_form("du2")),
    )
    boundary_o = wedge_all(
        circle_boundary,
        (
            circle_boundary.basis_form("du0"),
            circle_boundary.basis_form("du1"),
            circle_boundary.basis_form("du2"),
        ),
    )
    boundary_o_theta = boundary_o.wedge(circle_boundary.basis_form("dtheta"))
    expect("P02.generic_trace_before_descent", generic_trace == boundary_o_theta.scale(b0))
    expect("P02.descended_trace_zero", descended_trace.is_zero)
    expect("P02.ordinary_descended_zero", ordinary_descended.is_zero)
    expect("P02.haar_descended_zero", haar_descended.is_zero)
    expect("P02.ordinary_generic_exact", ordinary_generic == sigma_o.scale(tau * b0))
    expect("P02.haar_generic_exact", haar_generic == sigma_o.scale(b0))
    expect("N01.resolution_trace_nonzero", not generic_trace.is_zero)
    expect("N01.resolution_ordinary_nonzero", not ordinary_generic.is_zero)
    expect("N01.resolution_haar_nonzero", not haar_generic.is_zero)
    dense_alpha = (
        (("du0", "du1", "du2", "ds"), "a"),
        (("du0", "du1", "du2", "dtheta"), "b0"),
    )
    dense_resolution_trace = tuple(
        (word, coefficient) for word, coefficient in dense_alpha if "ds" not in word
    )
    dense_descended_trace = tuple(
        (word, coefficient)
        for word, coefficient in dense_resolution_trace
        if coefficient != "b0"
    )
    expect(
        "P02.dense_resolution_trace_before_descent",
        dense_resolution_trace
        == ((("du0", "du1", "du2", "dtheta"), "b0"),),
    )
    expect("P02.dense_descended_trace_zero", not dense_descended_trace)
    expect("P02.dense_descended_pushforwards_zero", not dense_descended_trace)

    # Universal primary reconstruction of D004 (31) in a free odd-generator algebra.
    pair_labels = tuple(f"w{first}{second}" for first, second in combinations(range(5), 2))
    coframe_labels = tuple(f"E{index}" for index in range(5))
    internal = ExteriorAlgebra(pair_labels + coframe_labels)

    def omega_symbol(first: int, second: int) -> ExteriorForm:
        if first == second:
            return internal.zero()
        if first < second:
            return internal.basis_form(f"w{first}{second}")
        return -internal.basis_form(f"w{second}{first}")

    def e_symbol(index: int) -> ExteriorForm:
        return internal.basis_form(f"E{index}")

    full_raw = internal.zero()
    persistent_raw = internal.zero()
    mixed_raw = internal.zero()
    for indices in permutations(range(5)):
        first, second, third, fourth, fifth = indices
        epsilon = levi_civita_sign(indices, (0, 1, 2, 3, 4))
        term = wedge_all(
            internal,
            (omega_symbol(first, second), e_symbol(third), e_symbol(fourth), e_symbol(fifth)),
        ).scale(Fraction(epsilon, 12))
        full_raw = full_raw + term
        if first < 4 and second < 4:
            persistent_raw = persistent_raw + term
        else:
            mixed_raw = mixed_raw + term

    e4_structure = internal.zero()
    mixed_structure = internal.zero()
    for indices in permutations(range(4)):
        first, second, third, fourth = indices
        epsilon = levi_civita_sign(indices, (0, 1, 2, 3))
        e4_structure = e4_structure + wedge_all(
            internal,
            (omega_symbol(first, second), e_symbol(third), e_symbol(fourth), e_symbol(4)),
        ).scale(epsilon)
        mixed_structure = mixed_structure + wedge_all(
            internal,
            (omega_symbol(4, first), e_symbol(second), e_symbol(third), e_symbol(fourth)),
        ).scale(epsilon)

    primary_e4_coefficient = constant_form_ratio(persistent_raw, e4_structure)
    primary_mixed_coefficient = constant_form_ratio(mixed_raw, mixed_structure)
    expected_full_split = e4_structure.scale(Fraction(1, 4)) + mixed_structure.scale(
        Fraction(1, 6)
    )
    expect("P03.full_has_only_two_channels", full_raw == persistent_raw + mixed_raw)
    expect("P03.primary_e4_coefficient", primary_e4_coefficient == Fraction(1, 4))
    expect("P03.primary_mixed_coefficient", primary_mixed_coefficient == Fraction(1, 6))
    expect("P03.primary_split_identity", full_raw == expected_full_split)

    # Alternate unordered-pair/dense reconstruction.  It does not call the kernel's
    # wedge or epsilon operations and counts 2 pair orders x 3! coframe orders.
    dense_basis = pair_labels + coframe_labels
    dense_order = {label: position for position, label in enumerate(dense_basis)}
    dense_full: DenseForm = {}
    dense_persistent: DenseForm = {}
    dense_mixed: DenseForm = {}
    for first, second in combinations(range(5), 2):
        remaining = tuple(index for index in range(5) if index not in (first, second))
        coefficient = Fraction(2 * 6, 12) * parity((first, second) + remaining)
        word = (f"w{first}{second}",) + tuple(f"E{index}" for index in remaining)
        dense_add_term(dense_full, word, coefficient, dense_order)
        channel = dense_persistent if second < 4 else dense_mixed
        dense_add_term(channel, word, coefficient, dense_order)

    dense_e4_structure: DenseForm = {}
    dense_mixed_structure: DenseForm = {}
    for indices in permutations(range(4)):
        first, second, third, fourth = indices
        epsilon = parity(indices)
        if first < second:
            omega_label, omega_sign = f"w{first}{second}", 1
        else:
            omega_label, omega_sign = f"w{second}{first}", -1
        dense_add_term(
            dense_e4_structure,
            (omega_label, f"E{third}", f"E{fourth}", "E4"),
            Fraction(epsilon * omega_sign),
            dense_order,
        )
        # omega^(4a)=-omega^(a4) for the canonical unordered pair (a,4).
        dense_add_term(
            dense_mixed_structure,
            (f"w{first}4", f"E{second}", f"E{third}", f"E{fourth}"),
            Fraction(-epsilon),
            dense_order,
        )

    dense_e4_coefficient = dense_ratio(dense_persistent, dense_e4_structure)
    dense_mixed_coefficient = dense_ratio(dense_mixed, dense_mixed_structure)
    dense_expected_split = dense_sum(
        dense_scale(dense_e4_structure, Fraction(1, 4)),
        dense_scale(dense_mixed_structure, Fraction(1, 6)),
    )
    expect("P03.dense_matches_primary_full", dense_full == form_as_constant_dense(full_raw))
    expect(
        "P03.dense_matches_primary_persistent",
        dense_persistent == form_as_constant_dense(persistent_raw),
    )
    expect("P03.dense_matches_primary_mixed", dense_mixed == form_as_constant_dense(mixed_raw))
    expect("P03.dense_e4_coefficient", dense_e4_coefficient == Fraction(1, 4))
    expect("P03.dense_mixed_coefficient", dense_mixed_coefficient == Fraction(1, 6))
    expect("P03.dense_split_identity", dense_full == dense_expected_split)

    # D004 planar scientific-faithfulness witness on Sigma x S1.
    bu0 = circle_boundary.basis_form("du0")
    bu1 = circle_boundary.basis_form("du1")
    bu2 = circle_boundary.basis_form("du2")
    bdtheta = circle_boundary.basis_form("dtheta")
    horizontal_a = bu0 + bu1.scale(2)
    core_coframes = {
        0: bu0,
        1: bu1,
        2: bu2,
        3: circle_boundary.zero(),
        4: (bdtheta + horizontal_a).scale(rho0),
    }
    persistent_variation = {(0, 3): bu0.scale(f)}
    # Canonical component (3,4) is minus the desired deltaomega^(43).
    mixed_variation = {(3, 4): bdtheta.scale(-chi0)}
    all_variations = {**persistent_variation, **mixed_variation}

    theta5_e4 = ordered_theta5(
        circle_boundary, core_coframes, persistent_variation, kappa5_inv
    )
    theta5_mixed = ordered_theta5(
        circle_boundary, core_coframes, mixed_variation, kappa5_inv
    )
    theta5_full = ordered_theta5(circle_boundary, core_coframes, all_variations, kappa5_inv)
    expected_theta5_e4 = boundary_o_theta.scale(rho0 * f * kappa5_inv)
    expected_theta5_mixed = boundary_o_theta.scale(chi0 * kappa5_inv)
    expect("P04.planar_full_channel_sum", theta5_full == theta5_e4 + theta5_mixed)
    expect("P04.e4_channel_exact", theta5_e4 == expected_theta5_e4)
    expect("P04.mixed_channel_exact", theta5_mixed == expected_theta5_mixed)
    expect("P04.horizontal_A_part_zero", theta5_e4 == boundary_o_theta.scale(rho0 * f * kappa5_inv))
    expect("S02.mixed_dtheta_move_sign", bdtheta.wedge(boundary_o) == -boundary_o_theta)
    expect("N03.e4_channel_pretrace_nonzero", not theta5_e4.is_zero)
    expect("N03.mixed_channel_pretrace_nonzero", not theta5_mixed.is_zero)

    collapsed_e4 = substitute_form(theta5_e4, {"rho0": 0})
    collapsed_mixed = substitute_form(theta5_mixed, {"chi0": 0})
    collapsed_full = substitute_form(theta5_full, {"rho0": 0, "chi0": 0})
    expect("P04.e4_channel_collapsed_zero", collapsed_e4.is_zero)
    expect("P04.mixed_channel_collapsed_zero", collapsed_mixed.is_zero)
    expect("P04.full_core_collapsed_zero", collapsed_full.is_zero)
    collapsed_ordinary = fiber_pushforward(
        collapsed_full, sigma, normalized_haar=False, tau=tau
    )
    collapsed_haar = fiber_pushforward(
        collapsed_full, sigma, normalized_haar=True, tau=tau
    )
    expect("P04.collapsed_ordinary_zero", collapsed_ordinary.is_zero)
    expect("P04.collapsed_haar_zero", collapsed_haar.is_zero)

    # Exterior planar potential and the total core-minus-exterior incidence sign.
    su0 = sigma.basis_form("du0")
    su1 = sigma.basis_form("du1")
    su2 = sigma.basis_form("du2")
    exterior_coframes = {0: su0, 1: su1, 2: su2, 3: sigma.zero()}
    exterior_variation = {(0, 3): su0.scale(f)}
    theta4 = ordered_theta4(sigma, exterior_coframes, exterior_variation, kappa4_inv)
    expected_theta4 = sigma_o.scale(f * kappa4_inv)
    expect("P05.theta4_planar_exact", theta4 == expected_theta4)
    expect("N02.theta4_planar_nonzero", not theta4.is_zero)

    if INTERNAL_MUTATION == "total-sign":
        collapsed_residual = collapsed_ordinary + theta4
    else:
        collapsed_residual = collapsed_ordinary - theta4
    expected_collapsed_residual = sigma_o.scale(-(f * kappa4_inv))
    expect("P05.total_collapsed_residual", collapsed_residual == expected_collapsed_residual)

    # Fixed-radius product-circle limit and normalized-Haar counterpart.
    fixed_theta5 = substitute_form(theta5_full, {"rho0": radius, "chi0": 0})
    fixed_ordinary = fiber_pushforward(fixed_theta5, sigma, normalized_haar=False, tau=tau)
    fixed_haar = fiber_pushforward(fixed_theta5, sigma, normalized_haar=True, tau=tau)
    expected_fixed_ordinary = sigma_o.scale(tau * radius * f * kappa5_inv)
    expected_fixed_haar = sigma_o.scale(radius * f * kappa5_inv)
    fixed_residual = fixed_ordinary - theta4
    fixed_haar_residual = fixed_haar - theta4
    expected_fixed_residual = sigma_o.scale(
        (tau * radius * kappa5_inv - kappa4_inv) * f
    )
    expected_fixed_haar_residual = sigma_o.scale(
        (radius * kappa5_inv - kappa4_inv) * f
    )
    expect("P06.fixed_ordinary_core", fixed_ordinary == expected_fixed_ordinary)
    expect("P06.fixed_ordinary_residual", fixed_residual == expected_fixed_residual)
    expect("N03.unmatched_fixed_residual_nonzero", not fixed_residual.is_zero)
    fixed_matched = substitute_form(
        fixed_residual,
        {"kappa4_inv": tau * radius * kappa5_inv},
    )
    expect("P06.product_circle_relation_zero", fixed_matched.is_zero)
    expect("P07.fixed_haar_core", fixed_haar == expected_fixed_haar)
    expect("P07.fixed_haar_residual", fixed_haar_residual == expected_fixed_haar_residual)
    expect(
        "P07.haar_removes_exactly_one_tau",
        fixed_ordinary == fixed_haar.scale(tau) and fixed_ordinary != fixed_haar,
    )
    fixed_haar_matched = substitute_form(
        fixed_haar_residual,
        {"kappa4_inv": radius * kappa5_inv},
    )
    expect("P07.normalized_relation_zero", fixed_haar_matched.is_zero)

    # The alternate dense path also recovers the planar multiplicities and both
    # product-circle relations without using Polynomial or ExteriorForm equality.
    dense_planar_core_factor = dense_e4_coefficient * 4
    dense_planar_exterior_factor = Fraction(4, 4)
    dense_fixed_residual: DenseForm = {
        tuple(sorted(("R", "f", "kappa5_inv", "tau"))): dense_planar_core_factor,
        tuple(sorted(("f", "kappa4_inv"))): -dense_planar_exterior_factor,
    }
    dense_fixed_haar_residual: DenseForm = {
        tuple(sorted(("R", "f", "kappa5_inv"))): dense_planar_core_factor,
        tuple(sorted(("f", "kappa4_inv"))): -dense_planar_exterior_factor,
    }
    dense_fixed_matched = dense_atom_substitute(
        dense_fixed_residual,
        "kappa4_inv",
        ("R", "kappa5_inv", "tau"),
    )
    dense_fixed_haar_matched = dense_atom_substitute(
        dense_fixed_haar_residual,
        "kappa4_inv",
        ("R", "kappa5_inv"),
    )
    expect("P06.dense_planar_core_factor", dense_planar_core_factor == 1)
    expect("P05.dense_planar_exterior_factor", dense_planar_exterior_factor == 1)
    expect("P06.dense_product_circle_relation_zero", not dense_fixed_matched)
    expect("P07.dense_normalized_relation_zero", not dense_fixed_haar_matched)
    expect(
        "P07.dense_haar_removes_tau",
        any("tau" in monomial for monomial in dense_fixed_residual)
        and all("tau" not in monomial for monomial in dense_fixed_haar_residual),
    )

    # Declared mutations: every wrong sign, factor, trace, and normalization must
    # differ from the conclusion-critical exact target.
    expect("M01.core_orientation_reversal_detected", -expected_core_orientation != core_boundary_orientation)
    expect(
        "M02.exterior_orientation_reversal_detected",
        exterior_o_sigma != exterior_boundary_orientation,
    )
    expect("M03.forbidden_trace_retention_detected", generic_trace != descended_trace)
    expect("M04.ordinary_tau_drop_detected", haar_generic != ordinary_generic)
    expect("M05.haar_tau_retention_detected", ordinary_generic != haar_generic)
    mutated_quarter = e4_structure.scale(Fraction(1, 2)) + mixed_structure.scale(
        Fraction(1, 6)
    )
    mutated_sixth = e4_structure.scale(Fraction(1, 4)) + mixed_structure.scale(
        Fraction(1, 3)
    )
    expect("M06.quarter_factor_mutation_detected", mutated_quarter != full_raw)
    expect("M07.sixth_factor_mutation_detected", mutated_sixth != full_raw)
    expect(
        "M08.missing_rho_trace_zero_detected",
        not substitute_form(theta5_e4, {}).is_zero,
    )
    expect(
        "M09.missing_chi_trace_zero_detected",
        not substitute_form(theta5_mixed, {}).is_zero,
    )
    expect("M10.exterior_pair_factor_detected", theta4.scale(Fraction(1, 2)) != expected_theta4)
    expect(
        "M11.total_plus_sign_detected",
        collapsed_ordinary + theta4 != expected_collapsed_residual,
    )
    expect("M12.fixed_tau_drop_detected", fixed_haar_residual != expected_fixed_residual)
    wrong_relation = substitute_form(
        fixed_residual,
        {"kappa4_inv": -(tau * radius * kappa5_inv)},
    )
    expect("M13.fixed_relation_sign_detected", not wrong_relation.is_zero)

    failed = sorted(name for name, passed in assertions.items() if not passed)
    observations = {
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": [PRODUCER_MODEL],
        "internal_mutation": INTERNAL_MUTATION or "none",
        "representation": {
            "coefficient_domain": "free sparse Polynomial ring over Fraction",
            "equality": "exact canonical sparse-map equality",
            "primary": "exact_graded ordered sparse exterior algebra",
            "alternate": "claim-local unordered-pair dense coefficient enumeration",
            "tau_semantics": "formal exact circle period interpreted as 2*pi",
        },
        "boundary_orientations": {
            "core": form_data(core_boundary_orientation),
            "exterior": form_data(exterior_boundary_orientation),
        },
        "descended_trace": {
            "trace": form_data(descended_trace),
            "ordinary": form_data(ordinary_descended),
            "normalized_haar": form_data(haar_descended),
        },
        "palatini_split": {
            "primary_e4_coefficient": str(primary_e4_coefficient),
            "primary_mixed_coefficient": str(primary_mixed_coefficient),
            "dense_e4_coefficient": str(dense_e4_coefficient),
            "dense_mixed_coefficient": str(dense_mixed_coefficient),
        },
        "alternate_scientific_crosscheck": {
            "core_boundary_sign": str(dense_core_sign),
            "exterior_boundary_sign": str(dense_exterior_sign),
            "descended_trace_zero": not dense_descended_trace,
            "fixed_radius_matched_zero": not dense_fixed_matched,
            "normalized_radius_matched_zero": not dense_fixed_haar_matched,
        },
        "collapsed_channels": {
            "e4": form_data(collapsed_e4),
            "mixed": form_data(collapsed_mixed),
            "ordinary_total": form_data(collapsed_ordinary),
            "haar_total": form_data(collapsed_haar),
        },
        "exterior_planar_witness": form_data(theta4),
        "collapsed_residual": form_data(collapsed_residual),
        "fixed_radius": {
            "ordinary_residual": form_data(fixed_residual),
            "matched_residual": form_data(fixed_matched),
            "normalized_haar_residual": form_data(fixed_haar_residual),
            "normalized_matched_residual": form_data(fixed_haar_matched),
        },
        "assertion_count": len(assertions),
        "failed_assertion_count": len(failed),
        "failed_assertions": failed,
        "all_declared_controls_passed": not failed,
    }
    emit_observations(observations)
    if failed:
        print(f"{OBLIGATION_ID} failed assertions: " + ", ".join(failed), file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        outcome = check()
    except UnsupportedSectorError as exc:
        emit_observations(
            {
                "producer_model": PRODUCER_MODEL,
                "inconclusive_reason": str(exc),
            }
        )
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001 - an unhandled failure is an execution error
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    if outcome not in {PASSED, FAILED, INCONCLUSIVE}:
        print(f"{OBLIGATION_ID} returned an undefined status {outcome!r}", file=sys.stderr)
        return ERROR
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
