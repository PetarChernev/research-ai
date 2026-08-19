#!/usr/bin/env python3
"""Allocate and scaffold the next reproducible experiment directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

import yaml

from _research import (
    PROJECT_ROOT,
    append_provenance,
    clean_inline,
    current_question,
    next_artifact_id,
    relative_to_root,
    render_template,
    utc_now,
    write_json,
    write_new,
)


CLAIM_ID = re.compile(r"^C\d{3}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", help="Short experiment title")
    parser.add_argument("--title", dest="title_option", help="Short experiment title")
    parser.add_argument("--claim", action="append", default=[], help="Claim ID under test")
    parser.add_argument("--method", help="Numerical or computational method")
    parser.add_argument("--question", help="Question addressed; defaults to QUESTION.md")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.title and args.title_option:
        raise SystemExit("Provide the title either positionally or with --title, not both.")
    claims = list(dict.fromkeys(args.claim))
    invalid = [claim for claim in claims if not CLAIM_ID.fullmatch(claim)]
    if invalid:
        raise SystemExit(f"Invalid claim ID(s): {', '.join(invalid)}")

    root = args.root.resolve()
    if claims:
        ledger_path = root / "research" / "claims" / "ledger.yaml"
        try:
            ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise SystemExit(f"Cannot read claim ledger: {exc}") from exc
        entries = ledger.get("claims") if isinstance(ledger, dict) else None
        if not isinstance(entries, list):
            raise SystemExit("Cannot create an experiment from a malformed claim ledger.")
        known_claims = {
            entry.get("id") for entry in entries if isinstance(entry, dict) and isinstance(entry.get("id"), str)
        }
        unknown = [claim for claim in claims if claim not in known_claims]
        if unknown:
            raise SystemExit(f"Unknown claim ID(s): {', '.join(unknown)}")
    experiments = root / "research" / "experiments"
    experiment_id = next_artifact_id(experiments, "E")
    destination = experiments / experiment_id
    title = clean_inline(
        args.title_option or args.title or "Untitled experiment",
        fallback="Untitled experiment",
    )
    question = clean_inline(
        args.question or current_question(root),
        fallback="Not set; define research/QUESTION.md before interpreting this experiment.",
        limit=1000,
    )
    method = clean_inline(args.method or "To be specified.", fallback="To be specified.")
    claims_json = json.dumps(claims)
    claims_display = ", ".join(claims) if claims else "None linked yet."
    created_at = utc_now()
    replacements = {
        "EXPERIMENT_ID": experiment_id,
        "TITLE": title,
        "DATE": created_at,
        "QUESTION": question,
        "METHOD": method,
        "CLAIMS_JSON": claims_json,
        "CLAIMS_DISPLAY": claims_display,
    }

    destination.mkdir(parents=True, exist_ok=False)
    try:
        template_map = {
            "experiment-readme.md": destination / "README.md",
            "experiment-config.yaml": destination / "config.yaml",
            "experiment-run.py": destination / "run.py",
            "experiment-analysis.py": destination / "analysis.py",
            "result.json": destination / "result.json",
            "raw-data-readme.md": destination / "raw" / "README.md",
            "figures-readme.md": destination / "figures" / "README.md",
        }
        for template_name, output_path in template_map.items():
            output_path.parent.mkdir(parents=True, exist_ok=True)
            content = render_template(root / "templates" / template_name, replacements)
            write_new(output_path, content)
        result_path = destination / "result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result.update({"experiment_id": experiment_id, "title": title, "claims": claims})
        write_json(result_path, result)
        (destination / "run.py").chmod(0o755)
        (destination / "analysis.py").chmod(0o755)
    except Exception:
        shutil.rmtree(destination)
        raise

    relative = relative_to_root(root, destination)
    append_provenance(
        root,
        operation="experiment-created",
        experiment_id=experiment_id,
        relevant_paths=[relative],
        success=True,
    )
    output = {"id": experiment_id, "path": relative}
    print(json.dumps(output) if args.json else f"Created {experiment_id}: {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
