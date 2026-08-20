# Integration and Incidence Literature Map

Date: 2026-08-19
Scope: theorem-targeted search for integration, Stokes, fiber-pushforward, and mixed-dimensional variational machinery applicable to the exact `D002` local model `R^{1,2} x C(S^1 disjoint_union point)` and to actions summed over strata of dimensions 5, 4, and 3.

This packet supports or bounds claims C010 and C011. It is a bounded eight-source map, not a comprehensive review. No source below establishes C010 or C011; they are recorded as `derived` from `D003`, not `literature-supported`.

## The two exact questions

1. **Vertical collapsed-face trace.** Does any established theorem give a nonzero intrinsic trace on the collapsed `S^1` face of the five-dimensional core, for forms that are smooth in the quotient sense?
2. **Direct `5 -> 3` incidence.** Does any established framework supply a canonical incidence/boundary operator from a five-dimensional stratum directly onto a three-dimensional interface, skipping a codimension-one four-dimensional face?

Both answers found are negative in the reviewed literature.

## Evidence map

| Cluster | Primary source | Exact usable result and locator | What it does **not** establish here |
|---|---|---|---|
| Diffeological integration and Stokes | Iglesias-Zemmour (2013), `IglesiasZemmour2013VariationsIntegrals` | Cubic-chain integration `§3.1, p. 1264, Eq. (3.1)`; chain pushforward `§3.3, pp. 1266-1267`; diffeological Stokes `§4.1, p. 1268`; variation of integrals over an arc of cubes `§4.2, pp. 1268-1272, Eqs. (4.1)-(4.2)`. | Stokes returns only the ordinary boundary chain. A rank-deficient four-face collapsed into the three-dimensional interface generates no new three-dimensional incidence term, and no fundamental class or measure is selected. |
| Repairing diffeological de Rham | Kuribayashi (2020), `Kuribayashi2020SimplicialCochain` | Singular de Rham algebra and factor map `§2, before Thm 2.4`; comparison `Thm 2.4`; integration iso `Cor. 2.5`; relation to Iglesias-Zemmour integration `Cor. 2.6(ii)-(iii)`. | A cohomological repair only. It supplies no vertical collapsed-face trace, no `5 -> 3` incidence operator, and no action functional. |
| Mixed-dimensional exterior calculus | Boon, Nordbotten & Vatne (2021), `BoonNordbottenVatne2021MixedDimensional` | Conforming DAG/forest `§2.1, Defs. 1-2`; summed forest integral `§3.1, Eqs. (21), (24)-(25)`; discrete differential and explicit `d_i+1` incidence set `§3.2, Def. 5, Eqs. (29)-(30), Ex. 7`; well-posedness `Thms 4.1-4.2`. | The construction assumes every `d`-manifold lies in the boundary of a `(d+1)`-manifold, i.e. a strictly codimension-one hierarchy. It therefore accommodates `4 -> 3` but not the benchmark's direct `5 -> 3` incidence, and it presumes positive nondegenerate coefficients. |
| Fiber integration at a circle | Bär & Becker (2013), `BarBecker2013DifferentialCharacters` | Fiber-integration hypotheses `Ch. 7, §7.1, Def. 7.1, Eqs. (7.1)-(7.4)`; uniqueness/construction `Thm 7.2, Def. 7.3, Eqs. (7.7)-(7.8)`; oriented circle-bundle pushforward `Ex. 7.15`; thin chains `Ch. 3, Def. 3.1`. | Requires a genuine fiber bundle with closed compact oriented fibers of **fixed** dimension. The `D002` collapse map is not such a bundle at the interface, so the theorem does not license a pushforward across the collapse. Also notes that "smooth space" de Rham properties are extra assumptions, not automatic for diffeological spaces. |
| First-order gravity boundary variation | Corichi, Rubalcava-García & Vukašinac (2014), `CorichiRubalcavaGarciaVukasinac2014Charges` | Variation and Stokes over `partial M` `§II.1, Eqs. (2)-(4)`; adding and varying a boundary term `Eqs. (5)-(8)`; boundary decomposition `Eq. (15)`; explicit Palatini bulk/boundary action `§III.1, Eqs. (36)-(37)`. | An ordinary four-manifold with a codimension-one boundary. It confirms the methodological principle used in `D004`/`D005` (a boundary term must be varied completely and changes the polarization) but supplies no mixed-dimensional or collapsed interface term. |
| Five-dimensional first-order boundary terms | Mora, Olea, Troncoso & Zanelli (2004), `MoraOleaTroncosoZanelli2004FiniteAction` | Five-dimensional first-order Chern-Simons AdS action `§2, Eq. (6)`; bulk equations and explicit four-form surface term `Eqs. (7)-(12)`; boundary condition and on-shell variation `§2.1, Eqs. (13)-(16)`; general odd-bulk/even-boundary construction `§3, Eqs. (17)-(22)`. | The boundary of the five-dimensional manifold is an ordinary four-dimensional hypersurface. It motivates the two-connection/tensorial-difference structure used in `D005` but is not the collapsed three-dimensional incidence, and its transgression theorem is not claimed for `D005`. |
| Intrinsic stratified local models | Ayala, Francis & Tanaka (2017), `AyalaFrancisTanaka2017LocalStructures` | Conically smooth local basics; `C(pt disjoint_union S^1)` appears explicitly as a connected non-pure space `Rem. 2.4.3`; local unzip `Lem. 7.3.5(6)`; resolution of pure spaces `Thm 7.3.8`. | Supplies local models and morphism spaces, not integration, Stokes, a Lorentzian structure, or an action. The resolution theorem covers pure `n`-dimensional stratified spaces, not this non-pure model. |
| Quotient differential forms | Hector, Macías-Virgós & Sanmartín-Carbón (2011), `HectorMaciasVirgosSanmartinCarbon2011DiffeologicalDeRham` | Quotient diffeology, plotwise forms, and exact descent for foliation leaf spaces. | No general singular-quotient descent theorem, no integration, no fundamental class, no changing-dimension Stokes theory. |

## Synthesis against C010 and C011

- **C010 (zero regular collapsed-face trace).** No reviewed theorem contradicts it, and two independently corroborate the mechanism from different directions. Functoriality of pullback through the blowdown forces a quotient-smooth form to have no vertical component at the collapsed face, so its ordinary `S^1`-fiber integral is zero. Bär-Becker independently show that a legitimate fiber pushforward requires a fixed-dimensional bundle, which fails exactly at the interface. This is corroboration of the mechanism, not literature support for the exact claim.
- **C011 (no canonical measure, weights, or incidence).** Iglesias-Zemmour supplies chains and Stokes but no canonical fundamental class; Boon et al. supply a genuine mixed-dimensional variational calculus but only under a codimension-one forest hypothesis that the benchmark violates. Together these locate the missing object precisely: an intrinsic `5 -> 3` incidence operator with declared weights.

Neither claim may be promoted to `literature-supported`.

## Dependence and mismatch warnings

1. Iglesias-Zemmour and Kuribayashi address the same diffeological calculus; Kuribayashi's repair is cohomological and does not add integration data beyond the comparison isomorphism. They are not two independent supports for an action calculus.
2. Boon et al. work in a finite-element/functional-analytic setting with positive nondegenerate coefficients. Transferring their well-posedness theorems to a Lorentzian first-order gravitational action is not licensed.
3. Bär-Becker's `Ex. 7.15` is the closest formal analogue to the wanted circle pushforward, but its hypothesis set is precisely what the collapse violates. Citing it as support for a collapsed pushforward would be a regime error.
4. Corichi et al. and Mora et al. are ordinary fixed-dimensional first-order gravity. They constrain method, not the benchmark's interface.
5. Brasselet-Hector-Saralegi and related stratified-integration sources were identified but remained inaccessible in full text; they are deliberately **not** used as evidence and remain an open lead.

## Remaining literature gaps

1. Integration and a fundamental class on a **non-pure** conically smooth or diffeological local model with a disconnected link.
2. A mixed-dimensional incidence/variational framework admitting codimension-two or collapsed incidence, i.e. direct `5 -> 3`.
3. Moving-stratum and shape variation with corner terms for mixed-dimensional actions.
4. Boundary/transgression terms for first-order gravity where a rank-four exterior meets a rank-five core across a collapsed interface.
5. A Hamiltonian treatment of connection components invisible to a degenerate coframe but carrying nonzero curvature.
6. Lorentzian causal structure and hyperbolic PDE theory on the selected quotient category.

## Next literature action

Only if the enriched boundary-circle route of `D005` is retained: search for edge-mode, Stueckelberg-reference, and corner-charge results in first-order gravity with an eye to whether a fixed reference connection can be traded for a dynamical edge field without introducing physical boundary charge. Broadening the stratified-integration survey has lower value until the enrichment question is settled.
