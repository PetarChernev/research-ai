# Computational Verification Strategy

Status: {{STATUS}}
Last updated: {{DATE}}

Research question: {{QUESTION}}

This artifact is the research program's own methodology record, owned by the
research director. The global architecture prescribes where computational
evidence lives, how it is executed, and how it is judged; it does not prescribe
which mathematics, representations, libraries, or tools this project should use.
Those are research decisions and belong here. Revise this plan whenever the
research enters a new mathematical or physical regime; it is not static
configuration.

## Current research phase

{{PHASE}}

Describe the current methodological regime in this project's own terms: what
kind of object is being studied, what is already settled, what is being
established now, and what class of reasoning currently dominates. Do not adopt a
generic phase taxonomy that does not fit the problem.

## Checkability map

List the important claims and derivations, and for each state which aspects are:

- machine-checkable now;
- potentially machine-checkable with additional infrastructure;
- primarily conceptual or not usefully machine-checkable.

Recording that something is not usefully machine-checkable is a legitimate and
valuable entry. Do not manufacture a check for an assertion that a check cannot
discriminate.

## Current machine-check obligations

Summarize the active claim-linked executable obligations (`ONNN`), what each one
tests, and its current recorded outcome. Keep superseded obligations visible with
the reason they were superseded. This section is a scientific summary; the
canonical machine outcome is `research/checks/ONNN/result.json`.

## Computational representations and methods

Record the representations and methods this research has chosen, and why: for
example exact rational or algebraic arithmetic, symbolic manipulation, interval
or ball arithmetic, arbitrary-precision floating point, numerical integration or
linear algebra, discretization schemes, proof assistants, model checkers,
property-based sampling, or bespoke machinery. Record convention choices that the
representation encodes, since a faithful-looking encoding can silently change the
mathematical statement.

## Research-specific computational infrastructure

Document reusable machinery under `research/computation/`: what it is, why it
exists, which obligations depend on it, how it is tested, and what its known
representational limitations are. A reusable library is methodology, not
evidence.

## Numerical and formal evidence standards

Record this project's acceptance standards: precision, working tolerance,
residual norms, convergence rates and refinement ladders, sample sizes, rigor
level (heuristic, controlled-error, or proof-level), what counts as an exact
result, and what a formal statement must include to be relevant. State thresholds
before running, not after seeing output.

## Independence strategy

State when a second implementation, algorithm, library, language, or method is
required rather than merely nice to have, and what would actually make it
independent. Two runners sharing a representation, a helper module, or the same
encoded assumption are not independent.

## Phase-transition triggers

State the concrete changes that would require reconsidering this plan: a new
class of object, a change of regime or limit, a failed obligation that
invalidates a representation, a discovered convention error, a claim promoted to
conclusion-critical, or a method reaching its accuracy or rigor ceiling.

## Deferred or non-machine-checkable issues

Keep important unformalized, deferred, or currently non-computable reasoning
visible here so it is not lost simply because it cannot be executed.

## Known limitations and risks

Include limitations of the chosen representations and tools themselves:
simplification and normal-form assumptions, branch-cut and domain handling,
floating-point and cancellation error, sampling coverage, solver stability,
proof-assistant axioms and encodings, version dependence, and the gap between the
formalized or discretized statement and the scientific claim.

## Related decisions

Link consequential methodological choices to entries in
`research/DECISIONS.md`.
