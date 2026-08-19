---
description: Allocate the next ENNN directory and design a reproducible, discriminating computational physics experiment.
agent: research-director
---

Create one computational experiment for:

<experiment-request>
$ARGUMENTS
</experiment-request>

If the request is empty, ask for the claim or hypothesis to test. Otherwise:

1. Read the current question, relevant hypothesis, exact ledger claim, and prior experiments. Confirm every referenced claim ID exists.
2. Define the observable, units, baseline, parameter range, possible discriminating outcomes, numerical method, convergence threshold, and scientific/numerical failure criteria before implementation.
3. Invoke `research_new_experiment` with a concise title and existing claim IDs. Never create the `ENNN` directory manually.
4. Complete `README.md` and `config.yaml`. Start with an analytic estimate or tiny diagnostic and explain when a full run would be justified.
5. Implement only enough `run.py` and `analysis.py` for the requested stage. Do not run an expensive calculation unless explicitly requested and justified by successful cheap diagnostics.
6. Leave unperformed result checks incomplete. A scaffold or successful process exit is not a scientific result.
7. Update `research/STATE.md` under running/next experiments and run `research_validate_state`.

Return the experiment ID/path, canonical command, discriminating observable, planned checks, and stop/go criterion for larger computation.
