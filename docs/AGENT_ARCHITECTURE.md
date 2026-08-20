# Agent Architecture

```text
User
  |
  v
Research Director
  |-- Literature
  |   `-- Bibliographer (small model)
  |-- Theorist
  |-- Numerics
  `-- Verifier
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

The `research-director` is the primary agent. It owns problem decomposition, competing hypotheses, bounded delegation, evidence integration, claim-ledger changes, decisions, and concise state compression.

The producer subagents and two model-bound verifier implementations use closed tool allowlists and scoped write access:

- `literature` writes only bibliography records and source evidence notes.
- `bibliographer` writes only `research/literature/bibliography.bib`, on a deliberately small model, and handles mechanical citation metadata without judging evidence.
- `theorist` writes only derivation artifacts.
- `numerics` writes only experiment directories.
- `verifier-anthropic` runs `anthropic/claude-sonnet-4-6`, reads source evidence, and writes only verification reports for non-Anthropic work.
- `verifier-openai` runs `openai/gpt-5.6-sol`, reads source evidence, and writes only verification reports for non-OpenAI work.

Workers cannot launch subagents. `subagent_depth` is one, and the director's task permission lists only these six configured subagents. This prevents recursive delegation while preserving genuine specialization and independent criticism. The `bibliographer` sits under `literature` conceptually, but the director invokes it directly, since workers cannot delegate.

Scientific agents deny secret-like files, undeclared tools, and external directories. Non-literature network access and all scientific computation require user approval. These controls reduce accidental scope, but OpenCode permissions are operational guardrails rather than an OS sandbox. Built-in OpenCode agents remain available for explicit infrastructure maintenance and are not independent scientific evidence.

## Why a Small Team

A large swarm increases duplicated arguments, hidden dependence, context volume, and fake consensus. Four conceptual roles cover the materially different operations; the verifier role has two provider-specific implementations solely to create a model boundary, and `bibliographer` is a cost split from `literature` rather than a new scientific role. Parallel work is useful only when tasks are separable and evidence streams are genuinely independent. Adding an agent purely to use a different model is not a reason to grow the team; change an existing agent's `model:` field instead.

## Claim Integration

Only the director changes the canonical ledger, and its write scope excludes verifier reports. A worker may provide a derivation, observation, source packet, or verification report, but the artifact's existence does not select the claim status automatically. The director uses model-bearing provenance to choose the opposite-provider verifier. The validator applies status-specific evidence predicates and blocks `verified` without a substantive, non-conflicted report that declares a known different-model boundary. Different-model review is necessary but does not replace alternate reasoning, code, or data checks.

## OpenCode Interfaces

This workspace targets the interfaces verified with OpenCode `1.18.18`:

- Markdown agents in `.opencode/agents/`;
- on-demand skills in `.opencode/skills/<name>/SKILL.md`;
- Markdown slash commands in `.opencode/commands/`;
- named TypeScript tools in `.opencode/tools/` using `@opencode-ai/plugin`;
- auto-discovered project plugins in `.opencode/plugins/`;
- scoped permission patterns and one-level task delegation.

Every agent's model is configured independently in its own file under `.opencode/agents/`, using the `model:` frontmatter field. There is no inheritance requirement: the director may run on one provider while a producer runs on another. An agent with no `model:` field follows the invoking primary model, which is a convenience default rather than a guarantee. Model changes are config-time and take effect only after OpenCode restarts.

Current assignment:

| Agent | Model | Rationale |
| --- | --- | --- |
| `research-director` | session model (unpinned) | Chosen at launch, so the operator can switch the director without editing files. |
| `theorist` | `openai/gpt-5.6-sol` | Analytical derivation on a provider distinct from the default verifier. |
| `literature` | session model (unpinned) | Source judgment benefits from a strong model; pin if determinism matters. |
| `numerics` | session model (unpinned) | Pin when experiment reproducibility requires a fixed model. |
| `bibliographer` | `anthropic/claude-haiku-4-5` | Mechanical BibTeX formatting and identifier checking; no evidence judgment. |
| `verifier-anthropic` | `anthropic/claude-sonnet-4-6` | Pinned to create a verification model boundary. |
| `verifier-openai` | `openai/gpt-5.6-sol` | Pinned to create a verification model boundary. |

Verifier models are pinned deliberately: they encode a correctness constraint rather than a preference, and their identity is asserted in every report. Both providers therefore need valid credentials. To change a verification model, edit its agent frontmatter and update the documented and reported identity together.

Two consequences follow from heterogeneous producers. First, provenance is no longer uniform, so verifier selection must be made per artifact from recorded model IDs rather than from the director's own model. Second, a producer sharing a model with a verifier makes that verifier ineligible for the affected claim; `theorist` on `openai/gpt-5.6-sol` already excludes `verifier-openai` from verifying theorist-authored work. Keep at least one verifier model unused by any producer so an eligible verifier always exists. With the table above, `anthropic/claude-sonnet-4-6` is reserved for verification only, which guarantees `verifier-anthropic` remains eligible provided the director is not launched on that exact model.

## Provenance Plugin

`research-provenance.js` uses the documented `chat.message`, `chat.params`, `command.execute.before`, and `tool.execute.after` hooks. It records agent, provider, and model metadata for research slash commands, research-artifact writes, and experiment commands. It never stores prompt text, arbitrary arguments, file contents, environment values, or tool output. All plugin writes are caught and fail open, so a logging problem cannot block research.

Direct helper scripts and generated experiment runners also write explicit provenance. This keeps the scientific workflow usable even if plugins are disabled with OpenCode's pure mode.

## Future Orchestration

Stable IDs, YAML claims, JSON results, explicit dependencies, and independently runnable experiments form an API for a later scheduler:

```text
external scheduler
    -> research-director session
    -> specialized worker sessions
    -> durable artifacts
    -> independent verification
    -> scheduler selects the next branch
```

No database, queue, or external supervisor is required now. A future orchestrator should call the same scripts and read the same artifacts rather than introduce a second research state.
