# Research-Specific Computational Infrastructure

This directory holds **reusable computational machinery that this research
program decided it needs**. It is empty by default and deliberately so: the
global architecture provides the place, process, and provenance semantics, not
the mathematics or the tooling.

Scientific Computation owns the mathematical contract, trust strategy, and
research-specific validation. The bounded Engineer implements and maintains the
reusable substrate from that contract. Engineer is not a scientific authority,
does not choose the representation, and does not write claim-specific
obligation runners.

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

- Record in `research/COMPUTATION.md` why the infrastructure exists, its
  computational contract and public API, dependencies and environment,
  implementation provenance, which obligations depend on it, and its
  representational limitations.
- Declare the dependency in each dependent obligation's `spec.yaml` under
  `implementation.infrastructure`.
- Engineer tests that the machinery satisfies its contract: relevant unit,
  property, algebra-law, API, serialization, determinism, environment smoke,
  compatibility, and performance sanity tests.
- Scientific Computation separately validates that the contract and
  implementation faithfully represent the mathematics needed for the claim,
  using hand calculations, soluble limits, sign/normalization regressions, or
  independent representations where relevant.
- Keep it runnable through the research environment documented under
  `research/environment/`, or through the root tooling environment only when no
  additional scientific substrate is needed.
- Do not add a global project dependency for a package only one obligation
  needs; record the requirement with the artifact that uses it.

The Engineer handoff must report files changed, dependency/environment changes,
tests and outcomes, API notes, limitations, unresolved problems, and actual
`provider/model` provenance. Passing infrastructure tests says the software
behaves according to its contract; it does not say that the contract is the
right scientific representation.

Shared infrastructure creates shared failure modes. Two obligations built on the
same module are not independent implementations, and a verifier must be told
when they overlap.
