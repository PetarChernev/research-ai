---
description: With explicit user approval, route one mature critical CNNN claim to the sole Opus 5 independent verifier.
agent: research-director
---

Verify the claim ID supplied here:

<claim-id>
$ARGUMENTS
</claim-id>

Require exactly one existing `CNNN` ID. Direct invocation of this command is
explicit user approval for one bounded Opus audit. It is not approval for full
reproduction or an independent implementation. Then:

1. Read the exact ledger entry, relevant `research/STATE.md` nomination, linked evidence, dependencies, conflicts, internal critiques, and prior verification reports. Identify the single load-bearing inference whose failure would change the conclusion. Do not recursively read every dependency without a concrete reason.
2. Apply the readiness gate. The claim must be narrow, mature, and `importance: critical`, or have an explicit user-approved exception recorded in `research/DECISIONS.md`. Applicable dimensional, limiting-case, and computational checks must be `passed` or justified `not-applicable`; every active required obligation must pass; material dependencies must be settled; and at least one fresh GPT internal critique must have attacked the primary result. If the gate fails, do not invoke Opus. Report the missing item and recommend convergence work instead.
3. Determine every model that materially produced the claim or primary evidence by combining artifact metadata with relevant `provider_id` and `model_id` records from `research/provenance.jsonl`. Include Scientific Computation and every Engineer that produced an environment, lock, reusable kernel, or infrastructure test used by the claim. Deterministic execution does not erase implementation authorship.
4. Confirm that `anthropic/claude-opus-5` is absent from all originating models and that provenance is complete enough for a model-separated judgment. If Opus contributed materially or provenance is unknown, stop and keep the claim below `verified`.
5. Use `update-claim-ledger` to set `checks.independent_verification: pending` only now that the user has approved a ready claim. Record the load-bearing and error-risk rationale in `research/DECISIONS.md`.
6. Assemble a minimal packet as paths: the frozen claim and assumptions; one primary derivation or evidence artifact; relevant internal critiques; the load-bearing `ONNN` spec, result, and claim-specific entrypoint when applicable; directly relevant failed or superseded obligations; and concise representation, contract, environment, infrastructure, fingerprint, and provenance records. Give broader paths only as escalation references.
7. Delegate only to `verifier-anthropic`. State explicitly that the user approved the audit. Supply the full originating model IDs, exact decisive inference, source paths, and a unique destination under `research/results/verification/`. Do not give an approving summary.
8. Impose the bounded audit: no code, scratch implementation, obligation reruns, repository validation, or web research; no more than twelve investigative tool calls; one compact alternate reconstruction; at most three serious falsification attacks; one report of at most 2,500 words; then stop. Allowed outcomes are `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`.
9. Inspect the report and update the ledger conservatively. Set `checks.independent_verification: passed` and ledger status `verified` only for a substantive Opus report with outcome `verified`, complete originating models, genuine alternate reasoning or a comparably strong attack, and no unresolved failed report. Set failed or inconclusive check state from the actual outcome otherwise.
10. Preserve every negative report and failing obligation. A recommendation for another obligation, full reproduction, or independent implementation is unsatisfied future work; the latter two require separate explicit approval.
11. Update `research/STATE.md`, `research/COMPUTATION.md` when strategy changed, and `research/DECISIONS.md`. Run `research_validate_state` and fix structural errors.

Report the Opus outcome, independence limitations including computational
dependence, failed attacks, untested failure modes, ledger transition, report
path, and required follow-up.
