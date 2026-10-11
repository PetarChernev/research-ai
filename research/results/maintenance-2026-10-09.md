# Repository maintenance — 2026-10-09

## Scope

Repair the 38 inherited state-validation errors reported at the end of W002.
This is software/repository maintenance, not scientific evidence or independent
verification. Historical research authorship and outcomes remain unchanged.

## Changes

- `scripts/validate_research_state.py` recognizes the historical internal-critic
  model `openai/gpt-5.6-sol` as well as the current `openai/gpt-6-astra`. It still
  rejects unsupported models, independent internal critiques, and verification
  outcomes in internal-critique artifacts. Current agent model configuration
  and the independent-verification model boundary were not changed.
- Direct inspection of O016 found only empty `logs/`; O017 and O018 contained
  only empty `logs/` and `history/`. Their origins are unknown. Explicit
  `reservation.yaml` and README files preserve these IDs. Reservations are not
  obligations and cannot contain implementations, specifications, results,
  nested evidence, or symlinks. No files were deleted from these directories.
- Added regression coverage for historical/unsupported critic models, reserved
  ID allocation, malformed reservations, hidden evidence, and unmarked orphans.
- Fixed a baseline test that inspected live research instead of its disposable
  scaffold; the scaffold now removes copied exploratory-literature content.

## Validation record

- Initial strict validation reproduced exactly 38 errors and zero warnings.
- First full suite: 140 passed, one baseline-scaffold failure. After correcting
  the test paths the remaining fixture-contamination failure persisted; fixing
  the disposable fixture cleanup resolved it.
- Final full suite via `research_run_tests(suite="all")`: **141 passed**.
- Strict state validation via `research_validate_state(strict=true)` (the locked
  `scripts/validate_research_state.py` runner): **passed, zero errors and zero
  warnings**. Counts: 29 claims, 34 derivations, 40 critiques, five hypotheses,
  zero experiments, and 15 obligations, all active.

The maintenance adds no scientific computation and reruns no historical
obligation. Existing O001–O015 outcomes remain their previously recorded results.
