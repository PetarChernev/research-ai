#!/usr/bin/env python3
"""Exact, claim-specific O014 obligation.  Never writes result.json.

The conclusion-critical path starts with one expression graph for

    B_V = -2 sum_{A,B} K^A V^B P_AB(E).

Its variation, integration by parts, Euler rows, generic connection residual,
Noether identity, and polar specialization are derived below.  Formulae used
as expectations are assembled separately from the D024 component statements.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Iterable, Mapping

OID = "O014"
MODEL = "openai/gpt-5.6-sol"
PASSED, FAILED, INCONCLUSIVE, ERROR = 0, 1, 2, 3
PREFIX = "##OBSERVATIONS##"
MUTATION = os.environ.get("O014_INTENTIONAL_MUTATION", "")
MUTATIONS = (
    "omit-delta-omega-V",
    "delete-second-F",
    "reverse-corner",
    "independent-Omega",
    "omit-polar-order",
    "all-plus-noether",
)
ETA = (-1, 1, 1, 1, 1)
PAIRS = tuple(combinations(range(5), 2))


def parity(word: tuple[int, ...]) -> int:
    if len(set(word)) != len(word):
        return 0
    inversions = sum(word[i] > word[j] for i in range(len(word)) for j in range(i + 1, len(word)))
    return -1 if inversions % 2 else 1


@dataclass(frozen=True, order=True)
class Atom:
    family: str
    indices: tuple[int, ...]
    degree: int

    def label(self) -> str:
        suffix = "".join(str(i) for i in self.indices)
        return f"{self.family}{suffix}"


@dataclass(frozen=True)
class Poly:
    """Canonical sparse free graded algebra over exact rationals."""

    terms: tuple[tuple[tuple[Atom, ...], Q], ...] = ()

    @staticmethod
    def scalar(value: int | Q) -> "Poly":
        value = Q(value)
        return Poly((((), value),)) if value else Poly()

    @staticmethod
    def atom(atom: Atom) -> "Poly":
        return Poly((((atom,), Q(1)),))

    @staticmethod
    def collect(items: Iterable[tuple[tuple[Atom, ...], Q]]) -> "Poly":
        out: dict[tuple[Atom, ...], Q] = {}
        for factors0, coefficient0 in items:
            factors = list(factors0)
            coefficient = Q(coefficient0)
            for i in range(len(factors)):
                for j in range(len(factors) - 1 - i):
                    if factors[j] > factors[j + 1]:
                        if factors[j].degree * factors[j + 1].degree % 2:
                            coefficient = -coefficient
                        factors[j], factors[j + 1] = factors[j + 1], factors[j]
            if any(factors[i] == factors[i + 1] and factors[i].degree % 2
                   for i in range(len(factors) - 1)):
                continue
            key = tuple(factors)
            out[key] = out.get(key, Q()) + coefficient
        return Poly(tuple(sorted((m, c) for m, c in out.items() if c)))

    def __add__(self, rhs: "Poly") -> "Poly":
        return Poly.collect(self.terms + rhs.terms)

    def __neg__(self) -> "Poly":
        return Poly(tuple((m, -c) for m, c in self.terms))

    def __sub__(self, rhs: "Poly") -> "Poly":
        return self + -rhs

    def __mul__(self, rhs: "Poly | int | Q") -> "Poly":
        if not isinstance(rhs, Poly):
            rhs = Poly.scalar(rhs)
        return Poly.collect((a + b, ca * cb) for a, ca in self.terms for b, cb in rhs.terms)

    __rmul__ = __mul__

    @property
    def is_zero(self) -> bool:
        return not self.terms

    def coefficient(self, marker: Atom) -> "Poly":
        """Coefficient with marker moved to the left; all terms must be linear."""
        out = Poly()
        for factors, coefficient in self.terms:
            if factors.count(marker) != 1:
                continue
            rest = list(factors)
            position = rest.index(marker)
            rest.pop(position)
            sign = -1 if marker.degree * sum(x.degree for x in rest[:position]) % 2 else 1
            out += Poly(((tuple(rest), coefficient * sign),))
        return out

    def substitute(self, mapping: Mapping[Atom, "Poly | int | Q"]) -> "Poly":
        out = Poly()
        for factors, coefficient in self.terms:
            term = Poly.scalar(coefficient)
            for atom in factors:
                replacement = mapping.get(atom, Poly.atom(atom))
                if not isinstance(replacement, Poly):
                    replacement = Poly.scalar(replacement)
                term *= replacement
            out += term
        return out

    def scalar_value(self) -> Q:
        if self.is_zero:
            return Q()
        if len(self.terms) == 1 and self.terms[0][0] == ():
            return self.terms[0][1]
        raise ValueError(f"not scalar: {self.text()}")

    def text(self) -> str:
        if self.is_zero:
            return "0"
        return "+".join(f"{c}*" + "^".join(a.label() for a in factors)
                        for factors, c in self.terms)


def psum(parts: Iterable[Poly]) -> Poly:
    out = Poly()
    for part in parts:
        out += part
    return out


def A(family: str, *indices: int, degree: int) -> Atom:
    return Atom(family, tuple(indices), degree)


# The graph layer preserves which leaves were differentiated.  It is deliberately
# small: addition, multiplication, scaling, and declared mathematical leaves.
@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()
    leaf: Atom | None = None
    coefficient: Q = Q(1)

    @staticmethod
    def atom(atom: Atom) -> "Expr":
        return Expr("atom", leaf=atom)

    @staticmethod
    def scalar(value: int | Q) -> "Expr":
        return Expr("scalar", coefficient=Q(value))

    def __add__(self, rhs: "Expr") -> "Expr":
        return Expr("add", (self, rhs))

    def __mul__(self, rhs: "Expr | int | Q") -> "Expr":
        if not isinstance(rhs, Expr):
            rhs = Expr.scalar(rhs)
        return Expr("mul", (self, rhs))

    __rmul__ = __mul__

    def __neg__(self) -> "Expr":
        return Expr("scale", (self,), coefficient=Q(-1))

    def __sub__(self, rhs: "Expr") -> "Expr":
        return self + -rhs

    def compile(self) -> Poly:
        if self.op == "atom":
            assert self.leaf is not None
            return Poly.atom(self.leaf)
        if self.op == "scalar":
            return Poly.scalar(self.coefficient)
        if self.op == "add":
            return self.args[0].compile() + self.args[1].compile()
        if self.op == "mul":
            return self.args[0].compile() * self.args[1].compile()
        if self.op == "scale":
            return self.coefficient * self.args[0].compile()
        raise ValueError(self.op)


def esum(parts: Iterable[Expr]) -> Expr:
    out = Expr.scalar(0)
    for part in parts:
        out = out + part
    return out


def E(i: int) -> Expr:
    return Expr.atom(A("E", i, degree=1))


def V(i: int) -> Expr:
    return Expr.atom(A("V", i, degree=0))


def K(i: int) -> Expr:
    return Expr.atom(A("K", i, degree=1))


def P(i: int, j: int) -> Expr:
    return Expr.atom(A("P", i, j, degree=3))


def W(i: int, j: int) -> Expr:
    """Canonical upper antisymmetric connection component."""
    if i == j:
        return Expr.scalar(0)
    return Expr.atom(A("W", min(i, j), max(i, j), degree=1)) * (1 if i < j else -1)


def mixed_w(i: int, j: int) -> Expr:
    return ETA[j] * W(i, j)


def dW(i: int, j: int) -> Expr:
    if i == j:
        return Expr.scalar(0)
    return Expr.atom(A("dW", min(i, j), max(i, j), degree=1)) * (1 if i < j else -1)


def mixed_dw(i: int, j: int) -> Expr:
    return ETA[j] * dW(i, j)


def primitive_graph(independent_omega: bool = False) -> Expr:
    if independent_omega:
        # A genuinely independent reference connection: -(omega-Omega)^AB P_AB.
        # Omega is held fixed for the omega row, as in D023's fixed-reference
        # construction.  This mutation changes the graph, not a downstream row.
        return -esum((W(a, b) - Expr.atom(A("OM", a, b, degree=1))) * P(a, b)
                     for a in range(5) for b in range(5) if a != b)
    return -2 * esum(K(a) * V(b) * P(a, b) for a in range(5) for b in range(5) if a != b)


def delta_leaf(atom: Atom, omit_delta_omega_v: bool = False) -> Expr:
    f, ix = atom.family, atom.indices
    if f == "E":
        return Expr.atom(A("dE", ix[0], degree=1))
    if f == "V":
        return Expr.atom(A("dV", ix[0], degree=0))
    if f == "K":
        a = ix[0]
        connection_part = Expr.scalar(0) if omit_delta_omega_v else esum(
            mixed_dw(a, c) * V(c) for c in range(5)
        )
        return Expr.atom(A("DKdV", a, degree=1)) + connection_part
    if f == "P":
        a, b = ix
        # Direct epsilon/wedge differentiation of P(E), equation (16).
        return Q(1, 4) * esum(
            Expr.scalar(eps) * Expr.atom(A("dE", c, degree=1)) * E(d) * E(e)
            for c in range(5) for d in range(5) for e in range(5)
            if (eps := parity((a, b, c, d, e)))
        )
    if f == "W":
        return Expr.atom(A("dW", *ix, degree=1))
    if f == "OM":
        return Expr.atom(A("dOM", *ix, degree=1))
    return Expr.scalar(0)


def vary_graph(expr: Expr, omit_delta_omega_v: bool = False) -> Expr:
    """Field variation is degree zero in spacetime and obeys Leibniz."""
    if expr.op == "atom":
        assert expr.leaf is not None
        return delta_leaf(expr.leaf, omit_delta_omega_v)
    if expr.op == "scalar":
        return Expr.scalar(0)
    if expr.op == "add":
        return vary_graph(expr.args[0], omit_delta_omega_v) + vary_graph(expr.args[1], omit_delta_omega_v)
    if expr.op == "mul":
        left, right = expr.args
        return vary_graph(left, omit_delta_omega_v) * right + left * vary_graph(right, omit_delta_omega_v)
    if expr.op == "scale":
        return expr.coefficient * vary_graph(expr.args[0], omit_delta_omega_v)
    raise ValueError(expr.op)


def d_leaf(atom: Atom) -> Poly:
    f, ix = atom.family, atom.indices
    if f == "V":
        return Poly.atom(A("K", ix[0], degree=1))
    if f == "P":
        return Poly.atom(A("DP", *ix, degree=4))
    if f == "E":
        return Poly.atom(A("DE", ix[0], degree=2))
    return Poly()


def covariant_d(poly: Poly) -> Poly:
    """Graded D at a normal-frame point; free-index connection terms cancel."""
    out = Poly()
    for factors, coefficient in poly.terms:
        for i, atom in enumerate(factors):
            da = d_leaf(atom)
            if da.is_zero:
                continue
            sign = -1 if sum(x.degree for x in factors[:i]) % 2 else 1
            term = Poly.scalar(coefficient * sign)
            for j, other in enumerate(factors):
                term *= da if i == j else Poly.atom(other)
            out += term
    return out


def integrate_dkdv(raw: Poly, delete_second_f: bool = False,
                    reverse_corner: bool = False) -> tuple[Poly, Poly]:
    """Put the graph variation in explicit IBP normal form.

    For each q_A of degree three,
      integral (D dV^A) q_A = boundary(dV^A q_A) - integral dV^A Dq_A.
    The delete-second-F mutation removes D(V)P from this upstream D(VP)
    product rule, rather than editing a final expected coefficient.
    """
    bulk = Poly()
    boundary = Poly()
    for factors, coefficient0 in raw.terms:
        markers = [x for x in factors if x.family == "DKdV"]
        if not markers:
            bulk += Poly(((factors, coefficient0),))
            continue
        if len(markers) != 1:
            raise ValueError("IBP normal form is nonlinear in D(delta V)")
        marker = markers[0]
        position = factors.index(marker)
        rest_factors = factors[:position] + factors[position + 1:]
        sign = -1 if marker.degree * sum(x.degree for x in factors[:position]) % 2 else 1
        coefficient = coefficient0 * sign
        q = Poly(((rest_factors, Q(1)),))
        dq = covariant_d(q)
        if delete_second_f:
            # Delete exactly the K P contribution generated by D(V P).
            dq = Poly(tuple((m, c) for m, c in dq.terms
                            if not any(x.family == "K" for x in m)))
        dv = Poly.atom(A("dV", marker.indices[0], degree=0))
        bulk += -coefficient * dv * dq
        boundary_sign = -1 if reverse_corner else 1
        boundary += boundary_sign * coefficient * dv * q
    return bulk, boundary


def target_momentum(a: int, b: int) -> Poly:
    """Separate compact D024 target for P_AB: complement, not permutations."""
    if a == b:
        return Poly()
    remaining = tuple(i for i in range(5) if i not in (a, b))
    eps = parity((a, b) + remaining)
    return Q(eps, 2) * psum([Poly.atom(A("E", i, degree=1)) for i in remaining[:1]]) \
        * Poly.atom(A("E", remaining[1], degree=1)) * Poly.atom(A("E", remaining[2], degree=1))


def expand_p(poly: Poly) -> Poly:
    mapping = {A("P", a, b, degree=3): target_momentum(a, b)
               for a in range(5) for b in range(5)}
    return poly.substitute(mapping)


def canonicalize_bivectors(poly: Poly) -> Poly:
    """Encode P_BA=-P_AB and the same relation for DP explicitly."""
    mapping: dict[Atom, Poly] = {}
    for family, degree in (("P", 3), ("DP", 4)):
        for a in range(5):
            for b in range(5):
                source = A(family, a, b, degree=degree)
                if a == b:
                    mapping[source] = Poly()
                else:
                    target = Poly.atom(A(family, min(a, b), max(a, b), degree=degree))
                    mapping[source] = target if a < b else -target
    return poly.substitute(mapping)


def target_delta_p(a: int, b: int) -> Poly:
    return Q(1, 4) * psum(
        Poly.scalar(eps) * Poly.atom(A("dE", c, degree=1))
        * Poly.atom(A("E", d, degree=1)) * Poly.atom(A("E", e, degree=1))
        for c in range(5) for d in range(5) for e in range(5)
        if (eps := parity((a, b, c, d, e)))
    )


def target_rows() -> tuple[dict[tuple[int, int], Poly], dict[int, Poly], dict[int, Poly], dict[int, Poly]]:
    """D024 (18)--(20), encoded independently of graph differentiation."""
    omega: dict[tuple[int, int], Poly] = {}
    for i, j in PAIRS:
        marker = A("dW", i, j, degree=1)
        formula = -2 * psum(
            mixed_dw(a, c).compile() * Poly.atom(A("V", c, degree=0))
            * Poly.atom(A("V", b, degree=0)) * Poly.atom(A("P", a, b, degree=3))
            for a in range(5) for b in range(5) for c in range(5) if a != b
        )
        omega[(i, j)] = formula.coefficient(marker)

    c_ab = {(a, b): Poly.atom(A("K", a, degree=1)) * Poly.atom(A("V", b, degree=0))
            - Poly.atom(A("V", a, degree=0)) * Poly.atom(A("K", b, degree=1))
            for a in range(5) for b in range(5)}
    e_rows = {
        c: Q(1, 4) * psum(
            Poly.scalar(eps) * c_ab[(a, b)] * Poly.atom(A("E", d, degree=1))
            * Poly.atom(A("E", e, degree=1))
            for a in range(5) for b in range(5) for d in range(5) for e in range(5)
            if a != b
            if (eps := parity((a, b, c, d, e)))
        )
        for c in range(5)
    }
    v_rows = {
        a: 2 * psum(
            Poly.atom(A("V", b, degree=0)) * Poly.atom(A("DP", a, b, degree=4))
            + 2 * Poly.atom(A("K", b, degree=1)) * Poly.atom(A("P", a, b, degree=3))
            for b in range(5) if a != b
        )
        for a in range(5)
    }
    corner = {
        a: -2 * psum(Poly.atom(A("V", b, degree=0)) * Poly.atom(A("P", a, b, degree=3))
                     for b in range(5) if a != b)
        for a in range(5)
    }
    return omega, e_rows, v_rows, corner


def rank(matrix: list[list[Q]]) -> int:
    a = [row[:] for row in matrix]
    r = 0
    for c in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def anti(vector: list[Q]) -> list[list[Q]]:
    out = [[Q() for _ in range(5)] for _ in range(5)]
    for value, (a, b) in zip(vector, PAIRS):
        out[a][b], out[b][a] = value, -value
    return out


def projector_assessment(v: list[Q] | None = None, k: list[Q] | None = None) -> dict[str, object]:
    # The default is deliberately Lorentz-boosted: its timelike component makes
    # an omitted lowering operation visible.  The former purely spatial vector
    # is retained below as an additional masking/control case.
    v = v if v is not None else [Q(3, 4), Q(), Q(), Q(), Q(5, 4)]
    k = k if k is not None else [Q(5), Q(1), Q(2), Q(3), Q(3)]
    vl = [ETA[i] * v[i] for i in range(5)]
    h = [[Q(i == j) - v[i] * vl[j] for j in range(5)] for i in range(5)]
    # h stores h^A{}_B.  For lower P_ab the required projector is
    # h_A{}^B = eta_AC h^C{}_D eta^{DB}; eta^{-1}=eta in this basis.
    h_lower_upper = [[ETA[a] * h[a][b] * ETA[b] for b in range(5)] for a in range(5)]
    multiply = lambda x, y: [[sum(x[i][k] * y[k][j] for k in range(5)) for j in range(5)]
                              for i in range(5)]
    omega = anti([Q(i + 1) for i in range(10)])
    addition = [[v[a] * k[b] - k[a] * v[b] for b in range(5)] for a in range(5)]
    induced = [[omega[a][b] + addition[a][b] for b in range(5)] for a in range(5)]

    def double(m: list[list[Q]]) -> list[list[Q]]:
        # Upper bivector projection: (hh m)^{AB}=h^A{}_C h^B{}_D m^{CD}.
        # The order of the second mixed projector matters in a boosted frame.
        return [[sum(h[a][c] * h[b][d] * m[c][d] for c in range(5) for d in range(5))
                 for b in range(5)] for a in range(5)]

    d_omega_v = [k[a] + sum(addition[a][b] * ETA[b] * v[b] for b in range(5)) for a in range(5)]
    retained = [[double(induced)[a][b] - double(omega)[a][b] for b in range(5)] for a in range(5)]
    constraint_columns = []
    parallel_columns = []
    coset_columns = []
    for column in range(10):
        basis = anti([Q(i == column) for i in range(10)])
        contraction = [sum(basis[a][b] * ETA[b] * v[b] for b in range(5)) for a in range(5)]
        projected = [double(basis)[a][b] for a, b in PAIRS]
        constraint_columns.append(contraction + projected)
        parallel_columns.append(projected)
        coset_columns.append([Q(i == column) - projected[i] for i in range(10)])
    rows = lambda columns, n: [[columns[c][r] for c in range(10)] for r in range(n)]
    return {
        "V": v,
        "V2": sum(v[i] * vl[i] for i in range(5)),
        "h2": multiply(h, h) == h,
        "hV": [sum(h[i][j] * v[j] for j in range(5)) for i in range(5)],
        "VK": sum(v[i] * ETA[i] * k[i] for i in range(5)),
        "D_Omega_V": d_omega_v,
        "retained": all(x == 0 for row in retained for x in row),
        "uniqueness_rank": rank(rows(constraint_columns, 15)),
        "parallel_rank": rank(rows(parallel_columns, 10)),
        "coset_rank": rank(rows(coset_columns, 10)),
        "h_upper_lower": h,
        "h_lower_upper": h_lower_upper,
    }


def row_matrix(rows: dict[tuple[int, int], Poly], v: list[Q]) -> list[list[Q]]:
    """Rows in delta-omega pair order, columns in generic P pair order."""
    matrix: list[list[Q]] = []
    for pair in PAIRS:
        row: list[Q] = []
        for p_pair in PAIRS:
            mapping: dict[Atom, Poly | Q] = {}
            for i in range(5):
                mapping[A("V", i, degree=0)] = v[i]
            for a in range(5):
                for b in range(5):
                    value = Q(1) if (a, b) == p_pair else Q(-1) if (b, a) == p_pair else Q()
                    mapping[A("P", a, b, degree=3)] = value
            row.append(rows[pair].substitute(mapping).scalar_value())
        matrix.append(row)
    return matrix


def independent_d004_matrix() -> list[list[Q]]:
    """Ordered D004 sum delta omega^AB P_AB, assembled without graph rows."""
    out = [[Q() for _ in PAIRS] for _ in PAIRS]
    for r, wpair in enumerate(PAIRS):
        for c, ppair in enumerate(PAIRS):
            total = Q()
            for a in range(5):
                for b in range(5):
                    ws = Q(1) if (a, b) == wpair else Q(-1) if (b, a) == wpair else Q()
                    ps = Q(1) if (a, b) == ppair else Q(-1) if (b, a) == ppair else Q()
                    total += ws * ps
            out[r][c] = total
    return out


def independent_hhp_matrix(h_lower_upper: list[list[Q]]) -> list[list[Q]]:
    """2 h_i{}^a h_j{}^b P_ab for lower P and upper delta-omega."""
    out = [[Q() for _ in PAIRS] for _ in PAIRS]
    for r, (i, j) in enumerate(PAIRS):
        for c, ppair in enumerate(PAIRS):
            p = anti([Q(k == c) for k in range(10)])
            hp = sum(h_lower_upper[i][a] * h_lower_upper[j][b] * p[a][b]
                     for a in range(5) for b in range(5))
            out[r][c] = 2 * hp  # both ordered D004 pair contributions
    return out


def old_unlowered_hhp_matrix(h_upper_lower: list[list[Q]]) -> list[list[Q]]:
    """Historical defective assembly, retained solely as a negative law test."""
    out = [[Q() for _ in PAIRS] for _ in PAIRS]
    for r, (i, j) in enumerate(PAIRS):
        for c, _ in enumerate(PAIRS):
            p = anti([Q(k == c) for k in range(10)])
            hp = sum(h_upper_lower[i][a] * h_upper_lower[b][j] * p[a][b]
                     for a in range(5) for b in range(5))
            out[r][c] = 2 * hp
    return out


def add_matrix(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [[x + y for x, y in zip(rx, ry)] for rx, ry in zip(a, b)]


def noether_polynomial(omega_rows: dict[tuple[int, int], Poly], e_rows: dict[int, Poly],
                       v_rows: dict[int, Poly], all_plus: bool = False) -> tuple[Poly, Poly, Poly, Poly]:
    """Assemble all three Noether rows independently with one antisymmetric alpha."""
    alpha = {(i, j): Poly.atom(A("alpha", i, j, degree=0)) for i, j in PAIRS}

    d_bomega = psum(alpha[pair] * covariant_d(omega_rows[pair]) for pair in PAIRS)

    def alpha_mixed(a: int, b: int) -> Poly:
        if a == b:
            return Poly()
        pair = (min(a, b), max(a, b))
        sign = 1 if a < b else -1
        return ETA[b] * sign * alpha[pair]

    # These are substitutions into independently extracted Euler rows.  The
    # coframe expression is naturally (alpha E) wedge B_E; moving B_E left
    # supplies the compulsory minus in the diamond notation.
    coframe_direct = psum(
        alpha_mixed(a, b) * Poly.atom(A("E", b, degree=1)) * e_rows[a]
        for a in range(5) for b in range(5)
    )
    if all_plus:
        # Upstream grading mutation: incorrectly commute the 1-form alpha E
        # through the 3-form Euler coefficient with a plus sign.
        coframe_direct = psum(
            e_rows[a] * alpha_mixed(a, b) * Poly.atom(A("E", b, degree=1))
            for a in range(5) for b in range(5)
        )
    v_direct = psum(v_rows[a] * alpha_mixed(a, b) * Poly.atom(A("V", b, degree=0))
                    for a in range(5) for b in range(5))
    # P is not an unconstrained bivector: impose its explicit epsilon/coframe
    # construction, and DP=D[P(E)], only after the three rows were assembled.
    physical: dict[Atom, Poly] = {}
    for a in range(5):
        for b in range(5):
            momentum = target_momentum(a, b)
            physical[A("P", a, b, degree=3)] = momentum
            physical[A("DP", a, b, degree=4)] = covariant_d(momentum)
    d_bomega = d_bomega.substitute(physical)
    coframe_direct = coframe_direct.substitute(physical)
    v_direct = v_direct.substitute(physical)
    return d_bomega + coframe_direct + v_direct, d_bomega, coframe_direct, v_direct


def polar_specialization(graph: Expr, bulk: Poly, boundary: Poly,
                         omit_order: bool = False) -> dict[str, object]:
    """Concrete exact support configuration, derived from coframe and epsilon.

    We choose c=2 (rather than a unit placeholder) so sign and multiplicity
    mistakes remain visible.  kappa_5^{-1} is an overall omitted unit.
    """
    c = Q(2)
    x = [Poly.atom(A("x", i, degree=1)) for i in range(3)]
    theta = Poly.atom(A("theta", degree=1))
    zero = Poly()
    coframe = {A("E", i, degree=1): (x[i] if i < 3 else zero) for i in range(5)}
    vector = {A("V", i, degree=0): Q(i == 4) for i in range(5)}
    omega_upper: dict[tuple[int, int], Poly] = {
        (a, b): zero for a in range(5) for b in range(5)
    }
    omega_upper[(4, 3)] = c * theta
    omega_upper[(3, 4)] = -c * theta
    # K^A=omega^A_B V^B is derived from the displayed connection and V=e4.
    k_components = {
        a: psum(ETA[b] * omega_upper[(a, b)] * Q(b == 4) for b in range(5))
        for a in range(5)
    }
    kvals = {A("K", i, degree=1): k_components[i] for i in range(5)}
    connection_values = {
        A("W", a, b, degree=1): omega_upper[(a, b)] for a, b in PAIRS
    }
    independent_values = {
        A("OM", a, b, degree=1): zero for a in range(5) for b in range(5) if a != b
    }

    # Derive P from the explicit support coframe using epsilon, and optionally
    # remove one ordered pair before the action contraction.
    pvals: dict[Atom, Poly] = {}
    for a in range(5):
        for b in range(5):
            pvals[A("P", a, b, degree=3)] = target_momentum(a, b).substitute(coframe)
    if omit_order:
        pvals[A("P", 3, 4, degree=3)] = zero

    mapping: dict[Atom, Poly | Q] = {}
    mapping.update(coframe)
    mapping.update(vector)
    mapping.update(kvals)
    mapping.update(connection_values)
    mapping.update(independent_values)
    mapping.update(pvals)
    orientation = x[0] * x[1] * x[2] * theta
    action = graph.compile().substitute(mapping)
    action_coefficient = None
    if len(action.terms) == 1 and len(orientation.terms) == 1 and action.terms[0][0] == orientation.terms[0][0]:
        action_coefficient = action.terms[0][1] / orientation.terms[0][1]

    # Connection row from the graph variation, with delta omega^{43}=dchi*dtheta.
    dchi = Poly.atom(A("dchi", degree=0))
    connection_mapping = dict(mapping)
    for pair in PAIRS:
        connection_mapping[A("dW", *pair, degree=1)] = zero
    connection_mapping[A("dW", 3, 4, degree=1)] = -dchi * theta  # d omega^{43}
    connection_mapping.update({A("dV", i, degree=0): zero for i in range(5)})
    connection_mapping.update({A("dE", i, degree=1): zero for i in range(5)})
    primitive_connection = bulk.substitute(connection_mapping)

    # D004 is independently the ordered sum delta omega^AB P_AB.
    d004_connection = Poly()
    for a in range(5):
        for b in range(5):
            if a == b:
                continue
            dwab = (-dchi * theta if (a, b) == (3, 4)
                    else dchi * theta if (a, b) == (4, 3) else zero)
            d004_connection += dwab * pvals[A("P", a, b, degree=3)]

    # Free common coframe rescaling is substituted into the graph-derived row.
    alpha = Poly.atom(A("scale", degree=0))
    coframe_mapping = dict(mapping)
    coframe_mapping.update({A("dW", *pair, degree=1): zero for pair in PAIRS})
    coframe_mapping.update({A("dV", i, degree=0): zero for i in range(5)})
    coframe_mapping.update({A("dE", i, degree=1): (alpha * x[i] if i < 3 else zero)
                            for i in range(5)})
    coframe_variation = bulk.substitute(coframe_mapping)

    # F is extracted from the same IBP graph.  DP=0 on constant polar support.
    v_coefficients = {i: bulk.coefficient(A("dV", i, degree=0)) for i in range(5)}
    f_mapping = dict(mapping)
    f_mapping.update({A("DP", a, b, degree=4): zero for a in range(5) for b in range(5)})
    f_values = [v_coefficients[i].substitute(f_mapping) for i in range(5)]
    transverse = f_values[:4]

    # Pull back the graph-derived corner form to a boundary support with only
    # x0,x1 horizontal directions; x2 is killed, theta remains.
    pullback = dict(mapping)
    pullback[A("x", 2, degree=1)] = zero
    pullback.update({A("dV", i, degree=0): Poly.atom(A("corner_dV", i, degree=0))
                     for i in range(5)})
    corner_pb = boundary.substitute(pullback).substitute({A("x", 2, degree=1): zero})

    return {
        "c": c,
        "P43": pvals[A("P", 4, 3, degree=3)],
        "P34": pvals[A("P", 3, 4, degree=3)],
        "action": action,
        "action_coefficient": action_coefficient,
        "d004_connection": d004_connection,
        "primitive_connection": primitive_connection,
        "connection_residual": d004_connection + primitive_connection,
        "coframe_variation": coframe_variation,
        "transverse": transverse,
        "longitudinal": f_values[4],
        "corner_pullback": corner_pb,
        "orientation": orientation,
        "dchi": dchi,
        "alpha": alpha,
    }


@dataclass
class Recorder:
    results: dict[str, bool] = field(default_factory=dict)

    def require(self, name: str, condition: bool) -> None:
        if name in self.results or type(condition) is not bool:
            raise ValueError(name)
        self.results[name] = condition

    @property
    def failed(self) -> list[str]:
        return sorted(name for name, passed in self.results.items() if not passed)


def evaluate(mutation: str) -> tuple[Recorder, dict[str, object]]:
    if mutation and mutation not in MUTATIONS:
        raise ValueError(f"unsupported mutation: {mutation}")
    rec = Recorder()

    pd = projector_assessment()
    rec.require("projector.V2_one", pd["V2"] == 1)
    rec.require("projector.h2_h", bool(pd["h2"]))
    rec.require("projector.hV_zero", pd["hV"] == [Q()] * 5)
    rec.require("projector.VK_zero", pd["VK"] == 0)
    rec.require("connection.D_Omega_V_zero", pd["D_Omega_V"] == [Q()] * 5)
    rec.require("connection.retained_stabilizer_block", bool(pd["retained"]))
    rec.require("connection.uniqueness_both_conditions", pd["uniqueness_rank"] == 10)
    rec.require("rows.four_coset", pd["coset_rank"] == 4)
    rec.require("rows.six_stabilizer", pd["parallel_rank"] == 6)

    independent = mutation == "independent-Omega"
    graph = primitive_graph(independent_omega=independent)
    raw = vary_graph(graph, omit_delta_omega_v=(mutation == "omit-delta-omega-V")).compile()
    bulk, boundary = integrate_dkdv(
        raw,
        delete_second_f=(mutation == "delete-second-F"),
        reverse_corner=(mutation == "reverse-corner"),
    )
    bulk = canonicalize_bivectors(bulk)
    boundary = canonicalize_bivectors(boundary)

    omega_target, e_target, v_target, corner_target = target_rows()
    omega_target = {pair: canonicalize_bivectors(row) for pair, row in omega_target.items()}
    v_target = {i: canonicalize_bivectors(row) for i, row in v_target.items()}
    corner_target = {i: canonicalize_bivectors(row) for i, row in corner_target.items()}
    omega_rows = {pair: bulk.coefficient(A("dW", *pair, degree=1)) for pair in PAIRS}
    e_rows = {i: bulk.coefficient(A("dE", i, degree=1)) for i in range(5)}
    v_rows = {i: bulk.coefficient(A("dV", i, degree=0)) for i in range(5)}
    corner_rows = {i: boundary.coefficient(A("dV", i, degree=0)) for i in range(5)}

    # Meaningful delta-P regression: compare the graph leaf rule to a separately
    # enumerated epsilon/wedge target for every ordered component.
    delta_p_ok = True
    for a in range(5):
        for b in range(5):
            delta_p_ok &= delta_leaf(A("P", a, b, degree=3)).compile() == target_delta_p(a, b)
    rec.require("variation.deltaP_epsilon_wedge_all_ordered", bool(delta_p_ok))
    rec.require("variation.omega_row_from_graph", omega_rows == omega_target)
    rec.require("variation.E_row_J_from_graph", e_rows == e_target)
    rec.require("variation.V_row_F_from_IBP", v_rows == v_target)
    rec.require("variation.corner_minus_from_IBP", corner_rows == corner_target)
    rec.require("variation.raw_and_IBP_nontrivial", not raw.is_zero and not bulk.is_zero and not boundary.is_zero)

    # Generic row bridge: D004 and primitive matrices are assembled separately.
    primitive_matrix = row_matrix(omega_rows, pd["V"])
    d004_matrix = independent_d004_matrix()
    residual_matrix = add_matrix(d004_matrix, primitive_matrix)
    hhp_matrix = independent_hhp_matrix(pd["h_lower_upper"])
    old_hhp_matrix = old_unlowered_hhp_matrix(pd["h_upper_lower"])
    row01 = PAIRS.index((0, 1))
    col01 = PAIRS.index((0, 1))
    col14 = PAIRS.index((1, 4))
    rec.require("rows.generic_residual_equals_double_projected_hhP", residual_matrix == hhp_matrix)
    rec.require("rows.generic_residual_not_inserted_parallel_map", residual_matrix != d004_matrix and any(
        value for row in residual_matrix for value in row))
    rec.require("rows.residual_rank_six", rank(residual_matrix) == 6)
    rec.require("rows.primitive_rank_four", rank(primitive_matrix) == 4)
    rec.require("rows.boosted_01_P01_coefficient_25_over_8", residual_matrix[row01][col01] == Q(25, 8))
    rec.require("rows.boosted_01_P14_coefficient_minus_15_over_8", residual_matrix[row01][col14] == Q(-15, 8))
    rec.require("rows.old_unlowered_01_has_wrong_plus_sign", old_hhp_matrix[row01][col14] == Q(15, 8))
    rec.require("rows.old_unlowered_assembly_differs", old_hhp_matrix != hhp_matrix)

    # The previous spatial representative is retained as a control showing why
    # it could not discriminate the lowering defect: there the two assemblies
    # coincide even though only the explicitly lowered one is generally valid.
    spatial_pd = projector_assessment(
        [Q(), Q(3, 5), Q(), Q(), Q(4, 5)],
        [Q(1), Q(4), Q(2), Q(3), Q(-3)],
    )
    spatial_correct = independent_hhp_matrix(spatial_pd["h_lower_upper"])
    spatial_old = old_unlowered_hhp_matrix(spatial_pd["h_upper_lower"])
    rec.require("rows.spatial_masking_control_old_equals_lowered", spatial_old == spatial_correct)

    noether, nbw, ne, nv = noether_polynomial(
        omega_rows, e_rows, v_rows, all_plus=(mutation == "all-plus-noether")
    )
    correct_noether, _, correct_e, _ = noether_polynomial(omega_target, e_target, v_target, all_plus=False)
    all_plus_noether, _, all_plus_e, _ = noether_polynomial(omega_target, e_target, v_target, all_plus=True)
    rec.require("noether.three_rows_independently_nonzero", not nbw.is_zero and not ne.is_zero and not nv.is_zero)
    rec.require("noether.corrected_graded_identity", noether.is_zero)
    rec.require("noether.target_corrected_zero", correct_noether.is_zero)
    rec.require("noether.all_plus_generic_nonzero", not all_plus_noether.is_zero and all_plus_e != correct_e)

    polar = polar_specialization(graph, bulk, boundary, omit_order=(mutation == "omit-polar-order"))
    orientation = polar["orientation"]
    # P is a horizontal 3-form, so compare before appending theta.
    osigma = Poly.atom(A("x", 0, degree=1)) * Poly.atom(A("x", 1, degree=1)) * Poly.atom(A("x", 2, degree=1))
    rec.require("polar.P43_from_epsilon_coframe", polar["P43"] == Q(-1, 2) * osigma)
    rec.require("polar.P34_from_epsilon_coframe", polar["P34"] == Q(1, 2) * osigma)
    rec.require("polar.action_from_ordered_graph", polar["action"] == -polar["c"] * orientation)
    rec.require("polar.ordered_action_ratio_minus_one", polar["action_coefficient"] == -polar["c"])
    rec.require("polar.D004_row_nonzero", not polar["d004_connection"].is_zero)
    rec.require("polar.primitive_row_nonzero", not polar["primitive_connection"].is_zero)
    rec.require("polar.delta_chi43_cancellation", polar["connection_residual"].is_zero)
    expected_coframe = -3 * polar["c"] * polar["alpha"] * orientation
    rec.require("polar.coframe_residual_minus_3c", polar["coframe_variation"] == expected_coframe)
    rec.require("polar.positive_c_excluded", not polar["coframe_variation"].is_zero)
    rec.require("polar.transverse_V_derived_zero", all(x.is_zero for x in polar["transverse"]))
    rec.require("polar.longitudinal_V_nonzero_control", not polar["longitudinal"].is_zero)
    rec.require("polar.basic_corner_pullback_derived_zero", polar["corner_pullback"].is_zero)

    details = {
        "mutation": mutation or None,
        "expression_graph": {
            "root": "B=-2*K^A*V^B*P_AB(E)" if not independent else "B=-(omega-Omega_ind)^AB*P_AB(E)",
            "raw_variation_terms": len(raw.terms),
            "ibp_bulk_terms": len(bulk.terms),
            "ibp_boundary_terms": len(boundary.terms),
        },
        "projector": {
            "V": [str(x) for x in pd["V"]],
            "V2": str(pd["V2"]),
            "VK": str(pd["VK"]),
            "uniqueness_rank": pd["uniqueness_rank"],
            "coset_rank": pd["coset_rank"],
            "stabilizer_rank": pd["parallel_rank"],
            "h_upper_lower": [[str(x) for x in row] for row in pd["h_upper_lower"]],
            "h_lower_upper": [[str(x) for x in row] for row in pd["h_lower_upper"]],
        },
        "derived_vs_expected": {
            "expected_omega": "-2*delta_omega^A_C*V^C*V^B*P_AB",
            "expected_E": "delta_E^C*(epsilon_ABCDE/4)*C^AB*E^D*E^E",
            "expected_V": "2*delta_V^A*(V^B*DP_AB+2*K^B*P_AB)",
            "expected_corner": "-2*delta_V^A*V^B*P_AB",
            "omega_rows_equal": omega_rows == omega_target,
            "E_rows_equal": e_rows == e_target,
            "V_rows_equal": v_rows == v_target,
            "corner_rows_equal": corner_rows == corner_target,
            "generic_residual_rank": rank(residual_matrix),
            "expected_hhP_rank": rank(hhp_matrix),
            "boosted_01_correct": {
                "P01": str(residual_matrix[row01][col01]),
                "P14": str(residual_matrix[row01][col14]),
                "formula": "(25/8) P01-(15/8) P14",
            },
            "boosted_01_old_unlowered": {
                "P01": str(old_hhp_matrix[row01][col01]),
                "P14": str(old_hhp_matrix[row01][col14]),
                "formula": "(25/8) P01+(15/8) P14",
            },
            "old_unlowered_differs": old_hhp_matrix != hhp_matrix,
            "spatial_masking_control_equal": spatial_old == spatial_correct,
        },
        "noether": {
            "D_Bomega_terms": len(nbw.terms),
            "minus_BE_diamond_E_terms": len(ne.terms),
            "BV_diamond_V_terms": len(nv.terms),
            "corrected_residual_terms": len(noether.terms),
            "all_plus_residual_terms": len(all_plus_noether.terms),
            "all_plus_witness": Poly((all_plus_noether.terms[:1])).text(),
        },
        "polar_exact_support": {
            "c": str(polar["c"]),
            "P43": polar["P43"].text(),
            "P34": polar["P34"].text(),
            "B_coefficient_before_circle_integration": str(polar["action_coefficient"]),
            "B_over_c": str(polar["action_coefficient"] / polar["c"] if polar["action_coefficient"] is not None else "undefined"),
            "connection_residual": polar["connection_residual"].text(),
            "coframe_residual": polar["coframe_variation"].text(),
            "transverse_V": [x.text() for x in polar["transverse"]],
            "longitudinal_V": polar["longitudinal"].text(),
            "corner_pullback": polar["corner_pullback"].text(),
            "ordinary_circle_result": "B=-(tau*c/kappa5)*oSigma; coframe=-(3*tau*c/kappa5)*alpha*oSigma",
        },
        "limitations": [
            "finite exact local algebra only", "frozen D005 Euler rows assumed zero on shell",
            "no tangent-admissibility decision", "no global holonomy or total mixed moment map",
            "no action-class completeness", "no functional preservation or C002/C003",
            "correlated OpenAI evidence, not independent verification",
        ],
    }
    return rec, details


def emit(payload: dict[str, object]) -> None:
    print(PREFIX + " " + json.dumps(payload, sort_keys=True, allow_nan=False, default=str))


def check() -> int:
    rec, details = evaluate(MUTATION)
    mutation_runs: dict[str, object] = {}
    if not MUTATION:
        for mutation in MUTATIONS:
            env = dict(os.environ)
            env["O014_INTENTIONAL_MUTATION"] = mutation
            process = subprocess.run(
                [sys.executable, str(Path(__file__).resolve())], env=env,
                capture_output=True, text=True, check=False,
            )
            mutation_runs[mutation] = {
                "exit_code": process.returncode,
                "detected": process.returncode == FAILED,
            }
            rec.require(f"mutation_process.{mutation}.exits_1", process.returncode == FAILED)

    failed = rec.failed
    emit({
        "obligation_id": OID,
        "producer_model": MODEL,
        "infrastructure_producer_models": [MODEL],
        "representation_and_trust": {
            "domain": "finite SO(1,4) tensors, antisymmetric ordered pairs, spacetime exterior forms, first field variation",
            "operations": "epsilon/wedge momentum, graph Leibniz variation, graded covariant D, explicit IBP, projector matrices",
            "coefficient_ring": "fractions.Fraction (Q)",
            "normal_form": "sorted sparse graded monomials; exact equality decidable",
            "assumptions": "eta=(-++++), epsilon01234=+1, V^2=1, ordered pairs, fiber-right positive incidence",
            "CAS_trusted": False,
            "custom_kernel_scope": "claim-local minimal Poly/Expr primitives",
            "existing_substrate_adequate": True,
            "custom_infrastructure_risk": "no reusable infrastructure introduced",
            "cross_checks": "separate D024 targets, explicitly lowered boosted D004/hhP matrices, historical unlowered negative law, concrete c=2 polar support, six upstream mutations",
            "floating_point": False,
            "random_sampling": False,
        },
        "details": details,
        "mutation_processes": mutation_runs,
        "assertions": {
            "total": len(rec.results),
            "passed": len(rec.results) - len(failed),
            "failed": len(failed),
            "failed_names": failed,
        },
    })
    if failed:
        for name in failed:
            print("FAILED: " + name, file=sys.stderr)
        return FAILED
    return PASSED


def main() -> int:
    try:
        return check()
    except (KeyError, ValueError, AssertionError) as exc:
        emit({"obligation_id": OID, "producer_model": MODEL, "inconclusive_reason": str(exc)})
        return INCONCLUSIVE
    except Exception as exc:  # noqa: BLE001
        print(f"{OID} execution error: {exc!r}", file=sys.stderr)
        return ERROR


if __name__ == "__main__":
    raise SystemExit(main())
