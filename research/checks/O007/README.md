# O007: Total Lorentz cut cancellation

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C017

Derivations: D008, D009

## Question tested

Under the C017 fixed-interface basic persistent SO(1,3) assumptions and D004-D006 conventions, does the exact persistent five-dimensional core Palatini cut momentum have zero ordinary and normalized-circle pushforward at rho=0, and does the exterior Palatini term -P^- combine with the interface moment map -Ad_(g^-1)lambda to vanish on lambda=-Q and Q=g.P^- with the declared orientation, normalization, and dressing?

## What this does not test

This finite check does not establish smooth-germ descent, functional
differentiability, admissibility of seed/right transformations, primary or
secondary stabilization, first-class closure, a corner polarization, or a
physical classification of the residual rank-ten shell block.  It imports the
fixed-interface regular sector and matching shell and tests only their exact
coefficient/sign/dressing bridge.

## Assumptions encoded in the implementation

The represented core has `E^a=e_+^a`, `E^4=rho eta`; internal orientations are
`epsilon_01234=epsilon_0123=+1`.  Both ordered values of antisymmetric contracted
indices are summed.  Lorentz pairs are `(01,02,03,12,13,23)`, the metric is
`diag(-,+,+,+)`, and cut/circle forms use `dx1<dx2<dtheta`.  The formal exact
period `tau` means `2pi`: ordinary pushforward multiplies the rightmost
`dtheta` coefficient by `tau`, while normalized pushforward does not.

The planar witness is `e1=dx1`, `e2=dx2`, `e0=e3=0`.  The shell is
`lambda=-Q`, `Q=Ad_g P^-`; the residual is
`-P^- - Ad_(g^-1)lambda`.  Identity and the rational `01` boost
`cosh=5/3`, `sinh=4/3` are checked.  Common orientation reversal multiplies all
cut momenta by `-1`.  No float, tolerance, random sample, or CAS occurs.

## Method

Exact sparse exterior forms and rational Lorentz matrices using the existing research/computation/exact_graded substrate, with an independently assembled hand-formula cross-check and sign/dressing mutations.

Rationale: The new conclusion is a finite sign-, factor-, and dressing-sensitive algebraic bridge. Exact canonical arithmetic is stronger and smaller-trust than floating sampling; the existing stable substrate already supplies the needed wedge, epsilon, and rational-matrix operations, so no new environment or reusable infrastructure is justified.

## Acceptance criterion

Pass iff the exact assertions and all four mutations in `spec.yaml` succeed.
There are no thresholds or tunable tolerances.  Any mismatch or ineffective
mutation fails; only a declared input outside this exact representation is
inconclusive; an exception is an execution error.

## Representation and trust-surface assessment

- **Forms and coefficients.** Sparse exterior forms use a free polynomial ring
  over `Fraction` in `rho`, `R`, `tau`, `kappa4_inv`, and `kappa5_inv`.
  Canonical wedge tuples and the fixed Lorentz-pair order make equality exact.
- **Conventions.** Ordered-pair multiplicity, both epsilon orientations,
  `dx1<dx2<dtheta`, rightmost fiber extraction, ordinary/normalized circle
  mass, exterior incidence, shell signs, Lorentz orientation/signature, and
  dressing direction are explicit.
- **Trust surface.** The reusable surface is the frozen public
  `exact_graded` exterior, polynomial, and epsilon API plus `Fraction` and the
  deterministic wrapper.  Claim-local code supplies only finite Palatini sums,
  fiber extraction, the rational Lorentz adjoint, and residual mutations.  No
  heuristic simplifier is trusted.
- **Alternate check.** A separate dense permutation/word count recovers the
  `03` 4D and 5D coefficients, and the nonidentity boost is compared with the
  hand values `Q03=5/6`, `Q13=2/3` at `kappa4_inv=1`; neither comparison calls
  the primary assembly as its expected-output oracle.
- **Unsupported cases.** Smooth limits/germs, nonbasic or mixed `SO(1,4)`
  modes, profile-divided/distributional traces, symbolic division, arbitrary
  metrics/groups, large gauge transformations, and global bundles are outside
  the representation.
- **Adequacy decision.** Every needed operation is already exact and tested.
  New environment files, reusable infrastructure, or Engineer work would add
  risk and provenance without supplying a missing capability.

## Infrastructure used

Declared fingerprint paths are `research/computation/exact_graded`,
`pyproject.toml`, `uv.lock`, `scripts/_research.py`, and
`scripts/run_check.py`.  The relevant frozen contract is the exact graded
kernel contract in `research/COMPUTATION.md`.  No environment file was added and
no Engineer was invoked.

Producer model: `openai/gpt-5.6-sol`.  The recorded material infrastructure
producer model is `openai/gpt-5.6-sol`.

## How to run

```bash
uv run --locked python scripts/run_check.py O007
```

The runner determines the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

Never write or edit `result.json` by hand.

## Development tests

Development execution on 2026-08-22 used the locked root runtime and did not
invoke the canonical wrapper:

- unmutated `run.py`: exit `0`, all 28 exact assertions passed;
- `exterior-sign`: exit `1`, three cancellation assertions failed;
- `lambda-sign`: exit `1`, three cancellation assertions failed;
- `dressing-omit`: exit `1`, the nonidentity and orientation-reversed witnesses
  failed;
- `dressing-invert`: exit `1`, the nonidentity and orientation-reversed
  witnesses failed;
- fixed `exact_graded` infrastructure suite: 45 tests passed (`OK`).

These are development diagnostics only.  They do not create a canonical
outcome; canonical execution remains reserved for the deterministic wrapper.

## Result

No result recorded. The absence of `result.json` means this obligation has not
run.

## Interpretation and limitations

The obligation is ready for deterministic execution.  A future passing outcome
would establish only the encoded finite exact identities and mutation
sensitivity.  It would not promote C017 or settle any excluded gauge, corner,
constraint, smoothness, or physical-classification question.
