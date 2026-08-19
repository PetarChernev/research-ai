#!/usr/bin/env python3
"""Allocate and scaffold the next hypothesis artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", help="Short hypothesis title")
    parser.add_argument("--title", dest="title_option", help="Short hypothesis title")
    parser.add_argument("--statement", help="Initial falsifiable statement")
    parser.add_argument("--question", help="Question addressed; defaults to QUESTION.md")
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.title and args.title_option:
        raise SystemExit("Provide the title either positionally or with --title, not both.")

    root = args.root.resolve()
    hypotheses = root / "research" / "hypotheses"
    hypothesis_id = next_artifact_id(hypotheses, "H")
    destination = hypotheses / f"{hypothesis_id}.md"
    title = clean_inline(
        args.title_option or args.title or "Untitled hypothesis",
        fallback="Untitled hypothesis",
    )
    question = clean_inline(
        args.question or current_question(root),
        fallback="Not set; define research/QUESTION.md before evaluating this hypothesis.",
        limit=1000,
    )
    statement = (args.statement or "To be specified as a falsifiable statement.").strip()
    created_at = utc_now()

    write_from_template(
        root / "templates" / "hypothesis.md",
        destination,
        {
            "HYPOTHESIS_ID": hypothesis_id,
            "TITLE": title,
            "DATE": created_at,
            "QUESTION": question,
            "STATEMENT": statement,
        },
    )
    relative = relative_to_root(root, destination)
    append_provenance(
        root,
        operation="hypothesis-created",
        relevant_paths=[relative],
        success=True,
    )
    output = {"id": hypothesis_id, "path": relative}
    print(json.dumps(output) if args.json else f"Created {hypothesis_id}: {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
