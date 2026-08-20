# Reproducibility and Provenance

## Environment

Helper dependencies are declared in `pyproject.toml` and locked with `uv.lock`:

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
uv run --locked python -m unittest discover -s tests -t .
```

The tests under `tests/` cover the helper scripts and the workspace configuration. They use only the standard library plus the locked `PyYAML` dependency, and they exercise the scripts through the same command-line entry points the OpenCode tools call.

The baseline environment contains only helper dependencies. No scientific package is installed globally or architecturally required. Preserve this separation:

```text
architecture/tooling environment
    -> invokes research computation environment
    -> executes claim-specific computation
```

The research chooses an appropriate environment mechanism and records its rationale in `research/COMPUTATION.md`. Neutral examples include conda/mamba-style manifests and locks, pixi, a research-scoped Python project and lock, Julia Project/Manifest files, containers, documented system packages, or another reproducible mechanism. Scientific Computation specifies required capabilities; Engineer creates and maintains the selected files under `research/environment/`. Do not install a broad scientific stack speculatively or add claim-specific packages to the root tooling environment.

For command-line software, prefer an ordinary reproducible command or a thin OpenCode tool that delegates to a checked-in script. Scientific output becomes evidence only after it is preserved and linked from the claim ledger.

Reproducibility requirements apply to symbolic and formal work exactly as they apply to numerical work. A symbolic calculation is still a computation: its result depends on the package version, simplification strategy, assumption declarations, branch-cut handling, and normal form. A proof-assistant run depends on the toolchain version, the axioms and imports in scope, and the exact formalized statement. Record those the same way you would record a solver tolerance.

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

## Machine-Check Obligation Record

An obligation under `research/checks/ONNN/` has its own reproducibility contract, and it applies to symbolic, exact, formal, and numerical checks alike. `scripts/run_check.py` records:

- the exact command executed and the canonical runner command;
- the Git commit and dirty-worktree state;
- the `spec_sha256` of `spec.yaml`;
- the `implementation_sha256` of the declared entrypoint;
- a per-path content fingerprint and aggregate `infrastructure_sha256` for every declared reusable source, directory, environment manifest, lock, container definition, or build record;
- environment information, including interpreter, platform, and installed package versions;
- start and completion timestamps;
- the process exit code and the derived outcome;
- structured observations emitted by the implementation;
- preserved stdout and stderr under `logs/`;
- generated files under `artifacts/`.

The declaration itself carries the rest: the exact question, encoded assumptions, predeclared acceptance criterion, method and rationale, parameters and tolerances or rigor level, random seeds where relevant, input provenance, and every material `research/computation/` or `research/environment/` dependency under `implementation.infrastructure`.

The validator recomputes the spec, entrypoint, and declared infrastructure fingerprints. A content change to a file, a deterministic directory tree, or a declared environment manifest makes the recorded result stale and requires a rerun. Directory fingerprints sort repository-relative entries and hash names, kinds, and file contents; timestamps and traversal order do not affect them. Prefer declaring a compact manifest or lock rather than an activated environment directory. A scaffolded obligation has no `result.json` at all, so a missing result file is the honest record of "not run".

Never hand-write or edit `research/checks/ONNN/result.json`. The wrapper writes it atomically through a temporary file and replaces the previous result, so a partially written file cannot be mistaken for a completed run.

## Create and Run

```bash
uv run --locked python scripts/new_experiment.py --title "Diagnostic" --claim C001
uv run --locked python research/experiments/E001/run.py
uv run --locked python research/experiments/E001/analysis.py

uv run --locked python scripts/new_check.py \
  --title "Declared assertion" --claim C001 \
  --question "..." --acceptance-criterion "..."
uv run --locked python scripts/run_check.py O001
```

Both scaffolds deliberately refuse to fabricate a result. The experiment's `compute()` raises `NotImplementedError`; the obligation's `check()` does the same and the wrapper records that as an execution error rather than a pass. After implementation, the experiment runner records the config SHA-256, command, environment, parameters, seeds, timestamps, Git metadata, and observables, leaves scientific validation incomplete until the declared checks are actually performed, and refuses to overwrite a nonempty result. Use a new `ENNN` artifact for a distinct run. The obligation wrapper replaces its result on each run, because the recorded hashes tie the result to the exact spec and implementation that produced it.

To reproduce an existing result, reconstruct the complete chain:

```text
repository state
+ research environment
+ declared infrastructure
+ obligation spec
+ claim-specific implementation
```

For conclusion-critical infrastructure preserve, where relevant: environment manifest and lock; package and external executable versions; build instructions; platform information; kernel commit or content fingerprint; declared dependent paths; infrastructure test commands and outcomes; Scientific Computation's research-specific validation; and Engineer and Scientific Computation model provenance. Start from the recorded commit when practical, recreate the research environment, rerun a known small limit first, then compare the full result within the declared tolerance.

Distinguish three modes explicitly. Rerunning `scripts/run_check.py ONNN` against the same entrypoint and infrastructure is repetition: it tests determinism and provenance, not correctness. Rebuilding the calculation from the recorded specification with your own code is reproduction. A different algorithm, representation, library, environment, or language is an independent implementation only to the extent it avoids shared assumptions and code paths. Engineer-built infrastructure is a shared dependency, not an independent evidence stream.

## Data Policy

`research/experiments/*/raw/` is ignored except for its README. Machine-check logs and artifacts under `research/checks/*/logs/` and `research/checks/*/artifacts/` are tracked, because they are the preserved evidence of a recorded run; keep them small, and record a stable external location for anything large. Large or licensed data should remain in an appropriate external store. Record a stable URI or acquisition command, content checksum, size, units, schema, and access constraints. Small indispensable inputs may be force-added deliberately after review.

Figures may be tracked, but each must identify its source result and analysis command. A figure is not a replacement for machine-readable output.

## Git

Git is part of the lab notebook. Commit coherent research states after review, but exploration does not require a clean worktree. Generated results record dirty state so later readers know when the commit alone is insufficient. Never rewrite failed experiments or verification history merely to produce a clean narrative.

## Provenance JSONL

`research/provenance.jsonl` contains one JSON object per significant action. Supported metadata includes:

```text
timestamp, agent, provider_id, model_id, session_id, tool, operation,
delegated_agent, task, experiment_id, obligation_id, claim_id, command, relevant_paths,
git_commit, dirty_worktree, success
```

The plugin distinguishes research-environment and reusable-infrastructure writes, records Engineer's actual agent/model on those writes, and records `engineer-provisioned` with Scientific Computation as parent plus `delegated_agent: engineer` and an associated obligation ID when one is present. It does not log prompts, credentials, environment values, arbitrary contents, or command output. Provenance is an audit aid, not proof that a scientific check or infrastructure test succeeded; actual outcomes belong in durable artifacts.

Validate JSONL and all research state with:

```bash
uv run --locked python scripts/validate_research_state.py --strict
```
