# W002-dimension-routes — frozen exploration packet

Date: 2026-09-09. Director: `openai/gpt-6-astra`. Width: **8**.
Status: closed on 2026-09-09 after complete first-pass and internal-critique
barriers, synthesis and pruning. Objective/matrix were frozen before allocation.
No missing or failed branch was replaced. Synthesis:
`research/results/W002-dimension-routes-synthesis.md`.

## Objective

Map materially different realizations of dynamical dimensionality before
selecting another baseline theory. For each constructive route, ask whether an
extra-direction region can be selected by autonomous dynamics and whether an
energy or probe response is calculable. A bounded toy success is useful; it
must not be relabelled an exact intrinsic gravitational success.

## Frozen common assumptions and scope

1. Natural units `c=hbar=1`; one persistent timelike direction. Use signature
   `(-,+,+,+)` when a continuum base is used. State other conventions and all
   parameter dimensions. Use `d` for total spacetime dimension and explicitly
   label spatial or spectral dimension differently.
2. Compare a `3+1` exterior and an extra **spacelike** direction in a localized
   region. Lower-dimensional analogues and planar walls are legitimate cheap
   diagnostics but are not finite-energy three-space particles.
3. Strong target: no physical exterior fifth direction and exact intrinsic
   `d=4/5` open regions. This is a target to score, not a shared axiom that
   forecloses emergent, discrete, finite-tower, or fixed-bulk models. Every route
   lists which demands it relaxes.
4. A spatial profile, interface position, or dimension label inserted as a
   spacetime-dependent coupling is not dynamical. Specify varied variables and
   an action, Hamiltonian, or autonomous transition law. Choosing initial data
   or a charge sector is allowed; distinguish motion of an initial region from
   spontaneous formation and from stable equilibrium.
5. At least one concrete, hand-derived witness: energy/force, dispersion,
   transmission, density of states, or a sharply scoped obstruction. It must
   expose a calculable observable, not just an analogy or model name.
6. Do not require GR, full covariance, quantum unitarity, or stability to be
   solved this wave; list their absence as costs. No Hopf, fermion, or electron
   fitting. Do not add infrastructure or run code during the theory first pass.
7. No broad web searches, priority claims, or source laundering. Unchecked
   literature associations are leads for a later `/literature-explore` or
   focused literature task, not evidence. This is a theory wave.
8. First-pass barrier: each worker reads only this packet, its own scaffold,
   QUESTION, and the specifically assigned historical context. Do **not** read
   sibling outputs. All sibling and critic GPT agreement is correlated.

## Existing route: warning packet, not universal assumptions

The prior F0 program fixed a circle-collapse quotient, resolution regularity,
first-order Palatini actions, and interface data. C021-C024 exclude smooth-flat
diagonal benchmark backgrounds or bounded curvature in their stated regimes.
C025-C028 exclude specified finite-slope action repairs with free mixed traces.
C029 concerns only boundary-trace descent, not a complete collar theory.
None proves impossibility of dynamical dimension in general. Do not repeat the
counterterm sequence or presume its state-space category is physically unique.

Useful primary context (only assigned branches need read it):
- `research/derivations/D001.md`: canonical information/charge diagnostic;
  gauged benign controls prevent a rank-change-alone no-go.
- `research/derivations/D021.md`: zero-value/zero-slope positive circle radius
  has unbounded radial-circle curvature; hypothesis-relative, not universal.
- `research/derivations/D026.md`: tangential trace category does not define the
  singular collar or full field object.
- C001-C006 remain conjectural strong program targets. C016's prior independent
  audit is only an isolated interface result and supplies no evidence here.

## Branch matrix (all eight must launch as siblings)

| Slot | Route | Material distinction | Required cheap bridge |
|---|---|---|---|
| A | Intrinsic mixed-dimensional free boundary | Geometry/domain is varied; exact extra fiber exists only over a dynamical region; no exterior ambient fiber | Moving-domain action and shape/energy balance; identify field-transfer/endpoint gap |
| B | Radion/compactification phase bubbles | Fixed higher-dimensional topology; radius is a positive dynamical scalar; dimension changes only by accessibility | Scalar/radion dynamics, finite-domain energy and KK probe threshold; test exact-zero limit |
| C | Dynamical localization or confinement | Dimension available to matter changes through a trapping/confining medium, not a shrinking geometric radius | Autonomous trap/order parameter and local transverse spectrum or escape observable |
| D | Deconstruction with dynamical links | Fixed finite internal sites with varied links; extra dimension emerges from propagation along a chain | Link equation and probe mass/dispersion spectrum; account for exterior site multiplicity |
| E | Variable-incidence cell complexes | Physical spatial complex itself can gain/lose higher-dimensional cells; discrete non-manifold ontology | Legal autonomous local move, energy accounting, and dimension/probe diagnostic; no labels posing as geometry |
| F | Matrix/operator emergent geometry | Adjacency/distance arises from dynamical noncommuting operators rather than a background manifold or fixed chain | Minimal matrix Hamiltonian and probe Laplacian spectral witness; locality and finite-N limit costs |
| G | Rank-changing propagation tensor | Fixed continuum labels but a varied kinetic/principal tensor opens/closes a direction; not geometric radius or trapping | Complete simple action, characteristic/energy witness, hidden exterior data and strong-coupling test |
| H | Adversarial definition and predictivity audit | Try to falsify the common intuition and identify minimal compatible requirement sets, not a constructive vote | At most three scoped obstructions/countercontrols: state information, probe universality, compact support |

## Allocated paths and first-pass barrier record

All destinations were allocated in one `research_new_derivations` call before
the single eight-sibling task batch. Each worker reports `openai/gpt-6-astra`.

| Slot | Frozen first pass | Assigned fresh critique |
|---|---|---|
| A | `research/derivations/D027.md` | `research/critiques/D027-2026-09-09-openai-01.md` |
| B | `research/derivations/D028.md` | `research/critiques/D028-2026-09-09-openai-01.md` |
| C | `research/derivations/D029.md` | `research/critiques/D029-2026-09-09-openai-01.md` |
| D | `research/derivations/D030.md` | `research/critiques/D030-2026-09-09-openai-01.md` |
| E | `research/derivations/D031.md` | `research/critiques/D031-2026-09-09-openai-01.md` |
| F | `research/derivations/D032.md` | `research/critiques/D032-2026-09-09-openai-01.md` |
| G | `research/derivations/D033.md` | `research/critiques/D033-2026-09-09-openai-01.md` |
| H | `research/derivations/D034.md` | `research/critiques/D034-2026-09-09-openai-01.md` |

All eight delivered explicit analytic witnesses and disclosed scope gaps. No
theory worker reports a scientific computation, literature search, or sibling
inspection. D027 and D031 additionally invoked repository validation despite
the no-execution charter; these are administrative validator calls, not machine
evidence, and their inherited/scaffold failures will be assessed by the director.

## Required first-pass artifact structure and stopping condition

Preserve scaffold metadata and required headings; use a concise route card,
roughly 1,200-2,000 words (hard ceiling 2,500). Include:
- definition of dimension and physical ontology;
- minimal variables, autonomous dynamics, explicit relaxed assumptions;
- one load-bearing hand calculation with energy/probe or obstruction;
- what makes the region dynamical, and which of formation/motion/stability is
  actually obtained;
- dimensional/sign/limiting checks and sharp failure modes;
- staged applicability roadmap, smallest decisive next assertion, and whether
  a cheap executable test would genuinely discriminate;
- epistemic labels, source/dependency limits, and actual `provider/model` ID.

Stop after one concrete witness and route triage. An unresolved gap is a valid
deliverable. Do not fill it with successive action repairs. Do not create
claims, hypotheses, checks, experiments, code, or sibling edits. No delegation.
The director owns integration, methodological choices, and the next decision.

## Critique and synthesis protocol

Wait for all eight first passes, preserve missing/failed perspectives, then
freeze each substantive artifact and send it to one fresh GPT internal critic
with a unique path. Each critic reconstructs one decisive inference, makes at
most three attacks, uses the four allowed internal outcomes, and stops. No
Opus request, pending audit, or independent-verification promotion.

Rank routes by explanatory reach, honesty/consistency, observable access,
falsifiability, and cost of the next discriminator, not by votes. Only allocate
cheap machine obligations after critique if an assertion can actually change
the shortlist. No large software investment before a route survives critique.
