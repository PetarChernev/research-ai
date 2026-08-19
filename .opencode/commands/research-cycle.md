---
description: Execute one bounded, high-information research iteration and integrate its artifacts, claims, verification needs, and next action.
agent: research-director
---

Run exactly one bounded research iteration. Optional focus supplied by the user:

<focus>
$ARGUMENTS
</focus>

1. Read `research/QUESTION.md`, `research/STATE.md`, the full claim ledger, active hypotheses, and linked evidence. Do not rely on conversation memory.
2. Identify the highest-information unresolved issue, respecting the optional focus. State which hypotheses or claims its possible outcomes distinguish.
3. Choose the cheapest adequate analytic, literature, numerical, or reproduction task. Delegate no more than three independent bounded subproblems, normally fewer. Give workers primary artifact paths, deliverables, and stopping conditions; prohibit recursive delegation.
4. Require workers to save important outputs in the appropriate literature-note, derivation, experiment, or verification artifact. A chat summary alone is not evidence.
5. Integrate the evidence using `research-synthesis`. Preserve conflicting regimes, failed checks, shared dependencies, and uncertainty.
6. If an important new claim is conclusion-critical, invoke `verifier` with the exact claim and primary artifacts. Do not use the originating agent as its verifier and do not call supportive repetition independent.
7. Update `research/claims/ledger.yaml`, `research/STATE.md`, and `research/DECISIONS.md` only to the extent warranted by actual evidence. Never silently promote status.
8. Run `research_validate_state` and fix structural errors.

Stop after this iteration. Report what changed, what remains unresolved, any failed falsification attempts, and the next single best action. Do not automatically launch another cycle.
