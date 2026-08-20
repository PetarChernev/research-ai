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

## Model Assignment

Each agent's model is configured independently in its file under `.opencode/agents/`. Producer agents do not inherit the director's model, so a single claim may have heterogeneous model provenance. Establish the producing model per artifact rather than assuming it matches the director.

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
2. Theorists propose checkable assertions; `scientific-computation` implements them.
3. Deterministic runners produce canonical machine outcomes. `research/checks/ONNN/result.json` is written only by `scripts/run_check.py`; no result file means the obligation has not run.
4. Independent verifiers judge whether the chosen obligations, methods, assumptions, and outcomes are sufficient for the scientific claim.
5. A passing computation does not automatically verify the scientific claim.
6. Symbolic output is not automatically a proof; it can depend on assumptions, simplification strategy, branch cuts, and representation.
7. Numerical agreement is not a derivation, and sampling is coverage rather than proof.
8. A formal proof establishes only the formalized proposition under its encoded assumptions and axioms.
9. Shared implementations, representations, infrastructure, or assumptions are not independent confirmation.
10. Computational strategy is phase-dependent and must be reconsidered when the research regime changes.
11. Failed and superseded checks remain durable artifacts; never delete failing history to clear a gate.

Directory boundaries:

```text
research/computation/   reusable research-specific methodology and infrastructure
research/checks/        claim-linked executable evidence (ONNN obligations)
research/experiments/   scientific computational experiments (ENNN)
```

A reusable mathematical library is not evidence. A reproducible execution of a declared obligation using that library is evidence. An experiment explores a hypothesis or computes an observable; an obligation tests one declared assertion.

The authority boundary is:

```text
LLMs decide what should be derived, tested, challenged, and implemented.
Deterministic computation establishes the outcome of declared obligations.
Independent verification decides whether those obligations, methods,
assumptions, and outcomes support the scientific claim.
```

## Reproducibility

An important computational result must be reproducible without its originating conversation. Preserve code, parameters, environment information, random seeds, input provenance, the exact command, and the Git commit when available. This applies to symbolic and formal checks as well as numerical runs; a symbolic calculation is still a computation. Do not claim a check was performed unless its artifact records the test and outcome.

## Research Behavior

- Prefer competing hypotheses and tests that discriminate among them.
- Start with analytic estimates or tiny numerical diagnostics before expensive computation.
- Reason about what needs checking, then build the smallest useful executable diagnostic, then stronger machinery only when scientifically justified.
- Bound delegated work, integrate its artifacts, and avoid recursive delegation.
- Give important claims and their originating model IDs to a model-separated verifier with primary artifacts, not an approving summary.
- Do not optimize manuscript prose before core claims are adequately supported.
- An experiment without method, configuration, provenance, and validation is incomplete.
- Never fabricate citations, results, checks, consensus, or verification.

Run `uv run --locked python scripts/validate_research_state.py` after material artifact changes.
