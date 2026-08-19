---
citation_key: "AltyFewster1996InitialValue"
title: >-
  Initial-value problems and signature change
authors:
  - "L. J. Alty"
  - "C. J. Fewster"
year: 1996
doi: "10.1088/0264-9381/13/5/024"
arxiv: "gr-qc/9501026"
url: "https://doi.org/10.1088/0264-9381/13/5/024"
date_accessed: "2026-08-19"
---

# Literature note: Initial-value problems and signature change

## Question investigated

Is there a rigorous primary-source example in which a field operator remains definable and interface conditions can be selected at metric degeneracy, yet classical evolution fails continuous dependence or finite-norm predictivity? How directly does that result apply to C003's Lorentzian spacelike-circle rank change?

## Search strategy

On 2026-08-19, arXiv, Crossref, DOI, and INSPIRE records were queried for `initial value signature change ill posed self-adjoint extension`. The complete arXiv v2 paper was read, especially §§3--6. Backward citations to earlier junction-condition and geometric-regularity work were used only to delimit originality. The exact instability argument, rather than the abstract, supplies the evidence below.

## Source identity

- L. J. Alty and C. J. Fewster, “Initial-value problems and signature change,” *Classical and Quantum Gravity* **13** (1996), 1129--1148 according to the author arXiv and INSPIRE records.
- DOI: [`10.1088/0264-9381/13/5/024`](https://doi.org/10.1088/0264-9381/13/5/024).
- arXiv: [`gr-qc/9501026`](https://arxiv.org/abs/gr-qc/9501026), version 2; report DAMTP R95/1.
- Stable publisher locator: <https://doi.org/10.1088/0264-9381/13/5/024>.
- Metadata caveat: the checked Crossref endpoint gives pp. 1129--1147, whereas arXiv and INSPIRE give pp. 1129--1148; equation/section locators are unambiguous.

## Claims supported

- **Literature-supported theorem-level neighboring obstruction:** on the specified two-dimensional Lorentzian-to-Kleinian signature-changing background, no reasonable local candidate Dirac Hamiltonian considered by the authors is symmetric, so it has no self-adjoint extension.
- **Literature-supported interface result:** the scalar spatial operator has deficiency indices `(2,2)` and therefore a `U(2)` family of self-adjoint extensions. Requiring continuity and the stated local relation between normal derivatives selects one extension with a derivative sign flip.
- **Literature-supported predictivity failure:** for that selected self-adjoint extension, the Klein--Gordon evolution is unbounded because the spatial Hamiltonian has spectrum unbounded below. The authors construct sequences of initial data tending to zero whose evolved norms diverge at any positive time.
- **Literature-supported finite-time failure:** smooth initial data compactly supported away from the interface on the Lorentzian side cease to define an `L^2` solution immediately after the signal reaches the signature-change surface.
- **Project interpretation, not source statement:** self-adjoint interface matching is therefore not by itself evidence for C003's strong hyperbolicity or continuous dependence. The source does not analyze C003's geometry.

## Claims contradicted

- The paper directly contradicts, in its exact model, the broad claim that selecting a self-adjoint extension and local continuous matching conditions suffices for a well-posed Klein--Gordon initial-value problem.
- It does not directly contradict C003: the paper changes a spatial sign so the metric becomes Kleinian with two time directions, while the project retains one time direction and removes a spacelike circle. Converting this result into a no-go theorem for circle collapse would conflate different principal symbols.
- The absence of a self-adjoint Dirac Hamiltonian and the scalar runaway are separate results; neither is a mere sign-convention discrepancy, because the authors fix a positive Hilbert-space measure and explicitly discuss the alternative indefinite/Krein-space choice.

## Exact evidence location

Locators use arXiv:`gr-qc/9501026v2`; the journal begins at p. 1129.

- §1, final four paragraphs: precise model scope, positive Hilbert-space measure, continuity assumption, and announced distinction between selecting boundary conditions and obtaining stability.
- §3, Eq. 3.1: `ds^2=dt^2+sign(z) dz^2`, Lorentzian `(+,-)` for `z<0` and Kleinian `(+,+)` for `z>0`, with a global `t`.
- §3.1, Eqs. 3.7--3.8: candidate Dirac Hamiltonians satisfy `D_+^*|_D=D_-`; neither is symmetric and neither admits a self-adjoint extension on any reasonable local domain containing `D`.
- §3.2, Eqs. 3.9--3.10: scalar spatial Hamiltonian `H=sign(z) d^2/dz^2`, unbounded above and below.
- §4.1, Eqs. 4.2--4.5: deficiency bases, indices `n_+=n_-=2`, and `U(2)` family of self-adjoint extensions; Eqs. 4.6--4.10 give the boundary form.
- §4.2, displayed conditions immediately after Eq. 4.10: within the authors' continuity ansatz the selected extension has `rho(0-)=rho(0+)` and `rho'(0-)=-rho'(0+)`.
- §5.2, Eqs. 5.13 and 5.19: Klein--Gordon evolution decomposes into oscillatory positive-energy and exponentially growing `cosh` negative-energy parts; the evolution operator is unbounded.
- §5.3, Eqs. 5.20--5.21: explicit instability sequence with initial norm at most `1/n` and evolved norm bounded below by `cosh(sqrt(n-1)t)`.
- §5.3, Eqs. 5.22--5.28: smooth compactly supported Lorentzian-side data; the negative-energy component fails to remain in `L^2` for `t>z_0`, the arrival time at the interface.
- §6.1, Eqs. 6.1--6.2 and following analysis: extension from the discontinuous example to a class of more general, including continuously signature-changing, metrics under the paper's stated regularity assumptions.

## Assumptions / regime

- Two-dimensional fixed background; no dynamical Einstein/coframe equations and no matter backreaction.
- Signature changes from Lorentzian to Kleinian across `z=0`; this introduces an elliptic/negative-spectrum sector and is not a rank loss that preserves one timelike direction.
- A global time coordinate `t` is retained to put equations in Hamiltonian form.
- Positive measure `|g_11|^{1/2} dz` and a Hilbert space are chosen; the indefinite-orientation/Krein-space alternative is explicitly excluded.
- Matter fields are continuous but not assumed differentiable at the interface. The preferred scalar matching is selected from self-adjoint extensions plus a local continuity ansatz.
- The instability is for free Dirac/Schrödinger/Klein--Gordon fields. It is neither a gravitational constraint-algebra theorem nor a nonlinear well-posedness theorem.

## Confidence

- **Source identity:** high; title, authors, year, DOI, report number, journal, and arXiv identifier agree. The one-page endpoint discrepancy is explicitly recorded rather than silently resolved.
- **Evidence extraction:** high; the complete arXiv v2 derivations and exact equations were read.
- **Project relevance:** high as a theorem-level warning about interface conditions and continuous dependence, but low-to-moderate as direct evidence about C003 because signature change and spatial-circle rank collapse have different causal/principal-symbol structures.

## Unresolved issues

- Whether the negative-spectrum mechanism persists for a Lorentzian system whose collapsing direction is spacelike and becomes gauge/quotiented rather than timelike.
- Whether a constrained gravitational system can remove the analog of the unstable sector through regular first-class generators without changing physical degree-of-freedom count.
- The correct interface energy norm and maximally dissipative/transmission conditions for a rank-changing coframe system.
- Nonlinear gravity, boundary displacement, ghosts, and quadratic reduced kinetic signs are outside this paper.
- Publisher/Crossref versus arXiv/INSPIRE final-page metadata should be checked against a physical journal copy if exact print pagination becomes consequential.
