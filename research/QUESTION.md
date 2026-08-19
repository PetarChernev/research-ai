# Research Question

Status: active — foundation stage

## Question

**Initiating question (2026-08-19):**

> Can a relativistic quantum theory be built in which physical spacetime is a single generalized object with dynamical local dimension, whose semiclassical vacuum is exactly `3+1` dimensional and whose localized `4+1`-dimensional regions can behave as particles? In particular, can the minimal `4 \leftrightarrow 5` theory be defined intrinsically (not by a physical ambient bulk), given a Lorentz-covariant action and well-posed classical dynamics, and eventually support a Hopf-framed defect whose exact configuration-space topology and quantum holonomy produce spin one-half and fermionic exchange?

This is the exact programmatic question distilled from the supplied working note **“Fermions as Local Dimensional Defects: Hopf-Framed Dynamical Dimension and a Solitonic Route to Spin-Statistics.”** The note is a source of conjectures and candidate calculations, not evidence that those conjectures hold.

The **current bounded question** is the first dependency gate:

> Does there exist a resolution-independent, Lorentz-covariant classical `4 \leftrightarrow 5` framework, formulated without an inverse coframe at rank change, whose bulk and transition equations follow from one variational principle and whose linearized initial-value problem is free of an evident constraint inconsistency, ghost, or loss of predictivity?

The Hopf defect is the first intended benchmark if this gate is passed, not an assumption used to pass it.

## Scope

### Included now: foundation stage F0

- Connected Lorentzian generalized spaces with only two regular open strata: total spacetime dimensions `d=4` and `d=5`, each with one timelike direction.
- An asymptotically `3+1`-dimensional, Poincaré-invariant candidate vacuum.
- A single compact spacelike circle direction on the resolved `d=5` stratum that is exactly quotiented/collapsed on an open `d=4` stratum.
- Two candidate descriptions to compare rather than identify by fiat:
  1. an intrinsic stratified/differential-space description; and
  2. equivalence classes of fixed-dimensional smooth resolutions with rank-varying soldering/coframe data.
- First-order coframe/connection actions that remain polynomial when the coframe loses rank, including whatever interface, corner, or transgression data a valid variation requires.
- The cheapest consistency observables: local dimension, resolution invariance, action finiteness, complete Euler–Lagrange and interface equations, gauge symmetries, constraint count/algebra, principal symbol, characteristic cones, and quadratic kinetic signs.
- Simple limiting backgrounds before solitons: pure `d=4` vacuum, pure `d=5` vacuum, and a planar or regular polar circle-collapse model.
- Downstream benchmark, only after F0: a localized timelike world-tube with an exactly `d=5` core, an exactly `d=4` exterior, and Hopf-framed collapse data of charge `Q=1`.
- Downstream topology observable: the map induced on fundamental groups by inclusion of the admissible Hopf sector into the full generalized-geometric configuration space, and the classes of a physical `2\pi` rotation and two-defect exchange.

### Explicit exclusions from the present stage

- A PRL-style manuscript, electron fit, Standard Model embedding, generations, or mass-spectrum fit.
- Identification of the collapsing circle with electromagnetism; gauge charge and chirality remain separate open problems.
- A sum over dimensional histories, UV completion, or claims of quantum unitarity before a classical state space and evolution law exist.
- Numerical solution of a spherical defect before equations, admissible boundary data, and a well-posed reduced problem are derived.
- Treating a small nonzero Kaluza–Klein radius, scale-dependent spectral dimension, a brane in a permanent bulk, or a degenerate metric on a still-physical fifth coordinate as automatically equivalent to exact lower local dimension.
- Assuming the Hopf-map configuration space is the full gravitational configuration space, or assuming an odd fiber mode selects the Finkelstein–Rubinstein character without deriving the relevant quantum bundle/holonomy.

### Observables and decision quantities

1. **Local dimension:** intrinsic tangent/derivation dimension and local covering dimension on each open stratum; agreement or controlled mismatch with coframe rank.
2. **Resolution independence:** invariance of physical observables under changes of resolution that represent the same quotient; an explicit equivalence relation is required.
3. **Variational completeness:** bulk equations, transition-locus equations, boundary/corner terms, conserved symplectic current, and stress-energy balance.
4. **Classical predictivity:** number of physical degrees of freedom, first-/second-class constraints, closure of the gauge/constraint algebra, hyperbolicity after gauge fixing, and required transition data.
5. **Health checks:** absence of negative kinetic eigenvalues and uncontrolled distributional curvature in the declared regime; finite on-shell action/energy for the elementary collapse model.
6. **Correct limits:** ordinary `3+1` Einstein gravity with two graviton helicities at long wavelengths; ordinary `4+1` first-order gravity on a nondegenerate five-dimensional region.
7. **Defect benchmark (later):** finite ADM mass, exact compact support of the opened direction, fluctuation spectrum, relativistic dispersion, and stability against nonspherical, overlap, topology-changing, and interface modes.
8. **Spin-statistics benchmark (later):** `\pi_1(\mathcal C_Q)`, the inclusion-induced map from the Hopf sector, rotation/exchange loop classes, and microscopic holonomy of the quantum state bundle.

### Parameter regime

- Foundation calculations are classical or semiclassical and below an unspecified ultraviolet cutoff `\Lambda_UV`; no continuum conclusion is extrapolated above it.
- The exterior is asymptotically flat unless a calculation explicitly declares otherwise.
- The extra direction is spacelike and compact where resolved; timelike extra dimensions are excluded.
- Candidate interfaces are timelike for particle world-tubes. Null or spacelike dimension-change loci are deferred.
- Torsion is allowed as an independent first-order variable until its equation is derived; it is not presumed zero at the transition.
- Couplings (`M_4`, `M_5`, cosmological terms, Lovelock/interface coefficients) are symbolic. Positivity or tuning assumptions must be stated per result.
- The defect radius, if one exists, must satisfy `R \gg \Lambda_UV^{-1}` for a continuum semiclassical treatment to be credible.

### Epistemic labels at initialization

- **Established background mathematics (to be source-checked):** ordinary Hopf-fibration and mapping-space homotopy facts in their standard categories.
- **Assumptions:** exact open-stratum dimension change is physically meaningful; a useful intrinsic/resolution formulation exists; a `3+1` phase can be stable.
- **Conjectures:** existence of a viable covariant action, preservation of the Hopf `\mathbb Z_2` loop in the full configuration space, dynamical selection of fermionic holonomy, stable finite defects, and recovery of GR/QFT.
- **Not admissible as evidence:** equations or citations in the initiating note until independently reconstructed or captured in exact-evidence artifacts.

## Conventions

- Natural units `c=\hbar=1` unless `\hbar` is restored to identify a semiclassical order or phase.
- Metric signature `(-,+,+,+)` on `d=4` and `(-,+,+,+,+)` on `d=5`.
- `d(x)` denotes **total spacetime dimension**, not spatial, spectral, or embedding dimension. The exterior has `d=4`; the core has `d=5`.
- Lowercase internal indices `a,b,\ldots=0,\ldots,3`; uppercase `A,B,\ldots=0,\ldots,4`. Spacetime-coordinate indices are introduced only on regular strata.
- Differential-form curvature is `R^{AB}=d\omega^{AB}+\omega^A{}_C\wedge\omega^{CB}` and torsion is `T^A=dE^A+\omega^A{}_B\wedge E^B`.
- Orientation and Levi-Civita symbols are chosen so `\epsilon_{0123}=+1` and `\epsilon_{01234}=+1` in an oriented orthonormal internal frame. Boundary orientations follow the outward-normal convention.
- Coordinates have length dimension; coframe one-forms have length dimension; spin connections and integrated angles are dimensionless in this convention. Every action calculation must state any departure.
- `X_4` and `X_5` denote regular open strata; `\Sigma` denotes transition data/locus but its intrinsic dimension and category are **unresolved**, not assumed to be an ordinary common hypersurface.
- `\widetilde X` denotes a calculational resolution and `X` the proposed physical generalized space. Diffeomorphisms of `\widetilde X` are not automatically physical equivalences; the resolution-equivalence relation remains to be defined.
- For later Hopf work, `Q` denotes the integer Hopf invariant after fixing area-form and orientation normalization; `k` denotes an integer right-`U(1)` fiber weight only when a global collective coordinate has been justified.
- Gauge fixing, regularity class, admissible topology/rank changes, and the precise definition of tangent dimension at singular points are unresolved choices and must be fixed before theorem-level claims.

## Success criteria

### Gate F0-A — mathematical state space

Pass only if a concrete category of `4/5`-dimensional Lorentzian objects supplies local models, smooth functions/forms, integration, causal structure, admissible morphisms, and a topology on configuration space, together with either:

- a proved correspondence to a controlled class of resolutions; or
- a documented reason to use one formulation while quantifying its resolution dependence.

An illustrative quotient alone does not pass this gate.

### Gate F0-B — covariant dynamics

Pass only if one explicit action has a complete variation on the chosen state space, including transition terms and admissible variations, and reduces to the declared `d=4` and `d=5` theories away from rank change. Gauge symmetries and conserved quantities must be identified. A schematic `S_4+S_5+S_\Sigma` does not pass.

### Gate F0-C — classical consistency

Pass provisionally if, on the simplest collapse background, a reproducible Hamiltonian/principal-symbol analysis finds a closed constraint system (or an equivalent consistent gauge structure), a finite number of propagating modes, no negative-norm/negative-kinetic physical mode, and a well-posed gauge-fixed linearized problem. Nonlinear well-posedness remains a later requirement.

### Gate F1 — dimensional defect

After F0, pass only with a finite-energy/finite-ADM-mass solution having exact `d=5` and `d=4` open regions, controlled transition curvature, a timelike world-tube, and no unstable physical mode within a declared fluctuation basis and numerical tolerance. A collective-radius minimum is necessary evidence at most, not sufficient evidence.

### Gate F2 — fermionic topology and quantization

Pass only if the admissible full one- and two-defect configuration spaces are defined, the relevant rotation/exchange loop classes survive all allowed rank changes and core overlaps, and a microscopic action or quantization rule derives—rather than chooses—the nontrivial holonomy. The standard Hopf mapping-space result alone is insufficient.

### Long-term program success

Requires recovery of low-energy GR and local relativistic QFT, unitary dimension-changing quantum evolution, a controlled UV definition, and falsifiable phenomenology. Gauge interactions and chirality are additional required gates for a Standard Model claim.

### Early stop / falsification criteria

The minimal route is disfavored or stopped if the cheapest explicit model shows an unavoidable failure—such as resolution-dependent observables, a nonclosing constraint algebra, an unavoidable ghost, loss of hyperbolicity at rank change, infinite transition action under the required exact collapse, or trivialization of the rotation/exchange loop by admissible geometric histories—and no clearly different hypothesis evades the same mechanism.
