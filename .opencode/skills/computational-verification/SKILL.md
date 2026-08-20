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

## 4. Predeclare the acceptance criterion

State pass, fail, and inconclusive conditions before implementing: exact
equality in a named normal form, a residual below a stated norm and threshold, a
convergence rate within a stated band, a proof term accepted by a named checker
under named axioms, a counterexample found or a search exhausted over a stated
domain. Never adjust the criterion after seeing output. If the criterion was
wrong, supersede the obligation and record why.

## 5. Assess representation and trust surface

Before selecting an implementation, answer explicitly:

1. What mathematical domain is represented?
2. Which operations actually need support?
3. Does the domain admit an exact or canonical representation?
4. Is equality decidable by explicit normalization or canonicalization?
5. Which assumptions and conventions must be encoded?
6. What would be trusted if a general-purpose CAS were used?
7. Would a small domain-specific kernel materially reduce the trust surface?
8. Is an existing well-tested implementation already adequate?
9. Would custom infrastructure introduce more risk than it removes?
10. Which independent checks can validate the selected representation?

Prefer explicit mathematical structure over heuristic symbolic simplification
when a compact exact representation, canonical form, or small decidable
operation set is practical. Minimize the trusted computational surface by
reducing conclusion-critical work to a small set of explicit, testable
primitives where possible. A general-purpose CAS remains valid when its
semantics are suitable, for exact coefficient arithmetic, for a targeted
algorithm, or as an independent cross-check. Do not treat heuristic
`simplify()`-like behavior as an equality oracle without considering a clearer
exact method.

Record substantial representation choices and trust analysis in
`research/COMPUTATION.md`. Do not require a custom kernel when an existing exact,
well-tested implementation is adequate, and do not build one if its engineering
risk exceeds the trust reduction.

## 6. Determine whether infrastructure is sufficient

Machinery that only this obligation needs goes in its own entrypoint. Machinery
that several obligations, experiments, or analyses will share goes in
`research/computation/`; research-scoped environment manifests and locks go in
`research/environment/`. Existing adequate infrastructure requires no Engineer
invocation.

Provision Engineer only when a dependency is absent; a research environment
must be created or materially changed; compatibility must be established;
reusable infrastructure is missing, broken, inadequate, or too slow; a custom
kernel is scientifically justified; reusable solver or formalization support is
needed; or a verifier raises a material substrate concern.

Do not provision Engineer merely to write claim-specific verification code.

## 7. Define the contract and provision Engineer when needed

For custom mathematical infrastructure, freeze a computational contract before
delegation. State where relevant: represented objects; coefficient domain or
ring; generators or bases; algebraic relations; grading, index, orientation, and
sign conventions; assumptions; canonical or normal form; equality semantics;
required primitive operations; invariants and law tests; behavior on invalid or
unsupported inputs; explicit non-goals; and the minimum API needed by intended
obligations.

Keep the contract durable: record it in the relevant obligation README/spec and
return its plan-level consequences to the director for
`research/COMPUTATION.md`. If no obligation exists yet, allocate the minimal
artifact before provisioning Engineer rather than leaving the contract only in
chat.

Give Engineer a bounded task with the purpose, capability, contract, permitted
paths, non-goals, required tests, deliverables, environment constraints, and
links to `research/COMPUTATION.md` and relevant obligations. Engineer may work
only in `research/computation/` and `research/environment/`, may not delegate,
and must return files, dependency changes, tests and actual outcomes, API notes,
limitations, unresolved issues, and model provenance.

## 8. Review and scientifically validate the substrate

Review every Engineer change. Engineer-owned tests establish that software
behaves according to the contract: API behavior, algebra laws, deterministic
canonicalization, serialization, expected exceptions, dependency smoke tests,
compatibility, and performance sanity where relevant.

Perform separate research-specific validation that the contract and
implementation faithfully represent the mathematics needed for the claim:
reproduce a hand calculation or soluble limit, recover a conclusion-critical
sign or normalization, compare with an independent representation, verify that
encoded assumptions match the claim, and exercise research-specific regression
cases where applicable. The same test may inform both questions, but do not
confuse them.

Declare every material reusable source, directory, environment manifest, lock,
or build configuration under `implementation.infrastructure` so a change makes
the canonical result stale.

## 9. Allocate or complete the obligation

```bash
uv run --locked python scripts/new_check.py \
  --title "..." --claim C001 \
  --question "..." --acceptance-criterion "..."
```

Or use `research_new_check`. Never choose an `ONNN` ID by hand and never create
the directory manually. Fill `spec.yaml` and `README.md`, and declare any
material `research/computation/` or `research/environment/` dependency under
`implementation.infrastructure`.

## 10. Scientific Computation writes the claim-specific check

Write the least code that can decide the declared criterion. Use the exit
protocol: `0` passed, `1` failed, `2` inconclusive, anything else an execution
error. Emit optional structured metrics with `emit_observations({...})`; they are
data and never select the outcome. Do not write `result.json`.

You, not Engineer, write `research/checks/ONNN/run.py`. Construct the object or
matrix under test, define the residual, choose scientific samples, and apply the
predeclared acceptance criterion. Engineer may provide generic examples or
fixtures, but must not turn them into the scientific claim check on your behalf.

## 11. Test the check itself

Where practical, confirm that the implementation fails when it should: feed it a
deliberately wrong input, a perturbed sign, or a known counterexample and verify
it returns `1`. A check that cannot fail proves nothing about the claim.

## 12. Execute only through the wrapper

Run via `research_run_check` or:

```bash
uv run --locked python scripts/run_check.py O001
```

The deterministic wrapper is the sole writer of `research/checks/ONNN/result.json`
and derives the canonical outcome from the actual process exit status, together
with the spec and implementation hashes, environment, timestamps, Git state, and
declared infrastructure fingerprints. Editing that file by hand, or reporting
an outcome it did not record, fabricates evidence.

## 13. Interpret, preserve, and escalate

Keep failures, inconclusive outcomes, logs, and generated artifacts. A failed
obligation is a durable scientific result and often the most informative one. If
the implementation or spec changes afterward, the recorded hashes no longer match
and the result is stale: rerun it. Return the obligation path, spec, result,
machine outcome, declared infrastructure, producer model provenance, and
limitations to the director and independent verifier. Keep these distinctions
visible:

- exact symbolic output may still depend on assumptions, simplification
  strategy, branch cuts, or the chosen representation;
- numerical agreement is not a derivation;
- random or property-based sampling is not proof, only coverage;
- a formal proof establishes exactly the formalized proposition under its
  encoded assumptions and axioms, no more;
- a second implementation is independent only if its material assumptions and
  code paths genuinely differ.

You do not set claim status, edit `research/claims/ledger.yaml`, write
verification reports, or call the scientific question verified. A successful
machine check is evidence for the declared assertion. Whether the declared
obligations are sufficient for the scientific claim is the independent
verifier's judgment, and the director integrates the result.
