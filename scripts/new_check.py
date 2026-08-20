#!/usr/bin/env python3
"""Allocate and scaffold the next machine-check obligation directory.

The obligation declares one concrete assertion, the method the research chose to
test it, and a predeclared acceptance criterion. Scaffolding never produces a
result: only `scripts/run_check.py` may write `research/checks/ONNN/result.json`.
"""

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
    next_artifact_id,
    relative_to_root,
    render_template,
    utc_now,
    write_new,
)


CLAIM_ID = re.compile(r"^C\d{3}$")
DERIVATION_ID = re.compile(r"^D\d{3}$")

# Generic, method-neutral vocabulary. A class describes the kind of assertion
# under test; it never selects a library, language, or tool.
CHECK_CLASSES = (
    "exact-symbolic",
    "formal",
    "numerical",
    "convergence",
    "independent-implementation",
    "limiting-case",
    "symmetry",
    "dimensional",
    "counterexample",
    "other",
)
INDEPENDENCE_REQUIREMENTS = ("not-required", "recommended", "required")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", help="Short obligation title")
    parser.add_argument("--title", dest="title_option", help="Short obligation title")
    parser.add_argument("--claim", action="append", default=[], help="Existing CNNN claim under test")
    parser.add_argument(
        "--derivation", action="append", default=[], help="Existing DNNN derivation under test"
    )
    parser.add_argument(
        "--question", required=True, help="Exact mathematical question the check tests"
    )
    parser.add_argument(
        "--acceptance-criterion",
        required=True,
        help="Predeclared pass/fail criterion, written before implementation",
    )
    parser.add_argument(
        "--check-class",
        default="other",
        choices=CHECK_CLASSES,
        help="Generic kind of assertion under test; does not select a tool",
    )
    parser.add_argument("--method", help="Method the research selected for this obligation")
    parser.add_argument("--method-rationale", help="Why that method suits this assertion")
    parser.add_argument(
        "--independence",
        default="not-required",
        choices=INDEPENDENCE_REQUIREMENTS,
        help="Whether an independent implementation or alternate method is warranted",
    )
    parser.add_argument("--independence-rationale", help="Why that independence level applies")
    parser.add_argument(
        "--optional",
        action="store_true",
        help="Record the obligation as not part of the currently required strategy",
    )
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def known_ledger_claims(root: Path) -> set[str]:
    ledger_path = root / "research" / "claims" / "ledger.yaml"
    try:
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise SystemExit(f"Cannot read claim ledger: {exc}") from exc
    entries = ledger.get("claims") if isinstance(ledger, dict) else None
    if not isinstance(entries, list):
        raise SystemExit("Cannot create an obligation from a malformed claim ledger.")
    return {
        entry.get("id")
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }


def main() -> int:
    args = parse_args()
    if args.title and args.title_option:
        raise SystemExit("Provide the title either positionally or with --title, not both.")
    title_value = args.title_option or args.title
    if not title_value or not title_value.strip():
        raise SystemExit("An obligation needs a concise title.")

    question = " ".join(args.question.split())
    acceptance = " ".join(args.acceptance_criterion.split())
    if not question:
        raise SystemExit("An obligation needs a nonempty question.")
    if not acceptance:
        raise SystemExit("Declare the acceptance criterion before implementing the check.")

    claims = list(dict.fromkeys(args.claim))
    derivations = list(dict.fromkeys(args.derivation))
    invalid = [value for value in claims if not CLAIM_ID.fullmatch(value)]
    invalid += [value for value in derivations if not DERIVATION_ID.fullmatch(value)]
    if invalid:
        raise SystemExit(f"Invalid target ID(s): {', '.join(invalid)}")

    root = args.root.resolve()
    if claims:
        unknown = sorted(set(claims) - known_ledger_claims(root))
        if unknown:
            raise SystemExit(f"Unknown claim ID(s): {', '.join(unknown)}")
    missing_derivations = [
        value for value in derivations if not (root / "research" / "derivations" / f"{value}.md").is_file()
    ]
    if missing_derivations:
        raise SystemExit(f"Unknown derivation ID(s): {', '.join(sorted(missing_derivations))}")

    checks = root / "research" / "checks"
    obligation_id = next_artifact_id(checks, "O")
    destination = checks / obligation_id
    created_at = utc_now()
    replacements = {
        "OBLIGATION_ID": obligation_id,
        "TITLE": clean_inline(title_value, fallback="Untitled obligation"),
        "DATE": created_at,
        "CLAIMS_JSON": json.dumps(claims),
        "DERIVATIONS_JSON": json.dumps(derivations),
        "CLAIMS_DISPLAY": ", ".join(claims) if claims else "None linked yet.",
        "DERIVATIONS_DISPLAY": ", ".join(derivations) if derivations else "None linked yet.",
        "CLASS": args.check_class,
        "REQUIRED": "false" if args.optional else "true",
        "QUESTION": clean_inline(question, fallback=question, limit=1000),
        "ACCEPTANCE_CRITERION": clean_inline(acceptance, fallback=acceptance, limit=1000),
        "METHOD_DESCRIPTION": clean_inline(
            args.method or "To be specified by the research plan.",
            fallback="To be specified by the research plan.",
            limit=1000,
        ),
        "METHOD_RATIONALE": clean_inline(
            args.method_rationale or "To be specified by the research plan.",
            fallback="To be specified by the research plan.",
            limit=1000,
        ),
        "INDEPENDENCE_REQUIREMENT": args.independence,
        "INDEPENDENCE_RATIONALE": clean_inline(
            args.independence_rationale or "Not yet assessed.",
            fallback="Not yet assessed.",
            limit=1000,
        ),
    }

    destination.mkdir(parents=True, exist_ok=False)
    try:
        template_map = {
            "check-readme.md": destination / "README.md",
            "check-spec.yaml": destination / "spec.yaml",
            "check-run.py": destination / "run.py",
        }
        for template_name, output_path in template_map.items():
            write_new(output_path, render_template(root / "templates" / template_name, replacements))
        (destination / "run.py").chmod(0o755)
    except Exception:
        shutil.rmtree(destination)
        raise

    relative = relative_to_root(root, destination)
    append_provenance(
        root,
        operation="check-created",
        obligation_id=obligation_id,
        relevant_paths=[relative],
        success=True,
    )
    output = {
        "id": obligation_id,
        "path": relative,
        "spec": f"{relative}/spec.yaml",
        "entrypoint": f"{relative}/run.py",
        "result": None,
        "run_command": f"uv run --locked python scripts/run_check.py {obligation_id}",
    }
    if args.json:
        print(json.dumps(output))
    else:
        print(f"Created {obligation_id}: {relative} (no result until it is run)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
