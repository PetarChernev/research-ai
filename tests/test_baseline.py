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
        self.assertEqual(payload["counts"]["critiques"], 0)

    def test_scaffold_copy_validates(self) -> None:
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_baseline_carries_no_research_content(self) -> None:
        ledger = yaml.safe_load((PROJECT_ROOT / "research" / "claims" / "ledger.yaml").read_text())
        self.assertEqual(ledger, {"schema_version": 2, "claims": []})
        self.assertEqual(status(PROJECT_ROOT)["question"], "Not set. Run /research-start <question>.")
        self.assertEqual(
            sorted(
                path.name
                for path in (PROJECT_ROOT / "research" / "checks").iterdir()
                if not (
                    path.is_dir()
                    and list(path.iterdir())
                    and all(child.name == "__pycache__" for child in path.iterdir())
                )
            ),
            ["README.md"],
        )
        self.assertEqual(
            sorted(path.name for path in (PROJECT_ROOT / "research" / "critiques").iterdir()),
            ["README.md"],
        )
        self.assertEqual(
            sorted(
                path.name
                for path in (PROJECT_ROOT / "research" / "computation").iterdir()
                if not (
                    path.is_dir()
                    and not any(
                        "__pycache__" not in child.parts
                        for child in path.rglob("*")
                        if child.is_file()
                    )
                )
            ),
            ["README.md"],
        )

    def test_existing_helpers_still_work(self) -> None:
        from tests.support import run_script

        hypothesis = run_script("new_hypothesis.py", ["--title", "Candidate", "--json"], self.root)
        self.assertEqual(hypothesis.returncode, 0, hypothesis.stderr)
        experiment = run_script("new_experiment.py", ["--title", "Diagnostic", "--json"], self.root)
        self.assertEqual(experiment.returncode, 0, experiment.stderr)
        derivations = self.new_derivations(
            [{"title": "Analytic route", "charter": "Test one bounded route."}]
        )
        self.assertTrue((self.root / "research" / "hypotheses" / "H001.md").is_file())
        self.assertTrue((self.root / "research" / "experiments" / "E001" / "config.yaml").is_file())
        self.assertEqual(derivations["derivations"][0]["id"], "D001")
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

    def test_provenance_accepts_engineer_delegation_metadata(self) -> None:
        path = self.root / "research" / "provenance.jsonl"
        path.write_text(
            '{"timestamp":"2026-01-01T00:00:00Z","agent":"scientific-computation",'
            '"operation":"engineer-provisioned","delegated_agent":"engineer",'
            '"task":"Build exact kernel","obligation_id":"O001","success":true}\n',
            encoding="utf-8",
        )
        payload = validate(self.root)
        self.assert_no_error_matching(payload, "delegated_agent")


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
