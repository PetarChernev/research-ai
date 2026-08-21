# Verification Reports

Store one user-approved Opus independent report per final verification attempt, using a filename such as `C003-2026-08-19-anthropic.md` and `templates/verification-report.md`. Give the verifier the exact claim and primary artifacts, not a summary asserting that the claim is correct. Same-model GPT reports belong under `research/critiques/`, never here.

Allowed report outcomes are `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, and `contradicted`. Set `verifier: verifier-anthropic`, `verifier_model: anthropic/claude-opus-5`, and `user_approved: true`, and identify every source artifact and originating model. Only the first outcome can support ledger status `verified`, and only when an alternate reconstruction or comparably strong independent check documents genuine independence.

Reports created before the 2026-08-22 lifecycle cutover remain in place with
`legacy: true`. They preserve their original model, outcome, source packet, and
body, but they cannot satisfy a current independent-verification gate. Do not
rewrite or move them to make them resemble current Opus reports or internal
critiques.
