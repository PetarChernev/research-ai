---
name: literature-review
description: Use for a focused physics literature review, primary-source search, citation chaining, exact evidence extraction, contradiction search, and creation of research/literature/notes evidence packets.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-literature
  artifact: literature-note
---

# Focused Literature Review

## 1. Frame the search

Write one answerable question. Include the observable or equation, physical system, parameter regime, conventions, date range if relevant, and the project claim or hypothesis being tested. Separate discovery questions from evidence questions.

## 2. Expand queries

Build a compact query set using:

- exact technical terms and historical synonyms;
- characteristic equations, effects, and dimensionless parameters;
- author names from known anchor papers;
- alternative conventions or neighboring subfields;
- explicit contradiction terms such as `failure`, `breakdown`, `comment`, or `reanalysis`.

Record databases and query strings. Discovery metadata is not yet claim evidence.

## 3. Identify primary sources

Prefer the original derivation, experiment, dataset, or authoritative correction. Confirm identity with title, authors, year, DOI, arXiv ID, and stable locator. Treat reviews as maps to primary sources unless the review itself establishes the relevant result.

## 4. Chain citations

Trace decisive claims backward to their originating source. Search forward for replications, corrections, comments, changed regimes, and contradictory findings. Stop when additional chaining has low expected value and record the stopping condition.

## 5. Extract exact evidence

For every materially used source, record:

- the exact statement supported or contradicted;
- page, section, equation, figure, table, appendix, or dataset;
- assumptions, approximation order, conventions, and parameter domain;
- whether the evidence is analytical, numerical, experimental, or interpretive;
- access limitations and extraction uncertainty.

Read enough surrounding context to avoid citation laundering. An abstract or search snippet is normally insufficient.

## 6. Search for disconfirmation

Actively search for incompatible data, alternate explanations, convention mismatches, retractions, errata, and results outside the claimed validity regime. Keep unresolved source disagreement visible.

## 7. Write the evidence packet

Create or update a note under `research/literature/notes/` from `templates/literature-note.md`. Include question investigated, search strategy, relevant sources, supported claims, contradicted claims, exact evidence locations, assumptions/regime, confidence, and unresolved issues. Add checked BibTeX metadata to `research/literature/bibliography.bib` when the source is used.

## 8. Report uncertainty

Distinguish confidence in source identity, confidence in evidence extraction, and confidence that the source applies to the project regime. Never fabricate inaccessible details. Return stable artifact paths and remaining literature gaps.
