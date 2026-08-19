---
name: research-synthesis
description: Use to integrate literature, derivations, experiments, and verification reports into a regime-aware research picture while preserving disagreements, dependence, uncertainty, and the next discriminating action.
compatibility: OpenCode 1.18+
metadata:
  domain: research-state
  operation: synthesis
---

# Research Synthesis

## 1. Inventory evidence

Build a table keyed by claim and regime. For each evidence item record type, artifact path or ID, assumptions, result, uncertainty, and status. Exclude unsupported conversational assertions.

## 2. Map dependence

Identify shared equations, datasets, code, priors, approximations, and source chains. Do not count dependent implementations or agents repeating one argument as independent confirmation.

## 3. Align regimes and conventions

Before comparing results, reconcile units, normalization, signs, gauge/coordinates, boundary conditions, approximation order, parameter domain, and observable definitions. Treat unresolved mismatches as contradictions or gaps, not averaging noise.

## 4. Triangulate without laundering

State separately what is derived, numerically observed, literature-supported, reproduced, independently verified, contradicted, or still conjectural. A source supporting a neighboring effect does not support the exact claim.

## 5. Keep disagreement visible

List contradictory artifacts and plausible reasons without choosing a preferred explanation solely for narrative coherence. State what test would discriminate convention mismatch, numerical artifact, regime change, and genuine physical disagreement.

## 6. Update durable state

Summarize the current question, working picture, active hypotheses, highest-value claims, strongest evidence, contradictions, verification tasks, experiments, literature gaps, and next actions in concise `research/STATE.md`. Use the claim-ledger skill for material claim changes and `DECISIONS.md` for consequential direction choices.

## 7. Choose the next action

Rank candidate tasks by expected information gain, cost, independence, and ability to discriminate hypotheses. Prefer a cheap analytic limit or tiny numerical diagnostic before a broad search or expensive run. Stop after a bounded synthesis; do not recurse into an unbounded agent swarm or premature manuscript polishing.
