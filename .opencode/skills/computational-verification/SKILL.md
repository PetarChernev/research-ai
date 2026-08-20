---
name: computational-verification
description: Use to turn a scientific assertion into a reproducible claim-linked machine-check obligation with a declared question, assumptions, predeclared acceptance criterion, executable implementation, and deterministically recorded outcome.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-computation
  artifact: machine-check-obligation
---

# Build a Machine-Check Obligation

An obligation is one concrete declared assertion made executable. It is not an
experiment: an experiment explores a hypothesis or computes an observable, while
an obligation tests whether a stated assertion holds under stated assumptions.
Use `numerical-experiment` for the former.

## 1. Read the target and the plan

Quote the exact `CNNN` claim or `DNNN` derivation step under test. Read
`research/COMPUTATION.md`: it records this project's current phase,
representations, methods, evidence standards, independence strategy, and
infrastructure. The global architecture prescribes none of those; the research
does. If the plan does not cover this case, say so and propose an option rather
than importing a preferred package by habit.

## 2. State what is and is not tested

Write the mathematical question precisely enough that a reader can see its
boundary. Then write the complement explicitly: which parts of the scientific
claim this obligation leaves untouched. An obligation that quietly tests a
weaker statement than the claim is the most common failure of this workflow.

## 3. Declare assumptions

Record every assumption the implementation will encode: conventions,
normalizations, signs, units, domains, regularity, parameter ranges, branch
choices, discretization, truncation order, and representation. An assumption
that exists only in code is a hidden assumption.

## 4. Choose a method the research plan supports

Select from what the plan declares, or propose an addition. Nothing in this
workspace binds a class to a tool: `symmetry` does not imply a computer-algebra
system, `formal` does not imply a particular proof assistant, and `numerical`
does not imply a particular array library. Prefer the smallest representation
that can actually discriminate.

## 5. Predeclare the acceptance criterion

State pass, fail, and inconclusive conditions before implementing: exact
equality in a named normal form, a residual below a stated norm and threshold, a
convergence rate within a stated band, a proof term accepted by a named checker
under named axioms, a counterexample found or a search exhausted over a stated
domain. Never adjust the criterion after seeing output. If the criterion was
wrong, supersede the obligation and record why.

## 6. Decide where the code belongs

Machinery that only this obligation needs goes in its own entrypoint. Machinery
that several obligations, experiments, or analyses will share goes in
`research/computation/`, gets its own tests, and is documented in
`research/COMPUTATION.md`. Remember that shared infrastructure creates shared
failure modes and destroys claimed independence.

## 7. Allocate the artifact

```bash
uv run --locked python scripts/new_check.py \
  --title "..." --claim C001 \
  --question "..." --acceptance-criterion "..."
```

Or use `research_new_check`. Never choose an `ONNN` ID by hand and never create
the directory manually. Fill `spec.yaml` and `README.md`, and declare any
`research/computation/` dependency under `implementation.infrastructure`.

## 8. Implement the smallest adequate check

Write the least code that can decide the declared criterion. Use the exit
protocol: `0` passed, `1` failed, `2` inconclusive, anything else an execution
error. Emit optional structured metrics with `emit_observations({...})`; they are
data and never select the outcome. Do not write `result.json`.

## 9. Test the check itself

Where practical, confirm that the implementation fails when it should: feed it a
deliberately wrong input, a perturbed sign, or a known counterexample and verify
it returns `1`. A check that cannot fail proves nothing about the claim.

## 10. Execute only through the wrapper

Run via `research_run_check` or:

```bash
uv run --locked python scripts/run_check.py O001
```

The deterministic wrapper is the sole writer of `research/checks/ONNN/result.json`
and derives the canonical outcome from the actual process exit status, together
with the spec and implementation hashes, environment, timestamps, Git state, and
provenance. Editing that file by hand, or reporting an outcome it did not record,
fabricates evidence.

## 11. Preserve everything the run produced

Keep failures, inconclusive outcomes, logs, and generated artifacts. A failed
obligation is a durable scientific result and often the most informative one. If
the implementation or spec changes afterward, the recorded hashes no longer match
and the result is stale: rerun it.

## 12. Report honestly to the director

Return the obligation path, the spec, the recorded result path, the machine
outcome, and the limitations. Keep these distinctions visible:

- exact symbolic output may still depend on assumptions, simplification
  strategy, branch cuts, or the chosen representation;
- numerical agreement is not a derivation;
- random or property-based sampling is not proof, only coverage;
- a formal proof establishes exactly the formalized proposition under its
  encoded assumptions and axioms, no more;
- a second implementation is independent only if its material assumptions and
  code paths genuinely differ.

## 13. Do not promote the claim

You do not set claim status, edit `research/claims/ledger.yaml`, write
verification reports, or call the scientific question verified. A successful
machine check is evidence for the declared assertion. Whether the declared
obligations are sufficient for the scientific claim is the independent
verifier's judgment, and the director integrates the result.
