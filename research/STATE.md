# Research State

Last updated: 2026-08-19T13:57:00Z

## Current question

Can an exact local `d=4 <-> d=5` Lorentzian dimensional theory be defined without a physical ambient bulk, supplied with a complete covariant first-order variational principle, and shown provisionally consistent at the linearized classical level? The current F0-A subproblem is now an explicit circle-collapse benchmark rather than an abstract quotient.

## Current working picture

- **Explicit benchmark:** `D002` defines `X=[U x I x S1]/~`, with complete circle collapse for `s<=0`, and two smooth blow-downs with profiles `rho_1=ell exp[-(L/s)^2]` and `rho_2=ell exp[-(L/s)^4]` on `s>0`.
- **Topology/dimension (C007, derived):** both blow-downs are homeomorphic to `X`. The regular core is five-dimensional, the regular exterior four-dimensional, and the timelike interface stratum three-dimensional. Neighborhoods of interface points have local model `R^{1,2} x C(S1 disjoint_union point)`. At the interface, covering dimension is 5, quotient-algebra derivation dimension 4, and ambient-horn derivation dimension 6; no category-independent singular-point dimension exists.
- **Resolution test (C008, derived):** the two ambient-horn smooth structures are not equivalent under the canonical resolution map. Their algebras obey `C_infinity,2` strictly contained in `C_infinity,1` strictly contained in the profile-independent final quotient algebra. The final quotient diffeology is therefore the provisional intrinsic smooth structure; this is a research choice, not a proof of physical uniqueness.
- **Forms/data survival (C009, derived):** the actual quotient-diffeological form equalizer removes `dtheta+A` but admits `rho(dtheta+A)`, horizontal `A`, `F=dA`, and horizontal mixed connection components. Fiber labels are erased outside; independently retained nonzero `F` or coframe-relative mixed curvature is not erased by ordinary `U(1)`/Lorentz gauge.
- **State-space fork:** in a coframe-only state, exterior `A/F` is absent as independent data. In a first-order state with independent connection, it survives unless an explicit forgetful equivalence or future equations/boundary conditions remove it. Forgetting is not yet a constraint-generated gauge symmetry.
- **Foundation status:** F0-A is not passed. Integration/Stokes, causal structure, physical category selection, and topology on the full field space remain missing; no action or dynamics has been defined.

## Active hypotheses

- **H001 — Intrinsic stratified continuum dynamics:** gains limited kinematical support from the final quotient diffeology and exact form descent, but still lacks integration, causality, and dynamics.
- **H002 — Resolution-based gauge-equivalent dynamics:** its naive ordinary-gauge form is disfavored because canonical horn smoothness is profile-dependent and exterior curvature survives ordinary gauge; an action-generated enlarged reduction remains possible.
- **H003 — Continuum rank-change obstruction:** gains concrete warning mechanisms, not a no-go; the bare quotient/form calculus itself is consistent in the tested local sense.
- **H004/H005:** downstream Hopf spin-statistics competitors remain unchanged and should not influence F0 action design.

## Highest-value claims

1. **C001–C003 (conjecture, critical):** complete state category, variational principle, and healthy linearized dynamics remain the main gates.
2. **C009 (derived, critical):** exact collapse does not by itself remove independently retained exterior connection curvature.
3. **C007 (derived, high):** explicit quotient topology and category-dependent interface dimensions.
4. **C008 (derived, high):** canonical inequivalence of the two profile-induced ambient smooth structures.
5. **C004–C006 (conjecture, critical; deferred):** full Hopf topology/holonomy and stable defect.

## Strongest evidence

- **Complete derivation:** `research/derivations/D002.md` proves C007–C009 with exact topology, local-ring, mean-value, diffeological descent, rank, and gauge-covariance arguments.
- **Procedurally separated checks:** reports for C007, C008, and C009 each conclude `supported but not independently verified`. They reconstructed the results by alternate arguments and forced wording/index/gauge-scope corrections now incorporated into D002 and the ledger. Same-model sessions are not genuine independent verification.
- **Canonical diagnostic:** `D001` remains the necessary dynamical test: only a regular zero-charge first-class reduction can upgrade an exterior forgetful relation to gauge.
- **Numerical evidence:** none; none is needed for C007–C009.

## Known contradictions

- No ledger claim is contradicted after the verification-driven corrections.
- **Resolution tension:** identical quotient topology does not imply identical smooth structure or core geometry. The two horn profiles have different circumference and canonical differential structures despite identical interface jets.
- **Gauge tension:** the bare quotient removes exterior fiber labels, while ordinary gauge does not remove nonzero curvature of an independently retained connection. Coframe-only omission, forgetful equivalence, ordinary gauge, and dynamical exclusion are inequivalent.
- **Dimension tension:** interface stratum, derivation, and covering dimensions differ. Any assertion of “the” interface dimension without choosing a notion is invalid.
- The final quotient form calculus accepts `rho(dtheta+A)`, whereas the ordinary ambient-restricted horn form module does not; the two calculi cannot be silently combined.

## Open verification tasks

1. Obtain a genuinely independent mathematical review of C007–C009, especially the local-ring dimensions and effective descent of forms; current checks are only procedural.
2. Test whether the final quotient diffeology supports a resolution-independent integration/Stokes functional compatible with the `5/4/3` incidence structure.
3. Determine whether the kernel-pair collapse and exterior connection-forgetting relation can arise as regular zero-charge first-class gauge or instead leave surface charges/transition data.
4. After an action exists, independently reconstruct its complete first variation and presymplectic current before changing C002/C003.
5. C004/C005 verification remains blocked on a full physical configuration space and microscopic quantum bundle.

## Running/next experiments

- **Running:** none.
- **Next analytic benchmark:** construct candidate integration maps on the core, exterior, and interface and derive the exact Stokes/incidence formula; compare both horn resolutions and the final quotient structure.
- **Then:** use the resulting calculus to write and vary the lowest-derivative first-order action while retaining all independent connection components.
- **Only after variation:** apply the `D001` Legendre/constraint/presymplectic rank table and a tiny frozen-coefficient principal-symbol calculation.
- A numerical defect boundary-value problem remains premature.

## Literature gaps

1. Integration and Stokes theorems on a non-pure conically smooth/diffeological local model with a disconnected link.
2. Moving-stratum/shape variation and incidence terms for mixed-dimensional actions.
3. First-order gravity boundary/transgression terms when a rank-four exterior meets a rank-five core through a codimension-two/codimension-one interface.
4. Hamiltonian treatment of connection components invisible to a degenerate coframe but carrying nonzero curvature.
5. Lorentzian causal and hyperbolic PDE theory on the selected quotient category.

## Next recommended actions

Ranked by expected information gain and dependency:

1. **Construct and test a resolution-independent integration/Stokes calculus on the exact D002 benchmark (single best next action).** Predeclare core, exterior, and interface measures; derive incidence signs and boundary terms; compare the two profiles; and identify which connection forms are integrable observables.
2. **Choose the minimal first-order field content and derive a complete action variation.** Keep the independent connection explicit; test coframe-only truncation as a separate theory rather than an implicit gauge choice.
3. **Apply the D001 reduction/limit-commutation diagnostic and principal-symbol test.** This decides whether the required forgetful relation can be dynamical gauge or is an obstruction.
4. **Only after F0:** return to a static defect and full Hopf configuration-space topology.
