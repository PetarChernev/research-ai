---
description: Initialize durable research artifacts, competing hypotheses, workstreams, and first discriminating tasks for a physics question.
agent: research-director
---

Start a new artifact-driven research program for this question:

<research-question>
$ARGUMENTS
</research-question>

If the question is empty, ask for it and make no scientific artifacts. Otherwise implement this bounded initialization:

1. Read `AGENTS.md`, current `research/QUESTION.md`, `research/STATE.md`, `research/COMPUTATION.md`, `research/DECISIONS.md`, and `research/claims/ledger.yaml`. Preserve relevant existing work; if this changes an established question, record the consequential scope decision.
2. Rewrite `research/QUESTION.md` with the exact question, physical scope, exclusions, observables, conventions, parameter regime, and practical success criteria. Mark unresolved choices explicitly.
3. Build an initial map of what is known, what must be derived, what needs literature evidence, and what can be tested computationally. Delegate at most three sharply bounded discovery tasks where specialization adds value; do not recurse through subagents.
4. Generate multiple competing hypotheses when the question permits. Use `research_new_hypothesis` for stable IDs, then fill assumptions, predictions, falsifiers, and discriminating tests. Do not manufacture diversity when there is only one meaningful hypothesis.
5. Add only genuinely precise candidate claims to the ledger, with status `conjecture` and no invented evidence. Use the `update-claim-ledger` skill.
6. Initialize the computational verification strategy. Invoke `research_init_computation_plan`, then populate `research/COMPUTATION.md` yourself. Keep the initial strategy deliberately lightweight and specifically:
   - describe the current methodological regime in this problem's own terms;
   - identify the important candidate machine-checkable aspects of the question;
   - identify what cannot yet be usefully machine checked, and say why;
   - state whether any custom infrastructure under `research/computation/` is already justified, and prefer "not yet" when it is;
   - name the cheapest useful initial executable tests;
   - define the triggers that would require revisiting the strategy.

   Do not preselect a symbolic algebra system, proof assistant, interval-arithmetic library, tensor package, PDE solver, or numerical stack without a scientific reason recorded in the plan. The intended progression is `reason about what needs checking -> smallest useful executable diagnostic -> stronger machinery only when scientifically justified`. Sophisticated infrastructure is not expected at initialization.
7. Rank the first tasks by information gain and cost. Prefer analytic limits and tiny diagnostics before full calculations or heavy machinery.
8. Update every section of concise `research/STATE.md`, including literature gaps and independent-verification needs. Do not pretend this invocation finishes the research.
9. Run `research_validate_state`. Fix structural failures and report scientific unknowns separately.

Finish with artifact paths created or changed, delegated work and its limits, the competing hypotheses, the initial computational strategy in one or two sentences, and the single best next discriminating action.
