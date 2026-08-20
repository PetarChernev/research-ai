# Research-Specific Computational Infrastructure

This directory holds **reusable computational machinery that this research
program decided it needs**. It is empty by default and deliberately so: the
global architecture provides the place, process, and provenance semantics, not
the mathematics or the tooling.

Typical contents, once a project justifies them, might include custom symbolic
representations, algebraic or tensor machinery, domain-specific transformations,
exact-arithmetic helpers, discretization or solver infrastructure, formalization
sources for a proof assistant, or shared test utilities. Nothing here is
prescribed; a project may also decide it needs none of this.

## What belongs here

- Machinery used by more than one obligation, experiment, or analysis.
- Encodings of the project's conventions that must stay consistent across checks.
- Utilities whose correctness deserves its own tests.

## What does not belong here

- A one-off computation for a single obligation. Put that in the obligation's
  own entrypoint under `research/checks/ONNN/`.
- Results, logs, or generated data. Those live with the artifact that produced
  them.
- Anything intended to substitute for the readable derivation.

## Evidence boundary

```text
research/computation/   reusable methodology and infrastructure
research/checks/        claim-linked executable evidence
research/experiments/   scientific computational experiments
```

**A reusable mathematical library is not itself evidence.** A reproducible
execution of a declared obligation that uses the library is evidence. Passing a
library's own unit tests says the library behaves as its authors intended; it
says nothing about whether the encoded representation is physically faithful.

## Requirements for anything added here

- Record in `research/COMPUTATION.md` why the infrastructure exists, which
  obligations depend on it, and its representational limitations.
- Declare the dependency in each dependent obligation's `spec.yaml` under
  `implementation.infrastructure`.
- Test the machinery itself where practical. A check built on untested
  infrastructure inherits its bugs.
- Keep it importable and runnable from the repository root with the project's
  locked environment, or record the additional environment it needs.
- Do not add a global project dependency for a package only one obligation
  needs; record the requirement with the artifact that uses it.

Shared infrastructure creates shared failure modes. Two obligations built on the
same module are not independent implementations, and a verifier must be told
when they overlap.
