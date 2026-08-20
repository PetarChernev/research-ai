# Reproducibility and Provenance

## Environment

Helper dependencies are declared in `pyproject.toml` and locked with `uv.lock`:

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
uv run --locked python -m unittest discover -s tests -t .
```

The tests under `tests/` cover the helper scripts and the workspace configuration. They use only the standard library plus the locked `PyYAML` dependency, and they exercise the scripts through the same command-line entry points the OpenCode tools call.

The baseline environment contains only the helper dependencies. No symbolic, formal, or numerical scientific package is installed globally, and none is architecturally required. A research project may use Python with NumPy, SciPy, SymPy, mpmath, JAX, or QuTiP; Julia; C/C++; Mathematica or `wolframscript`; SageMath; FeynCalc; FORM; Cadabra; a proof assistant; an exact- or interval-arithmetic library; a domain-specific simulation code; an HPC scheduler; or bespoke machinery it writes itself. That choice belongs in `research/COMPUTATION.md` with its rationale. Do not install a broad scientific stack speculatively. Add and lock only what the research needs, and record external executable versions and build flags in the experiment or obligation artifact.

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
- environment information, including interpreter, platform, and installed package versions;
- start and completion timestamps;
- the process exit code and the derived outcome;
- structured observations emitted by the implementation;
- preserved stdout and stderr under `logs/`;
- generated files under `artifacts/`.

The declaration itself carries the rest: the exact question, the encoded assumptions, the predeclared acceptance criterion, the method and its rationale, the parameters and tolerances or rigor level the criterion depends on, random seeds where relevant, input provenance, and the `research/computation/` infrastructure the implementation uses.

Two consequences matter. First, the validator recomputes both hashes; if either file changed after the run, the recorded result is stale and must be rerun. Second, a scaffolded obligation has no `result.json` at all, so a missing result file is the honest record of "not run" and can never be mistaken for a check that was performed.

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

To reproduce an existing result, start from its recorded commit when practical, use the lockfile and input checksums, rerun the smallest known limit first, then compare the full result within a declared tolerance. Preserve a separate result or verification report rather than overwriting the source artifact.

Distinguish three modes explicitly. Rerunning `scripts/run_check.py ONNN` against the same entrypoint is repetition: it tests determinism and provenance, not correctness of the implementation. Rebuilding the calculation from the recorded specification with your own code is reproduction. A different algorithm, representation, library, or language is an independent implementation, and shared machinery from `research/computation/` reduces it back toward reproduction. Shared code means repeatability, not independence.

## Data Policy

`research/experiments/*/raw/` is ignored except for its README. Machine-check logs and artifacts under `research/checks/*/logs/` and `research/checks/*/artifacts/` are tracked, because they are the preserved evidence of a recorded run; keep them small, and record a stable external location for anything large. Large or licensed data should remain in an appropriate external store. Record a stable URI or acquisition command, content checksum, size, units, schema, and access constraints. Small indispensable inputs may be force-added deliberately after review.

Figures may be tracked, but each must identify its source result and analysis command. A figure is not a replacement for machine-readable output.

## Git

Git is part of the lab notebook. Commit coherent research states after review, but exploration does not require a clean worktree. Generated results record dirty state so later readers know when the commit alone is insufficient. Never rewrite failed experiments or verification history merely to produce a clean narrative.

## Provenance JSONL

`research/provenance.jsonl` contains one JSON object per significant action. Supported metadata includes:

```text
timestamp, agent, provider_id, model_id, session_id, tool, operation,
experiment_id, obligation_id, claim_id, command, relevant_paths,
git_commit, dirty_worktree, success
```

The plugin does not log prompts, credentials, environment values, arbitrary contents, or command output. Helper scripts reject command logging when a string appears to contain credential-related terms. The validator itself appends a sanitized pass/fail metadata record, so a claimed validation run has a durable trace. Provenance is an audit aid, not proof that a scientific check succeeded; the actual check belongs in its evidence artifact.

Validate JSONL and all research state with:

```bash
uv run --locked python scripts/validate_research_state.py --strict
```
