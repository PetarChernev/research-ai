# Agent Architecture

```text
User
  |
  v
Research Director
  |-- Literature
  |-- Theorist
  |-- Scientific Computation
  |   `-- Engineer
  `-- Independent Verifier
      |-- Anthropic model
      `-- OpenAI model
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

The producer subagents and two model-bound verifier implementations use closed tool allowlists and scoped write access:

- `literature` writes only bibliography records and source evidence notes.
- `bibliographer` writes only `research/literature/bibliography.bib`, on a deliberately small model, and handles mechanical citation metadata without judging evidence.
- `theorist` writes only derivation artifacts, and exposes candidate machine-checkable obligations from substantial derivations.
- `scientific-computation` chooses the computational representation and trust strategy, defines machine-check semantics and acceptance criteria, writes experiment and claim-specific obligation code, validates reusable infrastructure against the intended mathematics, and runs obligations through the deterministic wrapper. It cannot write `research/checks/**/result.json`.
- `engineer` is a provisioned implementation subagent under `scientific-computation`, not a peer scientific role. It writes only reusable software and tests under `research/computation/` and research-scoped environment definitions under `research/environment/`, from a bounded computational contract. It cannot write claim checks, claims, state, decisions, canonical results, or verification reports.
- `verifier-anthropic` runs `anthropic/claude-sonnet-4-6`, reads source evidence, and writes only verification reports for non-Anthropic work.
- `verifier-openai` runs `openai/gpt-5.6-sol`, reads source evidence, and writes only verification reports for non-OpenAI work.

There is deliberately no separate global agent for symbolic algebra, formal proof, numerical simulation, PDEs, theorem proving, or code review. Those are methods the `scientific-computation` role uses when the research requires them, recorded in `research/COMPUTATION.md`. Adding a global agent per method would multiply roles without adding a materially different scientific operation.

`subagent_depth` is two to permit exactly one nested edge: `research-director -> scientific-computation -> engineer`. Scientific Computation's task allowlist contains only Engineer, and Engineer has `task: deny`. Every other worker remains unable to delegate. The director does not have Engineer in its task allowlist, preserving Scientific Computation's ownership of the contract and handoff. The `bibliographer` remains a director-invoked mechanical helper rather than a nested scientific worker.

Scientific agents deny secret-like files, undeclared tools, and external directories. Non-literature network access and all scientific computation require user approval. `scientific-computation` additionally denies edits to `research/checks/**/result.json`; Engineer cannot edit anything under `research/checks/` at all. These permission rules are guardrails, not a security boundary; the load-bearing architectural constraint is that only `scripts/run_check.py` produces a result file and Scientific Computation authors claim-specific runners. OpenCode permissions in general are operational guardrails rather than an OS sandbox.

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

independent verifier
    -> judges scientific sufficiency

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
        independent verifier evaluates the complete chain
```

## Why a Small Team

A large swarm increases duplicated arguments, hidden dependence, context volume, and fake consensus. Five conceptual scientific roles - director, literature, theorist, scientific computation, verifier - cover the materially different operations; Engineer is bounded implementation support beneath Scientific Computation, and `bibliographer` is a mechanical cost split rather than another scientific voice. Neither adds independent scientific evidence. Adding an agent per computational method remains unnecessary; methods belong in the research plan.

## Claim Integration

Only the director changes the canonical ledger, and its write scope excludes verifier reports. A worker may provide a derivation, observation, source packet, machine-check result, or verification report, but the artifact's existence does not select the claim status automatically. The director uses model-bearing provenance to choose the opposite-provider verifier. The validator applies status-specific evidence predicates and blocks `verified` without a substantive, non-conflicted report that declares a known different-model boundary. Different-model review is necessary but does not replace alternate reasoning, code, or data checks.

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

| Agent | Model | Rationale |
| --- | --- | --- |
| `research-director` | session model (unpinned) | Chosen at launch, so the operator can switch the director without editing files. |
| `theorist` | `openai/gpt-5.6-sol` | Analytical derivation on a provider distinct from the default verifier. |
| `literature` | session model (unpinned) | Source judgment benefits from a strong model; pin if determinism matters. |
| `scientific-computation` | session model (unpinned) | Pin when experiment or obligation authorship requires a fixed model. |
| `engineer` | session model (unpinned) | Implementation support; actual model remains material provenance for infrastructure it creates. |
| `bibliographer` | `anthropic/claude-haiku-4-5` | Mechanical BibTeX formatting and identifier checking; no evidence judgment. |
| `verifier-anthropic` | `anthropic/claude-sonnet-4-6` | Pinned to create a verification model boundary. |
| `verifier-openai` | `openai/gpt-5.6-sol` | Pinned to create a verification model boundary. |

Verifier models are pinned deliberately: they encode a correctness constraint rather than a preference, and their identity is asserted in every report. Both providers therefore need valid credentials. To change a verification model, edit its agent frontmatter and update the documented and reported identity together.

Two consequences follow from heterogeneous producers. First, provenance is no longer uniform, so verifier selection must be made per artifact from recorded model IDs rather than from the director's own model. Second, a producer sharing a model with a verifier makes that verifier ineligible for the affected claim; `theorist` on `openai/gpt-5.6-sol` already excludes `verifier-openai` from verifying theorist-authored work. Keep at least one verifier model unused by any producer so an eligible verifier always exists. With the table above, `anthropic/claude-sonnet-4-6` is reserved for verification only, which guarantees `verifier-anthropic` remains eligible provided the director is not launched on that exact model.

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
    -> independent verification
    -> scheduler selects the next branch
```

No database, queue, or external supervisor is required now. A future orchestrator should call the same scripts and read the same artifacts rather than introduce a second research state.
