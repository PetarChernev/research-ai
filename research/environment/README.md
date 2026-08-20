# Research-Scoped Computational Environment

This directory is reserved for the execution environment chosen by an active
research project. It is neutral and intentionally contains no environment
manifest, lock, package list, container definition, or scientific dependency on
the architecture-only baseline.

## Environment boundary

```text
architecture/tooling environment
    |
    | invokes
    v
research computation environment
    |
    v
claim-specific computation
```

The root `pyproject.toml` and `uv.lock` support repository helpers, structural
validation, and tests. Do not turn that locked tooling environment into a
speculative scientific stack. When a research question requires another
runtime, Scientific Computation chooses its capabilities and trust strategy;
the bounded Engineer creates and maintains the research-scoped substrate here.

## Allowed mechanisms

A project may add the mechanism appropriate to its work, for example:

- `environment.yml` or a conda/mamba lock;
- `pixi.toml` and its lock;
- a research-scoped `pyproject.toml` and requirements lock;
- Julia `Project.toml` and `Manifest.toml`;
- a container definition and pinned base-image identity;
- documented system-package or external-executable requirements;
- another reproducible mechanism selected by the research.

These are examples, not a preferred stack. No one format is required by the
global validator.

For compiled scientific ecosystems, mixed-language stacks, or dependencies
whose binary compatibility is difficult to reproduce, a project-scoped
conda/mamba-style environment plus an explicit lock is often a useful preferred
pattern when appropriate. It remains a research choice, not a global mandate.

## Ownership and reproducibility

Scientific Computation specifies the required capabilities, records the choice
and rationale in `research/COMPUTATION.md`, and decides whether the environment
faithfully supports the intended checks. Engineer implements the selected
environment, pins dependencies where appropriate, resolves compatibility,
records build and smoke-test commands, and documents platform limitations.

Any obligation that materially depends on a manifest, lock, container
definition, build configuration, or executable-version record here must list
that file or directory under `implementation.infrastructure` in its `spec.yaml`.
The deterministic runner fingerprints declared dependencies; changing one makes
the old result structurally stale until Scientific Computation reruns the
obligation.

Never store credentials, activated-environment contents, package caches, large
binary images, or machine-local absolute paths here. Record stable acquisition
instructions and content identities instead.
