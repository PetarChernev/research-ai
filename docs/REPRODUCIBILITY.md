# Reproducibility and Provenance

## Environment

Helper dependencies are declared in `pyproject.toml` and locked with `uv.lock`:

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
```

An experiment may use Python with NumPy, SciPy, SymPy, mpmath, JAX, or QuTiP; Julia; C/C++; Mathematica or `wolframscript`; SageMath; FeynCalc; FORM; Cadabra; a domain-specific simulation code; or an HPC scheduler. Do not install a broad scientific stack speculatively. Add and lock only what the research needs, and record external executable versions and build flags in the experiment README/result.

For command-line software, prefer an ordinary reproducible command or a thin OpenCode tool that delegates to a checked-in script. Scientific output becomes evidence only after it is preserved and linked from the claim ledger.

## Experiment Record

Every important computational result needs:

- code and configuration;
- equations, algorithm, discretization, and solver settings;
- parameter values with units and ranges;
- random seeds when relevant;
- input identity, provenance, schema, and checksums;
- software versions and hardware-sensitive settings;
- exact or canonical reproducing command;
- Git commit and dirty-worktree state when available;
- convergence, precision, finite-size, timestep, tolerance, and sensitivity checks that apply;
- machine-readable observables and uncertainty in `result.json`;
- known limitations and comparison to analytical limits.

Do not mark a check complete because a process exited successfully. Use `passed`, `failed`, `inconclusive`, or `not-applicable`, preferably with a reason, threshold, and evidence path.

## Create and Run

```bash
uv run --locked python scripts/new_experiment.py --title "Diagnostic" --claim C001
uv run --locked python research/experiments/E001/run.py
uv run --locked python research/experiments/E001/analysis.py
```

The scaffold's `compute()` deliberately raises `NotImplementedError`; it cannot fabricate a result. After implementation, the runner records the config SHA-256, command, environment, parameters, seeds, timestamps, Git metadata, and observables. It leaves scientific validation incomplete until the declared checks are actually performed and refuses to overwrite a nonempty result. Use a new `ENNN` artifact for a distinct run.

To reproduce an existing result, start from its recorded commit when practical, use the lockfile and input checksums, rerun the smallest known limit first, then compare the full result within a declared tolerance. Preserve a separate result or verification report rather than overwriting the source artifact. Shared code means repeatability, not an independent implementation.

## Data Policy

`research/experiments/*/raw/` is ignored except for its README. Large or licensed data should remain in an appropriate external store. Record a stable URI or acquisition command, content checksum, size, units, schema, and access constraints. Small indispensable inputs may be force-added deliberately after review.

Figures may be tracked, but each must identify its source result and analysis command. A figure is not a replacement for machine-readable output.

## Git

Git is part of the lab notebook. Commit coherent research states after review, but exploration does not require a clean worktree. Generated results record dirty state so later readers know when the commit alone is insufficient. Never rewrite failed experiments or verification history merely to produce a clean narrative.

## Provenance JSONL

`research/provenance.jsonl` contains one JSON object per significant action. Supported metadata includes:

```text
timestamp, agent, session_id, tool, operation, experiment_id,
claim_id, command, relevant_paths, git_commit, dirty_worktree, success
```

The plugin does not log prompts, credentials, environment values, arbitrary contents, or command output. Helper scripts reject command logging when a string appears to contain credential-related terms. The validator itself appends a sanitized pass/fail metadata record, so a claimed validation run has a durable trace. Provenance is an audit aid, not proof that a scientific check succeeded; the actual check belongs in its evidence artifact.

Validate JSONL and all research state with:

```bash
uv run --locked python scripts/validate_research_state.py --strict
```
