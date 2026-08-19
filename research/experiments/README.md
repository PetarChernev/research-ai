# Computational Experiments

Each experiment has a stable `ENNN` directory containing its method, configuration, code, result summary, raw-data manifest, and figures. Create one with:

```bash
uv run --locked python scripts/new_experiment.py --title "Small diagnostic" --claim C001
```

Use the progression `analytic estimate -> tiny test -> diagnostics -> convergence study -> full calculation`. Allowed statuses are `planned`, `ready`, `running`, `complete`, `failed`, and `archived`. Mark `complete` only after declared checks are recorded in `result.json`.

Raw data are ignored by default. Preserve small indispensable outputs or record a stable external location, checksum, units, schema, and generating command. Use explicit `passed`, `failed`, `inconclusive`, or `not-applicable` outcomes for completed checks. The generated runner refuses to overwrite nonempty results; create a new experiment for another run. Do not modify unrelated experiment directories.
