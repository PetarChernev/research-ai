---
name: derive-result
description: Use to produce an auditable theoretical physics derivation with explicit assumptions, exact relations, approximations, intermediate lemmas, validity regime, and physical consistency checks.
compatibility: OpenCode 1.18+
metadata:
  domain: theoretical-physics
  artifact: derivation
---

# Derive an Auditable Result

## 1. Create the artifact

Allocate the next unused `DNNN` ID, copy `templates/derivation.md` to `research/derivations/DNNN.md`, and link target `CNNN` IDs when they exist. A substantial result must be readable without the originating conversation.

## 2. State the target

Write the exact quantity or proposition to derive, including regime, perturbative order, error target, boundary/initial conditions, gauge or coordinate choice, and conventions.

## 3. Separate foundations

Record four distinct lists:

- assumptions about the physical model;
- definitions and notation;
- known inputs with evidence links;
- intermediate lemmas that require proof or citation.

Do not hide an assumption inside notation or call an imported result a definition.

## 4. Derive step by step

For every transition, mark it as an exact identity, equation of motion, cited input, approximation, asymptotic expansion, or numerical/symbolic check. Show sign choices, normalization, measures, degeneracies, and factors such as 2, pi, hbar, c, and k_B.

## 5. Control approximations

Name the expansion parameter, retained order, discarded terms, and error estimate where possible. State uniformity, secular behavior, singular limits, and interchange-of-limit assumptions. Never present a fitted pattern as an analytical derivation.

## 6. State the final result

Give the result in a boxed or otherwise unmistakable form. Immediately state its validity regime and dependencies. Distinguish exact and approximate conclusions.

## 7. Attack the derivation

Perform applicable checks:

- dimensions and units;
- signs, normalization, and symmetries;
- conservation laws and invariances;
- exactly soluble and limiting cases;
- boundary and initial conditions;
- gauge or coordinate dependence;
- comparison with convention-adjusted literature results.

Use symbolic software only as a documented cross-check. Preserve commands and outputs that materially support the claim.

## 8. Conclude epistemically

Record unresolved concerns and classify the output as a derived result only in its stated regime. Return the derivation path to the director for claim-ledger integration and, if important, independent verification.
