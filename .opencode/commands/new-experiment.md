---
description: Allocate the next ENNN directory and design a reproducible, discriminating computational physics experiment.
agent: research-director
---

Create one computational experiment for:

<experiment-request>
$ARGUMENTS
</experiment-request>

If the request is empty, ask for the claim or hypothesis to test. Otherwise:

0. Confirm an experiment is the right artifact. An experiment explores a hypothesis or computes an observable; a machine-check obligation tests one concrete declared assertion against a predeclared criterion. If the request is really the latter, use `/new-check` instead. The two may both be warranted, but do not substitute one for the other.
1. Read the current question, `research/COMPUTATION.md`, the relevant hypothesis, exact ledger claim, and prior experiments. Confirm every referenced claim ID exists.
2. Define the observable, units, baseline, parameter range, possible discriminating outcomes, numerical method, convergence threshold, and scientific/numerical failure criteria before implementation.
3. Invoke `research_new_experiment` with a concise title and existing claim IDs. Never create the `ENNN` directory manually. Delegate implementation to `scientific-computation` when the work is nontrivial.
4. Complete `README.md` and `config.yaml`, following the representations, methods, and evidence standards recorded in `research/COMPUTATION.md`. Start with an analytic estimate or tiny diagnostic and explain when a full run would be justified.
5. Implement only enough `run.py` and `analysis.py` for the requested stage. Do not run an expensive calculation unless explicitly requested and justified by successful cheap diagnostics.
6. Leave unperformed result checks incomplete. A scaffold or successful process exit is not a scientific result.
7. Update `research/STATE.md` under running/next experiments and run `research_validate_state`.

Return the experiment ID/path, canonical command, discriminating observable, planned checks, stop/go criterion for larger computation, and any assertion the experiment sharpened that may deserve its own `ONNN` obligation.
