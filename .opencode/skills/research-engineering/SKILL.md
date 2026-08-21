---
name: research-engineering
description: Use only when Scientific Computation has supplied a bounded task to build, repair, test, or document research-specific environments or reusable computational infrastructure under research/environment/ or research/computation/.
compatibility: OpenCode 1.18+
metadata:
  domain: research-software-engineering
  operation: computational-substrate
---

# Research Engineering

This skill implements a computational substrate from a scientific-computing
contract. It does not choose the scientific question or define evidence.

## 1. Read the bounded handoff

Read the task from `scientific-computation`, the linked section of
`research/COMPUTATION.md`, relevant obligation specifications, and any supplied
computational contract. Confirm the purpose, required capability, permitted
paths, non-goals, required tests, deliverables, and environment constraints.
Return an incomplete or contradictory contract instead of guessing.

## 2. Identify software and environment requirements

Separate architecture tooling from research computation:

```text
architecture/tooling environment
    -> invokes research computation environment
    -> executes claim-specific computation
```

Keep research-scoped manifests, locks, smoke tests, and setup instructions under
`research/environment/`. Use the environment mechanism selected by the research;
do not mandate a package manager or add scientific packages to the root tooling
environment.

## 3. Freeze mathematical semantics

When the task involves a mathematical kernel, treat the computational contract
as authoritative. It should state the represented domain, coefficient domain,
basis or generators, algebraic relations, grading/index/orientation/sign
conventions, assumptions, normal form, equality semantics, primitive
operations, invariants, law tests, invalid-input behavior, non-goals, and the
minimum API needed by intended obligations.

Do not change those semantics without explicit approval from
`scientific-computation`. Do not silently add identities, coercions,
simplifications, regularity assumptions, or convention choices.

## 4. Implement the smallest adequate reusable substrate

Put reusable software and its tests under `research/computation/`. Keep APIs
explicit and auditable. For mathematical kernels, prefer where appropriate:

- canonical representations and exact arithmetic;
- explicit algebraic rules;
- a minimal primitive operation set;
- deterministic normal forms and serialization;
- rejection of unsupported or ambiguous inputs rather than guessing;
- compositions of tested primitives instead of opaque convenience operations.

Do not build a custom kernel when a well-tested existing implementation already
satisfies the contract with a smaller total risk. Do not generalize beyond the
declared use without a concrete reuse need.

## 5. Add infrastructure tests

Test that the software satisfies the supplied contract. Use relevant unit,
property, API, algebra-law, canonicalization-idempotence, serialization
round-trip, determinism, environment smoke, dependency compatibility, expected
exception, and performance sanity tests. A known algebra-law test supplied in
the contract is a software requirement, not permission to invent new
mathematics.

## 6. Run and record tests

Run standard Python unittest suites with `research_run_infrastructure_tests`.
Use an approval-gated command when a declared research-specific environment or
another test mechanism genuinely requires it; never request a broad persistent
interpreter allow. Preserve the exact commands and outcomes in documentation
under the permitted directories. Record
package versions, external executable versions, platform constraints, build
steps, and lock or manifest paths where relevant. Do not claim a test ran when
it did not.

## 7. Document the handoff

Document the public API, setup and smoke-test commands, deterministic behavior,
invalid-input behavior, assumptions inherited from the contract, and known
limitations. Identify the files or directories that dependent obligations must
declare under `implementation.infrastructure` so changes invalidate prior
machine results.

## 8. Return to Scientific Computation

Return: files changed; dependency/environment changes; tests added; exact test
commands and outcomes; API and usage notes; known limitations; unresolved
problems; and your full `provider/model` ID. `scientific-computation` must review
the handoff, validate the representation on research-specific cases, write the
claim-specific `ONNN/run.py`, and execute it through the deterministic runner.

Do not write scientific conclusions, claim status, verification reports,
canonical `result.json`, or claim-specific obligation runners. You establish
that software behaves according to its contract; you do not establish that the
contract is the right scientific representation.
