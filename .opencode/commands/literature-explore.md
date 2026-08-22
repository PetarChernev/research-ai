---
description: Fan out a bounded creative literature-discovery wave, then validate only its best cross-domain or historical leads before synthesis.
agent: research-director
---

Run one bounded exploratory-literature wave. Optional focus and width supplied
by the user:

<exploration-request>
$ARGUMENTS
</exploration-request>

Use width 4 unless the user requests another value. Accept widths 2 through 8.
This width counts `literature-explorer` discovery branches, not later focused
evaluators.

1. Read `research/QUESTION.md`, `research/STATE.md`, the claim ledger, active hypotheses, and only the primary artifacts needed to extract reliable search anchors and avoid repeating recorded leads. If the question is not initialized, stop and request `/research-start`.
2. Freeze one discovery objective. Build a lens portfolio whose branches differ materially in terminology, historical lineage, mathematical structure, method family, neighboring phenomenon, or distant field. Choose lenses that fit the actual question rather than filling a fixed taxonomy. State exclusions and a bounded stopping condition for each branch.
3. Assign a wave label and a unique, non-existing destination to each branch under `research/literature/explorations/`, using a sortable name such as `<date>-<wave>-<number>-<lens>.md`. Do not let workers choose a shared path.
4. Launch all `literature-explorer` workers as sibling tasks in one parallel batch. Give each the common anchor packet, its distinct lens, exclusions, destination path, expected report sections, and stopping condition. Require candidate-lead language and ask workers not to inspect sibling reports during first pass. Parallel GPT sessions provide breadth, not independent evidence.
5. Wait for the complete discovery barrier. Preserve failed branches and credible negative results. Compare reports for duplicated source chains, terminology overlap, structural specificity, possible project value, known mismatches, and cost of decisive evaluation.
6. Triage rather than validate the reports yourself. Retain at most three high-value leads for immediate evaluation; leave other promising leads explicitly queued in `research/STATE.md`. An exploration report cannot support a claim, literature-supported status, or a research decision by itself.
7. Route each retained lead according to what must be established. Use `literature` for primary-source identity, exact evidence, regime matching, citation lineage, and contradiction search. Use `theorist` for an explicit mathematical or physical dictionary, derivation, limit checks, and a verdict on exact correspondence versus analogy. Use both when adoption depends on both source content and a nontrivial mapping; normally obtain a focused source packet before asking a theorist to rely on source-specific equations.
8. Before launching theorist evaluations, invoke `research_new_derivations` once with every required mapping charter so the `DNNN` paths are preallocated. Give focused literature workers unique source-note destinations. Launch evaluators in parallel only when their inputs and write paths are independent; otherwise respect the source-validation-to-theory dependency.
9. If a resulting derivation is load-bearing for the immediate decision, send the frozen artifact to `internal-critic-openai` for one bounded same-model attack. Do not send exploratory reports themselves to Opus and do not invoke independent verification anywhere in this command.
10. Integrate only evaluated outputs with `research-synthesis`. Preserve whether the result is an exact mapping, a regime-limited analogy, a reusable technique, a rejected resemblance, or still an unevaluated lead. Update claims, decisions, and the working picture only to the extent supported by focused literature notes and/or derivations. Keep report paths and deferred leads in the active exploration portfolio or literature gaps so they remain discoverable.
11. Run `research_validate_state`, fix structural failures, and stop after this wave.

Report the wave label, explorer report paths, useful negative results, leads
promoted or deferred, focused evaluation artifacts, rejected connections, and
the single best next action.
