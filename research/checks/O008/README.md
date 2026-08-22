# O008: Duplicated-trace primary reduction bridge

Canonical machine-checkable obligation for claims C018-C020 and derivations
D015-D017. `spec.yaml` is the declaration, `run.py` is the claim-specific exact
implementation, and `result.json` is written **only** by the deterministic
runner.

## Question and boundary

O008 tests the frozen finite bridge: formal gluing-coefficient elimination; all
tangential 5D Palatini `P_AB` and `dP_AB` rows at regular collapse; the complete
D005 shell-potential pullback; and the exterior Palatini defining reduction,
including ranks, null certificates, every coordinate row complement, the
coadjoint residual, separate `g` zero rows, and nonidentity matching tangency.

It does **not** prove that continuum trace maps or lifts exist, that local trace
surjectivity holds, or that the clean shell extends globally. It introduces no
functional trace adjoint, distributional bracket, or collar regularization. It
does not perform first preservation, test the mixed `SO(1,4)` truncation,
construct a total Hamiltonian, classify null directions, or establish a
physical degree count.

## Assumptions and conventions

The interface is fixed and planar. One-sided persistent trace maps are assumed
fixed, gauge equivariant, continuous, and locally trace-surjective; the
gluing/matching sector is assumed clean and constant rank. The regular equalizer
has `E4=rho eta`, with `rho=delta rho=0` and all admissible collapsed/circle-
vertical tangent coefficients zero at the cut. No profile division is allowed.

Orientations are `epsilon_01234=epsilon_0123=+1`; the Lorentz metric is
`diag(-,+,+,+)` and pair order is `(01,02,03,12,13,23)`. Spatial forms use
`dx1<dx2<ds`, with `dtheta` last. The exterior coframe is the nondegenerate
adapted triad `e1=dx1,e2=dx2,e3=ds,e0=0`; its cut pullback is planar. The
incidence `I_C` retains the `dx1 wedge dx2` coefficient of each Lorentz row.
The fixed-seed shell is `lambda=-Q`, `Q=g.P`, with no independent seed/corner
potential. Normal contraction by `partial_s` is never identified with circle
pushforward. Lorentz parameters are proper at temporal/lateral outer corners.

## Exact method and acceptance

The runner uses finite exterior algebra, exact Lorentz adjoint/coadjoint maps,
and rational matrices. It passes iff every assertion in `spec.yaml` holds and
each required semantic mutation is detected by its targeted assertion. There
are no thresholds, precision settings, random samples, floats, or heuristic CAS
simplifications. Unsupported declared exact-domain input is inconclusive;
scientific mismatch fails; malformed execution is an error.

## Representation and trust-surface assessment

- **Domains.** Formal gluing coefficients with named trace maps, finite 4D/5D
  exterior forms, six-component Lorentz bivectors, and exact rational primary
  matrices. A continuum trace operator is deliberately not represented.
- **Coefficients and bases.** `Fraction` is the coefficient field. Exterior
  monomials canonicalize in caller-declared order. `A` has 18 rows ordered by
  Lorentz pair and `(dx1dx2,dx1ds,dx2ds)`, and 12 columns ordered by spatial
  direction and internal index. Equality is canonical sparse-map or exact
  entrywise equality.
- **Primitives.** Ordered epsilon sums, wedge/pullback/contraction, coefficient
  extraction, exact one-slot differentiation, Lorentz bracket/dressing,
  rational row reduction/inversion, finite incidence, and block assembly.
- **Adequacy.** `exact_graded` was assessed rather than presumed: its tested
  exterior, epsilon, rank, and nullspace semantics cover the reusable portion.
  Claim-local multiplication, inversion, incidence, dressing, complement
  enumeration, and mutations are short and auditable. No reusable substrate or
  environment dependency is missing; Engineer was not invoked.
- **Trust and shared failures.** The trusted surface is Python `Fraction`, the
  fingerprinted `exact_graded` package, and this runner. O008 shares D004-D006
  conventions and infrastructure with O005-O007, so agreement is correlated.
  It cannot validate trace existence/surjectivity or clean-shell assumptions.
- **Alternate assembly.** Primary `A` is built from the actual Palatini coframe
  and independently from a dense two-letter wedge table that does not call the
  sparse assembly helper. All `C(18,12)=18564` row subsets are enumerated and
  every invertible complement checked. A separate dense/direct block product
  establishes the unmutated Schur zero without using the complement-loop result
  as its oracle.

## Infrastructure and provenance

Fingerprint paths declared in `spec.yaml` are
`research/computation/exact_graded`, `pyproject.toml`, `uv.lock`,
`scripts/_research.py`, and `scripts/run_check.py`. The root locked Python
environment and standard library suffice; no research environment manifest was
added. Producer and material infrastructure producer model:
`openai/gpt-5.6-sol`.

## How to run canonically

```bash
uv run --locked python scripts/run_check.py O008
```

The wrapper maps exit `0/1/2` to passed/failed/inconclusive; any other exit is
an error. Never write or edit `result.json` by hand.

## Development self-checks

Direct locked-runtime diagnostics on 2026-08-22, without the canonical wrapper,
gave:

- unmutated runner: exit `0`, all 51 assertions passed; 18,564 subsets were
  visited, 8 were admissible complements, and all 8 had zero Schur correction;
- `exterior-incidence-sign`: exit `1` at `gluing.Bminus_equals_minus_P`;
- `shell-potential-sign`: exit `1` at the pure-`g` kernel assertion;
- `delete-frame-commutator`: exit `1` at the exhaustive nonidentity matching-
  tangency basis assertion;
- `connection-half-coupling`: exit `1`; all 8 admissible complements acquired
  nonzero Schur correction;
- `exact_graded` infrastructure suite: 45 tests passed (`OK`).

Repository-state validation was also invoked and failed only on pre-existing
out-of-scope D016/D017 critique timestamp/section errors; it additionally gave
the expected warning that active O008 has no `result.json`. These diagnostics do
not create a canonical outcome.

## Result and interpretation

No result is recorded. Absence of `result.json` means O008 has not run through
the canonical wrapper.

A future passing result would support only the encoded finite coefficient,
trace-table, shell-potential, rank, Schur, nullspace, and tangency assertions
under the assumptions above. It would not promote C018-C020 to verified. First
preservation remains blocked on a functional trace pairing/adjoint, a boundary-
compatible background, and a total Hamiltonian.
