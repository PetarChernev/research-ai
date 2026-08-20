---
name: reproduce-result
description: Use to independently reproduce a recorded analytical or numerical result solely from durable repository artifacts, compare within declared tolerances, and document shared dependencies and failures.
compatibility: OpenCode 1.18+
metadata:
  domain: scientific-verification
  operation: reproduction
---

# Reproduce a Result

## 1. Establish independence

Start from a fresh session and the recorded repository artifacts, not transient chat context or an author's unstated instructions. List all shared model, code, data, assumptions, libraries, and environment components. A fresh same-model session is procedural separation; re-running the same function is a repeat, not an independent implementation.

Name the intended mode before starting, because the three are not interchangeable:

- **repetition**: rerunning the recorded implementation, for example
  `scripts/run_check.py ONNN` against the same entrypoint. This tests
  determinism, provenance completeness, and environment portability. It cannot
  detect an error encoded in the implementation itself.
- **reproduction**: rebuilding the calculation from the recorded specification
  and parameters with your own code, sharing only the stated mathematics.
- **independent implementation**: a different algorithm, representation,
  library, or language, sharing as little as possible. Shared machinery from
  `research/computation/` reduces this to reproduction at best.

## 2. Audit the record

Check that the target includes code or derivation, parameters, seeds, input provenance and checksums, environment, command, Git commit, observable definition, uncertainty, and acceptance tolerance. For a machine-check obligation, also check the declared question, encoded assumptions, predeclared acceptance criterion, and the recorded `spec_sha256` and `implementation_sha256`; a hash that no longer matches the current files means the recorded result is stale. Missing information is itself a reproducibility finding.

## 3. Reconstruct the environment

Use the lockfile and recorded domain-software versions where practical. Record unavoidable substitutions, platform differences, dirty worktree state, and any unavailable external inputs. Never silently fetch a mutable input.

## 4. Re-run the minimal case

First reproduce an analytic limit or tiny diagnostic. Then run the recorded calculation without changing parameters. Preserve logs and a separate machine-readable result rather than overwriting the source artifact.

## 5. Compare quantitatively

Compare observables, uncertainty estimates, convergence behavior, and qualitative features against predeclared tolerances. Investigate discrepancies through precision, seed, platform, solver, and input differences.

## 6. Increase independence when important

Use a different derivation route, algorithm, library, discretization, or implementation language when the claim's importance warrants it. Shared tests can also encode the same mistake; add independent analytical checks.

## 7. Report the outcome

Link the reproduction artifact and state explicitly whether the result was independently implemented, reproduced, only repeated, inconclusive, or contradicted, and list what was shared in each case. Do not promote the claim to `verified`; reproduction is one evidence stream and independent falsification remains separate.

If the work warrants a durable executable artifact, the director may adopt it as an obligation of class `independent-implementation`, implemented by `scientific-computation` and executed through the deterministic runner. Rerunning an existing obligation is not that; it is repetition.
