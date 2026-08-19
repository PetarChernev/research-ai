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
2. Invoke `verifier` with the frozen claim text, assumptions, regime, primary artifact paths, and a request for a uniquely named new report under `research/results/verification/`. Require the actual verifier/method, source artifacts, an explicit independence statement, and serious falsification attempts. A same-model session alone is not independent.
3. The verifier must reconstruct as much as practical and use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`.
4. Inspect the completed report. Use `update-claim-ledger` to link it and record the actual check outcome. Set ledger status `verified` only for a genuinely independent `verified` report; shared code or assumptions must remain visible.
5. For failure or contradiction, preserve the report, update conflicts/status as warranted, and add follow-up tasks. Do not delete the originating evidence.
6. Update `research/STATE.md` and any consequential `research/DECISIONS.md` entry.
7. Run `research_validate_state` and fix structural errors.

Report the verification outcome, independence limitations, failed attacks, ledger transition, report path, and required follow-up.
