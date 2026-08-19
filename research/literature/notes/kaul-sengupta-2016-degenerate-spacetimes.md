---
citation_key: "KaulSengupta2016DegenerateSpacetimes"
title: >-
  Degenerate spacetimes in first order gravity
authors:
  - "Romesh K. Kaul"
  - "Sandipan Sengupta"
year: 2016
doi: "10.1103/PhysRevD.93.084026"
arxiv: "1602.04559"
url: "https://doi.org/10.1103/PhysRevD.93.084026"
date_accessed: "2026-08-19"
---

# Literature note: Degenerate spacetimes in first order gravity

## Question investigated

What does an explicit first-order gravity calculation establish about algebraic regularity, equations, torsion, and underdetermined connection data when a tetrad loses one rank? Does it establish a differentiable `4 <-> 5` transition action or predictive evolution as required by C002--C003?

## Search strategy

On 2026-08-19, the bounded search queried arXiv, APS/DOI, and Crossref for `degenerate tetrad first order gravity noninvertible coframe equations torsion`. The full arXiv v2 text, stated by the authors to be identical to the journal version, was read. Backward references to Henneaux, Tseytlin, Horowitz, and related degenerate-tetrad work were noted to avoid assigning the general idea to this paper; the explicit rank-three solution analysis was taken from this primary source.

## Source identity

- Romesh K. Kaul and Sandipan Sengupta, “Degenerate spacetimes in first order gravity,” *Physical Review D* **93** (2016), 084026.
- DOI: [`10.1103/PhysRevD.93.084026`](https://doi.org/10.1103/PhysRevD.93.084026).
- arXiv: [`1602.04559`](https://arxiv.org/abs/1602.04559), version 2.
- Stable publisher locator: <https://doi.org/10.1103/PhysRevD.93.084026>.

## Claims supported

- **Literature-supported algebraic ingredient for C002, not C002 itself:** the four-dimensional Hilbert--Palatini bulk action is polynomial in tetrad and curvature and uses no inverse tetrad, so its displayed Euler--Lagrange equations remain algebraically defined for noninvertible tetrads.
- **Literature-supported degeneracy result:** for the rank-three tetrad ansatz with one null eigenvalue, the connection equation does not determine the full connection. After Eqs. 14--16, the authors count 12 fixed and 12 undetermined connection components, represented in part by symmetric matrices `M^{ij}` and `N^{ij}`.
- **Literature-supported torsion result:** broad vacuum solution families in the degenerate sector have nonzero contortion/torsion without matter. For the displayed homogeneous classes, six functions in symmetric `N^{ij}` are subject to one scalar relation.
- **Literature-supported bulk-action result:** for the degenerate configurations satisfying the stated equations, the Hilbert--Palatini bulk action evaluated in Eq. 30 vanishes.
- **Author-stated neighboring extension:** at the end of §V and in §VII the authors state that the analysis extends to Lorentzian signature, including a zero eigenvalue in a spatial direction after signature changes in the nontrivial three-geometry. The detailed calculation in the paper is Euclidean, so this statement is not treated as a completed Lorentzian hyperbolicity analysis.

## Claims contradicted

- No full project claim C001--C003 is directly contradicted.
- The paper directly contradicts the broad claim that metric and first-order gravity remain classically equivalent after noninvertible tetrads are admitted: §VII states that the extra degenerate phase makes the formalisms inequivalent.
- It also contradicts the weaker inference that a polynomial, finite equation at degeneracy automatically determines all connection data. This is an exact algebraic warning. Whether the undetermined functions are gauge, constrained transition data, or physical modes requires a Hamiltonian analysis absent here, so it is not yet a contradiction of C003's reduced-system claim.

## Exact evidence location

The arXiv v2 equation/section numbering is identical to the journal version according to the arXiv record.

- §II, Eq. 1: Hilbert--Palatini action `S=(8 kappa^2)^{-1} integral epsilon epsilon e e R`, with no determinant or inverse tetrad.
- §II, Eqs. 2--5: independent connection and tetrad equations, written without inverse tetrads.
- §III, Eqs. 6--9: inverse tetrads are used only in the nondegenerate sector to obtain zero torsion and equivalence with Einstein equations, marking where that equivalence fails.
- §IV, unnumbered block tetrad and metric immediately before Eq. 14: rank-three `3 x 3` triad block with `e_tau^I=e_a^4=0`.
- §IV, Eqs. 14--16 and the two paragraphs immediately following: solution of the connection equations and explicit count of 12 fixed versus 12 undetermined components; Eq. 17 removes only the `tau` dependence of the triad as `SO(3)` gauge.
- §IV, Eqs. 18--21: the remaining tetrad equations; Eqs. 22--25 give the simplifying `M^{ij}=lambda delta^{ij}` family and the one scalar condition on `N^{ij}`.
- §IV, Eq. 30: zero on-shell value of the displayed **bulk** action, using Eq. 19.
- §V, paragraph after Eqs. 31--38: six components of `N^{ij}` depend on all four coordinates and are independent apart from one constraint; generic solutions have torsion.
- End of §V: signature-regime statement distinguishing a temporal zero eigenvalue from a spatial one.
- §VII, first two paragraphs: classical inequivalence of first- and second-order formalisms once the noninvertible phase is included.

## Assumptions / regime

- Four-dimensional pure Hilbert--Palatini gravity without cosmological constant or matter.
- Main derivation uses Euclidean internal group `SO(4)` and a tetrad of constant rank three throughout the analyzed patch; it does not solve a rank-changing interface.
- The invertible `3 x 3` triad block and local coordinate/internal rotations used to reach the ansatz are assumed.
- The explicit eight classes use homogeneous Thurston three-geometries and, after Eq. 22, a special `M^{ij}=lambda delta^{ij}` choice.
- No boundary term is included in Eq. 1 or Eq. 30, no transition-locus displacement is varied, and no asymptotic/action differentiability analysis is performed.
- No Dirac--Bergmann constraint classification, physical degree-of-freedom count, gauge-fixed principal symbol, characteristic cone, or kinetic-sign calculation is supplied.

## Confidence

- **Source identity:** high; APS DOI, Crossref, and arXiv metadata agree, and arXiv v2 is labeled identical to the journal version.
- **Evidence extraction:** high for Eqs. 1--30 and the component count because the full text was read; moderate for the Lorentzian applicability because it is asserted briefly rather than rederived.
- **Project relevance:** high as a warning about noninvertible first-order variables, but only moderate as an ingredient for C002 and low for C003. The dimensionality, signature derivation, and absence of an interface are substantial mismatches.

## Unresolved issues

- Which of the arbitrary `M^{ij}`/`N^{ij}` functions are gauge or constrained after a complete canonical analysis at rank three.
- Whether the constraint rank changes when rank-four and rank-three regions are joined, and whether transition data can make the count constant.
- The first-order boundary/corner term and admissible variations needed for a differentiable action.
- A separate Lorentzian spatial-rank principal-symbol analysis; the author's signature comment is not evidence of hyperbolicity or causal predictivity.
- Generalization from four-dimensional rank three to five-dimensional rank four and, crucially, removal rather than mere degeneracy of the fifth coordinate.
