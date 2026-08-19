# Research Workflow

## Set Up

Install Python 3.11+ and `uv`, then create the locked helper environment:

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
```

Open the repository with `opencode .`. Restart OpenCode after changing files under `.opencode/` or `opencode.json`; configuration is loaded only at startup.

No literature service or API credential is required for the baseline workflow.

## Start a Question

```text
/research-start What is the leading finite-size correction to ...?
```

The director records the problem in `research/QUESTION.md`, maps literature/theory/numerical work, creates distinct `HNNN` artifacts when appropriate, registers only precise conjectural claims, and compresses the initial picture into `research/STATE.md`. This is initialization, not a completed research result.

Expected artifacts:

- a scoped question with conventions and success criteria;
- competing hypotheses with predictions and falsifiers;
- bounded workstreams and first discriminating tests;
- an updated state summary and structurally valid claim ledger.

## Run a Bounded Cycle

```text
/research-cycle
```

One cycle selects the highest-information unresolved issue, delegates a small number of specialized tasks, requires evidence artifacts, integrates disagreements, requests independent verification when warranted, and updates state. It stops rather than automatically launching another cycle.

Typical outputs are:

- `research/literature/notes/<source>.md` for exact source evidence;
- `research/derivations/DNNN.md` for an analytical argument;
- `research/experiments/ENNN/` for a computational test;
- a new or updated `CNNN` ledger entry;
- `research/results/verification/<claim>-<date>.md` for an independent attack.

## Create Artifacts Directly

From OpenCode:

```text
/new-hypothesis A boundary-layer mechanism controls the correction
/new-experiment Test C003 against increasing system size
```

From the shell:

```bash
uv run --locked python scripts/new_hypothesis.py --title "Boundary-layer mechanism"
uv run --locked python scripts/new_experiment.py --title "Finite-size scaling diagnostic" --claim C003
```

The helpers inspect existing IDs, allocate the next one, instantiate templates, refuse overwrite, and append lightweight provenance.

## Verify Before Acceptance

```text
/verify-claim C003
```

The verifier receives the exact ledger claim and primary artifacts, reconstructs or reproduces it, attempts falsification, and writes a report. Only a genuinely independent `verified` report can support ledger status `verified`; supportive work sharing code or assumptions remains below that threshold.

The normal lifecycle is:

```text
hypothesis
    -> derivation / literature / experiment
    -> claim entry
    -> recorded checks
    -> independent verifier
    -> verified / inconclusive / contradicted
```

Failed verification remains in the repository.

## Inspect State

```text
/research-status
```

This reports the question, active hypotheses, claims by status, verification gaps, experiments, contradictions, and next actions from files. The equivalent shell commands are:

```bash
uv run --locked python scripts/research_status.py
uv run --locked python scripts/research_status.py --json
uv run --locked python scripts/validate_research_state.py
```

Use `research/STATE.md` as concise durable memory, not a raw lab notebook. Put consequential changes of scope, conventions, methods, or interpretation in `research/DECISIONS.md`.
