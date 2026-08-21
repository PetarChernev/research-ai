# O001: D002 equalizer and curvature controls

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C009

Derivations: D002

The exact ledger claim under test is:

> For the quotient-form equalizer and connection choices defined in the C007
> benchmark, `dtheta+A` does not descend, whereas `rho_i(dtheta+A)`, horizontal
> `A`, `F=dA`, and horizontal theta-independent mixed connection components do
> descend; if an Ehresmann or independent `SO(1,4)` connection is retained on
> the nondegenerate rank-four exterior, ordinary `U(1)` or Lorentz gauge cannot
> map the displayed nonzero `F` or coframe-relative mixed curvature to zero,
> while a coframe-only state omits those independent data, an explicitly
> enlarged exterior-forgetful equivalence discards them, and future equations
> or boundary conditions could exclude them.

The encoded derivation steps are D002 equations (43)--(50), the U(1) witness
(58), and the Lorentz witness/covariance statements (59)--(61).

## Question tested

For the D002 kernel pair on the collapsed and resolved branches, do exact canonical pullback residuals classify eta=dtheta+A as non-descending while rho*eta, horizontal A, F=dA, and horizontal theta-independent mixed connection forms descend under the declared assumptions, and do the explicit exterior unit-jet curvature witnesses remain nonzero under ordinary invertible gauge transformations while leaving the collapsed coframe unchanged?

## What this does not test

This check does **not** prove the full smooth-germ equalizer theorem, profile
flatness, the quotient topology or diffeology, the existence of global bundles,
or any statement about large gauge transformations.  It does not decide whether
an independent connection belongs in the physical state, whether a forgetful
relation is gauge, whether equations remove the displayed curvature, or whether
the model has a variational principle, consistent constraints, hyperbolicity, or
solutions.  It also does not test C007/C008, integration, boundary incidence, or
any forward D006 dynamics.

The finite branch table checks only the displayed D002 sector.  In particular,
passing quotient descent is not principal-bundle basicness: on the positive
diagonal branch every pullback residual is automatically zero, while the check
requires
`i_(partial_theta)[rho(dtheta+A)]=rho != 0`.

## Assumptions encoded in the implementation

- The D002 kernel pair has exactly a positive diagonal branch (`s>0`) and a
  collapsed independent-angle branch (`s<=0`).
- On the collapsed branch, `rho=drho=0` exactly.  On the positive branch, `rho`
  is a nonzero formal coefficient.  The script does not establish profile
  flatness analytically.
- `A` and the positive mixed connection are horizontal and theta-independent.
  Vertical and theta-dependent forms occur only as declared negative controls.
- The unit jet is `A=chi du1`, `dchi=ds`, hence
  `F=ds wedge du1`; source coordinate one-forms and `dalpha` are closed.
- The target basis is ordered
  `du0 < du1 < du2 < ds < dtheta1 < dtheta2`.  Repeated legs vanish and
  permutation parity fixes every wedge sign.
- Coefficients are exact sparse rational polynomials in a fixed finite tag set.
  Equality is canonical map equality, never floating comparison or heuristic
  simplification.
- Gauge conventions are `theta -> theta-alpha`, `A -> A+dalpha` and
  `omega' = Lambda omega Lambda^-1` for the constant Lorentz control.  The
  metric is `diag(-,+,+,+,+)`.  The coframe-relative normal `n=e4` is used only
  on the open nondegenerate rank-four exterior image.
- The connection witnesses are independent fields.  Their addition is compared
  at fixed coframe; this is distinct from transforming the coframe under a frame
  change.

## Method

A self-contained sparse exact exterior-form branch table with explicit pullbacks, curvature jets, contractions, and invertible gauge substitutions; no shared custom kernel and no floating-point or heuristic simplification.

Rationale: The assertion lives in a finite branchwise kernel-pair sector with decidable exact equality. A self-contained representation minimizes trust and supplies a path materially separate from the shared graded kernel used by later obligations.

The implementation uses a one-off exact polynomial coefficient type, sparse
exterior forms, the explicit two-branch pullback table, contraction, the
declared exterior derivative jets, and exact 5 by 5 form matrices.  The primary
normal form is a map from strictly ordered wedge tuples to collected rational
coefficient monomials.

## Acceptance criterion

Pass iff exact canonical exterior-form equality gives residuals (dtheta1-dtheta2,0,0,0,0) for (eta,rho*eta,A,F,horizontal mixed connection) on the collapsed branch; a unit vertical mixed term and a theta-dependent horizontal control are nonzero; rho*eta has zero diagonal-branch residual but nonzero contraction with the fiber vector for rho!=0; the unit-jet U(1) and Lorentz examples have nonzero curvature, zero collapsed-coframe change, and exact gauge round trips; and every predeclared mutation control is detected. Fail on any exact mismatch. Inconclusive only for a predeclared missing branch/coefficient tag or a gauge map lacking an exact inverse; implementation exceptions are errors.

There are no thresholds, tolerances, random seeds, samples, or floating-point
settings.  Every comparison is exact.

### Declared controls

Positive controls cover the five collapsed residuals, the exact derivative and
flat pullback of `rho eta`, the diagonal-positive nonbasicness witness, and the
U(1) and Lorentz unit-jet curvature/coframe/gauge round trips.  Negative controls
require a vertical mixed term and a theta-dependent horizontal term to fail
descent, the wrong U(1) sign to fail invariance, and zero curvature to fail both
curvature witnesses.

The predeclared mutations reverse the `ds wedge du1` sign, identify the two
collapsed angles, omit either the `rho=0` or `drho=0` substitution, erase the
second theta coefficient tag, and replace the Lorentz inverse by the forward
matrix.  `O001_INTERNAL_MUTATION=wedge-sign` activates the first mutation solely
for a direct implementation-sensitivity test; it is absent from the canonical
run.

## Infrastructure used

The scientific implementation is self-contained in `run.py` and uses only the
Python standard library.  It does not import `research/computation/exact_graded`
or any other project kernel, and no Engineer-produced substrate or research
environment is involved.  `pyproject.toml` and `uv.lock` are declared and
fingerprinted because the canonical wrapper is launched by the locked root
`uv` environment; they are orchestration provenance, not a scientific algebra
dependency.

The trusted conclusion-critical surface is: Python integer and
`fractions.Fraction` arithmetic; the coefficient collection, wedge,
contraction, pullback, declared-jet derivative, and exact matrix functions in
`run.py`; and the hand-entered branch/gauge tables.  Law checks, explicit
expected canonical forms, the negative controls, and the external intentional
mutation test constrain that surface, but are not an independent
implementation.

## How to run

```bash
uv run --locked python scripts/run_check.py O001
```

The noncanonical implementation-sensitivity test is:

```bash
O001_INTERNAL_MUTATION=wedge-sign uv run --locked python research/checks/O001/run.py; test $? -eq 1
```

It must return shell status `0` only because the mutated entrypoint itself
returns the expected obligation status `1`.  It never invokes the canonical
wrapper and therefore cannot create or replace `result.json`.

The runner determines the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

Never write or edit `result.json` by hand.

## Result

Canonical outcome: **passed** (exit `0`).

- Canonical execution: 2026-08-20T12:09:34Z
- Result: `research/checks/O001/result.json`
- Logs: `research/checks/O001/logs/stdout.log` and `stderr.log`
- Declared assertions: 57; failed assertions: 0
- Canonical internal-mutation tag: `none`
- Declared-infrastructure aggregate SHA-256:
  `c21d6e0cb83ccdb378463a0a4e27009ab89dfd9fcf4660d9f30da50d95340de1`

The direct intentional mutation command above was run first.  The mutated
entrypoint returned `1` and reported exactly
`jet.F_exact`, `law.graded_antisymmetry`, and `law.wedge_sign` as failed; the
trailing shell assertion therefore returned `0`.  The mutation environment was
process-local and the canonical result records `internal_mutation: none`.

## Interpretation and limitations

A pass establishes only that the finite exact objects encoded here obey the
declared branch residual, contraction, curvature, fixed-coframe, and gauge
round-trip assertions.  It is regression evidence for C009/D002 under the
listed assumptions, not a proof of arbitrary smooth-germ quantifiers and not a
verified scientific claim.  The direct branch reconstruction required by the
independence plan remains work for an eligible verifier and must not reuse this
runner as its conclusion-critical path.

Producer model for the specification, documentation, and claim-specific
implementation: `openai/gpt-5.6-sol`.  No Engineer model contributed.
