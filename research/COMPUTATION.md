# Computational Verification Strategy

Status: active — corrected fixed-interface shell verification; bulk Gauss phase deferred
Last updated: 2026-08-21T21:05:00Z

Research question: Does there exist a resolution-independent, Lorentz-covariant classical `4 <-> 5` framework, formulated without an inverse coframe at rank change, whose bulk and transition equations follow from one variational principle and whose linearized initial-value problem is free of an evident constraint inconsistency, ghost, or loss of predictivity?

This is the project-specific methodology for testing research recorded in
`D001`–`D006`. It does not retroactively turn historical calculations into
machine evidence. D006 has completed the bounded interface-only canonical
analysis. O005 tests its off-shell and residual-block algebra; a model-separated
audit found O005's shell shortcut under-discriminating, and O006 now constructs
the honest pulled-back shell form. None supplies the omitted bulk Gauss system
required for a final gauge/physical classification.

## Current research phase

The existing work is in a fixed-interface, exact-algebraic foundation regime.
The benchmark object is the local non-pure quotient
`X=[U x I x S1]/~`, with an exactly collapsed circle for `s<=0`, together
with two infinitely flat resolutions. The load-bearing derivations use:

- quotient and ambient smooth-function algebras and kernel-pair form descent;
- finite exterior algebras of differential forms with exact wedge signs;
- oriented boundary pullback and circle pushforward;
- first-order Einstein–Cartan/Palatini coframe and connection variations;
- field-space exterior differentiation;
- finite-dimensional exact linear maps on Lorentz-valued interface forms.

The strict derivational backbone of the present frontier is

```text
C009 and C010 -> C012 -> C013 -> C014 -> C015 -> C016,
```

with C011 excluding an autonomous bare-quotient measure/incidence choice and
C007–C008 fixing the local category benchmark. C016 establishes exact
interface-only presymplectic ranks and a corner-charge witness on one planar
branch, but deliberately leaves total constraint closure undecided because the
bulk symplectic form and Lorentz Gauss generators are absent.

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
| C016 | O005 checks exact `dQ`, off-shell ranks and residual-block algebra; O006 checks the honest 20-dimensional shell pullback, cross blocks, nullity, moment-map sign, and planar witness. | A completed bulk-plus-interface canonical formulation could expose total Gauss rank and constraint-closure obligations. | Whether the residual rank-ten block is physical, second class, or removed by first-class total gauge in the presently omitted bulk system. |

## Current machine-check obligations

The program now has six required exact obligations, prioritized by the actual
dependency graph rather than chronology. None had a result at allocation time,
and all six now have current deterministic `passed` results.

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
- **Dependent obligations:** O002, O003, O004, O005 and O006; each must fingerprint the entire
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

All six required obligations use an alternate analytic path because they test
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

Fresh independent verification must review the old derivation, old reports,
plan, contracts, infrastructure/tests, research-specific validation, specs,
runners and canonical results. Producer provenance includes the current
OpenAI director, Scientific Computation, and every material Engineer model, as
well as historical producers. A verifier model present in that set is
ineligible. Deterministic execution supplies outcomes but not model independence.

## Phase-transition triggers

Redesign this strategy if any of the following occurs:

1. a required exact obligation fails for a scientifically faithful encoding;
2. a verifier finds that the finite exterior/field-space representation omits a
   conclusion-critical identity or imposes an extra one;
3. the state space moves beyond the basic fixed-interface sector to nonbasic
   circle modes, full `SO(1,4)` normal dynamics, moving interfaces or corners;
4. the interface-only D006 regime is extended to a complete bulk-plus-interface
   Hamiltonian system with primary/secondary constraints and total Gauss generators;
5. a concrete hyperbolic PDE is fixed, requiring principal-symbol and energy
   estimates;
6. a defect solution is posed, requiring a research-scoped numerical
   environment, convergence and error analysis;
7. the program reaches Hopf configuration-space topology or quantum holonomy,
   requiring computational topology/formalization rather than this graded
   exterior kernel.

At the immediate frontier, O006 closes the known finite shell-representation
gap, and no additional finite interface matrix is expected to discriminate H002
from restricted H003. The next theory object would be the
bulk-plus-interface Hamiltonian/Gauss system itself. New computation is deferred
until that object exists; the present exact kernel is not presumed adequate for
constraint closure or PDE questions.

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
- Legacy verification reports did not review this plan, infrastructure or
  obligations. Their scientific reconstructions remain evidence, but they do
  not satisfy the fresh computational evidential chain by themselves.
- The attempted Anthropic verification of C016 was interrupted before a report
  was produced. Tool access recorded in provenance is not a verification
  artifact. A later bounded `anthropic/claude-opus-5` audit produced a qualifying
  report and independently reconstructed C016.
- O005's hard-coded fixed-shell zero, direct-sum shell form, and self-comparison
  shell moment-map assertion do not discriminate the honest pullback. O006 is
  the adopted machine evidence for those shell clauses; O005 remains durable
  rather than being deleted or silently rewritten.

## Related decisions

- `research/DECISIONS.md`, **2026-08-20: Adopt current computational-verification semantics for legacy work**.
- `research/DECISIONS.md`, **2026-08-20: Use a minimal exact graded kernel for the migration obligations**.
- `research/DECISIONS.md`, **2026-08-21: Treat the interrupted C016 audit as no evidence and stop at the missing bulk canonical system**.
- `research/DECISIONS.md`, **2026-08-21: Verify C016 and replace its shell shortcut with O006**.
- Earlier scope and category choices remain recorded in the 2026-08-19 entries;
  the migration does not rewrite them.
