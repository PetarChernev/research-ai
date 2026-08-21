#!/usr/bin/env python3
"""Executable implementation of machine-check obligation O001.

Run this only through the deterministic wrapper:

    uv run --locked python scripts/run_check.py O001

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

from dataclasses import dataclass
from fractions import Fraction
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


OBLIGATION_ID = "O001"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]

# Reusable research-specific machinery belongs in research/computation/.
# Import it only if this obligation actually depends on it, and declare the
# dependency in spec.yaml under implementation.infrastructure:
#
# sys.path.insert(0, str(PROJECT_ROOT / "research" / "computation"))

PASSED = 0
FAILED = 1
INCONCLUSIVE = 2
ERROR = 3

OBSERVATION_PREFIX = "##OBSERVATIONS##"

PRODUCER_MODEL = "openai/gpt-5.6-sol"
INTERNAL_MUTATION = os.environ.get("O001_INTERNAL_MUTATION", "")
SUPPORTED_INTERNAL_MUTATIONS = {"", "wedge-sign"}


class MissingBranchTagError(ValueError):
    """A branch outside the declared two-row table was requested."""


class MissingCoefficientTagError(ValueError):
    """A coefficient atom has no declared pullback semantics."""


class GaugeInverseUnavailableError(ValueError):
    """The declared gauge map has no certified exact inverse."""


def _as_fraction(value: int | Fraction) -> Fraction:
    if isinstance(value, bool):
        return Fraction(int(value))
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(f"exact coefficients must be int or Fraction, got {type(value).__name__}")


class Poly:
    """Tiny exact sparse polynomial over Fraction with sorted atom monomials."""

    __slots__ = ("_terms",)

    def __init__(self, terms: Mapping[tuple[str, ...], int | Fraction] | None = None):
        collected: dict[tuple[str, ...], Fraction] = {}
        for monomial, coefficient in (terms or {}).items():
            if not isinstance(monomial, tuple) or any(
                not isinstance(atom, str) or not atom for atom in monomial
            ):
                raise TypeError("polynomial monomials must be tuples of nonempty atom names")
            canonical = tuple(sorted(monomial))
            exact = _as_fraction(coefficient)
            if exact:
                collected[canonical] = collected.get(canonical, Fraction(0)) + exact
        self._terms = tuple(
            sorted((monomial, coefficient) for monomial, coefficient in collected.items() if coefficient)
        )

    @classmethod
    def zero(cls) -> Poly:
        return cls()

    @classmethod
    def one(cls) -> Poly:
        return cls({(): 1})

    @classmethod
    def exact(cls, value: int | Fraction) -> Poly:
        coefficient = _as_fraction(value)
        return cls({(): coefficient}) if coefficient else cls.zero()

    @classmethod
    def atom(cls, name: str) -> Poly:
        if not isinstance(name, str) or not name:
            raise TypeError("atom name must be a nonempty string")
        return cls({(name,): 1})

    @property
    def terms(self) -> tuple[tuple[tuple[str, ...], Fraction], ...]:
        return self._terms

    @property
    def atoms(self) -> frozenset[str]:
        return frozenset(atom for monomial, _ in self._terms for atom in monomial)

    def is_zero(self) -> bool:
        return not self._terms

    @staticmethod
    def _coerce(value: Poly | int | Fraction) -> Poly:
        return value if isinstance(value, Poly) else Poly.exact(value)

    def __add__(self, other: Poly | int | Fraction) -> Poly:
        rhs = self._coerce(other)
        collected = dict(self._terms)
        for monomial, coefficient in rhs._terms:
            collected[monomial] = collected.get(monomial, Fraction(0)) + coefficient
        return Poly(collected)

    def __radd__(self, other: Poly | int | Fraction) -> Poly:
        return self + other

    def __neg__(self) -> Poly:
        return Poly({monomial: -coefficient for monomial, coefficient in self._terms})

    def __sub__(self, other: Poly | int | Fraction) -> Poly:
        return self + (-self._coerce(other))

    def __rsub__(self, other: Poly | int | Fraction) -> Poly:
        return self._coerce(other) - self

    def __mul__(self, other: Poly | int | Fraction) -> Poly:
        rhs = self._coerce(other)
        collected: dict[tuple[str, ...], Fraction] = {}
        for left_monomial, left_coefficient in self._terms:
            for right_monomial, right_coefficient in rhs._terms:
                monomial = tuple(sorted(left_monomial + right_monomial))
                collected[monomial] = (
                    collected.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(collected)

    def __rmul__(self, other: Poly | int | Fraction) -> Poly:
        return self * other

    def derivative(self, atom: str) -> Poly:
        collected: dict[tuple[str, ...], Fraction] = {}
        for monomial, coefficient in self._terms:
            multiplicity = monomial.count(atom)
            if not multiplicity:
                continue
            reduced = list(monomial)
            reduced.remove(atom)
            key = tuple(reduced)
            collected[key] = collected.get(key, Fraction(0)) + coefficient * multiplicity
        return Poly(collected)

    def rename_or_zero(self, substitutions: Mapping[str, str | None]) -> Poly:
        collected: dict[tuple[str, ...], Fraction] = {}
        for monomial, coefficient in self._terms:
            renamed: list[str] = []
            vanishes = False
            for atom in monomial:
                replacement = substitutions.get(atom, atom)
                if replacement is None:
                    vanishes = True
                    break
                renamed.append(replacement)
            if not vanishes:
                key = tuple(sorted(renamed))
                collected[key] = collected.get(key, Fraction(0)) + coefficient
        return Poly(collected)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Poly) and self._terms == other._terms

    def __str__(self) -> str:
        if not self._terms:
            return "0"
        pieces: list[str] = []
        for monomial, coefficient in self._terms:
            atom_text = "*".join(monomial)
            magnitude = abs(coefficient)
            if monomial and magnitude == 1:
                body = atom_text
            elif monomial:
                body = f"{magnitude}*{atom_text}"
            else:
                body = str(magnitude)
            if not pieces:
                pieces.append(("-" if coefficient < 0 else "") + body)
            else:
                pieces.append((" - " if coefficient < 0 else " + ") + body)
        return "".join(pieces)


@dataclass(frozen=True)
class ExteriorAlgebra:
    name: str
    basis: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(set(self.basis)) != len(self.basis):
            raise ValueError(f"{self.name}: duplicate exterior basis name")

    @property
    def order(self) -> dict[str, int]:
        return {name: index for index, name in enumerate(self.basis)}


SOURCE = ExteriorAlgebra("M", ("du0", "du1", "du2", "ds", "dtheta"))
BRANCH = ExteriorAlgebra(
    "kernel-pair", ("du0", "du1", "du2", "ds", "dtheta1", "dtheta2")
)


class Form:
    """Sparse exterior form in a declared algebra and exact canonical order."""

    __slots__ = ("algebra", "_terms")

    def __init__(
        self,
        algebra: ExteriorAlgebra,
        terms: Mapping[tuple[str, ...], Poly | int | Fraction] | None = None,
    ):
        order = algebra.order
        collected: dict[tuple[str, ...], Poly] = {}
        for legs, coefficient in (terms or {}).items():
            if not isinstance(legs, tuple) or any(leg not in order for leg in legs):
                raise ValueError(f"{algebra.name}: invalid exterior monomial {legs!r}")
            if len(set(legs)) != len(legs):
                raise ValueError("canonical form construction cannot contain a repeated leg")
            if tuple(sorted(legs, key=order.__getitem__)) != legs:
                raise ValueError(f"{algebra.name}: exterior monomial is not canonically ordered: {legs}")
            exact = coefficient if isinstance(coefficient, Poly) else Poly.exact(coefficient)
            if not exact.is_zero():
                collected[legs] = collected.get(legs, Poly.zero()) + exact
        self.algebra = algebra
        self._terms = tuple(
            sorted(
                ((legs, coefficient) for legs, coefficient in collected.items() if not coefficient.is_zero()),
                key=lambda item: tuple(order[leg] for leg in item[0]),
            )
        )

    @classmethod
    def zero(cls, algebra: ExteriorAlgebra) -> Form:
        return cls(algebra)

    @classmethod
    def one(cls, algebra: ExteriorAlgebra) -> Form:
        return cls(algebra, {(): 1})

    @classmethod
    def basis_form(cls, algebra: ExteriorAlgebra, name: str) -> Form:
        if name not in algebra.basis:
            raise ValueError(f"{name!r} is not in the {algebra.name} basis")
        return cls(algebra, {(name,): 1})

    @property
    def terms(self) -> tuple[tuple[tuple[str, ...], Poly], ...]:
        return self._terms

    def is_zero(self) -> bool:
        return not self._terms

    def _require_same_algebra(self, other: Form) -> None:
        if self.algebra != other.algebra:
            raise ValueError(
                f"exterior algebra mismatch: {self.algebra.name} versus {other.algebra.name}"
            )

    def __add__(self, other: Form) -> Form:
        self._require_same_algebra(other)
        collected = dict(self._terms)
        for legs, coefficient in other._terms:
            collected[legs] = collected.get(legs, Poly.zero()) + coefficient
        return Form(self.algebra, collected)

    def __neg__(self) -> Form:
        return Form(self.algebra, {legs: -coefficient for legs, coefficient in self._terms})

    def __sub__(self, other: Form) -> Form:
        return self + (-other)

    def scale(self, coefficient: Poly | int | Fraction) -> Form:
        exact = coefficient if isinstance(coefficient, Poly) else Poly.exact(coefficient)
        return Form(
            self.algebra,
            {legs: exact * value for legs, value in self._terms},
        )

    def wedge(self, other: Form) -> Form:
        self._require_same_algebra(other)
        order = self.algebra.order
        collected: dict[tuple[str, ...], Poly] = {}
        for left_legs, left_coefficient in self._terms:
            for right_legs, right_coefficient in other._terms:
                if set(left_legs).intersection(right_legs):
                    continue
                inversions = sum(
                    order[left] > order[right] for left in left_legs for right in right_legs
                )
                sign = -1 if inversions % 2 else 1
                if (
                    INTERNAL_MUTATION == "wedge-sign"
                    and left_legs == ("ds",)
                    and right_legs == ("du1",)
                ):
                    sign = -sign
                legs = tuple(sorted(left_legs + right_legs, key=order.__getitem__))
                coefficient = left_coefficient * right_coefficient * sign
                collected[legs] = collected.get(legs, Poly.zero()) + coefficient
        return Form(self.algebra, collected)

    def contract(self, vector_name: str) -> Form:
        if vector_name not in self.algebra.basis:
            raise ValueError(f"unknown coordinate vector {vector_name!r}")
        collected: dict[tuple[str, ...], Poly] = {}
        for legs, coefficient in self._terms:
            if vector_name not in legs:
                continue
            position = legs.index(vector_name)
            reduced = legs[:position] + legs[position + 1 :]
            value = coefficient * (-1 if position % 2 else 1)
            collected[reduced] = collected.get(reduced, Poly.zero()) + value
        return Form(self.algebra, collected)

    def rename_coefficients(self, substitutions: Mapping[str, str | None]) -> Form:
        return Form(
            self.algebra,
            {
                legs: coefficient.rename_or_zero(substitutions)
                for legs, coefficient in self._terms
            },
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Form)
            and self.algebra == other.algebra
            and self._terms == other._terms
        )

    def as_data(self) -> dict[str, str]:
        return {
            ("1" if not legs else "^".join(legs)): str(coefficient)
            for legs, coefficient in self._terms
        }

    def __str__(self) -> str:
        return json.dumps(self.as_data(), sort_keys=True, separators=(",", ":"))


RHO = Poly.atom("rho")
DRHO = Poly.atom("drho")
CHI = Poly.atom("chi")
THETA = Poly.atom("theta")

DU0 = Form.basis_form(SOURCE, "du0")
DU1 = Form.basis_form(SOURCE, "du1")
DU2 = Form.basis_form(SOURCE, "du2")
DS = Form.basis_form(SOURCE, "ds")
DTHETA = Form.basis_form(SOURCE, "dtheta")

DU0_B = Form.basis_form(BRANCH, "du0")
DU1_B = Form.basis_form(BRANCH, "du1")
DU2_B = Form.basis_form(BRANCH, "du2")
DS_B = Form.basis_form(BRANCH, "ds")
DTHETA1_B = Form.basis_form(BRANCH, "dtheta1")
DTHETA2_B = Form.basis_form(BRANCH, "dtheta2")

SOURCE_ATOMS = frozenset({"rho", "drho", "chi", "theta"})


def exterior_derivative(form: Form) -> Form:
    """Differentiate only the explicitly declared source jets."""
    if form.algebra != SOURCE:
        raise ValueError("the declared jet derivative is defined only on source forms")
    differentials = {
        "rho": DS.scale(DRHO),
        "chi": DS,
        "theta": DTHETA,
    }
    result = Form.zero(SOURCE)
    for legs, coefficient in form.terms:
        basis_monomial = Form(SOURCE, {legs: 1})
        for atom, differential in differentials.items():
            derivative = coefficient.derivative(atom)
            if not derivative.is_zero():
                result = result + differential.scale(derivative).wedge(basis_monomial)
    return result


def pullback(
    form: Form,
    branch: str,
    projection: int,
    *,
    mutation: str = "",
) -> Form:
    """Apply one row of the exact D002 branch/projection pullback table."""
    if form.algebra != SOURCE:
        raise ValueError("kernel-pair pullback expects a source form")
    if branch not in {"collapsed", "positive-diagonal"}:
        raise MissingBranchTagError(branch)
    if projection not in {1, 2}:
        raise MissingBranchTagError(f"projection {projection}")
    used_atoms = frozenset(atom for _, coefficient in form.terms for atom in coefficient.atoms)
    unknown_atoms = used_atoms - SOURCE_ATOMS
    if unknown_atoms:
        raise MissingCoefficientTagError(", ".join(sorted(unknown_atoms)))

    if branch == "collapsed":
        theta_target = "theta1" if projection == 1 else "theta2"
        angular_target = DTHETA1_B if projection == 1 else DTHETA2_B
        substitutions: dict[str, str | None] = {
            "rho": None,
            "drho": None,
            "theta": theta_target,
        }
        if mutation == "identify-second-angle" and projection == 2:
            substitutions["theta"] = "theta1"
            angular_target = DTHETA1_B
        elif mutation == "keep-rho":
            substitutions["rho"] = "rho"
        elif mutation == "keep-drho":
            substitutions["drho"] = "drho"
        elif mutation == "erase-second-theta-coefficient" and projection == 2:
            substitutions["theta"] = "theta1"
        elif mutation not in {
            "",
            "identify-second-angle",
            "keep-rho",
            "keep-drho",
            "erase-second-theta-coefficient",
        }:
            raise ValueError(f"unknown pullback mutation {mutation!r}")
    else:
        substitutions = {"theta": "theta1"}
        angular_target = DTHETA1_B
        if mutation:
            raise ValueError("mutations are declared only for the collapsed branch")

    leg_images = {
        "du0": DU0_B,
        "du1": DU1_B,
        "du2": DU2_B,
        "ds": DS_B,
        "dtheta": angular_target,
    }
    result = Form.zero(BRANCH)
    for legs, coefficient in form.terms:
        term = Form.one(BRANCH).scale(coefficient.rename_or_zero(substitutions))
        for leg in legs:
            term = term.wedge(leg_images[leg])
        result = result + term
    return result


def residual(form: Form, branch: str, *, mutation: str = "") -> Form:
    return pullback(form, branch, 1, mutation=mutation) - pullback(
        form, branch, 2, mutation=mutation
    )


ScalarMatrix = list[list[Fraction]]
FormMatrix = list[list[Form]]


def scalar_identity(size: int) -> ScalarMatrix:
    return [[Fraction(int(row == column)) for column in range(size)] for row in range(size)]


def scalar_matmul(left: ScalarMatrix, right: ScalarMatrix) -> ScalarMatrix:
    rows = len(left)
    inner = len(right)
    if not rows or any(len(row) != inner for row in left):
        raise ValueError("incompatible exact scalar matrices")
    columns = len(right[0]) if right else 0
    if any(len(row) != columns for row in right):
        raise ValueError("ragged exact scalar matrix")
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(inner)), Fraction(0))
            for j in range(columns)
        ]
        for i in range(rows)
    ]


def scalar_transpose(matrix: ScalarMatrix) -> ScalarMatrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def zero_form_matrix(size: int, algebra: ExteriorAlgebra) -> FormMatrix:
    return [[Form.zero(algebra) for _ in range(size)] for _ in range(size)]


def add_form_matrices(left: FormMatrix, right: FormMatrix) -> FormMatrix:
    return [
        [left[i][j] + right[i][j] for j in range(len(left[i]))]
        for i in range(len(left))
    ]


def derivative_form_matrix(matrix: FormMatrix) -> FormMatrix:
    return [[exterior_derivative(entry) for entry in row] for row in matrix]


def wedge_form_matrices(left: FormMatrix, right: FormMatrix) -> FormMatrix:
    size = len(left)
    algebra = left[0][0].algebra
    output = zero_form_matrix(size, algebra)
    for row in range(size):
        for column in range(size):
            value = Form.zero(algebra)
            for inner in range(size):
                value = value + left[row][inner].wedge(right[inner][column])
            output[row][column] = value
    return output


def conjugate_form_matrix(
    left: ScalarMatrix, middle: FormMatrix, right: ScalarMatrix
) -> FormMatrix:
    size = len(middle)
    algebra = middle[0][0].algebra
    output = zero_form_matrix(size, algebra)
    for row in range(size):
        for column in range(size):
            value = Form.zero(algebra)
            for first in range(size):
                for second in range(size):
                    coefficient = left[row][first] * right[second][column]
                    if coefficient:
                        value = value + middle[first][second].scale(coefficient)
            output[row][column] = value
    return output


def transform_form_vector(matrix: ScalarMatrix, vector: Sequence[Form]) -> list[Form]:
    algebra = vector[0].algebra
    return [
        sum(
            (vector[column].scale(matrix[row][column]) for column in range(len(vector))),
            Form.zero(algebra),
        )
        for row in range(len(matrix))
    ]


def any_nonzero_matrix(matrix: FormMatrix) -> bool:
    return any(not entry.is_zero() for row in matrix for entry in row)


def upper_component_as_mixed(form: Form) -> FormMatrix:
    """Return the mixed matrix for upper antisymmetric component T^{40}=form."""
    metric = (-1, 1, 1, 1, 1)
    upper = zero_form_matrix(5, form.algebra)
    upper[4][0] = form
    upper[0][4] = -form
    mixed = zero_form_matrix(5, form.algebra)
    for row in range(5):
        for column in range(5):
            mixed[row][column] = upper[row][column].scale(metric[column])
    return mixed


def mixed_to_upper(matrix: FormMatrix) -> FormMatrix:
    metric = (-1, 1, 1, 1, 1)
    return [
        [matrix[row][column].scale(metric[column]) for column in range(5)]
        for row in range(5)
    ]


def nonzero_matrix_data(matrix: FormMatrix) -> dict[str, dict[str, str]]:
    return {
        f"{row},{column}": entry.as_data()
        for row, entries in enumerate(matrix)
        for column, entry in enumerate(entries)
        if not entry.is_zero()
    }


def check() -> int:
    """Execute every exact positive, negative, and mutation control in spec.yaml."""
    if INTERNAL_MUTATION not in SUPPORTED_INTERNAL_MUTATIONS:
        raise ValueError(f"unsupported O001_INTERNAL_MUTATION={INTERNAL_MUTATION!r}")

    assertions: dict[str, bool] = {}

    def expect(name: str, condition: bool) -> None:
        if name in assertions:
            raise RuntimeError(f"duplicate assertion name {name}")
        assertions[name] = bool(condition)

    # Small law/normal-form controls constrain the self-contained trust surface.
    expected_ds_du1 = Form(SOURCE, {("du1", "ds"): -1})
    expect("law.wedge_sign", DS.wedge(DU1) == expected_ds_du1)
    expect("law.graded_antisymmetry", DS.wedge(DU1) == -DU1.wedge(DS))
    expect("law.repeated_leg_zero", DU1.wedge(DU1).is_zero())
    expect(
        "law.associativity",
        DU0.wedge(DU1).wedge(DS) == DU0.wedge(DU1.wedge(DS)),
    )
    expect(
        "law.contraction_sign",
        DU1.wedge(DS).contract("ds") == -DU1,
    )

    # Declared source forms and explicit unit jet.
    a_form = DU1.scale(CHI)
    f_form = exterior_derivative(a_form)
    eta = DTHETA + a_form
    rho_eta = eta.scale(RHO)
    horizontal_mixed = DU2.scale(CHI)
    vertical_mixed = DTHETA
    theta_horizontal = DU0.scale(THETA)

    expect("jet.F_exact", f_form == expected_ds_du1)
    expect("jet.F_nonzero", not f_form.is_zero())

    expected_eta_residual = DTHETA1_B - DTHETA2_B
    expected_theta_residual = DU0_B.scale(Poly.atom("theta1") - Poly.atom("theta2"))
    collapsed_residuals = {
        "eta": residual(eta, "collapsed"),
        "rho_eta": residual(rho_eta, "collapsed"),
        "A": residual(a_form, "collapsed"),
        "F": residual(f_form, "collapsed"),
        "horizontal_mixed": residual(horizontal_mixed, "collapsed"),
    }
    expected_collapsed = {
        "eta": expected_eta_residual,
        "rho_eta": Form.zero(BRANCH),
        "A": Form.zero(BRANCH),
        "F": Form.zero(BRANCH),
        "horizontal_mixed": Form.zero(BRANCH),
    }
    for name in expected_collapsed:
        expect(
            f"P01.collapsed_residual.{name}",
            collapsed_residuals[name] == expected_collapsed[name],
        )
    expect("P01.rho_eta_pullback1_zero", pullback(rho_eta, "collapsed", 1).is_zero())
    expect("P01.rho_eta_pullback2_zero", pullback(rho_eta, "collapsed", 2).is_zero())
    expect("P01.A_survives_as_common_form", not pullback(a_form, "collapsed", 1).is_zero())
    expect("P01.F_survives_as_common_form", not pullback(f_form, "collapsed", 1).is_zero())

    # Negative membership controls.
    vertical_residual = residual(vertical_mixed, "collapsed")
    theta_residual = residual(theta_horizontal, "collapsed")
    expect("N01.vertical_mixed_nonzero", vertical_residual == expected_eta_residual)
    expect("N02.theta_horizontal_nonzero", theta_residual == expected_theta_residual)
    expect("N02.theta_horizontal_really_nonzero", not theta_residual.is_zero())

    # Exact d(rho eta), including the flat drho substitution.
    d_rho_eta = exterior_derivative(rho_eta)
    manual_d_rho_eta = DS.scale(DRHO).wedge(eta) + f_form.scale(RHO)
    expect("P02.derivative_product_rule", d_rho_eta == manual_d_rho_eta)
    expect("P02.collapsed_residual_zero", residual(d_rho_eta, "collapsed").is_zero())
    expect("P02.collapsed_pullback1_zero", pullback(d_rho_eta, "collapsed", 1).is_zero())
    expect("P02.collapsed_pullback2_zero", pullback(d_rho_eta, "collapsed", 2).is_zero())

    # Critical logical control: diagonal descent is not principal-bundle basicness.
    positive_rho_eta = pullback(rho_eta, "positive-diagonal", 1)
    positive_residual = residual(rho_eta, "positive-diagonal")
    positive_contraction = positive_rho_eta.contract("dtheta1")
    expected_contraction = Form.one(BRANCH).scale(RHO)
    expect("P03.diagonal_residual_zero", positive_residual.is_zero())
    expect("P03.fiber_contraction_exact_rho", positive_contraction == expected_contraction)
    expect("P03.fiber_contraction_nonzero", not positive_contraction.is_zero())

    # U(1) gauge and fixed-collapsed-coframe controls.
    dalpha = DU0 + DS.scale(2)
    shifted_dtheta = DTHETA - dalpha
    transformed_a = a_form + dalpha
    transformed_eta = shifted_dtheta + transformed_a
    transformed_f = exterior_derivative(transformed_a)
    expect("P04.u1_eta_invariant", transformed_eta == eta)
    expect("P04.u1_curvature_invariant", transformed_f == f_form)
    expect("P04.u1_theta_roundtrip", shifted_dtheta + dalpha == DTHETA)
    expect("P04.u1_A_roundtrip", transformed_a - dalpha == a_form)
    expect("P04.u1_curvature_nonzero", not transformed_f.is_zero())

    collapsed_coframe_change = a_form.scale(RHO)
    collapsed_dcoframe_change = exterior_derivative(collapsed_coframe_change)
    expect(
        "P04.u1_collapsed_coframe_change_zero",
        pullback(collapsed_coframe_change, "collapsed", 1).is_zero()
        and pullback(collapsed_coframe_change, "collapsed", 2).is_zero(),
    )
    expect(
        "P04.u1_collapsed_dcoframe_change_zero",
        pullback(collapsed_dcoframe_change, "collapsed", 1).is_zero()
        and pullback(collapsed_dcoframe_change, "collapsed", 2).is_zero(),
    )
    wrong_sign_eta = shifted_dtheta + (a_form - dalpha)
    expect("N03.wrong_u1_sign_detected", wrong_sign_eta != eta)
    expect("N04.zero_u1_curvature_detected", Form.zero(SOURCE) != f_form)

    # SO(1,4) unit jet, curvature covariance, K, and exact round trips.
    omega = upper_component_as_mixed(a_form)
    curvature = add_form_matrices(
        derivative_form_matrix(omega), wedge_form_matrices(omega, omega)
    )
    expected_curvature = upper_component_as_mixed(f_form)
    expect("P05.lorentz_curvature_formula", curvature == expected_curvature)
    expect("P05.lorentz_curvature_nonzero", any_nonzero_matrix(curvature))

    boost: ScalarMatrix = scalar_identity(5)
    boost[0][0] = Fraction(5, 3)
    boost[0][1] = Fraction(4, 3)
    boost[1][0] = Fraction(4, 3)
    boost[1][1] = Fraction(5, 3)
    boost_inverse: ScalarMatrix = scalar_identity(5)
    boost_inverse[0][0] = Fraction(5, 3)
    boost_inverse[0][1] = Fraction(-4, 3)
    boost_inverse[1][0] = Fraction(-4, 3)
    boost_inverse[1][1] = Fraction(5, 3)
    identity5 = scalar_identity(5)
    metric: ScalarMatrix = [
        [Fraction((-1 if row == 0 else 1) if row == column else 0) for column in range(5)]
        for row in range(5)
    ]
    inverse_left = scalar_matmul(boost_inverse, boost)
    inverse_right = scalar_matmul(boost, boost_inverse)
    if inverse_left != identity5 or inverse_right != identity5:
        raise GaugeInverseUnavailableError("the declared rational Lorentz boost has no exact inverse")
    expect("P05.boost_inverse_left", inverse_left == identity5)
    expect("P05.boost_inverse_right", inverse_right == identity5)
    expect(
        "P05.boost_lorentz_metric",
        scalar_matmul(scalar_matmul(scalar_transpose(boost), metric), boost) == metric,
    )
    expect(
        "P05.boost_proper_orthochronous",
        boost[0][0] * boost[1][1] - boost[0][1] * boost[1][0] == 1
        and boost[0][0] > 0,
    )

    transformed_omega = conjugate_form_matrix(boost, omega, boost_inverse)
    transformed_curvature_direct = add_form_matrices(
        derivative_form_matrix(transformed_omega),
        wedge_form_matrices(transformed_omega, transformed_omega),
    )
    transformed_curvature_covariant = conjugate_form_matrix(
        boost, curvature, boost_inverse
    )
    expect(
        "P05.curvature_covariance",
        transformed_curvature_direct == transformed_curvature_covariant,
    )
    expect(
        "P05.transformed_curvature_nonzero",
        any_nonzero_matrix(transformed_curvature_covariant),
    )
    expect(
        "P05.connection_roundtrip",
        conjugate_form_matrix(boost_inverse, transformed_omega, boost) == omega,
    )
    expect(
        "P05.curvature_roundtrip",
        conjugate_form_matrix(boost_inverse, transformed_curvature_covariant, boost)
        == curvature,
    )

    coframe = [DU0, DU1, DU2, DS, Form.zero(SOURCE)]
    curved_state_coframe = list(coframe)  # independent connection: same fixed coframe
    transformed_coframe = transform_form_vector(boost, coframe)
    coframe_roundtrip = transform_form_vector(boost_inverse, transformed_coframe)
    expect("P05.independent_connection_fixed_coframe", curved_state_coframe == coframe)
    expect("P05.collapsed_vertical_coframe_stays_zero", transformed_coframe[4].is_zero())
    expect("P05.coframe_roundtrip", coframe_roundtrip == coframe)

    upper_curvature = mixed_to_upper(curvature)
    transformed_upper_curvature = mixed_to_upper(transformed_curvature_covariant)
    k_before = upper_curvature[4][:4]
    k_after = transformed_upper_curvature[4][:4]
    expect("P05.K_before_nonzero", any(not component.is_zero() for component in k_before))
    expect("P05.K_after_nonzero", any(not component.is_zero() for component in k_after))
    zero_matrix = zero_form_matrix(5, SOURCE)
    expect("N04.zero_lorentz_curvature_detected", zero_matrix != curvature)

    # Every declared source-level mutation must change a conclusion-critical check.
    wrong_wedge_value = Form(SOURCE, {("du1", "ds"): 1})
    expect("M01.wedge_sign_reversal_detected", wrong_wedge_value != expected_ds_du1)
    expect(
        "M02.collapsed_angle_identification_detected",
        residual(eta, "collapsed", mutation="identify-second-angle")
        != expected_eta_residual,
    )
    expect(
        "M03.missing_rho_zero_detected",
        not residual(rho_eta, "collapsed", mutation="keep-rho").is_zero(),
    )
    expect(
        "M04.missing_drho_zero_detected",
        not residual(d_rho_eta, "collapsed", mutation="keep-drho").is_zero(),
    )
    expect(
        "M05.theta_dependence_erasure_detected",
        residual(
            theta_horizontal,
            "collapsed",
            mutation="erase-second-theta-coefficient",
        )
        != expected_theta_residual,
    )
    expect(
        "M06.wrong_lorentz_inverse_detected",
        scalar_matmul(boost, boost) != identity5,
    )

    failed = sorted(name for name, passed in assertions.items() if not passed)
    observations = {
        "producer_model": PRODUCER_MODEL,
        "internal_mutation": INTERNAL_MUTATION or "none",
        "representation": {
            "coefficient_domain": "sparse exact Fraction polynomials",
            "target_basis": list(BRANCH.basis),
            "equality": "canonical sparse-map equality",
            "shared_research_kernel": False,
        },
        "collapsed_residuals": {
            name: value.as_data() for name, value in collapsed_residuals.items()
        },
        "negative_controls": {
            "vertical_mixed_residual": vertical_residual.as_data(),
            "theta_dependent_residual": theta_residual.as_data(),
        },
        "positive_diagonal_control": {
            "rho_eta_residual": positive_residual.as_data(),
            "fiber_contraction": positive_contraction.as_data(),
            "interpretation": "descent on the diagonal branch does not imply horizontality",
        },
        "u1_unit_jet": {
            "F": f_form.as_data(),
            "eta_invariant": assertions["P04.u1_eta_invariant"],
            "collapsed_coframe_change": pullback(
                collapsed_coframe_change, "collapsed", 1
            ).as_data(),
            "roundtrip": assertions["P04.u1_A_roundtrip"]
            and assertions["P04.u1_theta_roundtrip"],
        },
        "lorentz_unit_jet": {
            "curvature": nonzero_matrix_data(curvature),
            "transformed_curvature": nonzero_matrix_data(
                transformed_curvature_covariant
            ),
            "K_before_nonzero": assertions["P05.K_before_nonzero"],
            "K_after_nonzero": assertions["P05.K_after_nonzero"],
            "roundtrip": assertions["P05.connection_roundtrip"]
            and assertions["P05.curvature_roundtrip"]
            and assertions["P05.coframe_roundtrip"],
        },
        "assertion_count": len(assertions),
        "failed_assertions": failed,
        "all_declared_controls_passed": not failed,
    }
    emit_observations(observations)
    if failed:
        print("O001 failed assertions: " + ", ".join(failed), file=sys.stderr)
        return FAILED
    return PASSED


def emit_observations(observations: dict[str, Any]) -> None:
    """Emit one structured, machine-readable observation record to stdout."""
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


def main() -> int:
    try:
        outcome = check()
    except (
        MissingBranchTagError,
        MissingCoefficientTagError,
        GaugeInverseUnavailableError,
    ) as exc:
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
