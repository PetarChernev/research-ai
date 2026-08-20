---
citation_key: "Kuribayashi2020SimplicialCochain"
title: >-
  Simplicial Cochain Algebras for Diffeological Spaces
authors:
  - "Katsuhiko Kuribayashi"
year: 2020
doi: "10.1016/j.indag.2020.08.002"
arxiv: "1902.10937"
url: "https://doi.org/10.1016/j.indag.2020.08.002"
date_accessed: "2026-08-19"
---

# Literature note: Simplicial Cochain Algebras for Diffeological Spaces

## Question investigated

Does the singular de Rham complex repair the failure of ordinary diffeological de Rham cohomology, and does its integration map supply the missing intrinsic `5 -> 3` incidence or vertical collapsed-face trace for the benchmark quotient?

## Search strategy

On 2026-08-19, arXiv and DOI/Crossref records were queried for `diffeological singular de Rham integration cochains de Rham theorem`. The complete arXiv text was read through the main definitions, Theorem 2.4, Corollaries 2.5--2.6, and the irrational-torus counterexample in Remark 2.9. The article was followed forward from Iglesias-Zemmour's cubic integration and backward to the original Souriau complex. Publisher metadata were checked against the DOI record.

## Source identity

- Katsuhiko Kuribayashi, “Simplicial Cochain Algebras for Diffeological Spaces,” *Indagationes Mathematicae* **31** (2020), no. 6, 934--967.
- DOI: [`10.1016/j.indag.2020.08.002`](https://doi.org/10.1016/j.indag.2020.08.002).
- arXiv: [`1902.10937`](https://arxiv.org/abs/1902.10937).

## Claims supported

- **Literature-supported limitation:** Souriau's original diffeological de Rham cohomology and diffeological singular cohomology are not isomorphic in general.
- **Literature-supported result:** the paper defines a singular de Rham cochain algebra `A_DR^*(S^D_bullet(X))` and an integration map to smooth singular cochains that induces a cohomology-algebra isomorphism for every diffeological space.
- **Literature-supported restricted comparison:** the factor map from Souriau forms to the singular de Rham complex is a quasi-isomorphism for finite-dimensional smooth CW-complexes and spaces obtained from parametrized stratifolds; this is not automatic for every diffeological space.
- **Literature-supported counterexample:** for the irrational torus, the factor map from the original de Rham complex is a non-surjective monomorphism on cohomology.
- **Project interpretation:** the construction restores a cohomological de Rham theorem using fixed-degree smooth singular simplices. It does not define a geometric regrading of a collapsed four-face into a three-dimensional incidence term or select a physical fundamental chain for D002's non-pure quotient.

## Claims contradicted

- The irrational-torus calculation directly contradicts the general claim that the original Souriau form complex, or the Iglesias-Zemmour integration map from that complex, always computes smooth singular cohomology.
- The source does not contradict the exact benchmark gap; its successful theorem concerns cochain/cohomology comparison, not a direct codimension-two variational incidence operator.

## Exact evidence location

- Abstract and §1, especially the paragraphs introducing `int^IZ`: statement of the general failure and the new singular de Rham construction.
- §2, definitions immediately before Theorem 2.4: smooth singular set `S^D_bullet(X)`, singular de Rham algebra, and factor map `alpha(omega)(sigma)=sigma^*omega`.
- Theorem 2.4: homotopy-commutative comparison diagram and the hypotheses under which the factor map is a quasi-isomorphism.
- Corollary 2.5: the new integration map induces an isomorphism of cohomology algebras for every diffeological space.
- Corollary 2.6(ii)--(iii): Iglesias-Zemmour integration induces an algebra map and is an isomorphism exactly when the factor map is.
- Remark 2.9 and Eq. (2.3): irrational-torus calculation and non-surjectivity of `H(alpha)`.

## Assumptions / regime

- Diffeological spaces and smooth singular simplices defined using fixed-dimensional affine simplices/affine spaces.
- Real differential graded algebras and cochains; the principal result is cohomological.
- The stronger comparison with Souriau forms requires a finite-dimensional smooth CW-complex or a parametrized-stratifold origin.
- No Lorentzian metric, mixed-dimensional action, relative fundamental class, changing fiber dimension, or moving-stratum variational problem is included.

## Confidence

- **Source identity:** high; DOI, journal metadata, author/title, and arXiv record agree.
- **Evidence extraction:** high; theorem, corollary, and counterexample were read in the full arXiv text.
- **Project applicability:** moderate for choosing a cohomological integration model; low for the requested interface incidence because the theorem does not construct such an operator.

## Unresolved issues

- Whether D002's quotient is in either class for which the factor map is a quasi-isomorphism.
- How the singular de Rham complex compares to D002's explicit kernel-pair equalizer at the chain level.
- How to choose relative/fundamental cycles and interface orientations for a non-pure-dimensional Lorentzian action.
