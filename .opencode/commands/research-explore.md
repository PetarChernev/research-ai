---
description: Run one bounded breadth-first wave of parallel theory branches, GPT internal critiques, synthesis, and cheap discriminating checks.
agent: research-director
---

Run one breadth-first exploration wave. Optional focus and width supplied by the
user:

<exploration-request>
$ARGUMENTS
</exploration-request>

Use width 8 unless the user requests another value. Accept widths 2 through 16;
do not silently reduce the requested width merely to make integration easier.

1. Read `research/QUESTION.md`, `research/STATE.md`, `research/COMPUTATION.md`, the claim ledger, active hypotheses, and only the primary artifacts needed to avoid duplicate branches. If the question is not initialized, stop and request `/research-start`.
2. Freeze one exploration objective and build a branch matrix whose rows differ materially in assumptions, formalism, regime, limiting case, constructive route, no-go strategy, or observable consequences. Do not manufacture nominal diversity by paraphrasing one approach. Include at least one adversarial or impossibility branch when scientifically meaningful.
3. Assign a short wave label. Invoke `research_new_derivations` once with every branch title and charter so all `DNNN` destinations exist before workers launch. Speculative branches need not create ledger claims.
4. Launch every theorist as sibling tasks in one parallel batch. Give each its preassigned derivation path, exact charter, frozen common assumptions, relevant source paths, expected sections, and a stopping condition. Ask branches not to inspect sibling outputs during first pass. Parallel GPT sessions are procedurally separate, not independent evidence.
5. Wait for the complete first-pass barrier. Record missing or failed branches without silently replacing their intended perspective.
6. For every substantive completed branch, choose a unique path under `research/critiques/` and launch fresh `internal-critic-openai` tasks in one parallel batch. Give each only the frozen target and minimal dependencies. Require one load-bearing reconstruction, at most three attacks, and the internal-critique outcome vocabulary. Do not route any task to Opus.
7. Integrate branches and critiques using `research-synthesis`. Compare assumptions, predictions, regimes, contradictions, shared model dependence, and exposed failure modes. Rank by explanatory reach, consistency, falsifiability, and information value rather than votes or repeated agreement.
8. Prune clearly blocked branches, retain unresolved alternatives, and identify the smallest set of decisive assertions among the survivors. Do not build substantial infrastructure for a branch that has not survived internal critique.
9. When cheap machine checks can discriminate survivors, predeclare the questions and criteria, allocate distinct obligations, and launch Scientific Computation tasks in parallel only when they own disjoint paths and existing shared infrastructure is stable. Serialize any shared environment or infrastructure change through Scientific Computation and Engineer.
10. Update `research/STATE.md` with the active exploration portfolio, critique outcomes, shortlist, machine-check queue, contradictions, and next convergence or breadth action. Update claims only for precise results supported by actual artifacts. Update `research/COMPUTATION.md` only if the wave changes methodology or evidence strategy.
11. Leave ordinary claims at `checks.independent_verification: not-requested`. You may list a mature critical claim as a future Opus candidate, but do not set it pending, ask for approval, or invoke independent verification during this command.
12. Run `research_validate_state`, fix structural failures, and stop after this wave.

Report the wave label, branch and critique paths, pruned and surviving approaches,
shared-dependence risks, machine outcomes actually recorded, and the best next
fan-in or second-wave decision.
