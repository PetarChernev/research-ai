---
name: update-claim-ledger
description: Use when adding or changing entries in research/claims/ledger.yaml so stable IDs, controlled statuses, evidence links, checks, dependencies, conflicts, timestamps, and verification provenance remain valid.
compatibility: OpenCode 1.18+
metadata:
  domain: research-state
  artifact: claim-ledger
---

# Update the Claim Ledger

## 1. Read before editing

Inspect `research/claims/README.md`, the full ledger entry, linked artifacts, dependencies, conflicts, and current `research/STATE.md`. A claim is one precise, falsifiable, regime-qualified statement, not a paragraph of conclusions.

## 2. Allocate stable identity

For a new claim, choose one greater than the highest existing `CNNN` ID. Never reuse or renumber IDs. Set an ISO-8601 creation timestamp and preserve it on later edits.

## 3. Select status from evidence

Use only the controlled vocabulary. Match evidence category to status:

- derivation artifact for `derived`;
- experiment artifact for `numerically-supported`;
- exact primary-source note for `literature-supported`;
- independent reproduction, as an experiment or a passing obligation, plus
  `checks.computational_verification: passed`, for `reproduced`;
- passed independent report for `verified`.

Multiple weak or dependent items do not combine automatically into verification.

## 4. Link provenance

Use stable IDs for hypotheses, derivations, experiments, machine-check obligations, dependencies, and conflicts. Use repository-relative paths for literature notes and verification reports. Record material assumptions explicitly. Keep failed and contradictory evidence linked.

Ledger schema version 2 carries `evidence.computational_checks` for `ONNN` obligations under `research/checks/`. Links are bidirectional and the validator enforces both directions: a listed obligation must target the claim, and an active obligation targeting the claim must be listed by it.

## 5. Record computational verification honestly

`checks.computational_verification` replaces the older `numerical_reproduction` field, because computation is broader than numerical work. An obligation may be exact-symbolic, formal, numerical, convergence-based, a limiting case, a symmetry or dimensional test, a counterexample search, or an independent implementation.

Set it from recorded machine results, never from expectation. The validator applies a structural gate over the project's own declared strategy:

```text
pending required obligation      -> computational_verification must not be passed
failed required obligation       -> computational_verification must not be passed
inconclusive required obligation -> computational_verification must not be passed
passed required obligation       -> that obligation is satisfied
superseded obligation            -> does not block the current strategy
```

Use `not-applicable`, with the reason recorded in `research/COMPUTATION.md`, when the claim has no meaningful machine-checkable component. That is a legitimate state and does not by itself block verification.

A passing gate means the declared strategy is complete, not that it was scientifically adequate. If an obligation turns out to be misguided, mark its spec `superseded` and record why. Never delete a failed obligation to clear the gate.

## 6. Apply verification guardrails

Set `verified` only when `checks.independent_verification` is `passed`, `checks.dimensional_analysis`, `checks.limiting_cases`, and `checks.computational_verification` are each `passed` or `not-applicable`, every active required obligation targeting the claim has a passing result, and `evidence.verification` links a report documenting known verifier and originating model IDs, no exact-model overlap, genuine methodological independence, and serious falsification attempts. Different-model review is necessary but not sufficient, and neither is a green computational gate. A report with unknown model provenance or materially shared code or implementations must not be promoted silently.

## 7. Preserve material history

Change `updated_at` whenever wording, status, assumptions, evidence, dependencies, conflicts, or checks change. Record consequential reinterpretations in `research/DECISIONS.md`. Do not delete a contradicted or rejected claim, a failed obligation, or a failed verification report merely to simplify the story.

## 8. Synchronize state and validate

Update `research/STATE.md` when the change affects the working picture or next actions, and `research/COMPUTATION.md` when the change alters the declared computational strategy. Run:

```bash
uv run --locked python scripts/validate_research_state.py
```

Fix structural errors. Report warnings or unresolved scientific conflicts rather than suppressing them.
