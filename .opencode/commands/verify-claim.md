---
description: Independently attack a CNNN claim, save a verification report, and update its ledger status only as supported by the report.
agent: research-director
---

Verify the claim ID supplied here:

<claim-id>
$ARGUMENTS
</claim-id>

Require exactly one existing `CNNN` ID. Then:

1. Read the exact ledger entry and inventory its linked evidence, dependencies, conflicts, and prior reports. Identify the single load-bearing inference whose failure would change the claim. Read the primary artifacts for that inference; do not recursively read every dependency unless a concrete inconsistency requires it.
2. Determine every known model that materially produced the claim or its primary evidence by combining `provider_id` and `model_id` from relevant entries in `research/provenance.jsonl`. Include Scientific Computation and every Engineer that materially produced the research environment, dependency lock, reusable kernel, or infrastructure tests. Do not count a ledger-only integration edit as substantive authorship, and do not treat deterministic execution as removing implementation authorship.
3. Exclude a verifier when its exact configured model appears among the originating models. Of the remaining candidates, prefer a provider absent from the originating set: normally `verifier-anthropic` for OpenAI work or `verifier-openai` for Anthropic work. For mixed or other-provider work, choose the least-overlapping candidate. If provenance is unknown or both verifier models contributed, use the least-overlapping verifier but require that limitation in the report and do not treat the attempt as model-independent.
4. Decide the verification tier before delegation:
   - **bounded audit**, the default: one decisive alternate reconstruction plus at most three attacks;
   - **full reproduction**, exceptional and launched only when the user explicitly approved its additional cost.

   If the claim is too broad for the bounded audit, split it or accept a conservative outcome. Do not silently turn `/verify-claim` into full reproduction.
5. Assemble a minimal computational packet as paths, not an exhaustive reading assignment:
   - the relevant section of `research/COMPUTATION.md`;
   - the load-bearing `ONNN` spec, result, and claim-specific entrypoint;
   - any failed or superseded obligation that directly changes interpretation;
   - concise computational-contract, representation, environment, provenance, and infrastructure-fingerprint records;
   - only the reusable primitive source or tests needed to examine a specific representation risk;
   - the primary experiment artifact when the claim is empirical.

   Give broader environment, infrastructure, and dependency paths as escalation references. Do not require exhaustive inspection of whole directories or unrelated obligations. State explicitly when the claim has no applicable machine-checkable component and where the computational plan records that judgment.
6. Give the verifier the frozen claim text, assumptions, regime, primary artifact paths, full originating `provider/model` IDs, the single load-bearing inference, and a request for one uniquely named report under `research/results/verification/`. Do not give an approving summary.
7. Impose a hard task budget: no code or scratch implementation; no obligation reruns, repository validation, or web research; no more than twelve investigative tool calls; one compact alternate reconstruction; at most three serious falsification attacks; one report of at most 2,500 words; then stop. The verifier must use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. If the packet or budget is insufficient, it must choose a conservative outcome and recommend at most one next action rather than expanding scope.
8. Inspect the completed report. Use `update-claim-ledger` to link it and record the actual check outcomes. Set ledger status `verified` only for a different-model, genuinely independent `verified` report; different-model review alone is insufficient, a green computational gate is insufficient, and shared code or assumptions must remain visible. A claim with no applicable machine checks may still be verified with `checks.computational_verification: not-applicable`.
9. If the verifier recommends a further obligation, create it with `/new-check` rather than treating the recommendation as satisfied. If it recommends full reproduction or independent implementation, obtain explicit user approval before launching the additional work. If it raises an infrastructure concern, route it to Scientific Computation for scientific triage; Scientific Computation provisions Engineer if warranted. The verifier never provisions Engineer directly.
10. For failure or contradiction, preserve the report, the failing obligations, and their results; update conflicts/status as warranted, and add follow-up tasks. Do not delete the originating evidence.
11. Update `research/STATE.md`, `research/COMPUTATION.md` if the review changed the declared strategy, and any consequential `research/DECISIONS.md` entry.
12. Run `research_validate_state` and fix structural errors.

Report the verification outcome, independence limitations including computational dependence, failed attacks, untested failure modes, ledger transition, report path, and required follow-up.
