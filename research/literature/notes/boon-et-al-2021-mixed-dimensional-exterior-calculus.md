---
citation_key: "BoonNordbottenVatne2021MixedDimensional"
title: >-
  Functional Analysis and Exterior Calculus on Mixed-Dimensional Geometries
authors:
  - "Wietse M. Boon"
  - "Jan M. Nordbotten"
  - "Jon E. Vatne"
year: 2021
doi: "10.1007/s10231-020-01013-1"
arxiv: "1710.00556"
url: "https://doi.org/10.1007/s10231-020-01013-1"
date_accessed: "2026-08-19"
---

# Literature note: Functional Analysis and Exterior Calculus on Mixed-Dimensional Geometries

## Question investigated

Can this mixed-dimensional exterior calculus encode the benchmark's direct incidence of a five-dimensional stratum on a three-dimensional interface, or is its discrete differential restricted to declared codimension-one boundary hierarchies?

## Search strategy

On 2026-08-19, arXiv and the Springer DOI record were queried for `mixed-dimensional exterior calculus Stokes codimension one trace`. The complete arXiv text was read through the geometric hypotheses, the mixed differential, trace spaces, Stokes theorem, and cohomology limitation. Metadata were checked against Crossref and the publisher record. The search stopped after the operator's dimension-adjacency rule was explicit.

## Source identity

- Wietse M. Boon, Jan M. Nordbotten, and Jon E. Vatne, “Functional Analysis and Exterior Calculus on Mixed-Dimensional Geometries,” *Annali di Matematica Pura ed Applicata* **200** (2021), no. 2, 757--789; first published online in 2020.
- DOI: [`10.1007/s10231-020-01013-1`](https://doi.org/10.1007/s10231-020-01013-1).
- arXiv: [`1710.00556`](https://arxiv.org/abs/1710.00556).

## Claims supported

- **Literature-supported geometric hypothesis:** the geometry is hierarchical codimension one: each `d`-manifold is contained in the boundary of one or more `(d+1)`-manifolds.
- **Literature-supported operator:** the mixed exterior derivative combines the tangential de Rham derivative with a discrete jump operator. At a root of dimension `d_i`, Eq. (29) sums incident branches whose roots have dimension exactly `d_i+1`.
- **Literature-supported trace structure:** local Sobolev spaces impose trace data recursively along the declared boundary descendants, Eqs. (47)--(51).
- **Literature-supported result:** Theorem 3.2 proves a mixed-dimensional Stokes identity in the paper's conforming-forest setting.
- **Literature-supported limitation:** equality of mixed and ambient de Rham cohomology dimensions is proved in Theorem 3.3 for `n<=3`; Remark 6 says the authors expect the restriction to be unnecessary but have not confirmed all details for `n>=4`.
- **Project interpretation:** the calculus can encode the benchmark's ordinary `4 -> 3` exterior/interface adjacency. It has no direct `5 -> 3` edge unless an auxiliary four-dimensional face is added to the hierarchy; the physical four-dimensional exterior in D002 is not a boundary stratum of the five-dimensional core.

## Claims contradicted

- The source contradicts the broad claim that its discrete mixed-dimensional differential couples arbitrary dimension jumps directly. Its defining sum is over one-higher-dimensional incident roots.
- It does not show that direct `5 -> 3` coupling is impossible in every formalism; it only places that coupling outside this paper's declared geometry and operator.

## Exact evidence location

- Abstract and §1, first two paragraphs: each `d`-manifold lies in a `(d+1)`-boundary and the paper treats hierarchical codimension one.
- §2.1, Definitions 1--2: conforming DAG/forest, coordinate maps to boundary pieces, and unique descendant coverage.
- §3.1, Eqs. (21), (24)--(25): integration and degree assignment on the forest.
- §3.2, Definition 5, Eqs. (29)--(30), and Example 7: discrete differential and the explicit `d_i+1` incidence set.
- §3.3, Eqs. (47)--(51) and Lemma 10: recursively enhanced trace spaces and their product characterization.
- §3.4, Theorem 3.2, Eqs. (58)--(59): mixed-dimensional Stokes theorem.
- §3.4, Theorem 3.3 and Remark 6: cohomology result for `n<=3` and unconfirmed extension to `n>=4`.

## Assumptions / regime

- A partition of an open Euclidean domain into disjoint connected orientable manifolds, each represented by a bounded reference domain with boundary and a conforming forest of boundary maps.
- Incidence is supplied as external combinatorial/geometric data; it is not inferred from an arbitrary quotient topology.
- The analytic setup uses Euclidean reference metrics, Sobolev trace regularity, and applications motivated primarily by `n<=3` mixed-dimensional PDEs.
- No Lorentzian signature, collapsing fibers, rank-changing coframes, gravitational action, or resolution-equivalence principle is treated.

## Confidence

- **Source identity:** high; DOI/Crossref, journal, pagination, authors, and arXiv record agree.
- **Evidence extraction:** high; the geometric definitions and exact discrete differential were read in full.
- **Project applicability:** high for the codimension-one adjacency test; moderate overall because one could enlarge the benchmark with an auxiliary resolved face, but that would be a new model choice.

## Unresolved issues

- Whether an auxiliary resolved four-face can be added without becoming physical, and how its elimination could be resolution-independent.
- Whether a direct codimension-two jump operator can preserve `mathfrak d^2=0`, Stokes, and the required signs.
- The five-dimensional benchmark lies outside the proved `n<=3` cohomology comparison.
