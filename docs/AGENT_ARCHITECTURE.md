# Agent Architecture

```text
User
  |
  v
Research Director
  |-- Literature
  |-- Theorist
  |-- Numerics
  `-- Verifier
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

The four subagents use closed tool allowlists and scoped write access:

- `literature` writes only bibliography records and source evidence notes.
- `theorist` writes only derivation artifacts.
- `numerics` writes only experiment directories.
- `verifier` reads source evidence but writes only independent verification reports.

Workers cannot launch subagents. `subagent_depth` is one, and the director's task permission lists only these four roles. This prevents recursive delegation while preserving genuine specialization and independent criticism.

Scientific agents deny secret-like files, undeclared tools, and external directories. Non-literature network access and all scientific computation require user approval. These controls reduce accidental scope, but OpenCode permissions are operational guardrails rather than an OS sandbox. Built-in OpenCode agents remain available for explicit infrastructure maintenance and are not independent scientific evidence.

## Why a Small Team

A large swarm increases duplicated arguments, hidden dependence, context volume, and fake consensus. Five roles cover the materially different operations while keeping responsibility clear. Parallel work is useful only when tasks are separable and evidence streams are genuinely independent.

## Claim Integration

Only the director changes the canonical ledger, and its write scope excludes verifier reports. A worker may provide a derivation, observation, source packet, or verification report, but the artifact's existence does not select the claim status automatically. The validator applies status-specific evidence predicates and blocks `verified` without a substantive, non-conflicted independent report. Same-model procedural separation must be disclosed and is insufficient by itself.

## OpenCode Interfaces

This workspace targets the interfaces verified with OpenCode `1.18.18`:

- Markdown agents in `.opencode/agents/`;
- on-demand skills in `.opencode/skills/<name>/SKILL.md`;
- Markdown slash commands in `.opencode/commands/`;
- named TypeScript tools in `.opencode/tools/` using `@opencode-ai/plugin`;
- auto-discovered project plugins in `.opencode/plugins/`;
- scoped permission patterns and one-level task delegation.

No model or provider is selected by the project. The invoking primary model is inherited by subagents unless the user configures otherwise.

## Provenance Plugin

`research-provenance.js` uses the documented `chat.message`, `command.execute.before`, and `tool.execute.after` hooks. It records metadata for research slash commands, research-artifact writes, and experiment commands. It never stores prompt text, arbitrary arguments, file contents, environment values, or tool output. All plugin writes are caught and fail open, so a logging problem cannot block research.

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
