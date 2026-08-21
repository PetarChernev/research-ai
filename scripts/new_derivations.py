#!/usr/bin/env python3
"""Allocate a batch of preassigned derivation artifacts for parallel work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from _research import (
    PROJECT_ROOT,
    append_provenance,
    clean_inline,
    current_question,
    next_artifact_id,
    relative_to_root,
    utc_now,
    write_from_template,
)


MAX_BRANCHES = 16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branches-json",
        required=True,
        help="JSON array of {title, charter, target_claims?} branch objects",
    )
    parser.add_argument("--wave", required=True, help="Short exploration-wave label")
    parser.add_argument("--question", help="Question addressed; defaults to QUESTION.md")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def load_claim_ids(root: Path) -> set[str]:
    path = root / "research" / "claims" / "ledger.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    claims = data.get("claims", []) if isinstance(data, dict) else []
    return {
        claim["id"]
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }


def parse_branches(raw: str, known_claims: set[str]) -> list[dict[str, Any]]:
    try:
        branches = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--branches-json is not valid JSON: {exc}") from exc
    if not isinstance(branches, list) or not 1 <= len(branches) <= MAX_BRANCHES:
        raise SystemExit(f"Provide between 1 and {MAX_BRANCHES} branch objects.")

    normalized = []
    for index, branch in enumerate(branches, 1):
        if not isinstance(branch, dict):
            raise SystemExit(f"Branch {index} must be an object.")
        title = clean_inline(str(branch.get("title", "")), fallback="", limit=160)
        charter = str(branch.get("charter", "")).strip()
        targets = branch.get("target_claims", [])
        if not title or not charter:
            raise SystemExit(f"Branch {index} requires nonempty title and charter fields.")
        if not isinstance(targets, list) or any(not isinstance(item, str) for item in targets):
            raise SystemExit(f"Branch {index} target_claims must be a list of claim IDs.")
        unknown = sorted(set(targets) - known_claims)
        if unknown:
            raise SystemExit(f"Branch {index} references unknown claims: {', '.join(unknown)}")
        normalized.append({"title": title, "charter": charter, "target_claims": targets})
    return normalized


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    derivations = root / "research" / "derivations"
    branches = parse_branches(args.branches_json, load_claim_ids(root))
    wave = clean_inline(args.wave, fallback="", limit=80)
    if not wave:
        raise SystemExit("--wave must be nonempty.")
    question = clean_inline(
        args.question or current_question(root),
        fallback="Not set; define research/QUESTION.md before evaluating this branch.",
        limit=1000,
    )
    created_at = utc_now()
    created: list[dict[str, str]] = []

    try:
        for branch in branches:
            derivation_id = next_artifact_id(derivations, "D")
            destination = derivations / f"{derivation_id}.md"
            write_from_template(
                root / "templates" / "derivation.md",
                destination,
                {
                    "DERIVATION_ID": derivation_id,
                    "TITLE": branch["title"],
                    "TARGET_CLAIMS_JSON": json.dumps(branch["target_claims"]),
                    "EXPLORATION_WAVE_JSON": json.dumps(wave),
                    "PRODUCER_MODEL_JSON": json.dumps("openai/gpt-5.6-sol"),
                    "DATE": created_at,
                    "QUESTION": question,
                    "BRANCH_CHARTER": branch["charter"],
                },
            )
            relative = relative_to_root(root, destination)
            created.append({"id": derivation_id, "path": relative, "title": branch["title"]})
    except Exception:
        for item in created:
            (root / item["path"]).unlink(missing_ok=True)
        raise

    paths = [item["path"] for item in created]
    append_provenance(
        root,
        operation="derivation-portfolio-created",
        relevant_paths=paths,
        task=f"wave={wave}; branches={len(created)}",
        success=True,
    )
    output = {"wave": wave, "derivations": created}
    if args.json:
        print(json.dumps(output))
    else:
        print(f"Created {len(created)} derivations for {wave}: {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
