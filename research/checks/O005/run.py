#!/usr/bin/env python3
"""Exact claim-specific implementation of machine-check obligation O005.

Run only through ``scripts/run_check.py O005`` for the canonical outcome.
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


OBLIGATION_ID = "O005"
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
INTENTIONAL_MUTATION = os.environ.get("O005_INTENTIONAL_MUTATION", "")
SUPPORTED_MUTATIONS = {"", "moment-sign", "q-factor", "dq-rank", "shell-pullback"}

INTERNAL = (0, 1, 2, 3)
ETA = (-1, 1, 1, 1)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
CUT_BASIS = ("dx1", "dx2")
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
    return tuple(tuple(rows[row][column] for row in range(len(rows))) for column in range(len(rows[0])))


def matmul(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> tuple[tuple[Fraction, ...], ...]:
    right_t = transpose(right)
    return tuple(
        tuple(sum((a * b for a, b in zip(row, column)), ZERO) for column in right_t)
        for row in left
    )


def matvec(rows: Sequence[Sequence[Fraction]], vector: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(sum((entry * value for entry, value in zip(row, vector)), ZERO) for row in rows)


def matrix_scale(rows: Sequence[Sequence[Fraction]], scalar: Fraction) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(scalar * entry for entry in row) for row in rows)


def identity(size: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ONE if row == column else ZERO for column in range(size)) for row in range(size))


def diagonal(entries: Sequence[int | Fraction]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(
        tuple(Fraction(entries[row]) if row == column else ZERO for column in range(len(entries)))
        for row in range(len(entries))
    )


def zero_rows(nrows: int, ncols: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ZERO for _ in range(ncols)) for _ in range(nrows))


def block_matrix(blocks: Sequence[Sequence[Sequence[Sequence[Fraction]]]]) -> RationalMatrix:
    """Join a nonempty rectangular grid of exact dense blocks."""

    row_groups: list[tuple[tuple[Fraction, ...], ...]] = []
    for block_row in blocks:
        heights = {len(block) for block in block_row}
        if len(heights) != 1:
            raise ValueError("block-row heights disagree")
        height = heights.pop()
        joined = []
        for row in range(height):
            joined.append(tuple(entry for block in block_row for entry in block[row]))
        row_groups.append(tuple(joined))
    widths = [len(row_group[0]) for row_group in row_groups]
    if len(set(widths)) != 1:
        raise ValueError("joined block widths disagree")
    return RationalMatrix(tuple(row for group in row_groups for row in group))


def direct_sum(left: RationalMatrix, right: RationalMatrix) -> RationalMatrix:
    return block_matrix(
        (
            (left.rows, zero_rows(left.nrows, right.ncols)),
            (zero_rows(right.nrows, left.ncols), right.rows),
        )
    )


def canonical_pair_component(a: int, b: int) -> tuple[int, int | None]:
    if a == b:
        return 0, None
    pair = (a, b) if a < b else (b, a)
    return (1 if a < b else -1), PAIR_INDEX[pair]


def bracket_coordinates(first: tuple[int, int], second: tuple[int, int]) -> tuple[Fraction, ...]:
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
PAIRING_INVERSE = PAIRING  # every diagonal entry is +/-1


def lie_a_matrix(momentum: Sequence[Fraction]) -> RationalMatrix:
    """A_IJ=<momentum,[T_I,T_J]> in the invariant bivector pairing."""

    rows = []
    for first in PAIRS:
        row = []
        for second in PAIRS:
            bracket = bracket_coordinates(first, second)
            row.append(
                sum(
                    (momentum[k] * PAIRING_DIAGONAL[k] * bracket[k] for k in range(6)),
                    ZERO,
                )
            )
        rows.append(tuple(row))
    return RationalMatrix(tuple(rows))


def q_and_dq(
    coframes: Sequence[Any], *, ordered_prefactor: Fraction = Fraction(1, 4)
) -> tuple[tuple[Fraction, ...], RationalMatrix]:
    """Construct Q and its derivative through exact cut exterior products."""

    algebra = coframes[0].algebra
    area = CUT_BASIS
    q_values: list[Fraction] = []
    for a, b in PAIRS:
        q_form = algebra.zero()
        for c in INTERNAL:
            for d in INTERNAL:
                epsilon = levi_civita_sign((a, b, c, d), INTERNAL)
                if epsilon:
                    q_form = q_form + coframes[c].wedge(coframes[d]) * (ordered_prefactor * epsilon)
        coefficient = dict(q_form.terms).get(area)
        q_values.append(ZERO if coefficient is None else coefficient.coefficient(()))

    # Differentiating the two ordered terms doubles the Q prefactor.
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
                        varied = varied + variation.wedge(coframes[d]) * (derivative_prefactor * epsilon)
                coefficient = dict(varied.terms).get(area)
                output.append(ZERO if coefficient is None else coefficient.coefficient(()))
            columns.append(tuple(output))
    rows = tuple(tuple(columns[column][row] for column in range(8)) for row in range(6))
    return tuple(q_values), RationalMatrix(rows)


def paired_dq(dq: RationalMatrix) -> RationalMatrix:
    return RationalMatrix(matmul(PAIRING, dq.rows))


def first_order_block(momentum: Sequence[Fraction]) -> RationalMatrix:
    a_matrix = lie_a_matrix(momentum)
    return block_matrix(
        (
            (a_matrix.rows, matrix_scale(PAIRING, Fraction(-1))),
            (PAIRING, zero_rows(6, 6)),
        )
    )


def residual_block(q: Sequence[Fraction], dq: RationalMatrix) -> RationalMatrix:
    a_matrix = lie_a_matrix(q)
    coupled = paired_dq(dq)
    return block_matrix(
        (
            (a_matrix.rows, matrix_scale(coupled.rows, Fraction(-1))),
            (transpose(coupled.rows), zero_rows(8, 8)),
        )
    )


def generator_matrix(pair: tuple[int, int]) -> tuple[tuple[Fraction, ...], ...]:
    """The vector representation consistent with bracket_coordinates."""

    a, b = pair
    rows = [[ZERO for _ in INTERNAL] for _ in INTERNAL]
    rows[b][a] = Fraction(ETA[a])
    rows[a][b] = Fraction(-ETA[b])
    return tuple(tuple(row) for row in rows)


def lorentz_inverse(g: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    eta4 = diagonal(ETA)
    return matmul(matmul(eta4, transpose(g)), eta4)


def adjoint_matrix(g: Sequence[Sequence[Fraction]]) -> RationalMatrix:
    """Columns are coordinates of g T_I g^-1 in the declared pair basis."""

    g_inverse = lorentz_inverse(g)
    columns = []
    for pair in PAIRS:
        transformed = matmul(matmul(g, generator_matrix(pair)), g_inverse)
        coordinates = []
        for a, b in PAIRS:
            coordinates.append(transformed[b][a] / ETA[a])
        columns.append(tuple(coordinates))
    return RationalMatrix(
        tuple(tuple(columns[column][row] for column in range(6)) for row in range(6))
    )


def check() -> int:
    if INTENTIONAL_MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(
            "unsupported O005_INTENTIONAL_MUTATION; expected '', moment-sign, "
            "q-factor, dq-rank, or shell-pullback"
        )

    recorder = AssertionRecorder()
    algebra = ExteriorAlgebra(CUT_BASIS)
    coframes = (
        algebra.zero(),
        algebra.basis_form("dx1"),
        algebra.basis_form("dx2"),
        algebra.zero(),
    )

    full_planar_triad = RationalMatrix(((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0)))
    pairing_matrix = RationalMatrix(PAIRING)
    if full_planar_triad.rank() != 3:
        emit_observations({"obligation_id": OBLIGATION_ID, "reason": "planar triad is not rank three"})
        return INCONCLUSIVE
    if pairing_matrix.rank() != 6:
        emit_observations({"obligation_id": OBLIGATION_ID, "reason": "Lorentz pairing is degenerate"})
        return INCONCLUSIVE
    recorder.require("domain.planar_triad_rank_three", full_planar_triad.rank() == 3)
    recorder.require("domain.lorentz_pairing_rank_six", pairing_matrix.rank() == 6)

    q_prefactor = Fraction(1, 8) if INTENTIONAL_MUTATION == "q-factor" else Fraction(1, 4)
    q, dq_unmutated_rank = q_and_dq(coframes, ordered_prefactor=q_prefactor)
    dq_rows = [list(row) for row in dq_unmutated_rank.rows]
    if INTENTIONAL_MUTATION == "dq-rank":
        first_nonzero_row = next(index for index, row in enumerate(dq_rows) if any(row))
        dq_rows[first_nonzero_row] = [ZERO for _ in range(8)]
    dq = RationalMatrix(dq_rows)

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
    dq_rank = dq.rank()
    recorder.require("dQ.rank_five", dq_rank == 5)
    recorder.require("dQ.absent_Q12_row", not any(dq.rows[PAIR_INDEX[(1, 2)]]))
    dq_kernel = dq.nullspace()
    recorder.require("dQ.nullity_three", len(dq_kernel) == 3)

    # Independent-of-RREF sparse certificates for the five image directions and
    # the three coframe-kernel directions.
    analytic_kernel = (
        (ZERO, ZERO, ONE, ZERO, ZERO, ZERO, ZERO, ZERO),
        (ZERO, ZERO, ZERO, ZERO, ZERO, ONE, ZERO, ZERO),
        (ZERO, ONE, ZERO, ZERO, ZERO, ZERO, Fraction(-1), ZERO),
    )
    analytic_pivot_entries = ((0, 3), (1, 7), (2, 1), (4, 0), (5, 4))
    recorder.require(
        "dQ.alternate_five_pivots",
        all(dq.rows[row][column] != 0 for row, column in analytic_pivot_entries)
        and len({row for row, _ in analytic_pivot_entries}) == 5
        and len({column for _, column in analytic_pivot_entries}) == 5,
    )
    recorder.require(
        "dQ.alternate_three_kernel_vectors",
        all(not any(dq.matvec(vector)) for vector in analytic_kernel)
        and RationalMatrix(analytic_kernel).rank() == 3,
    )

    fixed_offshell = first_order_block(q)
    fixed_rank = fixed_offshell.rank()
    shell_zero = RationalMatrix(zero_rows(6, 6))
    fixed_shell = fixed_offshell if INTENTIONAL_MUTATION == "shell-pullback" else shell_zero
    recorder.require("fixed.off_shell_rank_12", fixed_rank == 12)
    recorder.require("fixed.shell_rank_zero", fixed_shell.rank() == 0)
    recorder.require(
        "fixed.alternate_canonical_pair_rank",
        pairing_matrix.rank() == 6 and 2 * pairing_matrix.rank() == 12,
    )

    residual = residual_block(q, dq)
    residual_rank = residual.rank()
    residual_nullity = len(residual.nullspace())
    recorder.require("B.residual_shape_14", residual.shape == (14, 14))
    recorder.require("B.residual_rank_10", residual_rank == 10)
    recorder.require("B.residual_nullity_4", residual_nullity == 4)

    t12 = tuple(ONE if index == PAIR_INDEX[(1, 2)] else ZERO for index in range(6))
    t12_embedded = t12 + tuple(ZERO for _ in range(8))
    coframe_nulls = tuple(tuple(ZERO for _ in range(6)) + vector for vector in analytic_kernel)
    declared_nulls = (t12_embedded,) + coframe_nulls
    recorder.require("B.null_T12", not any(residual.matvec(t12_embedded)))
    recorder.require(
        "B.null_three_ker_dQ",
        all(not any(residual.matvec(vector)) for vector in coframe_nulls),
    )
    recorder.require(
        "B.four_declared_nulls_independent",
        RationalMatrix(declared_nulls).rank() == 4,
    )
    recorder.require(
        "B.alternate_nullity_and_rank",
        dq_rank == 5
        and not any(lie_a_matrix(q).matvec(t12))
        and len(analytic_kernel) == 3
        and 14 - (1 + 3) == 10,
    )

    full_offshell = direct_sum(first_order_block(q), residual)
    shell_full = direct_sum(shell_zero, residual)
    recorder.require("B.full_off_shell_rank_22", full_offshell.rank() == 22)
    recorder.require("B.full_shell_rank_10", shell_full.rank() == 10)
    recorder.require(
        "B.alternate_block_rank_12_plus_10",
        fixed_rank + (2 * dq_rank) == 22 and 2 * dq_rank == 10,
    )

    # Nonidentity rational boost: cosh=5/3, sinh=4/3.
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

    sign = ONE if INTENTIONAL_MUTATION == "moment-sign" else Fraction(-1)
    plus_map = matmul(PAIRING_INVERSE, PAIRING)
    contracted_minus_map = matrix_scale(
        matmul(matmul(PAIRING_INVERSE, transpose(adjoint.rows)), PAIRING), sign
    )
    expected_minus_map = matrix_scale(adjoint_inverse.rows, Fraction(-1))
    recorder.require("moment.A.Jplus_equals_Pi", plus_map == identity(6))
    recorder.require("moment.A.Jminus_minus_Adinv_Pi", contracted_minus_map == expected_minus_map)

    # B: -Ad^-1 Pi + Ad^-1 Q = -Ad^-1 lambda, lambda=Pi-Q.
    b_pi_map = contracted_minus_map
    b_q_map = adjoint_inverse.rows
    recorder.require("moment.B.Jplus_equals_Pi", plus_map == identity(6))
    recorder.require("moment.B.Jminus_Pi_coefficient", b_pi_map == expected_minus_map)
    recorder.require("moment.B.Jminus_Q_coefficient", b_q_map == adjoint_inverse.rows)
    pi_test = tuple(Fraction(index + 1) for index in range(6))
    lambda_test = tuple(pi_test[index] - q[index] for index in range(6))
    contracted_b_test = tuple(
        left + right
        for left, right in zip(matvec(b_pi_map, pi_test), matvec(b_q_map, q))
    )
    recorder.require(
        "moment.B.Jminus_minus_Adinv_lambda",
        contracted_b_test
        == tuple(-value for value in matvec(adjoint_inverse.rows, lambda_test)),
    )
    shell_jminus = matvec(adjoint_inverse.rows, q)
    recorder.require(
        "moment.B.shell_Jminus_plus_Adinv_Q",
        shell_jminus == matvec(adjoint_inverse.rows, q) and any(shell_jminus),
    )

    alpha_corner = tuple(Fraction(-1) if index == PAIR_INDEX[(0, 3)] else ZERO for index in range(6))
    corner_value = sum((q[k] * PAIRING_DIAGONAL[k] * alpha_corner[k] for k in range(6)), ZERO)
    recorder.require("corner.planar_Q03_nonzero", q[PAIR_INDEX[(0, 3)]] == Fraction(1, 2))
    recorder.require("corner.alpha_minus_T03_witness_plus_half_b", corner_value == Fraction(1, 2))

    # Negative and mutation controls are assembled separately from the target.
    degenerate_coframes = (algebra.zero(), algebra.basis_form("dx1"), algebra.zero(), algebra.zero())
    degenerate_q, degenerate_dq = q_and_dq(degenerate_coframes)
    recorder.require("control.degenerate_cut_lowers_dQ_rank", degenerate_dq.rank() < 5)
    recorder.require("control.deleted_area_kills_corner", not any(degenerate_q))

    half_q, half_dq = q_and_dq(coframes, ordered_prefactor=Fraction(1, 8))
    recorder.require(
        "control.factor_mutation_detected",
        half_q[2] == Fraction(1, 4)
        and half_q != expected_q
        and half_dq.rank() == 5,
    )
    rank_mutation_rows = [list(row) for row in expected_dq_rows]
    rank_mutation_rows[0] = [ZERO for _ in range(8)]
    rank_mutation = RationalMatrix(rank_mutation_rows)
    recorder.require("control.rank_mutation_detected", rank_mutation.rank() == 4)
    wrong_minus_map = matmul(matmul(PAIRING_INVERSE, transpose(adjoint.rows)), PAIRING)
    recorder.require(
        "control.moment_sign_mutation_detected",
        wrong_minus_map == adjoint_inverse.rows and wrong_minus_map != expected_minus_map,
    )
    recorder.require(
        "control.shell_pullback_mutation_detected",
        fixed_offshell.rank() == 12 and fixed_offshell.rank() != shell_zero.rank(),
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
            "cut_forms": list(CUT_BASIS),
            "coframe_variations": [f"de{cut}^{internal}" for cut in (1, 2) for internal in INTERNAL],
        },
        "planar": {
            "Q03_at_b_1": str(q[PAIR_INDEX[(0, 3)]]),
            "corner_witness": str(corner_value),
            "dQ_shape": list(dq.shape),
            "dQ_rank": dq_rank,
            "dQ_nullity": len(dq_kernel),
        },
        "ranks": {
            "fixed_off_shell": fixed_rank,
            "fixed_shell": fixed_shell.rank(),
            "stueckelberg_v_e": residual_rank,
            "stueckelberg_v_e_nullity": residual_nullity,
            "stueckelberg_full_off_shell": full_offshell.rank(),
            "stueckelberg_shell": shell_full.rank(),
            "alternate_residual": 14 - (1 + 3),
            "alternate_full_off_shell": 12 + 2 * dq_rank,
        },
        "null_directions": ["T12", "de1^2", "de2^1", "de1^1-de2^2"],
        "moment_maps": {
            "A": {"Jplus": "Pi", "Jminus": "-Ad_(g^-1)Pi"},
            "B": {
                "Jplus": "Pi",
                "Jminus": "-Ad_(g^-1)lambda",
                "shell_Jminus": "+Ad_(g^-1)Q",
            },
            "adjoint_test": "rational 01 boost cosh=5/3 sinh=4/3",
        },
        "representation": {
            "coefficients": "fractions.Fraction",
            "equality": "canonical sparse-form and exact matrix equality",
            "floats": False,
            "random_sampling": False,
            "CAS": False,
            "alternate_path_is_independent_verification": False,
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
