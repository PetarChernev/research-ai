#!/usr/bin/env python3
"""Create research/COMPUTATION.md from the global, method-neutral template.

The plan is the research program's own computational-verification methodology.
This helper only makes initialization deterministic: it renders the template and
records the current question. It never chooses representations, methods, tools,
tolerances, or obligations. The research director writes those.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _research import (
    PROJECT_ROOT,
    append_provenance,
    clean_inline,
    current_question,
    relative_to_root,
    render_template,
    utc_now,
)


UNINITIALIZED_MARKER = "Status: not-started"
DEFAULT_PHASE = (
    "Initial. Record the current methodological regime: what is being established "
    "now, which reasoning dominates, and what class of assertion is in play."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", help="Question addressed; defaults to research/QUESTION.md")
    parser.add_argument("--phase", help="Short description of the current methodological regime")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an already-initialized plan instead of refusing",
    )
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    destination = root / "research" / "COMPUTATION.md"
    replaced = False
    if destination.exists():
        try:
            existing = destination.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise SystemExit(f"Cannot read {relative_to_root(root, destination)}: {exc}") from exc
        if UNINITIALIZED_MARKER not in existing and not args.force:
            raise SystemExit(
                "research/COMPUTATION.md is already initialized. Edit it directly, or pass "
                "--force to regenerate it from the template and lose the recorded strategy."
            )
        replaced = True

    question = clean_inline(
        args.question or current_question(root),
        fallback="Not set; define research/QUESTION.md before relying on this plan.",
        limit=1000,
    )
    content = render_template(
        root / "templates" / "computation-plan.md",
        {
            "STATUS": "active",
            "DATE": utc_now(),
            "QUESTION": question,
            "PHASE": clean_inline(args.phase or DEFAULT_PHASE, fallback=DEFAULT_PHASE, limit=1000),
        },
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(destination)

    relative = relative_to_root(root, destination)
    append_provenance(
        root,
        operation="computation-plan-initialized",
        relevant_paths=[relative],
        success=True,
    )
    output = {"path": relative, "replaced": replaced}
    if args.json:
        print(json.dumps(output))
    else:
        print(f"{'Replaced' if replaced else 'Created'} {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
