---
description: Report the current question, hypotheses, claims, verification gaps, experiments, contradictions, and next actions from repository artifacts.
agent: research-director
---

Produce a compact status report from durable artifacts, not conversation history. Optional emphasis:

<focus>
$ARGUMENTS
</focus>

1. Invoke `research_status` for the machine-derived summary.
2. Run `research_validate_state`; include validation failures without trying to hide or reinterpret them.
3. Read concise `research/STATE.md` for the working picture, strongest evidence, literature gaps, and next recommended actions.
4. Report the question, active hypotheses, important claims grouped by status, unresolved independent verification, active experiments, major contradictions, and the top next actions.
5. Flag stale or inconsistent state explicitly. Do not perform a research cycle or mutate artifacts unless the user asked for repair.
