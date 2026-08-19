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
- independent reproduction check for `reproduced`;
- passed independent report for `verified`.

Multiple weak or dependent items do not combine automatically into verification.

## 4. Link provenance

Use stable IDs for hypotheses, derivations, experiments, dependencies, and conflicts. Use repository-relative paths for literature notes and verification reports. Record material assumptions explicitly. Keep failed and contradictory evidence linked.

## 5. Apply verification guardrails

Set `verified` only when `checks.independent_verification` is `passed` and `evidence.verification` links a report documenting genuine independence and serious falsification attempts. A supportive report with shared code must not be promoted silently.

## 6. Preserve material history

Change `updated_at` whenever wording, status, assumptions, evidence, dependencies, conflicts, or checks change. Record consequential reinterpretations in `research/DECISIONS.md`. Do not delete a contradicted or rejected claim merely to simplify the story.

## 7. Synchronize state and validate

Update `research/STATE.md` when the change affects the working picture or next actions. Run:

```bash
uv run --locked python scripts/validate_research_state.py
```

Fix structural errors. Report warnings or unresolved scientific conflicts rather than suppressing them.
