# W001-total-gauss synthesis

Date: 2026-08-22

## Frozen objective and regime

This breadth-first wave asked for the minimum bulk-plus-interface Lorentz
generator and boundary polarization needed to classify C016's rank-ten
Stueckelberg shell block. All branches used the fixed timelike interface,
basic theta-independent persistent `SO(1,3)` sector, fixed circle period,
planar rank-three branch `b=kappa_4^{-1}`, `H(K)=0`, and the D005 shell

```text
Delta e=Delta omega=0, lambda=-Q, mu=0, Q=g.P^-.
```

Moving interfaces, full `SO(1,4)`, nonbasic modes, global/large gauge,
hyperbolicity, and Hopf physics were excluded. Parallel producers and all
internal critics used `openai/gpt-5.6-sol`; procedural agreement is not
independent evidence.

## Evidence inventory

| Branch | Distinct route | First-pass result | Internal critique | Integrated disposition |
|---|---|---|---|---|
| D007 | Direct canonical bulk/interface split | Exterior `-P^-` cancels `Ad_(g^-1)Q`; proposed shared Palatini/edge primary rows | `revision-required` | Retain the weak cut cancellation. Park the direct-matrix route until one trace/gluing phase-space presentation is fixed; closure and presentation-independent nonfactorization were overclaimed. |
| D008 | Covariant phase-space moment map | Derives total cut moment map and the same on-shell cancellation without ADM | `revision-required` | **Survivor and primary analytic route for C017.** The cancellation survived sign, orientation, and dressing attacks. Seed/corner data are necessary but not sufficient; primary stabilization and mixed brackets remain required. |
| D009 | Collapsed-core limiting flux | Regular 5D persistent Palatini flux is proportional to `rho` and vanishes at exact collapse; nonzero `Q` is enriched incidence data | `no-blocking-issue-found` | **Survivor.** Excludes a hidden regular core cancellation in the frozen class. Correct the minor explanation of the horizontal `A` term if the derivation is revised. |
| D010 | Linearized Dirac chain | Exterior Gauss tangency couples edge `dQ` to `delta P^-`; proposed exact core shared-row blocker | `revision-required` | Retain exterior nonautonomy and the need for a combined primary-preservation step. Prune the unproved core `dP_+` overlap and any claim that proper-boundary gauge establishes five physical pairs. |
| D011 | Symplectic quotient/stabilizers | Separates the two-dimensional coadjoint stabilizer from the one structural `T12` null; proposes rank bounds and product countermodels | `revision-required` | Retain the stabilizer-versus-kernel lemma and the empty interface-only zero level. Prune the singularity-robust survivor bound and the claim that a cotangent compensator itself demonstrates removal. |
| D012 | Polarization/counterterm portfolio | Exact corner shifts preserve rank; fixed nonzero `Q` pulls the isolated block to rank four; fixing `u` restricts it away | `revision-required` | Retain these local polarization guardrails. Fixed momentum retains projected coframe equations, and the displayed total moment map is only a necessary sign target unless supplied by D008/C017. |
| D013 | Seed-frame left/right action | Right seed relabeling removes duplicate `(u,a0)` factorizations but leaves the orbit variable; unrestricted seed variation forces `Q=0` | `revision-required` | Retain the dressing algebra and reference-choice classification. Canonical endpoint cancellation and any stabilizer charge require an explicit induced seed/corner polarization. |
| D014 | Adversarial no-go | Claimed a universal no-go was refuted by formal cancellation and five-generator templates | `revision-required` | **Pruned as a proof/counterexample route.** The formal ansätze show algebraic underdetermination but are not constructed action/Gauss completions; the artifact also conflates the `dQ` null with the coadjoint stabilizer. The actual no-go remains unresolved. |

Critique paths are `research/critiques/D007-2026-08-22-openai-01.md`
through `D014-2026-08-22-openai-01.md`.

## Integrated result

The strongest wave result is the new, tightly scoped C017:

1. The regular five-dimensional persistent core cut momentum contains the
   collapsing leg `E^4=rho eta`; ordinary and normalized circle pushforwards
   vanish exactly at `rho=0`.
2. In the unshifted D004/D005 polarization, the exterior bulk cut moment map is
   `-P^-`, while the interface contribution is
   `-Ad_(g^-1)lambda`.
3. On `lambda=-Q` and `Q=g.P^-`, the total exterior coefficient is exactly
   zero. This is a matching-constraint-surface cancellation, not an off-shell
   identity and not a consequence of `H(K)=0`.
4. The cancellation rules out treating C016's partial interface moment map by
   itself as a surviving physical Lorentz charge. It does **not** make the
   rank-ten shell form vanish, prove that boundary Lorentz transformations are
   admissible gauge, establish first-class closure, or decide physical versus
   second-class survivors.

O007 machine-checks only this finite coefficient/sign/dressing bridge. Its
canonical result is `passed` with 28/28 exact assertions, exact identity and
nonidentity Lorentz dressings, ordinary/Haar and fixed-radius controls, and four
effective mutations. O007 shares `research/computation/exact_graded/` and the
OpenAI producer model with earlier obligations; it is correlated supporting
evidence, not independent confirmation.

## Aligned conventions and dependence

- All surviving formulas use `epsilon_0123=epsilon_01234=+1`, ordered
  antisymmetric-pair sums, the D004 incident orientation, ordinary circle
  normalization absorbed into `b=2pi gamma`, and
  `delta_alpha omega=-D alpha`.
- The fixed-radius control gives the standard relation
  `kappa_4=kappa_5/(2pi R)`; it is a noncollapsed limit, not evidence for exact
  collapse.
- D007-D014 inherit the D005 action, D006 shell potential, and D004 signs. The
  critiques inherit the same source chain and model.
- C016's Opus report independently covers the earlier restricted interface
  rank/sign bridge. It did not review D007-D014, C017, or O007 and supplies no
  independent verification of this wave.
- O007 ran from a dirty worktree and fingerprints its spec, implementation,
  shared kernel, wrapper, and locked environment in its canonical result.

## Preserved contradictions and failure modes

1. **Zero total moment map versus nonzero shell form:** both are true. The first
   is a constraint-surface statement for the complete Lorentz generator; the
   second is an interface presymplectic statement before total reduction.
2. **Coadjoint stabilizer versus presymplectic null:** planar nonzero `Q` has
   stabilizer `span(T03,T12)`, but only `T12` is a structural group null of the
   free-`Q` shell form; `T03` pairs with the radial area variation. This does not
   itself produce five admissible first-class generators.
3. **Boundary fixing versus gauge removal:** fixing `u`, `Q`, or `e` can reduce
   rank but changes the tangent space and, generally, the Euler system. It is
   not evidence that the original variables were gauge.
4. **Trace presentation:** an intrinsic bulk trace and duplicated boundary
   variables with gluing constraints are not interchangeable until their
   canonical matrices are explicitly related. This is the main unresolved
   bridge in D007/D010.
5. **Regular core flux versus enriched incidence:** the former is zero; the
   latter supplies nonzero `Q`. Relabeling `Q` as an omitted regular bulk trace
   would double count or change the state space.

## Pruning and shortlist

Pruned as decisive routes in their present form:

- a universal obstruction inferred from rank ten or a partial nonzero charge;
- a formal compensator/cut potential presented as an admissible completion
  without a spacetime action, companion variations, and Gauss generator;
- interface-only zero-level reduction at nonzero `Q`;
- additive rank counting between the edge block and an unspecified bulk
  primary matrix;
- removal by fixing boundary variables and then calling them gauge;
- further searches for a hidden regular five-dimensional core flux.

Surviving ingredients for convergence:

1. D008+D009+C017+O007: exact total cut coefficient and regular-core limit.
2. D013: left/right seed architecture, after narrowing endpoint claims.
3. D012: polarization guardrails, after correcting fixed-momentum equations.
4. D010 plus its critique: the exterior tangent matching that makes an
   edge-only Dirac count nonautonomous.
5. D011's stabilizer/kernel lemma, used only as local algebra rather than a
   reduction theorem.

## Smallest decisive assertions still open

The survivors reduce the next scientific task to four linked assertions:

1. Choose one explicit trace-aware canonical presentation for the bulk and
   interface fields and show its equivalence, if claimed, to an alternative
   gluing presentation.
2. Assemble the planar core/exterior Palatini defining-primary matrix plus the
   interface block and determine which persistent core rows actually survive
   the regular collapsed pullback.
3. Perform the first preservation step, retaining every torsion/coframe or
   temporal-coframe equation that couples to the five `dQ` directions, and
   compute the relevant Schur complement/brackets without assuming an inverse
   coframe.
4. Declare the left exterior and right seed-frame gauge actions and temporal/
   lateral corner polarization, then test differentiability, total first-class
   closure, and the reduced rank.

No current finite check can decide these assertions because their mathematical
representation is not yet fixed. A new obligation is warranted only after the
trace-aware primary system is derived. Building reusable canonical or PDE
infrastructure now would be premature.

## Best next decision

Fan in to a focused convergence cycle, not another breadth wave. The next
derivation should freeze one trace/gluing phase-space presentation and derive
the combined planar Palatini-plus-interface primary matrix and first
preservation step, with the D013 seed/corner declaration included from the
start. A cheap exact check should then target the resulting trace-aware matrix
and bracket ranks. If the Lorentz sector cannot close without the nominally
frozen Hamiltonian/diffeomorphism equations, record that coupling as the
decisive blocker and widen only then.
