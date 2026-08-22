---
name: literature-exploration
description: Use for open-ended, cross-domain literature discovery that searches alternate terminology, historical lineages, shared equations, mathematical structures, and transferable methods, producing candidate leads rather than evidence.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-literature
  artifact: exploration-report
---

# Exploratory Literature Discovery

## 1. Extract Search Anchors

Read the assigned question and minimal project artifacts. Extract both semantic
and structural anchors: physical objects, observables, characteristic
equations, operators, invariants, symmetries, conservation laws, singular
limits, boundary conditions, scaling exponents, dimensionless groups, and
problem-solving bottlenecks. Do not add structures that are absent merely to
create an analogy.

## 2. Follow One Distinct Lens

Honor the director's assigned lens so parallel explorers cover genuinely
different territory. A lens may emphasize historical terminology, equation or
operator structure, methods and representations, neighboring phenomena, or a
specific distant discipline. These are examples, not a fixed taxonomy. State
what is intentionally outside this branch.

## 3. Let Vocabulary Drift Productively

Begin with several queries, then branch on technical terms found in useful
results. Search synonyms, older notation, named equations, classifications,
review taxonomies, citation ancestors, citing work, and terminology from other
disciplines. Keep a compact query trail that explains important pivots. Spend a
bounded fraction of the search on technically plausible surprises rather than
only nearest-neighbor papers.

## 4. Build Candidate Mappings

For every retained lead, record:

- source identity and a stable locator when available;
- what triggered the connection;
- a proposed dictionary from project objects to source objects;
- the correspondence class: exact, convention-dependent, regime-limited,
  method transfer, or heuristic;
- potential use for the project;
- the strongest known mismatch or failure mode;
- what primary material was actually inspected and what remains uninspected.

Prefer a few technically specific mappings over a long list of topical
similarities.

## 5. Attack the Analogy Early

Check cheap incompatibilities before ranking a lead: dimensions, domains,
linearity, locality, stochastic versus deterministic meaning, equilibrium
versus dynamics, boundary or initial conditions, conservation laws, regularity,
parameter regime, and observable definitions. Do not quietly repair a mismatch
by relabeling it.

## 6. Rank for Follow-Up

Rank candidates by structural specificity, plausible usefulness, novelty
relative to current project artifacts, and cost of decisive evaluation. Keep
uncertain but high-upside leads visible. Record informative dead ends so later
waves do not repeat them.

## 7. Preserve the Evidence Boundary

Write one report under `research/literature/explorations/` from
`templates/literature-exploration.md`. Label every connection a candidate lead.
An abstract, snippet, metadata record, secondary source, or structural
resemblance cannot support a ledger claim.

Recommend `literature` to inspect primary sources, extract exact evidence,
match regimes, seek contradictions, and create canonical source notes. Recommend
`theorist` to construct or falsify the proposed mathematical dictionary and
write a derivation. Recommend both when adoption depends on both source content
and a nontrivial mapping. The director alone decides which leads receive those
handoffs and whether evaluated results enter state, decisions, or claims.
