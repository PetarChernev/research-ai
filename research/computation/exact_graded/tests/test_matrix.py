from __future__ import annotations

import json
import unittest
from decimal import Decimal
from fractions import Fraction

from research.computation.exact_graded import RationalMatrix


class RationalMatrixReductionTests(unittest.TestCase):
    def test_deficient_rref_pivots_rank_and_nullspace(self) -> None:
        matrix = RationalMatrix(
            [
                [1, 2, 1],
                [2, 4, 0],
                [0, 0, 1],
            ]
        )
        reduced, pivots = matrix.rref()
        self.assertEqual(
            reduced,
            RationalMatrix(
                [
                    [1, 2, 0],
                    [0, 0, 1],
                    [0, 0, 0],
                ]
            ),
        )
        self.assertEqual(pivots, (0, 2))
        self.assertEqual(matrix.rank(), 2)
        self.assertEqual(matrix.nullspace(), ((Fraction(-2), Fraction(1), Fraction(0)),))
        for vector in matrix.nullspace():
            self.assertEqual(matrix.matvec(vector), (Fraction(0),) * matrix.nrows)

    def test_full_rank_control(self) -> None:
        matrix = RationalMatrix([[1, 2], [3, 4]])
        reduced, pivots = matrix.rref()
        self.assertEqual(reduced, RationalMatrix([[1, 0], [0, 1]]))
        self.assertEqual(pivots, (0, 1))
        self.assertEqual(matrix.rank(), 2)
        self.assertEqual(matrix.nullspace(), ())

    def test_rectangular_exact_fraction_control_and_every_null_vector(self) -> None:
        matrix = RationalMatrix(
            [
                [Fraction(1, 2), 1, 0, 2],
                [1, 2, 1, 5],
            ]
        )
        reduced, pivots = matrix.rref()
        self.assertEqual(pivots, (0, 2))
        self.assertEqual(matrix.shape, (2, 4))
        self.assertEqual(reduced.rows[0], (Fraction(1), Fraction(2), Fraction(0), Fraction(4)))
        self.assertEqual(reduced.rows[1], (Fraction(0), Fraction(0), Fraction(1), Fraction(1)))
        nullspace = matrix.nullspace()
        self.assertEqual(len(nullspace), 2)
        for vector in nullspace:
            self.assertEqual(matrix.matvec(vector), (Fraction(0), Fraction(0)))

    def test_pivot_selection_is_deterministic(self) -> None:
        matrix = RationalMatrix([[0, 2, 4], [1, 3, 5], [0, 0, 0]])
        first = matrix.rref()
        second = matrix.rref()
        self.assertEqual(first, second)
        self.assertEqual(first[1], (0, 1))


class RationalMatrixApiTests(unittest.TestCase):
    def test_rejects_empty_ragged_and_nonrational_matrices(self) -> None:
        with self.assertRaises(ValueError):
            RationalMatrix([])
        with self.assertRaises(ValueError):
            RationalMatrix([[]])
        with self.assertRaises(ValueError):
            RationalMatrix([[1, 2], [3]])
        with self.assertRaises(TypeError):
            RationalMatrix((row for row in [[1]]))  # type: ignore[arg-type]
        for value in (0.5, True, Decimal('1'), '1'):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    RationalMatrix([[value]])  # type: ignore[list-item]

    def test_matvec_validates_shape_and_entries(self) -> None:
        matrix = RationalMatrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            matrix.matvec([1])
        with self.assertRaises(TypeError):
            matrix.matvec((value for value in [1, 2]))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            matrix.matvec([1, 2.0])  # type: ignore[list-item]

    def test_serialization_is_exact_stable_and_auditable(self) -> None:
        matrix = RationalMatrix([[Fraction(1, 3), -2], [0, Fraction(5, 7)]])
        self.assertEqual(matrix.serialize(), matrix.serialize())
        equivalent = RationalMatrix([[Fraction(2, 6), -2], [0, Fraction(10, 14)]])
        self.assertEqual(matrix.serialize(), equivalent.serialize())
        data = json.loads(matrix.serialize())
        self.assertEqual(data['shape'], [2, 2])
        self.assertEqual(data['rows'][0], [[1, 3], [-2, 1]])


if __name__ == '__main__':
    unittest.main()
