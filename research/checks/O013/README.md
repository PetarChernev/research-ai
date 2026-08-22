# O013: Mixed polarization completion bridge

Canonical machine-checkable obligation for C026/D023. `spec.yaml` is the
predeclared contract, `run.py` is the claim-specific implementation, and only
the deterministic wrapper may create `result.json`.

## Exact question and boundary

The check asks whether
`B_ref=-integral_Y (omega_+-barOmega)^(AB) wedge P^(5)_AB(E)` has the
rank-three reduction, complete variation, D004 row cancellation,
coframe/reference consequences, orbit integration-by-parts signs, and
standalone infinitesimal simultaneous `SO(1,4)` covariance declared in the
specification.

It does **not** test the physical necessity of the finite tangent class, global
holonomy or winding, large gauge transformations, whether an edge mode is
gauge or physical, covariance of the complete frozen D005 theory, the full
off-polar solution of `J_C=0`, another interface action, a moving interface,
Hamiltonian preservation/closure, hyperbolicity, or C002/C003.

## Representation and trust-surface assessment

1. **Domain and coefficients.** The domain is a finite free spacetime exterior
   algebra tensored with a sparse commutative polynomial ring over exact
   `fractions.Fraction`. Formal atoms represent generic coframe,
   connection-difference, field-variation, gauge-parameter, and
   gauge-parameter-derivative components. `tau` is the exact ordinary oriented
   circle period interpreted as `2 pi`; no floating `pi` occurs.
2. **Bases/order.** Spacetime orders are
   `du0 < du1 < du2 < dtheta` for the polar trace and
   `x0 < x1 < x2 < x3` for generic boundary identities. Internal indices are
   `0,...,4`; `epsilon_01234=+1`; the metric is `diag(-,+,+,+,+)`; every
   antisymmetric pair is summed over both ordered values. Fiber forms are moved
   right before extraction.
3. **Primitive operations.** Supported operations are exact coefficient
   collection, polynomial addition/multiplication, exterior
   addition/wedge/scaling, permutation parity, antisymmetric lookup, finite
   ordered contraction, explicit momentum Leibniz differentiation, circle-leg
   extraction, and fresh-process execution.
4. **Canonical equality.** Polynomial monomials are sorted atom tuples;
   exterior monomials are sorted basis tuples with permutation sign and
   repeated-leg zero. Equality is decidable by exact tuple equality. There is no
   tolerance, randomization, sampling, or heuristic simplification.
5. **Encoded assumptions.** The implementation encodes D023's fixed rank-three
   trace, independent Palatini variations, full reference connection, D004
   positive core incidence, ordinary circle normalization, ordered pairs,
   `K=omega_+-barOmega`, `delta barOmega=-D_barOmega zeta`, and infinitesimal
   field-independent `SO(1,4)` transformations. The polar rescaling is
   rank-preserving and has a free nonzero formal coefficient.
6. **Omitted physics.** No bulk equation, quotient regularity theorem,
   distributional product, global bundle data, D005 mixed completion, edge
   classification, or canonical dynamics is represented.

### Self-contained representation versus `exact_graded`

The self-contained standard-library representation is scientifically
preferable. O013 needs only a compact polynomial/exterior subset and an explicit
generic `SO(1,4)` transformation. Reusing `exact_graded` would add its broader
field-space, map, and matrix API and the shared O002--O010 trust surface without
reducing claim-specific semantics. The local kernel keeps the equality and
tensor assumptions visible. No reusable substrate or Engineer work is used.

### Covariance rigor

The positive covariance path is a **generic exact tensor identity**, not a
finite witness and not sampling. Independent polynomial atoms are assigned to
all components of five generic coframe one-forms, ten antisymmetric `K`
one-forms, and all ten infinitesimal `so(1,4)` generators. The code builds
`P(E)`, applies the Lorentzian mixed-index transformation, and requires every
free-polynomial coefficient of `delta[-K^(AB) wedge P_AB(E)]` to vanish. This
proves the encoded infinitesimal identity in the finite tensor domain, but not
finite/large or global gauge covariance.

The transform-only-dynamical-connection control transforms the coframe but
holds `barOmega` fixed, exposing independent `-d lambda` atoms; its exact
residual must be nonzero.

### Correlated failure surfaces and alternate assembly

O012, D023, and O013 share D004 orientation, epsilon, ordered-pair, and ordinary
circle conventions, so they are correlated rather than independent evidence.
O013 separately computes `P43/P34` by a direct complement/permutation sum that
does not call the form momentum constructor. It checks all ten connection rows
rather than importing O012's `43` result and differentiates the unreduced
primitive rather than inserting its reduced variation. These controls reduce
code-path correlation but not shared assumptions or model provenance.

## Acceptance and mutation controls

Acceptance is exact canonical equality as declared in `spec.yaml`. Five
isolated mutations must each make a fresh process exit `1`: omit one
antisymmetric order; reverse the primitive sign; delete the coframe companion;
reverse the orbit-corner sign; and transform only the dynamical connection.

## Infrastructure and execution

The scientific implementation uses only Python's standard library and no
shared research computational infrastructure. Root lock/runner files declared
in `spec.yaml` are orchestration provenance, not scientific algebra.

```bash
uv run --locked python scripts/run_check.py O013
```

Exit `0/1/2` means passed/failed/inconclusive; any other exit is an execution
error. The entrypoint emits deterministic JSON observations and never writes
`result.json`.

## Interpretation

A passing outcome is exact machine evidence for the declared finite bridge
under the encoded assumptions. It is not independent verification and does not
promote C026 or a broader claim. Producer: `openai/gpt-5.6-sol`.
