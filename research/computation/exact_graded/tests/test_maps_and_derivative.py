from __future__ import annotations

import unittest

from research.computation.exact_graded import (
    AlgebraMismatchError,
    ExteriorAlgebra,
    Polynomial,
)


class FieldDerivativeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.algebra = ExteriorAlgebra(('dq', 'dr', 'ds', 'dt'))
        self.dq, self.dr, self.ds, self.dt = (
            self.algebra.basis_form(label) for label in self.algebra.basis
        )
        self.q = Polynomial.generator('q')
        self.r = Polynomial.generator('r')
        self.s = Polynomial.generator('s')
        self.mapping = {'q': self.dq, 'r': self.dr, 's': self.ds}

    def test_field_derivative_squares_to_zero_on_nontrivial_inhomogeneous_form(self) -> None:
        form = (
            self.algebra.scalar(self.q * self.r * self.s)
            + self.dr.scale(self.q * self.r + self.s**2)
            + self.dq.wedge(self.ds).scale(self.q**2 * self.r)
        )
        first = form.field_derivative(self.mapping)
        self.assertFalse(first.is_zero)
        self.assertEqual(first.field_derivative(self.mapping), self.algebra.zero())

    def test_graded_leibniz_rule_on_nontrivial_forms(self) -> None:
        alpha = self.dr.scale(self.q) + self.ds.scale(self.r)  # degree one
        beta = (
            self.dq.wedge(self.dt).scale(self.s)
            + self.dr.wedge(self.dt).scale(self.q)
        )  # degree two

        d_alpha = alpha.field_derivative(self.mapping)
        d_beta = beta.field_derivative(self.mapping)
        left = alpha.wedge(beta).field_derivative(self.mapping)
        right = d_alpha.wedge(beta) - alpha.wedge(d_beta)
        self.assertFalse(d_alpha.is_zero)
        self.assertFalse(d_beta.is_zero)
        self.assertFalse(left.is_zero)
        self.assertEqual(left, right)

    def test_explicit_zero_differential_and_constant_form(self) -> None:
        x = Polynomial.generator('x')
        scalar = self.algebra.scalar(x**3 + 2)
        self.assertEqual(scalar.field_derivative({'x': self.algebra.zero()}), self.algebra.zero())
        self.assertEqual(self.algebra.scalar(5).field_derivative({}), self.algebra.zero())

    def test_derivative_map_validation(self) -> None:
        form = self.algebra.scalar(self.q * self.r)
        with self.assertRaises(ValueError):
            form.field_derivative({'q': self.dq})
        with self.assertRaises(TypeError):
            form.field_derivative([('q', self.dq), ('r', self.dr)])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            form.field_derivative({'q': self.dq, 'r': 0})  # type: ignore[dict-item]
        with self.assertRaises(TypeError):
            form.field_derivative({1.0: self.dq, 'q': self.dq, 'r': self.dr})  # type: ignore[dict-item]

        other = ExteriorAlgebra(('du', 'dv'))
        with self.assertRaises(AlgebraMismatchError):
            form.field_derivative({'q': self.dq, 'r': other.basis_form('du')})
        with self.assertRaises(ValueError):
            form.field_derivative({'q': self.dq.wedge(self.dr), 'r': self.dr})
        with self.assertRaises(ValueError):
            form.field_derivative({'q': self.dq.scale(self.q), 'r': self.dr})


class PullbackTests(unittest.TestCase):
    def test_identity_pullback(self) -> None:
        source = ExteriorAlgebra(('a', 'b', 'c'))
        target = ExteriorAlgebra(('a', 'b', 'c'))
        x = Polynomial.generator('x')
        form = source.scalar(x + 1) + source.basis_form('a').wedge(source.basis_form('c')).scale(x)
        identity = {label: target.basis_form(label) for label in source.basis}
        expected = target.scalar(x + 1) + target.basis_form('a').wedge(target.basis_form('c')).scale(x)
        self.assertEqual(form.pullback(target, identity), expected)

    def test_pullback_wedge_compatibility_including_zero_image(self) -> None:
        source = ExteriorAlgebra(('a', 'b', 'c'))
        target = ExteriorAlgebra(('u', 'v', 'w'))
        a, b, c = (source.basis_form(label) for label in source.basis)
        u, v, w = (target.basis_form(label) for label in target.basis)
        mapping = {'a': u + v, 'b': v - w, 'c': target.zero()}
        alpha = a + 2 * b
        beta = b + c

        self.assertEqual(
            alpha.wedge(beta).pullback(target, mapping),
            alpha.pullback(target, mapping).wedge(beta.pullback(target, mapping)),
        )

    def test_pullback_composition_functoriality(self) -> None:
        source = ExteriorAlgebra(('a', 'b', 'c'))
        middle = ExteriorAlgebra(('u', 'v', 'w'))
        target = ExteriorAlgebra(('r', 's', 't'))
        a, b, c = (source.basis_form(label) for label in source.basis)
        u, v, w = (middle.basis_form(label) for label in middle.basis)
        r, s, t = (target.basis_form(label) for label in target.basis)

        first_map = {'a': u + v, 'b': v - w, 'c': 2 * u + w}
        second_map = {'u': r, 'v': s + t, 'w': r - t}
        composite_map = {
            label: image.pullback(target, second_map)
            for label, image in first_map.items()
        }
        form = a.wedge(b) + 3 * b.wedge(c) + 2 * a

        staged = form.pullback(middle, first_map).pullback(target, second_map)
        direct = form.pullback(target, composite_map)
        self.assertEqual(staged, direct)

    def test_pullback_map_rejects_incomplete_unknown_and_ill_typed_entries(self) -> None:
        source = ExteriorAlgebra(('a', 'b'))
        target = ExteriorAlgebra(('u', 'v'))
        other = ExteriorAlgebra(('r', 's'))
        form = source.basis_form('a') + source.basis_form('b')
        u, v = (target.basis_form(label) for label in target.basis)

        with self.assertRaises(ValueError):
            form.pullback(target, {'a': u})
        with self.assertRaises(ValueError):
            form.pullback(target, {'a': u, 'b': v, 'extra': u})
        with self.assertRaises(TypeError):
            form.pullback(target, {'a': u, 'b': 0})  # type: ignore[dict-item]
        with self.assertRaises(AlgebraMismatchError):
            form.pullback(target, {'a': u, 'b': other.basis_form('r')})
        with self.assertRaises(ValueError):
            form.pullback(target, {'a': u.wedge(v), 'b': v})
        with self.assertRaises(TypeError):
            form.pullback(target, [('a', u), ('b', v)])  # type: ignore[arg-type]


if __name__ == '__main__':
    unittest.main()
