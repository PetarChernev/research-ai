---
citation_key: "IglesiasZemmour2013VariationsIntegrals"
title: >-
  Variations of Integrals in Diffeology
authors:
  - "Patrick Iglesias-Zemmour"
year: 2013
doi: "10.4153/CJM-2012-044-5"
arxiv: null
url: "https://doi.org/10.4153/CJM-2012-044-5"
date_accessed: "2026-08-19"
---

# Literature note: Variations of Integrals in Diffeology

## Question investigated

Does cubic-chain integration on an arbitrary diffeological space provide Stokes and moving-chain variation formulas, and do those formulas turn a rank-deficient four-face of a five-chain into an intrinsic three-dimensional interface incidence term?

## Search strategy

On 2026-08-19, a theorem-targeted search used the DOI record, Cambridge publisher PDF, and the terms `diffeology cubic chains Stokes variation integral`. The complete 32-page article was read, especially §§1, 3, and 4. Forward citation chaining to Kuribayashi (2020) was used to check whether later singular de Rham theory changes the chain-degree issue. No secondary summary or abstract-only claim was used.

## Source identity

- Patrick Iglesias-Zemmour, “Variations of Integrals in Diffeology,” *Canadian Journal of Mathematics* **65** (2013), no. 6, 1255--1286.
- DOI and stable locator: [`10.4153/CJM-2012-044-5`](https://doi.org/10.4153/CJM-2012-044-5).
- No arXiv identifier was found in the checked source records.

## Claims supported

- **Literature-supported result:** a diffeological `p`-form is evaluated plotwise, and its integral over a smooth `p`-cube `sigma:R^p -> X` is the ordinary integral of the pulled-back `p`-form over `I^p`.
- **Literature-supported result:** for `c in C_p(X)` and `alpha in Omega^{p-1}(X)`, the cubic-chain Stokes formula is `int_c d alpha = int_{partial c} alpha`.
- **Literature-supported result:** pushforward by a smooth map preserves chain degree: a `p`-cube is sent to the `p`-cube `f o sigma`, even if its image is geometrically lower-dimensional.
- **Literature-supported result:** Eqs. (4.1)--(4.2) give a variation formula for a family of `p`-forms on a family of `p`-cubes, with bulk contraction, ordinary boundary, and explicit form-variation terms.
- **Project interpretation:** these definitions provide a fixed-degree Stokes/variation calculus. They do not regrade a collapsed four-cube as a three-chain; that missing regrading is the precise benchmark mismatch, not a theorem stated by the author.

## Claims contradicted

- The source contradicts the broad statement that diffeological spaces have no Stokes theorem or no smooth variation formula for chain integrals.
- It does **not** contradict the narrower project conclusion that the reviewed calculus lacks an intrinsic direct `5 -> 3` incidence operator. All displayed constructions retain the chosen cube degree `p`.

## Exact evidence location

- §1.1, pp. 1256--1257: plotwise definition and compatibility condition for diffeological forms.
- §3.1, p. 1264, Eq. (3.1): `p`-cube `sigma:R^p -> X` and integration over `I^p`; the following paragraph extends this to `C_p(X)`.
- §3.3, pp. 1266--1267: `f_*:Cub_p(X) -> Cub_p(X')`, `f_*(sigma)=f o sigma`, and the chain/form push-pull identity.
- §4.1, p. 1268: diffeological Stokes theorem and its reduction to ordinary Stokes on the standard `p`-cube.
- §4.2, pp. 1268--1272, Eqs. (4.1)--(4.2): variation of the integral over an arc of `p`-cubes; Eq. (4.2) exposes the ordinary boundary term.

## Assumptions / regime

- `X` is an arbitrary diffeological space; chains are finite integer combinations of smooth maps from fixed-dimensional Euclidean cubes.
- The integral pairs a `p`-form with a `p`-chain. Boundary and variation are defined within that fixed grading.
- No stratification, fundamental class for a non-pure-dimensional quotient, Lorentzian structure, action density, fiber collapse, or resolution-independence theorem is assumed.
- A lower-rank image can make a pulled-back top form vanish, but the source does not identify the map with a chain of lower degree.

## Confidence

- **Source identity:** high; title, author, volume, issue, pages, and DOI agree between the full publisher PDF and DOI metadata.
- **Evidence extraction:** high; the definitions, equations, and surrounding proofs were read in the full article.
- **Project applicability:** high for identifying the fixed chain grading; moderate for the negative conclusion, because absence of a regrading operator in this bounded source is not a no-go theorem for all possible stratified calculi.

## Unresolved issues

- Whether a separate relative, perverse, or constructible chain theory can attach an intrinsic three-chain to the collapsed four-face.
- Whether a corner term obtained on a chosen resolution can be proven independent of the resolution.
- How the cubic-chain complex relates to the exact equalizer complex in D002 for this rank-jumping quotient.
