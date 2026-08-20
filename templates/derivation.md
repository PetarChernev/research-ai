---
id: "{{DERIVATION_ID}}"
title: >-
  {{TITLE}}
status: draft
target_claims: {{TARGET_CLAIMS_JSON}}
created_at: "{{DATE}}"
updated_at: "{{DATE}}"
---

# {{DERIVATION_ID}}: {{TITLE}}

## Target claim

State the exact claim or quantity to derive.

## Assumptions

List physical and mathematical assumptions, conventions, and boundary conditions.

## Notation

Define every symbol needed to read this artifact independently.

## Known inputs

Link established equations, literature evidence, or prior derivations.

## Derivation

Separate exact equalities from approximations and show intermediate steps.

## Approximations

State approximation order and discarded terms.

## Validity regime

Give parameter, asymptotic, gauge, coordinate, and boundary-condition restrictions.

## Dimensional check

Record dimensions on both sides of the important equations.

## Limiting-case checks

Test soluble, symmetric, weak/strong-coupling, or other informative limits.

## Candidate machine-checkable obligations

Identify concrete assertions from this derivation that can be tested
mechanically. State the expected result and the assumptions each test would
encode, and say what it would leave untested. Link existing `ONNN` obligations
under `research/checks/` where they have already been instantiated, and record
recorded outcomes rather than expectations.

Recommend a method if one is obviously suited, but the research plan in
`research/COMPUTATION.md` decides the representation, tooling, and standard. It
is acceptable to record that a step is conceptual and not usefully
machine-checkable.

Do not treat proposed or successful machine checks as a replacement for the
readable derivation. Symbolic output is supporting evidence, not automatically a
proof; numerical agreement is not a derivation.

## Relationship to literature

Link exact source locations and explain any convention changes.

## Unresolved concerns

Keep suspected sign, normalization, or domain issues visible.

## Conclusion

State the result and its epistemic category without overstating it.
