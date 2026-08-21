# Scientific Research Repository

OpenCode is the execution layer for this physics workspace. The durable interface between agents is the repository, not accumulated chat history.

## Durable Artifacts

Record important conclusions in files:

- `research/QUESTION.md`: current scientific problem and scope
- `research/STATE.md`: concise current status and next actions
- `research/COMPUTATION.md`: research-specific computational verification strategy
- `research/hypotheses/`: explicit competing hypotheses (`HNNN`)
- `research/claims/ledger.yaml`: canonical claim registry (`CNNN`)
- `research/derivations/`: auditable derivations (`DNNN`)
- `research/experiments/`: reproducible calculations (`ENNN`)
- `research/checks/`: claim-linked machine-check obligations (`ONNN`)
- `research/computation/`: reusable research-specific computational machinery
- `research/environment/`: research-scoped environment manifests, locks, and setup records
- `research/literature/notes/`: source-specific evidence packets
- `research/results/`: validated consolidated results and verification reports
- `research/DECISIONS.md`: consequential research-direction choices

Do not leave an important result only in conversation. Link evidence by stable ID or repository-relative path. Material evidence changes require corresponding ledger and state updates.

## Epistemic Discipline

Label statements as one of: assumption, conjecture, derived result, numerical observation, literature-supported result, reproduced result, verified result, or contradicted result. Never silently promote between categories.

- A numerical fit is not a derivation.
- Symbolic output is not automatically a proof.
- A citation is evidence only when the source supports the exact claim in the stated regime.
- Repetition of one argument by several agents is not independent confirmation.
- Agreement between implementations sharing assumptions or code is not independent verification.
- A separate agent session using the same model is procedural separation, not independence by itself.
- Route verification to a model that did not materially produce the claim or its primary evidence, preferring a different provider, and record both sides of that model boundary.
- Keep material assumptions and unresolved contradictions visible.

Use `verified` only after an independent verifier has reconstructed or attacked the claim by an alternate method or comparably strong independent check and a substantive report is linked from the ledger. Failed verification remains part of the record.

Verification is a bounded adversarial audit, not a duplicate production stream. Most intermediate claims should remain below `verified`; reserve model-separated review for narrow claims whose verification changes an immediate decision or unlocks a conclusion. The default verifier reconstructs one load-bearing inference, attempts at most three decisive attacks, reviews only the computational paths needed to judge the claim-to-representation bridge, writes no code, and does not rerun obligations. Full reproduction or an independent implementation is a separate exceptional task requiring explicit user approval.

## Model Assignment

Each agent's model is configured independently in its file under `.opencode/agents/`, but an unpinned role may use the invoking session model. A single claim may therefore have heterogeneous or shared model provenance. Establish the actual producing model per artifact rather than inferring it from hierarchy. Engineer-authored environments and reusable infrastructure count as material production when they support a claim.

One constraint is hard: a claim may reach `verified` only through a verifier whose model is absent from every model that materially produced the claim or its primary evidence. A different provider is preferred and recorded, but only the model-level separation is mandatory. Choosing models for cost or capability is otherwise free, including a deliberately small model for mechanical work such as citation metadata.

Keep at least one verifier model unused by any producer agent, so an eligible verifier always exists. When no eligible verifier remains, leave the claim below `verified` and reassign a model rather than routing the check anyway.

## Physics Checks

For important theoretical results, check where relevant:

- dimensions and units;
- signs, normalization, and factors such as 2, pi, hbar, c, and k_B;
- symmetries, conservation laws, and gauge or coordinate dependence;
- limiting and exactly soluble cases;
- perturbative order and asymptotic domain;
- boundary and initial conditions.

For important numerical results, check where relevant:

- convergence and solver tolerance;
- discretization, finite-size, and timestep dependence;
- precision and random-seed dependence;
- initial-condition and parameter sensitivity;
- analytically known limits;
- an independent implementation when warranted.

## Computational Evidence

The architecture prescribes the process for designing computational evidence, not the methods themselves. Which symbolic, formal, exact, numerical, or bespoke method suits a problem is a research output, recorded in `research/COMPUTATION.md`, not a global rule.

1. Important claims should expose machine-checkable obligations where scientifically useful, and should explicitly record where they cannot.
2. Theorists derive mathematics and expose checkable assertions. `scientific-computation` defines machine-check semantics, chooses the representation and trust strategy, and writes claim-specific obligation code.
3. When the reusable software or research environment needs work, `scientific-computation` supplies a bounded computational contract and provisions `engineer`. Engineer verifies that software satisfies the contract but has no scientific or verification authority.
4. Deterministic runners produce canonical machine outcomes. `research/checks/ONNN/result.json` is written only by `scripts/run_check.py`; no result file means the obligation has not run.
5. Independent verifiers judge whether the reasoning, representation, implementation, obligations, assumptions, and outcomes are sufficient for the scientific claim.
6. A passing computation does not automatically verify the scientific claim.
7. Prefer explicit mathematical structure over heuristic symbolic simplification when a compact exact representation or small decidable operation set is practical. General-purpose CAS software remains allowed when justified.
8. Minimize the trusted computational surface: conclusion-critical calculations should compose a small set of explicit, tested primitives where practical.
9. Symbolic output is not automatically a proof; it can depend on assumptions, simplification strategy, branch cuts, and representation.
10. Numerical agreement is not a derivation, and sampling is coverage rather than proof.
11. A formal proof establishes only the formalized proposition under its encoded assumptions and axioms.
12. Shared implementations, representations, infrastructure, environments, or assumptions are not independent confirmation.
13. Computational strategy is phase-dependent and must be reconsidered when the research regime changes.
14. Failed and superseded checks remain durable artifacts; never delete failing history to clear a gate.

Directory boundaries:

```text
research/computation/   reusable research-specific methodology and infrastructure
research/environment/   research-scoped dependency and runtime definitions
research/checks/        claim-linked executable evidence (ONNN obligations)
research/experiments/   scientific computational experiments (ENNN)
```

A reusable mathematical library is not evidence. A reproducible execution of a declared obligation using that library is evidence. An experiment explores a hypothesis or computes an observable; an obligation tests one declared assertion.

The authority boundary is:

```text
LLMs decide what should be derived, tested, challenged, and implemented.
Scientific Computation owns computational semantics and claim-specific checks.
Engineer supplies bounded, contract-driven software and environment support.
Deterministic computation establishes the outcome of declared obligations.
Independent verification decides whether those obligations, methods,
assumptions, and outcomes support the scientific claim.
```

## Reproducibility

An important computational result must be reproducible without its originating conversation. Preserve code, parameters, research-environment manifests or locks, package and external executable versions, declared infrastructure fingerprints, infrastructure test commands and outcomes, random seeds, input provenance, the exact command, and the Git commit when available. This applies to symbolic and formal checks as well as numerical runs; a symbolic calculation is still a computation. Do not claim a check was performed unless its artifact records the test and outcome.

## Research Behavior

- Prefer competing hypotheses and tests that discriminate among them.
- Start with analytic estimates or tiny numerical diagnostics before expensive computation.
- Reason about what needs checking, then build the smallest useful executable diagnostic, then stronger machinery only when scientifically justified.
- Bound delegated work and integrate its artifacts. The only nested edge is `scientific-computation -> engineer` for a declared substrate task; Engineer cannot delegate.
- Give narrow, gate-critical claims and their originating model IDs to a model-separated verifier through a curated primary-artifact packet, not an approving summary or an exhaustive repository assignment.
- Do not optimize manuscript prose before core claims are adequately supported.
- An experiment without method, configuration, provenance, and validation is incomplete.
- Never fabricate citations, results, checks, consensus, or verification.

Run `uv run --locked python scripts/validate_research_state.py` after material artifact changes.
