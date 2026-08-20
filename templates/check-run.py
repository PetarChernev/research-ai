#!/usr/bin/env python3
"""Executable implementation of machine-check obligation {{OBLIGATION_ID}}.

Run this only through the deterministic wrapper:

    uv run --locked python scripts/run_check.py {{OBLIGATION_ID}}

This file decides nothing canonical. It performs the declared test and reports
the process exit status; `scripts/run_check.py` records the canonical outcome in
`result.json`. Do not write `result.json` from here.

Exit protocol:

    0 -> the declared acceptance criterion was met
    1 -> the declared acceptance criterion was not met
    2 -> the check could not decide (inconclusive)
    3 -> execution error

Optional structured observations may be emitted with `emit_observations({...})`.
The wrapper stores them as data; they never choose the outcome.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


OBLIGATION_ID = "{{OBLIGATION_ID}}"
CHECK_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHECK_DIR.parents[2]

# Reusable research-specific machinery belongs in research/computation/.
# Import it only if this obligation actually depends on it, and declare the
# dependency in spec.yaml under implementation.infrastructure:
#
# sys.path.insert(0, str(PROJECT_ROOT / "research" / "computation"))

PASSED = 0
FAILED = 1
INCONCLUSIVE = 2
ERROR = 3

OBSERVATION_PREFIX = "##OBSERVATIONS##"


def emit_observations(observations: dict[str, Any]) -> None:
    """Emit one structured, machine-readable observation record to stdout."""
    print(
        OBSERVATION_PREFIX
        + " "
        + json.dumps(observations, sort_keys=True, allow_nan=False, default=str)
    )


def check() -> int:
    """Perform the declared test and return one of the exit codes above.

    Implement the smallest adequate test of the assertion recorded in
    `spec.yaml`. Compare against the predeclared acceptance criterion; do not
    invent a threshold here that the specification does not state.
    """
    raise NotImplementedError(
        f"Implement check() for {OBLIGATION_ID} against its declared acceptance criterion."
    )


def main() -> int:
    try:
        outcome = check()
    except Exception as exc:  # noqa: BLE001 - an unhandled failure is an execution error
        print(f"{OBLIGATION_ID} execution error: {exc!r}", file=sys.stderr)
        return ERROR
    if outcome not in {PASSED, FAILED, INCONCLUSIVE}:
        print(f"{OBLIGATION_ID} returned an undefined status {outcome!r}", file=sys.stderr)
        return ERROR
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
