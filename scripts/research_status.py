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


COMPUTATION_UNINITIALIZED_MARKER = "Status: not-started"
BLOCKING_OUTCOMES = {"failed", "inconclusive", "error"}


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


def load_obligations(root: Path) -> list[dict[str, Any]]:
    """Read machine-check obligations without judging their science."""
    directory = root / "research" / "checks"
    obligations: list[dict[str, Any]] = []
    if not directory.exists():
        return obligations
    for path in sorted(directory.iterdir()):
        if not path.is_dir() or not re.fullmatch(r"O\d{3}", path.name):
            continue
        spec_path = path / "spec.yaml"
        if not spec_path.exists():
            continue
        try:
            spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise ValueError(f"{spec_path}: {exc}") from exc
        if not isinstance(spec, dict):
            raise ValueError(f"{spec_path}: spec.yaml must be a mapping")
        outcome = None
        result_path = path / "result.json"
        if result_path.exists():
            try:
                result = json.loads(result_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError) as exc:
                raise ValueError(f"{result_path}: {exc}") from exc
            if isinstance(result, dict) and isinstance(result.get("outcome"), str):
                outcome = result["outcome"]
        obligations.append(
            {
                "id": path.name,
                "title": spec.get("title"),
                "class": spec.get("class"),
                "status": spec.get("status"),
                "required": bool(spec.get("required")),
                "claims": spec.get("claims") if isinstance(spec.get("claims"), list) else [],
                "outcome": outcome or "pending",
            }
        )
    return obligations


def computational_status(root: Path, claims: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize computational verification from structured artifacts only."""
    plan = root / "research" / "COMPUTATION.md"
    plan_exists = plan.is_file()
    plan_initialized = False
    if plan_exists:
        try:
            plan_initialized = COMPUTATION_UNINITIALIZED_MARKER not in plan.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            plan_initialized = False

    obligations = load_obligations(root)
    active = [item for item in obligations if item["status"] == "active"]
    required_active = [item for item in active if item["required"]]
    required_by_outcome: dict[str, list[str]] = {}
    for item in required_active:
        required_by_outcome.setdefault(item["outcome"], []).append(item["id"])

    unsatisfied_by_claim: dict[str, list[str]] = {}
    for item in required_active:
        if item["outcome"] == "passed":
            continue
        for claim_id in item["claims"]:
            if isinstance(claim_id, str):
                unsatisfied_by_claim.setdefault(claim_id, []).append(item["id"])

    gaps = []
    for claim in claims:
        claim_id = claim.get("id")
        if not isinstance(claim_id, str):
            continue
        checks = claim.get("checks") if isinstance(claim.get("checks"), dict) else {}
        state = checks.get("computational_verification")
        blocking = sorted(unsatisfied_by_claim.get(claim_id, []))
        if blocking:
            gaps.append(
                {
                    "claim": claim_id,
                    "computational_verification": state,
                    "reason": "active required obligation without a passing result",
                    "obligations": blocking,
                }
            )
        elif state in {"pending", "failed", "inconclusive"}:
            gaps.append(
                {
                    "claim": claim_id,
                    "computational_verification": state,
                    "reason": "claim-level computational verification is not settled",
                    "obligations": [],
                }
            )

    return {
        "plan_exists": plan_exists,
        "plan_initialized": plan_initialized,
        "obligations_total": len(obligations),
        "active_obligations": [item["id"] for item in active],
        "superseded_obligations": [
            item["id"] for item in obligations if item["status"] == "superseded"
        ],
        "required_active_by_outcome": {
            name: sorted(values) for name, values in sorted(required_by_outcome.items())
        },
        "pending_required_obligations": sorted(
            item["id"] for item in required_active if item["outcome"] == "pending"
        ),
        "failed_obligations": sorted(
            item["id"] for item in active if item["outcome"] == "failed"
        ),
        "inconclusive_obligations": sorted(
            item["id"] for item in active if item["outcome"] == "inconclusive"
        ),
        "error_obligations": sorted(item["id"] for item in active if item["outcome"] == "error"),
        "claims_blocked_by_required_checks": sorted(unsatisfied_by_claim),
        "computational_verification_gaps": gaps,
    }


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


def state_items(root: Path, section_name: str) -> list[str]:
    state = root / "research" / "STATE.md"
    if not state.exists():
        return []
    section = markdown_sections(state.read_text(encoding="utf-8")).get(section_name, "")
    items = []
    for line in section.splitlines():
        cleaned = re.sub(r"^(?:[-*]|\d+\.)\s+", "", line.strip())
        if cleaned and cleaned.lower() not in {
            "none.",
            "none recorded.",
            "none nominated.",
            "not set.",
        }:
            items.append(cleaned)
    return items


def load_internal_critiques(root: Path) -> list[dict[str, Any]]:
    directory = root / "research" / "critiques"
    critiques = []
    if not directory.exists():
        return critiques
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        metadata, _ = load_frontmatter(path)
        critiques.append(
            {
                "path": path.relative_to(root).as_posix(),
                "targets": metadata.get("target_artifacts", []),
                "outcome": metadata.get("outcome", "unknown"),
                "independent": metadata.get("independent"),
            }
        )
    return critiques


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
    approved_independent_verification_claims = [
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
        "active_exploration_portfolio": state_items(root, "Active exploration portfolio"),
        "active_hypotheses": active_hypotheses,
        "claims_by_status": dict(sorted(Counter(status_names).items())),
        "important_claims": important_claims,
        "internal_critiques": load_internal_critiques(root),
        "internal_critique_queue": state_items(root, "Internal critique queue"),
        "final_independent_verification_nominations": state_items(
            root, "Final independent-verification nominations"
        ),
        "approved_independent_verification_claims": approved_independent_verification_claims,
        "active_experiments": active_experiments,
        "computational_verification": computational_status(root, claims),
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
    nominations = "; ".join(status["final_independent_verification_nominations"]) or "none"
    approved_verification = (
        ", ".join(status["approved_independent_verification_claims"]) or "none"
    )
    exploration = "; ".join(status["active_exploration_portfolio"]) or "none"
    critique_outcomes = Counter(item["outcome"] for item in status["internal_critiques"])
    critiques = ", ".join(
        f"{name}={count}" for name, count in sorted(critique_outcomes.items())
    ) or "none"
    critique_queue = "; ".join(status["internal_critique_queue"]) or "none"
    contradictions = "; ".join(
        f"{item['id']} [{item['status']}] conflicts={','.join(item['conflicts']) or 'unspecified'}"
        for item in status["major_contradictions"]
    ) or "none"
    actions = "; ".join(status["next_actions"]) or "none recorded"
    computation = status["computational_verification"]
    if not computation["plan_exists"]:
        plan_state = "missing"
    elif computation["plan_initialized"]:
        plan_state = "initialized"
    else:
        plan_state = "not initialized"
    required = ", ".join(
        f"{name}={','.join(values)}"
        for name, values in computation["required_active_by_outcome"].items()
    ) or "none"
    gaps = "; ".join(
        f"{item['claim']} [{item['computational_verification']}] {item['reason']}"
        + (f" ({','.join(item['obligations'])})" if item["obligations"] else "")
        for item in computation["computational_verification_gaps"]
    ) or "none"
    print(f"Question: {status['question']}")
    print(f"Active exploration portfolio: {exploration}")
    print(f"Active hypotheses: {format_artifacts(status['active_hypotheses'])}")
    print(f"Claims by status: {claim_counts}")
    print(f"Highest-value claims: {important}")
    print(f"Internal critiques: {critiques}")
    print(f"Internal critique queue: {critique_queue}")
    print(f"Final independent-verification nominations: {nominations}")
    print(f"Approved Opus verification claims: {approved_verification}")
    print(f"Active experiments: {format_artifacts(status['active_experiments'])}")
    print(f"Computation plan: {plan_state}")
    print(
        "Machine-check obligations: "
        f"{len(computation['active_obligations'])} active, "
        f"{len(computation['superseded_obligations'])} superseded"
    )
    print(f"Required active obligations by outcome: {required}")
    print(
        "Failed/inconclusive/error obligations: "
        f"{', '.join(computation['failed_obligations']) or 'none'} / "
        f"{', '.join(computation['inconclusive_obligations']) or 'none'} / "
        f"{', '.join(computation['error_obligations']) or 'none'}"
    )
    print(
        "Claims blocked by pending required checks: "
        f"{', '.join(computation['claims_blocked_by_required_checks']) or 'none'}"
    )
    print(f"Computational verification gaps: {gaps}")
    print(f"Major contradictions: {contradictions}")
    print(f"Next actions: {actions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
