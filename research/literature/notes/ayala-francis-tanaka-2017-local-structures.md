---
citation_key: "AyalaFrancisTanaka2017LocalStructures"
title: >-
  Local structures on stratified spaces
authors:
  - "David Ayala"
  - "John Francis"
  - "Hiro Lee Tanaka"
year: 2017
doi: "10.1016/j.aim.2016.11.032"
arxiv: "1409.0501"
url: "https://doi.org/10.1016/j.aim.2016.11.032"
date_accessed: "2026-08-19"
---

# Literature note: Local structures on stratified spaces

## Question investigated

Does the paper give an intrinsic, family-compatible category of stratified spaces with controlled local dimension, tangent information, mapping-space topology, and functorial resolution that could supply mathematical ingredients for C001? Does it also supply forms, integration, Lorentzian causality, or dynamics required by C001--C003?

## Search strategy

On 2026-08-19, the bounded search queried arXiv and DOI/Crossref records for `conically smooth stratified spaces tangent classifier resolution unzipping`. The complete arXiv v6 text was read, with backward chaining through the introduction to distinguish the authors' construction from Whitney-, Mather-, Siebenmann-, and Quinn-style antecedents. Identity and journal pagination were checked against the DOI record. No secondary summary was used as claim evidence.

## Source identity

- David Ayala, John Francis, and Hiro Lee Tanaka, “Local structures on stratified spaces,” *Advances in Mathematics* **307** (2017), 903--1028.
- DOI: [`10.1016/j.aim.2016.11.032`](https://doi.org/10.1016/j.aim.2016.11.032).
- arXiv: [`1409.0501`](https://arxiv.org/abs/1409.0501), version 6 (the authors state that it varies slightly from the published version).
- Stable publisher locator: <https://doi.org/10.1016/j.aim.2016.11.032>.

## Claims supported

- **Literature-supported mathematical ingredient, not C001:** conically smooth stratified spaces are defined intrinsically from local basics of the form `R^i x C(Z)`, without requiring an ambient smooth manifold.
- **Literature-supported mathematical ingredient, not an ordinary tangent bundle:** the tangent classifier records spaces of conically smooth open embeddings of basic singularity types. On a smooth manifold it recovers the usual tangent classifying map.
- **Literature-supported resolution ingredient:** within the paper's conically smooth category, unzipping is a functorial resolution procedure to stratified spaces with boundary/manifolds with corners, supporting controlled comparison between a singular object and a particular canonical resolution process.
- **Literature-supported configuration-topology ingredient:** morphism and embedding sets are topologically enriched, and the resulting categories support families of stratified spaces. This is relevant to, but does not by itself define, the physical field-configuration topology demanded in C001.

## Claims contradicted

- No exact statement in C001, C002, or C003 is directly contradicted.
- The introduction directly warns against a weaker neighboring proposal: taking maps that are only stratum-preserving and smooth on each stratum leads to pseudo-isotopy pathologies in families and, in the example discussed around Eq. 1.1, cannot support functorial resolution. Thus a “smooth on every stratum” definition alone is not adequate evidence for C001.
- Apparent tension is not a convention issue: the paper's “tangent classifier” is presheaf-valued tangential data, not a pointwise derivation space or a variable-rank vector bundle. Treating it as the exact tangent notion named in C001 would overstate the result.

## Exact evidence location

Locators use arXiv:`1409.0501v6` numbering because the arXiv and journal pagination differ; the journal article occupies pp. 903--1028.

- Introduction, Eq. 1.1 and the following pseudo-isotopy discussion: the conically smooth automorphism result and the pathology of the naive stratumwise-smooth category.
- §1.1, Eq. 1.3: local basics `R^n x C(X)`; §§2.4 and 3.2 give dimension/depth and the conically smooth definition.
- Definition 1.1.3, Eq. 1.6: `tau: Snglr -> PShv(Bsc)`, with `tau(X)(U)` the space of conically smooth open embeddings `U -> X`.
- Definition 1.1.5, Eqs. 1.7--1.8: the enter-path category and unstraightened tangent classifier.
- Theorem 4.3.1, “Basics are easy”: computation underlying the basic/tangential homotopy types.
- Corollary 4.4.9, “Classical tangents”: restriction to smooth `n`-manifolds recovers the classical tangent classifying map.
- §7.1: partitions of unity and bundle preliminaries in the conically smooth category.
- Theorem 7.3.8, “Unzip” (called Proposition 7.3.8 in the introduction): the functorial resolution construction.
- Theorem 8.3.10, “Open handlebody decompositions”: a further local-to-global differential-topology result, useful for scope but not used as an integration theorem.

## Assumptions / regime

- Paracompact conically smooth stratified spaces locally modeled inductively on `R^i x C(Z)`, with compact lower-depth links in the basic local models.
- Morphisms relevant to the tangent classifier are conically smooth open embeddings; conclusions about families rely on this stronger category, not arbitrary stratumwise-smooth maps.
- Tangential structures are formulated homotopy-categorically through presheaves on basic singularity types.
- The work is differential topology, not Lorentzian geometry. It assumes no metric signature, causal relation, field equations, action density, or physical resolution equivalence.
- The unzipping theorem controls the paper's canonical construction; it does not quantify invariance under all smooth resolutions that a physical model might declare equivalent.

## Confidence

- **Source identity:** high; title, authors, journal, pages, DOI, and arXiv identifier agree across arXiv, DOI, and Crossref records.
- **Evidence extraction:** high for the cited definitions/theorems because the complete arXiv v6 text was read. Moderate only for matching arXiv locators to publisher page numbers, so theorem/section identifiers rather than guessed pages are used.
- **Project relevance:** moderate for C001 local models, morphisms, and resolution control; low for the missing forms/integration/causal/action/PDE parts. It is neighboring framework evidence, not support for the full claim.

## Unresolved issues

- Whether the project's non-pure `4/5` circle-collapse quotient fits the conically smooth basics and frontier conditions without adding forbidden ambient data.
- How to add differential forms, integration, Stokes' theorem, Lorentzian cones/causal curves, and a field-space topology compatible with the same morphisms.
- Whether unzipping plus extra control data yields an equivalence relation under which action, charges, and transition equations are independent of resolution.
- The paper does not compare its tangent classifier to the derivation-tangent dimension required by C001 at the collapse locus.
