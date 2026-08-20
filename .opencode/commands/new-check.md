---
description: Allocate the next ONNN machine-check obligation for a concrete assertion, define its acceptance criterion, and delegate implementation.
agent: research-director
---

Create one machine-check obligation for:

<assertion>
$ARGUMENTS
</assertion>

If the request is empty, ask for the concrete assertion or the existing `CNNN`/`DNNN` artifact to test, and create nothing. Otherwise:

1. Read `research/COMPUTATION.md`, the exact ledger claim or derivation step, and the existing obligations under `research/checks/`. Confirm every referenced ID exists and that this assertion is not already covered by an active obligation.
2. Decide whether the assertion is actually machine-checkable. State plainly what a mechanical test could decide and what it could not. If a check would only restate a weaker statement, or could not fail, record that in the plan's checkability map and stop instead of manufacturing ceremony.
3. Before any implementation, write the exact mathematical question, the assumptions the check would encode, and a predeclared pass/fail/inconclusive acceptance criterion. Choose the method and representation from the plan's declared options, or record a new choice and its rationale; do not default to a favorite package.
4. Decide whether reusable machinery under `research/computation/` is warranted, or whether a one-off entrypoint is enough.
5. Invoke `research_new_check` with the title, question, acceptance criterion, target claim/derivation IDs, check class, method, and independence requirement. Never choose an `ONNN` ID or create the directory manually.
6. Delegate implementation to `scientific-computation` when the work is nontrivial. Give it the obligation path, the frozen assertion, the acceptance criterion, and a stopping condition. Require it to test that the check can fail, and to execute only through `research_run_check`.
7. Leave the result pending until the obligation has actually run. A scaffolded obligation has no `result.json`, and the absence of that file is the correct record of "not run". Never write or edit `result.json`.
8. Link the obligation from the claim's `evidence.computational_checks` when it targets a claim, and update `research/COMPUTATION.md` and `research/STATE.md` where materially relevant.
9. Run `research_validate_state` and fix structural errors.

A passing obligation is evidence for the declared assertion under its encoded assumptions. It does not verify the scientific claim, and this command must not declare the check sufficient for verification; that judgment belongs to the independent verifier.

Return the obligation ID and path, the frozen question, the acceptance criterion, the encoded assumptions, what the check will not settle, and the exact run command.
