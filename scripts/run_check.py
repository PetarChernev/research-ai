#!/usr/bin/env python3
"""Deterministic wrapper that executes a machine-check obligation.

This wrapper is the only component permitted to create or replace
`research/checks/ONNN/result.json`. It runs the research-authored entrypoint as
a subprocess and derives the canonical outcome from the actual process exit
status:

    exit 0 -> passed
    exit 1 -> failed
    exit 2 -> inconclusive
    anything else, a timeout, or a non-executable entrypoint -> error

The implementation may emit one structured JSON observation record to stdout
prefixed with `##OBSERVATIONS##`. That payload is stored as data and can never
select the outcome. Result schema v2 records the spec, entrypoint, and
deterministic content fingerprints of every declared infrastructure or
research-environment dependency. The wrapper does not interpret the science.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import platform
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from _research import (
    PROJECT_ROOT,
    append_provenance,
    fingerprint_paths,
    git_state,
    relative_to_root,
    sha256_file,
    utc_now,
    write_json,
)


OBLIGATION_ID = re.compile(r"^O\d{3}$")
OBSERVATION_PREFIX = "##OBSERVATIONS##"
RESULT_SCHEMA_VERSION = 2
DEFAULT_TIMEOUT_SECONDS = 900
MAX_LOG_BYTES = 1_048_576
MAX_OBSERVATION_BYTES = 65_536
MAX_PACKAGES = 500
EXIT_OUTCOMES = {0: "passed", 1: "failed", 2: "inconclusive"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("obligation", help="Obligation ID, for example O001")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Wall-clock limit in seconds (default {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def load_spec(path: Path) -> dict[str, Any]:
    try:
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc
    if not isinstance(spec, dict):
        raise SystemExit(f"{path}: spec.yaml must contain a mapping")
    return spec


def resolve_entrypoint(root: Path, check_dir: Path, spec: dict[str, Any]) -> Path:
    implementation = spec.get("implementation")
    entrypoint = implementation.get("entrypoint") if isinstance(implementation, dict) else None
    if not isinstance(entrypoint, str) or not entrypoint.strip():
        raise SystemExit("spec.yaml must declare implementation.entrypoint")
    if Path(entrypoint).is_absolute():
        raise SystemExit("implementation.entrypoint must be a repository-relative path")
    candidate = (root / entrypoint).resolve()
    try:
        candidate.relative_to(check_dir.resolve())
    except ValueError as exc:
        raise SystemExit(
            "implementation.entrypoint must resolve inside the obligation directory"
        ) from exc
    return candidate


def environment_summary() -> dict[str, Any]:
    packages: dict[str, str] = {}
    truncated = False
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata["Name"] if distribution.metadata else None
        if not name:
            continue
        if len(packages) >= MAX_PACKAGES:
            truncated = True
            break
        packages[name] = distribution.version or "unknown"
    summary: dict[str, Any] = {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "packages": dict(sorted(packages.items())),
    }
    if truncated:
        summary["packages_truncated"] = True
    return summary


def truncate(text: str, limit: int = MAX_LOG_BYTES) -> str:
    encoded = text.encode("utf-8", errors="replace")
    if len(encoded) <= limit:
        return text
    return encoded[:limit].decode("utf-8", errors="replace") + "\n[truncated by scripts/run_check.py]\n"


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON number '{value}'")


def extract_observations(stdout: str) -> dict[str, Any]:
    """Return the last well-formed observation record, or an empty mapping."""
    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if not stripped.startswith(OBSERVATION_PREFIX):
            continue
        payload = stripped[len(OBSERVATION_PREFIX) :].strip()
        if len(payload.encode("utf-8", errors="replace")) > MAX_OBSERVATION_BYTES:
            return {"_observation_error": "observation payload exceeds the size limit"}
        try:
            parsed = json.loads(payload, parse_constant=reject_json_constant)
        except ValueError as exc:
            return {"_observation_error": f"unparsable observation payload: {exc}"}
        if not isinstance(parsed, dict):
            return {"_observation_error": "observation payload must be a JSON object"}
        return parsed
    return {}


def collect_artifacts(root: Path, check_dir: Path) -> list[str]:
    directory = check_dir / "artifacts"
    if not directory.is_dir():
        return []
    return sorted(
        relative_to_root(root, path) for path in directory.rglob("*") if path.is_file()
    )


def write_logs(root: Path, check_dir: Path, stdout: str, stderr: str) -> list[str]:
    logs = check_dir / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    written = []
    for name, text in (("stdout.log", stdout), ("stderr.log", stderr)):
        path = logs / name
        try:
            path.write_text(truncate(text), encoding="utf-8")
        except OSError:
            continue
        written.append(relative_to_root(root, path))
    return written


def main() -> int:
    args = parse_args()
    obligation = args.obligation.strip()
    if not OBLIGATION_ID.fullmatch(obligation):
        raise SystemExit(f"Invalid obligation ID '{args.obligation}'; expected ONNN.")

    root = args.root.resolve()
    check_dir = root / "research" / "checks" / obligation
    if not check_dir.is_dir():
        raise SystemExit(
            f"{obligation} does not exist. Allocate it with scripts/new_check.py first."
        )
    spec_path = check_dir / "spec.yaml"
    if not spec_path.is_file():
        raise SystemExit(f"{obligation} has no spec.yaml; the obligation is not declared.")

    spec = load_spec(spec_path)
    if spec.get("id") != obligation:
        raise SystemExit(f"spec.yaml id '{spec.get('id')}' does not match directory {obligation}")
    entrypoint = resolve_entrypoint(root, check_dir, spec)
    if not entrypoint.is_file():
        raise SystemExit(f"Declared entrypoint does not exist: {relative_to_root(root, entrypoint)}")

    claims = spec.get("claims") if isinstance(spec.get("claims"), list) else []
    derivations = spec.get("derivations") if isinstance(spec.get("derivations"), list) else []
    implementation = spec.get("implementation")
    declared_infrastructure = (
        implementation.get("infrastructure") if isinstance(implementation, dict) else None
    )
    if not isinstance(declared_infrastructure, list):
        raise SystemExit("spec.yaml must declare implementation.infrastructure as a list")
    try:
        infrastructure, infrastructure_sha256 = fingerprint_paths(
            root, declared_infrastructure
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Cannot fingerprint declared infrastructure: {exc}") from exc
    spec_sha256 = sha256_file(spec_path)
    implementation_sha256 = sha256_file(entrypoint)
    implementation_path = relative_to_root(root, entrypoint)
    argv = [sys.executable, str(entrypoint)]
    command = shlex.join(argv)
    runner_command = f"uv run --locked python scripts/run_check.py {obligation}"

    environment = os.environ.copy()
    environment["PYTHONUNBUFFERED"] = "1"

    started_at = utc_now()
    exit_code: int | None = None
    notes = ""
    try:
        completed = subprocess.run(
            argv,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            check=False,
            env=environment,
        )
        stdout, stderr = completed.stdout, completed.stderr
        exit_code = completed.returncode
    except subprocess.TimeoutExpired as expired:
        stdout = expired.stdout or ""
        stderr = (expired.stderr or "") + f"\n[timeout after {args.timeout} s]\n"
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        notes = f"Execution exceeded the {args.timeout} s wall-clock limit."
    except OSError as exc:
        stdout, stderr = "", f"{exc!r}\n"
        notes = "The declared entrypoint could not be executed."
    completed_at = utc_now()

    outcome = EXIT_OUTCOMES.get(exit_code, "error") if exit_code is not None else "error"
    if outcome == "error" and not notes:
        notes = f"Entrypoint returned exit code {exit_code}, which is outside the declared protocol."
    if not notes:
        notes = "Canonical outcome derived from the recorded process exit status."

    commit, dirty = git_state(root)
    result = {
        "schema_version": RESULT_SCHEMA_VERSION,
        "obligation_id": obligation,
        "claims": claims,
        "derivations": derivations,
        "outcome": outcome,
        "exit_code": exit_code,
        "started_at": started_at,
        "completed_at": completed_at,
        "command": command,
        "runner_command": runner_command,
        "implementation": implementation_path,
        "git_commit": commit,
        "dirty_worktree": dirty,
        "spec_sha256": spec_sha256,
        "implementation_sha256": implementation_sha256,
        "infrastructure": infrastructure,
        "infrastructure_sha256": infrastructure_sha256,
        "environment": environment_summary(),
        "observations": extract_observations(stdout),
        "artifacts": collect_artifacts(root, check_dir),
        "logs": write_logs(root, check_dir, stdout, stderr),
        "notes": notes,
    }
    result_path = check_dir / "result.json"
    write_json(result_path, result)

    append_provenance(
        root,
        tool="run_check",
        operation="check-run",
        obligation_id=obligation,
        command=runner_command,
        relevant_paths=[
            relative_to_root(root, result_path),
            *[record["path"] for record in infrastructure],
        ],
        git_commit=commit,
        dirty_worktree=dirty,
        success=outcome == "passed",
    )

    summary = {
        "obligation_id": obligation,
        "outcome": outcome,
        "exit_code": exit_code,
        "result": relative_to_root(root, result_path),
        "logs": result["logs"],
        "artifacts": result["artifacts"],
        "infrastructure_sha256": infrastructure_sha256,
    }
    if args.json:
        print(json.dumps(summary))
    else:
        print(f"{obligation}: {outcome} (exit {exit_code}) -> {summary['result']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
