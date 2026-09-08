---
exploration_kind: literature-discovery
status: candidate-leads
question: "How can a reduction/reference/edge sector classify D023's finite normal-plane 43 holonomy as gauge, superselected, or physical?"
wave: "CY008"
lens: "edge/corner phase space, G/H reduction, reference connections, and holonomy sectors"
explorer: literature-explorer
explorer_model: openai/gpt-5.6-sol
created_at: "2026-08-23"
---

# Literature exploration: edge/corner reference-connection connections

> **DISCOVERY ONLY.** Every item below is a candidate lead, not validated source evidence. This report cannot support a claim-ledger entry.

## 1. Bounded question, anchors, and distinct lens

The bounded question is whether known boundary gauge constructions supply a *classification procedure* for D023's finite `43` connection tangent/holonomy after an explicit `SO(1,4)/SO(1,3)` reduction field is added. The structural anchors are

* `B_ref=-∫_Y(omega_+-barOmega)^{AB}∧P^(5)_{AB}` and the tensorial connection difference;
* a fixed seed orbit `barOmega=h Omega0 h^-1-dh h^-1`;
* a rank-three momentum whose only polar components are `P43=-P34`;
* the orbit equation `D_barOmega P=0` and corner potential `-∫ zeta P`;
* circle holonomy `Hol(barOmega)~exp(2 pi c T43)`; and
* the missing field selecting `H=SO(1,3)` inside `G=SO(1,4)`.

This lens is distinct because it searches for the *quotient and moment-map machinery* that separates gauge nulls, symplectic leaves/superselection labels, and charged edge pairs. It does not revisit collapse regularity, bulk existence, or Hopf defects.

## 2. Terminology/lineage map and search trail

Vocabulary branched as follows:

`normal/reduction field` → section of `P/H` or `P×_G(G/H)` → de Sitter compensator, Stelle–West field, nonlinear realization, Cartan geometry, spontaneous symmetry breaking without a Higgs potential;  
`seed frame` → dressing field, Stueckelberg field, boundary frame, covariance spurion, residual gauge;  
`barOmega` → second connection, background connection, transgression pair, dressed/composite connection;  
`43 holonomy` → conjugacy-class boundary condition, representation variety, group-valued moment map, large-gauge/winding sector;  
`corner P` → Lorentz surface charge, flux, moment map, normal-frame charge;  
`classification` → extended phase space, symplectic reduction, flux superselection, edge-mode quotient, BV–BFV reduction.

Surfaces inspected were the shared repository anchors, arXiv abstract/metadata pages and API records, one DOI metadata response, and a Project Euclid locator (which returned 404). Queries/pivots included: `SO(1,4) SO(1,3) compensator Stelle-West`, `bundle reduction G/H Higgs field`, `dressing field method principal bundle reduction`, `transgression two connections gauge invariant boundary`, `tetrad gravity corner internal normal Lorentz charges`, `normal plane edge modes`, `edge modes superselection flux rotations`, `group-valued moment maps flat connections boundary holonomy`, and `BV BFV corners gluing`. Direct conjunction searches for `SO(1,4) edge mode`, `Palatini reference connection corner`, and `Stueckelberg corner moment map` were attempted after the broader passes but rate-limited; they did not yield inspected results. Stopping occurred at 11 source families after the reduction, edge-phase-space, and holonomy passes covered all new structural categories.

## 3. High-value candidate source families

“Direct” means overlap in objects, not proof for D023. Inspection is explicitly limited.

| # | Candidate family and stable locator | Relevance / correspondence class | What was inspected; strongest mismatch |
|---|---|---|---|
| 1 | Stelle & West, *Spontaneously broken de Sitter symmetry and the gravitational holonomy group*, PRD 21 (1980), [DOI](https://doi.org/10.1103/PhysRevD.21.1466); Wise, *Symmetric Space Cartan Connections…*, [arXiv:0904.1738](https://arxiv.org/abs/0904.1738), [DOI](https://doi.org/10.3842/SIGMA.2009.080); Wise, *Geometric role…*, [arXiv:1112.2390](https://arxiv.org/abs/1112.2390) | **Direct; convention-dependent mapping.** `G/H` field can select Lorentz reduction without a symmetry-breaking potential; Cartan split supplies `H` connection plus coset part. | DOI metadata for Stelle–West and abstracts for Wise. Their gravity is ordinary fixed-dimensional Cartan geometry, not a rank-changing timelike interface or corner phase space.
| 2 | Pagels, *Gravitational gauge fields and the cosmological constant*, PRD 29 (1984), [DOI](https://doi.org/10.1103/PhysRevD.29.1690) | **Direct; potentially transferable action template.** A constrained internal vector/compensator is a candidate variational realization of the reduction. | Identity/locator only, not primary text. Its Euclidean/de Sitter conventions and bulk action may not furnish the required boundary kinetic term.
| 3 | Anabalón, *Some considerations on the MacDowell–Mansouri action*, [arXiv:0805.3558](https://arxiv.org/abs/0805.3558), [DOI](https://doi.org/10.1088/1126-6708/2008/06/069) | **Direct-adjacent; method transfer.** Connects Stelle–West compensators to a gauged WZW construction, suggesting that a reduction field can acquire boundary dynamics rather than remain a spurion. | Abstract only. A consistent truncation in AdS gravity is not D023's Palatini interface, and WZW degrees may over-enlarge the benchmark.
| 4 | Zając, *The dressing field method in gauge theories—geometric approach*, [arXiv:2105.09919](https://arxiv.org/abs/2105.09919) | **Direct; convention-dependent mapping.** Gives bundle-level criteria under which a dressing reduces gauge symmetry and configuration/phase bundles. | Abstract/API summary only. A dressing is not automatically a new physical field; D023 varies `h`, so residual symmetry and boundary symplectic terms must be recomputed.
| 5 | Mora, Olea, Troncoso & Zanelli, *Transgression forms and extensions of Chern-Simons gauge theories*, [arXiv:hep-th/0601081](https://arxiv.org/abs/hep-th/0601081), [DOI](https://doi.org/10.1088/1126-6708/2006/02/067) | **Direct-adjacent; method transfer.** A genuinely two-connection, gauge-invariant action with dictated boundary term is the nearest lineage for `omega-barOmega`. | Abstract/API summary only; the project already knows this broad family. Chern–Simons transgression uses invariant polynomials and two curvatures; D023's linear `K∧P(E)` is only transgression-like.
| 6 | Donnelly & Freidel, *Local subsystems in gauge theory and gravity*, [arXiv:1601.04744](https://arxiv.org/abs/1601.04744), [DOI](https://doi.org/10.1007/JHEP09(2016)102) | **Direct-adjacent; transferable classification.** Boundary gauge frame and its electric-flux momentum form an extended phase space; gravity adds a conformal normal frame and normal-plane surface symmetry. | Abstract only. Their boundary is codimension two in a standard Cauchy slice and mainly metric/Yang–Mills, not D023's codimension-one timelike Palatini interface plus circle.
| 7 | Freidel, Geiller & Pranzetti, *Edge modes of gravity I–II*, [arXiv:2006.12527](https://arxiv.org/abs/2006.12527), [arXiv:2007.03563](https://arxiv.org/abs/2007.03563), DOIs [I](https://doi.org/10.1007/JHEP11(2020)026), [II](https://doi.org/10.1007/JHEP11(2020)027) | **Most direct corner lead; convention-dependent mapping.** In tetrad gravity the internal normal and corner coframe participate in the corner phase space and Lorentz charges; different formulations/potentials represent different corner algebras. | Abstracts only. Their internal normal selects a foliation/corner structure in `SO(1,3)`, not an `SO(1,4)/SO(1,3)` reduction, and their coframe is nondegenerate in the standard regime.
| 8 | Speranza, *Local phase space and edge modes for diffeomorphism-invariant theories*, [arXiv:1706.05061](https://arxiv.org/abs/1706.05061), [DOI](https://doi.org/10.1007/JHEP02(2018)021) | **Analogical; transferable method.** Normal-plane `SL(2,R)` surface transformations and Noether-generated edge algebra offer a test for whether a normal-plane tangent is charged or null. | Abstract only. These are spacetime diffeomorphism normal-plane transformations, whereas `T43` is initially an internal compact rotation/coset generator.
| 9 | Riello, *Edge modes without edge modes*, [arXiv:2104.10182](https://arxiv.org/abs/2104.10182) | **Analogical; transferable quotient test.** Reduced symplectic gluing, flux superselection sectors, functional connections, and flux rotations directly distinguish edge coordinates from gauge-invariant bulk data. | Abstract only. Core exposition is Maxwell; the non-Abelian discussion is an overview, and Lorentz/de Sitter groups are noncompact.
| 10 | Alekseev, Malkin & Meinrenken, *Lie group valued moment maps*, JDG 48 (1998), [DOI](https://doi.org/10.4310/jdg/1214460866) | **Exact structural correspondence for holonomy models, analogical physically.** Boundary holonomy can be a group-valued moment map; fixing a conjugacy class then defines a reduction leaf rather than merely “freezing a connection.” | Stable DOI located; full-page fetch failed, primary text uninspected. Standard theory is clearest for compact groups/flat connections; D023 has `SO(1,4)`, nonzero Palatini momentum, and no established quasi-Hamiltonian two-form.
| 11 | Cattaneo, Mnev & Reshetikhin, *Classical BV theories on manifolds with boundary*, [arXiv:1201.0290](https://arxiv.org/abs/1201.0290), [DOI](https://doi.org/10.1007/s00220-014-2145-3) | **Method transfer.** BV–BFV systematically carries bulk gauge data to boundaries and higher-codimension strata and tests gluing/coisotropic reduction. | Abstract only. Examples are ordinary gauge/topological theories; adapting degenerate Palatini gravity and the mixed-dimensional trace is substantial.

## 4. Candidate dictionary and classification observable

| D023 object | Candidate source object |
|---|---|
| `barOmega` | transgression's second connection (#5); connection induced/dressed after choosing a `G/H` section (#1, #4) |
| seed orbit `(Omega0,h)` | boundary frame/dressing with residual right action (#4, #6); WZW/Stueckelberg variable (#3); choice of holonomy leaf (#10) |
| normal/reduction field | section `V` of `P×_G G/H`, with stabilizer `H` (#1–2); corner internal normal as a lower-dimensional analogue (#7) |
| `43` tangent/holonomy | coset/normal-plane component of the `G` connection; circle Wilson loop; group-valued moment map whose conjugacy class may label a leaf (#10) |
| corner moment map `P43` | electric flux/Lorentz surface charge (#6–7); ordinary Lie-algebra moment map dual to edge-frame displacement; infinitesimal limit of a group-valued moment map (#10) |

The cheapest proposed discriminator is to compute the *total* cut presymplectic form after adding `V` and pull it to all constraints. A `43` transformation is **gauge** only if its vector is a null direction and its total moment map (bulk plus interface/corner) vanishes for admitted parameters. It is a **superselection label** if conjugacy class/flux labels invariant symplectic leaves preserved by the observable algebra, with no conjugate edge coordinate inside one leaf. It is **physical edge data** if a nondegenerate `(edge frame, P43)` pair or nonzero Hamiltonian corner charge survives reduction. These are proposed tests, not literature-established conclusions for D023.

## 5. Known mismatches and failure modes

1. Internal `SO(1,4)` reduction, spacetime normal-frame symmetry, and diffeomorphism surface symmetry are three different groups; identifying them would be a category error.
2. `SO(1,4)/SO(1,3)` is de Sitter-type and noncompact. Compact quasi-Hamiltonian results and positive-definite orbit intuition may fail globally.
3. A constrained compensator can select `H` yet still have no boundary momentum; conversely a WZW/dressing completion may add more physical modes than wanted.
4. A fixed holonomy conjugacy class can be boundary data, a symplectic leaf, or a topological sector. Calling it “superselected” requires the reduced observable algebra and allowed large gauges.
5. D023's rank-three pullback and vanished coframe components violate standard nondegenerate tetrad assumptions. Corner rank and simplicity results cannot be imported unchanged.
6. Changing the boundary potential changes polarization and possibly represented corner symmetries; classification is action- and boundary-condition-dependent.

## 6. Informative negative searches

No inspected source directly combined all four features: first-order Palatini gravity, a covariantly transforming full reference connection, an `SO(1,4)/SO(1,3)` boundary reduction field, and classification of a finite circle holonomy. Exact-phrase searches were too narrow, while `normal holonomy` was dominated by differential-geometric holonomy rather than canonical edge data. `Spontaneous symmetry breaking` mostly implied a Higgs potential; the useful pivot was **compensator/nonlinear realization/Cartan reduction**. `Edge mode quotient` was more productive under **symplectic gluing**, **flux superselection**, and **dressing field**. The failed/rate-limited direct conjunctions should be retried through INSPIRE or citation trails, not treated as evidence of absence.

## 7. Ranked handoffs

1. **Stelle–West/Cartan reduction + tetrad corner phase space (#1, #7) — both `literature` and `theorist`.** Exact question: *Can a boundary compensator `V∈SO(1,4)/SO(1,3)` be varied without a potential so that the induced Lorentz connection and coset component reproduce a covariant completion of D023, and what is the resulting corner symplectic pairing of `delta V` with `P43`?* Literature should extract exact transformation/action formulas and corner-normal assumptions; theory should derive the D023 specialization.
2. **Group-valued moment-map/holonomy reduction (#10) — both.** Exact question: *Does the completed circle sector admit a quasi-Hamiltonian form with `Hol_43` as group-valued moment map, so that fixing its conjugacy class is a genuine reduction leaf rather than an externally frozen seed?* First check noncompact-group and nonflat-connection hypotheses; then attempt the smallest polar-sector two-form and reduction.
3. **Reduced gluing versus extended edge frames (#6, #9) — `theorist`, after focused `literature` extraction if selected.** Exact question: *After including both bulk Gauss terms and the reduction field, can the D023 edge-frame contribution be rewritten in gauge-invariant bulk/interface variables, and does `43` flux define a preserved superselection sector or a surviving canonical pair?*

## Epistemic status

Only abstracts, metadata, and project anchors were inspected; no candidate's equations were validated against its primary full text. Correspondences remain convention-dependent or methodological except for the abstract mathematical resemblance of boundary holonomy to a group-valued moment map, whose hypotheses are untested. **Nothing in this report is claim evidence.**
