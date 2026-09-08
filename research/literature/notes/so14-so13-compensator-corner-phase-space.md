---
citation_key: "focused-so14-so13-corner-validation"
title: >-
  SO(1,4)/SO(1,3) reduction fields and tetrad-gravity corner normals:
  evidence and non-transfer to D023
authors:
  - "Derek K. Wise"
  - "Laurent Freidel"
  - "Marc Geiller"
  - "Daniele Pranzetti"
  - "K. S. Stelle"
  - "P. C. West"
year: 2009
doi: "10.3842/SIGMA.2009.080"
arxiv: "0904.1738"
url: "https://arxiv.org/abs/0904.1738"
date_accessed: "2026-08-23"
---

# Evidence packet: SO(1,4)/SO(1,3) compensator and corner phase space

## Question investigated

Do the five specified primary-source items establish (a) a constrained
`SO(1,4)` reduction field selecting `SO(1,3)` and an inverse-coframe-free
connection split, and (b) a varied internal normal in a tetrad-gravity corner
symplectic form or Lorentz moment map? What, if anything, survives the mismatch
with D023's fixed interface, rank-three pullback, compact-circle `43` holonomy,
and exact `4<->5` rank change?

## Search strategy

On 2026-08-23 I first read the project anchors named in the task. I then read
the complete arXiv HTML texts (not merely abstracts) for `0904.1738`,
`1112.2390`, `2006.12527`, and `2007.03563`, searching within their relevant
bundle/Cartan, ECH, normal decomposition, corner potential, Lorentz charge,
simplicity, and edge-mode sections. I checked publication metadata through
arXiv/Crossref. Searches for the APS full text of Stelle--West through the DOI,
APS PDF/landing page, Crossref, INSPIRE, OpenAlex, and OSTI did not yield an
accessible full text. Crossref and INSPIRE metadata plus the publisher abstract
were inspected; no equation or page-content claim below is attributed to that
paper. No citation-chain item was needed.

## Source identity

1. K. S. Stelle and P. C. West, **“Spontaneously broken de Sitter symmetry and
   the gravitational holonomy group,”** *Phys. Rev. D* **21** (1980)
   1466--1488, DOI `10.1103/PhysRevD.21.1466`, stable DOI URL
   <https://doi.org/10.1103/PhysRevD.21.1466>. **Metadata/publisher abstract
   only.** INSPIRE record 7888 also reports preprint `ICTP-78-79-19`.
2. Derek K. Wise, **“Symmetric Space Cartan Connections and Gravity in Three
   and Four Dimensions,”** *SIGMA* **5** (2009) 080, arXiv:`0904.1738v2`, DOI
   `10.3842/SIGMA.2009.080`, <https://arxiv.org/abs/0904.1738v2>. **Full text.**
3. Derek K. Wise, **“The geometric role of symmetry breaking in gravity,”**
   *J. Phys.: Conf. Ser.* **360** (2012) 012017,
   DOI `10.1088/1742-6596/360/1/012017`, arXiv:`1112.2390v1` (2011),
   <https://arxiv.org/abs/1112.2390v1>. **Full four-page arXiv text.** The
   publication metadata was subsequently validated mechanically against the
   DOI record.
4. Laurent Freidel, Marc Geiller, and Daniele Pranzetti, **“Edge modes of
   gravity. Part I. Corner potentials and charges,”** *JHEP* 11 (2020) 026,
   arXiv:`2006.12527v3`, DOI `10.1007/JHEP11(2020)026`,
   <https://arxiv.org/abs/2006.12527v3>. **Full text.**
5. Same authors, **“Edge modes of gravity. Part II. Corner metric and Lorentz
   charges,”** *JHEP* 11 (2020) 027, arXiv:`2007.03563v1`, DOI
   `10.1007/JHEP11(2020)027`, <https://arxiv.org/abs/2007.03563v1>. **Full
   text.**

## Claims supported

### Reduction/compensator sector

**Wise 2009 (fixed reduction, not a compensator theory).** Section 2 defines a
reductive homogeneous space by an `H`-invariant split
`g = h + p`, with `[h,h] subset h` and `[h,p] subset p`; for symmetric spaces
also `[p,p] subset h` (eq. (1) and surrounding text). Section 3 then states

`A = omega + e`, with `omega in Omega^1(P,h)` and `e in Omega^1(P,p)`,

and gives `F = R + (1/2)[e,e] + d_omega e` (eq. (3)). For de Sitter in
spacetime dimension `n`, eqs. (4)--(5) give `G=SO(n,1)`,
`H=SO(n-1,1)`, `g=h+p`; the displayed block formulas are
`A^a_b=omega^a_b`, `A^a_n=e^a/ell`, and
`A^n_a=-epsilon e_a/ell`. This split is algebraic and uses no inverse coframe.

The blocking assumption is explicit in the same section: the composite
`TM -> g -> g/h`, called `e` in eq. (2), must be a linear isomorphism on every
tangent space; hence `dim M=dim(G/H)`. Thus this source's **Cartan geometry** is
nondegenerate and fixed-dimensional. It does not introduce or vary a field
`V`, nor give a `delta V` boundary pairing.

**Wise 2011 (bundle reduction field).** The text says a Cartan geometry can be
viewed as a principal `G` connection together with a section `y` of the
associated `Y` bundle, and specializes to
`Y = G/H = SO(4,1)/SO(3,1)`. It writes

`I[A,y] = integral tr(F_y wedge star_y F_y)`,

where `y` is locally de-Sitter-valued, `F_y` is the part of `F` valued in the
stabilizer algebra `g_y ~= so(3,1)`, and `star_y` is its Hodge operator. Earlier
paragraphs state `Y ~= G/G_y`, that `G_{g y}=g G_y g^{-1}`, and that different
choices are related `G`-equivariantly. Directly at bundle level, therefore,
`y` transforms in the associated `G/H` fiber and selects its conjugate Lorentz
stabilizer. The paper identifies Stelle--West as making the action fully gauge
invariant by dynamically breaking with such a field.

This supports a constrained reduction field (equivalently an ambient vector
representative with fixed norm after choosing the standard hyperboloid model),
but **the fixed-norm vector formula and an explicit `V -> gV` equation are not
printed in this short source**. It also does not print the `V`-dependent
projectors that split `A`; the precise bridge is instead supplied by combining
its stabilizer projection `F_y` with Wise 2009's split after choosing the
reduction. That combination remains an interpretation, not one displayed
formula in either paper.

**Status of the field.** In Wise 2009 the reduction `H` is fixed bundle data,
not a field. In Wise 2011 `y` is an argument of `I[A,y]` and is described as a
dynamical symmetry-breaking/Goldstone field; full `G` covariance makes it
locally gauge/Stueckelberg-like, but the paper does not perform constraint or
degree-of-freedom analysis, so it does not establish whether global or boundary
components are physical. It derives no presymplectic potential and no pairing
for `delta y`.

**Stelle--West limitation.** Its publisher abstract supports only that the
Goldstone field gives coordinates in an internal (anti-)de Sitter space and
that vierbein/spin connection arise from nonlinear field redefinition. The
accessible abstract actually names `SO(3,2)` and internal anti-de Sitter space,
not the requested `SO(1,4)` de Sitter convention. Without the full text, its
exact constraints, transformations, equations, and field status are
unvalidated here.

### Tetrad corner sector

**Bulk assumptions.** Part I sec. 3.2 begins with an `R^4` coframe `e^I` **with
inverse** `hat e_I`, defining a Lorentzian metric, and independent Lorentz
connection. Eqs. (3.21)--(3.25) give
`L_ECH=(1/2)E_IJ[e] wedge F^IJ`,
`E_IJ=(*+beta)(e wedge e)_IJ`; the text explicitly says the torsion equation
implies zero torsion *when the coframe is invertible*, yielding the unique
torsionless connection. Part II sec. 3, eqs. (3.1)--(3.4), again constructs
`n^I=hat n contracted with e^I`, uses the dual frame, imposes `n^2=sigma`, and
defines the nondegenerate induced coframe/metric. These are not degenerate-bulk
or rank-changing assumptions.

**Normal pairing and moment map.** Part II eqs. (5.1)--(5.4) split the ECH
potential and give the corner terms

`Theta_ECH^S = - integral_S [sigma E~_I delta n^I
                              +(beta/2)e~_I wedge delta e~^I]`,

`Omega_ECH |_on-shell = sigma integral_S delta E~_I wedge delta K~^I
 - integral_S [sigma delta E~_I delta n^I
                +(beta/2)delta e~_I wedge delta e~^I]`.

For a spacelike Cauchy slice (`sigma=-1`), eqs. (5.16), (5.20)--(5.21) write
the relative corner pair as
`Theta_ECH/GR=integral_S(E~_I delta n^I-(beta/2)e~_I wedge delta e~^I)` and
`Omega_ECH/GR=integral_S(delta E~_I wedge delta n^I
-(beta/2)delta e~_I wedge delta e~^I)`. Part I already summarizes the same in
eqs. (3.46)--(3.48) and explicitly says `(E~,n^I)` is nontrivial only when the
internal normal is included in phase space rather than gauge-fixed.

The Lorentz moment map is equally explicit: Part I eqs. (3.32)--(3.34) give
`H_ECH^S[alpha]=(1/2) integral_S alpha_IJ E^IJ`; eqs. (3.36)--(3.40) give its
Lorentz current algebra. Part II eqs. (2.12)--(2.14) repeat the charge, while
eqs. (5.33)--(5.34) show it is Hamiltonian for the relative corner symplectic
structure. Thus a varied internal normal can genuinely be paired at a corner
and contribute to a Lorentz moment map in this formulation.

**Polarization dependence/caveats.** Part II eqs. (5.15)--(5.21) show ECH and
canonical GR share a bulk structure but differ by this corner structure; sec.
7 explains that fixing the frame or changing the relative potential can kill
Lorentz charges. Eqs. (7.3)--(7.18) instead add independent edge variables and
a Lorentz frame `phi`, with a first-class dressed gluing condition. The result
is therefore action-, potential-, boundary-condition-, and polarization-
dependent, not a universal normal kinetic term.

**Corner rank.** Their corner `S` is a codimension-two two-surface. Geometric
interpretation assumes the pullback coframe has rank two and a spacelike,
nondegenerate metric: Part II eqs. (6.9)--(6.10) identify
`q_ab=e~_a^I e~_b^J eta_IJ`, and sec. 6.6 explicitly requires
`det Q(D)>0` for a spacelike surface. Some algebraic formulas can be written
before imposing simplicity, but the claimed tetrad-gravity geometry and area
interpretation do not cover a noninjective/degenerate corner coframe.

## Exact evidence location

- Wise 2009, §§2--3, especially eqs. (1)--(5): reductive split, Cartan
  connection decomposition, curvature decomposition, and the explicit
  nondegenerate soldering-isomorphism assumption.
- Wise 2011, complete four-page text around the displayed action `I[A,y]`:
  associated `G/H` section, stabilizer projection, and gauge-equivariant
  symmetry-breaking interpretation.
- Freidel--Geiller--Pranzetti Part I, §3.2, eqs. (3.21)--(3.48): invertible
  ECH bulk assumptions, corner potential, Lorentz charge, and normal pair.
- Freidel--Geiller--Pranzetti Part II, §§3, 5--7, especially eqs. (3.1)--(3.4),
  (5.1)--(5.4), (5.15)--(5.21), (5.33)--(5.34), (6.9)--(6.10), and
  (7.3)--(7.18): dual-frame normal, corner symplectic structure, moment map,
  nondegenerate corner geometry, and polarization/edge-frame dependence.
- Stelle--West: publisher abstract and metadata only; no equation-level
  statement is used.

## Assumptions / regime

- The validated reduction statement is kinematic: an associated `G/H` section
  selects a conjugate stabilizer and supports an algebraic reductive split.
- Wise 2009 assumes a fixed-dimensional nondegenerate Cartan soldering map.
- The Freidel--Geiller--Pranzetti construction assumes an invertible bulk
  tetrad/dual frame and an ordinary nondegenerate codimension-two corner.
- None of the sources treats exact local-dimension change, D023's rank-three
  pullback, or its compact-circle `43` holonomy.

## Interpretation and proposed project mapping

### Source-supported minimum

1. A section of an associated `G/H` bundle can select a conjugate `H`
   reduction; after that choice, a reductive Lie-algebra split decomposes a
   `G` connection into `H`-connection and coset one-forms without invoking an
   inverse coframe. This is a **kinematic bundle template**, not a D023 action.
2. In ordinary invertible 4D ECH gravity, a varied internal foliation normal
   enters a codimension-two corner potential as `E~_I delta n^I`, and Lorentz
   transformations have moment map `(1/2) integral alpha_IJ E^IJ`.
3. Whether that pair exists depends on the chosen gravitational potential and
   treatment of edge frames. No inspected compensator source supplies a
   boundary `delta V` pairing.

### What can legitimately inform a minimal fixed-interface D023 completion

Only the following design tests transfer: represent the core/exterior
reduction by a constrained section `V` of an associated
`SO(1,4)/SO(1,3)` bundle; build `V`-dependent stabilizer/coset projectors and
vary `V`; and compute the **total** fixed-interface presymplectic form and
Lorentz moment map rather than declaring `V` gauge. The FGP formulas are a
precedent that a normal may be a corner phase-space variable and that changing
polarization changes corner charges.

### What does not transfer

None of the sources treats a four-dimensional interface with rank-three
coframe pullback, a compact-circle `T_43` connection/holonomy, a jump from
`SO(1,4)` core data to an exterior `SO(1,3)` bundle, or exact coframe rank and
local-dimension change. Wise 2009's Cartan coframe is explicitly an
isomorphism; FGP use an invertible bulk tetrad/dual frame and a nondegenerate
rank-two spacelike corner. Their `n^I` lies in `SO(1,3)/SO(3)` (foliation
normal), not `SO(1,4)/SO(1,3)`; identifying it with D023's reduction field or
with the `43` holonomy would be a group/category error. Their pointwise
Lie-algebra moment map does not classify a finite circle holonomy conjugacy
class. Consequently these sources neither cancel D023's `43` row nor decide
whether its holonomy is gauge, superselected, or physical.

## Unresolved issues

1. Give explicit `V`-dependent projectors for `so(1,4)=so(1,3)_V+p_V` and the
   induced connection/coframe formulas on D023's rank-three trace, without
   imposing Cartan soldering invertibility.
2. Specify whether `V` is fixed, freely varied, constrained by a multiplier,
   or an edge/Stueckelberg field; derive its complete bulk/interface/corner
   variation and any `delta V` momentum.
3. Compute the total moment map after coupling to persistent D005 data. Is the
   `T_43` tangent null only after all Gauss/interface terms, and what observable
   distinguishes a gauge orbit from a fixed holonomy leaf or physical edge
   pair?
4. Determine admissible behavior of `V` and its bundle reduction across exact
   rank/local-dimension change, including whether the reduction extends over
   the collapsed circle and how large/winding transformations act.
5. Prove, rather than assume, that any FGP-like corner pairing remains defined
   for D023's degenerate four-dimensional pullback and chosen tangent class.

## Claims contradicted

No source contradicts D023 because none enters its regime. They do contradict
two tempting imports: Cartan geometry in Wise 2009 does **not** permit a
rank-changing soldering form, and FGP's corner normal is **not** a de Sitter
compensator. Stelle--West's accessible abstract also uses `SO(3,2)`/anti-de
Sitter conventions, so it cannot validate the requested `SO(1,4)` formulas.

## Confidence

Confidence is high in identities and equation extraction for the four complete
arXiv texts; moderate in the minimal cross-paper bundle interpretation; low in
applicability to D023. Stelle--West identity/abstract confidence is high but
equation-level confidence is absent. The stopping condition was reached after
the five specified items: the reduction and corner-normal mechanisms were
established in their native regimes, while the decisive rank-change/holonomy
bridge remained unsupported.
