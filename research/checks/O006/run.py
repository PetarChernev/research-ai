#!/usr/bin/env python3
"""Exact claim-specific implementation of machine-check obligation O006.

Run the unmutated obligation only through ``scripts/run_check.py O006``.
This entrypoint never writes ``result.json``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import json
import os
from pathlib import Path
import sys
from typing import Any, Sequence


OBLIGATION_ID = "O006"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra,
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
INTENTIONAL_MUTATION = os.environ.get("O006_INTENTIONAL_MUTATION", "")
SUPPORTED_MUTATIONS = {
    "",
    "cross-block-delete",
    "moment-sign",
    "q-factor",
    "independent-dlambda",
}

INTERNAL = (0, 1, 2, 3)
ETA = (-1, 1, 1, 1)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
CUT_BASIS = ("dx1", "dx2")
CHI_OFFSET = 0
XI_OFFSET = 6
E_OFFSET = 12
DLAMBDA_OFFSET = 20
ZERO = Fraction(0)
ONE = Fraction(1)


@dataclass
class AssertionRecorder:
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    def require(self, name: str, condition: bool) -> None:
        if type(condition) is not bool:
            raise TypeError(f"assertion {name!r} did not produce a bool")
        (self.passed if condition else self.failed).append(name)

    @property
    def total(self) -> int:
        return len(self.passed) + len(self.failed)


def emit_observations(observations: dict[str, Any]) -> None:
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


def transpose(rows: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(rows[row][column] for row in range(len(rows)))
        for column in range(len(rows[0]))
    )


def matmul(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> tuple[tuple[Fraction, ...], ...]:
    right_t = transpose(right)
    return tuple(
        tuple(
            sum((a * b for a, b in zip(row, column)), ZERO)
            for column in right_t
        )
        for row in left
    )


def matvec(
    rows: Sequence[Sequence[Fraction]], vector: Sequence[Fraction]
) -> tuple[Fraction, ...]:
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), ZERO)
        for row in rows
    )


def matrix_scale(
    rows: Sequence[Sequence[Fraction]], scalar: Fraction
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(scalar * entry for entry in row) for row in rows)


def identity(size: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(ONE if row == column else ZERO for column in range(size))
        for row in range(size)
    )


def diagonal(entries: Sequence[int | Fraction]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(
            Fraction(entries[row]) if row == column else ZERO
            for column in range(len(entries))
        )
        for row in range(len(entries))
    )


def zero_rows(nrows: int, ncols: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ZERO for _ in range(ncols)) for _ in range(nrows))


def mutable_zeros(size: int) -> list[list[Fraction]]:
    return [[ZERO for _ in range(size)] for _ in range(size)]


def block_matrix(
    blocks: Sequence[Sequence[Sequence[Sequence[Fraction]]]],
) -> RationalMatrix:
    """Join a nonempty rectangular grid of exact dense blocks."""

    groups: list[tuple[tuple[Fraction, ...], ...]] = []
    for block_row in blocks:
        heights = {len(block) for block in block_row}
        if len(heights) != 1:
            raise ValueError("block-row heights disagree")
        height = heights.pop()
        groups.append(
            tuple(
                tuple(entry for block in block_row for entry in block[row])
                for row in range(height)
            )
        )
    if len({len(group[0]) for group in groups}) != 1:
        raise ValueError("joined block widths disagree")
    return RationalMatrix(tuple(row for group in groups for row in group))


def canonical_pair_component(a: int, b: int) -> tuple[int, int | None]:
    if a == b:
        return 0, None
    pair = (a, b) if a < b else (b, a)
    return (1 if a < b else -1), PAIR_INDEX[pair]


def bracket_coordinates(
    first: tuple[int, int], second: tuple[int, int]
) -> tuple[Fraction, ...]:
    """Coordinates of the explicitly declared Lorentz bracket."""

    a, b = first
    c, d = second
    terms = (
        (ETA[a] if a == c else 0, b, d),
        (-(ETA[a] if a == d else 0), b, c),
        (-(ETA[b] if b == c else 0), a, d),
        (ETA[b] if b == d else 0, a, c),
    )
    result = [ZERO for _ in PAIRS]
    for coefficient, left, right in terms:
        sign, location = canonical_pair_component(left, right)
        if coefficient and location is not None:
            result[location] += Fraction(coefficient * sign)
    return tuple(result)


PAIRING_DIAGONAL = tuple(Fraction(ETA[a] * ETA[b]) for a, b in PAIRS)
PAIRING = diagonal(PAIRING_DIAGONAL)


def lie_a_matrix(momentum: Sequence[Fraction]) -> RationalMatrix:
    """Return A_IJ=<momentum,[T_I,T_J]> in the declared pairing."""

    rows = []
    for first in PAIRS:
        row = []
        for second in PAIRS:
            bracket = bracket_coordinates(first, second)
            row.append(
                sum(
                    (
                        momentum[k]
                        * PAIRING_DIAGONAL[k]
                        * bracket[k]
                        for k in range(6)
                    ),
                    ZERO,
                )
            )
        rows.append(tuple(row))
    return RationalMatrix(tuple(rows))


def q_and_dq(
    coframes: Sequence[Any], *, ordered_prefactor: Fraction = Fraction(1, 4)
) -> tuple[tuple[Fraction, ...], RationalMatrix]:
    """Construct Q and dQ from ordered epsilon/wedge sums on the cut."""

    algebra = coframes[0].algebra
    area = CUT_BASIS
    q_values: list[Fraction] = []
    for a, b in PAIRS:
        q_form = algebra.zero()
        for c in INTERNAL:
            for d in INTERNAL:
                epsilon = levi_civita_sign((a, b, c, d), INTERNAL)
                if epsilon:
                    q_form = q_form + coframes[c].wedge(coframes[d]) * (
                        ordered_prefactor * epsilon
                    )
        coefficient = dict(q_form.terms).get(area)
        q_values.append(
            ZERO if coefficient is None else coefficient.coefficient(())
        )

    # Differentiation combines the two ordered placements of the varied leg.
    derivative_prefactor = 2 * ordered_prefactor
    columns: list[tuple[Fraction, ...]] = []
    for cut_label in CUT_BASIS:
        for c in INTERNAL:
            variation = algebra.basis_form(cut_label)
            output = []
            for a, b in PAIRS:
                varied = algebra.zero()
                for d in INTERNAL:
                    epsilon = levi_civita_sign((a, b, c, d), INTERNAL)
                    if epsilon:
                        varied = varied + variation.wedge(coframes[d]) * (
                            derivative_prefactor * epsilon
                        )
                coefficient = dict(varied.terms).get(area)
                output.append(
                    ZERO if coefficient is None else coefficient.coefficient(())
                )
            columns.append(tuple(output))
    rows = tuple(
        tuple(columns[column][row] for column in range(8)) for row in range(6)
    )
    return tuple(q_values), RationalMatrix(rows)


def paired_derivative(derivative: RationalMatrix) -> RationalMatrix:
    return RationalMatrix(matmul(PAIRING, derivative.rows))


def insert_group_potential_term(
    rows: list[list[Fraction]],
    *,
    group_offset: int,
    ordinary_offset: int,
    momentum: Sequence[Fraction],
    derivative: RationalMatrix,
) -> None:
    """Differentiate one term <p(e),delta h h^-1> into a shared matrix.

    Under Omega=delta Theta, the inserted blocks are
    [[A_p,-G dp],[(G dp)^T,0]].
    """

    a_matrix = lie_a_matrix(momentum)
    coupled = paired_derivative(derivative)
    for i in range(6):
        for j in range(6):
            rows[group_offset + i][group_offset + j] += a_matrix.rows[i][j]
        for a in range(derivative.ncols):
            rows[group_offset + i][ordinary_offset + a] -= coupled.rows[i][a]
            rows[ordinary_offset + a][group_offset + i] += coupled.rows[i][a]


def differentiate_pulled_back_shell_potential(
    q: Sequence[Fraction], dq: RationalMatrix
) -> RationalMatrix:
    """Substitute lambda=-Q, d lambda=-dQ, then differentiate Theta_B."""

    shell_lambda = tuple(-entry for entry in q)
    shell_dlambda = RationalMatrix(matrix_scale(dq.rows, Fraction(-1)))
    rows = mutable_zeros(20)
    # Theta_B|shell = <Q,chi_v> + <-Q,xi>.
    insert_group_potential_term(
        rows,
        group_offset=CHI_OFFSET,
        ordinary_offset=E_OFFSET,
        momentum=q,
        derivative=dq,
    )
    insert_group_potential_term(
        rows,
        group_offset=XI_OFFSET,
        ordinary_offset=E_OFFSET,
        momentum=shell_lambda,
        derivative=shell_dlambda,
    )
    return RationalMatrix(rows)


def explicit_honest_shell_formula(
    q: Sequence[Fraction], dq: RationalMatrix
) -> RationalMatrix:
    """Independent explicit block transcription of delta<Q,chi_v-xi>."""

    a_matrix = lie_a_matrix(q)
    coupled = paired_derivative(dq)
    zero66 = zero_rows(6, 6)
    zero68 = zero_rows(6, 8)
    zero86 = zero_rows(8, 6)
    return block_matrix(
        (
            (
                a_matrix.rows,
                zero66,
                matrix_scale(coupled.rows, Fraction(-1)),
            ),
            (
                zero66,
                matrix_scale(a_matrix.rows, Fraction(-1)),
                coupled.rows,
            ),
            (
                transpose(coupled.rows),
                matrix_scale(transpose(coupled.rows), Fraction(-1)),
                zero_rows(8, 8),
            ),
        )
    )


def o005_shortcut_embedding(
    q: Sequence[Fraction], dq: RationalMatrix
) -> RationalMatrix:
    """Embed O005's zero xi block plus the (chi_v,e) residual in O006 order."""

    a_matrix = lie_a_matrix(q)
    coupled = paired_derivative(dq)
    return block_matrix(
        (
            (
                a_matrix.rows,
                zero_rows(6, 6),
                matrix_scale(coupled.rows, Fraction(-1)),
            ),
            (zero_rows(6, 6), zero_rows(6, 6), zero_rows(6, 8)),
            (transpose(coupled.rows), zero_rows(8, 6), zero_rows(8, 8)),
        )
    )


def delete_xi_e_cross_block(matrix: RationalMatrix) -> RationalMatrix:
    rows = [list(row) for row in matrix.rows]
    for i in range(6):
        for a in range(8):
            rows[XI_OFFSET + i][E_OFFSET + a] = ZERO
            rows[E_OFFSET + a][XI_OFFSET + i] = ZERO
    return RationalMatrix(rows)


def retained_independent_dlambda_form(
    q: Sequence[Fraction], dq: RationalMatrix
) -> RationalMatrix:
    """Wrong 26D form obtained by differentiating before eliminating lambda."""

    rows = mutable_zeros(26)
    insert_group_potential_term(
        rows,
        group_offset=CHI_OFFSET,
        ordinary_offset=E_OFFSET,
        momentum=q,
        derivative=dq,
    )
    # At the shell point lambda=-Q, but d lambda is wrongly kept independent.
    insert_group_potential_term(
        rows,
        group_offset=XI_OFFSET,
        ordinary_offset=DLAMBDA_OFFSET,
        momentum=tuple(-entry for entry in q),
        derivative=RationalMatrix(identity(6)),
    )
    return RationalMatrix(rows)


def fixed_reference_shell_form(
    q: Sequence[Fraction], dq: RationalMatrix
) -> tuple[tuple[Fraction, ...], RationalMatrix, RationalMatrix]:
    """Derive the A-shell form from Pi=Q+lambda=0 and dPi=dQ+d lambda=0."""

    shell_lambda = tuple(-entry for entry in q)
    shell_dlambda = RationalMatrix(matrix_scale(dq.rows, Fraction(-1)))
    pi = tuple(q[i] + shell_lambda[i] for i in range(6))
    dpi = RationalMatrix(
        tuple(
            tuple(dq.rows[i][a] + shell_dlambda.rows[i][a] for a in range(8))
            for i in range(6)
        )
    )
    rows = mutable_zeros(14)
    insert_group_potential_term(
        rows,
        group_offset=0,
        ordinary_offset=6,
        momentum=pi,
        derivative=dpi,
    )
    return pi, dpi, RationalMatrix(rows)


def generator_matrix(pair: tuple[int, int]) -> tuple[tuple[Fraction, ...], ...]:
    a, b = pair
    rows = [[ZERO for _ in INTERNAL] for _ in INTERNAL]
    rows[b][a] = Fraction(ETA[a])
    rows[a][b] = Fraction(-ETA[b])
    return tuple(tuple(row) for row in rows)


def lorentz_inverse(
    g: Sequence[Sequence[Fraction]],
) -> tuple[tuple[Fraction, ...], ...]:
    eta4 = diagonal(ETA)
    return matmul(matmul(eta4, transpose(g)), eta4)


def adjoint_matrix(g: Sequence[Sequence[Fraction]]) -> RationalMatrix:
    """Columns are coordinates of g T_I g^-1 in the declared pair basis."""

    g_inverse = lorentz_inverse(g)
    columns = []
    for pair in PAIRS:
        transformed = matmul(matmul(g, generator_matrix(pair)), g_inverse)
        columns.append(
            tuple(transformed[b][a] / ETA[a] for a, b in PAIRS)
        )
    return RationalMatrix(
        tuple(tuple(columns[column][row] for column in range(6)) for row in range(6))
    )


def shell_contraction_covector(
    q: Sequence[Fraction],
    adjoint: RationalMatrix,
    *,
    xi_sign: Fraction,
) -> tuple[Fraction, ...]:
    """Contract <Q,chi_v-xi> with chi_v=0, xi=xi_sign Ad_g alpha."""

    values = []
    for alpha_index in range(6):
        xi = tuple(
            xi_sign * adjoint.rows[row][alpha_index] for row in range(6)
        )
        values.append(
            -sum(
                (q[k] * PAIRING_DIAGONAL[k] * xi[k] for k in range(6)),
                ZERO,
            )
        )
    return tuple(values)


def pairing_covector(momentum: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(momentum[k] * PAIRING_DIAGONAL[k] for k in range(6))


def explicit_null_certificates() -> tuple[tuple[str, tuple[Fraction, ...]], ...]:
    """Ten named vectors in (chi_v[6],xi[6],de[8]) coordinates."""

    def vector(entries: dict[int, int]) -> tuple[Fraction, ...]:
        return tuple(Fraction(entries.get(index, 0)) for index in range(20))

    return (
        ("chi_T12", vector({3: 1})),
        ("common_T03", vector({2: 1, 8: 1})),
        ("xi_T12", vector({9: 1})),
        ("common_T01_plus_de1^0", vector({0: 1, 6: 1, 12: 1})),
        ("de1^2", vector({14: 1})),
        ("common_T13_plus_de1^3", vector({4: 1, 10: 1, 15: 1})),
        ("common_T02_plus_de2^0", vector({1: 1, 7: 1, 16: 1})),
        ("de2^1", vector({17: 1})),
        ("de2^2_minus_de1^1", vector({13: -1, 18: 1})),
        ("common_T23_plus_de2^3", vector({5: 1, 11: 1, 19: 1})),
    )


def check() -> int:
    if INTENTIONAL_MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(
            "unsupported O006_INTENTIONAL_MUTATION; expected '', "
            "cross-block-delete, moment-sign, q-factor, or independent-dlambda"
        )

    recorder = AssertionRecorder()
    algebra = ExteriorAlgebra(CUT_BASIS)
    coframes = (
        algebra.zero(),
        algebra.basis_form("dx1"),
        algebra.basis_form("dx2"),
        algebra.zero(),
    )
    planar_triad = RationalMatrix(((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)))
    pairing_matrix = RationalMatrix(PAIRING)
    if planar_triad.rank() != 3:
        emit_observations(
            {"obligation_id": OBLIGATION_ID, "reason": "planar triad is not rank three"}
        )
        return INCONCLUSIVE
    if pairing_matrix.rank() != 6:
        emit_observations(
            {"obligation_id": OBLIGATION_ID, "reason": "Lorentz pairing is degenerate"}
        )
        return INCONCLUSIVE
    recorder.require("domain.planar_triad_rank_three", planar_triad.rank() == 3)
    recorder.require("domain.lorentz_pairing_rank_six", pairing_matrix.rank() == 6)

    prefactor = (
        Fraction(1, 8)
        if INTENTIONAL_MUTATION == "q-factor"
        else Fraction(1, 4)
    )
    q, dq = q_and_dq(coframes, ordered_prefactor=prefactor)
    expected_q = (ZERO, ZERO, Fraction(1, 2), ZERO, ZERO, ZERO)
    expected_dq_rows = (
        (ZERO, ZERO, ZERO, Fraction(-1, 2), ZERO, ZERO, ZERO, ZERO),
        (ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, Fraction(-1, 2)),
        (ZERO, Fraction(1, 2), ZERO, ZERO, ZERO, ZERO, Fraction(1, 2), ZERO),
        (ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO),
        (Fraction(-1, 2), ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO),
        (ZERO, ZERO, ZERO, ZERO, Fraction(-1, 2), ZERO, ZERO, ZERO),
    )
    recorder.require("Q.planar_Q03_plus_half", q == expected_q)
    recorder.require("dQ.shape_6_by_8", dq.shape == (6, 8))
    recorder.require("dQ.explicit_sparse_entries", dq.rows == expected_dq_rows)
    recorder.require("dQ.rank_five", dq.rank() == 5)
    recorder.require("dQ.nullity_three", len(dq.nullspace()) == 3)
    recorder.require("dQ.absent_Q12_row", not any(dq.rows[PAIR_INDEX[(1, 2)]]))

    expected_honest = explicit_honest_shell_formula(q, dq)
    honest = differentiate_pulled_back_shell_potential(q, dq)
    if INTENTIONAL_MUTATION == "cross-block-delete":
        candidate_shell = delete_xi_e_cross_block(honest)
    elif INTENTIONAL_MUTATION == "independent-dlambda":
        candidate_shell = retained_independent_dlambda_form(q, dq)
    else:
        candidate_shell = honest

    candidate_is_20 = candidate_shell.shape == (20, 20)
    recorder.require("shell.shape_20_by_20", candidate_is_20)
    recorder.require("shell.matches_direct_potential_derivative", candidate_shell == expected_honest)
    recorder.require(
        "shell.antisymmetric",
        candidate_is_20
        and transpose(candidate_shell.rows)
        == matrix_scale(candidate_shell.rows, Fraction(-1)),
    )
    expected_xi_e = paired_derivative(dq).rows
    candidate_xi_e = (
        tuple(
            tuple(candidate_shell.rows[XI_OFFSET + i][E_OFFSET + a] for a in range(8))
            for i in range(6)
        )
        if candidate_is_20
        else zero_rows(6, 8)
    )
    recorder.require("shell.xi_deltae_block_exact_plus_GdQ", candidate_xi_e == expected_xi_e)
    recorder.require("shell.xi_deltae_block_nonzero", any(any(row) for row in candidate_xi_e))

    shell_rank = candidate_shell.rank()
    shell_nullity = len(candidate_shell.nullspace())
    recorder.require("shell.rank_10", shell_rank == 10)
    recorder.require("shell.nullity_10", candidate_is_20 and shell_nullity == 10)
    certificates = explicit_null_certificates()
    certificates_annihilated = candidate_is_20 and all(
        not any(candidate_shell.matvec(vector)) for _, vector in certificates
    )
    recorder.require("shell.ten_explicit_null_vectors", certificates_annihilated)
    recorder.require(
        "shell.ten_explicit_null_vectors_independent",
        RationalMatrix(tuple(vector for _, vector in certificates)).rank() == 10,
    )
    recorder.require(
        "shell.certificates_span_exact_nullity",
        certificates_annihilated and shell_nullity == len(certificates),
    )

    shortcut = o005_shortcut_embedding(q, dq)
    recorder.require("shortcut.shape_20_by_20", shortcut.shape == (20, 20))
    recorder.require("shortcut.rank_10", shortcut.rank() == 10)
    recorder.require("shortcut.honest_rank_equal", honest.rank() == shortcut.rank() == 10)
    recorder.require("shortcut.entrywise_unequal_to_honest", honest != shortcut)
    recorder.require(
        "shortcut.misses_nonzero_xi_deltae_entries",
        any(
            honest.rows[XI_OFFSET + i][E_OFFSET + a]
            != shortcut.rows[XI_OFFSET + i][E_OFFSET + a]
            for i in range(6)
            for a in range(8)
        ),
    )

    pi, dpi, fixed_shell = fixed_reference_shell_form(q, dq)
    recorder.require("fixed.shell_Pi_zero_from_Q_plus_lambda", not any(pi))
    recorder.require("fixed.shell_deltaPi_zero_from_dQ_plus_dlambda", not any(any(row) for row in dpi.rows))
    recorder.require("fixed.shell_form_entrywise_zero", not any(any(row) for row in fixed_shell.rows))
    recorder.require("fixed.shell_rank_zero", fixed_shell.rank() == 0)

    # Nonidentity rational 01 boost: cosh=5/3, sinh=4/3.
    g = (
        (Fraction(5, 3), Fraction(4, 3), ZERO, ZERO),
        (Fraction(4, 3), Fraction(5, 3), ZERO, ZERO),
        (ZERO, ZERO, ONE, ZERO),
        (ZERO, ZERO, ZERO, ONE),
    )
    g_inverse = lorentz_inverse(g)
    adjoint = adjoint_matrix(g)
    adjoint_inverse = adjoint_matrix(g_inverse)
    recorder.require(
        "moment.adjoint_inverse",
        matmul(adjoint.rows, adjoint_inverse.rows) == identity(6),
    )
    recorder.require(
        "moment.pairing_invariant",
        matmul(matmul(transpose(adjoint.rows), PAIRING), adjoint.rows) == PAIRING,
    )
    xi_sign = ONE if INTENTIONAL_MUTATION == "moment-sign" else Fraction(-1)
    direct_covector = shell_contraction_covector(q, adjoint, xi_sign=xi_sign)
    expected_jminus = matvec(adjoint_inverse.rows, q)
    expected_covector = pairing_covector(expected_jminus)
    recorder.require("moment.direct_contraction_plus_Adinv_Q", direct_covector == expected_covector)
    recorder.require("moment.shell_Jminus_nonzero", any(expected_jminus))

    identity_adjoint = RationalMatrix(identity(6))
    alpha_corner = tuple(
        Fraction(-1) if index == PAIR_INDEX[(0, 3)] else ZERO for index in range(6)
    )
    corner_covector = shell_contraction_covector(q, identity_adjoint, xi_sign=xi_sign)
    corner_value = sum(
        (corner_covector[index] * alpha_corner[index] for index in range(6)),
        ZERO,
    )
    recorder.require("corner.alpha_minus_T03_witness_plus_half_b", corner_value == Fraction(1, 2))

    # Internal semantic controls are built independently of the selected target mutation.
    deleted_cross = delete_xi_e_cross_block(expected_honest)
    recorder.require(
        "control.deleted_cross_block_detected",
        deleted_cross != expected_honest
        and not any(
            deleted_cross.rows[XI_OFFSET + i][E_OFFSET + a]
            for i in range(6)
            for a in range(8)
        ),
    )
    wrong_covector = shell_contraction_covector(q, adjoint, xi_sign=ONE)
    recorder.require(
        "control.reversed_moment_sign_detected",
        wrong_covector != expected_covector
        and wrong_covector == tuple(-entry for entry in expected_covector),
    )
    half_q, half_dq = q_and_dq(coframes, ordered_prefactor=Fraction(1, 8))
    recorder.require(
        "control.ordered_pair_factor_error_detected",
        half_q[PAIR_INDEX[(0, 3)]] == Fraction(1, 4)
        and half_q != expected_q
        and half_dq.rows != expected_dq_rows,
    )
    retained = retained_independent_dlambda_form(q, dq)
    recorder.require(
        "control.independent_dlambda_detected",
        retained.shape == (26, 26)
        and retained.shape != expected_honest.shape
        and any(
            retained.rows[XI_OFFSET + i][DLAMBDA_OFFSET + j]
            for i in range(6)
            for j in range(6)
        ),
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
        "basis": {
            "lorentz_pairs": [f"{a}{b}" for a, b in PAIRS],
            "shell_coordinates": [
                *[f"chi_v_{a}{b}" for a, b in PAIRS],
                *[f"xi_{a}{b}" for a, b in PAIRS],
                *[f"de{cut}^{internal}" for cut in (1, 2) for internal in INTERNAL],
            ],
        },
        "planar": {
            "Q03_at_b_1": str(q[PAIR_INDEX[(0, 3)]]),
            "dQ_shape": list(dq.shape),
            "dQ_rank": dq.rank(),
            "dQ_nullity": len(dq.nullspace()),
            "corner_witness": str(corner_value),
        },
        "shell": {
            "candidate_shape": list(candidate_shell.shape),
            "honest_shape": list(honest.shape),
            "honest_rank": honest.rank(),
            "candidate_rank": shell_rank,
            "candidate_nullity": shell_nullity,
            "xi_deltae_nonzero_entries": sum(
                1 for row in candidate_xi_e for entry in row if entry
            ),
            "null_certificates": [name for name, _ in certificates],
            "shortcut_rank": shortcut.rank(),
            "honest_equals_shortcut": honest == shortcut,
            "fixed_reference_rank": fixed_shell.rank(),
        },
        "moment_map": {
            "gauge_vector": "chi_v=0, xi=-Ad_g(alpha_-)",
            "direct_result": "+Ad_(g^-1)Q",
            "adjoint_test": "rational 01 boost cosh=5/3 sinh=4/3",
        },
        "mutation_controls": {
            "cross-block-delete": "detected",
            "moment-sign": "detected",
            "q-factor": "detected",
            "independent-dlambda": "detected",
        },
        "representation": {
            "coefficients": "fractions.Fraction",
            "equality": "canonical sparse-form and exact entrywise matrix equality",
            "assembly": "lambda=-Q and dlambda=-dQ substituted before differentiation",
            "floats": False,
            "random_sampling": False,
            "CAS": False,
            "independent_verification": False,
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
    except Exception as exc:  # noqa: BLE001
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    if outcome not in {PASSED, FAILED, INCONCLUSIVE}:
        print(f"{OBLIGATION_ID} returned undefined status {outcome!r}", file=sys.stderr)
        return ERROR
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
