---
description: Execute one bounded, high-information research iteration and integrate its artifacts, claims, verification needs, and next action.
agent: research-director
---

Run exactly one bounded research iteration. Optional focus supplied by the user:

<focus>
$ARGUMENTS
</focus>

1. Read `research/QUESTION.md`, `research/STATE.md`, `research/COMPUTATION.md`, the full claim ledger, active hypotheses, active machine-check obligations under `research/checks/`, and linked evidence. Do not rely on conversation memory.
2. Identify the highest-information unresolved issue, respecting the optional focus. State which hypotheses or claims its possible outcomes distinguish.
3. Decide whether that issue needs analytic, literature, experimental, or machine-check work, and choose the cheapest adequate task. Delegate no more than three independent bounded scientific subproblems, normally fewer. Give workers primary artifact paths, deliverables, and stopping conditions. The only nested task permitted is a bounded `scientific-computation -> engineer` substrate handoff; Engineer cannot delegate and its work does not become another scientific evidence stream.
4. Instantiate an executable obligation when a conclusion-critical mathematical assertion can actually be decided mechanically. Define its question and acceptance criterion first, allocate it with `research_new_check`, and delegate implementation to `scientific-computation`. Do not require new computational work every cycle, and do not turn obligation creation into ceremony for trivial claims or assertions a check cannot discriminate.
5. Require workers to save important outputs in the appropriate literature-note, derivation, experiment, obligation, or verification artifact. A chat summary alone is not evidence, and an obligation without a runner-produced `result.json` has not run.
6. Integrate the evidence using `research-synthesis`. Preserve conflicting regimes, failed and inconclusive obligations, shared dependencies, and uncertainty. Never delete a failed obligation; supersede it and record why.
7. Treat verifier effort as scarce. Most new claims should remain below `verified` until review would change an immediate research decision or unlock a conclusion. Verify at most one claim this cycle, only when it is narrow, gate-critical, and supported enough for a focused audit; do not launch verification merely because a claim is important, newly derived, computationally passed, or itself inconclusive. Otherwise record verification as pending and stop. For a warranted review, select the eligible model-bound verifier, curate only the load-bearing primary artifacts and provenance, and impose this stopping condition: no code, reruns, validator, or web work; no more than twelve investigative tool calls; one compact alternate reconstruction; at most three serious attacks; one report of at most 2,500 words; then stop. Full reproduction requires separate explicit user approval.
8. Update `research/claims/ledger.yaml`, `research/STATE.md`, and `research/DECISIONS.md` only to the extent warranted by actual evidence. Never silently promote status, and set `checks.computational_verification` only from recorded machine results.
9. Update `research/COMPUTATION.md` when representations, methods, evidence standards, infrastructure, independence needs, or the research phase materially changed this cycle. Leave it alone when nothing material changed.
10. Run `research_validate_state` and fix structural errors.

Stop after this iteration. Report what changed, what remains unresolved, any failed falsification attempts or failed obligations, and the next single best action. Do not automatically launch another cycle.
