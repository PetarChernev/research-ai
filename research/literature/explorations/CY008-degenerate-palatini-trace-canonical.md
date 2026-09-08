---
exploration_kind: literature-discovery
status: candidate-leads
question: "Trace-aware boundary and canonical formulations of Palatini/Einstein-Cartan gravity when the pulled-back coframe may change rank"
wave: "CY008"
lens: "degenerate Palatini traces, preboundary reduction, and functional boundary pairings"
explorer: literature-explorer
explorer_model: openai/gpt-5.6-sol
created_at: "2026-08-23"
---

# Literature exploration: degenerate Palatini trace/canonical structures

## Scope and evidence status

Bounded question: which canonical, covariant-phase-space, BV-BFV, geometric-constraint, or adjacent functional-analytic constructions could define one-sided traces, boundary pairings, and presymplectic reduction for independent connection/coframe variables when a timelike-interface pullback can change rank? The lens is the analytic/geometric obstruction behind D015--D017 and C018--C020, not a survey of edge-mode actions, reduction fields, or generic null-boundary charges. Stopping condition was 11 source families after two passes produced no further structural category.

**This is discovery only: all entries are candidate leads, not validated source evidence or claim support.**

## Project anchors and terminology/framework map

Structural fingerprints: polynomial Palatini potential `e^(D-2) delta omega`; no inverse coframe; one-sided trace `T`; duplicated copies constrained by gluing multipliers; a boundary incidence `B=I_C dP`; the missing functional adjoint `T*`; a preboundary two-form whose kernel may change rank; quotient by that kernel only when it is a subbundle and the quotient is smooth; corner residual one-forms; and rank-stratified coframe sectors.

Vocabulary branches:

| Project wording | Search vocabulary encountered |
|---|---|
| boundary trace/adjoint | tangential trace, weak trace, Green formula, transposition, extension/lifting operator, trace dual |
| degenerate pulled-back tetrad | lightlike induced metric, degeneracy constraint, degenerate triad sector, noninvertible tetrad phase |
| nonconstant-rank preboundary form | singular preboundary structure, characteristic distribution not a subbundle, pre-BFV obstruction |
| boundary phase-space reduction | Kijowski--Tulczyjew (KT) construction, geometric constraint algorithm, coisotropic/presymplectic reduction |
| corner data | BF(k)V, pre-Dirac corner structure, Courant/Dirac reduction, residual one-forms |
| duplicated traces/gluing | cutting and gluing, boundary-field projection, BV pushforward, auxiliary/contractible pairs |

## Assigned lens and search trail

This branch combines direct Palatini boundary geometry with adjacent weak-trace and singular-reduction mathematics. It intentionally does not classify normal/reduction-field actions (another gap) or assume a standard nondegenerate hypersurface.

Surfaces inspected: arXiv abstracts and experimental full HTML, Crossref metadata, and DOI landing metadata. Representative queries/pivots: `Palatini-Cartan boundary`; `Palatini-Cartan lightlike`; `degenerate tetrad boundary`; `pre-boundary two form constant rank`; `geometric constraint algorithm boundary functional analytic`; `weak tangential trace differential forms`; `degenerate sector Ashtekar`; then citation pivots from Cattaneo--Schiavina to KT/BV-BFV/corners and from Maxwell trace theory to Green pairings. One queried DOI (`10.1002/mma.189`) was unrelated; the correct Buffa Part-I locator was recovered from Crossref references.

## Candidate source families

| Rank / source family (stable locator) | Exact apparent object handled | Relevance / class | Inspection status; strongest mismatch; cheapest reality test |
|---|---|---|---|
| 1. Canepa--Cattaneo--Tecchiolli, *Gravitational Constraints on a Lightlike Boundary*, [arXiv:2010.14871](https://arxiv.org/abs/2010.14871), [DOI](https://doi.org/10.1007/s00023-021-01038-z) | PC boundary quotient when the **induced metric** is degenerate; weakened structural constraint, extra degeneracy constraint, first/second-class split | Direct neighbor; **convention-dependent/method transfer** | Full HTML sections inspected. Bulk coframe remains an isomorphism and boundary coframe is injective; only metric has one null direction. Test: redo its wedge-map kernel lemmas for rank-2/3 boundary coframes without any inverse.
| 2. Cattaneo--Schiavina, *BV-BFV approach…PCH*, [arXiv:1707.06328](https://arxiv.org/abs/1707.06328), [DOI](https://doi.org/10.4310/ATMP.2019.v23.n8.a3) | Preboundary one-/two-form; BFV descent requires kernel to be a subbundle and smooth reduction; natural PCH BV form has nonconstant-rank obstruction | **Exact structural correspondence** to the project’s regularity question, not to its rank-changing solution | Full HTML inspected. It explicitly assumes nondegenerate tetrads in the classical field space and does not cure rank change. Test: extract the exact rank-jump locus and compare its wedge operators with D015--D017.
| 3. Cattaneo--Schiavina; Canepa--Cattaneo--Schiavina, reduced/boundary PC phase space, [arXiv:1707.05351](https://arxiv.org/abs/1707.05351), [arXiv:2001.11004](https://arxiv.org/abs/2001.11004) | KT reduction of `∫ e^(N-2) δω`; connection quotient by `ker(e^(N-3)∧·)`; structural constraints and BFV algebra | Direct formalism; **regime-limited correspondence** | Abstracts and substantial 2001.11004 HTML inspected. Assumes injective boundary coframe and, for main theorems, nondegenerate boundary metric; wedge-map ranks are fixed. Test: identify every lemma whose proof uses injectivity/nondegenerate `g∂` and recompute ranks on each project stratum.
| 4. Cattaneo--Fila-Robattino--Tecchiolli, *Reduced Dirac Structure…Corners*, [arXiv:2607.28262](https://arxiv.org/abs/2607.28262) | Residual corner one-forms as sections of `TF⊕T*F`; pre-Dirac structure; quotient of invisible directions; reduced Poisson corner space | Direct corner neighbor; **potentially transferable method** | Full HTML overview inspected (recent preprint). Starts from standard PC boundary reduction with nondegenerate coframe. Test: ask whether its “kernel of residual one-forms” construction remains a smooth distribution on a fixed coframe-rank stratum and how it glues across strata.
| 5. Cattaneo--Mnev--Reshetikhin, *Classical BV Theories on Manifolds with Boundary*, [arXiv:1201.0290](https://arxiv.org/abs/1201.0290), [DOI](https://doi.org/10.1007/s00220-014-2145-3) | Bulk-to-boundary projection, preboundary reduction, cutting/gluing, and higher-codimension strata | General framework; **method transfer** | Abstract inspected. Examples are regular gauge/topological theories, not degenerate PCH. Test: locate precise hypotheses on surjective submersion and gluing fiber products; compare directly to D015’s trace-surjectivity and clean-shell assumptions.
| 6. Canepa--Cattaneo--Schiavina AKSZ and Canepa--Cattaneo BV pushforward, [arXiv:2006.13078](https://arxiv.org/abs/2006.13078), [arXiv:2507.06279](https://arxiv.org/abs/2507.06279) | Boundary-first BFV/AKSZ reconstruction and BV pushforward to a boundary-compatible PC theory | **Potentially transferable method** for replacing duplicated trace auxiliaries by a homological reduction | Abstracts inspected. Fixed-dimensional cylinders and ordinary PC nondegeneracy; no weak trace theorem. Test: determine whether D015 copy/multiplier pairs form a genuine contractible BV pair only after a functional trace map is supplied.
| 7. Barbero--Prieto--Villaseñor plus Gotay--Nester--Hinds, [arXiv:1306.5854](https://arxiv.org/abs/1306.5854), [DOI GNH](https://doi.org/10.1063/1.523597) | Geometric constraint algorithm on infinite-dimensional manifolds with spatial boundaries; explicit emphasis on functional domains for irregular theories | Adjacent mathematics; **potentially transferable method** | Abstract and metadata inspected. Linear scalar/Maxwell examples, not nonlinear Palatini or rank-varying bundles. Test: import one collar Sobolev domain and check whether the D017 Hamiltonian differential lies in the range of the presymplectic bundle map.
| 8. Buffa--Costabel--Sheen trace family, [DOI](https://doi.org/10.1016/S0022-247X(02)00455-9); Buffa--Ciarlet Part I, [DOI](https://doi.org/10.1002/1099-1476(20010110)24:1%3C9::AID-MMA191%3E3.0.CO;2-2) | Continuous tangential traces for `H(curl)` on Lipschitz domains, trace ranges, extension operators, integration-by-parts/Green pairing | Adjacent PDE; **potentially transferable method** | Crossref metadata/reference identities inspected, primary text unread. Linear Hilbert complexes use a background metric and fixed Lipschitz boundary; connection is affine and Palatini pairing is polynomial. Test: formulate coframe/connection as vector-valued differential forms in graph spaces and see whether the boundary Palatini wedge pairing is continuous without using the degenerating metric.
| 9. Degenerate Ashtekar sectors: Jacobson--Romano [arXiv:gr-qc/9207005](https://arxiv.org/abs/gr-qc/9207005); Lewandowski--Wiśniewski [arXiv:gr-qc/9609019](https://arxiv.org/abs/gr-qc/9609019), [arXiv:gr-qc/9902037](https://arxiv.org/abs/gr-qc/9902037) | Canonical evolution and constraint closure/preservation on fixed degenerate-triad sectors | **Regime-limited analogy** | Abstracts inspected. Ashtekar variables, often complex/time-gauge, no timelike internal boundary or trace adjoint. Test: compare their rank-sector preservation conditions with preservation of D017’s surviving null primaries, without importing inverse-triad constraints.
| 10. Kaul--Sengupta noninvertible phases, [arXiv:1709.00188](https://arxiv.org/abs/1709.00188), [DOI](https://doi.org/10.1103/PhysRevD.96.104011) | First-order vacuum solution joining invertible and degenerate tetrad phases, finite connection/field strength and torsionful degenerate region | Direct physical neighbor; **regime-limited analogy** | Abstract inspected; related family already noted in the foundation map. No boundary symplectic or functional trace analysis. Test: vary their joined solution in a collar and compute whether the Palatini preboundary kernel has locally constant rank.
| 11. Sjamaar--Lerman singular reduction, [DOI](https://doi.org/10.2307/2944350) | Symplectic reduction yielding stratified symplectic spaces when orbit types vary | Adjacent geometry; **potentially transferable method** | Metadata only. Finite-dimensional Hamiltonian compact-group setting, not an infinite-dimensional presymplectic form with rank-changing coefficients. Test: model a finite Palatini boundary fiber at several coframe ranks and test whether its strata satisfy the orbit-type/frontier pattern needed for a stratified quotient.

## Proposed dictionary to D015--D017

| D015--D017 object | Candidate source object | Qualification |
|---|---|---|
| one-sided `T_±` | boundary restriction/preboundary projection; in weak theory, tangential trace into a negative-order trace space | The gravity sources mostly assume smooth restrictions; Buffa supplies the missing analytic pattern, not a ready Palatini theorem. |
| duplicated `(epsilon_±,Omega_±)` | independent preboundary/cut fields or an extended/BV auxiliary sector | CMR/AKSZ suggest a gluing or contractible-pair interpretation, conditional on an actual trace map and clean reduction. |
| gluing multiplier `(A_±,B_±)` | conormal/Lagrange-multiplier data imposing a fiber-product matching condition | No inspected source proves D015’s multiplier sector is globally clean at rank change. |
| degenerate triad/coframe | lightlike metric degeneracy constraint (lead 1), or fixed Ashtekar rank sector (lead 9) | Neither is identical: lead 1 keeps `e:TΣ→V` injective; lead 9 changes canonical variables and boundary meaning. |
| functional adjoint `T*` | transpose of weak trace under a Green pairing; boundary functional injected into a bulk dual graph space | Lead 8 is the strongest analytic template. The pairing should be the polynomial wedge/internal pairing, not an inverse-coframe `L2` product. |
| preboundary quotient | `F_pre/ker(ω_pre)` (BV-BFV/KT), or a rank-stratified/Dirac reduction | Exact dictionary only on a fixed constant-rank stratum; across rank jumps it is conjectural. |

## Regime mismatches and hidden nondegeneracy assumptions

1. “Degenerate boundary metric” is not “degenerate pulled-back coframe”: the lightlike PC paper explicitly takes the bulk coframe as an isomorphism and its boundary restriction as an injective map.
2. The standard PC boundary theorems use constant ranks of wedge maps, injective boundary coframes, smooth kernel subbundles, complements, and smooth quotients. These are precisely the assumptions that may fail here.
3. Maxwell trace spaces presuppose fixed-dimensional Lipschitz domains and metric-defined graph norms. Only their trace/dual/Green architecture is portable.
4. Singular symplectic reduction does not automatically cover a presymplectic form whose rank changes for reasons unrelated to group orbit type.
5. None of the inspected sources distinguishes the project’s intrinsic boundary field from two independently duplicated one-sided traces with gluing constraints in a rank-changing Palatini theory.

## Negative searches / early falsification

- Direct searches for `degenerate tetrad + boundary` mostly returned solution-building papers, not trace-aware Hamiltonian analysis.
- `preboundary two-form` finds the BV-BFV vocabulary, but no inspected source provides a general quotient theorem for nonconstant-rank kernels.
- The lightlike-boundary result is not the requested rank-changing timelike case; treating it as exact would silently replace coframe-rank loss by metric nullness.
- Degenerate Ashtekar work concerns invariant fixed-rank sectors and does not define one-sided timelike traces.
- Ordinary Sobolev scalar trace theorems are too weak: the needed objects are differential-form/connection traces and a Green pairing compatible with the Palatini potential.

## Ranked handoffs

1. **Lightlike PC boundary construction (lead 1) — both `literature` and `theorist`.** Literature: extract exact field-space assumptions and wedge-map kernel/rank lemmas, including mixed-type boundaries. Theorist: replace injective `e|Σ` by each D015--D017 coframe-rank stratum and determine whether weakened structural and degeneracy constraints still exist without inversion.
2. **Weak tangential trace/Green pairing (lead 8) — both.** Literature: verify exact trace ranges, surjectivity/right inverses, and Green formula in the primary papers. Theorist: propose the smallest metric-independent graph spaces for `(e,omega)` on one collar and derive the transpose `T*` appearing in a D017 preservation bracket.
3. **PCH preboundary obstruction plus stratified/Dirac reduction (leads 2, 4, 11) — both.** Literature: identify the precise constant-rank and smooth-quotient hypotheses and any proposed remedies. Theorist: compute the finite fiberwise preboundary kernel at every relevant coframe rank and decide whether fixed-rank reductions form compatible strata or whether rank change destroys the quotient.

## Epistemic status

Primary full text was inspected only for leads 1--4; several other entries rest on abstracts or metadata and require focused validation. The proposed dictionaries are conjectural. Nothing in this report is claim evidence, and no lead should enter the working picture before the requested `literature` note and/or `theorist` derivation is completed and synthesized by the director.
