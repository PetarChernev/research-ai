---
exploration_kind: literature-discovery
status: candidate-leads
question: "Variational calculi for moving internal boundaries, changing strata, corners, and mixed-dimensional actions relevant to exact 4<->5 transitions"
wave: "CY008"
lens: "moving strata, incidence variation, and corner balance"
explorer: literature-explorer
explorer_model: openai/gpt-5.6-sol
created_at: "2026-08-23"
---

# Literature exploration: moving strata, incidence variation, and corner balance

## 1. Bounded question, distinct lens, and evidence status

**Discovery-only; non-evidentiary.** This report asks how one varies (i) the
location/embedding of an internal locus, (ii) its normal or reduction data,
(iii) incidence with lower strata and corners, and (iv) an action whose summands
have different dimensions. It is downstream of the fixed-interface
normal/reduction-field discriminator in D023/CY007 and does **not** assume that
moving `Sigma` repairs the fixed-interface polarization obstruction.

This lens seeks the calculus that makes displacement and corner equations well
defined, not a particular reduction field or edge classification. Ordinary
shells, probe branes, and fixed-boundary corners are controls. No direct source
for true `4/5` stratified incidence was found.

Fingerprints were the polydegree action `int_X5 L5 + int_X4 L4 + int_Sigma L3`,
maps `(j_+,p,j_-)`, rank-three pullback, `SO(1,4)->SO(1,3)` reduction field,
marked boundary circle, displacement variation, and corner moment maps.

## 2. Terminology/framework map and search trail

| Project phrase | Search vocabulary/pivot |
|---|---|
| moving transition locus | hypersurface position variation; embedding field; shape derivative; Hadamard/Reynolds transport; transversality condition |
| normal/reduction field | normal bundle connection; normal-plane frame; Gauss-Weingarten deformation; coset/reduction field; surface symmetry |
| transition equation | displacement operator; shape equation; configurational force; brane force balance; junction condition |
| corners/changing incidence | joint/crease term; edge action; boundary of a brane; BV-BFV higher-codimension stratum |
| mixed-dimensional action | polydegree action; relative/mapping-cone complex; current/chain boundary; defect/brane complex; stratified field theory |
| two-sided covariance | doubly covariant hypersurface action; independent embeddings from each side |

Searches used arXiv abstracts/pages and project artifacts: `moving hypersurface
position variation gravity action`, `doubly covariant singular hypersurface`,
`embedding fields covariant phase space`, `boundary corner tetrad gravity`,
`displacement operator defect Ward identity`, `surface action edges`, `brane
junction force balance`, `BV-BFV corners`, `transgression two connections`,
`Hadamard shape calculus`, `relative de Rham mapping cone`, and
`mixed-dimensional variational forms`. Pivots: position -> displacement
operator; normal -> normal bundle/surface symmetry; junction -> chain
boundary/BFV. Stopped at ten families after a second pass found no new category.

## 3. Source families (all are candidate leads)

“Direct” below means direct to one subproblem, never direct to exact dimension
change. Inspection was limited to the cited arXiv abstract/metadata unless
stated otherwise.

| # | Family and stable locator | Relevance / class | What was inspected; strongest mismatch |
|---|---|---|---|
| 1 | Mukohyama, *Doubly covariant action principle...*, [gr-qc/0108048](https://arxiv.org/abs/gr-qc/0108048), DOI `10.1103/PhysRevD.65.024028` | **Direct for two-sided position variation; convention-dependent.** Independently varies side-measured positions. | Abstract/metadata. Ordinary equal-dimensional hypersurface with nondegenerate induced metric.
| 2 | Capovilla & Guven, *Geometry of Deformations...*, [gr-qc/9411060](https://arxiv.org/abs/gr-qc/9411060), DOI `10.1103/PhysRevD.51.6736`; Carter, *Essentials...*, [gr-qc/0012036](https://arxiv.org/abs/gr-qc/0012036) | **Method transfer.** Covariant normal deformation and shape equations. | Abstracts. Branes inhabit a fixed smooth ambient spacetime.
| 3 | Armas & Tarrio, *On actions for surfaces and DCFTs*, [1709.06766](https://arxiv.org/abs/1709.06766), DOI `10.1007/JHEP04(2018)100`; Billò et al., [1601.02883](https://arxiv.org/abs/1601.02883) | **Direct for displacement/edge Ward identities; method transfer.** | Abstracts. Displacement is broken transverse translation in fixed dimension, not loss of a tangent direction.
| 4 | Ciambelli-Leigh-Pai, *Embeddings and Integrable Charges...*, [2111.13181](https://arxiv.org/abs/2111.13181), DOI `10.1103/PhysRevLett.128.171302`; Speranza [1706.05061](https://arxiv.org/abs/1706.05061) | **Direct for embedding fields/normal-plane charges; convention-dependent.** | Abstracts. Fixed-codimension subregion; no mixed-degree Stokes map.
| 5 | Jubb et al., *Boundary and Corner Terms...*, [1612.00149](https://arxiv.org/abs/1612.00149), DOI `10.1088/1361-6382/aa6014` | **Direct corner control; regime-limited.** Tetrad treatment of joints/creases. | Abstract/metadata. Piecewise `C2` boundaries with fixed metric pullback, not degenerate incidence.
| 6 | Cattaneo-Mnev-Reshetikhin, *Classical BV theories...*, [1201.0290](https://arxiv.org/abs/1201.0290), DOI `10.1007/s00220-014-2145-3` | **Method transfer.** BV-BFV descent to higher-codimension corner strata. | Abstract/metadata. Fixed manifold-with-corners; no dimension or rank change.
| 7 | Mora et al., *Transgression forms...*, [hep-th/0601081](https://arxiv.org/abs/hep-th/0601081), DOI `10.1088/1126-6708/2006/02/067` | **Convention-dependent/method transfer.** Gauge-invariant two-connection boundary action. | Abstract/metadata. Equal-dimensional AdS Chern-Simons setting; no embedding variation.
| 8 | Hadamard-Zolésio shape calculus (search lead; no primary selected) | **Method transfer.** Pull back moving integrals; normal velocity pairs with shape gradient. | No source inspected. Smooth domains; connections, corners, and degeneracy require derivation.
| 9 | Ambrosio & Kirchheim, *Currents in metric spaces*, DOI [`10.1007/s000390050117`](https://doi.org/10.1007/s000390050117) | **Loose/method transfer.** Currents, pushforward, and boundary operator for `T5+T4+T3`. | Metadata only. No gravitational variation or incidence dynamics.
| 10 | Israel/thin-shell and brane-junction family, represented by #1-2 | **Equal-dimensional control only.** Traction/jump and force-balance templates. | Abstract level. Presupposes common metric and comparable extrinsic curvatures.

## 4. Candidate dictionary to project data

| Project datum | Candidate source object | Qualification |
|---|---|---|
| `Sigma` plus one-sided resolutions | abstract parameter manifold `S` with embeddings `X_+:S x S1 -> closure(X5)` and `X_-:S -> closure(X4)` | Unlike an ordinary shell, domains and source dimensions differ before `p_!`; the pair should not be collapsed into one embedding prematurely. |
| incidence maps `(j_+,p,j_-)` | a diagram of embeddings/submersions, or a chain/current boundary map | The object to vary may be the whole diagram, including `p`, not merely the image of `Sigma`. |
| displacement variation | normal part of `delta X`; shape derivative; defect displacement operator | Tangential `delta X` is usually reparametrization, but only after proving the enriched incidence action has that gauge symmetry. |
| normal/reduction field | normal-frame/normal-bundle variable or coset section reducing `SO(1,4)` to `SO(1,3)` | Its material variation must include the change induced by `delta X` plus an independent internal rotation; fixing it would repeat D023's external-reference problem. |
| marked boundary circle `(Y=Sigma x S1, eta,p_!)` | fibered boundary current carried along by `X_+` | Variation must state whether period, connection, projection, and fiber orientation move; ordinary shape calculus varies none of these automatically. |
| polydegree action | pairing of Lagrangians with separate currents `T5,T4,T3`, with incidence encoded by `boundary T` or a mapping-cone differential | This is a proposed organizational method, not an established equivalence. Relative couplings and degree shifts remain physical data. |
| transition-displacement equation | coefficient of normal `delta X` after bulk equations: generalized traction/configurational-force balance plus surface Euler term | It cannot be assumed to be `[K-Kh]=surface stress`; a current pushforward or reduction-field momentum may replace the absent common extrinsic curvature. |
| corner balance | endpoint term from integrating displacement/reduction variation by parts; BFV descent or corner moment map | Candidate terms must include intersections of `partial Sigma` with `Y` and edge-frame charges already exposed in D023. |

## 5. Mismatches and assumptions that fail under dimension change

1. **No common first fundamental form:** Israel and standard brane formulae
compare tensors on one nondegenerate hypersurface. Here `j_+^*E` has a collapsed
leg and only becomes comparable after a noncanonical `p_!`/reduction.
2. **No shared unit normal:** normal normalization uses an inverse metric. At
rank loss, a coframe-built reduction field must replace it; its transformation
under displacement is an equation, not notation.
3. **Two embeddings are not enough:** Mukohyama's independent side positions
still map equal-dimensional copies of one hypersurface. The project additionally
varies a fiber projection/incidence diagram with unequal source dimensions.
4. **Transport theorem degree mismatch:** ordinary Reynolds/Hadamard variation
maps a top form to a boundary form one degree lower in the same dimension. It
does not turn a five-dimensional boundary four-form into the exterior
three-form without `p_!`, a scale, and boundary-circle data.
5. **Tangential displacement may be physical:** reparametrization is gauge only
if it also acts consistently on `p`, `eta`, the reduction field, and currents.
6. **Distributional shell calculus can be undefined:** delta functions and
extrinsic curvature normally rely on a common ambient measure and invertible
metric. Degenerate pullback blocks an automatic distributional Israel limit.
7. **Corner angle/boost formulae can fail:** their normals and dihedral angle may
be undefined when one side loses a tangent direction; a group-valued
normal-frame holonomy is a safer candidate variable, but D023 shows it may be
fixed or charged.

Cheapest reality test: on the planar finite-slope control, introduce abstract
embeddings `X_+,X_-`, projection `p`, and a dynamical reduction field; compute
the first variation only under compactly supported normal displacement. Check
whether all terms descend to one three-form on `Sigma`, whether tangential
displacements are Noether-null, and whether the fixed-interface `43` equation
is recovered at zero displacement. Failure of any one test rejects the proposed
dictionary before a full theory is built.

## 6. Negative results and uncertainties

- No inspected source treated a genuinely intrinsic transition between open
  strata of different dimensions. All gravity/brane leads use a smooth ambient
  manifold of fixed dimension.
- No direct replacement for Israel matching under a degenerate pullback was
  found. Search hits for `junction conditions` overwhelmingly concern
  equal-dimensional sides, branes in bulk, higher-curvature gravity, or
  signature change.
- `Mixed-dimensional variational calculus` mostly returned numerical rod or
  elasticity formulations, not incidence-changing field theory.
- `Brane complex` was terminologically noisy (topological field theory,
  black-hole entropy, or unrelated strings) and did not yield a classical
  moving-junction calculus.
- The current/chain and shape-calculus families remain under-inspected. They are
  methodological leads only; no claim about their precise hypotheses is made.
- The wrong arXiv trail `hep-th/0603091` was checked and is unrelated
  (Lorentz-violating particle phases); do not repeat it as a transgression lead.

## 7. Ranked handoffs

1. **Mukohyama double covariance + current-valued incidence — both
   `literature` and `theorist`.** Literature: extract the exact independent
   embedding variables, displacement Euler equation, boundary terms, and
   assumptions behind the common induced metric in `gr-qc/0108048`. Theorist:
   replace its common hypersurface by the diagram
   `S x S1 -> S -> X4` / `S x S1 -> X5`; determine whether a covariant
   three-form displacement equation exists without dividing by the collapsed
   coframe.
2. **Armas-Tarrio/Carter deformation calculus with edges — both.** Literature:
   extract the variation rules for projectors, normals, normal connection,
   embedding, and edge terms, including the displacement Ward identity.
   Theorist: test whether a dynamical `SO(1,4)/SO(1,3)` reduction field can play
   the role of normal data and whether its shape variation reproduces the
   zero-displacement D023 companion equations rather than fixing holonomy.
3. **Embedding-field covariant phase space + BV-BFV corner descent — both.**
   Literature: establish the exact corner symplectic potential/charge and the
   hypotheses for higher-codimension BFV descent in `2111.13181`, `1706.05061`,
   and `1201.0290`. Theorist: decide whether a polydegree current complex can
   support one nilpotent incidence differential and a conserved total
   presymplectic current for `5/4/3` strata. Reject if it merely repackages
   separate fixed-dimensional boundary systems.

## Epistemic status

All connections are candidate leads. Only abstracts, metadata, and search
results were inspected; no source statement has been validated against primary
text, and families 8-9 are especially preliminary. Exact correspondence to the
project is unproved. Nothing here is literature-supported evidence or may enter
the claim ledger without focused source notes and/or an auditable derivation.
