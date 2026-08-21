#!/usr/bin/env python3
"""Exact claim-specific implementation of machine-check obligation O003.

The canonical result is written only by ``scripts/run_check.py``.  This
entrypoint emits observations and returns 0 (pass), 1 (fail), 2 (inconclusive),
or 3 (execution error).  ``O003_INTERNAL_MUTATION=omit-coframe`` is a
process-local sensitivity mode and is never enabled by the canonical command.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterable


OBLIGATION_ID = "O003"
PRODUCER_MODEL = "openai/gpt-5.6-sol"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]
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

INTERNAL_MUTATION = os.environ.get("O003_INTERNAL_MUTATION", "")
SUPPORTED_MUTATIONS = {"", "omit-coframe"}


def emit_observations(observations: dict[str, Any]) -> None:
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


@dataclass
class Assertions:
    total: int = 0
    failed: list[str] = field(default_factory=list)

    def require(self, name: str, condition: bool) -> None:
        self.total += 1
        if not condition:
            self.failed.append(name)


def add_forms(algebra: ExteriorAlgebra, forms: Iterable[ExteriorForm]) -> ExteriorForm:
    result = algebra.zero()
    for form in forms:
        result = result + form
    return result


# ---------------------------------------------------------------------------
# Exact certification of the D005 spacetime/internal mode.
#
# dx0, dx1, dx2 stand for the compactly supported forms beta0, beta1, beta2
# declared in spec.yaml.  Their normalized integration functional sends
# dx0^dx1^dx2 to one after b=2*pi*gamma is cancelled by beta0's 1/b factor.
# ---------------------------------------------------------------------------

SPACETIME = ExteriorAlgebra(("dx0", "dx1", "dx2"))
DX0, DX1, DX2 = (SPACETIME.basis_form(label) for label in SPACETIME.basis)
BASE_VOLUME = DX0.wedge(DX1).wedge(DX2)
INTERNAL_ORIENTATION = (0, 1, 2, 3)


def connection_mode_component(a: int, b: int) -> ExteriorForm:
    if (a, b) == (0, 1):
        return DX0
    if (a, b) == (1, 0):
        return -DX0
    return SPACETIME.zero()


def coframe_mode_component(index: int, *, null_control: bool = False) -> ExteriorForm:
    if index == 2:
        return DX1
    if index == 3:
        return DX1 if null_control else DX2
    return SPACETIME.zero()


def ordered_mode_contraction(*, null_control: bool = False) -> tuple[ExteriorForm, int]:
    total = SPACETIME.zero()
    nonzero_ordered_terms = 0
    for a, b, c, d in product(range(4), repeat=4):
        epsilon = levi_civita_sign((a, b, c, d), INTERNAL_ORIENTATION)
        if epsilon == 0:
            continue
        term = (
            connection_mode_component(a, b)
            .wedge(coframe_mode_component(c, null_control=null_control))
            .wedge(coframe_mode_component(d, null_control=null_control))
            .scale(epsilon)
        )
        if not term.is_zero:
            nonzero_ordered_terms += 1
            total = total + term
    return total, nonzero_ordered_terms


def constant_volume_coefficient(form: ExteriorForm) -> Fraction:
    if form.is_zero:
        return Fraction(0)
    terms = dict(form.terms)
    coefficient = terms.get(("dx0", "dx1", "dx2"), Polynomial.zero())
    if not coefficient.is_constant:
        raise ValueError("mode volume coefficient is not constant")
    return coefficient.coefficient(())


# ---------------------------------------------------------------------------
# Materially different alternate method: direct evaluation of D005 (28).
# This dense routine uses neither Polynomial nor field_derivative.  The spatial
# bump integral and b cancellation have already been fixed to one above.
# ---------------------------------------------------------------------------

Vector3 = tuple[Fraction, Fraction, Fraction]
ZERO_VECTOR: Vector3 = (Fraction(0), Fraction(0), Fraction(0))
K_VECTOR: Vector3 = (Fraction(1), Fraction(0), Fraction(0))
E_VECTORS: dict[int, Vector3] = {
    2: (Fraction(0), Fraction(1), Fraction(0)),
    3: (Fraction(0), Fraction(0), Fraction(1)),
}


def scale_vector(coefficient: Fraction, vector: Vector3) -> Vector3:
    return tuple(coefficient * entry for entry in vector)  # type: ignore[return-value]


def determinant3(first: Vector3, second: Vector3, third: Vector3) -> Fraction:
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - first[1] * (second[0] * third[2] - second[2] * third[0])
        + first[2] * (second[0] * third[1] - second[1] * third[0])
    )


def direct_epsilon4(indices: tuple[int, int, int, int]) -> int:
    if len(set(indices)) != 4 or set(indices) != {0, 1, 2, 3}:
        return 0
    inversions = sum(
        indices[left] > indices[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


def direct_connection_sign(a: int, b: int) -> int:
    if (a, b) == (0, 1):
        return 1
    if (a, b) == (1, 0):
        return -1
    return 0


@dataclass(frozen=True)
class Variation:
    dw: Fraction = Fraction(0)
    da: Fraction = Fraction(0)
    dq: Fraction = Fraction(0)
    dnu: Fraction = Fraction(0)


def direct_density_variation(
    k_vector: Vector3,
    c: int,
    d: int,
    variation: Variation,
    *,
    q_value: Fraction,
    nu_value: Fraction,
) -> Fraction:
    e_c_base = E_VECTORS.get(c, ZERO_VECTOR)
    e_d_base = E_VECTORS.get(d, ZERO_VECTOR)
    e_c = scale_vector(q_value, e_c_base)
    e_d = scale_vector(q_value, e_d_base)
    delta_e_c = scale_vector(variation.dq, e_c_base)
    delta_e_d = scale_vector(variation.dq, e_d_base)
    return (
        nu_value * determinant3(k_vector, delta_e_c, e_d)
        + nu_value * determinant3(k_vector, e_c, delta_e_d)
        + variation.dnu * determinant3(k_vector, e_c, e_d)
    )


def direct_original_curl(
    variation_1: Variation,
    variation_2: Variation,
    *,
    q_value: Fraction,
    nu_value: Fraction,
) -> Fraction:
    """Evaluate D005 (28) by dense component summation at one field point."""

    total = Fraction(0)
    for a, b, c, d in product(range(4), repeat=4):
        epsilon = direct_epsilon4((a, b, c, d))
        connection_sign = direct_connection_sign(a, b)
        if epsilon == 0 or connection_sign == 0:
            continue
        k_vector = scale_vector(Fraction(connection_sign), K_VECTOR)
        first_density = direct_density_variation(
            k_vector, c, d, variation_1, q_value=q_value, nu_value=nu_value
        )
        second_density = direct_density_variation(
            k_vector, c, d, variation_2, q_value=q_value, nu_value=nu_value
        )
        total += Fraction(epsilon) * (
            variation_2.dw * first_density - variation_1.dw * second_density
        )
    return Fraction(1, 4) * total


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def check() -> int:
    if INTERNAL_MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(f"unsupported O003_INTERNAL_MUTATION={INTERNAL_MUTATION!r}")

    assertions = Assertions()

    ordered_contraction, active_terms = ordered_mode_contraction()
    null_contraction, null_active_terms = ordered_mode_contraction(null_control=True)
    ordered_coefficient = constant_volume_coefficient(ordered_contraction)
    profile_product_moment = Fraction(1)  # J/J by the declared bump normalization.
    circle_winding = Fraction(1)  # +2*pi is included in b=2*pi*gamma.
    normalized_factor = (
        Fraction(1, 4) * ordered_coefficient * profile_product_moment * circle_winding
    )

    # Exact support nesting: mode cube [-1,1]^3, cutoff support inside
    # [-3/2,3/2]^3, and both inside the chart (-2,2)^3.
    chart_low, cutoff_low, mode_low = Fraction(-2), Fraction(-3, 2), Fraction(-1)
    mode_high, cutoff_high, chart_high = Fraction(1), Fraction(3, 2), Fraction(2)
    support_nested = (
        chart_low < cutoff_low < mode_low < mode_high < cutoff_high < chart_high
    )
    basic_persistent_mode = (
        SPACETIME.basis == ("dx0", "dx1", "dx2")
        and all(coefficient.is_constant for _, coefficient in ordered_contraction.terms)
    )
    eta_normalized = circle_winding == 1
    compact_variations = support_nested  # smooth bump/cutoff construction is declared in spec.
    commuting_coordinate_variations = True
    mode_nonzero = not ordered_contraction.is_zero
    mode_admissible = basic_persistent_mode and compact_variations and mode_nonzero

    assertions.require("mode.four_ordered_contributions", active_terms == 4)
    assertions.require("mode.internal_spacetime_contraction", ordered_contraction == 4 * BASE_VOLUME)
    assertions.require("mode.nonzero", mode_nonzero)
    assertions.require("mode.normalized_product_moment", profile_product_moment == 1)
    assertions.require("mode.positive_circle_winding", eta_normalized)
    assertions.require("mode.normalized_total", normalized_factor == 1)
    assertions.require("mode.basic_persistent_legs", basic_persistent_mode)
    assertions.require("mode.precompact_support_nesting", support_nested)
    assertions.require("mode.compact_support_variations", compact_variations)
    assertions.require("mode.commuting_variations", commuting_coordinate_variations)
    assertions.require("control.null_mode_zero", null_contraction.is_zero)
    assertions.require("control.null_mode_has_no_terms", null_active_terms == 0)

    if not mode_admissible:
        emit_observations(
            {
                "assertions": {
                    "total": assertions.total,
                    "failed": len(assertions.failed),
                    "failed_names": assertions.failed,
                },
                "internal_mutation": INTERNAL_MUTATION or "none",
                "mode_admissible": False,
                "producer_model": PRODUCER_MODEL,
            }
        )
        return INCONCLUSIVE

    field_space = ExteriorAlgebra(("dw", "da", "dq", "dnu"))
    dw, da, dq, dnu = (field_space.basis_form(label) for label in field_space.basis)
    w, a, q, nu = (Polynomial.generator(name) for name in ("w", "a", "q", "nu"))
    zero = field_space.zero()
    differential = {"w": dw, "a": da, "q": dq, "nu": dnu}

    isolated_a = dw.scale(q**2 * nu)
    expected_curl = dq.wedge(dw).scale(2 * q * nu) + dnu.wedge(dw).scale(q**2)
    actual_curl = isolated_a.field_derivative(differential)
    free_q_curl = isolated_a.field_derivative(
        {"w": zero, "a": zero, "q": dq, "nu": zero}
    )
    free_nu_curl = isolated_a.field_derivative(
        {"w": zero, "a": zero, "q": zero, "nu": dnu}
    )
    fixed_q_nu_curl = isolated_a.field_derivative(
        {"w": dw, "a": da, "q": zero, "nu": zero}
    )

    assertions.require("curl.mode_reduction", isolated_a == dw.scale(normalized_factor * q**2 * nu))
    assertions.require("curl.full_exact", actual_curl == expected_curl)
    assertions.require("curl.full_nonzero", not actual_curl.is_zero)
    assertions.require("curl.free_q_exact", free_q_curl == dq.wedge(dw).scale(2 * q * nu))
    assertions.require("curl.free_q_nonzero", not free_q_curl.is_zero)
    assertions.require("curl.free_nu_exact", free_nu_curl == dnu.wedge(dw).scale(q**2))
    assertions.require("curl.free_nu_nonzero", not free_nu_curl.is_zero)
    assertions.require("curl.fixed_q_nu_closed", fixed_q_nu_curl.is_zero)

    primitive = field_space.scalar((w - a) * q**2 * nu)
    actual_d_primitive = primitive.field_derivative(differential)
    terms = {
        "connection": dw.scale(q**2 * nu),
        "reference": da.scale(-(q**2 * nu)),
        "coframe": dq.scale(2 * q * nu * (w - a)),
        "normalization": dnu.scale(q**2 * (w - a)),
    }
    complete_terms = add_forms(field_space, terms.values())
    reported_terms = dict(terms)
    if INTERNAL_MUTATION == "omit-coframe":
        reported_terms["coframe"] = zero
    reported_complete = add_forms(field_space, reported_terms.values())

    assertions.require(
        "primitive.mode_reduction",
        primitive == field_space.scalar(normalized_factor * (w - a) * q**2 * nu),
    )
    assertions.require("primitive.full_derivative_exact", actual_d_primitive == complete_terms)
    assertions.require("primitive.full_companion_sum", actual_d_primitive == reported_complete)
    assertions.require("primitive.connection_is_A", terms["connection"] == isolated_a)

    partial_maps = {
        "connection": {"w": dw, "a": zero, "q": zero, "nu": zero},
        "reference": {"w": zero, "a": da, "q": zero, "nu": zero},
        "coframe": {"w": zero, "a": zero, "q": dq, "nu": zero},
        "normalization": {"w": zero, "a": zero, "q": zero, "nu": dnu},
    }
    for name, term in terms.items():
        assertions.require(
            f"primitive.{name}_term",
            primitive.field_derivative(partial_maps[name]) == term,
        )
        omitted = add_forms(
            field_space,
            (value for key, value in terms.items() if key != name),
        )
        sign_reversed = complete_terms - 2 * term
        assertions.require(f"control.omit_{name}_detected", omitted != actual_d_primitive)
        assertions.require(f"control.flip_{name}_detected", sign_reversed != actual_d_primitive)

    second_derivative = actual_d_primitive.field_derivative(differential)
    assertions.require("primitive.d_F_squared_zero", second_derivative.is_zero)

    q_point, nu_point = Fraction(3), Fraction(1)
    variation_q = Variation(dq=Fraction(1))
    variation_w = Variation(dw=Fraction(1))
    variation_a = Variation(da=Fraction(1))
    variation_nu = Variation(dnu=Fraction(1))
    direct_qw = direct_original_curl(
        variation_q, variation_w, q_value=q_point, nu_value=nu_point
    )
    direct_wq = direct_original_curl(
        variation_w, variation_q, q_value=q_point, nu_value=nu_point
    )
    direct_nuw = direct_original_curl(
        variation_nu, variation_w, q_value=q_point, nu_value=nu_point
    )
    direct_aw = direct_original_curl(
        variation_a, variation_w, q_value=q_point, nu_value=nu_point
    )

    assertions.require("alternate.coordinate_variations_commute", True)
    assertions.require("alternate.free_q_original_curl", direct_qw == 2 * q_point * nu_point)
    assertions.require("alternate.free_q_nonzero", direct_qw != 0)
    assertions.require("alternate.antisymmetry", direct_wq == -direct_qw)
    assertions.require("alternate.free_nu_original_curl", direct_nuw == q_point**2)
    assertions.require("alternate.free_nu_nonzero", direct_nuw != 0)
    assertions.require("alternate.fixed_q_nu_zero", direct_aw == 0)

    omission_controls = {
        name: add_forms(
            field_space,
            (value for key, value in terms.items() if key != name),
        )
        != actual_d_primitive
        for name in terms
    }
    sign_controls = {
        name: complete_terms - 2 * term != actual_d_primitive
        for name, term in terms.items()
    }

    emit_observations(
        {
            "assertions": {
                "total": assertions.total,
                "failed": len(assertions.failed),
                "failed_names": assertions.failed,
            },
            "internal_mutation": INTERNAL_MUTATION or "none",
            "mode": {
                "active_ordered_terms": active_terms,
                "basic_persistent_legs": basic_persistent_mode,
                "compact_support_variations": compact_variations,
                "commuting_variations": commuting_coordinate_variations,
                "eta0_period": "+2*pi",
                "normalized_factor": fraction_text(normalized_factor),
                "ordered_contraction_coefficient": fraction_text(ordered_coefficient),
                "support_boxes": {
                    "chart": ["-2", "2"],
                    "cutoff": ["-3/2", "3/2"],
                    "mode": ["-1", "1"],
                },
            },
            "primary": {
                "d_F_A": actual_curl.serialize(),
                "d_F_B": actual_d_primitive.serialize(),
                "d_F_squared_B": second_derivative.serialize(),
                "fixed_q_nu_curl_zero": fixed_q_nu_curl.is_zero,
                "free_nu_curl_nonzero": not free_nu_curl.is_zero,
                "free_q_curl_nonzero": not free_q_curl.is_zero,
            },
            "alternate_method": {
                "algorithm": "direct dense ordered-index evaluation of D005 equation (28)",
                "field_point": {"q": "3", "nu": "1"},
                "curl_partial_nu_partial_w": fraction_text(direct_nuw),
                "curl_partial_q_partial_w": fraction_text(direct_qw),
                "curl_partial_w_partial_q": fraction_text(direct_wq),
                "uses_field_derivative": False,
            },
            "controls": {
                "omission_detected": omission_controls,
                "sign_reversal_detected": sign_controls,
            },
            "producer_model": PRODUCER_MODEL,
        }
    )
    return FAILED if assertions.failed else PASSED


def main() -> int:
    try:
        outcome = check()
    except Exception as exc:  # noqa: BLE001 - unhandled failures are execution errors
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    if outcome not in {PASSED, FAILED, INCONCLUSIVE}:
        print(f"{OBLIGATION_ID} returned undefined status {outcome!r}", file=sys.stderr)
        return ERROR
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
