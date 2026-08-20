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

Build a table keyed by claim and regime. For each evidence item record type, artifact path or ID, assumptions, result, uncertainty, and status. Include machine-check obligations (`ONNN`) alongside derivations, experiments, literature notes, and verification reports. For an obligation, record the declared question, encoded assumptions, predeclared acceptance criterion, and the outcome actually recorded in `research/checks/ONNN/result.json` — not the outcome someone expected. An obligation with no result has not run.

## 2. Map dependence

Identify shared equations, datasets, code, priors, approximations, and source chains. Do not count dependent implementations or agents repeating one argument as independent confirmation. Two obligations sharing a module from `research/computation/`, a representation, or an encoded convention share failure modes and are not independent evidence.

## 3. Align regimes and conventions

Before comparing results, reconcile units, normalization, signs, gauge/coordinates, boundary conditions, approximation order, parameter domain, and observable definitions. Treat unresolved mismatches as contradictions or gaps, not averaging noise.

## 4. Triangulate without laundering

State separately what is derived, numerically observed, literature-supported, machine-checked, reproduced, independently verified, contradicted, or still conjectural. A source supporting a neighboring effect does not support the exact claim.

A passed obligation is evidence for its declared assertion under its encoded assumptions; it does not promote a claim by itself. Symbolic output is not automatically a proof, numerical agreement is not a derivation, and a formal proof establishes only the formalized proposition. Failed and inconclusive obligations belong in the synthesis with the same weight as passing ones.

## 5. Keep disagreement visible

List contradictory artifacts and plausible reasons without choosing a preferred explanation solely for narrative coherence. State what test would discriminate convention mismatch, numerical artifact, regime change, and genuine physical disagreement.

## 6. Update durable state

Summarize the current question, working picture, active hypotheses, highest-value claims, strongest evidence, contradictions, verification tasks, experiments, literature gaps, and next actions in concise `research/STATE.md`. Use the claim-ledger skill for material claim changes and `DECISIONS.md` for consequential direction choices. Update `research/COMPUTATION.md` when the synthesis shows that the representations, methods, evidence standards, independence needs, or research phase have materially changed.

## 7. Choose the next action

Rank candidate tasks by expected information gain, cost, independence, and ability to discriminate hypotheses. Prefer a cheap analytic limit or the smallest useful executable diagnostic before a broad search, heavy machinery, or an expensive run. Stop after a bounded synthesis; do not recurse into an unbounded agent swarm or premature manuscript polishing.
