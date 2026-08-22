# Computational Verification Strategy

Status: active — first mixed polarization completion derived and checked; covariant reduction field next
Last updated: 2026-08-22T20:15:00Z

Research question: Does there exist a resolution-independent, Lorentz-covariant classical `4 <-> 5` framework, formulated without an inverse coframe at rank change, whose bulk and transition equations follow from one variational principle and whose linearized initial-value problem is free of an evident constraint inconsistency, ghost, or loss of predictivity?

This is the project-specific methodology for testing research recorded in
`D001`–`D023`. It does not retroactively turn historical calculations into
machine evidence. D006 completed the bounded interface-only canonical analysis;
W001-total-gauss derived the regular-core limit and total cut-moment-map
cancellation; CY001-trace-primary then derived a conditional duplicated-trace
reduction and the combined defining-primary algebra. CY002-background-existence
tested whether the presumed minimal background actually solves the bulk
equations. O007-O013 test the respective finite bridges. D019 excludes the
minimal source-free common-warp background analytically, and D020 excludes a
bounded NEC-respecting effective source for the two exact D002 profiles in that
geometry. D021/C024 now prove the profile-independent classical endpoint
theorem analytically; no check addresses that quantified real-analysis result,
a more general background, functional trace adjoint, or post-shell preservation.
D020/C023 derive the endpoint stress, boundedness, weighted-integrability, and
null-energy-condition verdict for the two exact D002 profiles and every
smooth-flat common warp. O011 passed that finite bridge. D021/C024 supply the
universal zero-slope endpoint theorem analytically; finite differentiation does
not test its quantifier, so formal real analysis remains deferred. D022/C025 now
test the selected nonzero-slope attachment and identify a finite mixed D004
boundary row absent from unchanged D005. O012 passed the predeclared exact
coefficient, incidence, shell, and mutation bridge. D023/C026 test one full
tensorial-difference polarization primitive; O013 passed its finite complete
variation and local-covariance bridge. No obligation decides the physical
admissibility of the finite tangent class, another mixed completion, global
holonomy/edge status, total-interface full covariance, weak-action
completeness, or C002/C003.

## Current research phase

The existing work is in a fixed-interface, exact-algebraic foundation regime.
It has passed from an interface-only shell through a trace-aware combined
defining-primary presentation. Smooth-flat background existence failed, while
the finite-slope control exposes an uncancelled mixed interface row and the
first covariant polarization repair fails its free-background criterion;
complete action/background existence therefore blocks the planned functional
bulk-boundary preservation phase.
The benchmark object is the local non-pure quotient
`X=[U x I x S1]/~`, with an exactly collapsed circle for `s<=0`, together
with two infinitely flat resolutions. The load-bearing derivations use:

- quotient and ambient smooth-function algebras and kernel-pair form descent;
- finite exterior algebras of differential forms with exact wedge signs;
- oriented boundary pullback and circle pushforward;
- first-order Einstein–Cartan/Palatini coframe and connection variations;
- field-space exterior differentiation;
- finite-dimensional exact linear maps on Lorentz-valued interface forms;
- covariant and canonical Lorentz cut moment maps with explicit incident signs.
- one-sided finite mixed traces and exact weak/distributional controls, kept
  distinct from the split action and from a general weak calculus.

The strict derivational backbone of the present frontier is

```text
C009 and C010 -> C012 -> C013 -> C014 -> C015 -> C016 -> C017
                                                    -> C018 -> C019/C020
                  C007 + C015 -------------------------------> C021
                                      `----------------------> C022
                   C007 --------------------------------------> C023
               endpoint data + D019 curvature ----------------> C024
                    C012 + C015 + finite-slope tangent --------> C025
                         C014 + C015 + C025 + one primitive ----> C026,
```

with C011 excluding an autonomous bare-quotient measure/incidence choice and
C007–C008 fixing the local category benchmark. C016 establishes exact
interface-only presymplectic ranks and a corner-charge witness on one planar
branch, but deliberately leaves total constraint closure undecided because the
bulk symplectic form and Lorentz Gauss generators are absent.

W001 adds the derived refinement C017: in the regular equalizer the persistent
five-dimensional core cut flux is zero, while the exterior `-P^-` contribution
cancels `Ad_(g^-1)Q` on the D005 matching shell in the unshifted polarization.
This removes the partial interface charge as a standalone obstruction but does
not remove or classify the rank-ten form. Seven of eight branches required
revision after same-model internal critique; the surviving convergence target
is a declared trace/gluing presentation plus the combined Palatini/interface
primary matrix and first preservation step.

The first focused convergence cycle froze a **duplicated one-sided trace
presentation with explicit covariant gluing constraints**. Independent
boundary copies enter the D005 interface functional and are constrained to the
regular bulk traces; the copies are not presumed to add physical phase-space
directions. This choice avoids an undeclared distributional trace bracket and
makes the reduction map auditable. The accompanying gauge class admits small
persistent core/exterior Lorentz transformations at the internal cut while
requiring them to vanish at temporal endpoints and the lateral boundary. The
fixed seed uses only its exact stabilizer redundancy and no independent
seed/corner potential. These choices are recorded in `research/DECISIONS.md`.

CY001 produced C018-C020. D015 makes the gluing equivalence conditional on
fixed gauge-equivariant locally trace-surjective maps and a clean auxiliary
sector. D016 proves zero regular tangential 5D Palatini overlap while retaining
nonzero normal contractions. D017 shows that the complete shell potential and
exterior Palatini defining reduction absorb the five isolated `dQ_C` pairs,
leaving six Palatini connection-primary nulls, a rank-four coadjoint block with
two nulls, and six `g` zero-momentum primaries. O008 passed the finite exact
bridge. The next representation must add a functional trace domain, boundary
pairing and adjoint, boundary-compatible background, and total Hamiltonian;
these are not inferred from the pointwise incidence used by O008.

CY002 then tested the smallest candidate background rather than assuming it.
D018/C021 show that the source-free static unwarped core
`E=(dt,dx,dy,ds,rho dtheta)` has `Lambda_5=0` and `rho''=0`, while the flat
exterior has `Lambda_4=0`; D002 smooth-flat attachment supplies
`rho(0)=rho'(0)=0`, so no positive-radius core exists. The limiting traces still
satisfy the complete frozen D005 shell. O009 passed the exact Cartan, Euler,
endpoint, and shell bridge. Planned Domain I is therefore deferred until a
genuine background is found; the next theory object is the minimal source-free
warped cohomogeneity-one extension, not a functional bracket around nonexistent
unwarped data.

CY003 tests that least-radical extension. D019/C022 use
`E^i=w(s)dx^i`, `E^3=ds`, `E^4=rho(s)dtheta` with one common `2+1` warp. The
five Euler forms imply `(w'/rho)'=0` and a regular equation for `w^2`; the
smooth-flat endpoint forces `Lambda_5=0`, `w=1`, and then `rho=0`. The shell
again remains compatible. O010 passed the frozen exact
Cartan/Euler/ODE/endpoint/shell bridge. The next analytic object is the
effective source required by the same geometry, not another vacuum warp or a
functional bracket around absent data.

CY004 performs that inverse-source diagnostic without choosing matter fields.
D020/C023 show for both exact D002 profiles and every common warp smooth-flat to
one that `rho''/rho` diverges positively, so orthonormal curvature/stress are
unbounded and both nontrivial NEC channels fail, while each absolute stress
component remains locally five-volume integrable. O011 passed the finite exact
contraction/profile/order bridge with five effective mutations. The next theory
object is a profile-independent endpoint lemma, not a matter action fitted to a
singular effective tensor.

CY005 derives that endpoint lemma. D021/C024 require only a positive radius in
`C^1` through the endpoint and `C^2` on the punctured side, with zero endpoint
value and proper-distance slope. A two-integrating-factor comparison gives
`limsup rho''/rho=+infinity`, so the orthonormal radial-circle sectional
curvature is unbounded below in every endpoint neighborhood. A smooth-flat
oscillatory witness shows that no actual limit or eventual sign follows. The
regular-lapse formula isolates invariant curvature from raw coordinate second
derivatives. CY005 adopts no obligation: exact differentiation or chain-rule checks
would not test the universal theorem, while formal real-analysis infrastructure
is disproportionate at this stage. The next methodological regime is one
deliberately selected finite-regularity/nonzero-slope attachment, with the
connection, diagonal geometry, and D004/D005 action otherwise frozen.

CY006 performs that finite-slope audit. D022/C025 use `rho=c s` on the positive
core and zero on the open collapsed side. The punctured bulks are flat and the
persistent D005 shell is compatible, but the newly admitted finite vertical
mixed tangent produces
`p_!Theta_(5,chi43)=+(2pi/kappa_5)delta chi43 o_Sigma`; unchanged D005 has no
conjugate field, so free variation forces the rank-three triad volume to vanish.
Fixing both slope and mixed holonomy leaves only a fixed-boundary control. O012
passed the finite ordered-index, orientation, D005-incidence, shell, and mutation
bridge. The next methodological question changes only the exposed action-side
datum: whether one minimal covariant integrable mixed interface completion can
repair this row without degeneracy or uncontrolled edge data.

CY007 tests exactly one such action-side repair. D023/C026 add the full
tensorial-difference core-boundary primitive
`B_ref=-integral (omega_+-barOmega)^AB wedge P^(5)_AB`. It cancels the C025
`43` row but changes polarization: fixed reference data anchor the slope,
unrestricted reference or seed variation forces boundary rank at most two, and
a fixed-seed gauge orbit fixes the holonomy conjugacy class while adding an
unclassified edge/corner sector. O013 passed the finite ordered-index,
field-space, orbit-sign, and generic infinitesimal-covariance bridge. Full
`SO(1,4)` covariance of the total frozen interface theory now requires an
explicit normal/reduction field or a full mixed D005 extension, so no further
computational representation is selected before that theory object exists.

## Checkability map

| Claim | Machine-checkable now | With materially more infrastructure | Not usefully machine-checkable in this phase |
|---|---|---|---|
| C001 | No finite test decides existence of the full state space. | A concrete category could expose computable invariance and descent obligations. | The present global existence, causality, configuration-topology, and resolution-equivalence conjunction. |
| C002 | Normalizations and variations of a specified candidate action can be checked. | A completed moving-interface action could expose variational and gauge obligations. | Existence over the still-open action class. |
| C003 | Exact constraint-matrix ranks and principal-symbol tests become possible after an action/background is fixed. | A reusable canonical/PDE representation will likely be required in the next phase. | The current existential health claim, because no candidate linearized system exists. |
| C004 | Loop classes can be computed only after the physical configuration spaces and inclusions are defined. | Formal/computational topology may become useful after F0/F1. | The current undefined full-space injectivity and exchange statement. |
| C005 | Holonomy and representation calculations become executable after a microscopic bundle/action is defined. | A topology/quantization implementation may then be warranted. | The present uniqueness and dynamical-selection claim. |
| C006 | A future solution can be tested by residuals, convergence, ADM mass and spectra. | Numerical PDE and certified stability infrastructure would be required. | Existence and complete stability before equations/boundary data exist. |
| C007 | Finite rank tables and explicit fiber tests are checkable. | Formal topology could encode the cone homeomorphism and covering-dimension theorem. | A finite script would not certify the full topological/local-ring theorem and would add little to the analytic proof. Computational verification remains pending/deferred. |
| C008 | Exact profile identities and finite witnesses are checkable, but do not certify `C-infinity` germ statements. | A formal analysis/topology development could encode flatness and extension obstructions. | Numerical profile sampling is weaker than the existing analytic and historical independent reconstruction; no required obligation is adopted in this migration. |
| C009 | Exact kernel-pair residuals, form membership controls, curvature witnesses and gauge round trips. | Global bundle/large-gauge questions would require a different representation. | Whether omission/forgetting is physical gauge or dynamics. |
| C010 | Exact generic degree-four trace map, orientation signs and ordinary/Haar pushforwards. | Formal diffeology could encode the full smooth-germ quantifier. | Claims outside the declared regular equalizer, such as singular or edge traces. |
| C011 | Profile pushforward formulas are checkable as supporting regressions. | A formal naturality theorem could encode automorphism-invariance. | The conclusion-critical absence of a canonical unmarked measure/incidence is conceptual and category-relative; `computational_verification: not-applicable` is adopted and is open to verifier challenge. |
| C012 | Palatini factorials, ordered-pair multiplicities, channel split, boundary signs, collapsed trace and fixed-radius control. | Broader Lovelock/transgression classes would require additional encodings. | Preference among potential representatives and enriched action classes. |
| C013 | Pure-multiplier degeneracy and the displayed completion coefficient algebra. | Exhaustive boundary-action classification is not currently formalized. | The bounded conceptual classification beyond the explicitly varied families. |
| C014 | Field-space curl and complete primitive on a certified nonzero mode. | A general formal calculus of local field-space functionals is unnecessary now. | A universal statement about every possible interface action (not claimed). |
| C015 | Reference-branch gradients, coupling relation, rank/minor implication, `H(K)` rank/nullity and nonflat kernel witness. | The interface-only canonical follow-up is now represented by C016/O005; a complete bulk canonical system would need materially more structure. | Gauge-versus-physical status, bulk compatibility, hyperbolicity and solution existence. |
| C016 | O005 checks exact `dQ`, off-shell ranks and residual-block algebra; O006 checks the honest 20-dimensional shell pullback, cross blocks, nullity, moment-map sign, and planar witness. | The adopted duplicated-trace presentation could expose total Gauss rank and constraint-closure obligations after its gluing reduction is derived. | Whether the residual rank-ten block is physical, second class, or removed by first-class total gauge in the presently incomplete bulk system. |
| C017 | O007 checks exact 4D/5D Palatini coefficients, zero regular core pushforward, fixed-radius normalization, exterior/interface cancellation, nonidentity dressing, common orientation reversal, and sign/dressing mutations. | The adopted duplicated-trace presentation could expose primary stabilization and reduced-rank obligations if it yields a finite faithful matrix. | Final gauge classification and physical degree count remain non-machine-checkable until the gluing reduction and first preservation are complete. |
| C018 | O008 checks the finite shell-potential coefficients and gluing-elimination sign bridge under the declared clean local maps. | A concrete functional trace realization could test continuity, adjointness, and equivalence of reduced brackets. | Existence and local surjectivity of the assumed trace maps, and global phase-space equivalence. |
| C019 | O008 exactly enumerates regular 5D tangential `P,dP` rows, zero circle pushforwards, and nonzero normal-contraction controls. | A functional trace/normal-domain implementation would be needed for post-gluing bulk-boundary brackets. | Any presentation-independent conclusion beyond the stated pre-gluing tangential theorem. |
| C020 | O008 checks the complete finite defining matrix, all legal Palatini complements, zero Schur correction, ranks, null certificates, direct assemblies, and mutations. | First preservation requires a functional trace adjoint and an explicit background total Hamiltonian; a new obligation is possible only after those are derived. | Gauge/physical/second-class classification and reduced degree count in the presently undefined preservation system. |
| C021 | O009 checks the complete exact Cartan solve, curvature signs, ordered-pair 5D Euler coefficients, flat 4D residual, affine endpoint elimination, shell table, alternate component contraction, and semantic mutations. | The common-warp extension is now C022/O010; sourceful or more general geometric backgrounds require new equations and representation assessment. | Whether another background/action or a different regularity category evades the restricted obstruction; broad C002/C003 remain undecided. |
| C022 | O010 passed the complete common-warp Cartan solve, curvature families, ordered-pair Euler vector, denominator-cleared ODEs, branch-preserving first integral, endpoint elimination, shell table, alternate component controls, and semantic mutations. | Anisotropic/off-diagonal or sourceful backgrounds require new equations and possibly a different representation. | Completeness of the source-free background search, physical necessity of the frozen category/action, and broad C002/C003. |
| C023 | O011 passed the exact effective-stress components, all-null NEC reduction, both fixed-profile derivatives/signs, formal flat-order bookkeeping, and the distinction between pointwise divergence and volume-weighted integrability. | A formal analytic or dynamical development would be needed for an all-profile source theorem or existence/nonexistence of a matter action. | Covariant matter realization, source dynamics, and every excluded geometric/action relaxation. |
| C024 | Exact differentiation can regress the oscillatory sharpness witness and the regular-lapse chain rule, but neither finite identity tests the quantified endpoint theorem. | A formal real-analysis development could encode the integrating-factor comparison, endpoint limits, positivity, and weak a.e. extension. | Finite symbolic sampling or profile enumeration cannot establish the universal theorem or its physical sufficiency; no required obligation is adopted in this cycle. |
| C025 | O012 checks the ordered D004 finite-slope mixed boundary coefficient, frozen D005 field incidence, persistent shell table, and semantic mutations exactly. | A completed lower-regularity quotient calculus or a proposed mixed interface action could expose new covariance, integrability, and gauge obligations. | Physical necessity of the finite mixed tangent, general BV action completeness, classification of all counterterms, and broad C002/C003. |
| C026 | O013 checks the single primitive's ordered rank-three reduction, complete finite field-space variation, all ten connection-row cancellations, polar coframe/reference residuals, orbit signs, and generic infinitesimal standalone `SO(1,4)` covariance. | A defined normal/reduction-field theory could expose mixed gauge, moment-map, and constraint obligations in a new representation. | Global holonomy/large-gauge classification, edge gauge-versus-physical status, full D005 covariance, all other mixed actions, and broad C002/C003. |

## Current machine-check obligations

The program now has thirteen required exact obligations, prioritized by the actual
dependency graph rather than chronology. All thirteen have current deterministic
`passed` results; each was allocated with its acceptance criterion fixed before
implementation.

CY005 added no obligation. C024's conclusion-critical content is a
quantified real-analysis comparison proved directly in D021. The available
finite exact regressions would test only derivative and coordinate identities;
a formal analysis stack is possible but not proportionate to the present
decision. Its computational-verification state remains pending/deferred rather
than being laundered through a non-discriminating check.

CY006 adds O012 because C025's decisive bridge is instead finite and
mechanically discriminating: an ordered-index sign/factor calculation plus the
absence of a mixed variable in the frozen D005 action. O012 does not encode the
scientific choice of tangent class or any candidate action repair.

CY007 adds O013 because C026's new load-bearing bridge is finite: the ordered
normal-bivector momentum, complete field-space variation of one polynomial
primitive, orbit integration-by-parts signs, and local covariance identity.
O013 does not encode global holonomy, edge classification, total D005
covariance, or sufficiency of the action class.

1. **O001 — D002 equalizer and curvature controls (C009/D002).** Exact
   branchwise pullback residuals for `eta`, `rho eta`, `A`, `F`, and mixed
   connection forms, plus explicit nonzero-curvature/gauge controls. This also
   guards against conflating quotient descent with principal-bundle basicness.
2. **O002 — collapsed Palatini boundary operator (C010, C012/D003–D004).** Exact
   orientation, zero-trace, Palatini split, exterior witness, fixed-radius and
   ordinary-versus-Haar normalization checks.
3. **O003 — field-space curl and complete primitive (C014/D005).** Exact
   nonclosure of the isolated momentum one-form and closure of the complete
   primitive with every companion term.
4. **O004 — reference-branch coefficient and rank table (C013, C015/D004–D005).**
   Exact differentiation/elimination for reference-free, fixed-reference and
   freely varied reference branches; coupling normalization; coframe-minor
   implication; and rank/nullity/nonflat-kernel checks for `K -> H(K)`.
5. **O005 — interface cut rank and moment maps (C016/D006).** Exact planar
   `dQ`, fixed-reference and Stueckelberg presymplectic ranks, null directions,
   Lorentz moment-map signs, and nonzero `Q_03` corner witness. Its off-shell
   and residual-block assertions remain useful, but an independent audit found
   its shell direct-sum and shell-moment assertions assumption-encoded.
6. **O006 — honest C016 shell pullback (C016/D006).** Substitutes
   `lambda=-Q(e)` before field-space differentiation, constructs the full
   20-dimensional `(chi_v,xi,delta e)` shell form including cross blocks, and
   checks rank/nullity, explicit null certificates, fixed-reference pullback,
   moment-map contraction, and mutations targeting the O005 shortcut.
7. **O007 — total Lorentz cut cancellation (C017/D008–D009).** Reconstructs
   exact persistent 4D/5D Palatini coefficients, verifies the zero regular core
   pushforward and fixed-radius control, and tests the exterior `-P^-` plus
   interface `-Ad_(g^-1)lambda` cancellation under identity and nonidentity
   Lorentz dressing. Four sign/dressing mutations must fail.
8. **O008 — duplicated-trace reduced primary bridge (C018-C020/D015-D017).**
   Reconstructs shell/gluing coefficients, regular tangential 5D Palatini rows,
   normal controls, the combined exterior/interface defining matrix, every
   legal Palatini complement, the zero Schur correction, and all residual
   primary nulls. Four semantic mutations must fail. It deliberately omits a
   functional trace adjoint and every first-preservation row.
9. **O009 — static collapse background equations (C021/D018).** Solves the
   complete open-core Cartan system, reconstructs curvature and all ordered-pair
   D004 coframe equations, checks the flat exterior, affine endpoint ideal, and
   D005 shell substitutions, and uses a direct warped-component cross-check.
   Four sign/normalization/equation-coverage/endpoint mutations must fail.
10. **O010 — minimal warped background equations (C022/D019).** Solves the
    common-warp Cartan system, reconstructs all curvature families and five
    Euler forms, checks the regular ODE and endpoint bridge without deleting the
    nonzero-first-integral branch, and evaluates the D005 shell/orbit table.
     Four sign/normalization/equation-coverage/endpoint mutations must fail.
11. **O011 — inverse-source stress and NEC bridge (C023/D020).** Reconstructs
    the Lorentzian effective tensor and all-null reduction, differentiates both
    exact D002 profiles, represents the declared flat-germ order consequences,
    and distinguishes unbounded orthonormal fields from absolute local
    five-volume integrability. Four semantic mutations must fail. It does not
    prove the analytic flat-germ theorem or construct a matter action.
12. **O012 — finite-slope mixed interface variation (C025/D022).** Reconstructs
    the ordered D004 boundary-potential split, the nonzero `43` mixed trace,
    unchanged D005 field incidence, and every persistent shell row. Four
    orientation/order/tangent/cancellation mutations must fail. It does not
    decide tangent-class admissibility, weak-action completeness, or a mixed
    interface repair.
13. **O013 — mixed polarization completion bridge (C026/D023).** Reconstructs
    the rank-three `P43/P34` table, the exact boundary primitive, its complete
    connection/coframe/reference variation, all ten core connection-row
    cancellations, polar coframe/reference consequences, gauge-orbit bulk and
    corner signs, and generic infinitesimal standalone `SO(1,4)` covariance.
    Five semantic mutations must fail. It does not classify global holonomy,
    edge modes, the total frozen interface gauge group, or other actions.

Each obligation includes mutation/negative controls. A passing outcome is
evidence only for the encoded finite exact assertions and does not establish
the conceptual remainder of its claim. An absent `result.json` would mean not
run.

| Obligation | Canonical outcome | Exact assertions | Recorded at | Principal scope |
|---|---|---:|---|---|
| O001 | `passed` | 57/57 | 2026-08-20T12:09:34Z | D002 equalizer, curvature, gauge, and nonbasicness controls |
| O002 | `passed` | 71/71 | 2026-08-20T14:13:21Z | D003/D004 trace, orientation, Palatini, and fixed-radius controls |
| O003 | `passed` | 44/44 | 2026-08-20T14:09:08Z | D005 one-mode field-space curl and complete primitive |
| O004 | `passed` | 60/60 | 2026-08-20T14:08:32Z | D004/D005 reference branches, minors, and exact rank table |
| O005 | `passed` | 40/40 | 2026-08-20T18:18:12Z | D006 cut ranks, null directions, moment maps, and corner witness |
| O006 | `passed` | 36/36 | 2026-08-21T20:58:46Z | Honest D006 shell pullback, cross blocks, null certificates, and moment map |
| O007 | `passed` | 28/28 | 2026-08-22T08:46:29Z | C017 regular-core limit, fixed-radius control, and total exterior cut cancellation |
| O008 | `passed` | 51/51 | 2026-08-22T10:11:06Z | C018-C020 gluing coefficients, 5D tangential rows, complete primary matrix, complements, Schur correction, and nulls |
| O009 | `passed` | 42/42 | 2026-08-22T13:25:51Z | C021 Cartan solve, curvature, 5D/4D Euler forms, endpoint obstruction, and shell compatibility |
| O010 | `passed` | 74/74 | 2026-08-22T13:54:12Z | C022 common-warp Cartan, curvature, Euler, regular ODE/endpoint, and shell bridge |
| O011 | `passed` | 79/79 | 2026-08-22T15:24:41Z | C023 effective stress, profile asymptotics, weighted integrability, and all-null NEC bridge |
| O012 | `passed` | 29/29 | 2026-08-22T16:30:05Z | C025 finite-slope D004 mixed boundary row, unchanged D005 incidence, and persistent shell table |
| O013 | `passed` | 38/38 | 2026-08-22T17:25:13Z | C026 single-primitive reduction, complete variation, orbit signs, and generic infinitesimal covariance |

O002–O004 record the same aggregate shared-infrastructure SHA-256
`0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`
and exact-kernel directory SHA-256
`197024e3f37dff868c931141ce25949e26e2249bd4850d0213ff06e81449268b`.
The O001–O004 results were produced on a dirty worktree at Git commit
`29367ed1e5874e2f3c2aeb1e981f5dd689b3eea7`; their specs, implementations,
and declared infrastructure remain fingerprinted for staleness detection.
O005 reused the unchanged `exact_graded` directory at the same directory
fingerprint but has its own claim-specific implementation and later full
infrastructure fingerprint at Git commit
`6eda62c0325e4feccff7148cb0da877bc028a46b`.
O006 reused that same unchanged kernel and aggregate infrastructure fingerprint
at Git commit `ba26507511bca36d84ad2cfcfdef624292fb0eac`; its canonical result was
recorded from a dirty worktree and fingerprints its distinct claim-specific
implementation.
O007 reused the same unchanged kernel and aggregate infrastructure SHA-256
`0b4aeb783458e144f6b86641ad631d0cb62dcc12398b414a552434f00d211b97`
at Git commit `38f38ea5c5c8419c2c77f4fdfd69870b38ca1595`; its canonical result was
recorded from a dirty worktree and fingerprints its distinct claim-specific
implementation. O007 is correlated with O002/O006 through both infrastructure
and conventions and is not an independent implementation.
O008 reused the same unchanged kernel and aggregate infrastructure fingerprint
at the same recorded Git commit and from a dirty worktree. Its distinct runner
is fingerprinted, but its exact-form and matrix paths remain correlated with
O002-O007 rather than an independent implementation.
O009 again reused that kernel and aggregate fingerprint at Git commit
`38f38ea5c5c8419c2c77f4fdfd69870b38ca1595` from a dirty worktree. Its direct
warped-component contraction avoids the ordered-epsilon Euler helper but shares
the action conventions, arithmetic, and producer model; it is correlated
support rather than an independent implementation.
O010 reused the same unchanged kernel and aggregate fingerprint at the same Git
commit from a dirty worktree. Its distinct runner, full Cartan matrix, component
Einstein path, coordinate-ODE path, and four mutations are fingerprinted, but
they share D004/D005 conventions, arithmetic, infrastructure, and OpenAI
provenance with O009 and are correlated support rather than an independent
implementation.
O011 used no reusable research kernel. Its self-contained exact
polynomial/Laurent/formal-order runner and root orchestration dependencies have
aggregate infrastructure SHA-256
`c161ea4ada2e2a5118552101f73cbe899007cc28701c86677cf238a6f6cb7357` at Git
commit `38f38ea5c5c8419c2c77f4fdfd69870b38ca1595` from a dirty worktree. It
changes the implementation surface but shares D002/D004/D019 assumptions and
the OpenAI producer, so it is correlated rather than independent evidence.
O012 likewise uses a self-contained exact claim-local runner and the same root
orchestration infrastructure fingerprint at that recorded commit from a dirty
worktree. Its canonical result fingerprints spec
`1c300fa4654d9d797f81f9c7657a41aeaa993d857135d30bfe78913355f15ee4` and
implementation
`743ac9e93ff3b6b6795418663c6dfec5649cd10a18d23071f114122a3e7e1616`.
Changing from the shared exterior kernel reduces code dependence but not the
shared D004/D005 conventions or OpenAI producer, so O012 remains correlated.
O013 is also self-contained and uses the same root orchestration fingerprint,
but implements a new exact sparse polynomial/exterior and generic infinitesimal
`SO(1,4)` path rather than reusing O012 or `exact_graded`. Its dirty-worktree
result at Git commit `9bd25b908d2d122b76bcbc97a02b9507fac7439a`
fingerprints spec
`aa5d989347ae6bca0b6201df61f370acfffe8a10c1e5f5e3b49ed32f2a1a3721`
and implementation
`5bf4ea80e6e5109eeb55ece330c353a424b266cd85534612bacbf15eac1aebaa`.
Its generic local covariance identity changes the code path, but D004/D023
conventions and the OpenAI producer remain shared, so it is correlated support.

## Computational representations and methods

### Domain A — kernel-pair forms and explicit gauge jets (O001)

- **Mathematical domain:** a finite formal sector of forms on the two branches
  of `M x_X M`, plus explicit local connection jets.
- **Representation/coefficient system:** a one-off sparse exterior form over
  exact integer/rational coefficient atoms. Ordered basis:
  `du0 < du1 < du2 < ds < dtheta1 < dtheta2`.
- **Primitive operations:** branch-tagged pullback, subtraction, wedge,
  contraction, explicit exterior derivative on declared jets, exact gauge
  substitution, and invertible matrix round trip.
- **Relations/normal form/equality:** wedge antisymmetry and repeated-leg zero;
  a canonical sparse coefficient map; exact map equality, never floating
  tolerance or heuristic simplification.
- **Conventions:** `theta -> theta-alpha`, `A -> A+dalpha`; `n=e4` only in the
  nondegenerate rank-four exterior frame; exact substitutions `rho=drho=0` on
  the collapsed branch.
- **External dependencies/custom infrastructure:** none beyond Python's standard
  library. Keeping P1 self-contained provides a representation path separate
  from the shared kernel used below.
- **Limitations:** this is a finite sector, not a decision procedure for all
  smooth germs, global bundles, or large gauge transformations.
- **Cross-check:** direct hand/set-theoretic pullback reconstruction, including
  the positive-branch control where quotient descent is not the same as
  principal-bundle horizontality.

### Domain B — boundary exterior algebra and Palatini indices (O002)

- **Mathematical domain:** free exterior algebras for the 5D resolution, 4D
  exterior and 3D interface, with explicit internal epsilon contractions.
- **Representation/coefficient system:** sparse forms over exact polynomials
  with rational coefficients and formal atoms `tau,R,rho0,f,kappa4_inv,kappa5_inv`.
  `tau` is the exact circle-period symbol interpreted as `2pi`; binary floating
  `pi` is forbidden.
- **Primitive operations:** wedge, boundary pullback `ds -> 0`, contraction with
  outward normals, fiber-coefficient extraction, epsilon parity and explicit
  ordered antisymmetric-pair enumeration.
- **Relations/normal form/equality:** canonical ordered wedge tuples and exact
  polynomial coefficient maps. `epsilon_01234=epsilon_0123=+1`,
  `epsilon_abcd=epsilon_abcd4`, and both orders of antisymmetric pairs are
  enumerated before canonicalization.
- **Orientation:** `oSigma=du0 du1 du2`, `o4=oSigma ds`,
  `o5=oSigma ds dtheta`; fiber forms are moved right.
- **Scientific rationale:** factorial, wedge-sign, orientation and `2pi`
  mistakes are conclusion-critical for C012 and propagate to C015.
- **Limitations:** bare fixed-interface Einstein–Cartan representative and
  regular descended variations only.
- **Cross-check:** an independently written unordered-pair/dense-array
  enumeration must recover the same split and fixed-radius relation.

### Domain C — field-space differential algebra (O003)

- **Mathematical domain:** polynomial differential forms on the affine
  one-mode field space `(w,a,q,nu)`.
- **Representation/coefficient system:** exact rational polynomials; commuting
  field coordinates and anticommuting `dw,da,dq,dnu`.
- **Primitive operations/relations:** polynomial differentiation, field-space
  wedge, graded Leibniz rule and `d_F^2=0`.
- **Normal form/equality:** canonical polynomial monomials times sorted
  field-differential tuples, compared exactly.
- **Scientific validation requirement:** certify first that the selected
  spacetime/internal contraction is nonzero and lies in the basic compact-
  support variation class. The mode checks an exact restriction of D005, not a
  numerical analogy.
- **Cross-check:** evaluate the original curl directly on two explicit commuting
  variations rather than through the shared differential engine.

### Domain D — interface branch algebra and exact linear maps (O004)

- **Mathematical domain:** six antisymmetric Lorentz-pair components, interface
  two-form coefficients, polynomial action gradients and rational matrices.
- **Coefficient system:** the integral-domain polynomial ring over rationals in
  `b,kappa4_inv,tau,gamma,ell_star,kappa5_inv`; substitutions
  `b=tau*gamma` and `gamma=ell_star*kappa5_inv` are explicit.
- **Bases/conventions:** canonical pairs `a<b`; planar triad
  `(e0,e1,e2)` with `e3=0`; ordered-pair sums are explicit rather than hidden
  Einstein summation.
- **Primitive operations:** exact polynomial differentiation and substitution,
  epsilon/Hodge pair map, rational row reduction/rank/nullspace, minors, and
  exact wedge-curvature evaluation.
- **Normal form/equality:** canonical coefficient vectors and rational reduced
  matrices.
- **Scientific rationale:** exact branch differentiation distinguishes setting
  `a=varpi` before variation from varying an independent reference. Exact rank
  is required; random-matrix sampling is not evidence.
- **Limitations:** no proof of nontrivial bundle covariance, edge charge,
  constraint closure, or a bulk solution.
- **Cross-check:** derive branch equations without differentiating the encoded
  action and derive the `H` kernel analytically from the adapted `M/S`
  decomposition rather than the shared row-reduction code.

### Domain E — interface cut presymplectic matrices (O005)

- **Mathematical domain:** rational `so(1,3)` structure constants and pairing,
  the two-dimensional cut exterior algebra, the exact `6 x 8` coframe-to-`Q`
  differential, and finite antisymmetric presymplectic matrices.
- **Representation:** ordered Lorentz pairs `(01,02,03,12,13,23)`, basis
  `dx1<dx2`, `Fraction` coefficients, canonical sparse forms, and deterministic
  rational RREF. The nonzero common scale is set to `b=1` for ranks and restored
  as `b/2` in the corner witness.
- **Scientific rationale:** the load-bearing assertions are finite exact ranks,
  null directions and signs; random matrices or floating-point sampling would
  be weaker and could conceal convention errors.
- **Trust surface:** the existing exterior, epsilon and rational-matrix
  primitives plus short claim-specific Lorentz/block formulas. No new generic
  presymplectic framework or Engineer work was justified.
- **Cross-check:** five explicit `dQ` pivots, four displayed shell null vectors,
  analytic block-rank addition, and a nonidentity rational Lorentz adjoint.
- **Limitation:** every path omits the bulk kinetic form, total Gauss generators,
  secondary constraints and polarization, so no final gauge/physical conclusion
  is encoded.

### Domain F — honest shell pullback (O006)

- **Mathematical domain:** the same rational Lorentz/cut exterior data as O005,
  but with the shell imposed before differentiation on the 20 coordinates
  `(chi_v[6],xi[6],delta e[8])`.
- **Representation:** the pulled-back potential
  `Theta_B|shell=<Q(e),chi_v-xi>` is differentiated term by term into one exact
  `20 x 20` alternating matrix. `lambda` and `delta lambda` are eliminated;
  the `xi`–`delta e` block is explicit and nonzero.
- **Scientific rationale:** an independent verifier showed that O005's shell
  direct sum had the correct rank but the wrong entrywise form. Equal rank is
  therefore not an adequate acceptance test; O006 requires the honest entries,
  ten null certificates, and inequality from the shortcut.
- **Trust surface:** unchanged `exact_graded` exterior/epsilon/rational-matrix
  primitives plus short claim-specific potential-term and Lorentz formulas. No
  new reusable kernel, environment, CAS, or Engineer work is justified.
- **Cross-checks:** explicit `Q,dQ`; exact antisymmetry; ten named null vectors;
  separately assembled equal-rank shortcut; direct gauge contraction; and four
  process-local semantic mutations.
- **Limitation:** O006 still imports D005's action, shell, and temporal-boundary
  potential and omits all bulk Gauss and polarization data.

### Domain G — total cut coefficient and regular-core limit (O007)

- **Mathematical domain:** exact 4D/5D Palatini momentum components on one
  planar cut, circle pushforward with formal period `tau`, and six-component
  Lorentz bivectors under exact rational dressing.
- **Representation:** sparse exterior forms over exact rational polynomials in
  `rho,R,tau,kappa4_inv,kappa5_inv`, ordered pairs
  `(01,02,03,12,13,23)`, and exact `4 x 4`/`6 x 6` rational matrices. Collapse
  is substitution `rho=0`; no limiting tolerance is used.
- **Scientific rationale:** C017 depends on incident signs, ordered-pair
  factors, fixed-radius normalization, and the direction of the adjoint
  dressing. These are finite decidable assertions for which sampling would be
  weaker.
- **Trust surface:** unchanged `exact_graded` wedge/epsilon/polynomial
  primitives plus claim-local circle extraction and Lorentz adjoint code. A
  dense permutation count and hand boost values provide alternate assembly
  controls; four isolated mutations test discriminating power.
- **Limitations:** O007 imports the regular equalizer, matching shell, and
  unshifted polarization. It does not prove smooth descent, functional
  differentiability, primary stabilization, seed/corner admissibility,
  first-class closure, or a reduced degree count.

### Domain H — duplicated traces and reduced defining primaries (O008)

- **Mathematical domain:** the finite exact content of D015-D017: shell/gluing
  coefficients, regular five-dimensional tangential Palatini forms and normal
  controls, the exterior triad-to-momentum map, finite trace incidence, Lorentz
  coadjoint block, and combined defining-primary matrix.
- **Representation:** canonical sparse exterior maps from `exact_graded`, exact
  `fractions.Fraction` coefficients, ordered Lorentz pairs, and explicit dense
  rational matrices. The complete local matrix has 42 rows on
  `(C_e,C_varpi,Phi_u,Psi_g)`; no floating point, randomization, or CAS
  simplification is used.
- **Scientific rationale:** the load-bearing bridge is sensitive to shell and
  incidence signs, the half-coupling in `dP`, which half of the Palatini form
  receives `B`, complement choice, and the distinction between tangential
  pullback and normal contraction. These are finite decidable assertions.
- **Trust surface and validation:** O008 uses the existing exact kernel plus a
  claim-local form/matrix runner. It compares sparse and independently assembled
  dense `A` and `B`, exhaustively enumerates all 18,564 twelve-row complements,
  checks six `ker(A^T)` certificates, and requires four process-local semantic
  mutations to fail. These paths still share one representation and producer
  model and are not independent confirmation.
- **Canonical outcome:** `passed`, 51/51 assertions. Eight complements are
  admissible and all have zero Schur correction; ranks are `A=12`, `B=5`,
  `A_P=4`, complete `=28`, residual `=4`; the normal control is
  `P_40=dP_40=1/(2 kappa_5)`.
- **Limitations:** trace-map existence, continuity, local surjectivity, global
  clean reduction, functional adjoints, total Hamiltonian, secondary
  constraints, closure, and physical degree count are not encoded. The result
  records `functional_trace_adjoint_encoded: false`.

### Deferred Domain I — functional trace and first preservation (blocked by C021)

- **Re-entry condition:** first supply a bulk-plus-shell background that solves
  the complete equations. C021 excludes the previously presumed static
  unwarped candidate, so implementing functional preservation now would test an
  off-shell background rather than C003.
- **Mathematical domain still required from theory:** one declared bulk field
  and boundary trace space, the trace pairing and adjoint, the reduced total
  Hamiltonian on a boundary-compatible exterior/reference background, and the
  preservation equations for the six Palatini nulls, `Phi_u`, `p_g`,
  `pi_varpi0`, and `pi_e0`.
- **Method not yet selected:** no Sobolev scale, distribution space, symbolic
  functional calculus, Dirac engine, or PDE stack is adopted before the theory
  fixes the regularity, domains, boundary conditions, and exact observable. A
  pointwise incidence matrix is not a substitute for an adjoint trace operator.
- **Required theory bridge before implementation:** derive every first-
  preservation row while retaining torsion/coframe equations; state whether
  multipliers are fixed, secondary constraints arise, or mixed `SO(1,4)` or
  another frozen sector is sourced; isolate any finite rank/closure assertion
  and its assumptions.
- **Trust-surface assessment:** reuse Domain H only for a genuinely finite
  coefficient subproblem. Functional operators or reusable canonical machinery
  would require a new computational contract and possibly research-scoped
  infrastructure; building them now would be speculative.
- **Independence:** a conclusion-critical preservation rank should use an
  alternate functional or matrix reconstruction, and may warrant an independent
  implementation if the result depends materially on trace discretization or
  elimination order. This is distinct from approval-gated Opus finalization.

### Domain J — static unwarped background equations (O009)

- **Mathematical domain:** the exact cohomogeneity-one coframe
  `E=(dt,dx,dy,ds,rho dtheta)` on the nondegenerate open core, all 50 spin-
  connection coefficients in the coframe basis, torsion/curvature exterior
  forms, the five D004 coframe Euler forms, flat 4D exterior residuals, affine
  endpoint data, and the finite D005 shell substitution table.
- **Representation:** exact `Fraction` and sparse polynomial coefficients,
  canonical `exact_graded` exterior maps on explicitly ordered coordinate and
  coframe bases, and rational RREF for the `50 x 50` Cartan and endpoint
  systems. `rho'/rho` is used only on `rho>0`; conversion
  `(rho'/rho)E4=rho' dtheta` removes division before curvature and endpoint
  comparisons.
- **Scientific rationale:** C021 hinges on a spin-connection sign, ordered-pair
  multiplicities, independent normal/circle equations, and two endpoint data.
  These are small exact assertions for which numerical ODE integration would be
  weaker and a general CAS would add an unnecessary simplification surface.
- **Trust and alternate path:** O009 enumerates D004 Euler forms explicitly and
  separately contracts a direct warped-plane Riemann component to Ricci,
  scalar, and Einstein components without the Euler helper. It also builds
  `P^-` by local parity independently of `Q`. Shared conventions, kernel,
  arithmetic, and OpenAI provenance remain correlated.
- **Canonical outcome:** `passed`, 42/42 assertions. Cartan rank is 50 with sole
  independent coefficient `omega^(34)_4=-rho'/rho`; the Euler coefficient
  vector is `(k-Lambda_5)^3,(-Lambda_5)^2`; endpoint ranks are two with the full
  jet and one with only `rho(0)=0`; all shell equalities hold. All four semantic
  mutations were effective.
- **Limitations:** O009 does not prove that the D002 category is compulsory,
  exhaust backgrounds or actions, construct a warped solution, define a
  functional trace, or decide broad C002/C003. No new infrastructure or
  research environment was justified.

### Domain K — minimal common-warp background equations (O010)

- **Mathematical domain:** the exact cohomogeneity-one coframe
  `E^i=w dx^i` for `i=0,1,2`, `E^3=ds`, `E^4=rho dtheta`; all 50
  spin-connection coefficients; sparse torsion, curvature, and five D004 Euler
  forms; denominator-cleared coordinate ODEs; endpoint linear data; and the
  finite D005 planar shell table.
- **Representation:** exact `Fraction` coefficients, free sparse polynomials in
  `A,p,q,r,Lambda_5` and coordinate-jet atoms, canonical `exact_graded`
  exterior maps, and rational RREF. Ratios are used only on `w,rho>0`; endpoint
  assertions use regular equations multiplied by the required positive powers
  of `w` and `rho`.
- **Scientific rationale:** C022 hinges on three additional warped curvature
  families, the complete Euler vector `(S,S,S,H,J)`, preservation of both
  `w'/rho=C` branches, and the order in which endpoint jets are imposed. These
  are finite exact assertions for which floating ODE integration or heuristic
  CAS simplification would be weaker.
- **Trust and alternate path:** the existing fingerprinted exact kernel is
  adequate, so no Engineer or new environment is justified. A separately
  assembled component Einstein/constant-curvature path and direct coordinate-
  ODE identities must cross-check the epsilon enumeration. Four isolated
  semantic mutations test plane-curvature sign, cosmological normalization,
  circle-equation coverage, and endpoint uniqueness. Shared conventions,
  infrastructure, arithmetic, and OpenAI provenance remain correlated.
- **Canonical outcome:** `passed`, 74/74 assertions. Cartan rank is 50; all four
  curvature families and the Euler vector `(S,S,S,H,J)` agree; both `C`
  branches are represented before endpoint elimination; endpoint/polar ranks
  are two/one; six shell momentum rows are nonzero; and all four mutations are
  effective.
- **Limitations:** O010 cannot establish that D002/D004/D005 is compulsory,
  exhaust source-free metrics, or decide sourceful, anisotropic, lapse,
  off-diagonal, moving-interface, functional-preservation, or broad C002/C003
  questions.

### Domain L — inverse-source regularity (D020/C023/O011)

- **Derived question and answer:** D020 defines
  `G_AB+Lambda_5 eta_AB=kappa_5 T_AB` in the zero-spin-current D019 geometry,
  fixes boundedness in an orthonormal frame, componentwise absolute `L1` against
  `w^3 rho ds` on compact tangential cells, and the NEC for every null vector.
  For both exact D002 profiles and every common warp smooth-flat to one,
  `rho''/rho` diverges positively: curvature/stress are unbounded and both
  independent NEC coefficients are eventually negative, while each absolute
  stress component is volume-integrable.
- **Checkability assessment:** O011 tests the finite contraction, profile,
  order-bookkeeping, and endpoint-integrability bridge. The analytic theorem
  that every smooth zero extension supplies arbitrary flat orders remains a
  displayed derivation premise rather than a machine theorem. Existence of a
  covariant matter action and physical source dynamics are not usefully checked
  by this obligation.
- **Selected representation and rationale:** use exact Lorentzian component
  contraction and sparse rational/polynomial arithmetic, plus a claim-local
  exponent/order representation for the two fixed profiles and the declared
  flat-germ premise. Equality is canonical coefficient/exponent equality; no
  floating sampling or heuristic simplification is allowed. The inherited
  `exact_graded` primitives may be reused if Scientific Computation finds them
  adequate, but no new reusable kernel or environment is scientifically
  justified.
- **Trust and independence:** Scientific Computation must reconstruct the
  curvature-to-Einstein contraction rather than insert D020's target tensor,
  retain both NEC channels, and use semantic mutations for the timelike sign,
  profile derivative, channel coverage, and bounded-versus-integrable
  distinction. An alternate component/order assembly is recommended, but it is
  correlated support rather than independent verification.
- **Canonical outcome:** `passed`, 79/79 assertions. The executable reconstructed
  ten off-diagonal stress zeros, both exact profile tables and positivity
  thresholds, both independent NEC channels, the declared flat-order bridge,
  and the distinct unbounded versus absolute-`L1` verdicts. All five semantic
  mutations were effective. It used self-contained exact `Fraction`, sparse
  polynomial/Laurent, and formal-order code rather than `exact_graded`.
- **Failure modes attacked:** mistaking volume-integrated finiteness for bounded
  orthonormal stress; inferring an energy condition from one component; hiding
  divergent ratios behind flat coordinate forms; or treating an effective
  conserved tensor as a realized local matter action.

### Deferred Domain M — profile-independent endpoint comparison (D021/C024)

- **Derived question and answer:** for every positive
  `rho in C^1([0,epsilon)) intersect C^2((0,epsilon))` with zero endpoint value
  and proper-distance slope, D021 proves
  `limsup_(s->0+) rho''/rho=+infinity`. The invariant torsion-free
  radial-circle sectional curvature is therefore unbounded below on every
  endpoint neighborhood. A regular lapse gives the exact combination
  `[rho_xx-(N_x/N)rho_x]/(N^2 rho)`.
- **Representation and checkability assessment:** the decisive proof is an
  inequality plus two integrating factors and endpoint limits. Exact symbolic
  differentiation can check the oscillatory counterexample and lapse chain
  rule, but cannot decide the universal quantifier. A faithful executable
  obligation would require a formal real-analysis representation of ordered
  functions, one-sided limits, positivity, and integration/monotonicity.
- **Method decision:** no proof assistant, CAS, custom kernel, or research
  environment is selected. Building that infrastructure for this transparent
  lemma would add a larger trust and producer surface than the current
  scientific risk justifies. This is a phase-specific deferral, not a claim that
  C024 is unformalizable.
- **Failure modes attacked analytically:** dropping the zero-slope datum is
  exposed by `rho=cs`; the dimensionally repaired smooth-flat oscillatory
  witness has both infinite-sign subsequential limits and blocks an erroneous
  actual-limit or eventual-sign promotion; regular-lapse covariance blocks a
  raw-coordinate escape.
- **Independence:** D021 and both critiques use `openai/gpt-5.6-sol`, and its
  curvature bridge imports D019 conventions. The second critique resolves the
  first report's dimensional revision but remains same-model, non-independent
  evidence. No Opus audit is requested for this intermediate theorem.

### Domain N — finite-slope mixed interface variation (D022/C025/O012)

- **Derived question and answer:** D022 admits the finite one-sided tangent
  `delta omega43=delta chi43 dtheta` for `rho=c s` while keeping D004/D005
  unchanged. The ordered D004 potential gives
  `+(2pi/kappa_5)delta chi43 o_Sigma`; D005 has no mixed incidence, so free
  variation is incompatible with the planar rank-three triad. Fixing slope and
  holonomy leaves only a fixed-boundary background.
- **Representation and rationale:** O012 uses a self-contained finite exterior
  algebra and sparse exact rational polynomials, complete five-index epsilon
  enumeration, rightmost circle-leg extraction, an explicit frozen D005
  field/variation table, and exact shell substitutions. The assertion is a
  finite sign/factor/incidence problem; a CAS, weak-geometry solver, or reusable
  BV kernel would enlarge rather than reduce trust.
- **Canonical outcome:** `passed`, 29/29 assertions. The executable recovered
  D004 split coefficients `1/4` and `1/6`,
  `epsilon_(3bcd)e^b e^c e^d=-6 o_Sigma`, the exact positive mixed coefficient,
  no D005 `chi43` variable, and all persistent shell rows. Core-sign,
  omitted-order, smooth-flat-zero, and fictitious-cancellation mutations each
  exited `1`.
- **Trust boundary:** the direct hand/permutation count and mutations are
  correlated controls. O012 does not establish that the chosen finite tangent
  is physically mandatory, define intrinsic lower-regularity traces, validate
  general nonlinear distribution products, or classify a future mixed
  completion.
- **Disposition:** D023 subsequently specified one primitive, its full
  reference connection, companion variations, and gauge-orbit action; Domain O
  records the resulting O013 representation. O012 remains only the finite C025
  coefficient/incidence bridge and is not presumed to decide field-space
  integrability or full `SO(1,4)` reduction.

### Domain O — single mixed polarization completion (D023/C026/O013)

- **Derived question and answer:** D023 tests only
  `B_ref=-integral (omega_+-barOmega)^AB wedge P^(5)_AB`. The primitive cancels
  the C025 `43` row but changes polarization. Fixed reference data anchor
  `c=barChi43`; unrestricted reference or seed variation imposes `P^(5)=0` and
  rank at most two; a fixed-seed orbit preserves only a fixed holonomy
  conjugacy class and adds `D_barOmega P=0` plus a corner moment map.
- **Representation and rationale:** O013 uses a self-contained exact sparse
  polynomial/exterior algebra over `Fraction`, complete ordered five-index
  enumeration, explicit field-space Leibniz differentiation, and generic
  component atoms for all five coframes, ten connection differences, and ten
  infinitesimal `so(1,4)` generators. Canonical tuple equality proves the
  encoded local infinitesimal covariance identity; no sampling, float, CAS, or
  shared scientific kernel is used. Reusing `exact_graded` would enlarge the
  fingerprinted surface without removing claim-specific semantics.
- **Canonical outcome:** `passed`, 38/38 assertions. The exact result recovers
  `P43=-oSigma/(2kappa5)`, `P34=+oSigma/(2kappa5)`,
  `B_ref=-(tau/kappa5)k oSigma`, all ten connection-row cancellations, the
  `-3 alpha k tau/kappa5` coframe-rescaling residual, nonzero free-reference
  row, orbit signs `(+1,-1)`, and zero generic simultaneous-covariance residual.
  All five fresh-process semantic mutations exited `1`.
- **Trust boundary and independence:** a direct complement/permutation count is
  separate from the primary momentum constructor, but O013 shares D004/D023
  conventions and the OpenAI producer. It is correlated machine support, not
  independent verification. It does not test finite/large gauge transformations,
  global holonomy, edge classification, total D005 covariance, or another
  action.
- **Next representation decision:** the research has crossed phase-transition
  trigger 8. No finite normal/reduction-field, mixed Gauss, or canonical
  representation is selected until theory defines that field, its gauge action,
  variational primitive, and the observable deciding whether the `43` datum is
  gauge, superselected, or physical. O013 must not be extended by assumption to
  that wider system.

No general-purpose CAS is used as a conclusion-critical equality oracle. A CAS
may be used later only as an explicitly independent targeted exact cross-check
with its assumptions and normal form recorded.

## Research-specific computational infrastructure

O002–O004 share enough conclusion-critical graded algebra to justify one small
project-owned exact kernel under `research/computation/exact_graded/`. O001 stays
self-contained to retain a materially different representation path.

### Frozen computational contract

- **Domain:** sparse multivariate polynomials over `fractions.Fraction`, sparse
  exterior forms over a caller-declared ordered basis, rational matrices, and
  Levi-Civita signs relative to an explicit orientation tuple.
- **Canonical semantics:** polynomial monomials are sorted
  `(generator, exponent)` tuples; form monomials are strictly increasing basis
  tuples; a repeated exterior generator is zero; equality is exact canonical
  map equality. Float coercion, tolerances, randomization and heuristic
  simplification are forbidden.
- **Minimum API:** exact polynomial construction/arithmetic/differentiation/
  substitution; exterior-algebra basis construction, addition, scalar
  multiplication and wedge; pullback, contraction and field-space exterior
  derivative; Levi-Civita sign; rational RREF/rank/nullspace; deterministic
  serialization.
- **Required invariants/tests:** coefficient collection; wedge bilinearity,
  associativity, graded commutativity and repeated-leg zero; `d_F^2=0` and
  graded Leibniz; pullback functoriality and wedge compatibility; contraction
  signs; every epsilon permutation and duplicate-index zero; exact rank and
  nullspace controls; deterministic serialization; rejection of floats,
  negative polynomial exponents, duplicate basis declarations, basis
  mismatches, invalid pullbacks and non-rational matrices.
- **Invalid/unsupported inputs:** ambiguous bases, implicit metric/index raising,
  symbolic division, zero-divisor coefficient systems and numerical matrices.
- **Non-goals:** smooth-germ/asymptotic algebra, quotient topology or diffeology,
  tensor automation, gauge-group solving, factorization/Groebner bases, theorem
  proving, numerical linear algebra, Markdown parsing, and generic canonical
  dynamics. O005 reused only the already-contracted exterior and matrix API.
- **Dependent obligations:** O002, O003, O004, O005, O006, O007, O008, O009 and O010; each must fingerprint the entire
  kernel directory. The kernel is methodology, not evidence.

Engineer is required because this reusable primitive set and its law tests are
distinct from the claim-specific assertions. Scientific Computation owns this
contract, must review the implementation, and must separately validate the
D003 orientation signs, D004 planar coefficient, D005 one-mode derivative and
`H`-matrix rank before writing the obligation runners. Engineer must not write
any `ONNN/run.py`.

The root locked Python environment is sufficient: Python 3.11+, `fractions`,
`dataclasses`, `itertools`, and standard collections. No scientific package,
external executable, seed, floating precision, hardware-specific setting or
new `research/environment/` manifest is justified. The architecture
`pyproject.toml`/`uv.lock` remain orchestration provenance, not a new scientific
stack; dependent specs will declare the exact paths they materially use.

## Numerical and formal evidence standards

- **Exact symbolic/exact algebra:** `passed` only when every declared identity,
  zero/nonzero witness, rank, nullspace, sign, factor and negative control agrees
  in the named canonical representation. `failed` means any exact mismatch.
  `inconclusive` is reserved for a predeclared unsupported or ambiguously tagged
  domain case; an exception or malformed implementation is an execution error.
- **Formal proof:** `passed` would require the frozen proposition, assumptions,
  imports/axioms and checker version to be recorded and accepted. No formal
  obligation is adopted in this migration.
- **Certified numerical result:** requires a stated enclosure/error certificate
  proving the threshold. None is used here.
- **Converged numerical evidence:** requires a predeclared refinement ladder,
  norm, tolerance and observed rate. None is used here.
- **Floating-point or randomized diagnostics:** suggestive/regression evidence
  only; never sufficient for the exact claims in D002–D005.
- **Independent implementation:** counts as independent only when it changes a
  material representation, algorithm or library and does not share the custom
  kernel or conclusion-critical helper path.

All acceptance criteria and negative controls are declared before
implementation. A bad criterion is superseded rather than edited after output.

## Independence strategy

All thirteen required obligations use an alternate analytic path because they test
load-bearing reasoning. The primary implementations and exact kernel are
not mutually independent when they share `exact_graded/`.

- O001: direct set-theoretic branch-table reconstruction, with no shared kernel.
- O002: unordered-pair/dense coefficient enumeration versus the primary ordered
  sparse exterior representation.
- O003: direct evaluation on two variations versus polynomial field-space `d_F`.
- O004: analytic branch elimination and `M/S` kernel decomposition versus action
  differentiation and rational row reduction.
- O005: explicit pivots/null vectors and first-order block-rank reasoning versus
  assembled presymplectic matrices and exact RREF. This is correlated, not an
  independent verification.
- O006: explicit potential-first shell assembly and ten null certificates versus
  RREF, with the O005 equal-rank shortcut retained as an entrywise negative
  control. The model-separated C016 verifier supplied the independent hand path;
  O006 itself is correlated machine evidence.
- O007: dense permutation/word coefficient reconstruction and hand rational
  boost values versus sparse exterior/Lorentz assembly. It shares the kernel,
  shell, and conventions with earlier checks and is correlated evidence.
- O008: direct dense `A/B` assembly, exhaustive complement enumeration, and
  explicit null certificates versus sparse exterior and block-matrix assembly.
  It shares the kernel, finite incidence, conventions, and OpenAI producer with
  earlier checks and is correlated evidence, not an independent implementation.
- O009: direct warped-component Riemann/Ricci/Einstein contraction versus the
  ordered-epsilon Palatini Euler enumeration, plus a full Cartan solve and
  endpoint controls. It shares D004 conventions, exact infrastructure, and the
  OpenAI producer, so it remains correlated evidence.
- O010: a component Einstein/constant-curvature reconstruction and direct
  denominator-cleared ODE path versus the ordered-epsilon Euler enumeration,
  plus full Cartan and mutation controls. It shares D004/D005 conventions,
  exact infrastructure, and OpenAI provenance, so it is correlated evidence,
  not an independent implementation.
- O011: a self-contained Lorentzian component contraction, exact Laurent profile
  table, explicit null witnesses, and formal-order bookkeeping versus D020's
  differential-form/asymptotic derivation. It does not reuse `exact_graded`, but
  imports D002/D019 conventions and analytic flat-germ premises and shares the
  OpenAI producer, so it remains correlated support rather than an independent
  implementation.
- O012: complete ordered five-index enumeration plus a separate direct
  pair/permutation count and four semantic mutations versus D022's hand
  reduction. It is self-contained but imports D004/D005 conventions and shares
  the OpenAI producer, so it is correlated support rather than independent
  confirmation.
- O013: generic sparse-polynomial infinitesimal `SO(1,4)` covariance and full
  field-space differentiation plus a direct complement/permutation momentum
  count and five semantic mutations versus D023's hand variation. It does not
  reuse O012 or `exact_graded`, but shares D004 conventions and the OpenAI
  producer, so it remains correlated support rather than independent
  confirmation.

Any future current-lifecycle independent verification must be explicitly
user-approved and use the reserved `anthropic/claude-opus-5` verifier. It must
review the old derivation, old reports, plan, contracts, infrastructure/tests,
research-specific validation, specs, runners and canonical results. Producer
provenance includes the current OpenAI director, Scientific Computation, and
every material Engineer model, as well as historical producers. Opus is
ineligible if it appears in that set. Deterministic execution supplies outcomes
but not model independence. Seven pre-cutover reports remain marked
`legacy: true` and cannot satisfy this gate; C016 retains its explicitly
user-approved Opus report.

## Phase-transition triggers

Redesign this strategy if any of the following occurs:

1. a required exact obligation fails for a scientifically faithful encoding;
2. a verifier finds that the finite exterior/field-space representation omits a
   conclusion-critical identity or imposes an extra one;
3. the state space moves beyond the basic fixed-interface sector to nonbasic
   circle modes, full `SO(1,4)` normal dynamics, moving interfaces or corners;
4. the interface-only D006 regime is extended to a trace-aware
   bulk-plus-interface Hamiltonian system with primary/secondary constraints
   and total Gauss generators;
5. a concrete hyperbolic PDE is fixed, requiring principal-symbol and energy
   estimates;
6. a defect solution is posed, requiring a research-scoped numerical
   environment, convergence and error analysis;
7. the program reaches Hopf configuration-space topology or quantum holonomy,
   requiring computational topology/formalization rather than this graded
   exterior kernel;
8. a proposed mixed interface completion introduces new fields, covariance,
   field-space primitives, edge symplectic data, or full `SO(1,4)` reduction;
   its representation must be reassessed before any post-O012 obligation.

Trigger 8 occurred in CY007. Domain O records the bounded O013 reassessment for
the one specified primitive; it does not authorize reuse for the now-required
normal/reduction-field theory.

At the immediate frontier, O006 closes the honest interface-shell gap, O007 the
finite total-cut cancellation, O008 the selected duplicated-trace defining-
primary matrix, O009-O010 the unwarped/common-warp source-free background
bridges, O011 the two-profile inverse-source bridge, and O012 the finite-slope
mixed-interface coefficient/incidence bridge. O013 now closes the finite bridge
for the first tensorial-difference polarization primitive. No computation is
queued.
D021/C024 close the zero-slope profile-rate escape; D022/C025 show that the
selected nonzero-slope attachment is separately flat but activates an
uncancelled mixed D004 boundary equation under free finite tangents. D023/C026
then show that the first full covariant polarization primitive cancels that row
but leaves only external reference amplitude, rank degeneracy, or fixed-holonomy
edge structure. The next cheapest theory discriminator is an explicit minimal
normal/reduction field relating core `SO(1,4)` to exterior `SO(1,3)`, with a
declared observable deciding whether the normal-plane datum is gauge,
superselected, or physical. Its fields and equations must be derived before a
method or O014 is selected. Planned Domain I resumes only if that or another
explicitly declared complete action admits an actual background. The present
exact kernels are not presumed adequate for full mixed gauge reduction,
functional trace brackets, constraint closure, or PDE questions.

## Deferred or non-machine-checkable issues

- C001–C006 remain conjectural and lack defined objects required for meaningful
  machine obligations.
- C007’s cone homeomorphism and covering/local-ring theorem, and C008’s full
  `C-infinity` germ obstruction, are analytically stronger than finite
  diagnostics; formalization is deferred rather than replaced by sampling.
- C011’s absence-of-canonical-choice conclusion is explicitly
  `not-applicable` for machine verification in this phase; its exact algebraic
  premises are covered upstream and an independent verifier may reject this
  classification.
- C013’s statement is bounded to the three completion families varied in D004;
  no exhaustive automated search over local boundary actions is claimed.
- Gauge-versus-physical status of the C015/C016 edge/reference sector, moving-
  interface variation, constraint closure, hyperbolicity and positivity remain
  outside migration. Existing derived results may be used exploratorily only
  with these dependencies and pending verification visible.
- C017's finite cut cancellation is machine-checkable and passed; its explicit
  non-decision clause remains non-machine-checkable until the trace-aware total
  constrained phase space is defined.
- C018's finite gluing coefficients are checked, but existence and analytic
  properties of the assumed trace maps and global reduced-phase-space
  equivalence are not usefully decided by O008.
- C019's regular tangential theorem and normal witness are checked. Functional
  post-gluing brackets require a different trace-domain representation.
- C020's defining-primary ranks and Schur result are checked. Its explicit
  non-decision about preservation, closure, and physical status remains outside
  any current machine obligation.
- C021's restricted equation and endpoint bridge is checked. Existence of a
  warped, sourceful, mixed/nonbasic, moving-interface, or alternative-action
  background remains a new analytic question, not an untested clause of C021.
- C022's common-warp equation and endpoint bridge is checked by passing O010.
  This cannot exclude anisotropic/off-diagonal or sourceful backgrounds and
  does not decide broad C002/C003.
- C023's two-profile effective-stress, weighted-integrability, and NEC bridge is
  checked by passing O011. C024 now supplies the all-profile geometric
  unbounded-curvature input, but an all-profile stress/NEC/`L1` theorem and
  realization by a healthy local matter action remain analytic and dynamical
  questions outside O011 and C024.
- C024's comparison theorem and regular-lapse curvature bridge are analytically
  derived. Finite symbolic regressions cannot test the universal quantifier;
  formal real-analysis verification is possible only with materially more
  infrastructure and is deferred rather than replaced by profile sampling.
- C025's finite D004 coefficient, frozen D005 incidence, and persistent shell
  table are checked by passing O012. Whether the finite mixed tangent belongs to
  the correct physical quotient category, whether fixing it is principled, and
  whether another covariant integrable mixed completion succeeds remain theory
  questions outside the obligation; C026 tests only one primitive.
- C026's finite primitive reduction, complete variation, orbit signs, and local
  infinitesimal standalone covariance are checked by passing O013. Global
  holonomy, large-gauge sectors, edge classification, total D005 covariance,
  normal/reduction-field dynamics, and every other action remain outside it.

## Known limitations and risks

- A finite basis can faithfully check encoded exterior identities but cannot
  prove quantification over arbitrary smooth germs without a separate theorem.
- Exact canonical equality is only as faithful as the declared algebraic
  relations; accidental extra identities are a primary verifier target.
- Ordered versus unordered antisymmetric-index conventions, outward-normal
  signs, fiber-form ordering and ordinary versus normalized circle integration
  are correlated failure surfaces across O002 and O004.
- The one-mode field-space check establishes nonclosure by a witness and exact
  restriction; it does not classify the full infinite-dimensional field space.
- The custom kernel creates a shared trust surface for O002–O004. Passing law tests
  shows conformance to the contract, not that the contract models the physics.
- The fixed-reference C015 result is covariance of a family with geometrically
  transforming background data, not established gauge redundancy in one fixed
  sector. “Nondegenerate branch” means algebraic admission of a rank-three
  interface triad, not a proved bulk-compatible solution.
- Varying vertical normalization adds an equation that is redundant after the
  free-coframe equations in D005; fixing the period defines the normalized
  principal-connection variation class and avoids adding that equation, rather
  than being proved necessary for all consistent repairs.
- Reports marked `legacy: true` did not review this plan, infrastructure or
  obligations. Their scientific reconstructions remain archival evidence, but
  they do not satisfy the current Opus evidential chain by themselves.
- The attempted Anthropic verification of C016 was interrupted before a report
  was produced. Tool access recorded in provenance is not a verification
  artifact. A later bounded `anthropic/claude-opus-5` audit produced a qualifying
  report and independently reconstructed C016.
- O005's hard-coded fixed-shell zero, direct-sum shell form, and self-comparison
  shell moment-map assertion do not discriminate the honest pullback. O006 is
  the adopted machine evidence for those shell clauses; O005 remains durable
  rather than being deleted or silently rewritten.
- W001 branches share D004-D006 and one producer model. Internal critiques
  required revision of D007-D008 and D010-D014. In particular, a regular core
  Palatini shared-row overlap was not established, the proposed singularity-
  robust rank bound lacked clean-splitting hypotheses, and formal compensators
  were not admissible action/Gauss completions.
- CY001 derivations, critics, and O008 share D004-D006 conventions and the same
  OpenAI model. D015's trace equivalence is conditional; D016 distinguishes
  tangential pullback from normal contraction; D017/O008 establish only the
  pointwise defining-primary algebra. None defines a functional trace adjoint
  or permits primary null directions to be labelled gauge or physical.
- D018, its critic, and O009 share D002/D004/D005 assumptions and the OpenAI
  producer model. The exact restricted obstruction is robust to the recorded
  sign, coefficient, omitted-equation, endpoint, and polar-cap attacks, but it
  must not be generalized to warped or sourceful backgrounds. Shell
  compatibility and bulk solution existence are distinct.
- D019, its critic, and O010 share the same category/action/shell chain
  and OpenAI model. The common-warp no-solution argument is narrower than a
  general cohomogeneity-one theorem; a lapse, anisotropic warps, off-diagonal
  fields, weaker regularity, sources, or a different topology change the
  problem.
- D020, its critic, and O011 share D002/D004/D019 conventions and the OpenAI
  producer. O011 changes the claim-local representation and does not reuse
  `exact_graded`, but it imports the flat-germ and exponential-domination
  premises. Its passing result cannot turn an effective conserved tensor into a
  matter action or generalize two explicit profiles to the full smooth-flat
  class.
- D021 and both internal critiques use the same OpenAI model and import D019's
  curvature convention. The first critique correctly required dimensional
  scales in the oscillatory witness; the revised artifact and second critique
  resolve that defect. Their agreement remains same-model and cannot promote
  C024 to independently verified. The theorem supplies only `limsup=+infinity`
  and unbounded sectional curvature, not an actual limit, eventual sign, source
  theorem, or universal H003 result.
- D022, its critic, and O012 share D002/D004/D005 conventions and the OpenAI
  producer. O012 changes to a self-contained representation and catches the
  declared sign/order/incidence mutations, but it encodes rather than proves
  the finite tangent class and frozen D005 field content. Its pass cannot
  establish a general lower-regularity action, rule out mixed counterterms, or
  promote C025 beyond its restricted derived status.
- D023, its critic, and O013 share D004/D005/D022 conventions and the OpenAI
  producer. O013 uses a new self-contained exact representation and a generic
  polynomial infinitesimal-covariance identity, but it cannot classify global
  holonomy or edge modes, supply the missing total-interface reduction field,
  test another primitive, or promote C026 beyond restricted derived status.

## Related decisions

- `research/DECISIONS.md`, **2026-08-20: Adopt current computational-verification semantics for legacy work**.
- `research/DECISIONS.md`, **2026-08-20: Use a minimal exact graded kernel for the migration obligations**.
- `research/DECISIONS.md`, **2026-08-21: Treat the interrupted C016 audit as no evidence and stop at the missing bulk canonical system**.
- `research/DECISIONS.md`, **2026-08-21: Verify C016 and replace its shell shortcut with O006**.
- `research/DECISIONS.md`, **2026-08-22: Migrate live research to the exploration and approval-gated verification lifecycle**.
- `research/DECISIONS.md`, **2026-08-22: Adopt the total-cut cancellation and converge on a trace-aware primary system**.
- `research/DECISIONS.md`, **2026-08-22: Freeze duplicated traces and proper outer-corner gauge for the first convergence cycle**.
- `research/DECISIONS.md`, **2026-08-22: Close the defining-primary question and require functional preservation next**.
- `research/DECISIONS.md`, **2026-08-22: Reject the unwarped static background before preservation**.
- `research/DECISIONS.md`, **2026-08-22: Close the common-warp escape and test source regularity next**.
- `research/DECISIONS.md`, **2026-08-22: Reject the ordinary regular-source escape for the exact D002 profiles**.
- `research/DECISIONS.md`, **2026-08-22: Close the profile-rate escape and relax only endpoint regularity next**.
- `research/DECISIONS.md`, **2026-08-22: Close the unchanged-action finite-slope escape and test one mixed completion**.
- `research/DECISIONS.md`, **2026-08-22: Reject the single polarization repair and expose the reduction-field gate**.
- Earlier scope and category choices remain recorded in the 2026-08-19 entries;
  the migration does not rewrite them.
