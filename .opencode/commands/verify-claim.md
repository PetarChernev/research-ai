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
2. Determine every known model that materially produced the claim or its primary evidence by combining `provider_id` and `model_id` from relevant entries in `research/provenance.jsonl`. Include Scientific Computation and every Engineer that materially produced the research environment, dependency lock, reusable kernel, or infrastructure tests. Do not count a ledger-only integration edit as substantive authorship, and do not treat deterministic execution as removing implementation authorship.
3. Exclude a verifier when its exact configured model appears among the originating models. Of the remaining candidates, prefer a provider absent from the originating set: normally `verifier-anthropic` for OpenAI work or `verifier-openai` for Anthropic work. For mixed or other-provider work, choose the least-overlapping candidate. If provenance is unknown or both verifier models contributed, use the least-overlapping verifier but require that limitation in the report and do not treat the attempt as model-independent.
4. Assemble the computational evidence packet. Give the verifier, as files rather than as a summary:
   - `research/COMPUTATION.md`, so the declared strategy and its stated gaps are inspectable;
   - every active `ONNN` specification targeting the claim, plus superseded ones that carry relevant history;
   - the obligation implementations, not only their specs;
   - the machine-generated `result.json` for each, including failed, inconclusive, and error outcomes;
   - the computational contract and trust strategy;
   - the `research/environment/` manifests, locks, smoke tests, and dependency provenance;
   - the Engineer-authored `research/computation/` infrastructure and its software-level tests;
   - Scientific Computation's research-specific validation of the representation;
   - the relevant experiment artifacts.

   State explicitly when the claim has no applicable machine-checkable component, and point at where `research/COMPUTATION.md` records that judgment. Absence of checks is a reviewable position, not a silent omission.
5. Give the verifier the frozen claim text, assumptions, regime, primary artifact paths, full originating `provider/model` IDs, and a request for a uniquely named new report under `research/results/verification/`. Require the actual verifier agent and model, source artifacts, an explicit independence statement, and serious falsification attempts.
6. Require the verifier to assess sufficiency, not merely whether checks passed: whether the declared obligations actually test the claim; whether the representation, normal form, equality semantics, and conventions are faithful; whether dependencies or APIs introduce hidden assumptions; whether infrastructure tests cover primitive laws and unsupported inputs; whether Scientific Computation validated the contract on research-specific cases; whether the acceptance criteria are adequate; whether shared implementations or Engineer/Scientific Computation model provenance undermine independence; whether an alternate method is warranted; and whether apparently strong evidence establishes only a narrower statement.
7. The verifier must reconstruct as much as practical and use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. It may recommend additional obligations; it must not author canonical machine-result outcomes. Any computation it performs itself is described in its report, not written into `research/checks/**/result.json`.
8. Inspect the completed report. Use `update-claim-ledger` to link it and record the actual check outcomes. Set ledger status `verified` only for a different-model, genuinely independent `verified` report; different-model review alone is insufficient, a green computational gate is insufficient, and shared code or assumptions must remain visible. A claim with no applicable machine checks may still be verified with `checks.computational_verification: not-applicable`.
9. If the verifier recommends further obligations, create them with `/new-check` rather than treating the recommendation as satisfied. If it raises an infrastructure concern, route it to Scientific Computation for scientific triage; Scientific Computation provisions Engineer if warranted, validates the change, reruns every affected obligation, and returns the fresh evidence to the verifier. The verifier never provisions Engineer directly.
10. For failure or contradiction, preserve the report, the failing obligations, and their results; update conflicts/status as warranted, and add follow-up tasks. Do not delete the originating evidence.
11. Update `research/STATE.md`, `research/COMPUTATION.md` if the review changed the declared strategy, and any consequential `research/DECISIONS.md` entry.
12. Run `research_validate_state` and fix structural errors.

Report the verification outcome, independence limitations including computational dependence, failed attacks, untested failure modes, ledger transition, report path, and required follow-up.
