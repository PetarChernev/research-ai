# AI-Assisted Physics Research Workspace

This repository uses OpenCode as a lightweight orchestration layer for theoretical and computational physics. Agents exchange durable hypotheses, claims, derivations, experiments, machine-check obligations, literature notes, and verification reports through the filesystem and Git.

## Quick Start

Requirements: OpenCode 1.18+, Python 3.11+, and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
uv run --locked python -m unittest discover -s tests -t .
opencode .
```

Then begin in OpenCode:

```text
/research-start <your physics question>
```

Continue with `/research-cycle`, inspect with `/research-status`, and independently test an important claim with `/verify-claim C001`. Turn a concrete assertion into an executable obligation with `/new-check` and run it with `/run-check O001`.

Create artifacts directly when needed:

```bash
uv run --locked python scripts/new_hypothesis.py --title "Candidate mechanism"
uv run --locked python scripts/new_experiment.py --title "Small-scale diagnostic"
uv run --locked python scripts/new_check.py --title "Declared assertion" \
  --question "..." --acceptance-criterion "..."
uv run --locked python scripts/run_check.py O001
```

## Computational Evidence

The architecture provides the place, process, provenance, and verification semantics for computational evidence. It does not prescribe the mathematics or the tooling: no symbolic, formal, or numerical package is installed or required globally. Each research project records its own representations, methods, standards, and independence strategy in `research/COMPUTATION.md`.

```text
research/computation/   reusable research-specific machinery
research/environment/   research-scoped environment definitions
research/checks/        claim-linked executable evidence (ONNN)
research/experiments/   scientific computational experiments (ENNN)
```

Scientific Computation owns the representation, trust strategy, computational contract, and claim-specific `ONNN/run.py`. When reusable software or a research environment must be created or materially changed, it provisions the bounded Engineer; Engineer is implementation support, not a scientific peer or verifier. `scripts/run_check.py` is the only writer of `research/checks/ONNN/result.json`, fingerprints declared infrastructure and environment manifests, and derives the outcome from actual process execution. A passing computation is evidence for a declared assertion, not a verified scientific claim; sufficiency remains the independent verifier's judgment.

See `docs/RESEARCH_WORKFLOW.md` for the workflow and `docs/REPRODUCIBILITY.md` for experiment and obligation requirements. The project binds verification roles to one OpenAI and one Anthropic model so the director can route review away from every model that materially produced a claim or its computational substrate. Unpinned producer roles may use the invoking session model, so actual artifact provenance remains authoritative.
