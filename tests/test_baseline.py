"""The architecture-only baseline must stay valid and research-neutral."""

from __future__ import annotations

import unittest

import yaml

from tests.support import PROJECT_ROOT, WorkspaceTestCase, status, validate


class BaselineTests(WorkspaceTestCase):
    def test_repository_baseline_validates(self) -> None:
        payload = validate(PROJECT_ROOT)
        self.assertTrue(payload["valid"], payload["errors"])
        self.assertEqual(payload["counts"]["obligations"], 0)

    def test_scaffold_copy_validates(self) -> None:
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_baseline_carries_no_research_content(self) -> None:
        ledger = yaml.safe_load((PROJECT_ROOT / "research" / "claims" / "ledger.yaml").read_text())
        self.assertEqual(ledger, {"schema_version": 2, "claims": []})
        self.assertEqual(status(PROJECT_ROOT)["question"], "Not set. Run /research-start <question>.")
        self.assertEqual(
            sorted(path.name for path in (PROJECT_ROOT / "research" / "checks").iterdir()),
            ["README.md"],
        )
        self.assertEqual(
            sorted(path.name for path in (PROJECT_ROOT / "research" / "computation").iterdir()),
            ["README.md"],
        )

    def test_existing_helpers_still_work(self) -> None:
        from tests.support import run_script

        hypothesis = run_script("new_hypothesis.py", ["--title", "Candidate", "--json"], self.root)
        self.assertEqual(hypothesis.returncode, 0, hypothesis.stderr)
        experiment = run_script("new_experiment.py", ["--title", "Diagnostic", "--json"], self.root)
        self.assertEqual(experiment.returncode, 0, experiment.stderr)
        self.assertTrue((self.root / "research" / "hypotheses" / "H001.md").is_file())
        self.assertTrue((self.root / "research" / "experiments" / "E001" / "config.yaml").is_file())
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_provenance_accepts_obligation_id(self) -> None:
        self.new_check()
        payload = validate(self.root)
        self.assert_no_error_matching(payload, "unsupported field")
        records = [
            line
            for line in (self.root / "research" / "provenance.jsonl").read_text().splitlines()
            if "obligation_id" in line
        ]
        self.assertTrue(records, "expected an obligation provenance record")


class DependencyTests(unittest.TestCase):
    def test_no_physics_specific_dependency_was_introduced(self) -> None:
        pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
        for package in (
            "sympy",
            "cadabra",
            "lean",
            "mathematica",
            "sage",
            "julia",
            "arb",
            "flint",
            "hypothesis",
            "numpy",
            "scipy",
            "jax",
            "torch",
        ):
            self.assertNotIn(package, pyproject, f"{package} must not be a global dependency")


if __name__ == "__main__":
    unittest.main()
