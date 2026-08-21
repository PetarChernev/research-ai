"""Sparse exterior forms with explicit ordered-basis semantics."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, TypeAlias

from .polynomial import Polynomial

ExteriorMonomial: TypeAlias = tuple[str, ...]
ExteriorTerm: TypeAlias = tuple[ExteriorMonomial, Polynomial]


class AlgebraMismatchError(ValueError):
    """Raised when forms or vectors use different ordered exterior bases."""


def _validate_basis_label(label: Any, *, what: str = "basis label") -> str:
    if type(label) is not str or not label:
        raise TypeError(f"{what} must be a non-empty string")
    return label


def _as_polynomial(value: Any, *, what: str = "exterior coefficient") -> Polynomial:
    if isinstance(value, Polynomial):
        return value
    try:
        return Polynomial.constant(value)
    except TypeError as exc:
        raise TypeError(f"{what} must be a Polynomial, int, or Fraction") from exc


def _iter_term_pairs(terms: Any) -> Iterable[tuple[Any, Any]]:
    if isinstance(terms, Mapping):
        iterator = iter(terms.items())
    else:
        if isinstance(terms, (str, bytes)):
            raise TypeError("exterior terms must be a mapping or an iterable of pairs")
        try:
            iterator = iter(terms)
        except TypeError as exc:
            raise TypeError("exterior terms must be a mapping or an iterable of pairs") from exc
    for position, entry in enumerate(iterator):
        if not isinstance(entry, (tuple, list)) or len(entry) != 2:
            raise TypeError(f"exterior term {position} must be a (monomial, coefficient) pair")
        yield entry[0], entry[1]


class ExteriorAlgebra:
    """An exterior algebra declared by a unique ordered tuple/list of labels."""

    __slots__ = ("_basis", "_index")

    def __init__(self, basis: tuple[str, ...] | list[str]) -> None:
        if not isinstance(basis, (tuple, list)) or isinstance(basis, (str, bytes)):
            raise TypeError("an exterior basis must be an ordered tuple or list")
        labels = tuple(
            _validate_basis_label(label, what=f"basis label at position {position}")
            for position, label in enumerate(basis)
        )
        if len(set(labels)) != len(labels):
            raise ValueError("an exterior basis must contain unique labels")
        self._basis = labels
        self._index = {label: position for position, label in enumerate(labels)}

    @property
    def basis(self) -> tuple[str, ...]:
        return self._basis

    def zero(self) -> ExteriorForm:
        return ExteriorForm(self)

    def unit(self) -> ExteriorForm:
        return self.scalar(1)

    def scalar(self, coefficient: Polynomial | int | Fraction) -> ExteriorForm:
        return ExteriorForm(self, [((), coefficient)])

    def basis_form(self, label: str) -> ExteriorForm:
        name = _validate_basis_label(label)
        if name not in self._index:
            raise ValueError(f"unknown exterior basis label {name!r}")
        return ExteriorForm(self, [((name,), 1)])

    def basis_vector(self, label: str) -> BasisVector:
        return BasisVector(self, label)

    def from_terms(self, terms: Any) -> ExteriorForm:
        return ExteriorForm(self, terms)

    def field_derivative(
        self,
        form: ExteriorForm,
        coordinate_to_differential: Mapping[str, ExteriorForm],
    ) -> ExteriorForm:
        if not isinstance(form, ExteriorForm):
            raise TypeError("field derivative requires an ExteriorForm")
        form._require_algebra(self)
        if not isinstance(coordinate_to_differential, Mapping):
            raise TypeError("coordinate-to-differential data must be a mapping")

        differential_map: dict[str, ExteriorForm] = {}
        for raw_coordinate, differential in coordinate_to_differential.items():
            if type(raw_coordinate) is not str or not raw_coordinate:
                raise TypeError("field-coordinate names must be non-empty strings")
            if not isinstance(differential, ExteriorForm):
                raise TypeError(
                    f"differential assigned to {raw_coordinate!r} must be an ExteriorForm"
                )
            differential._require_algebra(self)
            if not differential._is_zero_or_degree_one():
                raise ValueError(
                    f"differential assigned to {raw_coordinate!r} must be zero or degree one"
                )
            if not differential._has_constant_coefficients():
                raise ValueError(
                    f"differential assigned to {raw_coordinate!r} must have constant coefficients"
                )
            differential_map[raw_coordinate] = differential

        used_coordinates = {
            generator
            for _, coefficient in form.terms
            for generator in coefficient.generators
        }
        missing = sorted(used_coordinates.difference(differential_map))
        if missing:
            raise ValueError(
                "coordinate-to-differential map is incomplete for coefficient generators: "
                + ", ".join(repr(name) for name in missing)
            )

        result = self.zero()
        for monomial, coefficient in form.terms:
            for generator in coefficient.generators:
                derivative = coefficient.differentiate(generator)
                if derivative.is_zero:
                    continue
                coefficient_form = self.from_terms([(monomial, derivative)])
                result = result + differential_map[generator].wedge(coefficient_form)
        return result

    def _canonicalize_monomial(self, raw: Any) -> tuple[int, ExteriorMonomial]:
        if type(raw) is not tuple:
            raise TypeError("an exterior monomial must be a tuple of basis labels")
        indices: list[int] = []
        for position, raw_label in enumerate(raw):
            label = _validate_basis_label(
                raw_label, what=f"exterior monomial label at position {position}"
            )
            if label not in self._index:
                raise ValueError(f"unknown exterior basis label {label!r}")
            indices.append(self._index[label])
        if len(set(indices)) != len(indices):
            return 0, ()
        inversions = sum(
            1
            for left in range(len(indices))
            for right in range(left + 1, len(indices))
            if indices[left] > indices[right]
        )
        canonical = tuple(self._basis[index] for index in sorted(indices))
        return (-1 if inversions % 2 else 1), canonical

    def _monomial_order(self, monomial: ExteriorMonomial) -> tuple[int, ...]:
        return tuple(self._index[label] for label in monomial)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ExteriorAlgebra) and self._basis == other._basis

    def __hash__(self) -> int:
        return hash(self._basis)

    def __repr__(self) -> str:
        return f"ExteriorAlgebra({self._basis!r})"


@dataclass(frozen=True)
class BasisVector:
    """A declared basis vector dual to one named basis one-form.

    The dual pairing is part of the basis declaration; it does not use a
    metric or perform index raising.
    """

    algebra: ExteriorAlgebra
    label: str

    def __post_init__(self) -> None:
        if not isinstance(self.algebra, ExteriorAlgebra):
            raise TypeError("a basis vector requires an ExteriorAlgebra")
        name = _validate_basis_label(self.label, what="basis-vector label")
        if name not in self.algebra.basis:
            raise ValueError(f"unknown basis-vector label {name!r}")


class ExteriorForm:
    """An immutable sparse form belonging to an explicit ``ExteriorAlgebra``."""

    __slots__ = ("_algebra", "_items")

    def __init__(self, algebra: ExteriorAlgebra, terms: Any = ()) -> None:
        if not isinstance(algebra, ExteriorAlgebra):
            raise TypeError("an ExteriorForm requires an ExteriorAlgebra")
        collected: dict[ExteriorMonomial, Polynomial] = {}
        for raw_monomial, raw_coefficient in _iter_term_pairs(terms):
            sign, monomial = algebra._canonicalize_monomial(raw_monomial)
            coefficient = _as_polynomial(raw_coefficient)
            if not sign or coefficient.is_zero:
                continue
            if sign < 0:
                coefficient = -coefficient
            updated = collected.get(monomial, Polynomial.zero()) + coefficient
            if updated.is_zero:
                collected.pop(monomial, None)
            else:
                collected[monomial] = updated
        self._algebra = algebra
        self._items: tuple[ExteriorTerm, ...] = tuple(
            sorted(collected.items(), key=lambda item: algebra._monomial_order(item[0]))
        )

    @property
    def algebra(self) -> ExteriorAlgebra:
        return self._algebra

    @property
    def terms(self) -> tuple[ExteriorTerm, ...]:
        return self._items

    @property
    def is_zero(self) -> bool:
        return not self._items

    @property
    def degrees(self) -> tuple[int, ...]:
        return tuple(sorted({len(monomial) for monomial, _ in self._items}))

    def _require_algebra(self, algebra: ExteriorAlgebra) -> None:
        if not isinstance(algebra, ExteriorAlgebra):
            raise TypeError("expected an ExteriorAlgebra")
        if self._algebra != algebra:
            raise AlgebraMismatchError(
                f"exterior algebra mismatch: {self._algebra.basis!r} != {algebra.basis!r}"
            )

    def _require_compatible_form(self, other: Any) -> ExteriorForm:
        if not isinstance(other, ExteriorForm):
            raise TypeError("operation requires another ExteriorForm")
        other._require_algebra(self._algebra)
        return other

    def _is_zero_or_degree_one(self) -> bool:
        return self.is_zero or self.degrees == (1,)

    def _has_constant_coefficients(self) -> bool:
        return all(coefficient.is_constant for _, coefficient in self._items)

    def __add__(self, other: Any) -> ExteriorForm:
        if not isinstance(other, ExteriorForm):
            return NotImplemented
        rhs = self._require_compatible_form(other)
        collected = dict(self._items)
        for monomial, coefficient in rhs._items:
            updated = collected.get(monomial, Polynomial.zero()) + coefficient
            if updated.is_zero:
                collected.pop(monomial, None)
            else:
                collected[monomial] = updated
        return ExteriorForm(self._algebra, collected)

    def __sub__(self, other: Any) -> ExteriorForm:
        if not isinstance(other, ExteriorForm):
            return NotImplemented
        return self + (-self._require_compatible_form(other))

    def __neg__(self) -> ExteriorForm:
        return ExteriorForm(
            self._algebra,
            ((monomial, -coefficient) for monomial, coefficient in self._items),
        )

    def scale(self, scalar: Polynomial | int | Fraction) -> ExteriorForm:
        coefficient = _as_polynomial(scalar, what="exterior scalar")
        if coefficient.is_zero or self.is_zero:
            return self._algebra.zero()
        return ExteriorForm(
            self._algebra,
            ((monomial, form_coefficient * coefficient) for monomial, form_coefficient in self._items),
        )

    def __mul__(self, scalar: Any) -> ExteriorForm:
        if isinstance(scalar, ExteriorForm):
            raise TypeError("form multiplication is not implicit; call wedge()")
        return self.scale(scalar)

    def __rmul__(self, scalar: Any) -> ExteriorForm:
        return self * scalar

    def wedge(self, other: ExteriorForm) -> ExteriorForm:
        rhs = self._require_compatible_form(other)
        collected: dict[ExteriorMonomial, Polynomial] = {}
        index = self._algebra._index
        for left_monomial, left_coefficient in self._items:
            left_set = set(left_monomial)
            for right_monomial, right_coefficient in rhs._items:
                if left_set.intersection(right_monomial):
                    continue
                inversions = sum(
                    1
                    for left_label in left_monomial
                    for right_label in right_monomial
                    if index[left_label] > index[right_label]
                )
                monomial = tuple(
                    sorted(left_monomial + right_monomial, key=index.__getitem__)
                )
                coefficient = left_coefficient * right_coefficient
                if inversions % 2:
                    coefficient = -coefficient
                updated = collected.get(monomial, Polynomial.zero()) + coefficient
                if updated.is_zero:
                    collected.pop(monomial, None)
                else:
                    collected[monomial] = updated
        return ExteriorForm(self._algebra, collected)

    def pullback(
        self,
        target: ExteriorAlgebra,
        generator_map: Mapping[str, ExteriorForm],
    ) -> ExteriorForm:
        """Extend a complete one-form generator map as an algebra pullback."""

        if not isinstance(target, ExteriorAlgebra):
            raise TypeError("pullback target must be an ExteriorAlgebra")
        if not isinstance(generator_map, Mapping):
            raise TypeError("pullback generator map must be a mapping")

        keys = tuple(generator_map.keys())
        for key in keys:
            if type(key) is not str or not key:
                raise TypeError("pullback generator-map keys must be non-empty strings")
        unknown = [key for key in keys if key not in self._algebra.basis]
        missing = [label for label in self._algebra.basis if label not in generator_map]
        if unknown or missing:
            details: list[str] = []
            if missing:
                details.append("missing " + ", ".join(repr(label) for label in missing))
            if unknown:
                details.append("unknown " + ", ".join(repr(label) for label in unknown))
            raise ValueError("invalid pullback map: " + "; ".join(details))

        images: dict[str, ExteriorForm] = {}
        for label in self._algebra.basis:
            image = generator_map[label]
            if not isinstance(image, ExteriorForm):
                raise TypeError(
                    f"pullback image for {label!r} must be a target ExteriorForm "
                    "(use target.zero() for zero)"
                )
            image._require_algebra(target)
            if not image._is_zero_or_degree_one():
                raise ValueError(f"pullback image for {label!r} must be zero or degree one")
            images[label] = image

        result = target.zero()
        for monomial, coefficient in self._items:
            image = target.scalar(coefficient)
            for label in monomial:
                image = image.wedge(images[label])
            result = result + image
        return result

    def contract(self, vector: BasisVector) -> ExteriorForm:
        """Left contraction by a declared dual basis vector."""

        if not isinstance(vector, BasisVector):
            raise TypeError("contraction requires a declared BasisVector")
        if vector.algebra != self._algebra:
            raise AlgebraMismatchError(
                f"basis-vector algebra {vector.algebra.basis!r} does not match "
                f"form algebra {self._algebra.basis!r}"
            )

        contracted: list[tuple[ExteriorMonomial, Polynomial]] = []
        for monomial, coefficient in self._items:
            if vector.label not in monomial:
                continue
            position = monomial.index(vector.label)
            reduced = monomial[:position] + monomial[position + 1 :]
            contracted.append((reduced, -coefficient if position % 2 else coefficient))
        return ExteriorForm(self._algebra, contracted)

    def field_derivative(
        self,
        coordinate_to_differential: Mapping[str, ExteriorForm],
    ) -> ExteriorForm:
        return self._algebra.field_derivative(self, coordinate_to_differential)

    def to_data(self) -> dict[str, Any]:
        return {
            "type": "exterior_form",
            "basis": list(self._algebra.basis),
            "terms": [
                {
                    "monomial": list(monomial),
                    "coefficient": coefficient.to_data(),
                }
                for monomial, coefficient in self._items
            ],
        }

    def serialize(self) -> str:
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExteriorForm):
            return False
        other._require_algebra(self._algebra)
        return self._items == other._items

    def __bool__(self) -> bool:
        return not self.is_zero

    def __repr__(self) -> str:
        return f"ExteriorForm({self.serialize()})"
