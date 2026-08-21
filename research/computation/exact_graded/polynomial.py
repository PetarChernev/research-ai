"""Canonical sparse multivariate polynomials over ``fractions.Fraction``."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from fractions import Fraction
from typing import Any, TypeAlias

from ._rational import as_fraction, is_rational_input

Generator: TypeAlias = str
Monomial: TypeAlias = tuple[tuple[Generator, int], ...]
Term: TypeAlias = tuple[Monomial, Fraction]


def _validate_generator(generator: Any, *, what: str = "generator") -> str:
    if type(generator) is not str or not generator:
        raise TypeError(f"{what} must be a non-empty string")
    return generator


def _normalize_monomial(raw: Any) -> Monomial:
    if type(raw) is not tuple:
        raise TypeError("a polynomial monomial must be a tuple of (generator, exponent) pairs")

    powers: dict[str, int] = {}
    for position, factor in enumerate(raw):
        if type(factor) is not tuple or len(factor) != 2:
            raise TypeError(
                f"monomial factor {position} must be a two-item tuple "
                "(generator, exponent)"
            )
        generator, exponent = factor
        name = _validate_generator(generator, what=f"monomial generator at factor {position}")
        if type(exponent) is not int:
            raise TypeError(f"exponent for {name!r} must be a nonnegative integer")
        if exponent < 0:
            raise ValueError(f"negative exponent for {name!r} is not supported")
        if exponent:
            powers[name] = powers.get(name, 0) + exponent

    return tuple(sorted(powers.items()))


def _iter_term_pairs(terms: Any) -> Iterable[tuple[Any, Any]]:
    if isinstance(terms, Mapping):
        iterator = iter(terms.items())
    else:
        if isinstance(terms, (str, bytes)):
            raise TypeError("sparse terms must be a mapping or an iterable of pairs")
        try:
            iterator = iter(terms)
        except TypeError as exc:
            raise TypeError("sparse terms must be a mapping or an iterable of pairs") from exc

    for position, entry in enumerate(iterator):
        if not isinstance(entry, (tuple, list)) or len(entry) != 2:
            raise TypeError(f"sparse term {position} must be a (monomial, coefficient) pair")
        yield entry[0], entry[1]


class Polynomial:
    """An immutable canonical sparse polynomial.

    Public sparse terms have shape ``(monomial, coefficient)``.  A monomial is
    a tuple of ``(nonempty_string, nonnegative_int)`` pairs.  Construction
    sorts factors, combines repeated generators and terms, removes zero powers,
    and removes zero coefficients.
    """

    __slots__ = ("_items",)

    def __init__(self, terms: Any = ()) -> None:
        collected: dict[Monomial, Fraction] = {}
        for raw_monomial, raw_coefficient in _iter_term_pairs(terms):
            monomial = _normalize_monomial(raw_monomial)
            coefficient = as_fraction(raw_coefficient, what="polynomial coefficient")
            if coefficient:
                updated = collected.get(monomial, Fraction(0)) + coefficient
                if updated:
                    collected[monomial] = updated
                else:
                    collected.pop(monomial, None)
        self._items: tuple[Term, ...] = tuple(sorted(collected.items()))

    @classmethod
    def zero(cls) -> Polynomial:
        return cls()

    @classmethod
    def one(cls) -> Polynomial:
        return cls.constant(1)

    @classmethod
    def constant(cls, coefficient: int | Fraction) -> Polynomial:
        return cls([((), coefficient)])

    @classmethod
    def generator(cls, name: str) -> Polynomial:
        name = _validate_generator(name)
        return cls([(((name, 1),), 1)])

    @classmethod
    def monomial(
        cls,
        powers: Monomial,
        coefficient: int | Fraction = 1,
    ) -> Polynomial:
        return cls([(powers, coefficient)])

    @classmethod
    def from_terms(cls, terms: Any) -> Polynomial:
        return cls(terms)

    @property
    def terms(self) -> tuple[Term, ...]:
        """Canonical terms ordered lexicographically by canonical monomial."""

        return self._items

    @property
    def generators(self) -> tuple[str, ...]:
        names = {name for monomial, _ in self._items for name, _ in monomial}
        return tuple(sorted(names))

    @property
    def is_zero(self) -> bool:
        return not self._items

    @property
    def is_constant(self) -> bool:
        return all(not monomial for monomial, _ in self._items)

    def coefficient(self, monomial: Monomial) -> Fraction:
        canonical = _normalize_monomial(monomial)
        return dict(self._items).get(canonical, Fraction(0))

    @staticmethod
    def _coerce_operand(value: Any) -> Polynomial | Any:
        if isinstance(value, Polynomial):
            return value
        if is_rational_input(value):
            return Polynomial.constant(value)
        if isinstance(value, (float, complex)) or type(value) is bool:
            raise TypeError("polynomial arithmetic accepts only polynomials, ints, or Fractions")
        return NotImplemented

    def __add__(self, other: Any) -> Polynomial:
        rhs = self._coerce_operand(other)
        if rhs is NotImplemented:
            return NotImplemented
        collected = dict(self._items)
        for monomial, coefficient in rhs._items:
            updated = collected.get(monomial, Fraction(0)) + coefficient
            if updated:
                collected[monomial] = updated
            else:
                collected.pop(monomial, None)
        return Polynomial(collected)

    def __radd__(self, other: Any) -> Polynomial:
        return self + other

    def __neg__(self) -> Polynomial:
        return Polynomial((monomial, -coefficient) for monomial, coefficient in self._items)

    def __sub__(self, other: Any) -> Polynomial:
        rhs = self._coerce_operand(other)
        if rhs is NotImplemented:
            return NotImplemented
        return self + (-rhs)

    def __rsub__(self, other: Any) -> Polynomial:
        lhs = self._coerce_operand(other)
        if lhs is NotImplemented:
            return NotImplemented
        return lhs - self

    def __mul__(self, other: Any) -> Polynomial:
        rhs = self._coerce_operand(other)
        if rhs is NotImplemented:
            return NotImplemented
        if self.is_zero or rhs.is_zero:
            return Polynomial.zero()

        collected: dict[Monomial, Fraction] = {}
        for left_monomial, left_coefficient in self._items:
            left_powers = dict(left_monomial)
            for right_monomial, right_coefficient in rhs._items:
                powers = dict(left_powers)
                for generator, exponent in right_monomial:
                    powers[generator] = powers.get(generator, 0) + exponent
                monomial = tuple(sorted(powers.items()))
                coefficient = left_coefficient * right_coefficient
                updated = collected.get(monomial, Fraction(0)) + coefficient
                if updated:
                    collected[monomial] = updated
                else:
                    collected.pop(monomial, None)
        return Polynomial(collected)

    def __rmul__(self, other: Any) -> Polynomial:
        return self * other

    def __pow__(self, exponent: int, modulo: Any = None) -> Polynomial:
        if modulo is not None:
            raise TypeError("modular polynomial powers are not supported")
        if type(exponent) is not int:
            raise TypeError("polynomial exponent must be a nonnegative integer")
        if exponent < 0:
            raise ValueError("negative polynomial exponents are not supported")

        result = Polynomial.one()
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * base
            remaining >>= 1
            if remaining:
                base = base * base
        return result

    def __truediv__(self, other: Any) -> Polynomial:
        raise TypeError("polynomial division is unsupported; construct exact coefficients explicitly")

    def __rtruediv__(self, other: Any) -> Polynomial:
        raise TypeError("symbolic division by a polynomial is unsupported")

    def differentiate(self, generator: str) -> Polynomial:
        name = _validate_generator(generator, what="differentiation generator")
        differentiated: list[tuple[Monomial, Fraction]] = []
        for monomial, coefficient in self._items:
            powers = dict(monomial)
            exponent = powers.get(name, 0)
            if not exponent:
                continue
            if exponent == 1:
                del powers[name]
            else:
                powers[name] = exponent - 1
            differentiated.append((tuple(sorted(powers.items())), coefficient * exponent))
        return Polynomial(differentiated)

    def substitute(self, replacements: Mapping[str, Polynomial | int | Fraction]) -> Polynomial:
        """Simultaneously substitute exact constants or polynomials.

        Replacement polynomials are inserted as supplied and are not themselves
        recursively transformed by other entries in *replacements*.  Generators
        absent from the mapping remain unchanged.
        """

        if not isinstance(replacements, Mapping):
            raise TypeError("polynomial substitutions must be supplied as a mapping")

        normalized: dict[str, Polynomial] = {}
        for raw_name, replacement in replacements.items():
            name = _validate_generator(raw_name, what="substitution generator")
            if isinstance(replacement, Polynomial):
                normalized[name] = replacement
            elif is_rational_input(replacement):
                normalized[name] = Polynomial.constant(replacement)
            else:
                raise TypeError(
                    f"replacement for {name!r} must be a Polynomial, int, or Fraction"
                )

        result = Polynomial.zero()
        for monomial, coefficient in self._items:
            term = Polynomial.constant(coefficient)
            for generator, exponent in monomial:
                replacement = normalized.get(generator)
                if replacement is None:
                    replacement = Polynomial.generator(generator)
                term = term * (replacement**exponent)
            result = result + term
        return result

    def to_data(self) -> dict[str, Any]:
        return {
            "type": "polynomial",
            "terms": [
                {
                    "monomial": [[generator, exponent] for generator, exponent in monomial],
                    "coefficient": [coefficient.numerator, coefficient.denominator],
                }
                for monomial, coefficient in self._items
            ],
        }

    def serialize(self) -> str:
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polynomial):
            return False
        return self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def __bool__(self) -> bool:
        return not self.is_zero

    def __repr__(self) -> str:
        return f"Polynomial({self.serialize()})"
