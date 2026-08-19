---
id: "{{EXPERIMENT_ID}}"
title: >-
  {{TITLE}}
status: planned
claims: {{CLAIMS_JSON}}
created_at: "{{DATE}}"
updated_at: "{{DATE}}"
---

# {{EXPERIMENT_ID}}: {{TITLE}}

## Question

{{QUESTION}}

## Hypothesis/claim tested

{{CLAIMS_DISPLAY}}

## Method

{{METHOD}}

## Expected discriminating result

State outcomes that support, disfavor, or fail to distinguish the alternatives before running the calculation.

## Parameters

The canonical machine-readable configuration is `config.yaml`. Explain parameter ranges and units here.

## Environment

Use the root `uv.lock` for helper dependencies. Record additional domain software, hardware-sensitive settings, and external input provenance here.

## How to run

```bash
uv run --locked python research/experiments/{{EXPERIMENT_ID}}/run.py
uv run --locked python research/experiments/{{EXPERIMENT_ID}}/analysis.py
```

## Convergence plan

Define resolution, timestep, finite-size, tolerance, precision, and seed studies that apply. Set pass/fail thresholds before the full run.

## Validation checks

List analytical limits, conservation laws, symmetry checks, and independent implementations. Leave unchecked items explicit.

## Result

No result recorded. `result.json` remains incomplete until the calculation and declared checks are run.

## Interpretation

Do not infer a claim status from raw output alone.

## Known limitations

Record omitted physics, numerical pathologies, and untested regimes.
