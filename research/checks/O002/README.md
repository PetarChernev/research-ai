# O002: Collapsed Palatini boundary operator

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: C010, C012

Derivations: D003, D004

The exact target is the finite algebraic content of C010 and C012: D003's
regular descended degree-four core trace is zero, and D004's bare
five-dimensional Palatini potential consequently contributes no regular
collapsed core momentum while the four-dimensional potential has a nonzero
planar witness.  The encoded derivation targets are D003 equations (9), (20),
(25), and (29), and D004 equations (24), (30)--(31), (34), (36), (39), (42)--
(43), and (83).

## Question tested

Under the D002/D003 smooth equalizer and D004 ordered-index, epsilon, orientation, and circle conventions, does the exact boundary-incidence operator annihilate the descended degree-four core trace and reduce the bare five-plus-four-dimensional Einstein-Cartan interface variation to the negative exterior Palatini potential, with the declared planar witness and fixed-radius product-circle control?

## What this does not test

This obligation does not prove the D002 smooth equalizer or its flatness theorem
for arbitrary germs.  It takes their boundary consequences `rho0=0`, `b0=0`,
and `chi0=0` as encoded assumptions.  It does not formalize quotient topology,
diffeology, global bundles, large gauge transformations, or arbitrary smooth
fields.

It tests only the bare fixed-interface Einstein--Cartan representative.  It does
not test Lovelock curvature channels, boundary/polarization/transgression terms,
Holst or matter terms, singular or divided traces, retained boundary-circle
fields, moving interfaces, corners, field-space integrability, constraints,
hyperbolicity, ghosts, deterministic reopening, or existence of a bulk
solution.  It does not choose among enriched action completions and does not
establish C011, C013, or any claim status.

## Assumptions encoded in the implementation

- The local closures, supports, and fixed interface are exactly those in
  D003--D004; outer faces, corners, and interface displacement are absent.
- `oSigma=du0 wedge du1 wedge du2`, `o4=oSigma wedge ds`, and
  `o5=oSigma wedge ds wedge dtheta`.  Boundary orientation is outward-normal
  first with `n_+=-partial_s` and `n_-=+partial_s`; `dtheta` is moved right.
- `epsilon_01234=epsilon_0123=+1`,
  `epsilon_abcd=epsilon_abcd4`, and antisymmetric internal pairs are summed over
  both ordered values.
- The only potentials are
  `Theta5=(kappa5_inv/12) epsilon_ABCDE deltaomega^AB E^C E^D E^E` and
  `Theta4=(kappa4_inv/4) epsilon_abcd deltavarpi^ab e^c e^d`.
- Persistent core coframes are horizontal and `E4=rho(dtheta+A)` with horizontal
  `A`.  Smooth descent is encoded at the trace as `rho0=0`; the vertical mixed
  variation coefficient is encoded as `chi0=0`.
- For `alpha4=a4+b3 wedge dtheta`, the boundary-relevant generic coefficients
  are `a*oSigma wedge ds` and `b0*oSigma wedge dtheta`; pullback sets `ds=0`
  and descent sets `b0=0`.
- Ordinary pushforward sends a rightmost `dtheta` coefficient to `tau` times
  that coefficient, with exact formal `tau=2*pi`; normalized Haar sends it to
  the coefficient.  No symbolic division or floating approximation is used.
- The planar witness is `(e0,e1,e2,e3)=(du0,du1,du2,0)` and
  `deltavarpi^03=f du0`.  The mixed core witness is
  `deltaomega^43=chi0 dtheta`.
- The fixed-radius check is a separate regular product-circle control with
  `rho0=R`, `chi0=0`, and exact relation
  `kappa4_inv=tau*R*kappa5_inv`.
- Coefficients form a free exact rational polynomial ring.  Wedge tuples use
  explicit ordered bases and exact canonical equality; there are no
  tolerances, random samples, floats, or hidden algebraic relations.

## Method

Exact sparse polynomial exterior algebra, explicit ordered antisymmetric-index enumeration, boundary contraction/pullback, and formal circle-period extraction over a canonical basis.

Rationale: C010 and C012 depend on exact wedge signs, factorials, orientation, and a formal 2pi count. The finite algebra has a transparent normal form and needs no heuristic CAS operation.

The primary calculation uses the frozen public API
`Polynomial`, `ExteriorAlgebra`, `ExteriorForm`, and `levi_civita_sign` from
`research/computation/exact_graded/`.  The universal split is formed in a free
odd-generator algebra; the trace, boundary, and planar calculations use
separate explicit spacetime bases.  A claim-local alternate path uses an
unordered antisymmetric pair and a dense coefficient dictionary with its own
inversion-parity and contraction routines.  It recovers the boundary signs,
zero-trace branch table, two split ratios, planar multiplicities, and ordinary
and normalized fixed-radius relations without calling the kernel's wedge,
epsilon, polynomial, or pullback implementations for those alternate checks.

### Representation and trust-surface assessment

1. **Domain:** finite free exterior algebras for the five-dimensional closure,
   four-dimensional closure, circle boundary, three-dimensional interface, and
   formal internal coframe/connection generators, over exact rational
   polynomials.
2. **Needed operations:** exact wedge, left contraction, pullback `ds -> 0`,
   coefficient substitution, epsilon parity, ordered-pair enumeration, and
   rightmost-fiber coefficient extraction.  No general tensor or smooth
   calculus is required.
3. **Exact representation:** every object has finite sparse support and exact
   `Fraction` coefficients; `tau` remains formal.
4. **Decidable equality:** polynomial monomials and exterior tuples have
   canonical normal forms, so equality is direct map equality.
5. **Encoded conventions:** orientations, outward normals, epsilon signs,
   antisymmetric ordered-pair multiplicity, vertical-leg ordering, equalizer
   trace substitutions, and ordinary versus normalized circle mass are all
   explicit in `spec.yaml` and `run.py`.
6. **CAS trust avoided:** a CAS would add branch/simplifier and assumption
   semantics without supplying any needed operation.  No CAS is used.
7. **Kernel choice:** the existing small exact kernel materially reduces the
   trust surface relative to ad hoc symbolic simplification.
8. **Adequacy:** its public API directly supplies every required exact primitive;
   no dependency or environment change is needed.
9. **Custom-risk boundary:** only claim-local maps and index tables are added.
   Building another reusable algebra would increase risk and violate scope.
10. **Cross-checks:** D003 signs and trace are reconstructed both sparsely and
    by a direct dense branch table; D004 factors are reconstructed from the
    original `1/12` ordered sum and by an unordered-pair dense count; the planar
    multiplicities and regular product-circle relations are also recovered in
    both representations.

## Acceptance criterion

Pass iff exact canonical calculation gives the declared core and exterior boundary orientations; maps a generic descended alpha4=a4+b3 wedge dtheta to zero core trace and zero ordinary/Haar pushforward; derives the D004 five-dimensional potential split with coefficients kappa5_inv/4 and kappa5_inv/6; makes both collapsed core channels zero; gives j_-^*Theta4=f*kappa4_inv*oSigma and total collapsed residual -f*kappa4_inv*oSigma; gives fixed-radius residual (tau*R*kappa5_inv-kappa4_inv)*f*oSigma and exact zero after kappa4_inv=tau*R*kappa5_inv; removes exactly one tau under normalized Haar; and detects every sign, factor, trace, and orientation mutation. Fail on any exact mismatch. Inconclusive only when a term is predeclared outside the bare fixed-interface regular-descended sector or conventions are absent/contradictory; implementation exceptions are errors.

There are no thresholds, tolerances, precision settings, seeds, or samples.
Every verdict-bearing comparison is exact.

### Scientific reconstruction before coding

- `i_(partial_s)(oSigma wedge ds)=-oSigma`; therefore the exterior outward
  normal gives `-oSigma`.  The core has one additional rightmost `dtheta` and
  outward normal `-partial_s`, giving `+oSigma wedge dtheta`.
- In `alpha4=a4+b3 wedge dtheta`, boundary pullback kills the horizontal
  four-form and the equalizer kills the tangent coefficient of `b3`; ordinary
  and Haar pushforwards are consequently both zero.  Before descent they are
  respectively `tau*b0*oSigma` and `b0*oSigma` with positive sign.
- Starting from `1/12`, the persistent channel has three placements of internal
  index `4` among the coframes, yielding `3/12=1/4`.  The mixed channel has two
  orders of the antisymmetric connection pair, yielding `2/12=1/6` after the
  remaining ordered coframe sum is retained.
- On the planar witness the four ordered contributions associated with
  `03/30` and `12/21` turn `(1/4)` into unity, so
  `Theta4=f*kappa4_inv*oSigma`.  The incident exterior sign makes the collapsed
  total its negative.
- At fixed `rho=R`, ordinary pushforward gives
  `tau*R*kappa5_inv*f*oSigma`; matching requires
  `kappa4_inv=tau*R*kappa5_inv`.  Normalized Haar removes exactly that one
  `tau`.

### Declared controls

Positive controls cover both boundary contractions, the generic trace,
ordinary/Haar maps, both primary split coefficients, the unordered/dense
cross-check, both separate collapsed channels, the planar exterior witness,
the total incidence sign, and ordinary/normalized fixed-radius relations.

Negative controls retain a forbidden non-descended boundary coefficient,
require each pretrace core channel and the exterior planar witness to be
nonzero, and require an unmatched fixed-radius residual to be nonzero.

Mutations reverse each boundary orientation, retain the forbidden trace, swap
ordinary and Haar `tau` behavior, alter each split factor, omit either collapsed
trace substitution, lose an exterior ordered-pair multiplicity, replace the
incidence minus by plus, drop the fixed-radius `tau`, and reverse the matching
relation sign.  The process-local `total-sign` mode intentionally activates the
incidence mutation for a direct sensitivity run.

## Infrastructure used

`spec.yaml` declares and fingerprints the **entire**
`research/computation/exact_graded/` directory, including implementation,
tests, documentation, and any extant directory entries.  It also fingerprints
`pyproject.toml`, `uv.lock`, `scripts/run_check.py`, and `scripts/_research.py`,
which materially supply locked orchestration and canonical recording.

The kernel is standard-library-only and its README records 45 passing
contract/law tests.  Those tests establish substrate behavior, not this
scientific assertion.  O002 separately checks the conclusion-critical D003
contractions, D004 multiplicities, planar sign/normalization, and soluble
fixed-radius limit.

The trusted surface is Python integer/`Fraction` arithmetic; the fingerprinted
kernel; the small claim-local pullback, pushforward, and index tables in
`run.py`; and deterministic wrapper recording.  The dense alternate path uses
different local data structures, contraction, parity, branch, and coefficient-
substitution routines, but it remains in the same producer file and shares the
stated mathematical conventions; it is not fresh model-separated verification.

## How to run

```bash
uv run --locked python scripts/run_check.py O002
```

The required noncanonical implementation-sensitivity command is:

```bash
O002_INTERNAL_MUTATION=total-sign uv run --locked python research/checks/O002/run.py; test $? -eq 1
```

The mutated entrypoint must return obligation status `1`; the trailing shell
assertion then returns `0`.  This direct command never invokes the canonical
wrapper and cannot create or replace `result.json`.  The environment assignment
is process-local and must be absent from the canonical run.

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

- Canonical execution: `2026-08-20T14:13:21Z`
- Result: `research/checks/O002/result.json`
- Logs: `research/checks/O002/logs/stdout.log` and `stderr.log`
- Canonical assertions: 71 total, 71 passed, 0 failed
- Canonical internal-mutation tag: `none`
- Ordered sparse split: `1/4`, `1/6`
- Unordered dense split: `1/4`, `1/6`
- Entire `exact_graded/` directory SHA-256:
  `197024e3f37dff868c931141ce25949e26e2249bd4850d0213ff06e81449268b`
- Declared-infrastructure aggregate SHA-256:
  `0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`

The direct intentional-mutation command was run first.  The mutated entrypoint
returned `1` after 71 assertions, with exactly
`P05.total_collapsed_residual` failing; the trailing shell assertion returned
`0`.  The canonical wrapper then recorded 71 passing assertions, zero failed
assertions, and `internal_mutation: none`.

## Interpretation and limitations

The pass establishes only the finite exact identities encoded under the
listed regularity, orientation, action-representative, and trace assumptions.
It is machine evidence for C010/C012's declared algebraic content, not a
proof of the smooth-germ premise and not a verified scientific claim.  Fresh
independent verification must reconstruct the derivations and challenge the
representation without treating the shared kernel or this runner as an
independent source.

Producer model for this specification, documentation, and claim-specific
implementation: `openai/gpt-5.6-sol`.  The materially used exact kernel was also
produced earlier by Engineer model `openai/gpt-5.6-sol`.  No Engineer was
delegated during this O002 claim-specific implementation/execution task, and
Engineer did not author `run.py`.
