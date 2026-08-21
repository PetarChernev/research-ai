from __future__ import annotations

import json
import unittest
from fractions import Fraction

from research.computation.exact_graded import (
    AlgebraMismatchError,
    ExteriorAlgebra,
    Polynomial,
)


class ExteriorConstructionTests(unittest.TestCase):
    def test_basis_ordering_collection_and_repeated_leg_zero(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy', 'dz'))
        dx = algebra.basis_form('dx')
        dy = algebra.basis_form('dy')

        self.assertEqual(algebra.from_terms([(('dy', 'dx'), 1)]), -dx.wedge(dy))
        self.assertEqual(
            algebra.from_terms([(('dy', 'dx'), 2), (('dx', 'dy'), 2)]),
            algebra.zero(),
        )
        self.assertEqual(algebra.from_terms([(('dx', 'dx'), 9)]), algebra.zero())
        self.assertEqual(dx.wedge(dx), algebra.zero())

    def test_zero_scalar_unit_and_polynomial_scaling(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy'))
        x = Polynomial.generator('x')
        dx = algebra.basis_form('dx')
        self.assertEqual(algebra.scalar(0), algebra.zero())
        self.assertEqual(algebra.unit().wedge(dx), dx)
        self.assertEqual(dx.scale(x + Fraction(1, 2)), (x + Fraction(1, 2)) * dx)
        self.assertEqual(dx * 3, 3 * dx)

    def test_empty_basis_is_scalar_only(self) -> None:
        algebra = ExteriorAlgebra(())
        self.assertEqual(algebra.unit().wedge(algebra.scalar(2)), algebra.scalar(2))
        with self.assertRaises(ValueError):
            algebra.basis_form('missing')

    def test_duplicate_and_malformed_basis_rejection(self) -> None:
        with self.assertRaises(ValueError):
            ExteriorAlgebra(('dx', 'dx'))
        with self.assertRaises(TypeError):
            ExteriorAlgebra({'dx', 'dy'})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ExteriorAlgebra(('dx', 1.0))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ExteriorAlgebra(('dx',)).from_terms([(('unknown',), 1)])
        with self.assertRaises(TypeError):
            ExteriorAlgebra(('dx',)).from_terms([(('dx', 'dx'), 0.5)])


class ExteriorAlgebraLawTests(unittest.TestCase):
    def setUp(self) -> None:
        self.algebra = ExteriorAlgebra(('e0', 'e1', 'e2', 'e3', 'e4'))
        self.e = [self.algebra.basis_form(label) for label in self.algebra.basis]

    def test_wedge_bilinearity(self) -> None:
        alpha = 2 * self.e[0] - self.e[2]
        beta = self.e[1] + 3 * self.e[3]
        gamma = self.e[2] - 2 * self.e[4]
        self.assertEqual(
            (alpha + beta).wedge(gamma),
            alpha.wedge(gamma) + beta.wedge(gamma),
        )
        self.assertEqual(
            gamma.wedge(alpha + beta),
            gamma.wedge(alpha) + gamma.wedge(beta),
        )

    def test_wedge_associativity(self) -> None:
        alpha = self.e[0] + 2 * self.e[1]
        beta = self.e[2] - self.e[3]
        gamma = self.e[1] + self.e[4]
        self.assertEqual(
            alpha.wedge(beta).wedge(gamma),
            alpha.wedge(beta.wedge(gamma)),
        )

    def test_graded_commutativity_for_nontrivial_homogeneous_forms(self) -> None:
        one_a = self.e[0] + self.e[1]
        one_b = self.e[2] - 2 * self.e[3]
        two_a = self.e[0].wedge(self.e[2]) + self.e[1].wedge(self.e[4])
        two_b = self.e[1].wedge(self.e[3]) - self.e[2].wedge(self.e[4])

        self.assertEqual(one_a.wedge(one_b), -one_b.wedge(one_a))
        self.assertEqual(two_a.wedge(one_b), one_b.wedge(two_a))
        self.assertEqual(two_a.wedge(two_b), two_b.wedge(two_a))

    def test_basis_mismatch_is_rejected_but_equal_declarations_are_compatible(self) -> None:
        same = ExteriorAlgebra(tuple(self.algebra.basis))
        reordered = ExteriorAlgebra(('e1', 'e0', 'e2', 'e3', 'e4'))
        self.assertEqual(self.e[0] + same.basis_form('e0'), 2 * self.e[0])

        with self.assertRaises(AlgebraMismatchError):
            _ = self.e[0] + reordered.basis_form('e0')
        with self.assertRaises(AlgebraMismatchError):
            self.e[0].wedge(reordered.basis_form('e0'))
        with self.assertRaises(AlgebraMismatchError):
            _ = self.e[0] == reordered.basis_form('e0')

    def test_no_implicit_form_product_or_inexact_scalar(self) -> None:
        with self.assertRaises(TypeError):
            _ = self.e[0] * self.e[1]
        with self.assertRaises(TypeError):
            _ = self.e[0] * 0.5


class ExteriorContractionAndSerializationTests(unittest.TestCase):
    def test_left_contraction_signs(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy', 'dz'))
        dx, dy, dz = (algebra.basis_form(label) for label in algebra.basis)
        volume = dx.wedge(dy).wedge(dz)
        self.assertEqual(volume.contract(algebra.basis_vector('dx')), dy.wedge(dz))
        self.assertEqual(volume.contract(algebra.basis_vector('dy')), -dx.wedge(dz))
        self.assertEqual(volume.contract(algebra.basis_vector('dz')), dx.wedge(dy))

    def test_contraction_antiderivation_identity(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy', 'dz', 'dw'))
        dx, dy, dz, dw = (algebra.basis_form(label) for label in algebra.basis)
        x = Polynomial.generator('x')
        alpha = dx.scale(x) + 2 * dy  # homogeneous degree one
        beta = dy.wedge(dz) + 3 * dx.wedge(dw)  # homogeneous degree two
        vector = algebra.basis_vector('dy')

        left = alpha.wedge(beta).contract(vector)
        right = alpha.contract(vector).wedge(beta) - alpha.wedge(beta.contract(vector))
        self.assertFalse(left.is_zero)
        self.assertEqual(left, right)

    def test_contraction_requires_a_matching_declared_vector(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy'))
        other = ExteriorAlgebra(('du', 'dv'))
        with self.assertRaises(TypeError):
            algebra.basis_form('dx').contract('dx')  # type: ignore[arg-type]
        with self.assertRaises(AlgebraMismatchError):
            algebra.basis_form('dx').contract(other.basis_vector('du'))
        with self.assertRaises(ValueError):
            algebra.basis_vector('missing')

    def test_form_serialization_is_canonical_and_auditable(self) -> None:
        algebra = ExteriorAlgebra(('dx', 'dy', 'dz'))
        x = Polynomial.generator('x')
        first = algebra.from_terms(
            [
                (('dy', 'dx'), -x),
                ((), Fraction(1, 2)),
                (('dz',), 2),
            ]
        )
        second = algebra.from_terms(
            [
                (('dx', 'dy'), x),
                (('dz',), 1),
                ((), Fraction(2, 4)),
                (('dz',), 1),
            ]
        )
        self.assertEqual(first, second)
        self.assertEqual(first.serialize(), second.serialize())
        data = json.loads(first.serialize())
        self.assertEqual(data['basis'], ['dx', 'dy', 'dz'])
        self.assertEqual([term['monomial'] for term in data['terms']], [[], ['dx', 'dy'], ['dz']])
        self.assertEqual(data['terms'][1]['coefficient']['terms'][0]['monomial'], [['x', 1]])


if __name__ == '__main__':
    unittest.main()
