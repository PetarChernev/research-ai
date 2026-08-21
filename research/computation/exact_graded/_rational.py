"""Internal exact-rational validation shared by the kernel modules."""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def as_fraction(value: Any, *, what: str = "coefficient") -> Fraction:
    """Return an exact ``Fraction`` without performing lossy coercions.

    Only built-in integers (excluding booleans) and already-constructed
    ``Fraction`` instances are accepted.  In particular, this helper never
    calls ``Fraction`` on a float, string, decimal, or arbitrary numeric type.
    """

    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise TypeError(
        f"{what} must be an int or fractions.Fraction; "
        f"got {type(value).__name__}"
    )


def is_rational_input(value: Any) -> bool:
    """Whether *value* is an accepted public rational input."""

    return type(value) is int or type(value) is Fraction
