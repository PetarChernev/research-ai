---
name: numerical-experiment
description: Use to design and execute a reproducible computational physics experiment with a predeclared observable, parameter range, baseline, convergence and failure criteria, provenance, and result.json output.
compatibility: OpenCode 1.18+
metadata:
  domain: computational-physics
  artifact: experiment
---

# Reproducible Numerical Experiment

## 1. Define the test before coding

Record the hypothesis or claim, measurable observable, units, baseline, parameter range, and outcomes that would support, disfavor, falsify, or fail to distinguish alternatives. State numerical and scientific failure criteria in advance.

## 2. Choose the cheapest useful scale

Proceed through:

`analytic estimate -> tiny numerical test -> diagnostic checks -> convergence study -> full calculation`

Do not start an expensive run before the small test exercises the method and discriminating observable.

## 3. Scaffold the experiment

Use the `research_new_experiment` tool or:

```bash
uv run --locked python scripts/new_experiment.py --title "..." --claim C001
```

Work only in the resulting `research/experiments/ENNN/` directory. Fill `README.md` and `config.yaml` before the full run.

## 4. Specify the method

Record equations, discretization, solver, tolerances, precision, boundary/initial conditions, random seeds, input provenance, software versions, and hardware-sensitive choices. Define reference or analytic limits.

## 5. Design convergence and robustness checks

Choose applicable resolution, finite-size, timestep, basis-cutoff, tolerance, precision, seed, initial-condition, and parameter-sensitivity studies. Set quantitative acceptance thresholds. Include conservation and symmetry diagnostics.

## 6. Run and preserve provenance

Keep parameters in `config.yaml`; do not bury them in a transient command. Execute the canonical command from the experiment README. Preserve the Git commit and dirty state, command, environment, configuration hash, seeds, and input checksums or stable locations.

## 7. Write machine-readable output

Put observables and uncertainties in `result.json`; list generated artifacts. Raw data alone are not a result summary. Leave every unperformed check as `null`, `pending`, or explicitly `not-applicable` with a reason. Computation completion does not imply check completion.

## 8. Interpret conservatively

Compare against the predeclared outcomes, baselines, and known limits. Label the output a numerical observation or numerical support, not a derivation. Record failures and limitations, validate repository state, and return artifact paths to the director.
