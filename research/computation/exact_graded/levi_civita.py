"""Levi-Civita permutation signs relative to explicit orientations."""

from __future__ import annotations

from typing import Any


def _validate_index_label(label: Any, *, what: str) -> int | str:
    if type(label) is int:
        return label
    if type(label) is str and label:
        return label
    raise TypeError(f"{what} must be an integer or non-empty string")


def levi_civita_sign(indices: tuple[int | str, ...], orientation: tuple[int | str, ...]) -> int:
    """Return ``-1``, ``0`` or ``+1`` for an explicitly oriented index tuple.

    Every valid permutation receives its parity.  A valid-length tuple made
    entirely of known indices returns zero when an index is repeated.  Unknown
    indices and wrong lengths are errors.
    """

    if type(orientation) is not tuple:
        raise TypeError("orientation must be an explicit tuple")
    if type(indices) is not tuple:
        raise TypeError("indices must be an explicit tuple")
    if not orientation:
        raise ValueError("orientation must contain at least one index")

    checked_orientation = tuple(
        _validate_index_label(label, what=f"orientation label at position {position}")
        for position, label in enumerate(orientation)
    )
    if len(set(checked_orientation)) != len(checked_orientation):
        raise ValueError("orientation indices must be unique")
    if len(indices) != len(checked_orientation):
        raise ValueError(
            f"index tuple length {len(indices)} does not match orientation length "
            f"{len(checked_orientation)}"
        )

    checked_indices = tuple(
        _validate_index_label(label, what=f"index at position {position}")
        for position, label in enumerate(indices)
    )
    positions = {label: position for position, label in enumerate(checked_orientation)}
    unknown = [label for label in checked_indices if label not in positions]
    if unknown:
        raise ValueError("unknown indices: " + ", ".join(repr(label) for label in unknown))
    if len(set(checked_indices)) != len(checked_indices):
        return 0

    permutation = [positions[label] for label in checked_indices]
    inversions = sum(
        1
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
        if permutation[left] > permutation[right]
    )
    return -1 if inversions % 2 else 1
