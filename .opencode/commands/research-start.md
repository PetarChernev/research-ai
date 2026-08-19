---
description: Initialize durable research artifacts, competing hypotheses, workstreams, and first discriminating tasks for a physics question.
agent: research-director
---

Start a new artifact-driven research program for this question:

<research-question>
$ARGUMENTS
</research-question>

If the question is empty, ask for it and make no scientific artifacts. Otherwise implement this bounded initialization:

1. Read `AGENTS.md`, current `research/QUESTION.md`, `research/STATE.md`, `research/DECISIONS.md`, and `research/claims/ledger.yaml`. Preserve relevant existing work; if this changes an established question, record the consequential scope decision.
2. Rewrite `research/QUESTION.md` with the exact question, physical scope, exclusions, observables, conventions, parameter regime, and practical success criteria. Mark unresolved choices explicitly.
3. Build an initial map of what is known, what must be derived, what needs literature evidence, and what can be tested numerically. Delegate at most three sharply bounded discovery tasks where specialization adds value; do not recurse through subagents.
4. Generate multiple competing hypotheses when the question permits. Use `research_new_hypothesis` for stable IDs, then fill assumptions, predictions, falsifiers, and discriminating tests. Do not manufacture diversity when there is only one meaningful hypothesis.
5. Add only genuinely precise candidate claims to the ledger, with status `conjecture` and no invented evidence. Use the `update-claim-ledger` skill.
6. Rank the first tasks by information gain and cost. Prefer analytic limits and tiny diagnostics before full calculations.
7. Update every section of concise `research/STATE.md`, including literature gaps and independent-verification needs. Do not pretend this invocation finishes the research.
8. Run `research_validate_state`. Fix structural failures and report scientific unknowns separately.

Finish with artifact paths created or changed, delegated work and its limits, the competing hypotheses, and the single best next discriminating action.
