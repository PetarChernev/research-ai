# Computational Verification Strategy

Status: not-started
Last updated: not-started

Research question: Not set. Run `/research-start <physics question>`.

This artifact is the research program's own methodology record, owned by the
research director. The global architecture prescribes where computational
evidence lives, how it is executed, and how it is judged; it does not prescribe
which mathematics, representations, libraries, or tools this project should use.
Those are research decisions and belong here. Revise this plan whenever the
research enters a new mathematical or physical regime; it is not static
configuration.

## Current research phase

Not set. The computational verification strategy is written when a research
question is initialized with `/research-start`.

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

None. No research question has been initialized.

## Computational representations and methods

None chosen. The global architecture deliberately does not pre-select exact
algebra, symbolic manipulation, interval arithmetic, numerical integration,
theorem proving, or any package. Record the project's own choices and their
rationale here once a question exists. For substantial reusable or
conclusion-critical machinery, record a proportionate trust strategy: the
mathematical domain, representation, trusted primitives, equality or normal-form
semantics, dependencies, custom infrastructure, rationale, limitations,
infrastructure tests, research-specific scientific validation, and independent
cross-check strategy. Trivial calculations do not need a lengthy analysis.

## Research-specific computational infrastructure

None. Reusable machinery, if the research justifies any, belongs under
`research/computation/`; research-scoped environment definitions belong under
`research/environment/`. Document the computational contract, minimum API,
dependencies and environment identity, dependent obligations, Engineer
implementation provenance, infrastructure tests, Scientific Computation's
research-specific validation, and known limitations. Scientific Computation
owns the semantics; Engineer is provisioned only when the substrate needs work.

## Numerical and formal evidence standards

None declared. Record precision, tolerance, residual, convergence, sample-size,
and rigor requirements before running the checks they govern.

## Independence strategy

None declared. Record when a second implementation, algorithm, library,
language, or method is required rather than optional.

## Phase-transition triggers

None declared. Record the concrete changes that would require reconsidering the
computational strategy.

## Deferred or non-machine-checkable issues

None recorded.

## Known limitations and risks

None recorded. Include limitations of the chosen representations and tools
themselves, not only of the physics.

## Related decisions

None. Link consequential methodological choices to entries in
`research/DECISIONS.md`.
