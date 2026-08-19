---
name: falsify-claim
description: Use to attack a precise scientific claim through counterexamples, limiting cases, symmetry tests, alternative derivations, independent numerics, and contradictory literature before any verified status.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-verification
  operation: falsification
---

# Falsify a Claim

## 1. Freeze the target

Quote the exact ledger claim, status, assumptions, dependencies, regime, and linked primary artifacts. Do not let the target drift during the attack. State which resources are shared with the originating work.

## 2. Build an attack matrix

Attempt applicable attacks independently:

- dimensional or unit counterexample;
- sign, factor, normalization, or convention mismatch;
- zero, infinite, weak/strong-coupling, short/long-time, or thermodynamic limit;
- exactly soluble special case;
- symmetry, gauge, coordinate, or conservation-law violation;
- boundary/initial-condition counterexample;
- hidden parameter or regularization dependence;
- alternate derivation from different starting assumptions;
- alternate numerical method or clean implementation;
- contradictory primary literature or data.

Prioritize attacks that would decisively change the research conclusion.

## 3. Separate failure classes

Distinguish a false claim from a narrower validity regime, ambiguous wording, insufficient numerical precision, inaccessible evidence, and a failed reproduction caused by incomplete provenance.

## 4. Preserve negative results

Record every serious failed check, including commands and artifacts needed to inspect it. Do not repair the originating derivation or code in place; that destroys independence and provenance.

## 5. Assign an outcome

Use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. Passing one check is not verification. Shared assumptions, code, data, or model reduce independence and must be disclosed; a fresh same-model session is procedural separation only.

## 6. Write the report

Create a report from `templates/verification-report.md` under `research/results/verification/`. Link source artifacts, document the independence boundary, and list required follow-up. The director, not the verifier, updates the claim ledger and `STATE.md`.
