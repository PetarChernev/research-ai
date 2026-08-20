# Verification Reports

Store one independent report per verification attempt, using a filename such as `C003-2026-08-19-anthropic.md` and `templates/verification-report.md`. Give the verifier the exact claim and primary artifacts, not a summary asserting that the claim is correct. Record the fixed verifier `provider/model` ID and every known model that materially produced the claim or its evidence.

Allowed report outcomes are `verified`, `supported but not independently verified`, `inconclusive`, `failed verification`, and `contradicted`. Identify the actual verifier/method and every source artifact. A separate same-model session is only procedural separation. A different model is required but is not sufficient by itself. Only the first outcome can support ledger status `verified`, and only when the report has a known different-model boundary and an alternate reconstruction or comparably strong independent check documents genuine independence.
