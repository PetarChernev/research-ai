"""Obligation allocation is deterministic, never overwrites, and checks links."""

from __future__ import annotations

import unittest

import yaml

from tests.support import WorkspaceTestCase, run_script, validate


class NewCheckTests(WorkspaceTestCase):
    def test_ids_are_allocated_in_order(self) -> None:
        first = self.new_check()
        second = self.new_check()
        third = self.new_check()
        self.assertEqual([first["id"], second["id"], third["id"]], ["O001", "O002", "O003"])
        self.assertEqual(first["path"], "research/checks/O001")

    def test_scaffold_creates_no_result(self) -> None:
        created = self.new_check()
        directory = self.root / "research" / "checks" / created["id"]
        self.assertEqual(
            sorted(path.name for path in directory.iterdir()),
            ["README.md", "run.py", "spec.yaml"],
        )
        self.assertFalse((directory / "result.json").exists())
        self.assertIsNone(created["result"])

    def test_existing_ids_are_never_overwritten(self) -> None:
        self.new_check()
        marker = self.root / "research" / "checks" / "O001" / "spec.yaml"
        original = marker.read_text(encoding="utf-8")
        self.new_check()
        self.assertEqual(marker.read_text(encoding="utf-8"), original)
        self.assertTrue((self.root / "research" / "checks" / "O002").is_dir())

    def test_question_and_acceptance_criterion_are_required(self) -> None:
        completed = run_script("new_check.py", ["--title", "No criterion", "--json"], self.root)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("acceptance-criterion", completed.stderr)

    def test_unknown_claim_reference_is_rejected(self) -> None:
        failure = self.new_check("--claim", "C404", expect_success=False)
        self.assertNotEqual(failure["returncode"], 0)
        self.assertIn("Unknown claim ID", failure["stderr"])
        self.assertFalse((self.root / "research" / "checks" / "O001").exists())

    def test_unknown_derivation_reference_is_rejected(self) -> None:
        failure = self.new_check("--derivation", "D404", expect_success=False)
        self.assertNotEqual(failure["returncode"], 0)
        self.assertIn("Unknown derivation ID", failure["stderr"])

    def test_spec_records_declared_fields(self) -> None:
        self.write_ledger()
        created = self.new_check(
            "--claim",
            "C001",
            "--check-class",
            "exact-symbolic",
            "--method",
            "Exact algebra in a declared normal form.",
            "--independence",
            "recommended",
        )
        spec = yaml.safe_load(
            (self.root / "research" / "checks" / created["id"] / "spec.yaml").read_text()
        )
        self.assertEqual(spec["id"], "O001")
        self.assertEqual(spec["claims"], ["C001"])
        self.assertEqual(spec["class"], "exact-symbolic")
        self.assertTrue(spec["required"])
        self.assertEqual(spec["status"], "active")
        self.assertEqual(spec["independence"]["requirement"], "recommended")
        self.assertEqual(spec["implementation"]["entrypoint"], "research/checks/O001/run.py")

    def test_optional_flag_marks_the_obligation_not_required(self) -> None:
        created = self.new_check("--optional")
        spec = yaml.safe_load(
            (self.root / "research" / "checks" / created["id"] / "spec.yaml").read_text()
        )
        self.assertFalse(spec["required"])

    def test_invalid_check_class_is_rejected(self) -> None:
        failure = self.new_check("--check-class", "sympy", expect_success=False)
        self.assertNotEqual(failure["returncode"], 0)


class ObligationStructureValidationTests(WorkspaceTestCase):
    def test_duplicate_or_malformed_obligation_directory_fails(self) -> None:
        self.new_check()
        duplicate = self.root / "research" / "checks" / "O001-old"
        duplicate.mkdir()
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "obligation directories must be named ONNN")

    def test_spec_id_must_match_the_directory(self) -> None:
        self.new_check()
        self.edit_spec("O001", {'id: "O001"': 'id: "O007"'})
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "id must be 'O001'")

    def test_empty_acceptance_criterion_fails_validation(self) -> None:
        self.new_check()
        self.edit_spec(
            "O001",
            {
                "acceptance_criterion: >-\n  Exact zero residual in the declared normal form.":
                    'acceptance_criterion: ""'
            },
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "acceptance_criterion must be a nonempty string")

    def test_missing_entrypoint_fails_validation(self) -> None:
        self.new_check()
        (self.root / "research" / "checks" / "O001" / "run.py").unlink()
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "implementation.entrypoint does not exist")

    def test_entrypoint_outside_the_obligation_is_rejected(self) -> None:
        self.new_check()
        self.edit_spec(
            "O001",
            {'entrypoint: "research/checks/O001/run.py"': 'entrypoint: "scripts/run_check.py"'},
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "must resolve inside the obligation directory")

    def test_invalid_status_is_rejected(self) -> None:
        self.new_check()
        self.edit_spec("O001", {"status: active": "status: retired"})
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "invalid obligation status")

    def test_missing_infrastructure_path_is_rejected(self) -> None:
        self.new_check()
        self.edit_spec(
            "O001",
            {"  infrastructure: []": '  infrastructure: ["research/computation/absent.py"]'},
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "infrastructure path does not exist")

    def test_declared_infrastructure_that_exists_is_accepted(self) -> None:
        self.new_check()
        self.edit_spec(
            "O001",
            {"  infrastructure: []": '  infrastructure: ["research/computation/README.md"]'},
        )
        payload = validate(self.root)
        self.assert_no_error_matching(payload, "infrastructure")

    def test_validator_does_not_judge_the_scientific_method(self) -> None:
        self.new_check("--check-class", "symmetry", "--method", "Hand-rolled bespoke arithmetic.")
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])


if __name__ == "__main__":
    unittest.main()
