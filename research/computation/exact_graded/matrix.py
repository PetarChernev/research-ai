"""Deterministic exact row reduction for nonempty rational matrices."""

from __future__ import annotations

import json
from fractions import Fraction
from typing import Any, Sequence

from ._rational import as_fraction


class RationalMatrix:
    """An immutable nonempty rectangular matrix over ``Fraction``.

    Zero-row and zero-column shapes are deliberately rejected.  Pivot columns
    use zero-based indices.
    """

    __slots__ = ("_rows", "_nrows", "_ncols")

    def __init__(self, rows: Sequence[Sequence[int | Fraction]]) -> None:
        if not isinstance(rows, (tuple, list)) or isinstance(rows, (str, bytes)):
            raise TypeError("matrix rows must be supplied as a tuple or list")
        if not rows:
            raise ValueError("matrices with zero rows are unsupported")

        normalized: list[tuple[Fraction, ...]] = []
        width: int | None = None
        for row_index, row in enumerate(rows):
            if not isinstance(row, (tuple, list)) or isinstance(row, (str, bytes)):
                raise TypeError(f"matrix row {row_index} must be a tuple or list")
            if width is None:
                width = len(row)
                if width == 0:
                    raise ValueError("matrices with zero columns are unsupported")
            elif len(row) != width:
                raise ValueError("matrix rows must all have the same length")
            normalized.append(
                tuple(
                    as_fraction(value, what=f"matrix entry ({row_index}, {column_index})")
                    for column_index, value in enumerate(row)
                )
            )

        self._rows = tuple(normalized)
        self._nrows = len(normalized)
        self._ncols = width if width is not None else 0

    @property
    def rows(self) -> tuple[tuple[Fraction, ...], ...]:
        return self._rows

    @property
    def nrows(self) -> int:
        return self._nrows

    @property
    def ncols(self) -> int:
        return self._ncols

    @property
    def shape(self) -> tuple[int, int]:
        return self._nrows, self._ncols

    def rref(self) -> tuple[RationalMatrix, tuple[int, ...]]:
        """Return deterministic reduced row-echelon form and pivot columns."""

        data = [list(row) for row in self._rows]
        pivot_columns: list[int] = []
        pivot_row = 0

        for column in range(self._ncols):
            selected = next(
                (row for row in range(pivot_row, self._nrows) if data[row][column]),
                None,
            )
            if selected is None:
                continue
            if selected != pivot_row:
                data[pivot_row], data[selected] = data[selected], data[pivot_row]

            pivot = data[pivot_row][column]
            data[pivot_row] = [entry / pivot for entry in data[pivot_row]]
            for row in range(self._nrows):
                if row == pivot_row:
                    continue
                factor = data[row][column]
                if factor:
                    data[row] = [
                        entry - factor * pivot_entry
                        for entry, pivot_entry in zip(data[row], data[pivot_row])
                    ]

            pivot_columns.append(column)
            pivot_row += 1
            if pivot_row == self._nrows:
                break

        return RationalMatrix(data), tuple(pivot_columns)

    def rank(self) -> int:
        return len(self.rref()[1])

    def nullspace(self) -> tuple[tuple[Fraction, ...], ...]:
        """Return a deterministic basis ordered by ascending free column."""

        reduced, pivots = self.rref()
        pivot_set = set(pivots)
        free_columns = [column for column in range(self._ncols) if column not in pivot_set]
        basis: list[tuple[Fraction, ...]] = []
        for free_column in free_columns:
            vector = [Fraction(0) for _ in range(self._ncols)]
            vector[free_column] = Fraction(1)
            for row, pivot_column in enumerate(pivots):
                vector[pivot_column] = -reduced.rows[row][free_column]
            basis.append(tuple(vector))
        return tuple(basis)

    def matvec(self, vector: Sequence[int | Fraction]) -> tuple[Fraction, ...]:
        if not isinstance(vector, (tuple, list)) or isinstance(vector, (str, bytes)):
            raise TypeError("matrix vector must be supplied as a tuple or list")
        if len(vector) != self._ncols:
            raise ValueError(
                f"matrix-vector dimension mismatch: expected {self._ncols}, got {len(vector)}"
            )
        exact_vector = tuple(
            as_fraction(value, what=f"vector entry {position}")
            for position, value in enumerate(vector)
        )
        return tuple(
            sum((entry * component for entry, component in zip(row, exact_vector)), Fraction(0))
            for row in self._rows
        )

    def to_data(self) -> dict[str, Any]:
        return {
            "type": "rational_matrix",
            "shape": [self._nrows, self._ncols],
            "rows": [
                [[entry.numerator, entry.denominator] for entry in row]
                for row in self._rows
            ],
        }

    def serialize(self) -> str:
        return json.dumps(self.to_data(), sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RationalMatrix) and self._rows == other._rows

    def __repr__(self) -> str:
        return f"RationalMatrix({self.serialize()})"
