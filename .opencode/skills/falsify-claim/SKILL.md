---
name: falsify-claim
description: Use to perform a bounded, risk-first adversarial audit of a precise scientific claim through a few decisive counterexamples, limiting cases, symmetry tests, or alternate arguments before any verified status.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-verification
  operation: falsification
---

# Falsify a Claim

## 1. Freeze the target

Quote the exact ledger claim, status, assumptions, dependencies, regime, and linked primary artifacts. Do not let the target drift during the attack. State which resources are shared with the originating work.

## 2. Select decisive attacks

Rank plausible attacks by their ability to change the conclusion. Attempt at
most three by default, rather than mechanically exhausting every category:

- dimensional or unit counterexample;
- sign, factor, normalization, or convention mismatch;
- zero, infinite, weak/strong-coupling, short/long-time, or thermodynamic limit;
- exactly soluble special case;
- symmetry, gauge, coordinate, or conservation-law violation;
- boundary/initial-condition counterexample;
- hidden parameter or regularization dependence;
- alternate derivation from different starting assumptions;
- alternate computational method or representation assessment;
- contradictory primary literature or data.

Prioritize attacks that would decisively change the research conclusion. Select
one load-bearing inference for a compact alternate reconstruction. Do not
reproduce the whole derivation, dependency chain, or computation merely to make
the review look independent. If the frozen claim is too broad for a bounded
audit, report that scope problem instead of silently expanding the work.

## 2a. Request adversarial computational obligations

Inspect only the load-bearing active machine-check obligations that target the
claim: their specs, claim-specific implementation paths, encoded assumptions,
and machine-recorded results. Ask whether they test the decisive inference or
only a narrower statement, whether one plausible failure mode is untested, and
whether their acceptance criteria are scientifically adequate.

Where an attack is mechanical and decisive, recommend a new adversarial
obligation to the director: a counterexample search over the stated domain, a
limiting case the current checks avoid, a symmetry or conservation test, a
perturbed-sign or perturbed-convention variant that should fail, or an
independent implementation that does not share the existing code path. Specify
the assertion, the expected outcome, and the acceptance criterion.

Do not write a scratch implementation or author canonical machine outcomes
yourself during an ordinary verification audit. Obligations are implemented
by the `scientific-computation` role and executed only through the deterministic
runner, which alone writes `research/checks/ONNN/result.json`. If a full
reproduction or independent implementation is genuinely needed, recommend it
as a separately approved task with its own budget and artifact.

## 3. Separate failure classes

Distinguish a false claim from a narrower validity regime, ambiguous wording, insufficient numerical precision, inaccessible evidence, and a failed reproduction caused by incomplete provenance.

## 4. Preserve negative results

Record each serious attempted attack, including the exact artifact or relation inspected. Do not repair the originating derivation or code in place; that destroys independence and provenance.

## 5. Assign an outcome

Use only: `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, or `contradicted`. Passing one check is not verification. Record the verifier and originating `provider/model` IDs. This workspace requires a known verifier model different from every originating model before `verified` is available, preferably across providers. Model separation alone is not sufficient; shared assumptions, code, and data reduce independence and must be disclosed.

## 6. Write the report

Create one concise report from `templates/verification-report.md` under `research/results/verification/`. Link source artifacts, fill `verifier_model` and `originating_models`, document the independence boundary, and list at most one highest-value follow-up. The director, not the verifier, updates the claim ledger and `STATE.md`.
