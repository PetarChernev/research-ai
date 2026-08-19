#!/usr/bin/env python3
"""Inspect {{EXPERIMENT_ID}} output and add explicit diagnostics or figures."""

from __future__ import annotations

import json
from pathlib import Path


EXPERIMENT_DIR = Path(__file__).resolve().parent


def main() -> int:
    result = json.loads((EXPERIMENT_DIR / "result.json").read_text(encoding="utf-8"))
    if not result.get("results"):
        raise SystemExit("No numerical results exist yet; implement and run run.py first.")
    print(json.dumps(result["results"], indent=2, sort_keys=True))
    print("Add convergence diagnostics and tracked figure paths before marking checks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
