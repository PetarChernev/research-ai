#!/usr/bin/env python3
"""Summarize research state from durable artifacts rather than session memory."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from _research import PROJECT_ROOT, current_question, load_frontmatter, markdown_sections


def load_claims(root: Path) -> list[dict[str, Any]]:
    path = root / "research" / "claims" / "ledger.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("research/claims/ledger.yaml: root must be a mapping")
    claims = data.get("claims", [])
    if not isinstance(claims, list):
        raise ValueError("research/claims/ledger.yaml: claims must be a list")
    if any(not isinstance(claim, dict) for claim in claims):
        raise ValueError("research/claims/ledger.yaml: every claim must be a mapping")
    return claims


def scan_markdown_metadata(directory: Path, pattern: str) -> list[dict[str, Any]]:
    artifacts = []
    regex = re.compile(pattern)
    if not directory.exists():
        return artifacts
    for path in sorted(directory.iterdir()):
        if not regex.fullmatch(path.name):
            continue
        target = path / "README.md" if path.is_dir() else path
        if not target.exists():
            continue
        metadata, _ = load_frontmatter(target)
        artifacts.append(metadata)
    return artifacts


def next_actions(root: Path) -> list[str]:
    state = root / "research" / "STATE.md"
    if not state.exists():
        return []
    section = markdown_sections(state.read_text(encoding="utf-8")).get(
        "Next recommended actions", ""
    )
    actions = []
    for line in section.splitlines():
        cleaned = re.sub(r"^(?:[-*]|\d+\.)\s+", "", line.strip())
        if cleaned and cleaned.lower() not in {"none.", "none recorded.", "not set."}:
            actions.append(cleaned)
    return actions


def build_status(root: Path) -> dict[str, Any]:
    claims = load_claims(root)
    hypotheses = scan_markdown_metadata(root / "research" / "hypotheses", r"H\d{3}\.md")
    experiments = scan_markdown_metadata(root / "research" / "experiments", r"E\d{3}")
    active_hypotheses = [
        item
        for item in hypotheses
        if item.get("status") in {"proposed", "active", "testing"}
    ]
    active_experiments = [
        item
        for item in experiments
        if item.get("status") in {"planned", "ready", "running"}
    ]
    important_claims = [
        {
            "id": claim.get("id"),
            "claim": claim.get("claim"),
            "status": claim.get("status"),
            "importance": claim.get("importance"),
        }
        for claim in claims
        if claim.get("importance") in {"high", "critical"}
    ]
    unresolved_verification = [
        claim.get("id")
        for claim in claims
        if isinstance(claim.get("checks"), dict)
        and claim["checks"].get("independent_verification") in {"pending", "inconclusive", "failed"}
        and claim.get("status") not in {"rejected"}
        and isinstance(claim.get("id"), str)
    ]
    contradictions = [
        {
            "id": claim.get("id"),
            "status": claim.get("status"),
            "conflicts": [
                item for item in claim.get("conflicts", []) if isinstance(item, str)
            ]
            if isinstance(claim.get("conflicts"), list)
            else [],
        }
        for claim in claims
        if claim.get("status") == "contradicted" or claim.get("conflicts")
    ]
    verification_directory = root / "research" / "results" / "verification"
    if verification_directory.exists():
        for path in sorted(verification_directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            metadata, _ = load_frontmatter(path)
            if metadata.get("outcome") in {"failed verification", "contradicted"}:
                contradictions.append(
                    {
                        "id": metadata.get("claim_id", "?"),
                        "status": metadata.get("outcome"),
                        "conflicts": [path.relative_to(root).as_posix()],
                    }
                )
    status_names = [
        claim.get("status") if isinstance(claim.get("status"), str) else "unknown"
        for claim in claims
    ]
    return {
        "question": current_question(root) or "Not set. Run /research-start <question>.",
        "active_hypotheses": active_hypotheses,
        "claims_by_status": dict(sorted(Counter(status_names).items())),
        "important_claims": important_claims,
        "unresolved_verification": unresolved_verification,
        "active_experiments": active_experiments,
        "major_contradictions": contradictions,
        "next_actions": next_actions(root),
    }


def format_artifacts(items: list[dict[str, Any]]) -> str:
    if not items:
        return "none"
    return "; ".join(
        f"{item.get('id', '?')} [{item.get('status', 'unknown')}]: {item.get('title', 'untitled')}"
        for item in items
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        status = build_status(args.root.resolve())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise SystemExit(f"Cannot summarize invalid research state: {exc}")
    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True, default=str))
        return 0

    claim_counts = ", ".join(
        f"{name}={count}" for name, count in status["claims_by_status"].items()
    ) or "none"
    important = "; ".join(
        f"{claim['id']} [{claim['status']}]: {claim['claim']}"
        for claim in status["important_claims"]
    ) or "none"
    verification = ", ".join(status["unresolved_verification"]) or "none"
    contradictions = "; ".join(
        f"{item['id']} [{item['status']}] conflicts={','.join(item['conflicts']) or 'unspecified'}"
        for item in status["major_contradictions"]
    ) or "none"
    actions = "; ".join(status["next_actions"]) or "none recorded"
    print(f"Question: {status['question']}")
    print(f"Active hypotheses: {format_artifacts(status['active_hypotheses'])}")
    print(f"Claims by status: {claim_counts}")
    print(f"Highest-value claims: {important}")
    print(f"Unresolved verification: {verification}")
    print(f"Active experiments: {format_artifacts(status['active_experiments'])}")
    print(f"Major contradictions: {contradictions}")
    print(f"Next actions: {actions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
