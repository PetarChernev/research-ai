# {{OBLIGATION_ID}}: {{TITLE}}

Canonical machine-checkable obligation. `spec.yaml` is the declaration,
`run.py` (or the declared entrypoint) is the implementation, and `result.json`
is written **only** by the deterministic runner.

## Targets

Claims: {{CLAIMS_DISPLAY}}

Derivations: {{DERIVATIONS_DISPLAY}}

## Question tested

{{QUESTION}}

## What this does not test

State the parts of the scientific claim this obligation leaves untouched. A
passing check is evidence for the declared assertion only.

## Assumptions encoded in the implementation

Record conventions, normalizations, domains, parameter ranges, representation
choices, and any simplification the implementation relies on. An assumption that
exists only in code is a hidden assumption.

## Method

{{METHOD_DESCRIPTION}}

Rationale: {{METHOD_RATIONALE}}

## Acceptance criterion

{{ACCEPTANCE_CRITERION}}

Declare thresholds, tolerances, precision, sample sizes, or rigor level before
running. Do not adjust the criterion after seeing output; supersede the
obligation instead and say why.

## Infrastructure used

List reusable machinery from `research/computation/` that this obligation
depends on, and how that machinery is itself tested.

## How to run

```bash
uv run --locked python scripts/run_check.py {{OBLIGATION_ID}}
```

The runner determines the canonical outcome from actual process execution:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

Never write or edit `result.json` by hand.

## Result

No result recorded. The absence of `result.json` means this obligation has not
run.

## Interpretation and limitations

Record what the machine outcome does and does not establish, the limitations of
the representation and tooling, and any follow-up obligation that would close a
remaining gap. A passing computation is not a verified scientific claim.
