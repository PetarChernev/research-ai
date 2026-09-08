# CY008 reduction-field literature and evaluation synthesis

Date: 2026-08-23

## Bounded issue and stopping rule

This iteration mapped five unresolved literature neighborhoods but evaluated
only the lead with the highest immediate information value: whether a
covariant `SO(1,4)/SO(1,3)` reduction field supplies the missing dynamics and
classification in the exact C025/C026 finite-slope benchmark. The fixed flat
bulks, fixed interface, D022 finite mixed tangent, and persistent D005 sector
were otherwise frozen. The iteration stopped after one focused source packet,
one preallocated derivation, two derivation critiques, three computation-bridge
critiques with two bounded repairs, one exact machine obligation, and synthesis.

The positive decision quantity was whether the smallest induced-connection
reduction-field primitive preserves a freely selected rank-three `c>0`
background and classifies the finite `43` datum without external reference
data, degeneracy, or an uncontrolled edge pair.

## Evidence inventory and dependence

| Item | Result | Epistemic status and dependence |
|---|---|---|
| Five reports under `research/literature/explorations/CY008-*.md` | Map edge/corner reduction fields, degenerate Palatini traces, rank-changing constraints, moving strata, and mixed-dimensional hyperbolicity; 52 source families total. | Discovery maps only. Abstracts, metadata, snippets, and preliminary full-text inspection cannot support ledger claims. |
| `research/literature/notes/so14-so13-compensator-corner-phase-space.md` | Validates a kinematic `G/H` reduction template and ordinary tetrad-corner normal pairing, while locating the assumptions that block direct import. | Focused primary-source evidence. Four arXiv full texts were inspected; Stelle--West remained abstract/metadata-only. Applicability to rank change is low. |
| D024 | Constructs the unique minimal induced stabilizer connection under two declared conditions, varies the dependent primitive, and derives the polar coframe obstruction. | Exact restricted derivation by `openai/gpt-5.6-sol`, dependent on D004/D005/D022/D023 conventions and the selected ansatz. |
| First D024 critique | Found the central exclusion intact but required correction of the graded coframe sign in the displayed Noether identity. | Durable `revision-required` same-model critique; not independent evidence. |
| Revised D024 and second critique | Corrected the identity to `D B_omega-B_E diamond E+B_V diamond V=0`; direct projector and polar attacks found no remaining blocker. | Same-model revision and `no-blocking-issue-found` re-critique; procedural separation only. |
| Initial O014 implementation and first computation-bridge critique | The first canonical run reported 34/34, but the critic showed that its variation, IBP, generic residual, Noether, and polar rows largely inserted targets or compared expressions with themselves. | Durable `revision-required` same-model critique. The initial green outcome was not accepted as satisfying the declared criterion. |
| First O014 repair and second computation-bridge critique | Replaced target-shaped rows with graph differentiation, graded IBP, extracted Euler/corner coefficients, concrete polar support, a three-row Noether contraction, and upstream mutations. A 41/41 canonical run followed, but the critic found that the generic `hhP` target omitted Lorentzian index lowering and that the spatial test vector masked it. | Durable `revision-required` same-model critique. The 41-assertion result became stale after repair. |
| Final O014 repair and third computation-bridge critique | Uses a boosted unit-spacelike vector, explicitly distinguishes `h^A{}_B` from `h_A{}^B`, checks every generic row, and makes the old wrong-sign assembly a negative law. | Canonical outcome `passed`, 46/46 assertions and 6/6 effective fresh-process mutations; final same-model outcome `no-blocking-issue-found`. Shared conventions and OpenAI provenance make this correlated support only. |

No experiment, Engineer task, research-scoped environment, or Opus audit was
used. The five explorers, focused literature worker, theorist, critics, and
Scientific Computation all report `openai/gpt-5.6-sol`; their agreement is not
independent confirmation. A later mechanical BibTeX validation was produced by
`anthropic/claude-haiku-4-5`; it changes citation metadata, not scientific
source interpretation or model independence.

## Literature triage

### Evaluated immediate lead

The focused note establishes only the following source-supported minimum:

1. A section of an associated `G/H` bundle selects a conjugate `H` reduction.
2. After that choice, a reductive Lie-algebra split decomposes a `G` connection
   algebraically without an inverse coframe.
3. In ordinary invertible 4D Einstein--Cartan--Holst gravity, a varied internal
   foliation normal can occur in a codimension-two corner pairing and Lorentz
   moment map, with the result depending on polarization and edge-frame
   treatment.

The sources do **not** provide a `delta V` corner pairing for a de Sitter
compensator, a rank-three degenerate pullback, compact-circle `43` holonomy, or
exact `4<->5` local-dimension change. Wise's Cartan soldering is explicitly
nondegenerate, and the Freidel--Geiller--Pranzetti normal is a different
quotient object constructed with an inverse tetrad. These sources therefore
motivate a calculation but do not solve or support C027 by themselves.

### Unevaluated but preserved leads

- **Degenerate Palatini traces:** lightlike Palatini/BV--BFV and weak
  tangential-trace/Green-pairing families may expose the exact constant-rank
  assumptions behind C018--C020. Their lightlike or fixed-dimensional regimes
  do not yet establish a rank-changing trace adjoint.
- **Rank-changing constraints:** GNH, irregular-constraint, constraint-
  bifurcation, and stratified-reduction work offers candidate diagnostics for
  future preservation. No inspected source supplies a complete
  bulk-plus-interface Dirac analysis for exact tetrad-rank change.
- **Moving strata:** doubly covariant embedding variation, displacement
  operators, shape calculus, and current complexes are possible methods, but
  every inspected gravity source retains a fixed-dimensional ambient manifold.
- **Hyperbolicity:** Friedrichs/Kreiss--Secchi boundary-flux methods,
  port-Hamiltonian interconnection, edge propagation, and dynamic-boundary
  fields are candidate tools only. There is no direct theorem for the D002
  unequal-dimensional Lorentzian junction and no operator to test yet.

These four branches remain queued leads, not evidence or direction changes.

## Exact scoped result

For a spacelike unit internal field `V`, define

```text
h = 1 - V V_flat,
K = D_omega V.
```

Requiring both `D_(Omega_V)V=0` and retention of the doubly `V`-orthogonal
block of `omega` uniquely gives

```text
Omega_V^(AB) = omega^(AB) + V^A K^B - K^A V^B,
C = omega - Omega_V = 2 K^[A V^(B].
```

This is a covariant, inverse-coframe-free kinematic reduction. Substitution in
the single D023-type primitive gives

```text
B_V = - integral_Y C^(AB) wedge P_AB
    = -2 integral_Y K^A V^B P_AB.
```

Its dependent variation cancels only the coset projection of the D004
connection momentum. The six stabilizer rows remain generically. On the basic
rank-three polar trace, only `P43/P34` are nonzero, so the mixed connection row
does cancel and

```text
B_V|polar = -(2 pi c/kappa_5) integral_Sigma o_Sigma.
```

The transverse `V` equation is satisfied and the basic polar corner pullback
vanishes. Free rank-preserving coframe variation nevertheless leaves

```text
delta(S_+ + B_V) = -(2 pi c/kappa_5) integral_Sigma delta o_Sigma,
```

so stationarity sets the formal Euler coefficient `c=0`, outside the
stipulated positive-slope branch. The failure is therefore a compulsory
coframe-polarization equation, not an external reference amplitude or a new
polar corner pair.

Off shell, changing continuous `c` changes the covariant scalar
`(D_theta V)^2` and generically the connection-holonomy conjugacy class, so the
isolated `delta omega43` tangent at fixed `V` is not a full gauge tangent.
Nevertheless frozen D005 supplies neither a mixed total cut moment map nor an
observable algebra; no final gauge/superselection/physical classification is
warranted.

This is C027: an exact restricted derived negative benchmark. It does not
establish or refute broad C002/C003 and does not classify all reduction-field
actions.

## Critique and computational disposition

The first derivation critic found one real but non-load-bearing defect: D024's original
Noether identity used an all-plus sign despite the graded movement of a
three-form coframe Euler coefficient past a one-form gauge variation. D024 was
revised, the adverse report retained, and a fresh critic found no remaining
blocking issue. The corrected identity is explicitly guarded by O014's
all-plus mutation.

The first computation-bridge critic then rejected O014's initial 34-assertion
implementation because its load-bearing variation and residual checks were
target-shaped rather than derived. Scientific Computation replaced them with an
explicit primitive expression graph, Leibniz variation, graded IBP, coefficient
extraction, independent D004/polar assemblies, and semantic upstream mutations.
A second critic found one remaining Lorentz-index defect: the `hhP` target used
an unlowered projector, hidden by a purely spatial `V`. The final repair uses
the boosted exact representative `V=(3/4,0,0,0,5/4)`, checks the full matrix and
the witness `(25/8)P01-(15/8)P14`, and requires the historical wrong-sign target
to fail. A third critic found no blocking issue.

O014's current canonical result is `passed`: 46/46 exact assertions, four coset
rows canceled, six stabilizer rows retained, the polar coframe coefficient `-3`
in units of `tau c/kappa_5`, zero transverse `V` residual, zero basic corner
pullback, and six mutations each exiting `1`. It uses exact rational tensors,
sparse free graded algebra, and canonical tuple equality without floats,
sampling, CAS, reusable scientific infrastructure, or Engineer work. It tests
only the encoded finite algebra and remains correlated same-model evidence.

## Hypothesis disposition

- **H002:** weakened in one additional, sharply specified realization. A
  kinematic reduction field does not by itself convert C026 into a viable free
  background; the one induced-connection primitive forces `c=0`. H002 remains
  unsupported because other invariant reduction-field actions and a principled
  tangent category remain open.
- **H003:** strengthened only in its restricted action-class reading. C027 is
  another exact failure of the selected continuum representative, not a
  universal rank-change no-go. Strong H003 remains unproved.
- **H001/H004/H005:** unchanged. The four unevaluated literature maps do not
  alter their status.

## Cycle decision and next discriminator

Close `CY008-reduction-field-literature-evaluation`. Reject the idea that the
kinematic `G/H` reduction plus the single induced-connection polarization term
is the missing complete interface dynamics. Do not proceed to functional Dirac
preservation, moving interfaces, hyperbolicity, or defects around the excluded
positive-slope background.

The next future theory task, if authorized, should first state a bounded action
class and classify the lowest-degree local `SO(1,4)`-covariant polynomial
interface four-forms built from `V`, `D_omega V`, `E`, and curvature/momentum.
The decision quantity is whether any nonredundant term can cancel the C027
coframe residual while retaining free `c>0`, rank three, and a complete gauge
variation, rather than merely introducing another external datum. A separate
future category task may instead test whether D022's finite mixed tangent is
admissible. No O015, experiment, independent verification, or further cycle is
queued here.
