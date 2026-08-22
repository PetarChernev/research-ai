# O011: Inverse-source stress and NEC bridge

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C023

Derivations: D020

## Question tested

Under the C023/D020 common-warp, zero-spin-current conventions, do exact Lorentzian curvature contractions, exact differentiation of both D002 profiles, formal flat-germ order bookkeeping, and absolute-volume identities reproduce the claimed unbounded orthonormal curvature/stress, componentwise local L1 stress, and two-channel NEC violation near s=0?

## What this does not test

This obligation does not prove the analytic theorem that a smooth-flat zero
extension has arbitrary vanishing order, quantify over profiles other than the
two exact D002 choices, construct a covariant matter action, test source-field
dynamics, define a distribution at the endpoint, or address torsion/spin,
anisotropic/off-diagonal geometry, moving interfaces, alternative actions,
weaker regularity, broad C002/C003, or independent verification.

## Assumptions encoded in the implementation

- The geometry, signature, curvature convention, positive `kappa_5`, finite
  `Lambda_5`, and zero-spin-current torsion-free connection are exactly those
  declared in D020 and `spec.yaml`.
- `rho=ell exp[-(L/s)^nu]` with `nu=2,4` and positive `ell,L,s`; arbitrary-order
  flatness of `w-1` is an encoded analytic premise, not a sampled family.
- Stress is the effective tensor `G+Lambda_5 eta=kappa_5 T`; boundedness is
  orthonormal pointwise boundedness, local `L1` is componentwise absolute with
  weight `w^3 rho ds`, and NEC means every orthonormal null vector.
- Exact deterministic coefficient and exponent/order arithmetic is required;
  floats, tolerances, randomization, heuristic simplification, and hidden
  endpoint cancellation are excluded.

## Method

Exact Lorentzian component contraction and sparse rational/polynomial arithmetic, augmented by a small explicit exponent/order representation for the two fixed profiles and the declared flat-germ premise; use analytic endpoint identities rather than floating sampling or heuristic simplification.

Rationale: The load-bearing risks are finite metric signs, profile derivative exponents, null-condition elimination, and confusing exponential volume suppression with pointwise boundedness. These admit canonical exact arithmetic and explicit asymptotic order rules; numerical sampling would be weaker and a general CAS would add unnecessary simplification assumptions.

## Representation and trust-surface assessment

- **Objects and operations.** Curvature, Ricci, Einstein, effective-stress, and
  null-contraction coefficients are sparse polynomials over `Fraction` in
  `A^2,p,q,r,Lambda_5`. Exact profile expressions are Laurent maps
  `c L^a s^b`. Required operations are collection, addition, multiplication,
  differentiation in `s`, finite tensor contraction, null-relation
  substitution, and explicit order composition.
- **Exponent, coefficient, and order semantics.** Coefficients and exponents
  are exact integers/rationals. Laurent powers of `s` may be negative; powers
  of positive `L` are nonnegative. The formal-order model has finite powers and
  an explicit `flat` element meaning the *declared premise* `O(s^N)` for every
  requested `N`; multiplying it by any fixed inverse power remains flat. This
  bookkeeping does not prove the analytic smooth-flat theorem.
- **Canonical equality.** Zero coefficients are removed and sparse maps are
  lexicographically sorted, so equality is decidable tuple equality. Tensor
  indices and all ten planes are finite explicit enumerations. No heuristic
  simplification, branch inference, float, tolerance, or sampling is present.
- **Encoded assumptions and reconstruction boundary.** Imported inputs are the
  four D019 curvature families/conventions, D002's two exact profiles and its
  flatness/exponential-domination facts, D004 normalization, positivity and
  finite-constant assumptions, and the frozen arbitrary-order flat-germ
  premise for `w-1`. The implementation reconstructs Ricci, scalar and Einstein
  tensors rather than inserting `G`; it then reconstructs all stress, NEC,
  profile, endpoint, and verdict tables.
- **Kernel choice and trust.** `research/computation/exact_graded/` is not used.
  Its exact primitives are adequate for ordinary sparse polynomials/exterior
  words, but its contract intentionally excludes negative polynomial exponents,
  tensor automation, and smooth-germ orders. Reuse would not remove the
  claim-local code and would enlarge the trust surface. A small self-contained
  implementation using only Python `Fraction` is safer than a CAS or an
  unnecessary custom reusable kernel. No Engineer work is justified.
- **Controls and correlation.** Product-space signs, separate `0-3` and `0-4`
  null witnesses, profile endpoint identities, and isolated semantic mutations
  control the calculation. Both NEC omissions are tested separately. These
  controls share conventions, code paths, arithmetic, and producer model, and
  are correlated rather than independent evidence.

## Acceptance criterion

Pass iff one exact canonical execution establishes: the Lorentzian
curvature-to-Einstein contraction and all five effective-stress entries; ten
off-diagonal zeros; the exact two-coefficient all-null NEC reduction with
explicit `0-3` and `0-4` witnesses; both profile derivative tables,
positivity thresholds, and divergent leading terms; the declared formal
flat-order dominance over every warp contribution; finite absolute
`rho |r|` integral together with unbounded `r` and exponentially damped
weighted `r^2`; and the final four-entry verdict for each profile. Mutations of
the timelike sign, a profile-derivative sign, either NEC-channel coverage, and
the bounded-versus-integrable distinction must all fail. Any mismatch or
ineffective mutation fails; only a predeclared unsupported exact-domain case is
inconclusive, and an exception is an execution error.

Declare thresholds, tolerances, precision, sample sizes, or rigor level before
running. Do not adjust the criterion after seeing output; supersede the
obligation instead and say why.

## Infrastructure used

- No reusable `research/computation/` kernel and no research-specific
  environment are used.
- Root orchestration provenance declared in `spec.yaml`: `pyproject.toml`,
  `uv.lock`, `scripts/_research.py`, and `scripts/run_check.py`.
- Check and infrastructure producer model: `openai/gpt-5.6-sol`. No Engineer
  participated.

## How to run

```bash
uv run --locked python scripts/run_check.py O011
```

The runner determines the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

Never write or edit `result.json` by hand.

### Direct implementation validation (noncanonical)

The scientific-computation producer validates only the entrypoint directly;
canonical wrapper execution is reserved for the director:

```bash
uv run --locked python research/checks/O011/run.py
uv run --locked python scripts/validate_research_state.py
```

Actual outcomes on 2026-08-22:

- Direct entrypoint: exit `0`; `79/79` exact assertions passed. The process-local
  mutations `timelike-stress-sign`, `profile-derivative-sign`,
  `omit-nec-normal-channel`, `omit-nec-circle-channel`, and
  `bounded-integrable-conflation` each returned exit `1`, as required.
- Research-state validator: exit `1` because of eight pre-existing structural
  errors outside the permitted O011 edit scope: the C023/D020 reciprocal target
  mismatch and seven required D020 heading/status errors. It also emitted the
  expected warning that active O011 has no `result.json`. O011's spec and
  entrypoint produced no additional validation error. The director subsequently
  corrected those integration errors; after canonical execution the strict
  validator passed with no warnings.
- No reusable-kernel suite is applicable because O011 imports no reusable
  kernel. Canonical execution was not invoked.

## Result

Canonical outcome: `passed` on 2026-08-22 at `15:24:41Z`, with 79/79 exact
assertions, ten off-diagonal stress zeros, both profile tables and NEC channels,
the formal flat-order bridge, distinct unbounded/L1 verdicts, and all five
mutations effective. See `result.json` and `logs/`.

## Interpretation and limitations

The executable decides only the frozen finite exact contraction, profile,
formal-order, and endpoint bridge under its encoded premises. It does not prove
that smooth zero extension implies arbitrary-order flatness, construct a matter
action, define an endpoint distribution, quantify over other profiles or
geometries, or provide independent verification. Exponential domination of
fixed inverse powers and the endpoint derivative value are imported from D002,
while their use in the weighted identities is checked. `r -> infinity` and
finite `integral rho |r|` are represented as distinct propositions. A passing
computation would be correlated supporting evidence, not a verified claim.
