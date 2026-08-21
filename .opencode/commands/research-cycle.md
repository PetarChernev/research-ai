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
3. Decide whether that issue needs analytic, literature, experimental, or machine-check work, and choose the cheapest adequate task. Delegate no more than three distinct bounded scientific subproblems, normally fewer. Give workers primary artifact paths, deliverables, and stopping conditions. The only nested task permitted is a bounded `scientific-computation -> engineer` substrate handoff; Engineer cannot delegate and its work does not become another scientific evidence stream.
4. Instantiate an executable obligation when a conclusion-critical mathematical assertion can actually be decided mechanically. Define its question and acceptance criterion first, allocate it with `research_new_check`, and delegate implementation to `scientific-computation`. Do not require new computational work every cycle, and do not turn obligation creation into ceremony for trivial claims or assertions a check cannot discriminate.
5. Require workers to save important outputs in the appropriate literature-note, derivation, experiment, obligation, or internal-critique artifact. A chat summary alone is not evidence, and an obligation without a runner-produced `result.json` has not run.
6. Integrate the evidence using `research-synthesis`. Preserve conflicting regimes, failed and inconclusive obligations, shared dependencies, and uncertainty. Never delete a failed obligation; supersede it and record why.
7. Use `internal-critic-openai` for a fresh second pass when a frozen result is concrete enough and the critique can change the immediate decision. Its report belongs under `research/critiques/` and is not independent evidence. Never invoke Opus during an ordinary cycle. If this cycle produces a mature, critical, final load-bearing claim, list it as a candidate under `Final independent-verification nominations` with the readiness gaps and rationale, but leave `checks.independent_verification: not-requested` until the user explicitly approves `/verify-claim`.
8. Update `research/claims/ledger.yaml`, `research/STATE.md`, and `research/DECISIONS.md` only to the extent warranted by actual evidence. Never silently promote status, and set `checks.computational_verification` only from recorded machine results.
9. Update `research/COMPUTATION.md` when representations, methods, evidence standards, infrastructure, independence needs, or the research phase materially changed this cycle. Leave it alone when nothing material changed.
10. Run `research_validate_state` and fix structural errors.

Stop after this iteration. Report what changed, what remains unresolved, any failed falsification attempts or failed obligations, and the next single best action. Do not automatically launch another cycle.
