# Hypotheses

Hypotheses use stable IDs `H001`, `H002`, and so on, with one Markdown file per ID. Create the next artifact with:

```bash
uv run --locked python scripts/new_hypothesis.py --title "Short candidate explanation"
```

Allowed lifecycle statuses are `proposed`, `active`, `testing`, `supported`, `disfavored`, `falsified`, and `retired`. These describe a hypothesis, not the verification level of every related claim.

Maintain multiple competing hypotheses when the question permits. Each artifact must state assumptions, predictions, discriminating tests, and falsifiers. Do not delete falsified hypotheses; preserve why they failed.
