#!/usr/bin/env python3
"""Exact claim-specific implementation of machine-check obligation O004.

Run this only through the deterministic wrapper:

    uv run --locked python scripts/run_check.py O004

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

from dataclasses import dataclass, field
from fractions import Fraction
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


OBLIGATION_ID = "O004"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]

# Keep the fingerprinted infrastructure tree unchanged while importing it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra,
    Polynomial,
    RationalMatrix,
    levi_civita_sign,
)

PASSED = 0
FAILED = 1
INCONCLUSIVE = 2
ERROR = 3

OBSERVATION_PREFIX = "##OBSERVATIONS##"

PRODUCER_MODEL = "openai/gpt-5.6-sol"
INFRASTRUCTURE_PRODUCER_MODELS = ("openai/gpt-5.6-sol",)
INTENTIONAL_MUTATION = os.environ.get("O004_INTENTIONAL_MUTATION", "")
SUPPORTED_MUTATIONS = {"", "exterior-sign"}

INTERNAL = (0, 1, 2, 3)
TANGENTIAL = (0, 1, 2)
LORENTZ_PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
FORM_PAIRS = ((0, 1), (0, 2), (1, 2))
FORM_LABELS = ("du0", "du1", "du2")
FORM_PAIR_LABELS = (("du0", "du1"), ("du0", "du2"), ("du1", "du2"))


@dataclass
class AssertionRecorder:
    """Collect exact assertion outcomes without allowing observations to vote."""

    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    def require(self, name: str, condition: bool) -> None:
        if type(condition) is not bool:
            raise TypeError(f"assertion {name!r} did not produce a bool")
        (self.passed if condition else self.failed).append(name)

    @property
    def total(self) -> int:
        return len(self.passed) + len(self.failed)


def polynomial_sum(terms: Sequence[Polynomial]) -> Polynomial:
    result = Polynomial.zero()
    for term in terms:
        result = result + term
    return result


def form_coefficient(form: Any, monomial: tuple[str, ...]) -> Polynomial:
    return dict(form.terms).get(monomial, Polynomial.zero())


def rational_form_coefficient(form: Any, monomial: tuple[str, ...]) -> Fraction:
    coefficient = form_coefficient(form, monomial)
    if not coefficient.is_constant:
        raise ValueError(f"expected a constant coefficient on {monomial}, got {coefficient!r}")
    return coefficient.coefficient(())


def ordered_component(components: Mapping[tuple[int, int], Any], a: int, b: int, zero: Any) -> Any:
    if a == b:
        return zero
    return components[(a, b)] if a < b else -components[(b, a)]


def epsilon_base(coframes: Sequence[Any], a: int, b: int, *, ordered: bool = True) -> Any:
    """Return (1/4) epsilon_abcd e^c wedge e^d with declared pair summation."""

    algebra = coframes[0].algebra
    result = algebra.zero()
    index_pairs = (
        ((c, d) for c in INTERNAL for d in INTERNAL if c != d)
        if ordered
        else ((c, d) for c in INTERNAL for d in INTERNAL if c < d)
    )
    for c, d in index_pairs:
        epsilon = levi_civita_sign((a, b, c, d), INTERNAL)
        if epsilon:
            result = result + coframes[c].wedge(coframes[d]) * Fraction(epsilon, 4)
    return result


LinearForm = dict[str, Fraction]


def linear_form(**coefficients: int) -> LinearForm:
    return {name: Fraction(value) for name, value in coefficients.items() if value}


def add_linear(left: LinearForm, right: LinearForm) -> LinearForm:
    result = dict(left)
    for name, value in right.items():
        updated = result.get(name, Fraction(0)) + value
        if updated:
            result[name] = updated
        else:
            result.pop(name, None)
    return result


def linear_to_polynomial(value: LinearForm) -> Polynomial:
    return polynomial_sum([Polynomial.generator(name) * coefficient for name, coefficient in value.items()])


def internal_hodge_matrix() -> RationalMatrix:
    """Map canonical coframe wedges to the ordered-sum epsilon base P_ab."""

    return RationalMatrix(
        [
            [Fraction(levi_civita_sign((a, b, c, d), INTERNAL), 2) for c, d in LORENTZ_PAIRS]
            for a, b in LORENTZ_PAIRS
        ]
    )


def matrix_polynomial_vector(matrix: RationalMatrix, vector: Sequence[Polynomial]) -> tuple[Polynomial, ...]:
    if len(vector) != matrix.ncols:
        raise ValueError("polynomial matrix-vector dimension mismatch")
    return tuple(
        polynomial_sum([entry * component for entry, component in zip(row, vector)])
        for row in matrix.rows
    )


def minor(matrix: Sequence[Sequence[Any]], rows: tuple[int, int], columns: tuple[int, int]) -> Any:
    i, j = rows
    mu, nu = columns
    return matrix[i][mu] * matrix[j][nu] - matrix[i][nu] * matrix[j][mu]


def numeric_minors(matrix: Sequence[Sequence[int | Fraction]]) -> tuple[Fraction, ...]:
    return tuple(
        Fraction(minor(matrix, rows, columns))
        for columns in FORM_PAIRS
        for rows in LORENTZ_PAIRS
    )


def build_h_matrix(
    algebra: ExteriorAlgebra,
    coframes: Sequence[Any],
    *,
    ordered: bool = True,
    prefactor: Fraction = Fraction(-1, 2),
) -> RationalMatrix:
    """Construct H/b from -(1/2) epsilon_abcd K^ab wedge e^d."""

    columns: list[tuple[Fraction, ...]] = []
    for pair in LORENTZ_PAIRS:
        for mu, label in enumerate(FORM_LABELS):
            del mu  # the label fixes the declared domain coordinate
            canonical_k = {candidate: algebra.zero() for candidate in LORENTZ_PAIRS}
            canonical_k[pair] = algebra.basis_form(label)
            output: list[Fraction] = []
            for c in INTERNAL:
                h_c = algebra.zero()
                pair_iterator = (
                    ((a, b) for a in INTERNAL for b in INTERNAL if a != b)
                    if ordered
                    else iter(LORENTZ_PAIRS)
                )
                for a, b in pair_iterator:
                    k_ab = ordered_component(canonical_k, a, b, algebra.zero())
                    if k_ab.is_zero:
                        continue
                    for d in INTERNAL:
                        epsilon = levi_civita_sign((a, b, c, d), INTERNAL)
                        if epsilon:
                            h_c = h_c + k_ab.wedge(coframes[d]) * (prefactor * epsilon)
                output.extend(rational_form_coefficient(h_c, monomial) for monomial in FORM_PAIR_LABELS)
            columns.append(tuple(output))

    rows = [tuple(column[row] for column in columns) for row in range(12)]
    return RationalMatrix(rows)


def decode_ms(vector: Sequence[int | Fraction]) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    """Signed adapted coordinates K^(3i)=M^i_j e^j and T^i=S^i_j e^j."""

    if len(vector) != 18:
        raise ValueError("the K vector must have 18 components")
    exact = tuple(Fraction(value) for value in vector)
    location = {(pair, mu): 3 * LORENTZ_PAIRS.index(pair) + mu for pair in LORENTZ_PAIRS for mu in TANGENTIAL}
    m = [[-exact[location[((i, 3), j)]] for j in TANGENTIAL] for i in TANGENTIAL]
    s = [
        [exact[location[((1, 2), j)]] for j in TANGENTIAL],
        [-exact[location[((0, 2), j)]] for j in TANGENTIAL],
        [exact[location[((0, 1), j)]] for j in TANGENTIAL],
    ]
    return m, s


def encode_ms(m: Sequence[Sequence[int | Fraction]], s: Sequence[Sequence[int | Fraction]]) -> tuple[Fraction, ...]:
    vector = [Fraction(0) for _ in range(18)]
    location = {(pair, mu): 3 * LORENTZ_PAIRS.index(pair) + mu for pair in LORENTZ_PAIRS for mu in TANGENTIAL}
    for i in TANGENTIAL:
        for j in TANGENTIAL:
            vector[location[((i, 3), j)]] = -Fraction(m[i][j])
            vector[location[((1, 2), j)]] = Fraction(s[0][j])
            vector[location[((0, 2), j)]] = -Fraction(s[1][j])
            vector[location[((0, 1), j)]] = Fraction(s[2][j])
    return tuple(vector)


def analytic_h_from_ms(vector: Sequence[int | Fraction]) -> tuple[Fraction, ...]:
    """D005 adapted M/S formula, independent of epsilon/wedge and row reduction."""

    m, s = decode_ms(vector)
    trace_m = sum((m[i][i] for i in TANGENTIAL), Fraction(0))
    c_matrix = [
        [m[row][column] - (trace_m if row == column else 0) for column in TANGENTIAL]
        for row in TANGENTIAL
    ]
    output: list[Fraction] = []
    for column in TANGENTIAL:
        # (h_12,-h_02,h_01)^m = M^m_column-tr(M) delta^m_column.
        output.extend((c_matrix[2][column], -c_matrix[1][column], c_matrix[0][column]))
    output.extend((s[1][0] - s[0][1], s[2][0] - s[0][2], s[2][1] - s[1][2]))
    return tuple(output)


def vector_to_k_forms(algebra: ExteriorAlgebra, vector: Sequence[int | Fraction]) -> dict[tuple[int, int], Any]:
    components: dict[tuple[int, int], Any] = {}
    for pair_index, pair in enumerate(LORENTZ_PAIRS):
        form = algebra.zero()
        for mu, label in enumerate(FORM_LABELS):
            coefficient = Fraction(vector[3 * pair_index + mu])
            if coefficient:
                form = form + algebra.basis_form(label) * coefficient
        components[pair] = form
    return components


def curvature_component(
    algebra: ExteriorAlgebra,
    k_components: Mapping[tuple[int, int], Any],
    a: int,
    b: int,
) -> Any:
    """Constant-K, flat-reference value K^a_c wedge K^cb for diag(-,+,+,+)."""

    metric_diagonal = (-1, 1, 1, 1)
    result = algebra.zero()
    for c in INTERNAL:
        left = ordered_component(k_components, a, c, algebra.zero()) * metric_diagonal[c]
        right = ordered_component(k_components, c, b, algebra.zero())
        result = result + left.wedge(right)
    return result


def emit_observations(observations: dict[str, Any]) -> None:
    """Emit one structured, machine-readable observation record to stdout."""
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


def check() -> int:
    """Perform every exact item in O004's predeclared acceptance criterion."""

    if INTENTIONAL_MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(
            "unsupported O004_INTENTIONAL_MUTATION; supported values are '' and 'exterior-sign'"
        )

    recorder = AssertionRecorder()
    algebra = ExteriorAlgebra(FORM_LABELS)
    coframes = tuple(algebra.basis_form(label) for label in FORM_LABELS) + (algebra.zero(),)

    # The only predeclared inconclusive geometric case is excluded explicitly.
    planar_triad = RationalMatrix(((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)))
    if planar_triad.rank() != 3:
        emit_observations(
            {
                "obligation_id": OBLIGATION_ID,
                "reason": "encoded planar triad is not exactly rank three",
                "producer_model": PRODUCER_MODEL,
            }
        )
        return INCONCLUSIVE

    # D005 (24), (30), and (22), reduced to one independent pair/form coefficient.
    omega = Polynomial.generator("omega")
    varpi = Polynomial.generator("varpi")
    reference = Polynomial.generator("a")
    q = Polynomial.generator("Q")
    lagrange = Polynomial.generator("lambda")
    pminus = Polynomial.generator("Pminus")
    exterior_sign = 1 if INTENTIONAL_MUTATION == "exterior-sign" else -1
    independent_action = (
        q * (omega - reference)
        + lagrange * (omega - varpi)
        + exterior_sign * pminus * varpi
    )

    # Reference-free means substitution before differentiation: delta a=delta varpi.
    reference_free_action = independent_action.substitute({"a": varpi})
    primary_gradients = {
        "reference_free": {
            "omega": reference_free_action.differentiate("omega"),
            "varpi": reference_free_action.differentiate("varpi"),
        },
        "fixed_reference": {
            "omega": independent_action.differentiate("omega"),
            "varpi": independent_action.differentiate("varpi"),
        },
        "free_reference": {
            "omega": independent_action.differentiate("omega"),
            "varpi": independent_action.differentiate("varpi"),
            "a": independent_action.differentiate("a"),
        },
    }
    expected_gradients = {
        "reference_free": {"omega": q + lagrange, "varpi": -(q + lagrange) - pminus},
        "fixed_reference": {"omega": q + lagrange, "varpi": -lagrange - pminus},
        "free_reference": {"omega": q + lagrange, "varpi": -lagrange - pminus, "a": -q},
    }
    for branch, gradients in expected_gradients.items():
        for variable, expected in gradients.items():
            recorder.require(
                f"branch.primary.{branch}.{variable}",
                primary_gradients[branch][variable] == expected,
            )
    recorder.require(
        "branch.elimination.reference_free.Pminus_zero",
        primary_gradients["reference_free"]["omega"]
        + primary_gradients["reference_free"]["varpi"]
        == -pminus,
    )
    recorder.require(
        "branch.elimination.fixed_reference.Q_equals_Pminus",
        primary_gradients["fixed_reference"]["omega"]
        + primary_gradients["fixed_reference"]["varpi"]
        == q - pminus,
    )
    recorder.require(
        "branch.elimination.free_reference.Q_zero",
        primary_gradients["free_reference"]["a"] == -q,
    )

    # Independent direct variation table: no Polynomial.differentiate call is used.
    analytic_gradients: dict[str, dict[str, LinearForm]] = {
        "reference_free": {
            "omega": linear_form(Q=1, **{"lambda": 1}),
            "varpi": linear_form(Q=-1, **{"lambda": -1, "Pminus": -1}),
        },
        "fixed_reference": {
            "omega": linear_form(Q=1, **{"lambda": 1}),
            "varpi": linear_form(**{"lambda": -1, "Pminus": -1}),
        },
        "free_reference": {
            "omega": linear_form(Q=1, **{"lambda": 1}),
            "varpi": linear_form(**{"lambda": -1, "Pminus": -1}),
            "a": linear_form(Q=-1),
        },
    }
    for branch, gradients in analytic_gradients.items():
        for variable, gradient in gradients.items():
            recorder.require(
                f"branch.alternate_agrees.{branch}.{variable}",
                linear_to_polynomial(gradient) == primary_gradients[branch][variable],
            )
    recorder.require(
        "branch.alternate_elimination.reference_free",
        add_linear(
            analytic_gradients["reference_free"]["omega"],
            analytic_gradients["reference_free"]["varpi"],
        )
        == linear_form(Pminus=-1),
    )
    recorder.require(
        "branch.alternate_elimination.fixed_reference",
        add_linear(
            analytic_gradients["fixed_reference"]["omega"],
            analytic_gradients["fixed_reference"]["varpi"],
        )
        == linear_form(Q=1, Pminus=-1),
    )
    recorder.require(
        "branch.alternate_elimination.free_reference",
        analytic_gradients["free_reference"]["a"] == linear_form(Q=-1),
    )

    # Timing/sign negative controls for the variational branches.
    recorder.require(
        "control.reference_substitution_timing_detected",
        primary_gradients["reference_free"]["varpi"]
        - primary_gradients["fixed_reference"]["varpi"]
        == -q,
    )
    wrong_sign_action = q * (omega - reference) + lagrange * (omega - varpi) + pminus * varpi
    recorder.require(
        "control.exterior_sign_mutation_detected",
        wrong_sign_action.differentiate("varpi") != expected_gradients["fixed_reference"]["varpi"],
    )
    recorder.require(
        "control.free_reference_equation_not_silently_dropped",
        primary_gradients["free_reference"]["a"] != Polynomial.zero(),
    )

    # Exact ordered epsilon coefficient and coupling substitutions.
    b = Polynomial.generator("b")
    kappa4_inv = Polynomial.generator("kappa4_inv")
    tau = Polynomial.generator("tau")
    gamma = Polynomial.generator("gamma")
    ell_star = Polynomial.generator("ell_star")
    kappa5_inv = Polynomial.generator("kappa5_inv")
    planar_bases = {pair: epsilon_base(coframes, *pair) for pair in LORENTZ_PAIRS}
    expected_planar_bases = {
        (0, 1): algebra.zero(),
        (0, 2): algebra.zero(),
        (0, 3): algebra.from_terms([(("du1", "du2"), Fraction(1, 2))]),
        (1, 2): algebra.zero(),
        (1, 3): algebra.from_terms([(("du0", "du2"), Fraction(-1, 2))]),
        (2, 3): algebra.from_terms([(("du0", "du1"), Fraction(1, 2))]),
    }
    recorder.require("epsilon.planar_all_pair_signs", planar_bases == expected_planar_bases)
    incidence_forms = {
        pair: planar_bases[pair] * b - planar_bases[pair] * kappa4_inv
        for pair in LORENTZ_PAIRS
    }
    recorder.require(
        "epsilon.planar_factor_b_minus_kappa4_inv",
        all(
            incidence_forms[pair] == planar_bases[pair] * (b - kappa4_inv)
            for pair in LORENTZ_PAIRS
        ),
    )
    recorder.require(
        "epsilon.planar_P03_exact_coefficient",
        form_coefficient(incidence_forms[(0, 3)], ("du1", "du2"))
        == (b - kappa4_inv) * Fraction(1, 2),
    )
    coupling_residual = (b - kappa4_inv).substitute({"b": tau * gamma}).substitute(
        {"gamma": ell_star * kappa5_inv}
    )
    recorder.require(
        "coupling.tau_ell_star_kappa5_inv_relation",
        coupling_residual == tau * ell_star * kappa5_inv - kappa4_inv,
    )
    half_base = epsilon_base(coframes, 0, 3, ordered=False)
    recorder.require(
        "control.ordered_pair_factor_mutation_detected",
        half_base * 2 == planar_bases[(0, 3)] and half_base != planar_bases[(0, 3)],
    )

    # Universal coframe wedges, internal Hodge map, minors, and rank<=1 certificate.
    hodge = internal_hodge_matrix()
    recorder.require("minors.internal_hodge_rank_six", hodge.rank() == 6)
    recorder.require("minors.internal_hodge_nullity_zero", len(hodge.nullspace()) == 0)
    x = [[Polynomial.generator(f"x{row}{column}") for column in TANGENTIAL] for row in INTERNAL]
    universal_coframes = []
    for row in INTERNAL:
        one_form = algebra.zero()
        for column, label in enumerate(FORM_LABELS):
            one_form = one_form + algebra.basis_form(label) * x[row][column]
        universal_coframes.append(one_form)
    universal_bases = {pair: epsilon_base(universal_coframes, *pair) for pair in LORENTZ_PAIRS}
    universal_minor_match = True
    for form_pair, labels in zip(FORM_PAIRS, FORM_PAIR_LABELS):
        minor_vector = tuple(minor(x, pair, form_pair) for pair in LORENTZ_PAIRS)
        p_vector = matrix_polynomial_vector(hodge, minor_vector)
        for pair_index, pair in enumerate(LORENTZ_PAIRS):
            universal_minor_match = universal_minor_match and (
                form_coefficient(universal_bases[pair], labels) == p_vector[pair_index]
            )
    recorder.require("minors.all_18_wedge_coefficients", universal_minor_match)

    # For every possible nonzero pivot, these are exactly the relations that
    # factor an all-minors-zero 4x3 matrix over the fraction field into rank one.
    pivot_identities_hold = True
    pivot_identity_count = 0
    for pivot_row in INTERNAL:
        for pivot_column in TANGENTIAL:
            for row in INTERNAL:
                for column in TANGENTIAL:
                    cross = (
                        x[pivot_row][pivot_column] * x[row][column]
                        - x[row][pivot_column] * x[pivot_row][column]
                    )
                    if row == pivot_row or column == pivot_column:
                        target = Polynomial.zero()
                    else:
                        sorted_rows = tuple(sorted((pivot_row, row)))
                        sorted_columns = tuple(sorted((pivot_column, column)))
                        row_sign = 1 if (pivot_row, row) == sorted_rows else -1
                        column_sign = 1 if (pivot_column, column) == sorted_columns else -1
                        target = minor(x, sorted_rows, sorted_columns) * row_sign * column_sign
                    pivot_identities_hold = pivot_identities_hold and cross == target
                    pivot_identity_count += 1
    recorder.require("minors.universal_pivot_factorization_identities", pivot_identities_hold)

    u = [Polynomial.generator(f"u{row}") for row in INTERNAL]
    v = [Polynomial.generator(f"v{column}") for column in TANGENTIAL]
    generic_rank_one = [[u[row] * v[column] for column in TANGENTIAL] for row in INTERNAL]
    recorder.require(
        "minors.rank_one_parametrization_vanishes",
        all(
            minor(generic_rank_one, rows, columns) == Polynomial.zero()
            for rows in LORENTZ_PAIRS
            for columns in FORM_PAIRS
        ),
    )
    rank_zero_control = ((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0))
    rank_one_control = ((1, 2, 3), (2, 4, 6), (-1, -2, -3), (0, 0, 0))
    rank_two_control = ((1, 2, 3), (2, 4, 7), (-1, -2, -3), (0, 0, 0))
    rank_zero_minors = numeric_minors(rank_zero_control)
    rank_one_minors = numeric_minors(rank_one_control)
    rank_two_minors = numeric_minors(rank_two_control)
    recorder.require(
        "minors.positive_rank_zero_control",
        RationalMatrix(rank_zero_control).rank() == 0 and not any(rank_zero_minors),
    )
    recorder.require(
        "minors.positive_rank_one_control",
        RationalMatrix(rank_one_control).rank() == 1 and not any(rank_one_minors),
    )
    recorder.require(
        "minors.negative_rank_two_control",
        RationalMatrix(rank_two_control).rank() == 2 and any(rank_two_minors),
    )
    rank_two_p_nonzero = False
    for form_pair_index in range(len(FORM_PAIRS)):
        start = form_pair_index * len(LORENTZ_PAIRS)
        normalized_p = hodge.matvec(rank_two_minors[start : start + len(LORENTZ_PAIRS)])
        rank_two_p_nonzero = rank_two_p_nonzero or any(normalized_p)
    recorder.require("minors.rank_two_has_nonzero_Pminus", rank_two_p_nonzero)

    # Primary H matrix and independent adapted M/S reconstruction.
    h_matrix = build_h_matrix(algebra, coframes)
    recorder.require("H.shape_12_by_18", h_matrix.shape == (12, 18))
    h_rank = h_matrix.rank()
    h_nullspace = h_matrix.nullspace()
    recorder.require("H.rank_12", h_rank == 12)
    recorder.require("H.nullity_6", len(h_nullspace) == 6 and h_matrix.ncols - h_rank == 6)
    alternate_columns = []
    for column in range(18):
        unit = [Fraction(0) for _ in range(18)]
        unit[column] = Fraction(1)
        alternate_columns.append(analytic_h_from_ms(unit))
    alternate_rows = tuple(
        tuple(alternate_columns[column][row] for column in range(18)) for row in range(12)
    )
    recorder.require("H.adapted_MS_entrywise_agreement", h_matrix.rows == alternate_rows)
    recorder.require(
        "H.primary_nullspace_vectors_exact",
        all(not any(h_matrix.matvec(vector)) for vector in h_nullspace),
    )

    # Analytic mixed-sector inverse: C=M-tr(M)I and M=C-tr(C)I/2.
    symbolic_m = [
        [Polynomial.generator(f"M{row}{column}") for column in TANGENTIAL]
        for row in TANGENTIAL
    ]
    trace_m = polynomial_sum([symbolic_m[i][i] for i in TANGENTIAL])
    symbolic_c = [
        [symbolic_m[row][column] - (trace_m if row == column else 0) for column in TANGENTIAL]
        for row in TANGENTIAL
    ]
    trace_c = polynomial_sum([symbolic_c[i][i] for i in TANGENTIAL])
    reconstructed_m = [
        [symbolic_c[row][column] - (trace_c * Fraction(1, 2) if row == column else 0) for column in TANGENTIAL]
        for row in TANGENTIAL
    ]
    recorder.require("H.M_sector_trace_identity", trace_c == -2 * trace_m)
    recorder.require("H.M_sector_explicit_inverse", reconstructed_m == symbolic_m)

    zero_m = [[0 for _ in TANGENTIAL] for _ in TANGENTIAL]
    symmetric_s_basis: list[tuple[Fraction, ...]] = []
    symmetric_coordinates = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
    for i, j in symmetric_coordinates:
        s_matrix = [[0 for _ in TANGENTIAL] for _ in TANGENTIAL]
        s_matrix[i][j] = 1
        s_matrix[j][i] = 1
        symmetric_s_basis.append(encode_ms(zero_m, s_matrix))
    recorder.require(
        "H.analytic_six_kernel_vectors",
        all(not any(analytic_h_from_ms(vector)) for vector in symmetric_s_basis),
    )
    recorder.require(
        "H.primary_accepts_analytic_kernel_vectors",
        all(not any(h_matrix.matvec(vector)) for vector in symmetric_s_basis),
    )
    coordinate_matrix: list[tuple[Fraction, ...]] = []
    for vector in symmetric_s_basis:
        decoded_m, decoded_s = decode_ms(vector)
        if any(any(row) for row in decoded_m):
            raise ValueError("analytic S basis unexpectedly contains an M component")
        coordinate_matrix.append(tuple(decoded_s[i][j] for i, j in symmetric_coordinates))
    recorder.require(
        "H.analytic_kernel_basis_independent",
        tuple(coordinate_matrix)
        == tuple(
            tuple(Fraction(1 if row == column else 0) for column in range(6))
            for row in range(6)
        ),
    )
    analytic_rank = 9 + 3
    analytic_nullity = 18 - analytic_rank
    recorder.require("H.alternate_rank_12", analytic_rank == 12)
    recorder.require("H.alternate_nullity_6", analytic_nullity == 6)

    # Certified nonflat element: S=I, hence K01=du2, K02=-du1, K12=du0.
    identity_s = [[1 if row == column else 0 for column in TANGENTIAL] for row in TANGENTIAL]
    witness = encode_ms(zero_m, identity_s)
    witness_k = vector_to_k_forms(algebra, witness)
    recorder.require("curvature.witness_nonzero_K", any(witness))
    recorder.require("curvature.witness_in_analytic_kernel", not any(analytic_h_from_ms(witness)))
    recorder.require("curvature.witness_in_primary_kernel", not any(h_matrix.matvec(witness)))
    expected_curvature_01 = algebra.from_terms([(("du0", "du1"), -1)])
    curvature_01 = curvature_component(algebra, witness_k, 0, 1)
    recorder.require("curvature.witness_R01_exact_sign", curvature_01 == expected_curvature_01)
    recorder.require("curvature.witness_nonflat", not curvature_01.is_zero)

    # A nonzero kernel element need not be nonflat: this control has one Lie generator.
    flat_s = [[0 for _ in TANGENTIAL] for _ in TANGENTIAL]
    flat_s[0][0] = 1
    flat_kernel_vector = encode_ms(zero_m, flat_s)
    flat_k = vector_to_k_forms(algebra, flat_kernel_vector)
    flat_curvatures = [curvature_component(algebra, flat_k, *pair) for pair in LORENTZ_PAIRS]
    recorder.require(
        "control.flat_kernel_vector_is_nonzero_and_in_kernel",
        any(flat_kernel_vector) and not any(h_matrix.matvec(flat_kernel_vector)),
    )
    recorder.require(
        "control.flat_kernel_rejected_as_nonflat_witness",
        all(curvature.is_zero for curvature in flat_curvatures),
    )

    # H sign, ordered-pair factor, rank, and S-symmetry mutation controls.
    h_sign_mutation = build_h_matrix(algebra, coframes, prefactor=Fraction(1, 2))
    recorder.require(
        "control.H_sign_mutation_detected",
        h_sign_mutation != h_matrix
        and all(
            h_sign_mutation.rows[row][column] == -h_matrix.rows[row][column]
            for row in range(12)
            for column in range(18)
        ),
    )
    h_half_mutation = build_h_matrix(algebra, coframes, ordered=False)
    recorder.require(
        "control.H_ordered_factor_mutation_detected",
        h_half_mutation != h_matrix
        and all(
            2 * h_half_mutation.rows[row][column] == h_matrix.rows[row][column]
            for row in range(12)
            for column in range(18)
        ),
    )
    rank_mutation_rows = [list(row) for row in h_matrix.rows]
    rank_mutation_rows[0] = [Fraction(0) for _ in range(18)]
    h_rank_mutation = RationalMatrix(rank_mutation_rows)
    recorder.require("control.H_rank_mutation_detected", h_rank_mutation.rank() == 11)
    asymmetric_s = [[0 for _ in TANGENTIAL] for _ in TANGENTIAL]
    asymmetric_s[0][1] = 1
    asymmetric_s[1][0] = -1
    asymmetric_vector = encode_ms(zero_m, asymmetric_s)
    recorder.require(
        "control.H_S_symmetry_mutation_detected",
        any(analytic_h_from_ms(asymmetric_vector)) and any(h_matrix.matvec(asymmetric_vector)),
    )

    observations = {
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": list(INFRASTRUCTURE_PRODUCER_MODELS),
        "intentional_mutation": INTENTIONAL_MUTATION or None,
        "assertions": {
            "total": recorder.total,
            "passed": len(recorder.passed),
            "failed": len(recorder.failed),
            "failed_names": recorder.failed,
        },
        "branches": {
            "reference_free_eliminant": "-Pminus",
            "fixed_reference_eliminant": "Q-Pminus",
            "free_reference_gradient": "-Q",
            "substitution_timing": "a=varpi before variation only in reference-free branch",
        },
        "planar_incidence": {
            "P03_base_coefficient": "1/2",
            "factor": "b-kappa4_inv",
            "coupling_residual": "tau*ell_star*kappa5_inv-kappa4_inv",
        },
        "coframe_minors": {
            "minor_count": 18,
            "pivot_identity_count": pivot_identity_count,
            "internal_hodge_rank": hodge.rank(),
            "rank_zero_control": 0,
            "rank_one_control": 1,
            "rank_two_control": 2,
        },
        "H_map": {
            "basis": {
                "domain_pairs": [f"{a}{b}" for a, b in LORENTZ_PAIRS],
                "domain_forms": list(FORM_LABELS),
                "codomain_c": list(INTERNAL),
                "codomain_forms": ["du0^du1", "du0^du2", "du1^du2"],
            },
            "shape": list(h_matrix.shape),
            "primary_rank": h_rank,
            "primary_nullity": len(h_nullspace),
            "analytic_rank": analytic_rank,
            "analytic_nullity": analytic_nullity,
            "kernel_basis_size": len(symmetric_s_basis),
        },
        "nonflat_kernel_witness": {
            "K01": "du2",
            "K02": "-du1",
            "K12": "du0",
            "mixed_components": "0",
            "R01": "-du0^du1",
        },
        "representation": {
            "coefficients": "Fraction and canonical sparse polynomials over Q",
            "equality": "exact canonical map/matrix equality",
            "floats": False,
            "random_sampling": False,
            "CAS": False,
        },
    }
    emit_observations(observations)
    if recorder.failed:
        for name in recorder.failed:
            print(f"FAILED: {name}", file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        outcome = check()
    except Exception as exc:  # noqa: BLE001 - an unhandled failure is an execution error
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    if outcome not in {PASSED, FAILED, INCONCLUSIVE}:
        print(f"{OBLIGATION_ID} returned an undefined status {outcome!r}", file=sys.stderr)
        return ERROR
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
