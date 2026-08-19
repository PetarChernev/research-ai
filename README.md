# AI-Assisted Physics Research Workspace

This repository uses OpenCode as a lightweight orchestration layer for theoretical and computational physics. Agents exchange durable hypotheses, claims, derivations, experiments, literature notes, and verification reports through the filesystem and Git.

## Quick Start

Requirements: OpenCode 1.18+, Python 3.11+, and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
opencode .
```

Then begin in OpenCode:

```text
/research-start <your physics question>
```

Continue with `/research-cycle`, inspect with `/research-status`, and independently test an important claim with `/verify-claim C001`.

Create artifacts directly when needed:

```bash
uv run --locked python scripts/new_hypothesis.py --title "Candidate mechanism"
uv run --locked python scripts/new_experiment.py --title "Small-scale diagnostic"
```

See `docs/RESEARCH_WORKFLOW.md` for the workflow and `docs/REPRODUCIBILITY.md` for experiment requirements. OpenCode configuration is project-local and does not select an LLM vendor or model.
