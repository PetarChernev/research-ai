# Machine-Check Obligations

A machine-check obligation is a claim-linked, executable test of one concrete
declared assertion. Obligations use stable IDs `O001`, `O002`, and so on. Create
one with the helper so IDs are never chosen by hand:

```bash
uv run --locked python scripts/new_check.py \
  --title "Short obligation title" \
  --claim C001 \
  --question "The exact mathematical question tested" \
  --acceptance-criterion "The predeclared pass/fail condition"
```

## Directory layout

```text
research/checks/O001/
    README.md      # scientific context: what is and is not tested
    spec.yaml      # declaration: targets, class, question, assumptions, criterion
    run.py         # the executable implementation (entrypoint declared in spec.yaml)
    result.json    # written ONLY by scripts/run_check.py
    logs/          # preserved stdout/stderr from the last recorded run
    artifacts/     # generated evidence files, when the check produces any
```

Scaffolding never creates `result.json`. **No result file means the obligation
has not run.**

## Execution

```bash
uv run --locked python scripts/run_check.py O001
```

The deterministic wrapper is the only component that creates or replaces
`result.json`. It derives the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

An implementation may print one structured JSON observation record to stdout
prefixed with `##OBSERVATIONS##`. The wrapper stores that payload as data; it
cannot select the outcome. The wrapper does not interpret the physics.

## Status and the structural gate

`status` is `active` or `superseded`. An active obligation with `required: true`
is part of the currently declared verification strategy for its target claims:

```text
pending required obligation      -> computational verification is not complete
failed required obligation       -> computational verification cannot be passed
inconclusive required obligation -> computational verification cannot be passed
passed required obligation       -> that obligation is satisfied
superseded obligation            -> does not block the current strategy
```

A claim cannot reach ledger status `verified` while an active required
obligation lacks a passing result. This is a structural statement about the
project's own declared strategy, not a judgment that the obligations are
scientifically sufficient. Sufficiency is the independent verifier's call.

If research later concludes that an obligation was misguided, mark it
`superseded` and record why. Do not delete failed history to clear the gate.

## Relationship to the neighbouring directories

```text
research/computation/   reusable research-specific computational machinery
research/checks/        claim-linked executions that produce evidence
research/experiments/   scientific numerical/computational experiments
```

A reusable mathematical library is not evidence. A reproducible execution of a
declared obligation using that library is evidence. An experiment explores a
hypothesis or computes an observable; an obligation tests a concrete declared
assertion. One computation may motivate both artifacts, but they are not the
same thing.

The research-specific plan in `research/COMPUTATION.md` decides which
obligations exist, what method each uses, and what standard it must meet.
