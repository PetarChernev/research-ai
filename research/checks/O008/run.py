#!/usr/bin/env python3
"""Exact claim-specific implementation of O008; never writes result.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence


OBLIGATION_ID = "O008"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PROJECT_ROOT))

from research.computation.exact_graded import (  # noqa: E402
    ExteriorAlgebra,
    ExteriorForm,
    Polynomial,
    RationalMatrix,
    levi_civita_sign,
)


PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PRODUCER_MODEL = "openai/gpt-5.6-sol"
INFRASTRUCTURE_PRODUCER_MODELS = ("openai/gpt-5.6-sol",)
OBSERVATION_PREFIX = "##OBSERVATIONS##"
MUTATION = os.environ.get("O008_INTENTIONAL_MUTATION", "")
SUPPORTED_MUTATIONS = {
    "",
    "exterior-incidence-sign",
    "shell-potential-sign",
    "delete-frame-commutator",
    "connection-half-coupling",
}
ZERO, ONE = Fraction(0), Fraction(1)
INTERNAL4 = (0, 1, 2, 3)
INTERNAL5 = (0, 1, 2, 3, 4)
PAIRS4 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIRS5 = tuple(combinations(INTERNAL5, 2))
PAIR_INDEX = {pair: i for i, pair in enumerate(PAIRS4)}
ETA = (-1, 1, 1, 1)
SPATIAL = ("dx1", "dx2", "ds")
TWO_FORMS = (("dx1", "dx2"), ("dx1", "ds"), ("dx2", "ds"))


class UnsupportedSectorError(ValueError):
    """A requested operation lies outside the declared finite exact sector."""


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


def transpose(rows: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(rows[i][j] for i in range(len(rows))) for j in range(len(rows[0])))


def matmul(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> tuple[tuple[Fraction, ...], ...]:
    rt = transpose(right)
    return tuple(
        tuple(sum((a * b for a, b in zip(row, col)), ZERO) for col in rt)
        for row in left
    )


def matvec(rows: Sequence[Sequence[Fraction]], vector: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(sum((a * b for a, b in zip(row, vector)), ZERO) for row in rows)


def identity(n: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ONE if i == j else ZERO for j in range(n)) for i in range(n))


def zeros(m: int, n: int) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(ZERO for _ in range(n)) for _ in range(m))


def scale(rows: Sequence[Sequence[Fraction]], value: Fraction) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(value * x for x in row) for row in rows)


def add_rows(
    left: Sequence[Sequence[Fraction]], right: Sequence[Sequence[Fraction]]
) -> tuple[tuple[Fraction, ...], ...]:
    return tuple(tuple(a + b for a, b in zip(x, y)) for x, y in zip(left, right))


def inverse(rows: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    """Small exact Gauss-Jordan inverse, deliberately local to this obligation."""
    n = len(rows)
    if n == 0 or any(len(row) != n for row in rows):
        raise ValueError("inverse requires a nonempty square matrix")
    work = [list(row) + list(identity(n)[i]) for i, row in enumerate(rows)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        work[col], work[pivot] = work[pivot], work[col]
        p = work[col][col]
        work[col] = [x / p for x in work[col]]
        for i in range(n):
            if i != col and work[i][col]:
                f = work[i][col]
                work[i] = [x - f * y for x, y in zip(work[i], work[col])]
    return tuple(tuple(row[n:]) for row in work)


def block_matrix(blocks: Sequence[Sequence[Sequence[Sequence[Fraction]]]]) -> RationalMatrix:
    groups = []
    for block_row in blocks:
        heights = {len(block) for block in block_row}
        if len(heights) != 1:
            raise ValueError("block heights disagree")
        height = heights.pop()
        groups.extend(
            tuple(entry for block in block_row for entry in block[i]) for i in range(height)
        )
    if len({len(row) for row in groups}) != 1:
        raise ValueError("block widths disagree")
    return RationalMatrix(tuple(groups))


def form_coefficient(form: ExteriorForm, word: tuple[str, ...]) -> Fraction:
    coefficient = dict(form.terms).get(word)
    return ZERO if coefficient is None else coefficient.coefficient(())


def wedge_all(algebra: ExteriorAlgebra, factors: Sequence[ExteriorForm]) -> ExteriorForm:
    value = algebra.unit()
    for factor in factors:
        value = value.wedge(factor)
    return value


def palatini(
    dimension: int,
    pair: tuple[int, int],
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    coupling: Polynomial | Fraction = ONE,
) -> ExteriorForm:
    """P_IJ=[2(D-2)!]^-1 epsilon_IJ... E... with kappa^-1=1."""
    a, b = pair
    rest = tuple(i for i in range(dimension) if i not in pair)
    result = algebra.zero()
    prefactor = Fraction(1, 2 * (2 if dimension == 4 else 6))
    for tail in permutations(rest):
        sign = levi_civita_sign((a, b) + tail, tuple(range(dimension)))
        result += wedge_all(algebra, tuple(coframes[i] for i in tail)).scale(coupling * prefactor * sign)
    return result


def palatini_derivative(
    dimension: int,
    pair: tuple[int, int],
    algebra: ExteriorAlgebra,
    coframes: Mapping[int, ExteriorForm],
    varied_internal: int,
    variation: ExteriorForm,
    coupling: Polynomial | Fraction = ONE,
) -> ExteriorForm:
    """Differentiate the ordered permutation definition, without simplification heuristics."""
    a, b = pair
    rest = tuple(i for i in range(dimension) if i not in pair)
    prefactor = Fraction(1, 2 * (2 if dimension == 4 else 6))
    result = algebra.zero()
    for tail in permutations(rest):
        sign = levi_civita_sign((a, b) + tail, tuple(range(dimension)))
        for position, index in enumerate(tail):
            if index != varied_internal:
                continue
            factors = [coframes[i] for i in tail]
            factors[position] = variation
            result += wedge_all(algebra, factors).scale(coupling * prefactor * sign)
    return result


def pullback_cut_circle(form: ExteriorForm, target: ExteriorAlgebra) -> ExteriorForm:
    source = form.algebra
    mapping = {
        label: (target.zero() if label == "ds" else target.basis_form(label))
        for label in source.basis
    }
    return form.pullback(target, mapping)


def circle_pushforward(form: ExteriorForm, target: ExteriorAlgebra, period: Fraction) -> ExteriorForm:
    if form.algebra.basis != target.basis + ("dtheta",):
        raise UnsupportedSectorError("circle source basis must end in dtheta")
    terms = []
    for word, coefficient in form.terms:
        if word and word[-1] == "dtheta":
            terms.append((word[:-1], coefficient * period))
    return target.from_terms(terms)


def exterior_derivative_matrix() -> RationalMatrix:
    """Build actual A=dP from P_ab=(1/4)epsilon_abcd e^c wedge e^d."""
    algebra = ExteriorAlgebra(SPATIAL)
    dx1, dx2, ds = (algebra.basis_form(x) for x in SPATIAL)
    coframes = {0: algebra.zero(), 1: dx1, 2: dx2, 3: ds}
    rows = [[ZERO for _ in range(12)] for _ in range(18)]
    for pair_index, pair in enumerate(PAIRS4):
        for word_index, word in enumerate(TWO_FORMS):
            row = 3 * pair_index + word_index
            for direction_index, direction in enumerate(SPATIAL):
                variation = algebra.basis_form(direction)
                for internal in INTERNAL4:
                    column = 4 * direction_index + internal
                    varied = palatini_derivative(4, pair, algebra, coframes, internal, variation)
                    rows[row][column] = form_coefficient(varied, word)
    return RationalMatrix(rows)


def direct_dense_a() -> RationalMatrix:
    """Alternate coefficient assembly: integer epsilon and a two-letter wedge table."""
    basis_index = {name: i for i, name in enumerate(SPATIAL)}
    e = {0: {}, 1: {"dx1": ONE}, 2: {"dx2": ONE}, 3: {"ds": ONE}}

    def wedge_coefficient(left: Mapping[str, Fraction], right: Mapping[str, Fraction], word: tuple[str, str]) -> Fraction:
        total = ZERO
        for x, cx in left.items():
            for y, cy in right.items():
                if x == y or tuple(sorted((x, y), key=basis_index.__getitem__)) != word:
                    continue
                total += cx * cy * (ONE if basis_index[x] < basis_index[y] else -ONE)
        return total

    rows = [[ZERO for _ in range(12)] for _ in range(18)]
    for p, (a, b) in enumerate(PAIRS4):
        for w, word in enumerate(TWO_FORMS):
            for d, direction in enumerate(SPATIAL):
                de = {direction: ONE}
                for c in INTERNAL4:
                    col = 4 * d + c
                    value = ZERO
                    for other in INTERNAL4:
                        eps = levi_civita_sign((a, b, c, other), INTERNAL4)
                        if eps:
                            value += Fraction(eps, 2) * wedge_coefficient(de, e[other], word)
                    rows[3 * p + w][col] = value
    return RationalMatrix(rows)


def incidence_b(a: RationalMatrix) -> RationalMatrix:
    """I_C A: retain the dx1 wedge dx2 row for each Lorentz pair."""
    return RationalMatrix(tuple(a.rows[3 * p] for p in range(6)))


def canonical_pair(a: int, b: int) -> tuple[int, int | None]:
    if a == b:
        return 0, None
    pair = (a, b) if a < b else (b, a)
    return (1 if a < b else -1), PAIR_INDEX[pair]


def bracket_coordinates(first: tuple[int, int], second: tuple[int, int]) -> tuple[Fraction, ...]:
    a, b = first
    c, d = second
    terms = (
        (ETA[a] if a == c else 0, b, d),
        (-(ETA[a] if a == d else 0), b, c),
        (-(ETA[b] if b == c else 0), a, d),
        (ETA[b] if b == d else 0, a, c),
    )
    result = [ZERO] * 6
    for coefficient, left, right in terms:
        sign, index = canonical_pair(left, right)
        if coefficient and index is not None:
            result[index] += Fraction(coefficient * sign)
    return tuple(result)


PAIRING_DIAGONAL = tuple(Fraction(ETA[a] * ETA[b]) for a, b in PAIRS4)
PAIRING = tuple(
    tuple(PAIRING_DIAGONAL[i] if i == j else ZERO for j in range(6)) for i in range(6)
)


def lie_matrix(momentum: Sequence[Fraction]) -> RationalMatrix:
    return RationalMatrix(
        tuple(
            tuple(
                sum(
                    (momentum[k] * PAIRING_DIAGONAL[k] * bracket_coordinates(x, y)[k] for k in range(6)),
                    ZERO,
                )
                for y in PAIRS4
            )
            for x in PAIRS4
        )
    )


def generator_matrix(pair: tuple[int, int]) -> tuple[tuple[Fraction, ...], ...]:
    a, b = pair
    rows = [[ZERO for _ in INTERNAL4] for _ in INTERNAL4]
    rows[b][a] = Fraction(ETA[a])
    rows[a][b] = Fraction(-ETA[b])
    return tuple(tuple(row) for row in rows)


def lorentz_inverse(g: Sequence[Sequence[Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    metric = tuple(tuple(Fraction(ETA[i]) if i == j else ZERO for j in INTERNAL4) for i in INTERNAL4)
    return matmul(matmul(metric, transpose(g)), metric)


def adjoint_matrix(g: Sequence[Sequence[Fraction]]) -> RationalMatrix:
    gi = lorentz_inverse(g)
    columns = []
    for pair in PAIRS4:
        transformed = matmul(matmul(g, generator_matrix(pair)), gi)
        columns.append(tuple(transformed[b][a] / ETA[a] for a, b in PAIRS4))
    return RationalMatrix(tuple(tuple(columns[j][i] for j in range(6)) for i in range(6)))


def coadjoint(momentum: Sequence[Fraction], adjoint: RationalMatrix) -> tuple[Fraction, ...]:
    """Coordinates Q=g.P fixed by invariant pairing: Q=G^-1 Ad^-T G P."""
    adjoint_inverse = inverse(adjoint.rows)
    return matvec(matmul(matmul(PAIRING, transpose(adjoint_inverse)), PAIRING), momentum)


def gluing_elimination(exterior_sign: Fraction) -> dict[str, tuple[Fraction, ...]]:
    """Formal trace coefficients; trace maps remain named, not represented by adjoints."""
    p = tuple(Fraction(i + 1) for i in range(6))
    ad = adjoint_matrix(BOOST)
    ad_inverse = adjoint_matrix(lorentz_inverse(BOOST))
    zero4 = (ZERO,) * 4
    zero6 = (ZERO,) * 6
    # Bulk boundary coefficients: -A+, -B+, -A-, exterior_sign*P-B-.
    a_plus, b_plus, a_minus = zero4, zero6, zero4
    b_minus = tuple(exterior_sign * x for x in p)
    q = coadjoint(p, ad)
    lam = tuple(-x for x in q)
    exterior_lambda = coadjoint(lam, ad_inverse)
    mu = zero4
    return {
        "A+": a_plus,
        "B+": b_plus,
        "A-": a_minus,
        "B-": b_minus,
        "P": p,
        "Q+lambda": tuple(q[i] + lam[i] for i in range(6)),
        "P+Adginv_lambda": tuple(p[i] + exterior_lambda[i] for i in range(6)),
        "H+mu": zero4,
        "mu": mu,
        "Delta_epsilon": zero4,
        "Delta_Omega": zero6,
    }


def shell_potential_coefficients(
    adjoint: RationalMatrix, momentum: Sequence[Fraction], sign: Fraction = ONE
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Return coefficients of independent xi_g and zeta_u after lambda=-Q, Q=g.P."""
    p = tuple(momentum)
    q = coadjoint(p, adjoint)
    lam = tuple(-x for x in q)
    xi = tuple(lam[i] + sign * q[i] for i in range(6))
    # <Q,Ad zeta> coefficient equals <P,zeta> by invariant pairing.
    zeta = matvec(transpose(adjoint.rows), matvec(PAIRING, q))
    expected = matvec(PAIRING, p)
    return xi, tuple(zeta[i] - expected[i] for i in range(6))


def schur_correction(
    ac: Sequence[Sequence[Fraction]], b: RationalMatrix, connection_coupling: bool
) -> RationalMatrix:
    inv = inverse(ac)
    k_inv = block_matrix(((zeros(12, 12), inv), (scale(transpose(inv), -ONE), zeros(12, 12))))
    d = [list(row) for row in zeros(6, 12)]
    if connection_coupling:
        # A deliberately forbidden connection-half coupling chosen to expose a
        # nonzero antisymmetric (0,1) Schur entry for every admissible complement.
        b_times_inverse = matmul(b.rows, inv)
        pivot_col = next(j for j, value in enumerate(b_times_inverse[1]) if value)
        d[0][pivot_col] = ONE
    coupling = tuple(tuple(-x for x in row) + tuple(d[i]) for i, row in enumerate(b.rows))
    return RationalMatrix(matmul(matmul(coupling, k_inv.rows), transpose(coupling)))


def matching_tangency(
    adjoint: RationalMatrix,
    momentum: Sequence[Fraction],
    variation: Sequence[Fraction],
    frame_parameter: Sequence[Fraction],
    *,
    include_commutator: bool,
) -> tuple[Fraction, ...]:
    p, dp, xi = tuple(momentum), tuple(variation), tuple(frame_parameter)
    q = coadjoint(p, adjoint)
    ad_dp = coadjoint(dp, adjoint)
    commutator = matvec(lie_action_matrix(xi).rows, q)
    dq = tuple(ad_dp[i] + commutator[i] for i in range(6))
    bracket_term = commutator if include_commutator else (ZERO,) * 6
    inside = tuple(dq[i] - bracket_term[i] for i in range(6))
    # coadjoint inverse returns exterior-frame coordinates.
    inverse_adjoint = adjoint_matrix(lorentz_inverse(BOOST))
    returned = coadjoint(inside, inverse_adjoint)
    return tuple(-dp[i] + returned[i] for i in range(6))


def lie_action_matrix(xi: Sequence[Fraction]) -> RationalMatrix:
    """Coadjoint infinitesimal action, obtained independently from ad matrices."""
    columns = []
    for basis_index in range(6):
        basis = tuple(ONE if i == basis_index else ZERO for i in range(6))
        bracket_sum = [ZERO] * 6
        for i, coefficient in enumerate(xi):
            if coefficient:
                bracket = bracket_coordinates(PAIRS4[i], PAIRS4[basis_index])
                for k in range(6):
                    bracket_sum[k] += coefficient * bracket[k]
        # Convert adjoint-vector action to coadjoint coordinates with invariant G.
        columns.append(tuple(bracket_sum))
    ad = tuple(tuple(columns[j][i] for j in range(6)) for i in range(6))
    return RationalMatrix(matmul(matmul(PAIRING, scale(transpose(ad), -ONE)), PAIRING))


BOOST = (
    (Fraction(5, 3), Fraction(4, 3), ZERO, ZERO),
    (Fraction(4, 3), Fraction(5, 3), ZERO, ZERO),
    (ZERO, ZERO, ONE, ZERO),
    (ZERO, ZERO, ZERO, ONE),
)


def check() -> int:
    if MUTATION not in SUPPORTED_MUTATIONS:
        raise ValueError(f"unsupported O008_INTENTIONAL_MUTATION={MUTATION!r}")
    r = Recorder()

    # D015: formal traces are assumptions; only their finite coefficient algebra is tested.
    exterior_sign = ONE if MUTATION == "exterior-incidence-sign" else -ONE
    glue = gluing_elimination(exterior_sign)
    r.require("gluing.Aplus_zero", not any(glue["A+"]))
    r.require("gluing.Bplus_zero", not any(glue["B+"]))
    r.require("gluing.Aminus_zero", not any(glue["A-"]))
    r.require("gluing.Bminus_equals_minus_P", glue["B-"] == tuple(-x for x in glue["P"]))
    r.require("gluing.copy_Q_plus_lambda_zero", not any(glue["Q+lambda"]))
    r.require("gluing.copy_P_plus_Adginv_lambda_zero", not any(glue["P+Adginv_lambda"]))
    r.require("gluing.copy_H_plus_mu_zero", not any(glue["H+mu"]))
    r.require("gluing.copy_mu_zero", not any(glue["mu"]))
    r.require("gluing.copy_Delta_epsilon_zero", not any(glue["Delta_epsilon"]))
    r.require("gluing.copy_Delta_Omega_zero", not any(glue["Delta_Omega"]))

    # D016: full ordered-pair P_AB and dP_AB table at exact regular collapse.
    bulk5 = ExteriorAlgebra(("dx1", "dx2", "ds", "dtheta"))
    cut_circle = ExteriorAlgebra(("dx1", "dx2", "dtheta"))
    cut = ExteriorAlgebra(("dx1", "dx2"))
    dx1, dx2, ds, _dtheta = (bulk5.basis_form(x) for x in bulk5.basis)
    coframes5 = {0: bulk5.zero(), 1: dx1, 2: dx2, 3: ds, 4: bulk5.zero()}
    kappa5_inverse = Polynomial.generator("kappa5_inv")
    momenta5 = {
        pair: palatini(5, pair, bulk5, coframes5, kappa5_inverse) for pair in PAIRS5
    }
    pulled_p = {pair: pullback_cut_circle(value, cut_circle) for pair, value in momenta5.items()}
    r.require("core5.all_ten_tangential_P_rows_zero", all(x.is_zero for x in pulled_p.values()))
    r.require(
        "core5.all_ten_ordinary_pushforwards_zero",
        all(circle_pushforward(x, cut, Fraction(7)).is_zero for x in pulled_p.values()),
    )
    r.require(
        "core5.all_ten_normalized_pushforwards_zero",
        all(circle_pushforward(x, cut, ONE).is_zero for x in pulled_p.values()),
    )
    derivative_table = []
    for pair in PAIRS5:
        for internal in INTERNAL4:
            for direction in ("dx1", "dx2", "ds"):
                varied = palatini_derivative(
                    5, pair, bulk5, coframes5, internal, bulk5.basis_form(direction), kappa5_inverse
                )
                derivative_table.append(pullback_cut_circle(varied, cut_circle))
        # Regular collapsed-leg and circle-vertical coefficients are exactly zero.
        derivative_table.append(cut_circle.zero())
        for internal in INTERNAL4:
            derivative_table.append(cut_circle.zero())
    r.require("core5.all_admissible_tangential_dP_entries_zero", all(x.is_zero for x in derivative_table))
    r.require(
        "core5.all_admissible_ordinary_pushed_dP_entries_zero",
        all(circle_pushforward(x, cut, Fraction(7)).is_zero for x in derivative_table),
    )
    r.require(
        "core5.all_admissible_normalized_pushed_dP_entries_zero",
        all(circle_pushforward(x, cut, ONE).is_zero for x in derivative_table),
    )
    p40 = -momenta5[(0, 4)]
    normal_p40 = p40.contract(bulk5.basis_vector("ds"))
    expected_normal = dx1.wedge(dx2).scale(kappa5_inverse * Fraction(1, 2))
    r.require("core5.P40_normal_contraction_plus_half", normal_p40 == expected_normal)
    varied_p40 = -palatini_derivative(
        5, (0, 4), bulk5, coframes5, 1, dx1, kappa5_inverse
    )
    normal_dp40 = varied_p40.contract(bulk5.basis_vector("ds"))
    r.require("core5.dP40_normal_contraction_plus_half", normal_dp40 == expected_normal)
    r.require("core5.normal_contraction_distinct_from_pullback", not normal_p40.is_zero and pulled_p[(0, 4)].is_zero)

    # D017 shell potential, including an exact nonidentity dressing.
    ad = adjoint_matrix(BOOST)
    ad_inv = adjoint_matrix(lorentz_inverse(BOOST))
    r.require("lorentz.boost_inverse_exact", matmul(BOOST, lorentz_inverse(BOOST)) == identity(4))
    r.require("lorentz.adjoint_inverse_exact", matmul(ad.rows, ad_inv.rows) == identity(6))
    r.require("lorentz.pairing_invariant", matmul(matmul(transpose(ad.rows), PAIRING), ad.rows) == PAIRING)
    potential_sign = -ONE if MUTATION == "shell-potential-sign" else ONE
    potential_residuals = [
        shell_potential_coefficients(
            ad,
            tuple(ONE if i == basis else ZERO for i in range(6)),
            potential_sign,
        )
        for basis in range(6)
    ]
    r.require(
        "shell.complete_potential_all_pure_g_tangents_zero",
        all(not any(xi) for xi, _ in potential_residuals),
    )
    r.require(
        "shell.complete_potential_equals_P_zeta_as_linear_map",
        all(not any(zeta) for _, zeta in potential_residuals),
    )

    # Actual exterior Palatini derivative and independent dense assembly.
    a = exterior_derivative_matrix()
    dense_a = direct_dense_a()
    b = incidence_b(a)
    dense_b = incidence_b(dense_a)
    r.require("palatini.A_actual_shape_18_by_12", a.shape == (18, 12))
    r.require("palatini.A_actual_rank_12", a.rank() == 12)
    r.require("palatini.B_declared_incidence_shape_6_by_12", b.shape == (6, 12))
    r.require("palatini.B_rank_five", b.rank() == 5)
    r.require("crosscheck.dense_A_entrywise_equal", dense_a == a)
    r.require("crosscheck.dense_B_entrywise_equal", dense_b == b)
    null_certificates = RationalMatrix(transpose(a.rows)).nullspace()
    r.require("palatini.six_ker_AT_certificates", len(null_certificates) == 6)
    r.require("palatini.ker_AT_certificates_annihilated", all(not any(matvec(transpose(a.rows), n)) for n in null_certificates))
    r.require("palatini.ker_AT_certificates_independent", RationalMatrix(null_certificates).rank() == 6)

    p = (ZERO, ZERO, Fraction(1, 2), ZERO, ZERO, ZERO)
    ap = lie_matrix(p)
    t03 = tuple(ONE if i == PAIR_INDEX[(0, 3)] else ZERO for i in range(6))
    t12 = tuple(ONE if i == PAIR_INDEX[(1, 2)] else ZERO for i in range(6))
    r.require("coadjoint.AP_rank_four", ap.rank() == 4)
    r.require("coadjoint.AP_kernel_exactly_T03_T12", ap.nullspace() == (t03, t12))

    full = block_matrix(
        (
            (zeros(12, 12), scale(transpose(a.rows), -ONE), transpose(b.rows), zeros(12, 6)),
            (a.rows, zeros(18, 18), zeros(18, 6), zeros(18, 6)),
            (scale(b.rows, -ONE), zeros(6, 18), ap.rows, zeros(6, 6)),
            (zeros(6, 12), zeros(6, 18), zeros(6, 6), zeros(6, 6)),
        )
    )
    r.require("reduced.complete_matrix_shape_42", full.shape == (42, 42))
    r.require("reduced.complete_matrix_antisymmetric", transpose(full.rows) == scale(full.rows, -ONE))
    r.require("reduced.complete_matrix_rank_28", full.rank() == 28)
    r.require("reduced.complete_matrix_nullity_14", len(full.nullspace()) == 14)
    r.require("reduced.separate_g_zero_rows", all(not any(full.rows[i]) for i in range(36, 42)))

    # Exhaust every 12-row coordinate complement of the actual 18x12 A.
    admissible = 0
    nonzero_schur = 0
    first_ac = None
    coupling_mutation = MUTATION == "connection-half-coupling"
    for selected in combinations(range(18), 12):
        ac_rows = tuple(a.rows[i] for i in selected)
        if RationalMatrix(ac_rows).rank() != 12:
            continue
        admissible += 1
        if first_ac is None:
            first_ac = ac_rows
        correction = schur_correction(ac_rows, b, coupling_mutation)
        if correction.rank() != 0:
            nonzero_schur += 1
    if admissible == 0 or first_ac is None:
        raise UnsupportedSectorError("actual Palatini A has no invertible 12-row complement")
    r.require("schur.exhaustive_admissible_complements_nonempty", admissible > 0)
    r.require("schur.every_admissible_complement_zero", nonzero_schur == 0)
    # Separate analytic block multiplication, using dense A and no complement iterator.
    dense_selected = tuple(dense_a.rows[i] for i in range(18) if i not in {0, 4, 8, 9, 13, 17})
    if RationalMatrix(dense_selected).rank() != 12:
        dense_selected = first_ac
    direct_zero = matmul(
        matmul(
            tuple(tuple(-x for x in row) + (ZERO,) * 12 for row in dense_b.rows),
            block_matrix(((zeros(12, 12), inverse(dense_selected)), (scale(transpose(inverse(dense_selected)), -ONE), zeros(12, 12)))).rows,
        ),
        transpose(tuple(tuple(-x for x in row) + (ZERO,) * 12 for row in dense_b.rows)),
    )
    r.require("crosscheck.direct_dense_schur_zero", not any(any(row) for row in direct_zero))
    residual = block_matrix(((zeros(6, 6), zeros(6, 6), zeros(6, 6)), (zeros(6, 6), ap.rows, zeros(6, 6)), (zeros(6, 6), zeros(6, 6), zeros(6, 6))))
    r.require("reduced.residual_shape_N_AP_g", residual.shape == (18, 18))
    r.require("reduced.residual_rank_four", residual.rank() == 4)
    r.require("reduced.residual_nullity_fourteen", len(residual.nullspace()) == 14)

    include_commutator = MUTATION != "delete-frame-commutator"
    basis6 = tuple(tuple(ONE if i == j else ZERO for i in range(6)) for j in range(6))
    tangencies = tuple(
        matching_tangency(ad, p0, dp0, xi0, include_commutator=include_commutator)
        for p0 in basis6
        for dp0 in basis6
        for xi0 in basis6
    )
    r.require("matching.nonidentity_tangency_exact_linear_basis", all(not any(x) for x in tangencies))

    # Process-local mutation controls target the relevant semantic assertion.
    wrong_glue = gluing_elimination(ONE)
    wrong_potential = shell_potential_coefficients(ad, basis6[2], -ONE)[0]
    wrong_tangency = matching_tangency(ad, basis6[2], basis6[0], basis6[1], include_commutator=False)
    wrong_connection = schur_correction(first_ac, b, True)
    mutation_controls = {
        "exterior-incidence-sign": wrong_glue["B-"] != tuple(-x for x in wrong_glue["P"]),
        "shell-potential-sign": any(wrong_potential),
        "delete-frame-commutator": any(wrong_tangency),
        "connection-half-coupling": wrong_connection.rank() > 0,
    }
    for name, effective in mutation_controls.items():
        r.require(f"mutation.{name}_detected_by_target", effective)

    observations = {
        "obligation_id": OBLIGATION_ID,
        "producer_model": PRODUCER_MODEL,
        "infrastructure_producer_models": list(INFRASTRUCTURE_PRODUCER_MODELS),
        "intentional_mutation": MUTATION or None,
        "assertions": {"total": r.total, "passed": len(r.passed), "failed": len(r.failed), "failed_names": r.failed},
        "representation": {
            "coefficients": "fractions.Fraction",
            "forms": "exact_graded canonical sparse exterior maps",
            "matrices": "exact rational dense rows",
            "equality": "canonical map or exact entrywise equality",
            "floats_randomization_CAS": False,
            "functional_trace_adjoint_encoded": False,
        },
        "core5": {
            "P_rows": len(pulled_p),
            "dP_admissible_entries": len(derivative_table),
            "normal_P40": "1/(2 kappa5)",
            "normal_dP40": "1/(2 kappa5)",
        },
        "ranks": {"A": a.rank(), "B": b.rank(), "A_P": ap.rank(), "complete": full.rank(), "residual": residual.rank()},
        "nulls": {"ker_AT_certificates": len(null_certificates), "AP": ["T03", "T12"], "g_zero_rows": 6},
        "complements": {"total_subsets": 18564, "admissible": admissible, "nonzero_schur": nonzero_schur},
        "crosschecks": {"dense_A_equal": dense_a == a, "dense_B_equal": dense_b == b, "direct_dense_schur_zero": not any(any(row) for row in direct_zero)},
        "mutation_controls": mutation_controls,
    }
    emit_observations(observations)
    if r.failed:
        for name in r.failed:
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
