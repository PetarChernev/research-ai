"""research/COMPUTATION.md initialization and structural validation."""

from __future__ import annotations

import unittest

from tests.support import PROJECT_ROOT, WorkspaceTestCase, run_script, validate


REQUIRED_SECTIONS = [
    "Current research phase",
    "Checkability map",
    "Current machine-check obligations",
    "Computational representations and methods",
    "Research-specific computational infrastructure",
    "Numerical and formal evidence standards",
    "Independence strategy",
    "Phase-transition triggers",
    "Deferred or non-machine-checkable issues",
    "Known limitations and risks",
    "Related decisions",
]


class ComputationPlanTests(WorkspaceTestCase):
    @property
    def plan(self):
        return self.root / "research" / "COMPUTATION.md"

    def test_template_declares_every_required_section(self) -> None:
        template = (PROJECT_ROOT / "templates" / "computation-plan.md").read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            self.assertIn(f"## {section}", template)

    def test_initialization_creates_an_active_plan(self) -> None:
        self.initialize_question()
        completed = run_script(
            "init_computation_plan.py",
            ["--phase", "Initial analytic scoping of the stated relation.", "--json"],
            self.root,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        text = self.plan.read_text(encoding="utf-8")
        self.assertIn("Status: active", text)
        self.assertIn("Does the declared relation hold?", text)
        for section in REQUIRED_SECTIONS:
            self.assertIn(f"## {section}", text)

    def test_initialization_refuses_to_clobber_an_initialized_plan(self) -> None:
        run_script("init_computation_plan.py", ["--json"], self.root)
        second = run_script("init_computation_plan.py", ["--json"], self.root)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("already initialized", second.stderr)
        forced = run_script("init_computation_plan.py", ["--force", "--json"], self.root)
        self.assertEqual(forced.returncode, 0, forced.stderr)

    def test_uninitialized_plan_is_valid_before_a_question_exists(self) -> None:
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_uninitialized_plan_fails_after_a_question_exists(self) -> None:
        self.initialize_question()
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "still the uninitialized scaffold")

    def test_missing_plan_fails_validation(self) -> None:
        self.plan.unlink()
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "required artifact is missing")

    def test_missing_required_section_fails_validation(self) -> None:
        text = self.plan.read_text(encoding="utf-8").replace(
            "## Independence strategy", "## Independence approach"
        )
        self.plan.write_text(text, encoding="utf-8")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "missing required section '## Independence strategy'")

    def test_initialized_plan_with_a_question_validates(self) -> None:
        self.initialize_question()
        run_script(
            "init_computation_plan.py",
            ["--phase", "Initial analytic scoping of the stated relation.", "--json"],
            self.root,
        )
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_validator_does_not_judge_the_declared_methodology(self) -> None:
        self.initialize_question()
        run_script("init_computation_plan.py", ["--phase", "Bespoke hand-rolled arithmetic only."], self.root)
        text = self.plan.read_text(encoding="utf-8").replace(
            "## Computational representations and methods",
            "## Computational representations and methods\n\nExact arithmetic implemented from scratch; no external package.",
        )
        self.plan.write_text(text, encoding="utf-8")
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])


if __name__ == "__main__":
    unittest.main()
