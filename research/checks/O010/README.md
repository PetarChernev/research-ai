# O010: Minimal warped background equations

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C022

Derivations: D019

## Question tested

Under the D019 common-warp ansatz and frozen D002/D004/D005 conventions, do an exact Cartan solve, curvature reconstruction, complete five-form Palatini Euler enumeration, regular endpoint reduction, branch-preserving first-integral analysis, and shell/orbit substitution reproduce the restricted nonexistence bridge claimed in C022?

## What this does not test

This finite check does not test whether the D002 category or D004/D005 action is
physically compulsory, any more general source-free metric, matter or singular
sources, anisotropic/lapse/off-diagonal sectors, moving interfaces, functional
Hamiltonian preservation, broad C002/C003, hyperbolicity, stability, or
independent verification. It tests only the exact restricted D019/C022 bridge.

## Assumptions encoded in the implementation

- The Cartan system is solved only on the invertible core `s>0`, for
  `E^i=w dx^i`, `E^3=ds`, `E^4=rho dtheta`, signature
  `diag(-,+,+,+,+)`, `epsilon_01234=+1`, and D004's curvature convention.
- D004's exact action coefficients and ordered antisymmetric-pair convention are
  used. Both bulks are source free; omitted sectors are listed in `spec.yaml`.
- Endpoint work uses the denominator-cleared coordinate equations and
  `w(0)=1`, `w'(0)=w''(0)=0`, `rho(0)=rho'(0)=0`. The polar control drops only
  `rho'(0)=0`.
- The D005 shell uses planar traces, `a0=0`, `u=g=1`,
  `b=kappa_4^-1`, and proper outer corners. `K=0` must follow from the limiting
  persistent connection and seed.
- Arithmetic and equality are exact and canonical; floats, tolerances,
  randomization, and heuristic simplification are excluded.

## Representation and trust-surface assessment

The obligation represents all 50 spin-connection coefficients, sparse torsion
and curvature forms, all five D004 Euler forms, regular coordinate ODE
identities, endpoint linear data, and planar shell forms. It uses exact rational
linear algebra and sparse polynomials/exterior maps from the already tested
`exact_graded` kernel. Equality is deterministic RREF or canonical map equality.

No CAS, new dependency, environment, or Engineer work is justified: the finite
domain is decidable with the existing primitives. A separately assembled
component Einstein/constant-curvature path and direct coordinate-ODE identities
attack the main transcription risk, but share assumptions, arithmetic, and
OpenAI provenance and are not independent confirmation.

**Implemented trust surface.** `run.py` trusts Python `Fraction`, immutable
`exact_graded.Polynomial` normalization, canonical `ExteriorForm.wedge`,
`levi_civita_sign`, and deterministic `RationalMatrix.rref/rank/nullspace`.
Claim-local code supplies the 50-row Cartan matrix, coframe derivative rules
`A'=p-A^2`, `B'=r-B^2`, ordered D004 Euler enumeration, coordinate-jet ODE
identities, endpoint systems, component contraction, and D005 substitutions.
It uses no symbolic division, float, tolerance, random sample, or CAS. The
component/ODE route is explicitly **correlated, not independent**.

The implementation solves two exact rational right-hand sides of the same
full-rank Cartan matrix and combines them over the free atoms `A,B`; it does not
insert the desired connection. Curvature is differentiated from that solution,
and the raw `-A*B` family is checked before being renamed `-q` for Euler-form
comparison. Both first-integral branches are retained in denominator-cleared
form. Endpoint elimination is tested separately from the affine polar control.

## Method

Exact sparse exterior algebra and rational linear algebra using the existing fingerprinted `research/computation/exact_graded/` kernel, plus a separately assembled component/ODE control path and process-local semantic mutations.

Rationale: The disputed assertions are finite polynomial exterior identities, exact ranks, and endpoint ideal implications. Canonical rational/polynomial arithmetic is stronger and more transparent than floating integration or heuristic CAS simplification, while the existing tested kernel already supports the required wedge, epsilon, and RREF operations without new infrastructure.

## Acceptance criterion

Pass iff exact canonical arithmetic establishes: the full-rank Cartan solve and
unique connection; precisely the four curvature families in D019; the complete
Euler coefficient vector `(S,S,S,H,J)` with correct cosmological normalization;
all three denominator-cleared coordinate equations; the first integral while
retaining both `C=0` and `C!=0` branches; endpoint elimination to
`Lambda_5=0`, `w=1`, `rho=0` with an affine polar negative control; flat
exterior and complete shell/orbit residuals; unwarped and constant-curvature
controls; and effective isolated mutations of the plane-curvature sign,
cosmological normalization, circle-equation coverage, and `rho'(0)` endpoint
condition. Any exact mismatch or ineffective mutation fails. Only a
predeclared unsupported exact-domain operation is inconclusive; an exception is
an execution error.

Declare thresholds, tolerances, precision, sample sizes, or rigor level before
running. Do not adjust the criterion after seeing output; supersede the
obligation instead and say why.

## Infrastructure used

- `research/computation/exact_graded/`
- `pyproject.toml`, `uv.lock`, `scripts/_research.py`, `scripts/run_check.py`

Infrastructure and check producer model: `openai/gpt-5.6-sol`. No new reusable
substrate or research environment is required.

## How to run

```bash
uv run --locked python scripts/run_check.py O010
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

The scientific-computation producer ran only the entrypoint directly, as
requested, leaving canonical execution to the director:

```bash
uv run --locked python research/checks/O010/run.py
```

Local outcome on 2026-08-22: exit `0`, with `74/74` exact assertions. The
process-local mutations `plane-curvature-sign`,
`cosmological-normalization`, `omit-circle-equation`, and
`delete-rho-prime-endpoint` each returned exit `1` and were recorded effective
by the parent process. The fixed reusable-kernel suite was also run through its
typed test entrypoint: `45/45` tests passed. These are implementation-validation
observations, not a canonical obligation result.

## Result

Canonical outcome: `passed` on 2026-08-22 at `13:54:12Z`, with 74/74 exact
assertions, Cartan rank 50, both first-integral branches represented before
endpoint elimination, endpoint/polar ranks two/one, six nonzero shell momentum
rows, and all four mutations effective. See `result.json` and `logs/`.

## Interpretation and limitations

When canonically executed, the outcome applies only to the encoded finite exact
assertions. It cannot establish completeness of the background/action search,
functional preservation, broad C002/C003, or independent verification.
Mutation controls establish discriminating power for named faults but do not
make the shared representation independent.

The finite endpoint checks encode the declared regular equations and finite
jets; they do not formalize smooth-function existence/uniqueness as a theorem.
Positivity and connectedness are assumptions used to interpret the exact branch
relations. The shell path checks the frozen planar, constant-coefficient seed
sector only. Actual producer model: `openai/gpt-5.6-sol`; the selected reusable
infrastructure was also materially produced by `openai/gpt-5.6-sol`.
