---
description: Allocate the next HNNN artifact and turn the supplied candidate explanation into a falsifiable competing hypothesis.
agent: research-director
---

Create one new hypothesis from:

<candidate>
$ARGUMENTS
</candidate>

If no candidate was supplied, ask for a short statement and do not create an empty artifact. Otherwise:

1. Read the current question, active hypotheses, and claim ledger to avoid accidental duplication.
2. Invoke `research_new_hypothesis` with a concise title and initial falsifiable statement. Never choose an ID manually.
3. Complete every template section: question addressed, motivation, material assumptions, distinct predictions, supporting evidence criteria, concrete falsifiers, discriminating derivations/experiments, related claims/literature, current evidence, and open problems.
4. Explain how it differs from named alternatives. If it duplicates an existing hypothesis, update that artifact instead and preserve the unused new artifact only if it contains a genuinely distinct branch; otherwise remove only the just-created empty duplicate.
5. Do not add supporting claim evidence merely because the hypothesis was articulated.
6. Update `research/STATE.md` if this becomes active and run `research_validate_state`.

Return the stable ID, artifact path, sharpest prediction, and cheapest falsifying test.
