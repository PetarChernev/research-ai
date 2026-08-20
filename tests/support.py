"""Shared helpers for the workspace tests.

The tests exercise the helper scripts through their command-line interfaces
against a throwaway copy of the repository scaffold, so they check the same
entry points the OpenCode tools call.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PASSING_CHECK = '''#!/usr/bin/env python3
import json
import sys

print("##OBSERVATIONS## " + json.dumps({"residual": 0.0}))
sys.exit(0)
'''

FAILING_CHECK = '''#!/usr/bin/env python3
import json
import sys

print("##OBSERVATIONS## " + json.dumps({"residual": 1.5}))
sys.exit(1)
'''

INCONCLUSIVE_CHECK = '''#!/usr/bin/env python3
import sys

print("insufficient precision to decide", file=sys.stderr)
sys.exit(2)
'''

ERROR_CHECK = '''#!/usr/bin/env python3
import sys

sys.exit(42)
'''

CLAIM_TEMPLATE = """schema_version: 2
claims:
  - id: C001
    claim: "A precise, regime-qualified test statement."
    status: {status}
    importance: medium
    hypotheses: []
    assumptions: []
    evidence:
      derivations: []
      experiments: []
      literature: []
      computational_checks: {computational_checks}
      verification: {verification}
    checks:
      dimensional_analysis: {dimensional}
      limiting_cases: {limiting}
      computational_verification: {computational}
      independent_verification: {independent}
    dependencies: []
    conflicts: []
    created_at: "2026-01-01T00:00:00Z"
    updated_at: "2026-01-01T00:00:00Z"
"""


def run_script(script: str, args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    """Invoke a helper script the same way the OpenCode tools do."""
    return subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / script), *args, "--root", str(root)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def validate(root: Path, *, strict: bool = False) -> dict[str, Any]:
    args = ["--json"]
    if strict:
        args.append("--strict")
    completed = run_script("validate_research_state.py", args, root)
    if not completed.stdout.strip():
        raise AssertionError(f"validator produced no output: {completed.stderr}")
    return json.loads(completed.stdout)


def status(root: Path) -> dict[str, Any]:
    completed = run_script("research_status.py", ["--json"], root)
    if completed.returncode != 0:
        raise AssertionError(f"research_status failed: {completed.stderr}")
    return json.loads(completed.stdout)


def error_messages(payload: dict[str, Any]) -> list[str]:
    return [f"{item['location']}: {item['message']}" for item in payload["errors"]]


class WorkspaceTestCase(unittest.TestCase):
    """Base class providing a disposable copy of the research scaffold."""

    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="research-workspace-")
        self.addCleanup(self._temporary.cleanup)
        self.root = Path(self._temporary.name) / "workspace"
        self.root.mkdir()
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        shutil.copytree(
            PROJECT_ROOT / "research",
            self.root / "research",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        # The scaffold on main carries no research artifacts; make that explicit
        # so a stray local artifact cannot influence a test.
        for pattern in ("checks/O*", "experiments/E*", "derivations/D*", "hypotheses/H*"):
            for path in (self.root / "research").glob(pattern):
                shutil.rmtree(path) if path.is_dir() else path.unlink()
        (self.root / "research" / "provenance.jsonl").write_text("", encoding="utf-8")

    # -- convenience builders -------------------------------------------------

    def new_check(self, *extra: str, expect_success: bool = True) -> dict[str, Any]:
        args = [
            "--title",
            "Declared assertion",
            "--question",
            "Does the declared relation hold exactly?",
            "--acceptance-criterion",
            "Exact zero residual in the declared normal form.",
            "--json",
            *extra,
        ]
        completed = run_script("new_check.py", args, self.root)
        if not expect_success:
            return {"returncode": completed.returncode, "stderr": completed.stderr}
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def implement(self, obligation: str, source: str) -> Path:
        path = self.root / "research" / "checks" / obligation / "run.py"
        path.write_text(source, encoding="utf-8")
        return path

    def run_check(self, obligation: str) -> dict[str, Any]:
        completed = run_script("run_check.py", [obligation, "--json"], self.root)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def result_of(self, obligation: str) -> dict[str, Any]:
        path = self.root / "research" / "checks" / obligation / "result.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def edit_spec(self, obligation: str, replacements: dict[str, str]) -> None:
        path = self.root / "research" / "checks" / obligation / "spec.yaml"
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            self.assertIn(old, text, f"{old!r} not present in {path}")
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    def write_ledger(
        self,
        *,
        status: str = "conjecture",
        computational_checks: str = "[]",
        verification: str = "[]",
        dimensional: str = "pending",
        limiting: str = "pending",
        computational: str = "pending",
        independent: str = "pending",
    ) -> None:
        (self.root / "research" / "claims" / "ledger.yaml").write_text(
            CLAIM_TEMPLATE.format(
                status=status,
                computational_checks=computational_checks,
                verification=verification,
                dimensional=dimensional,
                limiting=limiting,
                computational=computational,
                independent=independent,
            ),
            encoding="utf-8",
        )

    def initialize_question(self, text: str = "Does the declared relation hold?") -> None:
        path = self.root / "research" / "QUESTION.md"
        content = path.read_text(encoding="utf-8").replace(
            "Not set. Run `/research-start <physics question>`.", text
        )
        path.write_text(content, encoding="utf-8")

    def assert_no_error_matching(self, payload: dict[str, Any], fragment: str) -> None:
        matches = [item for item in error_messages(payload) if fragment in item]
        self.assertEqual(matches, [], f"unexpected error(s) containing {fragment!r}: {matches}")

    def assert_error_matching(self, payload: dict[str, Any], fragment: str) -> None:
        matches = [item for item in error_messages(payload) if fragment in item]
        self.assertTrue(matches, f"expected an error containing {fragment!r}; got {error_messages(payload)}")
