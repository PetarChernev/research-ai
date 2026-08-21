Use the following as the task prompt for the research director. It is designed as a **one-time migration and revalidation pass**, not a new research cycle.

# Full Migration and Revalidation Pass for Existing Research

The research branch has now been merged with the new computational-verification architecture from `main`.

Perform a **complete update pass over all research already conducted in this repository** so that the current research state honestly conforms to the new architecture while preserving all prior scientific work and provenance.

This is primarily a **research-state migration, computational-verification design, and revalidation task**. Do not discard or gratuitously redo existing reasoning. Do not begin a new forward research workstream until the existing research state has been migrated and its current evidential status is clear.

The goal is:

> Preserve all prior hypotheses, derivations, experiments, literature work, decisions, verification reports, and provenance as historical scientific evidence, while reassessing the current claim ledger under the new computational-verification procedure and adding appropriate machine-checkable evidence for the work already done.

A change in status caused solely by the stronger architecture is **not a contradiction of the earlier science**. Make that distinction explicit.

---

# 1. Begin with a complete repository audit

Read the current versions of at least:

```text
AGENTS.md
docs/RESEARCH_WORKFLOW.md
docs/AGENT_ARCHITECTURE.md
docs/REPRODUCIBILITY.md

research/QUESTION.md
research/STATE.md
research/COMPUTATION.md
research/DECISIONS.md

research/claims/ledger.yaml
research/hypotheses/**
research/derivations/**
research/experiments/**
research/literature/**
research/results/**
research/provenance.jsonl
```

Also inspect:

```text
research/computation/
research/checks/
```

and the new computational-verification skill, check templates, runner, and validator.

Establish:

1. every current claim and its status;
2. which derivation(s) support each claim;
3. which prior verification reports exist;
4. which claims are load-bearing for later work;
5. which old checks were analytical, numerical, or merely prose assertions;
6. which parts of each claim are now meaningfully machine-checkable;
7. which claims have no useful machine-checkable component;
8. which current ledger fields became stale or semantically invalid after the architecture merge.

Do not infer that old work satisfies a new field merely because an analogous old field existed.

In particular, do not mechanically map an old numerical-reproduction status to the new general `computational_verification` field.

---

# 2. Preserve historical scientific artifacts

Treat all pre-migration scientific artifacts as durable historical evidence.

Do not rewrite old derivations merely to make them look as though they were produced under the new architecture.

Do not alter old verification reports to imply they reviewed computational obligations that did not yet exist.

Do not delete failed, superseded, incomplete, or now-insufficient evidence.

Preserve:

* derivations;
* hypotheses;
* literature packets;
* experiments;
* previous verification reports;
* decisions;
* provenance;
* original producing/verifying model information.

Small corrections required for broken repository references or schema compatibility are acceptable, but do not silently change scientific content.

If an existing derivation requires substantive correction, create a new derivation or explicit revision artifact according to the normal research procedure rather than rewriting history.

---

# 3. Record the architecture migration as a research decision

Add an explicit entry to:

```text
research/DECISIONS.md
```

recording that the research has adopted the new computational-verification architecture.

The decision must state, in substance:

* prior scientific artifacts remain valid historical evidence;
* prior claims are not assumed to satisfy newly introduced computational-verification requirements retroactively;
* current epistemic status will be reassessed conservatively;
* machine-check obligations will be assigned to existing claims where scientifically appropriate;
* previous independent verification remains evidence but does not automatically satisfy the new end-to-end procedure if the verifier never reviewed the newly required computational evidence;
* status downgrades caused by this migration indicate stronger evidence requirements, not newly discovered counterevidence.

Include the relevant Git/architecture transition in provenance if the repository convention supports it.

---

# 4. Construct the research-specific computational strategy

Populate or comprehensively revise:

```text
research/COMPUTATION.md
```

based on the actual mathematics already present in the research repository.

Do not use generic architecture boilerplate as a substitute for scientific judgment.

For the existing research, determine:

## Current research phase

Describe where the project actually is now and what mathematical structures dominate the work already completed.

## Checkability map

For every conclusion-relevant existing claim, classify its important components as one or more of:

* directly machine-checkable now;
* machine-checkable after implementing research-specific infrastructure;
* suitable mainly for numerical evidence;
* suitable for exact symbolic evidence;
* suitable for formal proof if justified;
* primarily conceptual and not usefully machine-checkable;
* requiring independent implementation;
* requiring an explicit counterexample or witness.

Do not force every claim into machine computation.

## Current obligations

Identify the concrete executable obligations warranted by the existing claims and derivations.

## Representations and methods

Decide which representations and computational methods are appropriate to this research.

These choices are scientific outputs.

Do not select a package merely because the global architecture mentions that such packages may exist.

## Research-specific infrastructure

Identify any bespoke mathematical machinery that should live in:

```text
research/computation/
```

For example, if the existing derivations require exact manipulation of structures inadequately represented by off-the-shelf tools, specify and justify the custom infrastructure needed.

## Evidence standards

For each relevant type of computation, state what would count as:

```text
pass
fail
inconclusive
```

and distinguish exact evidence from numerical diagnostics.

## Independence strategy

Identify where a second algorithm, independent implementation, alternate mathematical representation, or different computational method is warranted.

## Phase-transition triggers

Record how the computational methodology should change when the scientific research enters a materially different regime.

This is particularly important if later work will involve mathematical objects substantially different from those dominating the current derivations.

---

# 5. Migrate the claim ledger conservatively

Bring:

```text
research/claims/ledger.yaml
```

fully into the current schema.

For every claim:

* preserve claim wording unless a genuine scientific revision is required;
* preserve assumptions and regime;
* preserve links to derivations;
* preserve literature evidence;
* preserve experiments;
* preserve old verification reports;
* initialize and populate `evidence.computational_checks`;
* populate the new check fields according to evidence actually earned.

Do not preserve `verified` merely for historical convenience if the current architecture's requirements for `verified` have not been satisfied.

Likewise, do not label computational verification `not-applicable` merely to avoid performing a check.

`not-applicable` must itself reflect an explicit scientific judgment that the claim has no meaningful machine-checkable component.

### Previously verified claims

For any claim that was `verified` under the old procedure:

1. retain all old verification reports as evidence;
2. determine whether the claim now has applicable computational obligations;
3. if applicable obligations have not yet passed and been reviewed under the current procedure, move the claim to the strongest current status it actually deserves;
4. set current independent-verification state conservatively if a fresh verifier still needs to review newly generated computational evidence.

This is not a repudiation of the old verification report.

Document the distinction between:

```text
historically independently supported
```

and:

```text
verified under the current procedure
```

### Previously derived claims

Keep valid derivations as `derived` unless new evidence warrants another state.

Do not demote a sound derivation to conjecture simply because computational verification is pending.

### Contradictions

Only use `contradicted` if new scientific evidence actually contradicts the claim.

Architecture migration by itself is never a contradiction.

---

# 6. Create machine-check obligations for existing work

For each existing conclusion-critical claim with a meaningful machine-checkable component, instantiate explicit `ONNN` obligations using the new helper/tool.

Do not manually choose obligation IDs.

Do not create obligations merely for ceremony.

Each obligation must correspond to a concrete mathematical assertion, not a vague instruction such as:

```text
check the derivation
```

Instead specify questions of the form:

```text
Does expression A reduce exactly to expression B under assumptions X?

Does the proposed solution give a zero equation residual?

Does this linear map have the claimed rank?

Does this variation produce the claimed boundary term?

Does the claimed symmetry transformation leave the relevant object invariant?

Does a stated limiting case reproduce the claimed result?

Does a proposed counterexample give a demonstrably nonzero witness?

Does an approximation exhibit the declared remainder order?
```

The actual obligations must follow from the existing research, not from this prompt.

For every obligation:

* link the target claim(s);
* link relevant derivation(s);
* state assumptions explicitly;
* predeclare the acceptance criterion;
* justify the chosen computational method;
* state independence requirements;
* identify reusable research-specific infrastructure if needed.

An obligation created during this migration is a **new test of an existing result**.

Do not backdate it or imply it was part of the original derivation.

---

# 7. Prioritize obligations by scientific dependency

Do not mechanically verify the research in chronological order.

Construct the dependency graph of current claims and identify which existing results are load-bearing for:

* the present research state;
* unresolved discriminators;
* upcoming work;
* downstream claims.

Prioritize computational revalidation of those claims first.

Older peripheral claims can remain correctly labeled with pending obligations while the critical dependency chain is addressed.

However, this is a **full update pass**, so before finishing the migration every existing important claim must at least have:

* an explicit checkability assessment;
* appropriate obligation links if applicable;
* a truthful current status;
* an explicit reason if no machine check is applicable.

---

# 8. Implement research-specific computational infrastructure

Delegate appropriate work to `scientific-computation`.

Any reusable machinery motivated by the existing research belongs under:

```text
research/computation/
```

Examples may include domain-specific exact algebra, symbolic transformations, specialized numerical methods, formal representations, or testing utilities.

Choose these methods from the actual requirements of the research.

Do not implement unnecessarily general infrastructure.

Prefer:

```text
smallest scientifically adequate representation
    ->
tests of the representation itself
    ->
claim-specific executable obligation
```

over building a large symbolic framework preemptively.

Document:

* conventions;
* assumptions;
* representation choices;
* known limitations;
* tests of the infrastructure;
* which obligations depend on it.

If an off-the-shelf library is sufficient and trustworthy for the required operation, use it rather than implementing custom code without reason.

If a custom implementation is scientifically safer, record why.

---

# 9. Execute obligations only through the deterministic runner

The scientific-computation agent may implement checks.

It may not fabricate canonical results.

Run every obligation through:

```text
research_run_check
```

or the corresponding deterministic repository wrapper.

Canonical `result.json` files must come from actual execution.

Preserve:

* passes;
* failures;
* inconclusive results;
* errors;
* logs;
* observations;
* hashes;
* environment;
* commands;
* Git state;
* generated artifacts.

Never edit a failed result into a pass.

If an implementation bug is found:

1. fix the implementation;
2. rerun through the deterministic runner;
3. preserve provenance/history according to repository conventions.

If a scientific obligation itself was poorly designed, supersede it rather than silently changing its meaning.

---

# 10. Treat computational infrastructure as an object of verification

Do not assume that because a script runs, its mathematical representation is correct.

For newly created research-specific infrastructure, perform suitable self-tests where feasible.

Examples include:

* identities known analytically;
* canonical sign tests;
* round-trip transformations;
* simple exactly soluble cases;
* comparison with an independent implementation;
* randomized regression tests;
* dimension/rank sanity checks.

These infrastructure tests support confidence in later obligation results but do not replace claim-specific obligations.

Record limitations explicitly.

---

# 11. Revalidate existing high-value claims under the new procedure

Once applicable computational obligations have been executed, route claims requiring current verification to an eligible independent verifier under the existing model-separation rules.

The fresh verifier must receive the primary evidence, including:

* frozen claim;
* assumptions/regime;
* original derivation(s);
* relevant prior verification reports as historical evidence;
* current `COMPUTATION.md`;
* obligation specifications;
* implementations;
* machine-generated results;
* relevant research-specific computational infrastructure;
* provenance/model information.

The verifier must independently judge:

1. whether the original reasoning is sound;
2. whether the declared machine checks actually test the relevant assertions;
3. whether computational assumptions match scientific assumptions;
4. whether the representations are faithful;
5. whether acceptance criteria are strong enough;
6. whether important failure modes remain untested;
7. whether code/method dependence requires an alternate implementation;
8. whether a passing check proves only a narrower proposition than the claim;
9. whether additional adversarial obligations are warranted.

If the verifier requests additional machine checks:

```text
instantiate obligation
    ->
implement
    ->
execute deterministically
    ->
return new results to verifier
```

Do not replace this with prose-only reasoning.

Only restore or assign `verified` after the current architecture's conditions are genuinely satisfied.

Append new verification reports; do not replace old reports.

---

# 12. Do not require computational evidence where it adds no epistemic value

The new architecture is intended to strengthen research, not create bureaucracy.

If a claim is genuinely conceptual and no meaningful executable test exists:

* document this in `COMPUTATION.md`;
* set `computational_verification: not-applicable` only when justified;
* let the independent verifier scrutinize that judgment;
* rely on the strongest relevant analytic, literature, formal, or conceptual evidence.

Do not manufacture meaningless numerical examples simply to produce a passing machine artifact.

---

# 13. Update `STATE.md` after the migration

Rewrite the current state summary so it accurately distinguishes among:

* verified under the current procedure;
* previously independently supported but pending current-procedure revalidation;
* derived with computational verification pending;
* contradicted;
* conjectural;
* blocked by a failed or inconclusive required obligation.

Explicitly state that any status changes caused solely by adoption of the new architecture represent **changed evidence standards rather than new scientific counterevidence**.

Update the next-action list according to the actual dependency graph and the outcome of the migration.

Do not erase the previously identified scientific direction merely because migration work was performed.

---

# 14. Update claim and computation links consistently

After obligations and fresh reports have been created, ensure bidirectional consistency among:

```text
claim ledger
derivations
experiments
ONNN obligations
result.json files
verification reports
COMPUTATION.md
STATE.md
DECISIONS.md
provenance
```

Every active obligation targeting a claim must be represented in the ledger.

Every computational check listed by a claim must exist and target that claim.

Do not leave stale paths or IDs.

---

# 15. Preserve the distinction between exploratory use and verified dependency

Existing derived claims may continue to guide research before full computational revalidation is complete.

Do not treat migration as requiring every prior result to become verified before any thinking can continue.

Instead, when later work depends on an incompletely revalidated result, make that dependency explicit.

For example:

```text
depends on Cxxx:
status = derived
computational revalidation = pending
```

This allows research to continue without laundering uncertainty.

However, do not promote downstream results to stronger epistemic states than their unresolved load-bearing dependencies justify.

---

# 16. Do not redo completed work without a reason

The purpose of this pass is to add stronger evidence and clearer epistemic accounting.

Do not ask the theorist to independently reproduce every old derivation from zero merely because the architecture changed.

Redo or revise an old derivation only if:

* a machine check fails;
* the verifier identifies a substantive gap;
* assumptions were underspecified;
* the original derivation is not auditable enough to formulate a meaningful obligation;
* the research has genuinely changed the claim.

Otherwise treat the existing derivation as the object being tested.

---

# 17. Distinguish exact checks from numerical diagnostics

When designing obligations, explicitly classify the strength of the evidence.

Where an exact mathematical result can be checked exactly, prefer exact computation over floating-point agreement.

Numerical sampling may be useful for:

* adversarial bug finding;
* regression testing;
* edge-case discovery;
* exploring regimes;
* checking conjectured behavior.

Do not label finite numerical sampling as a proof of a universal identity.

Where numerical evidence is conclusion-critical, establish research-specific standards for:

* convergence;
* tolerance;
* precision;
* seed dependence;
* discretization dependence;
* parameter sensitivity;
* independently known limits;
* independent implementation when warranted.

---

# 18. Reassess the computation strategy at the current frontier

After migrating the existing work, identify whether the mathematical character of the **next planned research step** differs enough that `COMPUTATION.md` should define a new computational regime.

Do not perform the new forward research itself as part of this migration unless a minimal calculation is required to decide the methodology.

Instead, record:

* what new types of objects will appear;
* what new machine evidence will become relevant;
* what existing infrastructure may stop being sufficient;
* what triggers should cause the director to instantiate a new class of obligations.

This ensures the next ordinary `/research-cycle` begins with an appropriate computational strategy.

---

# 19. Run full repository validation

Before declaring the migration complete:

1. run all relevant computational obligations intended for this pass;
2. run the repository test suite if changes were made to project-local computational infrastructure;
3. run:

```bash
uv run --locked python scripts/validate_research_state.py
```

4. run the strict validator mode if supported;
5. run the research-status report;
6. inspect all reported computational blockers;
7. resolve structural inconsistencies;
8. inspect `git diff`;
9. confirm no old scientific artifact was silently rewritten;
10. confirm failed/inconclusive obligations remain visible;
11. confirm ledger statuses correspond to evidence actually earned.

Do not weaken validation rules to make legacy research pass.

Migrate the research instead.

---

# 20. Deliverable

At the end of the pass, provide a concise migration report containing:

## Research artifacts preserved

Summarize prior derivations, reports, experiments, and other evidence retained unchanged.

## Ledger migration

List every claim whose current status or check state changed and explain why.

Distinguish:

```text
architecture-driven status change
```

from:

```text
scientific-evidence-driven status change
```

## Computational strategy

Summarize the contents and major decisions in:

```text
research/COMPUTATION.md
```

## Obligations created

For every new `ONNN`, report:

* target claim(s);
* target derivation(s);
* mathematical question;
* method;
* required/optional;
* outcome;
* relevant implementation/infrastructure.

## Infrastructure added

Describe any new files under:

```text
research/computation/
```

and why they were necessary.

## Verification

Report:

* which claims received fresh independent verification;
* which regained or newly earned `verified`;
* which remain `derived`;
* which remain pending computational evidence;
* which are blocked by failed/inconclusive checks;
* any genuine contradictions discovered.

## Remaining migration debt

List any existing claim whose new-procedure revalidation is intentionally deferred and why.

## Current frontier

State the scientifically highest-value next research action once this migration is complete.

---

# Governing principle

Perform this pass according to the following distinction:

```text
The old artifacts record what was previously reasoned and observed.

The migrated ledger records what the repository is currently entitled
to claim under the stronger evidence procedure.

New machine checks test the old work; they do not erase it.

Fresh independent verification judges the old reasoning together with
the new computational evidence.

Only genuine scientific counterevidence constitutes a contradiction.
```

Do the migration and revalidation work now. Do not stop after producing a plan.
> Legacy migration prompt. It is not loaded by `opencode.json` and predates the
> breadth-first exploration, GPT internal-critique, and user-approved Opus-only
> verification architecture. Follow `AGENTS.md` and `.opencode/commands/` for
> current research behavior.
