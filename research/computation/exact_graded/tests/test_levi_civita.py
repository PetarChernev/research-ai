from __future__ import annotations

import itertools
import math
import unittest

from research.computation.exact_graded import levi_civita_sign


def independent_permutation_parity(permutation: tuple[int, ...]) -> int:
    inversions = 0
    for left, value in enumerate(permutation):
        inversions += sum(value > later for later in permutation[left + 1 :])
    return -1 if inversions % 2 else 1


class LeviCivitaTests(unittest.TestCase):
    def test_every_permutation_in_dimensions_three_four_and_five(self) -> None:
        for dimension in (3, 4, 5):
            orientation = tuple(range(dimension))
            signs: list[int] = []
            for permutation in itertools.permutations(orientation):
                expected = independent_permutation_parity(permutation)
                actual = levi_civita_sign(permutation, orientation)
                self.assertEqual(actual, expected, (dimension, permutation))
                signs.append(actual)
            self.assertEqual(len(signs), math.factorial(dimension))
            self.assertEqual(signs.count(1), math.factorial(dimension) // 2)
            self.assertEqual(signs.count(-1), math.factorial(dimension) // 2)

    def test_duplicate_indices_are_zero_in_each_control_dimension(self) -> None:
        for dimension in (3, 4, 5):
            orientation = tuple(range(dimension))
            duplicate = (0, 0) + tuple(range(2, dimension))
            self.assertEqual(len(duplicate), dimension)
            self.assertEqual(levi_civita_sign(duplicate, orientation), 0)

    def test_orientation_order_is_explicit(self) -> None:
        orientation = ('z', 'x', 'y')
        self.assertEqual(levi_civita_sign(('z', 'x', 'y'), orientation), 1)
        self.assertEqual(levi_civita_sign(('x', 'z', 'y'), orientation), -1)
        self.assertEqual(levi_civita_sign(('y', 'z', 'x'), orientation), 1)

    def test_malformed_inputs_are_rejected(self) -> None:
        orientation = (0, 1, 2)
        with self.assertRaises(TypeError):
            levi_civita_sign([0, 1, 2], orientation)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            levi_civita_sign((0, 1, 2), [0, 1, 2])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            levi_civita_sign((0, 1), orientation)
        with self.assertRaises(ValueError):
            levi_civita_sign((0, 1, 3), orientation)
        with self.assertRaises(ValueError):
            levi_civita_sign((0, 1, 2), (0, 0, 2))
        with self.assertRaises(TypeError):
            levi_civita_sign((0, 1, 2.0), orientation)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            levi_civita_sign((0, True, 2), orientation)
        with self.assertRaises(ValueError):
            levi_civita_sign((), ())

    def test_unknown_duplicate_is_invalid_not_silently_zero(self) -> None:
        with self.assertRaises(ValueError):
            levi_civita_sign((0, 9, 9), (0, 1, 2))


if __name__ == '__main__':
    unittest.main()
