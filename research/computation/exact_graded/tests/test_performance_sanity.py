from __future__ import annotations

import math
import time
import unittest

from research.computation.exact_graded import Polynomial, RationalMatrix


class DeterministicPerformanceSanityTests(unittest.TestCase):
    def test_moderate_exact_workload_completes_with_expected_sizes(self) -> None:
        start = time.monotonic()

        generators = [Polynomial.generator(f'x{index}') for index in range(4)]
        total = sum(generators, Polynomial.zero())
        expanded = total**12
        self.assertEqual(len(expanded.terms), math.comb(12 + 4 - 1, 4 - 1))
        self.assertEqual(len(expanded.differentiate('x0').terms), math.comb(11 + 4 - 1, 4 - 1))

        # A deterministic rectangular Vandermonde control: rank 10, nullity 4.
        matrix = RationalMatrix(
            [[(row + 1) ** column for column in range(14)] for row in range(10)]
        )
        self.assertEqual(matrix.rank(), 10)
        nullspace = matrix.nullspace()
        self.assertEqual(len(nullspace), 4)
        for vector in nullspace:
            self.assertEqual(matrix.matvec(vector), (0,) * 10)

        # Deliberately generous: this catches accidental explosive regressions,
        # not machine-to-machine microbenchmark variation.
        self.assertLess(time.monotonic() - start, 30.0)


if __name__ == '__main__':
    unittest.main()
