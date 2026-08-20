---
description: Execute one ONNN machine-check obligation through the deterministic runner and record the actual outcome.
agent: research-director
---

Execute the machine-check obligation supplied here:

<obligation-id>
$ARGUMENTS
</obligation-id>

Require exactly one existing `ONNN` ID. Then:

1. Read `research/checks/ONNN/spec.yaml`, its `README.md`, and the declared entrypoint. Confirm the question, encoded assumptions, and acceptance criterion are already recorded, and that the entrypoint actually implements that criterion rather than a weaker one.
2. If the obligation is still a scaffold, or the acceptance criterion is missing, stop and delegate implementation to `scientific-computation` first.
3. Invoke `research_run_check` with the obligation ID. This is the only permitted way to produce a result. Do not run the entrypoint directly to establish an outcome, and never write or edit `research/checks/ONNN/result.json`.
4. Report the outcome exactly as the runner recorded it: `passed`, `failed`, `inconclusive`, or `error`. Do not reinterpret a failure as a pass, and do not rerun with altered parameters to obtain a preferred outcome. If the acceptance criterion itself was wrong, mark the obligation `superseded`, record why, and allocate a new one.
5. Preserve logs and generated artifacts. A failed or inconclusive obligation is a durable scientific result.
6. Update the claim's `checks.computational_verification` only from recorded results, update `research/COMPUTATION.md` and `research/STATE.md` where materially relevant, and run `research_validate_state`.

A passed obligation satisfies that obligation. It does not verify the scientific claim.

Return the obligation ID, machine outcome, exit code, result path, log and artifact paths, and any structural validation error.
