---
description: Independently attack a CNNN claim, save a verification report, and update its ledger status only as supported by the report.
agent: research-director
---

Verify the claim ID supplied here:

<claim-id>
$ARGUMENTS
</claim-id>

Require exactly one existing `CNNN` ID. Then:

1. Read the exact ledger entry and all linked derivation, experiment, literature, machine-check, dependency, conflict, and prior verification artifacts. Do not give the verifier an approving summary.
2. Determine every known model that materially produced the claim or its primary evidence by combining `provider_id` and `model_id` from relevant entries in `research/provenance.jsonl`. Do not count a ledger-only integration edit as substantive authorship.
3. Exclude a verifier when its exact configured model appears among the originating models. Of the remaining candidates, prefer a provider absent from the originating set: normally `verifier-anthropic` for OpenAI work or `verifier-openai` for Anthropic work. For mixed or other-provider work, choose the least-overlapping candidate. If provenance is unknown or both verifier models contributed, use the least-overlapping verifier but require that limitation in the report and do not treat the attempt as model-independent.
4. Assemble the computational evidence packet. Give the verifier, as files rather than as a summary:
   - `research/COMPUTATION.md`, so the declared strategy and its stated gaps are inspectable;
   - every active `ONNN` specification targeting the claim, plus superseded ones that carry relevant history;
   - the obligation implementations, not only their specs;
   - the machine-generated `result.json` for each, including failed, inconclusive, and error outcomes;
   - the `research/computation/` infrastructure those results depend on;
   - the relevant experiment artifacts.

   State explicitly when the claim has no applicable machine-checkable component, and point at where `research/COMPUTATION.md` records that judgment. Absence of checks is a reviewable position, not a silent omission.
5. Give the verifier the frozen claim text, assumptions, regime, primary artifact paths, full originating `provider/model` IDs, and a request for a uniquely named new report under `research/results/verification/`. Require the actual verifier agent and model, source artifacts, an explicit independence statement, and serious falsification attempts.
6. Require the verifier to assess sufficiency, not merely whether checks passed: whether the declared obligations actually test the claim, whether important failure modes are untested, whether the assumptions encoded in computation match the claim's assumptions, whether the representation is faithful, whether the acceptance criteria are scientifically adequate, whether shared implementations or infrastructure undermine independence, whether an alternate method or implementation is warranted, and whether apparently strong machine evidence establishes only a narrower statement.
7. The verifier must reconstruct as much as practical and use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. It may recommend additional obligations; it must not author canonical machine-result outcomes. Any computation it performs itself is described in its report, not written into `research/checks/**/result.json`.
8. Inspect the completed report. Use `update-claim-ledger` to link it and record the actual check outcomes. Set ledger status `verified` only for a different-model, genuinely independent `verified` report; different-model review alone is insufficient, a green computational gate is insufficient, and shared code or assumptions must remain visible. A claim with no applicable machine checks may still be verified with `checks.computational_verification: not-applicable`.
9. If the verifier recommends further obligations, create them with `/new-check` rather than treating the recommendation as satisfied.
10. For failure or contradiction, preserve the report, the failing obligations, and their results; update conflicts/status as warranted, and add follow-up tasks. Do not delete the originating evidence.
11. Update `research/STATE.md`, `research/COMPUTATION.md` if the review changed the declared strategy, and any consequential `research/DECISIONS.md` entry.
12. Run `research_validate_state` and fix structural errors.

Report the verification outcome, independence limitations including computational dependence, failed attacks, untested failure modes, ledger transition, report path, and required follow-up.
