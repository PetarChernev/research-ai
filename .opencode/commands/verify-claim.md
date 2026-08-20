---
description: Independently attack a CNNN claim, save a verification report, and update its ledger status only as supported by the report.
agent: research-director
---

Verify the claim ID supplied here:

<claim-id>
$ARGUMENTS
</claim-id>

Require exactly one existing `CNNN` ID. Then:

1. Read the exact ledger entry and all linked derivation, experiment, literature, dependency, conflict, and prior verification artifacts. Do not give the verifier an approving summary.
2. Determine every known model that materially produced the claim or its primary evidence by combining `provider_id` and `model_id` from relevant entries in `research/provenance.jsonl`. Do not count a ledger-only integration edit as substantive authorship.
3. Exclude a verifier when its exact configured model appears among the originating models. Of the remaining candidates, prefer a provider absent from the originating set: normally `verifier-anthropic` for OpenAI work or `verifier-openai` for Anthropic work. For mixed or other-provider work, choose the least-overlapping candidate. If provenance is unknown or both verifier models contributed, use the least-overlapping verifier but require that limitation in the report and do not treat the attempt as model-independent.
4. Give the verifier the frozen claim text, assumptions, regime, primary artifact paths, full originating `provider/model` IDs, and a request for a uniquely named new report under `research/results/verification/`. Require the actual verifier agent and model, source artifacts, an explicit independence statement, and serious falsification attempts.
5. The verifier must reconstruct as much as practical and use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`.
6. Inspect the completed report. Use `update-claim-ledger` to link it and record the actual check outcome. Set ledger status `verified` only for a different-model, genuinely independent `verified` report; different-model review alone is insufficient, and shared code or assumptions must remain visible.
7. For failure or contradiction, preserve the report, update conflicts/status as warranted, and add follow-up tasks. Do not delete the originating evidence.
8. Update `research/STATE.md` and any consequential `research/DECISIONS.md` entry.
9. Run `research_validate_state` and fix structural errors.

Report the verification outcome, independence limitations, failed attacks, ledger transition, report path, and required follow-up.
