# Research Workflow

## Set Up

Install Python 3.11+ and `uv`, then create the locked helper environment:

```bash
uv sync --locked
uv run --locked python scripts/validate_research_state.py
uv run --locked python -m unittest discover -s tests -t .
```

Open the repository with `opencode .`. Restart OpenCode after changing files under `.opencode/` or `opencode.json`; configuration is loaded only at startup.

No literature service or API credential is required for the baseline workflow.

## Start a Question

```text
/research-start What is the leading finite-size correction to ...?
```

The director records the problem in `research/QUESTION.md`, maps literature, theory, and computational work, creates distinct `HNNN` artifacts when appropriate, registers only precise conjectural claims, initializes `research/COMPUTATION.md`, and compresses the initial picture into `research/STATE.md`. This is initialization, not a completed research result.

Expected artifacts:

- a scoped question with conventions and success criteria;
- competing hypotheses with predictions and falsifiers;
- bounded workstreams and first discriminating tests;
- an initial computational verification strategy;
- an updated state summary and structurally valid claim ledger.

The initial computational strategy is deliberately lightweight. It names the candidate machine-checkable aspects of the problem, what cannot yet be usefully machine checked, whether custom infrastructure or a research-scoped environment is already justified (usually not), the cheapest useful initial executable tests, and the triggers for revisiting the plan. The architecture prefers:

```text
reason about what needs checking
    -> smallest useful executable diagnostic
    -> stronger machinery only when scientifically justified
```

No symbolic, formal, numerical, or environment package is prescribed globally. The project chooses its own and records the choice with its rationale. Scientific Computation owns representation and trust-strategy choices; Engineer implements a bounded environment or reusable substrate only when Scientific Computation supplies an explicit need and contract.

## Run a Bounded Cycle

For broad, ambitious, or weakly mapped questions, explore before converging:

```text
/research-explore --width 8 optional focus
```

The director creates genuinely distinct branch charters, preallocates every
`DNNN` path, launches sibling GPT-5.6 Sol theorists concurrently, waits for the
first-pass barrier, and then launches fresh GPT internal critics concurrently.
The critics write under `research/critiques/`, are explicitly same-model, and
cannot independently verify a claim. The director synthesizes and prunes only
after both barriers, then sends cheap decisive assertions from surviving
branches to Scientific Computation. Opus is never invoked by this command.

Use a focused convergence cycle after a shortlist exists:

```text
/research-cycle
```

The director begins each cycle by reading `research/COMPUTATION.md` alongside the question, state, ledger, and hypotheses. One cycle selects the highest-information unresolved issue, decides whether it needs analytic, literature, experimental, or machine-check work, delegates a small number of specialized tasks, may request a fresh GPT internal critique, integrates disagreements, and updates state. It never invokes Opus. Scientific Computation may provision Engineer for one bounded substrate task; the Director does not invoke Engineer directly and Engineer cannot delegate. The cycle stops rather than automatically launching another cycle.

Typical outputs are:

- `research/literature/notes/<source>.md` for exact source evidence;
- `research/derivations/DNNN.md` for an analytical argument;
- `research/critiques/<target>-<date>-openai-NN.md` for same-model internal review;
- `research/experiments/ENNN/` for a computational experiment;
- `research/checks/ONNN/` for a claim-linked machine-check obligation;
- a new or updated `CNNN` ledger entry;
- `research/results/verification/<claim>-<date>.md` for an independent attack.

Not every cycle needs new computational work, and trivial claims do not need obligations. Update `research/COMPUTATION.md` only when representations, methods, evidence standards, infrastructure, or the research phase materially changed.

## Experiments and Obligations Are Different

```text
research/computation/   reusable research-specific machinery
research/environment/   research-scoped environment definitions
research/checks/        claim-linked executable evidence (ONNN)
research/experiments/   scientific computational experiments (ENNN)
```

An experiment explores a hypothesis or computes an observable. An obligation tests one concrete declared assertion against a predeclared acceptance criterion. One computation may motivate both, but they are separate artifacts with separate workflows: `numerical-experiment` and `computational-verification`.

A reusable library under `research/computation/` is methodology, not evidence. Only a reproducible execution of a declared obligation is evidence.

## Scientific Computation and Engineer

Theorist derives the mathematics. Scientific Computation identifies the precise
machine-checkable assertion, declares assumptions and acceptance criteria,
assesses the representation and trusted surface, and writes the claim-specific
obligation runner. Prefer explicit mathematical structure and a small tested
primitive set when practical, without banning a well-suited existing CAS or
library.

If existing software and environments are adequate, Scientific Computation
writes and runs the check directly. Engineer is provisioned only when a
dependency or research environment is missing, reusable infrastructure must be
created or repaired, a custom kernel is justified, compatibility must be
established, or substrate performance blocks required work.

Before that handoff, Scientific Computation freezes a computational contract:
represented domain, coefficient domain, bases/generators, relations,
grading/index/orientation/sign conventions, assumptions, normal form, equality,
primitive operations, invariants and law tests, invalid inputs, non-goals, and
minimum API as relevant. Engineer implements the smallest adequate substrate and
its software tests under `research/computation/` or `research/environment/`.
Scientific Computation reviews the handoff, validates the representation on
research-specific cases, and then writes `research/checks/ONNN/run.py`.

```text
theorist derives mathematics
        |
scientific computation defines assertion and representation
        |
existing infrastructure sufficient?
        | yes                         | no
        |                             v
        |                    computational contract
        |                             |
        |                    engineer builds/tests substrate
        |                             |
        `-----------------------------+
                      |
scientific computation validates substrate and writes claim check
                      |
deterministic runner executes
                      |
GPT internal critic attacks the result during ordinary convergence
                      |
optional late, user-approved Opus verifier audits a final critical claim
```

Engineer-owned tests answer whether software satisfies the supplied contract.
Scientific-Computing-owned validation answers whether that contract faithfully
represents the claim's mathematics. Engineer examples and fixtures never become
the claim check by default.

## Create Artifacts Directly

From OpenCode:

```text
/new-hypothesis A boundary-layer mechanism controls the correction
/new-experiment Test C003 against increasing system size
/new-check The residual of equation (12) vanishes identically for C003
/run-check O001
```

From the shell:

```bash
uv run --locked python scripts/new_hypothesis.py --title "Boundary-layer mechanism"
uv run --locked python scripts/new_derivations.py \
  --wave "initial-map" \
  --branches-json '[{"title":"Direct route","charter":"Derive from the stated axioms."}]'
uv run --locked python scripts/new_experiment.py --title "Finite-size scaling diagnostic" --claim C003
uv run --locked python scripts/new_check.py \
  --title "Residual identity" --claim C003 \
  --question "Does the residual of the stated relation vanish identically?" \
  --acceptance-criterion "Exact zero in the declared normal form."
uv run --locked python scripts/run_check.py O001
```

The helpers inspect existing IDs, allocate the next one, instantiate templates, refuse overwrite, and append lightweight provenance. `new_check.py` requires the question and acceptance criterion up front, so the criterion is declared before implementation, and it never creates `result.json`: an obligation with no result file has not run.

`run_check.py` is the only writer of `research/checks/ONNN/result.json`. It executes the declared entrypoint, fingerprints every declared infrastructure file/directory and environment manifest, and derives the canonical outcome from the actual exit status:

```text
exit 0 -> passed
exit 1 -> failed
exit 2 -> inconclusive
anything else, timeout, or a non-executable entrypoint -> error
```

An implementation may print one `##OBSERVATIONS## {...}` line of structured metrics; the wrapper stores it as data and it cannot choose the outcome.

## Independently Verify Only Final Critical Claims

```text
/verify-claim C003
```

Direct invocation is explicit approval for one bounded Opus audit. The director first requires a mature, critical, narrowly frozen claim, settled applicable checks, passing required obligations, stable dependencies, a prior GPT internal critique, complete producer provenance, and a recorded load-bearing/error-risk rationale. It then confirms that `anthropic/claude-opus-5` produced none of the claim or primary evidence. If readiness, approval, provenance, or model separation is missing, no independent audit runs.

The sole verifier is `verifier-anthropic` on `anthropic/claude-opus-5`. It receives a curated packet: the exact claim, originating model IDs, primary evidence, internal critiques, load-bearing obligation spec/result and implementation path, and concise contract, environment, infrastructure, and fingerprint records needed to judge the decisive bridge. Broader paths are escalation references rather than an instruction to audit the repository.

The verifier's task is not to observe that checks passed or reproduce the producer's effort. It identifies the single most load-bearing inference, reconstructs that point by a compact alternate hand argument, and attempts at most three falsification attacks. It inspects only enough implementation and infrastructure to judge whether the representation and acceptance criterion faithfully test that inference. It has no Bash or web access, writes no code, does not rerun obligations or the validator, uses no more than twelve investigative tool calls, and writes one report of at most 2,500 words. If this budget cannot support `verified`, it returns a conservative outcome and recommends at most one next action.

Full reproduction or a clean independent implementation is a separate expensive workflow. Launch it only with explicit user approval after a bounded verifier identifies a concrete need; do not make it an implicit condition of every verification report.

Core producers and the internal critic are pinned to GPT-5.6 Sol; Opus 5 is reserved for independent verification. Actual provenance remains authoritative. Historical or exceptional Opus production makes Opus ineligible for that claim, which must then remain below `verified`; GPT critique cannot substitute for independence.

A different model, preferably from a different provider, is required but not sufficient. Only a genuinely independent `verified` report using alternate reasoning, code, data, or comparably strong checks can support ledger status `verified`; supportive work sharing assumptions or implementations remains below that threshold.

The normal lifecycle is:

```text
hypothesis or broad question
    -> parallel derivation branches
    -> GPT internal critiques
    -> synthesis / pruning / machine checks
    -> supported claim entry
    -> final critical nomination
    -> explicit user approval
    -> Opus independent verifier
    -> verified / inconclusive / contradicted
```

A claim cannot reach `verified` while an active `required: true` obligation targeting it lacks a passing result. That structural gate reflects the project's own declared strategy, not a judgment that the obligations were sufficient. If an obligation turns out to have been misguided, mark it `superseded` and record why; never delete failing history to clear the gate.

Failed verification and failed obligations remain in the repository.

## Inspect State

```text
/research-status
```

This reports the question, exploration portfolio, active hypotheses, internal critiques, claims by status, explicitly nominated final audits, experiments, machine-check obligations, claims blocked by the computational gate, contradictions, and next actions from files. Ordinary `not-requested` independent checks are not reported as verification debt. The equivalent shell commands are:

```bash
uv run --locked python scripts/research_status.py
uv run --locked python scripts/research_status.py --json
uv run --locked python scripts/validate_research_state.py
```

Use `research/STATE.md` as concise durable memory, not a raw lab notebook. Use `research/COMPUTATION.md` as the evolving record of how this project decides what to check by machine, its representation and trust strategy, computational contracts, environment identity, infrastructure tests, scientific validation, and independent cross-checks; it is not an Engineer backlog. Put consequential changes of scope, conventions, methods, substrate, or interpretation in `research/DECISIONS.md`.

Inside OpenCode, use `read` rather than shell `cat`, `research_safe_search`
rather than shell `grep` or `rg`, and typed `research_*` helpers for standard
operations. Generic `uv` and `python` stay approval-gated because command-level
allowlists cannot prevent an interpreter from writing outside a role's artifact
directory.
