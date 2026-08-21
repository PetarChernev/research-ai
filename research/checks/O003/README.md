# O003: Field-space curl and complete primitive

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C014

Derivations: D005

The exact target is C014's restricted statement that D005's isolated finite
connection momentum is not a closed field-space one-form when the coframe or
vertical circle normalization is free, whereas the gauge-covariant primitive
is integrable only with its connection, reference/edge, coframe, and
unconstrained-`eta` companion variations.  The encoded derivation steps are
D005 equations (1), (2), (24)--(29), and (61), with the fixed-interface and
variation assumptions in D005 sections 2 and 4.

## Question tested

On a certified nonzero one-mode restriction of D005's basic normalized boundary sector, is the isolated field-space one-form A=q^2*nu*dw nonclosed whenever the coframe amplitude q or vertical normalization nu varies, while B=(w-a)*q^2*nu has exactly the required connection, reference, coframe, and normalization companion terms and satisfies d_F^2 B=0?

## What this does not test

This is one exact nonzero restriction, not a formalization of arbitrary smooth
fields or local functionals.  It does not classify every possible interface
action, prove global bundle existence, test the dressing identities for a
nontrivial `g`, or decide whether reference/edge data are gauge or physical.  It
does not test the matching equations or rank claims in C015/O004, a bulk
solution, moving interfaces, corners, nonbasic circle modes, mixed `SO(1,4)`
components, Hamiltonian constraint closure, hyperbolicity, positivity, or any
quantum statement.  It also does not prove the analytic smooth-bump facts used
to select the mode; those are explicit mathematical inputs below.

## Assumptions encoded in the implementation

- The interface and variation class are exactly D005's fixed, persistent,
  local `SO(1,3)` sector.  A local trivialization sets `g=1` for mode selection,
  without identifying the dynamical connection and dressed reference.
- `epsilon_0123=+1`; antisymmetric connection pairs are summed in both ordered
  directions.  The base orientation is `dx0 wedge dx1 wedge dx2`, the circle
  orientation is positive, and `integral_(S1) eta_0=+2*pi`.
- `b=2*pi*gamma` is nonzero and is absorbed into the normalized connection
  mode.  No binary approximation to `pi` occurs.
- Field coordinates `w,a,q,nu` commute.  The field-differential order is
  `dw < da < dq < dnu`; their wedge product is anticommuting and each basis
  field differential is closed.
- The coefficient domain is the free exact rational polynomial ring.  There
  are no unrecorded algebraic relations, denominators in field coordinates,
  tolerances, samples, or branch choices.
- `nu=1` is the normalized principal connection.  Varying `nu` is explicitly
  D005's unconstrained vertical-density direction, not a variation within the
  affine space of normalized principal connections.  Horizontal normalized
  connection variations are not represented because their basic horizontal
  four-form vanishes on the three-dimensional base.

## Certified one-mode restriction

Choose an oriented coordinate cube `(-2,2)^3` precompactly inside `U`, after an
inessential affine rescaling of a smaller chart.  Let

```text
r(t) = exp[-1/(1-t^2)] for |t|<1, and 0 for |t|>=1,
phi(x0,x1,x2) = r(x0) r(x1) r(x2),
J = integral phi^3 dx0 dx1 dx2 > 0.
```

`r` and `phi` are smooth compactly supported bumps; positivity on the open
cube proves `J>0`.  Let `chi` be a smooth cutoff supported in
`(-3/2,3/2)^3` and equal to one on `[-1,1]^3`.  Define

```text
beta0 = phi dx0/(b J),   beta1 = phi dx1,   beta2 = phi dx2,
omega_+^01 = w beta0,    bar(a)^01 = a beta0,
e_+^2 = q beta1,         e_+^3 = q beta2,
eta(nu) = eta_0 + (nu-1) chi eta_0,
```

with the `10` connection components fixed by antisymmetry and all other active
components zero.  The persistent forms are horizontal and
`theta`-independent, hence basic pullbacks from `Sigma`.  `eta_0` is the marked
normalized principal connection; it is intentionally the one vertical leg,
not a horizontal basic form.  On the support of the other three factors,
`eta(nu)=nu eta_0`.

Every amplitude variation is compactly supported in the base and therefore in
`Sigma x S1`, since `S1` is compact; the support lies away from outer faces and
corners.  The coordinate variations commute.  Exact ordered-index enumeration
gives four equal positive terms:

```text
epsilon_abcd beta0^(ab) wedge beta^c wedge beta^d
    = 4 beta0 wedge beta1 wedge beta2,
integral_Sigma b beta0 wedge beta1 wedge beta2 = 1.
```

Thus the coefficient `gamma/4`, ordinary positive circle integration, internal
sum, and normalized base integral give total factor `+1`, not merely a nonzero
unspecified constant.  Consequently the actual D005 expressions restrict to

```text
A_Q = q^2 nu dw,
B_a = (w-a) q^2 nu.
```

The executable independently reconstructs the four internal contributions,
their sign, a zero repeated-leg control, the normalized factor, basicness of
the persistent legs, and exact support nesting.  This is the required
scientific-faithfulness certification; it is not inferred from the scalar
polynomials after the fact.

## Method

Exact polynomial field-space exterior differentiation on a nonzero normalized mode, with canonical anticommuting field differentials and explicit mutation controls.

Rationale: A single nonzero mode is an exact restriction that can witness nonclosure, while complete polynomial differentiation checks every companion term without claiming to formalize the entire infinite-dimensional field space.

The primary representation is the frozen `exact_graded` sparse polynomial and
exterior algebra.  Canonical coefficient collection and ordered field-wedge
tuples make equality decidable.  The check constructs `A_Q` and `B_a`, applies
the kernel's restricted field derivative, and compares every term with a
separately assembled exact normal form.

The required alternate method does not call the polynomial or field-derivative
path.  It evaluates D005 equation (28) directly with dense ordered internal
indices, a hand-written three-form determinant, and explicit constant commuting
variations.  At the normalized point `q=3, nu=1`, it evaluates
`(partial_q,partial_w)` and `(partial_nu,partial_w)` exactly; exchange of the
first pair tests antisymmetry.  This changes the conclusion-critical algorithm,
but it shares the selected physical mode and script, so it is an alternate
method check rather than independent verification.

## Representation and trust-surface assessment

1. **Domain represented.** Polynomial differential forms on the affine
   one-mode field space `(w,a,q,nu)`, preceded by a finite exterior/internal
   contraction on an oriented three-dimensional base and the marked circle.
2. **Operations required.** Exact rational polynomial arithmetic and
   differentiation, field-space wedge, ordered internal epsilon parity,
   spacetime wedge signs, exact zero/equality, and a normalized coefficient
   extraction.  General tensor algebra, integration, factorization, and
   equation solving are not required.
3. **Exact/canonical representation.** Both coefficient polynomials and
   exterior forms admit finite sparse canonical maps over `Fraction`; the
   internal mode is a finite component table.
4. **Equality semantics.** Equality is decidable after explicit coefficient
   collection and wedge canonicalization.  No heuristic simplifier or
   evaluation at sample points decides the primary identities.
5. **Encoded conventions.** Internal and base orientations, ordered-pair
   multiplicity, positive ordinary circle period, the absorbed nonzero `b`,
   support nesting, basicness, the normalized versus unconstrained `eta`
   classes, field-basis order, and commuting compact-support variations are all
   stated in `spec.yaml` and reconstructed above.
6. **CAS trust.** No CAS is used.  Were one used, its differentiation,
   anticommuting-form semantics, assumptions, and simplification normal form
   would become trusted; none is needed for this finite polynomial algebra.
7. **Small-kernel benefit.** The existing domain-specific kernel reduces the
   conclusion-critical surface to explicit rational and graded primitives and
   rejects floats and ambiguous bases.
8. **Existing implementation adequacy.** The public API exactly supplies the
   needed primitives, and its documented 45-law-test suite covers coefficient
   collection, wedge laws, field differentiation, `d_F^2`, epsilon parity,
   serialization, and invalid-input rejection.
9. **Custom-infrastructure risk.** A second general symbolic implementation
   would duplicate a tested substrate and enlarge risk.  O003 therefore adds
   only claim-specific mode construction, expected forms, and controls.
10. **Independent checks available.** A repeated-leg zero mode, per-term
    omission/sign controls, the process-local mutation, and the direct dense
    evaluation of D005 (28) attack the selected representation.  The dense
    evaluator is materially different from `field_derivative` but shares mode
    assumptions and producer model, so fresh model-separated verification is
    still required.

## Acceptance criterion

Pass iff exact field-space normal forms give d_F A=(2*q*nu*dq+q^2*dnu) wedge dw nonzero, d_F B=q^2*nu*(dw-da)+2*q*nu*(w-a)*dq+q^2*(w-a)*dnu, and d_F^2 B=0; free-q and free-nu controls separately give nonzero curl; fixing q and nu gives zero curl; the selected mode is certified nonzero and admissible; and deleting or sign-perturbing each companion term is detected. Fail on any exact mismatch. Inconclusive only if the selected mode has zero spacetime/internal contraction or lies outside the declared basic compact-support variation class; implementation exceptions are errors.

This is the allocation-time mathematical criterion, unchanged.  There are no
thresholds, tolerances, precision settings, random seeds, or samples.

### Declared controls

Positive controls cover the four-term normalized mode contraction; basicness,
circle orientation/normalization, compact support, and commuting variations;
the full curl; separate free-`q` and free-`nu` curls; fixed-`q,nu` closure; all
four terms of `d_F B`; and `d_F^2 B=0`.  Direct evaluation of the original curl
must give `6` on `(partial_q,partial_w)` and `9` on
`(partial_nu,partial_w)` at `q=3,nu=1`.

Negative controls make the spacetime contraction zero by repeating a mode leg,
delete each of the connection/reference/coframe/normalization terms in turn,
reverse each term's sign in turn, exchange the direct variations, and evaluate
a pair with `q,nu` fixed.  Every omission and sign mutation must be detected.

The process-local external mutation
`O003_INTERNAL_MUTATION=omit-coframe` removes the `dq` companion only from the
candidate complete variation.  It must make the entrypoint return `1`; it does
not modify any file or survive into the canonical process.

## Infrastructure used

The entire `research/computation/exact_graded/` directory is declared and
fingerprinted, including its source, law tests, and contract documentation.
The kernel supplies exact rational polynomials, sparse exterior forms,
field-space differentiation, wedge canonicalization, and epsilon parity.  Its
documented 45-test infrastructure suite establishes contract conformance, not
the scientific mode selection.  O003 separately validates the D005 internal
factor, sign, normalization, support/basicness assumptions, and direct curl.

`pyproject.toml`, `uv.lock`, `scripts/run_check.py`, and
`scripts/_research.py` are also declared because the sensitivity command uses
the locked root environment and the canonical wrapper/helper select the
process, outcome, hashes, logs, and result serialization.  No research
environment, scientific package, CAS, random source, float, or external
executable is used.  The frozen existing kernel was adequate, so no Engineer
was delegated for O003.

The conclusion-critical trust surface is Python integer and
`fractions.Fraction` arithmetic; the public kernel operations; the explicit
internal/component and orientation table; the analytically normalized bump and
cutoff construction; and the separate dense direct evaluator.  Canonical
equality reduces the symbolic trust surface, but cannot certify assumptions not
encoded in the finite mode.

## How to run

Run the noncanonical sensitivity command first:

```bash
O003_INTERNAL_MUTATION=omit-coframe uv run --locked python research/checks/O003/run.py
```

The mutated entrypoint itself must return `1`.  It does not invoke the wrapper
and cannot create `result.json`.

Then create the canonical result only through:

```bash
uv run --locked python scripts/run_check.py O003
```

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

- Canonical execution: `2026-08-20T14:09:08Z`
- Result: `research/checks/O003/result.json`
- Logs: `research/checks/O003/logs/stdout.log` and `stderr.log`
- Assertions: `44` total, `0` failed
- Canonical mutation tag: `none`
- Mode: four nonzero ordered contributions, coefficient `4`, normalized total
  `+1`, basic persistent legs, positive `+2*pi` period, commuting compact-
  support variations
- Direct D005 (28) values at `q=3,nu=1`: `6` on
  `(partial_q,partial_w)`, `9` on `(partial_nu,partial_w)`, and `-6` after
  exchanging the first pair
- All four omissions and all four sign reversals detected
- Whole `exact_graded/` directory SHA-256:
  `197024e3f37dff868c931141ce25949e26e2249bd4850d0213ff06e81449268b`
- Aggregate declared-infrastructure SHA-256:
  `0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`

The first development invocation of the direct mutation command exposed a
Python generator-parenthesization syntax error and exited `1`; that was an
implementation failure, not accepted sensitivity evidence.  After correcting
`run.py`, the same process-local mutation command returned `1` with `44`
assertions and exactly one intended failure,
`primitive.full_companion_sum`.  The explicit shell status check

```bash
O003_INTERNAL_MUTATION=omit-coframe uv run --locked python research/checks/O003/run.py; status=$?; test "$status" -eq 1
```

then returned `0`, confirming that the mutated entrypoint itself returned `1`.
No mutation was present in the canonical process.

## Interpretation and limitations

A passing outcome establishes the stated identities only in this exact finite
restriction and under the explicit D005 conventions.  The one-mode
nonzero curl is a witness to nonclosure on any field space containing these
variations; it is not a classification of the full field space.  Exact closure
of `d_F B` confirms algebraic integrability of the encoded primitive, not the
existence, differentiability, gauge status, or dynamical consistency of a full
bulk/interface theory.  Independent scientific verification must reconstruct
the assumptions and physical restriction rather than treating a passing kernel
execution as claim verification.

## Producer provenance

`openai/gpt-5.6-sol` produced D005, the current computation plan and frozen
contract, the Engineer implementation of `exact_graded`, and this O003
claim-specific implementation and scientific assessment.  The direct method
is algorithmically separate but not model-separated.  Deterministic execution
does not make these shared assumptions independent.
