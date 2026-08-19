---
citation_key: "HectorMaciasVirgosSanmartinCarbon2011DiffeologicalDeRham"
title: >-
  De Rham cohomology of diffeological spaces and foliations
authors:
  - "G. Hector"
  - "E. Macías-Virgós"
  - "E. Sanmartín-Carbón"
year: 2011
doi: "10.1016/j.indag.2011.04.004"
arxiv: "0903.2871"
url: "https://doi.org/10.1016/j.indag.2011.04.004"
date_accessed: "2026-08-19"
---

# Literature note: De Rham cohomology of diffeological spaces and foliations

## Question investigated

Can quotient diffeology provide intrinsic smooth maps and differential forms on a quotient of a smooth resolution, with an exact descent theorem strong enough to inform the differential-data and resolution-invariance parts of C001? Does this source also provide integration, tangent dimension, causal structure, or a variational calculus?

## Search strategy

On 2026-08-19, arXiv, Crossref, and the DOI record were queried for `diffeological quotient de Rham forms foliation`. The full arXiv text was read, especially §§2--3. Citation chaining was used to separate definitions originating with Souriau/Iglesias from the paper's comparison theorem for leaf quotients. Journal identity was checked against the publisher DOI record; no abstract-only inference was used.

## Source identity

- G. Hector, E. Macías-Virgós, and E. Sanmartín-Carbón, “De Rham cohomology of diffeological spaces and foliations,” *Indagationes Mathematicae* **21** (2011), no. 3--4, 212--220.
- DOI: [`10.1016/j.indag.2011.04.004`](https://doi.org/10.1016/j.indag.2011.04.004).
- arXiv: [`0903.2871`](https://arxiv.org/abs/0903.2871).
- Stable publisher locator: <https://doi.org/10.1016/j.indag.2011.04.004>.

## Claims supported

- **Literature-supported mathematical ingredient, not C001:** a quotient of a diffeological space carries the direct-image/quotient diffeology, the weakest diffeology making the projection smooth.
- **Literature-supported forms calculus:** a differential `r`-form on a diffeological space is a family of ordinary `r`-forms on plot domains satisfying pullback compatibility; exterior differentiation is defined plotwise and smooth maps pull forms back functorially.
- **Exact result for a restricted quotient class:** for a smooth foliated manifold, pullback from its diffeological leaf space is an isomorphism onto the complex of base-like forms. Thus, in this regime, form data on the quotient can be computed exactly as invariant horizontal form data on the smooth resolution.
- **Neighboring resolution-invariance ingredient:** the descent result is independent of the selected total transversal used in the proof. This is useful methodology for C001, but it is not invariance under the project's still-undefined class of circle-collapse resolutions.

## Claims contradicted

- No exact statement in C001--C003 is contradicted.
- The source does not support the broader assertion that arbitrary quotient forms coincide with all invariant forms on every resolution. Its exact theorem uses the local-lift and holonomy structure of a foliation quotient; applying it to an unrelated singular quotient would be citation laundering.
- Theorem 4.3's topological-invariance conclusion is restricted to Riemannian foliations through the preceding argument. It does not establish that diffeological de Rham data are topological or resolution invariants for all diffeological spaces.

## Exact evidence location

Locators use arXiv:`0903.2871v1` section/theorem numbering; the published article occupies pp. 212--220.

- §2.1, axioms (1)--(3): definition of a diffeology by plots and closure under localization and smooth precomposition.
- §2.1, Example 2, “Quotient diffeologies”: direct-image construction and its universal “weakest diffeology” characterization.
- §2.2, first two displayed compatibility formulas: a form is `{omega_alpha}` with `omega_{alpha o h}=h^*omega_alpha`; `d` and pullback are plotwise.
- Theorem 2.1: for a smooth manifold, ordinary and diffeological de Rham complexes are isomorphic.
- Proposition 3.1: base-like forms identify with forms on a total transversal invariant under the holonomy pseudogroup.
- Lemma 3.2: the quotient of the total transversal is diffeologically isomorphic to the leaf space.
- Lemma 3.3: local holonomy comparison of two lifts on a countable dense open union, the technical descent input.
- Lemma 3.4: `pi^*` identifies forms on the quotient transversal with holonomy-invariant forms.
- Theorem 3.5: `p^*: Omega^*(M/F) -> Omega_b^*(M,F)` is an isomorphism, and therefore so are the corresponding cohomologies.
- Theorems 4.2--4.3: the later, restricted topological-invariance statements; these delimit rather than enlarge the regime used here.

## Assumptions / regime

- Smooth diffeological spaces defined through plots from open subsets of Euclidean spaces.
- For the exact comparison theorem, `M` is a smooth foliated manifold and `M/F` has the quotient diffeology. The proof uses a locally finite foliated cocycle, total transversal, countable holonomy pseudogroup, and local lifts.
- Forms are contravariant plotwise objects. The paper does not construct an integration functional, fundamental class, Stokes theorem, or measure at changing dimension.
- No metric, Lorentzian signature, causality, tangent/derivation rank, connection, action, boundary displacement, or PDE problem is present.

## Confidence

- **Source identity:** high; DOI, journal metadata, title/authors, and arXiv record agree.
- **Evidence extraction:** high; the complete arXiv text and proofs around Lemmas 3.2--3.4 and Theorem 3.5 were read. Exact publisher page-to-theorem mapping was not assumed because the accessible version was arXiv.
- **Project relevance:** moderate for quotient smoothness and differential-form descent; low for C001 as a whole and negligible for C002--C003. The leaf-space hypothesis is a material restriction.

## Unresolved issues

- Whether the proposed circle collapse is realizable as a foliation/stack-like quotient with the local-lift property required by Lemmas 3.2--3.4.
- Whether a useful top-degree integration and Stokes theory survives when plot dimensions and physical stratum dimensions differ.
- How this plotwise form complex relates to conically smooth forms and to the tangent classifier of Ayala--Francis--Tanaka.
- No criterion here removes exterior fiber holonomy, connection, or symplectic data; form descent alone is not the H002 phase-space reduction.
