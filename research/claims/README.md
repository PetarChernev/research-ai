# Claim Ledger

`ledger.yaml` is the canonical registry of research claims. IDs are stable (`C001`, `C002`, ...); never reuse an ID after rejection. The ledger begins with no claims and must not contain examples presented as evidence.

## Status vocabulary

- `conjecture`: proposed but not established.
- `derived`: supported by an auditable derivation in its stated regime.
- `numerically-supported`: supported by a recorded experiment; not thereby derived.
- `literature-supported`: directly supported by cited primary-source evidence in the same regime.
- `reproduced`: an existing computational result was independently reproduced from durable artifacts.
- `verified`: an independent verifier passed the claim and a verification report is linked.
- `inconclusive`: available evidence does not decide the claim.
- `contradicted`: evidence directly conflicts with the claim.
- `rejected`: no longer treated as viable; the history remains.

Evidence count alone never implies `verified`. Shared code, assumptions, or derivations are not independent evidence. The validator requires a reciprocal complete derivation for `derived`, a complete checked experiment for `numerically-supported`, an exact-evidence literature note for `literature-supported`, qualifying computational evidence plus a passed computational-verification check for `reproduced`, and a substantive non-conflicted report for `verified`.

## Schema

Schema version 2. The following is schema documentation only, not an actual research claim:

```yaml
- id: C001
  claim: "<one precise, regime-qualified statement>"
  status: conjecture
  importance: medium       # low | medium | high | critical
  hypotheses: []           # HNNN IDs
  assumptions: []
  evidence:
    derivations: []          # DNNN IDs
    experiments: []          # ENNN IDs
    literature: []           # note paths or bibliography keys
    computational_checks: [] # ONNN machine-check obligation IDs
    verification: []         # paths under research/results/verification/
  checks:
    dimensional_analysis: pending
    limiting_cases: pending
    computational_verification: pending
    independent_verification: pending
  dependencies: []         # CNNN IDs
  conflicts: []            # CNNN IDs
  created_at: "<ISO-8601 timestamp>"
  updated_at: "<ISO-8601 timestamp>"
```

Check values are `pending`, `passed`, `failed`, `inconclusive`, or `not-applicable`.

## Computational checks

`evidence.computational_checks` lists `ONNN` machine-check obligations under `research/checks/`. Links are bidirectional: a listed obligation must target the claim, and an active obligation that targets the claim must be listed by it.

`checks.computational_verification` is the coarse summary of the project's currently declared executable strategy for the claim. It replaces the older `numerical_reproduction` field because computation is broader than numerical work. An obligation may be exact-symbolic, formal, numerical, convergence-based, a limiting case, a symmetry or dimensional test, a counterexample search, or an independent implementation.

The validator applies a structural gate:

```text
pending required obligation      -> computational_verification must not be passed
failed required obligation       -> computational_verification must not be passed
inconclusive required obligation -> computational_verification must not be passed
passed required obligation       -> that obligation is satisfied
superseded obligation            -> does not block the current strategy
```

A claim cannot reach `verified` while an active `required: true` obligation lacks a passing result. That gate says only that the project's own declared strategy is incomplete; it makes no claim that the chosen obligations are scientifically adequate. A claim with no applicable machine-checkable component may still be verified, with `computational_verification: not-applicable` and the absence explained in `research/COMPUTATION.md`.

Run `uv run --locked python scripts/validate_research_state.py` after edits. The validator rejects a `verified` claim without passing dimensional, limiting-case, and computational-verification checks, a passed independent-verification check, and a substantive linked report; linked failed or contradicted reports block promotion.
