# Claim Ledger

`ledger.yaml` is the canonical registry of research claims. IDs are stable (`C001`, `C002`, ...); never reuse an ID after rejection. The ledger begins with no claims and must not contain examples presented as evidence.

## Status vocabulary

- `conjecture`: proposed but not established.
- `derived`: supported by an auditable derivation in its stated regime.
- `numerically-supported`: supported by a recorded experiment; not thereby derived.
- `literature-supported`: directly supported by cited primary-source evidence in the same regime.
- `reproduced`: an existing numerical result was independently reproduced from durable artifacts.
- `verified`: an independent verifier passed the claim and a verification report is linked.
- `inconclusive`: available evidence does not decide the claim.
- `contradicted`: evidence directly conflicts with the claim.
- `rejected`: no longer treated as viable; the history remains.

Evidence count alone never implies `verified`. Shared code, assumptions, or derivations are not independent evidence. The validator requires a reciprocal complete derivation for `derived`, a complete checked experiment for `numerically-supported` or `reproduced`, an exact-evidence literature note for `literature-supported`, and a substantive non-conflicted report for `verified`.

## Schema

The following is schema documentation only, not an actual research claim:

```yaml
- id: C001
  claim: "<one precise, regime-qualified statement>"
  status: conjecture
  importance: medium       # low | medium | high | critical
  hypotheses: []           # HNNN IDs
  assumptions: []
  evidence:
    derivations: []        # DNNN IDs
    experiments: []        # ENNN IDs
    literature: []         # note paths or bibliography keys
    verification: []       # paths under research/results/verification/
  checks:
    dimensional_analysis: pending
    limiting_cases: pending
    independent_verification: pending
    numerical_reproduction: not-applicable
  dependencies: []         # CNNN IDs
  conflicts: []            # CNNN IDs
  created_at: "<ISO-8601 timestamp>"
  updated_at: "<ISO-8601 timestamp>"
```

Check values are `pending`, `passed`, `failed`, `inconclusive`, or `not-applicable`. Run `uv run --locked python scripts/validate_research_state.py` after edits. The validator rejects a `verified` claim without passing dimensional/limiting checks, a passed independent-verification check, and a substantive linked report; linked failed or contradicted reports block promotion.
