# CY007 mixed-polarization-completion synthesis

Date: 2026-08-22

## Bounded issue and decision quantity

This single-branch convergence cycle changed exactly one action-side datum in
the C025 finite-slope benchmark.  It added the full core-boundary primitive

```text
B_ref = - integral_(Sigma x S1)
        (omega_+ - barOmega)^(AB) wedge P^(5)_AB(E),
```

with one geometrically transforming `SO(1,4)` reference connection.  The
finite-slope flat bulks, fixed interface, free one-sided mixed tangent, and
complete persistent D005 shell were otherwise frozen.  The decision quantity
was whether cancellation of the `43` row survives the primitive's compulsory
coframe, reference, gauge-orbit, and corner equations and yields a freely
selected `c>0` rank-three background without external amplitude or
unclassified edge structure.

## Evidence inventory and dependence

| Evidence | Result | Status and dependence |
|---|---|---|
| `research/derivations/D023.md` | Derives the exact rank-three reduction and complete variation of the single primitive; evaluates fixed, unrestricted, and fixed-seed gauge-orbit reference treatments. | Exact restricted derivation by `openai/gpt-5.6-sol`; imports D004/D005/D022 conventions. |
| `research/critiques/D023-2026-08-22-openai-01.md` | Reconstructs the coefficient, complete-variation signs, rank implications, orbit corner sign, holonomy qualification, and covariance boundary. | `no-blocking-issue-found`; same-model internal critique, not independent evidence. |
| O013 | Checks the ordered momentum table, primitive reduction, complete variation, all ten connection-row cancellations, polar coframe/reference residuals, orbit signs, and generic infinitesimal `SO(1,4)` covariance. | Canonical outcome `passed`, 38/38 assertions; self-contained exact arithmetic but shared conventions and OpenAI provenance make it correlated support. |
| C025/D022/O012 | Supplies the positive uncancelled D004 mixed row and frozen-D005 incidence that the new primitive attempts to repair. | Prior restricted derived and machine-checked evidence; O012 does not test the new primitive. |

No experiment, literature search, reusable infrastructure, Engineer task, or
Opus audit was used.

## Exact scoped result

On the rank-three trace only the ordered momenta `P43` and `P34` survive:

```text
P43 = -o_Sigma/(2 kappa_5),
P34 = +o_Sigma/(2 kappa_5).
```

Both ordered connection components therefore contribute, giving

```text
B_ref|polar = -(2 pi/kappa_5)
              integral_Sigma (chi43-barChi43) o_Sigma.
```

This cancels the positive C025 core row.  The complete variation is instead

```text
delta B_ref = -delta omega wedge P
              +delta barOmega wedge P
              +delta E^C wedge J_C,

J_C = (4 kappa_5)^(-1) epsilon_ABCDE
      (omega-barOmega)^(AB) wedge E^D wedge E^E.
```

Thus the primitive changes polarization; it does not introduce a new mixed
momentum-matching equation.  On the polar background the surviving variation is

```text
(2 pi/kappa_5) integral_Sigma
[delta barChi43 o_Sigma
 -(chi43-barChi43) delta o_Sigma].
```

The compulsory equations separate the reference treatments:

1. **Fixed geometric reference:** free triad rescalings require
   `chi43=barChi43`, hence the torsion-free slope obeys `c=barChi43`.  A
   positive slope survives only as externally supplied reference data.
2. **Unrestricted reference:** its equation is `P^(5)=0`, which kills every
   triple coframe minor and gives boundary coframe rank at most two.
3. **Fixed-seed gauge orbit:** the reference equation becomes
   `D_barOmega P^(5)=0` with corner potential
   `-integral_(partial Y) zeta P^(5)`.  The polar background can satisfy the
   bulk edge equation, but one fixed orbit preserves the circle-holonomy
   conjugacy class, so generic continuous `c` is not free.  Nonproper corner
   transformations have a nonzero normal-bivector moment map, whose
   gauge/physical status is unclassified.
4. **Freely varied seed:** the unrestricted `P^(5)=0` equation returns.

No treatment meets the positive criterion.  This is C026, a derived restricted
single-primitive result with passing correlated machine support.

## Covariance boundary

The primitive itself is exactly `SO(1,4)` covariant because both connections
transform geometrically and their difference is tensorial.  That covariance
also means that its full variation cancels all ten core connection rows and its
orbit equation is ten-component; it is not intrinsically a one-scalar `43`
term.  The otherwise frozen D005 interface action contains only the selected
persistent `SO(1,3)` reduction.  Making the total interface problem fully
`SO(1,4)` covariant therefore requires an explicit normal/reduction field or a
full mixed extension of D005.  Those are new fields and equations, so the cycle
stops rather than adding them silently.

## Falsification attempts and computational disposition

- Recounting both antisymmetric orders, six coframe permutations, the odd
  `dtheta` move, positive core incidence, and ordinary circle period reproduces
  the coefficient and sign.
- The complete variation preserves the coframe and reference rows; D004 has no
  boundary `delta E` row and frozen D005 has no mixed/reference row that could
  cancel them.
- Vanishing of all reference momenta is equivalent to vanishing of all triple
  minors, hence rank at most two rather than merely failure of one polar gauge.
- The orbit integration by parts has bulk sign `+zeta D P` and corner sign
  `-zeta P`.
- The integer-`c` zero-seed winding control is discrete and assumes the standard
  compact `T43` normalization; it does not restore a free continuous slope.
- O013 passed 38/38 exact assertions.  The `omit-order`,
  `reverse-primitive-sign`, `delete-coframe-companion`,
  `reverse-orbit-corner-sign`, and `transform-only-dynamical-connection`
  mutations each exited `1` as required.  Its generic infinitesimal covariance
  identity is not a global or large-gauge theorem.

## Cycle decision and next discriminator

Close `CY007-mixed-polarization-completion`.  Reject this standard covariant
polarization primitive as a positive repair of C025: cancellation alone only
relocates the obstruction into reference/coframe/edge data.  Do not infer a
universal no-go or test another ad hoc scalar counterterm inside the same
undeclared reduction.

The next future theory task should explicitly widen one level and define the
minimal covariant boundary normal/reduction field relating the core
`SO(1,4)` bundle to the exterior `SO(1,3)` bundle.  Its bounded decision should
be whether the finite normal-plane `43` holonomy/tangent is a genuine gauge
direction, fixed superselection datum, or physical edge variable.  Only after
that decision should a full mixed interface action or canonical representation
be selected.  No computation is queued for that undefined object.
