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

State the originating and verifier `provider/model` IDs, including every Scientific Computation and Engineer model that materially produced the load-bearing environment or reusable infrastructure. Identify which reasoning, code, data, environments, and assumptions were independently attacked and which were shared.

## Scope and decisive bridge

Name the single load-bearing inference selected for review, why its failure would change the claim, the packet inspected, and what was deliberately left outside this bounded audit.

## Reconstruction

Give one compact alternate reconstruction of the decisive bridge from primary artifacts. Do not reproduce the whole derivation or computation.

## Falsification attempts

Record no more than three serious attacks selected for their ability to change the conclusion. Failed attacks are useful evidence; checklist completion is not the goal.

## Checks

- Dimensions and units:
- Signs and normalization:
- Symmetries and conservation laws:
- Limiting or exactly soluble cases:
- Computational representation or convergence:
- Hidden parameter dependence:

## Computational evidence reviewed

Summarize only the load-bearing `ONNN` obligations: declared question, encoded
assumptions, acceptance criterion, implementation path inspected, and recorded
outcome. Include a failed or superseded obligation only when it changes the
claim's interpretation. State plainly when no machine-checkable component
applies. Cite the relevant contract, environment, provenance, infrastructure
tests, and fingerprints without exhaustively inventorying them.

## Sufficiency of computational obligations

Explain whether the declared checks address the decisive bridge or only a
narrower statement. Assess the highest-risk mismatch among assumptions,
representation, conventions, equality semantics, dependencies, primitive
tests, and acceptance criteria. Do not exhaustively audit low-risk machinery.
A passing computation is not by itself verification of the scientific claim.

## Missing or adversarial checks

Identify at most one missing check that could expose the most plausible
remaining decisive failure mode. Recommend it; do not implement it or author a
canonical machine outcome.

## Computational independence

State which load-bearing implementations, representations, assumptions, data,
environments, and infrastructure are shared, and what the focused alternate
argument independently checks. Deterministic execution does not make the
scientific design or implementation independent of its producing models. The
ordinary verifier does not write a second implementation.

## Findings

List failures and residual uncertainty before supportive observations.

## Outcome

Use exactly one: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. Explain the evidentiary threshold applied.

## Required follow-up

State the single highest-value action that would resolve the principal remaining issue. Failed verification remains a durable result.

Keep the complete report at or below 2,500 words.
