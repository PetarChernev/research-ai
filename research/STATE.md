# Research State

Last updated: 2026-08-20T00:02:00Z

## Repository integrity notice (resolved 2026-08-20)

- Work was briefly performed with the worktree checked out at the `main` baseline instead of the research branch `reseach/hopf-solitons`. Switching back restored all committed artifacts; nothing was lost.
- Two artifacts produced during that window, `research/results/verification/C008-2026-08-19-anthropic.md` and `research/results/verification/C009-2026-08-19-anthropic.md`, were **deleted**. They verified against a stale session transcript and a prompt-supplied claim string respectively, and asserted (falsely, about the actual repository) that `D002.md` and the ledger were missing. They were never cited in the ledger. Superseded by the genuine cross-provider `-anthropic-r2.md` reports, which were produced after the branch was corrected and verified against the real `D002.md` and ledger. See `research/DECISIONS.md` for the full incident record.
- `uv run --locked python scripts/validate_research_state.py` now **passes** (`valid: true`, 0 errors). The four legacy same-model reports (`C004-`, `C007-`, `C008-`, `C009-2026-08-19.md`) were patched with `verifier_model`/`originating_models` frontmatter required by the current schema; their content was untouched. Under `--strict`, 8 expected warnings remain (`verifier model also materially produced the claim`, `verifier shares a provider with at least one originating model`) — these correctly and honestly flag that those four reports are same-model/same-provider procedural-separation-only checks, consistent with their `"supported but not independently verified"` outcome. This is intended validator behavior, not a defect.

## Current question

Can an exact local `d=4 <-> d=5` Lorentzian dimensional theory be defined without a physical ambient bulk, given a complete covariant first-order variational principle, and shown provisionally consistent at the linearized classical level? Following `D003`–`D005`, the live F0 question has narrowed to: **what is the minimal enrichment beyond the bare quotient that yields a covariant, field-space-integrable interface action, and is that enrichment physical or gauge?**

## Current working picture

- **Benchmark.** `D002` fixes `X=[U x I x S1]/~` with exact circle collapse for `s<=0`, plus two smooth blow-downs `rho_1=ell exp[-(L/s)^2]` and `rho_2=ell exp[-(L/s)^4]`.
- **Kinematics is settled and partly verified.** Both blow-downs are homeomorphic to `X` (C007). The two ambient-horn smooth structures are canonically **inequivalent**, with `C_inf,2` strictly inside `C_inf,1` strictly inside the profile-independent final quotient algebra (C008, verified). The final quotient diffeology is therefore the provisional intrinsic smooth structure. Form descent is exactly characterized: `dtheta+A` does not descend, while `rho(dtheta+A)`, `A`, `F=dA`, and horizontal mixed `omega^{4a}` do (C009, verified).
- **The bare quotient cannot carry dynamics.** It selects no measure, no relative stratum weights, and no nontrivial collapsed-fiber incidence (C011). Every compactly supported descended four-form has **zero** trace on the resolved core boundary, so there is no core-to-exterior Stokes flux (C010).
- **This propagates directly into gravity.** For bare five- and four-dimensional Einstein-Cartan/Palatini actions, the five-dimensional presymplectic boundary potential pushes forward to **zero** through both available channels, while the four-dimensional one is generically nonzero, leaving an uncancelled boundary variation (C012). Completion attempts are classified: fixed data give no transition equation; a pure matching multiplier forces `P^-_{ab}=0`, incompatible with a nondegenerate induced triad; only a generalized trace or retained boundary-circle data can supply a finite momentum-matching equation (C013).
- **The natural repair is real but enriching.** The desired finite core-momentum term is not a closed field-space one-form under free coframe or vertical-`eta` variation, so it is not an action variation by itself (C014). The fully covariant reference-free two-connection action is integrable and Lorentz invariant yet **fails**, forcing `P^-_{ab}=0` and induced coframe rank at most one. Splitting off a fixed covariantly transforming reference connection gives a nondegenerate branch with `Q=g.P^-` and `2 pi ell_*/kappa_5 = 1/kappa_4`, at the cost of reference/edge data, a companion coframe equation, and a fixed vertical circle period (C015).
- **Physics checks that passed.** In the regular fixed-radius limit the same construction reproduces the standard Kaluza-Klein relation `kappa_4 = kappa_5/(2 pi R)`, and the collapsed-interface coupling `ell_* = kappa_5/(2 pi kappa_4)` is its exact counterpart. Dimensions, orientation signs, and every `2pi` are explicit throughout `D003`–`D005`.
- **Foundation status.** F0-A is partly answered negatively for the *bare* structure and remains open for an enriched one. F0-B and F0-C are untouched: no complete moving-interface action, no constraint analysis, no hyperbolicity result.

## Active hypotheses

- **H001 — Intrinsic stratified continuum dynamics.** Weakened. The strong form, an autonomous action from the quotient calculus, is excluded by C010–C011. Survives only as "intrinsic state space plus declared incidence data."
- **H002 — Resolution-based gauge-equivalent dynamics.** Substantially disfavored as *pure gauge equivalence*. C013 and C015 show the economical reductions force `P^-_{ab}=0` and triad degeneracy. Survives only as an enriched theory whose extra boundary data have undetermined charge status.
- **H003 — Continuum rank-change obstruction.** Now splits. A **restricted form** (no canonical bare-quotient continuum dynamics) is well supported by C010–C012 and C015. The **strong form** (no admissible continuum theory at all) is *not* established, because `D005` exhibits an explicit nondegenerate enriched branch.
- **H004 / H005 — Hopf spin-statistics competitors.** Unchanged and still downstream. They must not influence F0 action design.

The live discriminator among H001/H002/H003 is now a single question: is the `D005` edge sector regular zero-charge first-class gauge, or does it carry physical boundary degrees of freedom?

## Highest-value claims

| Status | Claims |
|---|---|
| `verified` (cross-provider) | **C008** smooth-structure inequivalence; **C009** connection data survive exact collapse |
| `derived`, unverified | **C007** quotient topology/dimensions; **C010** zero collapsed-face trace; **C011** no canonical measure/incidence; **C012** Palatini boundary mismatch; **C013** completion classification; **C014** non-integrability of the momentum term; **C015** reference-free failure and fixed-reference repair |
| `conjecture` | **C001–C003** the three F0 gates; **C004–C006** Hopf topology, holonomy selection, stable defect |

C009, C012, and C015 are the load-bearing results: together they say exact dimensional collapse neither erases independent connection data nor supplies the incidence needed to match it, and repairing that requires genuinely new boundary structure.

## Strongest evidence

- **Cross-provider verification.** `C008-2026-08-19-anthropic-r2.md` and `C009-2026-08-19-anthropic-r2.md`: `anthropic/claude-sonnet-4-6` attacking `openai/gpt-5.6-sol` work, each with an alternate reconstruction (a Fourier/Taylor-coefficient route to the `C^1` obstruction; an independent derivation of the descent conditions before reading `D002`) and ten to twelve failed falsification attacks each.
- **Complete derivations.** `D002` (topology, local rings, descent), `D003` (exact Stokes/incidence obstruction), `D004` (general-`D` Palatini variation, both vertical channels, Lovelock extension), `D005` (bundle-covariant master action, field-space curl, exact failure and repair). All exact, no approximations.
- **Literature corroboration of the gap.** `research/literature/INTEGRATION_MAP.md`: eight primary sources confirm that no established theorem supplies a collapsed-fiber pushforward or a direct `5 -> 3` incidence operator. Bär-Becker's fiber integration requires a fixed-dimensional bundle; Boon et al.'s mixed-dimensional calculus assumes strict codimension-one hierarchy.
- **Diagnostic standard.** `D001` remains the canonical test any completion must pass: only a regular zero-charge first-class reduction can upgrade a forgetful relation to gauge.
- **Numerical evidence.** None. No experiment is yet warranted.

## Known contradictions

- No ledger claim is contradicted, and `research_status` reports no major contradictions.
- **Resolution tension.** Identical quotient topology does not imply identical smooth structure or core geometry; the two profiles differ despite identical interface jets.
- **Gauge tension.** Coframe-only omission, forgetful equivalence, ordinary gauge, and dynamical exclusion are four inequivalent operations. Conflating them is the most likely source of error in this program.
- **Dimension tension.** Interface stratum, derivation, and covering dimensions are 3, 4, and 5 respectively. No category-independent "interface dimension" exists.
- **Calculus tension.** The final quotient form calculus admits `rho(dtheta+A)` while the ambient-restricted horn module does not; the two must not be silently combined.
- **Enrichment tension (open).** `D005`'s repair is profile-independent yet strictly enriches the quotient with a marked circle, an edge isomorphism `g`, multipliers, a length scale, and a reference connection. Whether this is legitimate physics or a concealed reintroduction of the fifth dimension is unresolved.

## Open verification tasks

1. **C010–C015 have no verification report at all.** Six `derived`, mostly critical claims rest on single-model derivations. This is the largest current evidence gap and should be closed by `verifier-anthropic` against the primary artifacts `D003`, `D004`, `D005`.
2. **C007** has only supportive reports; `independent_verification` remains `inconclusive`.
3. **C004** remains `inconclusive`, blocked on a defined full configuration space.
4. **C005** has never been verification-tested.
5. Any future action must have its complete first variation and presymplectic current independently reconstructed before C002 or C003 status changes.

## Running/next experiments

- **Running:** none. No `ENNN` experiment exists.
- **Next analytic step:** the `D006` canonical edge-sector test called for at the end of `D005` — a `2+1` split of the interface/edge sector on a planar rank-three background, computing primary constraints, the presymplectic form and its rank, Lorentz moment maps, and corner charges, for both the fixed-reference and Stueckelberg-reference variants.
- **First plausible numerical work:** a finite-dimensional mode/rank table from that canonical analysis, checkable by independent linear algebra. Not yet a field-theory simulation.
- A defect boundary-value problem remains premature.

## Literature gaps

1. Integration and a fundamental class on a **non-pure** stratified/diffeological model with a disconnected link.
2. A mixed-dimensional incidence framework admitting collapsed or codimension-two incidence, i.e. direct `5 -> 3`.
3. Moving-stratum and shape variation with corner terms for mixed-dimensional actions.
4. Boundary/transgression terms for first-order gravity where a rank-four exterior meets a rank-five core across a collapsed interface.
5. Hamiltonian treatment of connection components invisible to a degenerate coframe but carrying nonzero curvature.
6. Lorentzian causal structure and hyperbolic PDE theory on the selected quotient category.
7. Edge-mode, Stueckelberg-reference, and corner-charge results in first-order gravity, needed to interpret `D005`.
8. Stratified-integration sources such as Brasselet-Hector-Saralegi remain inaccessible in full text and unused.

## Next recommended actions

Ranked by information gain, dependency, and cost:

1. **Repair repository validity (blocked, needs user).** Add `verifier_model`/`originating_models` to the four legacy reports and remove the two void wrong-branch reports. Requires relaxing the deny rule on `research/results/verification/**` or a manual fix.
2. **Verify C010–C015 cross-provider (highest scientific value).** Six unverified critical claims now carry the program's main conclusion. Route to `verifier-anthropic` with `D003`/`D004`/`D005` as primary artifacts.
3. **Run the `D006` canonical edge-sector test (the decisive discriminator).** Its outcome directly separates H002 from H003: regular zero-charge first-class implies the enrichment is gauge and H002 revives; an unavoidable physical edge pair or second-class constraint supports the restricted H003.
4. **Only after F0 resolves:** return to a static Hopf defect, the full configuration space, and C004–C006.
