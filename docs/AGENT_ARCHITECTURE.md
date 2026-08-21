# Agent Architecture

```text
User
  |
  v
Research Director
  |-- Literature
  |-- Theorist x N (parallel breadth wave)
  |-- Scientific Computation
  |   `-- Engineer
  |-- GPT Internal Critic x N
  `-- Opus Independent Verifier (late, user-approved)
```

## Three Layers

```text
agent    = who performs work
skill    = how a scientific operation is performed
artifact = persistent evidence or state produced by the work
```

Agents carry stable role boundaries. Skills are loaded on demand so every prompt does not contain every scientific procedure. Artifacts are the durable interface: a worker returns paths and stable IDs, and the director integrates those artifacts rather than relying on a long conversation.

## Roles

The `research-director` is the primary agent. It owns problem decomposition, competing hypotheses, bounded delegation, evidence integration, the computational verification strategy in `research/COMPUTATION.md`, claim-ledger changes, decisions, and concise state compression.

The producer and review roles use closed tool allowlists and scoped write access:

- `literature` writes only bibliography records and source evidence notes.
- `bibliographer` writes only `research/literature/bibliography.bib`, on a deliberately small model, and handles mechanical citation metadata without judging evidence.
- `theorist` writes only derivation artifacts, and exposes candidate machine-checkable obligations from substantial derivations.
- `scientific-computation` chooses the computational representation and trust strategy, defines machine-check semantics and acceptance criteria, writes experiment and claim-specific obligation code, validates reusable infrastructure against the intended mathematics, and runs obligations through the deterministic wrapper. It cannot write `research/checks/**/result.json`.
- `engineer` is a provisioned implementation subagent under `scientific-computation`, not a peer scientific role. It writes only reusable software and tests under `research/computation/` and research-scoped environment definitions under `research/environment/`, from a bounded computational contract. It cannot write claim checks, claims, state, decisions, canonical results, or verification reports.
- `internal-critic-openai` runs `openai/gpt-5.6-sol`, performs fast same-model second-pass attacks, and writes only `research/critiques/`. It is never independent evidence.
- `verifier-anthropic` runs `anthropic/claude-opus-5`, accepts only user-approved final audits, and is the sole writer of independent verification reports.

There is deliberately no separate global agent for symbolic algebra, formal proof, numerical simulation, PDEs, theorem proving, or code review. Those are methods the `scientific-computation` role uses when the research requires them, recorded in `research/COMPUTATION.md`. Adding a global agent per method would multiply roles without adding a materially different scientific operation.

`subagent_depth` is two to permit exactly one nested edge: `research-director -> scientific-computation -> engineer`. Scientific Computation's task allowlist contains only Engineer, and Engineer has `task: deny`. Every other worker remains unable to delegate. The director does not have Engineer in its task allowlist, preserving Scientific Computation's ownership of the contract and handoff. The `bibliographer` remains a director-invoked mechanical helper rather than a nested scientific worker.

Scientific agents deny secret-like files, undeclared tools, and external directories. Built-in `read` and the path-confined `research_safe_search` replace shell `cat`, `grep`, and `rg`; fixed tools cover Git inspection, repository tests, artifact allocation, status, validation, and canonical checks. Generic `uv` and `python` remain approval-gated because any interpreter can bypass edit paths. Reviewers have no Bash or web access. `scientific-computation` additionally denies edits to `research/checks/**/result.json`; Engineer cannot edit anything under `research/checks/` at all. These permissions are guardrails, not an OS sandbox; the load-bearing constraint remains that only `scripts/run_check.py` produces a result file and Scientific Computation authors claim-specific runners.

## Computational Authority Layers

Computation is not a synonym for numerics, and a computation is not self-certifying. The authority chain is:

```text
scientific reasoning
    -> identifies assertions and obligations

scientific computation
    -> selects representation and trust strategy
    -> defines computational contracts
    -> writes claim-specific executable tests

engineer
    -> builds and tests bounded reusable software/environment substrate

deterministic runner
    -> records actual outcomes

GPT internal critic
    -> attacks ordinary reasoning and the claim-to-computation bridge

user-approved Opus verifier
    -> judges independent sufficiency for a final claim

director
    -> integrates evidence and controls claim status
```

The artifact boundary mirrors it:

```text
research/computation/   reusable methodology/infrastructure
research/environment/   research-scoped dependency/runtime definitions
research/checks/        claim-linked executable evidence
research/experiments/   scientific computational experiments
```

A reusable mathematical library is methodology, not evidence. A reproducible execution of a declared obligation using that library is evidence. An experiment explores a hypothesis or computes an observable; an obligation tests one concrete declared assertion against a predeclared acceptance criterion. The same computation may motivate both artifacts.

`scripts/run_check.py` is the only writer of `research/checks/ONNN/result.json`. It derives the outcome from the actual process exit status (`0` passed, `1` failed, `2` inconclusive, anything else an error), records the spec and implementation hashes, deterministically fingerprints declared infrastructure files/directories and research-environment manifests, captures runtime environment, timestamps, Git state, logs, and generated artifacts, and writes the result atomically. An implementation may emit structured observations to stdout; that payload is stored as data and cannot select the outcome. The runner never interprets the physics.

The global architecture does not select SymPy, Cadabra, Lean, Mathematica, Sage, Julia, interval arithmetic, a tensor engine, a PDE solver, an environment manager, or any other tool. Those choices are research output, recorded with their rationale in `research/COMPUTATION.md`. Project-specific machinery lives under `research/computation/`; environment manifests and locks live under `research/environment/`. The root locked environment remains for architecture tooling.

## Representation First

Scientific Computation explicitly assesses the mathematical domain, required operations, exact/canonical representations, equality semantics, encoded assumptions, external trust, existing-library adequacy, custom-kernel risk, and independent checks. Prefer explicit mathematical structure over heuristic symbolic simplification when a compact exact representation or small decidable operation set is practical. Minimize the trusted computational surface by composing conclusion-critical calculations from a small set of explicit, tested primitives where practical.

This does not ban general-purpose CAS software or heuristic simplification. It requires an explicit judgment about whether conclusion-critical equality or transformation depends on opaque heuristic behavior when a clearer exact method is practical.

When reusable mathematical machinery is needed, Scientific Computation freezes a contract covering the domain, coefficient ring, bases/generators, relations, grading/index/orientation/sign conventions, assumptions, normal form, equality, primitive operations, invariants, law tests, invalid inputs, non-goals, and minimum API as relevant. Engineer implements the contract. Engineer-owned infrastructure tests answer "does the software satisfy the contract?" Scientific Computation's research-specific tests answer "does this contract faithfully represent the mathematics needed for the claim?"

## Need-Based Provisioning

Engineer is invoked only when the substrate needs work: a dependency or research environment is absent, compatibility must be established, reusable infrastructure is missing or broken, a custom kernel is justified, reusable solver/formalization support is needed, performance blocks the required calculation, or a verifier raises a material substrate concern. Existing adequate infrastructure and trivial claim-specific coding remain entirely with Scientific Computation.

```text
theorist derives mathematics
        |
scientific computation identifies a machine-checkable obligation
        |
representation assessment
        |
        +-- existing substrate sufficient --> scientific computation writes check
        |
        `-- substrate work required
                |
        scientific computation defines contract
                |
        engineer builds environment/infrastructure and tests it
                |
        scientific computation validates representation and writes check
                |
        deterministic runner executes
                |
        GPT internal critic attacks the chain during convergence
                |
        user-approved Opus verifier audits only a final critical claim
```

## Bounded Breadth, Not Fake Consensus

A permanently unbounded swarm increases duplicated arguments, hidden dependence, and context volume, but a bounded breadth wave is valuable when the solution space is poorly mapped. `/research-explore` preallocates distinct `DNNN` paths, launches a configurable batch of sibling theorists, waits for a first-pass barrier, launches fresh GPT critics, and only then synthesizes and prunes. Diversity comes from distinct assumptions, formalisms, regimes, constructive routes, and falsification strategies, not from repeated GPT votes. Multiple theorists are parallel production capacity, not independent confirmation. Methods still belong in the research plan rather than separate global agents.

## Claim Integration

Only the director changes the canonical ledger, and its write scope excludes internal critiques, canonical check results, and verification reports. A worker may provide a derivation, observation, source packet, machine-check result, critique, or verification report, but existence never selects claim status automatically. Ordinary claims use `checks.independent_verification: not-requested`; `pending` is reserved for a ready, user-approved final audit. The validator blocks `passed` and `verified` without a substantive Opus report and known different-model boundary.

GPT internal critique is the normal second pass and can run across every substantive branch without claiming independence. Opus verification is deliberately much smaller than production. It is absent from start, exploration, and ordinary convergence commands. After explicit approval, the director gives the sole Opus verifier one narrow critical claim, a minimal packet, one decisive reconstruction target, and at most three attacks. Full reproduction and independent implementation remain separately approved workflows.

Ledger schema version 2 records computational evidence directly. `evidence.computational_checks` lists `ONNN` obligations, links are validated in both directions, and `checks.computational_verification` replaces the older numerics-only `numerical_reproduction` field. A structural gate blocks `checks.computational_verification: passed`, and blocks ledger status `verified`, while any active `required: true` obligation targeting the claim lacks a passing result. Superseded obligations remain durable history and do not block the current strategy. That gate is a statement about the project's own declared strategy; whether the obligations are scientifically sufficient remains the verifier's judgment, and a claim with no applicable machine-checkable component can be verified with `computational_verification: not-applicable`.

## OpenCode Interfaces

This workspace targets the interfaces verified with OpenCode `1.18.18`:

- Markdown agents in `.opencode/agents/`;
- on-demand skills in `.opencode/skills/<name>/SKILL.md`;
- Markdown slash commands in `.opencode/commands/`;
- named TypeScript tools in `.opencode/tools/` using `@opencode-ai/plugin`;
- auto-discovered project plugins in `.opencode/plugins/`;
- scoped permission patterns and one bounded two-level delegation path.

Every agent's model is configured independently in its own file under `.opencode/agents/`, using the `model:` frontmatter field. There is no inheritance requirement: the director may run on one provider while a producer runs on another. An agent with no `model:` field follows the invoking primary model, which is a convenience default rather than a guarantee. Model changes are config-time and take effect only after OpenCode restarts.

Current assignment:

| Agent                    | Model                        | Rationale                                                                                       |
| ------------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------- |
| `research-director`      | `openai/gpt-5.6-sol`         | Fixed orchestration and synthesis model; keeps Opus unused by production.                       |
| `theorist`               | `openai/gpt-5.6-sol`         | Analytical derivation on a provider distinct from the default verifier.                         |
| `literature`             | `openai/gpt-5.6-sol`         | Strong source judgment while preserving the reserved Opus boundary.                             |
| `scientific-computation` | `openai/gpt-5.6-sol`         | Fixed authorship for computational semantics and claim-specific checks.                         |
| `engineer`               | `openai/gpt-5.6-sol`         | Fixed implementation provenance for research substrate.                                         |
| `bibliographer`          | `anthropic/claude-haiku-4-5` | Mechanical BibTeX formatting and identifier checking; no evidence judgment.                     |
| `internal-critic-openai` | `openai/gpt-5.6-sol`         | Fast same-model critique; explicitly not independent verification.                              |
| `verifier-anthropic`     | `anthropic/claude-opus-5`    | Pinned to create a verification model boundary.                                                 |

Producer and review models are pinned deliberately. Opus 5 is absent from every producer role and appears only in `verifier-anthropic`; its identity and explicit user approval are asserted in every independent report. To change a model, edit agent frontmatter and update the documented, validated, and reported identity together.

Provenance remains authoritative even with pinned roles. If historical or exceptional work used `anthropic/claude-opus-5` materially, Opus is ineligible for that claim and GPT internal review cannot substitute for independence. Otherwise the fixed assignments preserve a clear model boundary while retaining actual producer IDs for every artifact and computational substrate.

Computational evidence does not relax any of this. Deterministic execution removes the model from the *outcome*, not from the *design or implementation*: the assertion, representation, encoded assumptions, acceptance criterion, environment, and reusable kernel were still authored by models. Treat Scientific Computation and every material Engineer model as originating provenance for supported claims. Engineer does not need to be model-separated from the theorist, but its contribution can make a verifier model ineligible and can create correlated implementation risk.

## Provenance Plugin

`research-provenance.js` uses the documented `chat.message`, `chat.params`, `command.execute.before`, and `tool.execute.after` hooks. It records agent, provider, and model metadata for research slash commands, infrastructure/environment writes, experiment commands, machine-check commands, and Engineer provisioning. Engineer provisioning records Scientific Computation as the parent agent, `delegated_agent: engineer`, and an associated obligation ID when one appears in the bounded task. Child writes carry Engineer's actual session model. It never stores prompt text, arbitrary arguments, file contents, environment values, or tool output. All plugin writes are caught and fail open, so a logging problem cannot block research.

Direct helper scripts, generated experiment runners, and `scripts/run_check.py` also write explicit provenance. This keeps the scientific workflow usable even if plugins are disabled with OpenCode's pure mode.

## Future Orchestration

Stable IDs, YAML claims, JSON results, explicit dependencies, independently runnable experiments, and deterministically executed machine-check obligations form an API for a later scheduler:

```text
external scheduler
    -> research-director session
    -> specialized worker sessions
    -> durable artifacts
    -> GPT internal critique
    -> rare user-approved Opus verification
    -> scheduler selects the next branch
```

No database, queue, or external supervisor is required now. A future orchestrator should call the same scripts and read the same artifacts rather than introduce a second research state.
