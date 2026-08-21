from __future__ import annotations

import json
import unittest
from decimal import Decimal
from fractions import Fraction

from research.computation.exact_graded import Polynomial


class PolynomialConstructionTests(unittest.TestCase):
    def test_collection_canonicalization_and_cancellation(self) -> None:
        polynomial = Polynomial.from_terms(
            [
                ((('y', 1), ('x', 1), ('x', 1)), Fraction(3, 2)),
                ((('x', 2), ('y', 1)), Fraction(-1, 2)),
                ((('z', 0),), 4),
                ((), -4),
            ]
        )
        self.assertEqual(
            polynomial,
            Polynomial.monomial((('x', 2), ('y', 1))),
        )
        self.assertEqual(polynomial.terms, (((('x', 2), ('y', 1)), Fraction(1)),))

        cancelled = Polynomial.from_terms(
            [
                ((('x', 1),), Fraction(7, 5)),
                ((('x', 1),), Fraction(-7, 5)),
            ]
        )
        self.assertTrue(cancelled.is_zero)
        self.assertEqual(cancelled.terms, ())

    def test_constants_generators_and_coefficients(self) -> None:
        x = Polynomial.generator('x')
        self.assertEqual(Polynomial.zero() + x, x)
        self.assertEqual(Polynomial.one(), Polynomial.constant(Fraction(1)))
        self.assertEqual(x.generators, ('x',))
        self.assertEqual(x.coefficient((('x', 1),)), Fraction(1))
        self.assertEqual(x.coefficient((('missing', 1),)), Fraction(0))
        self.assertTrue(Polynomial.zero().is_constant)
        self.assertTrue(Polynomial.constant(3).is_constant)
        self.assertFalse(x.is_constant)

    def test_sparse_mapping_constructor(self) -> None:
        polynomial = Polynomial.from_terms(
            {
                (('b', 1), ('a', 2)): Fraction(2, 3),
                (): -1,
            }
        )
        self.assertEqual(
            polynomial,
            Fraction(2, 3) * Polynomial.generator('a') ** 2 * Polynomial.generator('b') - 1,
        )


class PolynomialOperationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.x = Polynomial.generator('x')
        self.y = Polynomial.generator('y')

    def test_arithmetic_and_exact_scalars(self) -> None:
        identity = (self.x + self.y) * (self.x - self.y)
        self.assertEqual(identity, self.x**2 - self.y**2)
        self.assertEqual(-(-identity), identity)
        self.assertEqual(Fraction(3, 2) * self.x, self.x * Fraction(3, 2))
        self.assertEqual(2 + self.x, self.x + 2)
        self.assertEqual(2 - self.x, -(self.x - 2))

    def test_differentiation(self) -> None:
        polynomial = Fraction(3, 2) * self.x**3 * self.y - 2 * self.y + 7
        self.assertEqual(
            polynomial.differentiate('x'),
            Fraction(9, 2) * self.x**2 * self.y,
        )
        self.assertEqual(
            polynomial.differentiate('y'),
            Fraction(3, 2) * self.x**3 - 2,
        )
        self.assertEqual(polynomial.differentiate('unused'), Polynomial.zero())

    def test_simultaneous_substitution_is_not_recursive(self) -> None:
        polynomial = self.x * self.y + self.x
        substituted = polynomial.substitute({'x': self.y + 1, 'y': 2})
        self.assertEqual(substituted, 3 * (self.y + 1))
        self.assertNotEqual(substituted, Polynomial.constant(9))

        rational_substitution = (self.x**2 + self.y).substitute(
            {'x': Fraction(1, 2), 'y': Fraction(3, 4)}
        )
        self.assertEqual(rational_substitution, Polynomial.constant(1))

    def test_nonnegative_power_edge_cases(self) -> None:
        self.assertEqual((self.x + 1) ** 0, Polynomial.one())
        self.assertEqual(Polynomial.zero() ** 0, Polynomial.one())
        self.assertEqual(Polynomial.zero() ** 4, Polynomial.zero())
        self.assertEqual((self.x + 1) ** 1, self.x + 1)
        self.assertEqual((self.x + 1) ** 3, self.x**3 + 3 * self.x**2 + 3 * self.x + 1)


class PolynomialRejectionAndSerializationTests(unittest.TestCase):
    def test_rejects_nonexact_coefficients_and_float_arithmetic(self) -> None:
        x = Polynomial.generator('x')
        for value in (0.5, True, Decimal('0.5'), '1/2'):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    Polynomial.constant(value)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            _ = x + 0.25
        with self.assertRaises(TypeError):
            _ = x * 0.25
        with self.assertRaises(TypeError):
            x.substitute({'x': 0.25})  # type: ignore[dict-item]

    def test_rejects_invalid_generators_monomials_and_exponents(self) -> None:
        with self.assertRaises(TypeError):
            Polynomial.generator(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            Polynomial.generator('')
        with self.assertRaises(TypeError):
            Polynomial.monomial([('x', 1)])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            Polynomial.monomial((('x', 1.0),))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            Polynomial.monomial((('x', -1),))
        with self.assertRaises(TypeError):
            _ = Polynomial.generator('x') ** Fraction(2)
        with self.assertRaises(ValueError):
            _ = Polynomial.generator('x') ** -1
        with self.assertRaises(TypeError):
            pow(Polynomial.generator('x'), 2, 3)

    def test_rejects_symbolic_division_and_ambiguous_substitution(self) -> None:
        x = Polynomial.generator('x')
        with self.assertRaises(TypeError):
            _ = x / 2
        with self.assertRaises(TypeError):
            _ = 2 / x
        with self.assertRaises(TypeError):
            x.substitute([('x', 2)])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            Polynomial.from_terms('not sparse terms')

    def test_serialization_is_canonical_and_deterministic(self) -> None:
        first = Polynomial.from_terms(
            [
                ((('y', 1), ('x', 2)), Fraction(1, 3)),
                ((), -2),
            ]
        )
        second = Polynomial.from_terms(
            [
                ((), -1),
                ((('x', 2), ('y', 1)), Fraction(2, 3)),
                ((('x', 2), ('y', 1)), Fraction(-1, 3)),
                ((), -1),
            ]
        )
        self.assertEqual(first, second)
        self.assertEqual(first.serialize(), second.serialize())
        self.assertEqual(first.serialize(), first.serialize())
        data = json.loads(first.serialize())
        self.assertEqual(data['type'], 'polynomial')
        self.assertEqual(data['terms'][0]['monomial'], [])
        self.assertEqual(data['terms'][1]['monomial'], [['x', 2], ['y', 1]])
        self.assertEqual(data['terms'][1]['coefficient'], [1, 3])


if __name__ == '__main__':
    unittest.main()
