# Exact graded-algebra substrate

`exact_graded` is a small, standard-library-only kernel for exact finite
graded-algebra calculations. It is reusable methodology for the legacy
verification migration, not claim-specific evidence. Its frozen consumers are
O002, O003, and O004; those obligations must fingerprint the entire
`research/computation/exact_graded/` directory.

The package implements only the computational contract recorded in
`research/COMPUTATION.md`. Passing its tests establishes software conformance
to that contract. It does **not** establish that an encoding is scientifically
faithful, prove a physics claim, or make calculations sharing this kernel
independent of one another.

## Runtime and imports

- Python 3.11 or newer.
- Dependencies: Python standard library only (`fractions`, `dataclasses`,
  `itertools`, `json`, and standard collections/typing support).
- No random seed, floating-point precision, external executable, or
  hardware-specific setting is used.
- No research-specific environment manifest is required. The repository's
  root locked environment can invoke the tests, but remains architecture
  tooling rather than a scientific dependency stack.

The complete package-level export surface is:

```python
from research.computation.exact_graded import (
    AlgebraMismatchError,
    BasisVector,
    ExteriorAlgebra,
    ExteriorForm,
    Monomial,
    Polynomial,
    RationalMatrix,
    levi_civita_sign,
)
```

`research.computation.exact_graded._rational` is internal and is not a public
API.

## Represented domains and exact semantics

### Coefficients and polynomials

`Polynomial` represents a finite sparse element of a free commutative
multivariate polynomial ring over `fractions.Fraction`. Generator names are
nonempty strings. There is no separately declared generator universe and no
relations among generators.

A public `Monomial` is
`tuple[tuple[str, int], ...]`. During construction:

- factors are sorted lexicographically by generator name;
- repeated generator factors are combined by adding exponents;
- zero powers and zero coefficients are removed;
- terms with the same canonical monomial are collected; and
- cancelling terms disappear.

Exponents must be nonnegative built-in integers. Coefficients and exact scalar
operands must be built-in integers (excluding `bool`) or already-constructed
`fractions.Fraction` values. In particular, floats are never converted to
rationals.

Polynomial equality is equality of the canonical sparse term tuples. It uses
no assumptions, tolerance, numerical evaluation, randomized testing, or
heuristic simplification.

### Exterior forms

`ExteriorAlgebra` is declared by an explicit ordered tuple or list of unique,
nonempty string labels. An empty declaration is allowed and denotes a
scalar-only algebra. The declaration order, not lexical order, fixes wedge
signs.

An exterior monomial is a tuple of declared labels. Construction sorts it into
the declared basis order and applies the permutation sign. A repeated label
makes that term exactly zero. `ExteriorForm` is a finite sparse map from these
canonical, strictly increasing monomials to `Polynomial` coefficients; equal
monomials are collected and zero coefficients are removed.

Two independently constructed `ExteriorAlgebra` objects are compatible when
their ordered basis tuples are exactly equal. Forms over unequal declarations
are not comparable objects in one algebra: mixed operations, including form
equality, raise `AlgebraMismatchError` rather than guessing an identification.
Within one declared algebra, equality is exact canonical-map equality.

### Rational matrices

`RationalMatrix` represents an immutable, nonempty rectangular matrix over
`fractions.Fraction`. Both dimensions must be positive. Entries accept only
the same exact built-in `int`/`Fraction` inputs as polynomial coefficients.
RREF, rank, nullspace, and matrix-vector products use exact rational
arithmetic. RREF scans columns from left to right and chooses the first
available nonzero pivot row, making its output deterministic. Pivot columns
use zero-based indices. Nullspace basis vectors are ordered by ascending free
column, with that free coordinate set to one.

### Levi-Civita signs

`levi_civita_sign(indices, orientation)` computes parity relative to a
nonempty, explicit orientation tuple. Labels are built-in integers (excluding
`bool`) or nonempty strings. The orientation must contain unique labels.
Both arguments must be actual tuples rather than lists. `indices` must have the
same length and contain only orientation labels. A permutation returns `-1` or
`+1`; a valid known-label tuple with a duplicate returns `0`. Unknown labels
are errors, even when duplicated.

## Public API

### `Polynomial`

Construction and inspection:

- `Polynomial(terms=())` and `Polynomial.from_terms(terms)` accept either a
  mapping or an iterable of `(monomial, coefficient)` pairs.
- `Polynomial.zero()`, `Polynomial.one()`, and
  `Polynomial.constant(coefficient)` construct constants.
- `Polynomial.generator(name)` constructs one named generator.
- `Polynomial.monomial(powers, coefficient=1)` constructs one sparse term.
- `.terms` is the canonical tuple of `(Monomial, Fraction)` terms.
- `.generators` is the sorted tuple of generator names actually present.
- `.is_zero` and `.is_constant` report exact canonical properties.
- `.coefficient(monomial)` canonicalizes the requested monomial and returns
  its `Fraction` coefficient, or zero when absent.

Operations:

- `+`, `-`, unary `-`, and `*` support polynomials and exact rational scalars.
- `polynomial ** exponent` supports nonnegative built-in integer powers;
  exponent zero returns one, including `Polynomial.zero() ** 0`.
- `.differentiate(generator)` performs formal polynomial differentiation.
- `.substitute(replacements)` performs **simultaneous**, nonrecursive
  substitution from generator names to `Polynomial`, `int`, or `Fraction`.
  Replacement polynomials are inserted unchanged rather than being processed
  by other entries in the same mapping. Unmapped generators remain formal;
  extra mapping entries have no effect.
- `/` is deliberately unavailable, including division by a rational scalar.
  Construct an exact `Fraction` coefficient and multiply instead.

Canonical output:

- `.to_data()` returns the canonical JSON-compatible data tree.
- `.serialize()` returns compact deterministic JSON with sorted object keys,
  ASCII escaping, monomials in canonical order, and every rational as
  `[numerator, denominator]`.
- Equality, hashing, truth testing, and `repr` use the canonical value; only
  zero is false.

### `ExteriorAlgebra`

- `ExteriorAlgebra(basis)` declares the ordered basis. A set or other
  unordered container is rejected.
- `.basis` returns the immutable ordered basis tuple.
- `.zero()`, `.unit()`, and `.scalar(coefficient)` construct forms of degree
  zero.
- `.basis_form(label)` constructs one declared basis one-form.
- `.basis_vector(label)` constructs the declared vector dual to that named
  one-form.
- `.from_terms(terms)` constructs an `ExteriorForm` from a mapping or iterable
  of `(tuple_of_basis_labels, coefficient)` pairs.
- `.field_derivative(form, coordinate_to_differential)` is the algebra-level
  spelling of `form.field_derivative(...)` described below.
- Algebra equality, hashing, and `repr` depend only on the ordered basis tuple.

### `ExteriorForm`

`ExteriorForm(algebra, terms=())` is public, although
`algebra.from_terms(...)` is normally clearer.

- `.algebra`, `.terms`, `.is_zero`, and `.degrees` expose the declared algebra,
  canonical terms, exact zero status, and the sorted tuple of degrees present.
- `+`, `-`, and unary `-` act only on forms over a matching algebra.
- `.scale(scalar)`, `form * scalar`, and `scalar * form` multiply by a
  `Polynomial`, `int`, or `Fraction` exactly.
- `.wedge(other)` is the only form product. `form * other_form` is rejected so
  that wedge multiplication cannot be implicit.
- `.pullback(target, generator_map)` extends an explicit one-form generator map
  as described under **Pullback convention**.
- `.contract(vector)` performs left contraction as described under
  **Contraction convention**.
- `.field_derivative(coordinate_to_differential)` applies the restricted
  field-space derivative described under **Field-derivative convention**.
- `.to_data()` and `.serialize()` emit canonical data/JSON; equality, truth
  testing, and `repr` use the canonical value. Exterior forms are not hashable.

### `BasisVector` and `AlgebraMismatchError`

`BasisVector(algebra, label)` is an immutable declaration of the basis vector
dual to one named basis one-form. Prefer `algebra.basis_vector(label)`. It is
not a metric-raised one-form and does not represent arbitrary linear
combinations.

`AlgebraMismatchError` is a `ValueError` subclass raised when forms or declared
vectors use unequal ordered exterior bases.

### `RationalMatrix`

- `RationalMatrix(rows)` accepts a nonempty tuple/list of equal-length,
  nonempty tuple/list rows.
- `.rows`, `.nrows`, `.ncols`, and `.shape` expose immutable exact data and
  dimensions.
- `.rref()` returns `(reduced_matrix, pivot_columns)`.
- `.rank()` returns the exact rank.
- `.nullspace()` returns a deterministic tuple of exact rational basis vectors.
- `.matvec(vector)` multiplies by an exact tuple/list vector of matching length.
- `.to_data()` and `.serialize()` emit canonical data/JSON; equality and
  `repr` use exact matrix entries.

### `levi_civita_sign`

`levi_civita_sign(indices, orientation) -> int` returns `-1`, `0`, or `+1`
under the explicit-orientation rules above. It performs no metric operation,
index raising, or Hodge conversion.

## Map and sign conventions

### Simultaneous substitution

For `p.substitute({"x": q, "y": r})`, every occurrence in the original `p`
is replaced at once. Symbols occurring inside `q` or `r` are not replaced
again. This distinguishes simultaneous substitution from sequential rewriting.

### Pullback convention

For `source_form.pullback(target, generator_map)`, `source_form.algebra` is the
source algebra and every source basis generator must occur exactly as a key in
`generator_map`; unknown keys are rejected, even if a source generator is
unused by that particular form. Each image must be `target.zero()` or a
homogeneous degree-one `ExteriorForm` over `target`. Use `target.zero()` rather
than numeric zero for a vanishing image.

The map is extended in source monomial order by wedge multiplication. Original
polynomial coefficients are carried through unchanged; pullback does not also
perform polynomial substitution. Degree-one images may themselves have exact
polynomial coefficients.

### Left-contraction convention

For a canonical monomial
`e[0] wedge ... wedge e[k-1]`, contraction by the declared vector dual to
`e[j]` removes that leg with sign `(-1) ** j`, where `j` is zero-based. A
missing leg contributes zero. Coefficients are unchanged. Only declared basis
vectors are accepted; there is no implicit metric, index raising, or generic
vector expression.

### Field-derivative convention

`coordinate_to_differential` maps polynomial generator names to zero or
homogeneous degree-one forms in the same exterior algebra. Every image must
have constant polynomial coefficients. The mapping must include every
polynomial generator occurring in the input form's coefficients; extra entries
are allowed but validated. A symbol intended as a constant parameter must
therefore be mapped explicitly to `algebra.zero()` whenever it occurs.

The mapping declares `d_F(x)`. Rational constants and the algebra's basis
one-forms are closed. On a canonical term `f * omega`, the implementation is

```text
d_F(f * omega) = sum_x d_F(x) wedge omega * (partial f / partial x).
```

Thus differential images are placed on the left, and the operation extends
termwise to inhomogeneous forms. Nonconstant or higher-degree differential
images, missing coordinate declarations, and differentiation rules for basis
legs are outside this restricted API.

## Deterministic serialization

The three value types serialize as compact JSON:

- polynomials record `type`, canonical `terms`, monomial
  `[generator, exponent]` pairs, and rational `[numerator, denominator]` pairs;
- exterior forms additionally record the complete ordered `basis`, canonical
  exterior monomials, and nested polynomial coefficient data; and
- matrices record `type`, `[nrows, ncols]` shape, and row-major rational data.

Equivalent construction histories produce identical serialization. There is
no parser or `from_data` API: serialization is an auditable deterministic
output, not a general persistence or untrusted-input format. The schema is not
independently versioned; dependent obligations fingerprint the entire kernel
directory so any implementation or documentation change invalidates an older
infrastructure fingerprint.

## Rejected and unsupported inputs

The kernel rejects rather than guesses:

- floats, complex numbers, `Decimal`, booleans, strings used as numbers, and
  arbitrary numeric/coefficient objects;
- negative or non-integer polynomial exponents, modular powers, and all
  symbolic division;
- empty generator/basis labels, duplicate exterior basis declarations,
  unordered basis containers, unknown exterior labels, and malformed sparse
  terms;
- operations across unequal ordered exterior bases;
- incomplete/overcomplete pullback maps, non-form pullback images, images over
  the wrong target basis, and nonzero images outside degree one;
- incomplete or non-mapping field-derivative declarations, images over the
  wrong algebra, nonconstant images, and nonzero images outside degree one;
- empty, zero-column, ragged, iterator-backed, or non-rational matrices, and
  matrix-vector dimension mismatches; and
- empty/duplicate orientations, wrong-length index tuples, unknown indices,
  and malformed Levi-Civita labels.

Exact exterior coefficient systems are fixed to the polynomial ring over
rationals. Alternate coefficient systems, quotient rings, zero divisors, and
implicit algebraic relations are unsupported. Numerical matrices and tolerance
comparisons are unsupported; there is no NumPy-array coercion or approximate
linear algebra.

## Limitations and non-goals

The intentionally small API does not provide:

- smooth germs, limits, asymptotics, topology, quotient topology, or
  diffeology;
- tensor/index automation, a metric, index raising, Hodge-star conventions, or
  automatic Einstein summation;
- arbitrary vector fields, general connections, or a general exterior
  derivative on basis forms;
- coefficient-ring maps combined with pullback;
- symbolic division, rational functions, alternate/zero-divisor coefficient
  systems, factorization, or Groebner bases;
- matrix determinants, minors, inverses, matrix-matrix arithmetic, or numerical
  linear algebra beyond the explicit exact API above;
- gauge-group solving, theorem proving, Markdown parsing, or untrusted-data
  deserialization; or
- any D006 canonical/presymplectic work.

The finite sparse representation checks only identities encoded in a declared
finite algebra. It cannot establish statements quantified over arbitrary
smooth fields or global geometric objects. Performance tests are regression
sanity checks, not a large-problem scalability guarantee.

## Infrastructure tests

From the repository root, run:

```bash
uv run --locked python -m unittest discover -s research/computation/exact_graded/tests -t . -v
```

The suite covers coefficient collection; wedge bilinearity, associativity,
graded commutativity, and repeated-leg zero; `d_F^2 = 0` and graded
Leibniz; pullback identity, composition, and wedge compatibility; left
contraction signs; every Levi-Civita permutation in dimensions 3, 4, and 5 plus
duplicate-index zero; exact full/deficient rank and nullspace controls;
deterministic serialization; required invalid-input rejection; and one generous
deterministic performance sanity bound. These are infrastructure tests, not
O002/O003/O004 executions or scientific verification.

Recorded infrastructure run for this documentation repair (2026-08-20,
Python 3.12.12): the exact command above ran 45 tests in 0.027 seconds and
reported `OK`.
