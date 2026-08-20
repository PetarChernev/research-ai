---
claim_id: "{{CLAIM_ID}}"
outcome: "{{OUTCOME}}"
date: "{{DATE}}"
verifier: "{{VERIFIER}}"
verifier_model: "{{VERIFIER_MODEL}}"
originating_models: {{ORIGINATING_MODELS_JSON}}
source_artifacts: {{SOURCE_ARTIFACTS_JSON}}
---

# Verification report for {{CLAIM_ID}}

## Claim tested

Quote the exact ledger claim and status at the start of verification.

## Independence statement

State the originating and verifier `provider/model` IDs, including every Scientific Computation and Engineer model that materially produced the environment or reusable infrastructure. Identify which reasoning, code, data, environments, and assumptions were reconstructed independently and which were shared.

## Reconstruction

Re-derive or reproduce the claim from primary artifacts rather than an approving summary.

## Falsification attempts

Record attempted counterexamples, extreme regimes, alternative interpretations, and literature conflicts.

## Checks

- Dimensions and units:
- Signs and normalization:
- Symmetries and conservation laws:
- Limiting or exactly soluble cases:
- Computational reproducibility and convergence:
- Hidden parameter dependence:

## Computational evidence reviewed

List the relevant `ONNN` obligations with, for each: the declared question, the
method and representation, the assumptions the implementation encodes, the
predeclared acceptance criterion, the entrypoint inspected, and the outcome
actually recorded by the deterministic runner. Include failed, inconclusive,
superseded, and never-run obligations. State plainly when the claim has no
applicable machine-checkable component and where the computational plan records
that judgment. For load-bearing computations, also list the computational
contract, research-environment manifests and locks, dependency provenance,
Engineer-authored reusable source and infrastructure tests, Scientific
Computation's research-specific validation, and recorded infrastructure
fingerprints.

## Sufficiency of computational obligations

Explain whether the declared checks actually address the claim, or only a
narrower statement. Assess whether the assumptions encoded in computation match
the claim's stated assumptions and regime, whether the representation is
faithful to the mathematics, whether normal forms and equality semantics are
valid under the declared domain, whether dependencies or APIs add hidden
assumptions, whether infrastructure tests cover the required primitives and
invalid inputs, and whether the acceptance criteria are
scientifically adequate rather than merely satisfiable. A passing computation is
not by itself verification of the scientific claim.

## Missing or adversarial checks

Identify checks that could expose plausible failure modes and are currently
absent: untested limits, sign or convention variants, counterexample searches,
domains the criterion avoids, or a perturbed input the implementation should
reject but may not. Recommend them; do not author canonical machine outcomes.

## Computational independence

State which implementations, algorithms, libraries, representations,
assumptions, data, research environments, Engineer-authored infrastructure,
Scientific Computation validation, and code paths are shared with the
originating work, and which are genuinely independent. Deterministic execution
does not make either the scientific design or the engineering implementation
independent of their producing models. Describe any computation you performed
yourself and what it shares with the original.

## Findings

List failures and residual uncertainty before supportive observations.

## Outcome

Use exactly one: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. Explain the evidentiary threshold applied.

## Required follow-up

State what would resolve each remaining issue. Failed verification remains a durable result.
