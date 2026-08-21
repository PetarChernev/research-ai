# Internal Critiques

Store fast second-pass GPT-5.6 Sol critiques here, using names such as
`D003-2026-08-22-openai-01.md` and `templates/internal-critique.md`. Each report
must target frozen artifacts, identify its reviewer and originating models, and
set `independent: false`.

Allowed outcomes are `no-blocking-issue-found`, `revision-required`,
`blocking-issue-found`, and `inconclusive`. These reports can prune a branch,
trigger revision, or nominate a machine check. They are not verification
reports, never support `checks.independent_verification: passed`, and never
support ledger status `verified`.
