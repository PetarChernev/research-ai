---
exploration_kind: literature-discovery
status: candidate-leads
question: "Which Lorentzian causal and hyperbolic-PDE frameworks could test a future gauge-fixed linearized 4/5-dimensional quotient system?"
wave: "CY008"
lens: "mixed-dimensional hyperbolicity, transmission, edge propagation, and energy-preserving interconnection"
explorer: literature-explorer
explorer_model: openai/gpt-5.6-sol
created_at: "2026-08-23"
---

# Literature exploration: mixed-dimensional hyperbolicity

> **NON-EVIDENTIARY METHODS MAP.** Every item below is a candidate lead. Metadata, abstracts, search records, and structural analogies are not source evidence and support no project claim.

## 1. Bounded question and distinct lens

The bounded question is how to test a *future* gauge-fixed C003 linearization on the D002 local object, where Lorentzian `5D` and `4D` open strata meet at a timelike `3D` stratum and a circle/reduction sector may disappear. No candidate operator presently exists. I therefore map tests for principal-symbol hyperbolicity, branchwise characteristics, traces, incoming-mode counts, interface power balance, energy estimates, and determinism.

This lens is PDE/causal rather than action design, canonical classification, or topology. It intentionally distinguishes (i) fixed-dimensional hyperbolic transmission, (ii) evolution on graphs/edges, (iii) elliptic mixed-dimensional complexes, (iv) signature change, and (v) genuine dimension change. I did not inspect sibling reports.

## 2. Terminology/framework map and search trail

Structural anchors were D002's local model `R^{1,2} x C(S1 disjoint union {*})`, timelike `Sigma`, branch dimensions `5/4/3`, D017's missing functional trace/adjoint, and C003's future principal symbol and energy norm. Vocabulary branches were:

- **Hyperbolic boundary/transmission:** symmetric or Friedrichs systems; maximally nonnegative/dissipative boundary subspaces; characteristic boundary; constant multiplicity; Kreiss--Lopatinski condition; boundary flux form; anisotropic trace spaces.
- **Mixed dimension:** 3D--1D coupling; dimensional reduction; Wentzell/dynamic boundary conditions; PDE on networks/metric graphs; vertex scattering.
- **Singular geometry:** conic/edge manifolds; compressed characteristic set; generalized broken bicharacteristics; diffraction; edge pseudodifferential calculus.
- **Interconnection:** port-Hamiltonian; effort/flow variables; Dirac structure; passivity and power balance.
- **Causality:** spacetime with timelike boundary; Lorentzian length space; time-separation function; Cauchy temporal splitting.

Queries/pivots included `symmetric hyperbolic transmission interface incoming modes`, `characteristic boundary constant multiplicity trace theorem`, `Friedrichs system globally hyperbolic timelike boundary`, `PDE coupling domains different dimensions hyperbolic`, `3D 1D wave coupling energy`, `wave equation edge manifold diffraction`, `port-Hamiltonian systems graphs networks`, `Lorentzian causal stratified space`, `dynamic Wentzell boundary field`, and the literal searches `dimension changing Lorentzian PDE`, `hyperbolic PDE stratified space dimension jump`. Surfaces inspected: repository source notes, arXiv abstract records, Crossref metadata/abstracts, and DOI metadata. Stopped at **10 families** after a second pass produced no new structural category.

## 3. Candidate source families

| # | Source family and stable locator | Equation type | Relevance/class | Inspection status |
|---:|---|---|---|---|
| 1 | Kreiss, “Initial boundary value problems for hyperbolic systems” (1970), [DOI](https://doi.org/10.1002/cpa.3160230304); Secchi, “Linear symmetric hyperbolic systems with characteristic boundary” (1995), [DOI](https://doi.org/10.1002/mma.1670181103) | First-order strongly/symmetric hyperbolic IBVP | **Method transfer.** Boundary symbol, stable subspace, compatibility and energy estimate are the baseline incoming-mode audit. | DOI metadata; Secchi abstract (weighted Sobolev loss in normal direction); primary texts unread. |
| 2 | Ginoux & Murro, “On the Cauchy problem for Friedrichs systems on globally hyperbolic manifolds with timelike boundary,” [arXiv:2007.02544](https://arxiv.org/abs/2007.02544), [DOI](https://doi.org/10.57262/ade027-0708-497) | Friedrichs/symmetric hyperbolic systems on Lorentzian manifolds with timelike boundary | **Potentially transferable method**, closest Lorentzian energy framework: admissible boundary conditions and Hadamard well-posedness. | ArXiv metadata and abstract inspected; full text unread. |
| 3 | Formaggia, Gerbeau, Nobile & Quarteroni, “On the coupling of 3D and 1D Navier–Stokes equations...” (2001), [DOI](https://doi.org/10.1016/S0045-7825(01)00302-4) | Evolutionary fluid models coupled across different-dimensional descriptions | **Convention/model-dependent mapping.** Candidate vocabulary for characteristic-variable matching and dimension-reduced interface data. | DOI bibliographic record only; primary text unread. |
| 4 | Boon, Nordbotten & Vatne, “Functional Analysis and Exterior Calculus on Mixed-Dimensional Geometries,” [arXiv:1710.00556](https://arxiv.org/abs/1710.00556), [DOI](https://doi.org/10.1007/s10231-020-01013-1) | Mixed-dimensional de Rham/Hilbert complex, predominantly elliptic | **Method transfer only.** Recursive trace spaces, incidence signs, and Stokes pairing could organize an interface energy form. | Existing project note reports full-text inspection. Not a hyperbolic result; direct `5→3` incidence absent. |
| 5 | Mugnolo, *Semigroup Methods for Evolution Equations on Networks* (2014), [DOI](https://doi.org/10.1007/978-3-319-04621-1); Kuchment, “Quantum graphs I” (2004), [DOI](https://doi.org/10.1088/0959-7174/14/1/014) | Wave/evolution equations and differential operators on metric graphs with vertex conditions | **Regime-limited analogy.** Vertex trace vectors and scattering/Kirchhoff conditions make incoming/outgoing counts explicit. | Book and article metadata only; contents/theorems uninspected. |
| 6 | van der Schaft & Maschke, “Port-Hamiltonian Systems on Graphs” (2013), [DOI](https://doi.org/10.1137/110840091) | Hamiltonian/passive dynamics interconnected by graph incidence and Dirac structures | **Method transfer.** Interface conditions can be tested as a maximal power-conserving/dissipative relation between branch ports. | Crossref abstract and metadata inspected; article unread. Abstract is finite/open-graph generality, not specifically hyperbolic PDE. |
| 7 | Melrose, Vasy & Wunsch, “Propagation of singularities for the wave equation on edge manifolds,” [arXiv:math/0612750](https://arxiv.org/abs/math/0612750) | Wave equation on fixed-dimensional manifolds with edge singularities | **Potentially transferable microlocal method.** Compressed cotangent geometry and diffraction are candidates for branchwise characteristic continuation at the conical interface. | ArXiv abstract/metadata inspected; full text unread. |
| 8 | Kunzinger & Sämann, “Lorentzian length spaces,” [arXiv:1711.08990](https://arxiv.org/abs/1711.08990); Aké, Flores & Sánchez, “Structure of globally hyperbolic spacetimes-with-timelike-boundary,” [DOI](https://doi.org/10.4171/rmi/1201) | Synthetic causality; causal splitting with timelike boundary | **Heuristic-to-method lead.** Supplies candidate definitions of causal order/time separation and a branchwise Cauchy slicing test without demanding a smooth metric everywhere. | Both abstracts/metadata inspected; primary texts unread. |
| 9 | Zahn, “Generalized Wentzell boundary conditions and quantum field theory” (2018), [DOI](https://doi.org/10.1007/s00023-017-0629-3) | Bulk hyperbolic field coupled to dynamical boundary degrees of freedom | **Regime-limited analogy.** A disappearing bulk sector might leave an interface reduction field with its own kinetic/trace equation rather than a bare boundary condition. | Identity/locator found through publisher reference metadata; abstract/full text unread. |
| 10 | Alty & Fewster, “Initial-value problems and signature change,” [arXiv:gr-qc/9501026](https://arxiv.org/abs/gr-qc/9501026), [DOI](https://doi.org/10.1088/0264-9381/13/5/024) | Scalar/Dirac evolution through Lorentzian-to-Kleinian signature change | **Regime-limited warning, not dimension change.** Tests whether matching/self-adjointness still fails continuous dependence. | Existing project note reports full-text inspection and exact instability locators. |

No family is an exact structural correspondence. Families 1--2 are the strongest operator-level methods; 5--7 and 9 are controlled analogies; 4 is elliptic infrastructure; 8 concerns causality rather than PDE hyperbolicity.

## 4. Candidate dictionary to future C003 objects

| Future project object | Candidate source object | Cheapest reality test |
|---|---|---|
| Gauge-fixed principal symbol `P(x,xi)` | Friedrichs/symmetric symbol `A^mu xi_mu`; edge-wave compressed principal symbol | On each open stratum, exhibit a positive symmetrizer and real semisimple characteristic roots. Then test whether it remains uniform as `s→0`. |
| Branchwise characteristics | Stable/incoming eigenspaces of the normal boundary matrix; generalized broken bicharacteristics at an edge | Freeze tangential frequency and plot/count normal roots on both branches, including glancing and zero-speed roots. |
| Interface trace | Sobolev/anisotropic trace vector; graph endpoint value; mixed-dimensional recursive trace | Prove continuity of each proposed one-sided trace in one declared energy space. D017's finite incidence map is insufficient. |
| Incoming modes | Negative/positive spectral subspaces of the boundary flux matrix (orientation dependent) | Compare rank of imposed interface relations with total incoming dimension for every nonzero tangential covector. |
| Reduction field | Wentzell boundary variable or port state; graph vertex state | Derive, rather than posit, whether it has an interface evolution equation and whether its energy is positive, null/gauge, or indefinite. |
| Energy estimate | Friedrichs boundary flux inequality; port-Hamiltonian power balance; semigroup dissipativity | Integrate the branchwise symmetrized energy, retain every `Sigma` flux, and ask whether interface equations make the sum conservative or maximally dissipative without derivative loss. |

The proposed port dictionary is `branch trace ↔ effort/flow port`, `incident orientation ↔ signed graph incidence`, and `Palatini/interface pairing ↔ boundary power form`. Its strongest mismatch is that a Dirac interconnection guarantees algebraic power balance, not strong hyperbolicity, constraint propagation, or positivity of gravitational physical modes.

## 5. Regime mismatches and failure modes

1. **Dimension versus signature:** Alty--Fewster acquire an elliptic/negative-spectrum sector; D002 removes a spacelike circle while retaining one time direction. Their instability cannot be imported.
2. **Boundary versus singular junction:** Families 1--2 assume a fixed-rank bundle over a manifold-with-boundary. D002 has two branches of unequal dimension and no established common hypersurface bundle.
3. **Elliptic versus evolutionary:** Boon et al.'s complex and trace theory does not provide a hyperbolic energy estimate; its codimension-one forest does not directly encode `5→3`.
4. **Fixed ambient dimension:** edge calculus resolves geometric singularities within a fixed-dimensional manifold; D002's physical quotient has an open lower-dimensional stratum and a disconnected cone link.
5. **Networks suppress tangential microlocal structure:** graph vertex counts are finite-dimensional and miss glancing, surface waves, gauge constraints, and higher-dimensional trace loss.
6. **Nonuniform symmetrizer:** even branchwise strong hyperbolicity may fail uniformly if the symmetrizer degenerates with the collapsing radius or if characteristic multiplicity changes.
7. **Over/underdetermination:** the number of incoming modes can jump when a field sector disappears. A fixed interface law may overconstrain one side or leave free zero-speed data.
8. **Constraints:** an energy estimate for a gauge-fixed evolution does not show reduction/Palatini constraints propagate. Conversely, treating disappearing variables as gauge without a regular generator can conceal nondeterminism.
9. **Trace mismatch:** ordinary `H^s` traces may not exist for characteristic boundaries; Secchi's abstract explicitly signals weighted anisotropic normal regularity.
10. **Causality without dynamics:** Lorentzian length-space axioms may define order/time separation but do not supply Green operators or uniqueness on this stratification.

## 6. Negative searches

- Literal `dimension-changing Lorentzian hyperbolic PDE` and `hyperbolic PDE stratified space dimension jump` produced no credible direct theorem for a `5D/4D` open-stratum junction with a disappearing tangent/field sector.
- Searches for “mixed-dimensional PDE” were dominated by elliptic fracture/porous-flow complexes or by numerical dimensional reduction, not Lorentzian well-posedness.
- “Signature change” is abundant but structurally wrong unless used only as a failure-control.
- “Causal stratified space” did not reveal, in this pass, a framework combining synthetic causality, differential traces, and hyperbolic Green operators on the D002 cone link.
- “Port-Hamiltonian on graphs” yielded a useful power-balance language, but the inspected abstract does not establish infinite-dimensional hyperbolic PDE interconnection or changing fiber rank.

## 7. Ranked handoffs

1. **Ginoux--Murro plus Kreiss/Secchi — both `literature` and `theorist`.** Literature: extract the exact admissible-boundary subspace, flux form, trace regularity, uniformity, and mode-count hypotheses. Theorist: for a toy two-branch first-order system with unequal field ranks, determine whether doubling `Sigma` as two timelike boundaries plus one interface relation yields a maximally dissipative relation. **Decisive question:** can the summed boundary flux be controlled with exactly as many interface conditions as incoming modes when one branch has extra characteristic fields?
2. **Port-Hamiltonian/graph interconnection plus Wentzell dynamics — both.** Literature: validate whether PDE ports/dynamic boundary states (not merely finite graph ODEs) admit generation and energy theorems. Theorist: derive the minimal power form for a disappearing reduction sector and test maximal isotropy versus maximal dissipativity. **Decisive question:** does adding a reduction field close energy balance without adding an uncontrolled physical interface mode?
3. **Melrose--Vasy--Wunsch edge propagation — both.** Literature: extract the geometric hypotheses, compressed characteristic set, and domains used for the wave energy. Theorist: test whether `C(S1 disjoint union {*})` can enter any comparable edge calculus or fails because the link is disconnected/nonmanifold and branch dimensions differ. **Decisive question:** is there a legitimate compressed cotangent/edge-symbol object whose bicharacteristics encode both branches, or must the project use a transmission operator on a disjoint union instead?

## Epistemic status

This report records candidate methods, not validated statements about C003. Only the repository notes for Boon et al. and Alty--Fewster report full-text inspection; the new leads are abstract/metadata-level or unread. The future operator, gauge, symmetrizer, trace spaces, and interface equations are undefined, so no correspondence can yet be established. Focused `literature` must validate source regimes and `theorist` must derive or falsify each dictionary before any lead enters the working picture.
