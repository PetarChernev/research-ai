#!/usr/bin/env python3
"""Execute {{EXPERIMENT_ID}} and write its machine-readable result."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import shlex
import sys
from pathlib import Path
from typing import Any

import yaml


EXPERIMENT_ID = "{{EXPERIMENT_ID}}"
EXPERIMENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EXPERIMENT_DIR.parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from _research import append_provenance, git_state, relative_to_root, utc_now, write_json


def compute(config: dict[str, Any]) -> dict[str, Any]:
    """Implement the scientific calculation and return observables only."""
    raise NotImplementedError(
        "Implement compute(config), then declare and run validation checks before interpreting it."
    )


def environment_summary() -> dict[str, Any]:
    packages: dict[str, str] = {}
    for distribution in ("numpy", "scipy", "sympy", "mpmath", "jax", "PyYAML"):
        try:
            packages[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            continue
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=EXPERIMENT_DIR / "config.yaml")
    return parser.parse_args()


def reject_nonstandard_json(value: str) -> None:
    raise ValueError(f"Non-standard JSON number in result.json: {value}")


def main() -> int:
    args = parse_args()
    command = shlex.join([sys.executable, *sys.argv])
    result_path = EXPERIMENT_DIR / "result.json"
    try:
        config_path = args.config.resolve()
        config_bytes = config_path.read_bytes()
        config = yaml.safe_load(config_bytes) or {}
        if not isinstance(config, dict):
            raise TypeError("config.yaml must contain a mapping")
        if config.get("experiment_id") != EXPERIMENT_ID:
            raise ValueError("config.yaml experiment_id does not match this directory")

        result = json.loads(
            result_path.read_text(encoding="utf-8"), parse_constant=reject_nonstandard_json
        )
        if result.get("results"):
            raise FileExistsError(
                "result.json already contains observables; create a new experiment rather than overwrite run history."
            )

        started_at = utc_now()
        observables = compute(config)
        if not isinstance(observables, dict):
            raise TypeError("compute(config) must return a dictionary")
        json.dumps(observables, allow_nan=False)

        commit, dirty = git_state(PROJECT_ROOT)
        result.update(
            {
                "claims": config.get("claims", []),
                "git_commit": commit,
                "dirty_worktree": dirty,
                "command": command,
                "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
                "started_at": started_at,
                "completed_at": utc_now(),
                "environment": environment_summary(),
                "parameters": config.get("parameters", {}),
                "random_seeds": config.get("random_seeds", []),
                "results": observables,
                "checks": {
                    "completed": False,
                    "convergence": None,
                    "independent_seed": None,
                    "known_limit": None,
                    "precision": None,
                },
                "artifacts": [],
                "notes": "Calculation completed; validation checks remain incomplete.",
            }
        )
        write_json(result_path, result)
    except Exception:
        append_provenance(
            PROJECT_ROOT,
            operation="experiment-run",
            experiment_id=EXPERIMENT_ID,
            command=command,
            relevant_paths=[relative_to_root(PROJECT_ROOT, EXPERIMENT_DIR)],
            success=False,
        )
        raise

    append_provenance(
        PROJECT_ROOT,
        operation="experiment-run",
        experiment_id=EXPERIMENT_ID,
        command=command,
        relevant_paths=[relative_to_root(PROJECT_ROOT, result_path)],
        git_commit=commit,
        dirty_worktree=dirty,
        success=True,
    )
    print(f"Wrote {relative_to_root(PROJECT_ROOT, result_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
