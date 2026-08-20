"""The deterministic wrapper alone establishes the canonical machine outcome."""

from __future__ import annotations

import json
import unittest

from tests.support import (
    ERROR_CHECK,
    FAILING_CHECK,
    INCONCLUSIVE_CHECK,
    PASSING_CHECK,
    WorkspaceTestCase,
    run_script,
    validate,
)


class RunCheckOutcomeTests(WorkspaceTestCase):
    def test_exit_zero_is_recorded_as_passed(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        summary = self.run_check("O001")
        self.assertEqual(summary["outcome"], "passed")
        self.assertEqual(summary["exit_code"], 0)
        self.assertEqual(self.result_of("O001")["outcome"], "passed")

    def test_exit_one_is_recorded_as_failed(self) -> None:
        self.new_check()
        self.implement("O001", FAILING_CHECK)
        self.assertEqual(self.run_check("O001")["outcome"], "failed")

    def test_exit_two_is_recorded_as_inconclusive(self) -> None:
        self.new_check()
        self.implement("O001", INCONCLUSIVE_CHECK)
        self.assertEqual(self.run_check("O001")["outcome"], "inconclusive")

    def test_undeclared_exit_code_is_recorded_as_error(self) -> None:
        self.new_check()
        self.implement("O001", ERROR_CHECK)
        summary = self.run_check("O001")
        self.assertEqual(summary["outcome"], "error")
        self.assertEqual(self.result_of("O001")["exit_code"], 42)

    def test_unimplemented_scaffold_cannot_pass(self) -> None:
        self.new_check()
        self.assertEqual(self.run_check("O001")["outcome"], "error")

    def test_observations_never_select_the_outcome(self) -> None:
        self.new_check()
        self.implement(
            "O001",
            '#!/usr/bin/env python3\n'
            'import json, sys\n'
            'print("##OBSERVATIONS## " + json.dumps({"outcome": "passed", "residual": 9.0}))\n'
            "sys.exit(1)\n",
        )
        summary = self.run_check("O001")
        self.assertEqual(summary["outcome"], "failed")
        recorded = self.result_of("O001")
        self.assertEqual(recorded["outcome"], "failed")
        self.assertEqual(recorded["observations"], {"outcome": "passed", "residual": 9.0})

    def test_unknown_obligation_is_refused(self) -> None:
        completed = run_script("run_check.py", ["O404", "--json"], self.root)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("does not exist", completed.stderr)


class RunCheckProvenanceTests(WorkspaceTestCase):
    def test_result_records_hashes_and_provenance(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        result = self.result_of("O001")
        for field in (
            "schema_version",
            "obligation_id",
            "claims",
            "outcome",
            "started_at",
            "completed_at",
            "command",
            "runner_command",
            "git_commit",
            "dirty_worktree",
            "spec_sha256",
            "implementation_sha256",
            "infrastructure",
            "infrastructure_sha256",
            "environment",
            "observations",
            "artifacts",
            "logs",
        ):
            self.assertIn(field, result)
        self.assertEqual(len(result["spec_sha256"]), 64)
        self.assertEqual(len(result["implementation_sha256"]), 64)
        self.assertEqual(result["schema_version"], 2)
        self.assertEqual(result["infrastructure"], [])
        self.assertEqual(len(result["infrastructure_sha256"]), 64)
        self.assertEqual(result["implementation"], "research/checks/O001/run.py")
        self.assertIn("python", result["environment"])
        self.assertEqual(
            result["logs"],
            ["research/checks/O001/logs/stdout.log", "research/checks/O001/logs/stderr.log"],
        )
        for log in result["logs"]:
            self.assertTrue((self.root / log).is_file())

    def test_provenance_line_is_appended(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        records = [
            json.loads(line)
            for line in (self.root / "research" / "provenance.jsonl").read_text().splitlines()
            if line.strip()
        ]
        runs = [item for item in records if item.get("operation") == "check-run"]
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["obligation_id"], "O001")
        self.assertTrue(runs[0]["success"])

    def test_result_is_replaced_atomically(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.assertEqual(self.result_of("O001")["outcome"], "passed")
        self.implement("O001", FAILING_CHECK)
        self.run_check("O001")
        directory = self.root / "research" / "checks" / "O001"
        self.assertFalse((directory / "result.json.tmp").exists())
        replaced = self.result_of("O001")
        self.assertEqual(replaced["outcome"], "failed")
        self.assertEqual(replaced["observations"], {"residual": 1.5})

    def test_stdout_is_preserved_in_logs(self) -> None:
        self.new_check()
        self.implement(
            "O001",
            '#!/usr/bin/env python3\nimport sys\nprint("diagnostic detail")\nsys.exit(0)\n',
        )
        self.run_check("O001")
        stdout = (self.root / "research" / "checks" / "O001" / "logs" / "stdout.log").read_text()
        self.assertIn("diagnostic detail", stdout)

    def test_generated_artifacts_are_collected(self) -> None:
        self.new_check()
        self.implement(
            "O001",
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "from pathlib import Path\n"
            "directory = Path(__file__).resolve().parent / 'artifacts'\n"
            "directory.mkdir(exist_ok=True)\n"
            "(directory / 'table.txt').write_text('0\\n')\n"
            "sys.exit(0)\n",
        )
        self.run_check("O001")
        self.assertEqual(
            self.result_of("O001")["artifacts"], ["research/checks/O001/artifacts/table.txt"]
        )
        payload = validate(self.root)
        self.assert_no_error_matching(payload, "artifacts path")


class StaleResultTests(WorkspaceTestCase):
    def test_changed_implementation_makes_the_result_stale(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.assertTrue(validate(self.root)["valid"])
        self.implement("O001", PASSING_CHECK + "# adjusted\n")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "implementation_sha256 does not match")

    def test_changed_spec_makes_the_result_stale(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.edit_spec("O001", {"assumptions: []": "assumptions: [\"declared normal form\"]"})
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "spec_sha256 does not match")

    def test_rerunning_clears_the_stale_result(self) -> None:
        self.new_check()
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.implement("O001", PASSING_CHECK + "# adjusted\n")
        self.run_check("O001")
        self.assertTrue(validate(self.root)["valid"], validate(self.root)["errors"])

    def test_hand_written_result_is_detected(self) -> None:
        self.new_check()
        path = self.root / "research" / "checks" / "O001" / "result.json"
        path.write_text(json.dumps({"obligation_id": "O001", "outcome": "passed"}), encoding="utf-8")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "missing required field 'spec_sha256'")


class InfrastructureStalenessTests(WorkspaceTestCase):
    def _declare(self, path: str) -> None:
        self.edit_spec(
            "O001",
            {"  infrastructure: []": f'  infrastructure: ["{path}"]'},
        )

    def test_changed_infrastructure_file_makes_result_stale(self) -> None:
        self.new_check()
        infrastructure = self.root / "research" / "computation" / "kernel.txt"
        infrastructure.write_text("contract-v1\n", encoding="utf-8")
        self._declare("research/computation/kernel.txt")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.assertTrue(validate(self.root)["valid"])

        infrastructure.write_text("contract-v2\n", encoding="utf-8")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "infrastructure fingerprints do not match")

        self.run_check("O001")
        self.assertTrue(validate(self.root)["valid"], validate(self.root)["errors"])

    def test_changed_file_in_declared_directory_makes_result_stale(self) -> None:
        self.new_check()
        directory = self.root / "research" / "computation" / "kernel"
        directory.mkdir()
        (directory / "b.txt").write_text("b\n", encoding="utf-8")
        (directory / "a.txt").write_text("a\n", encoding="utf-8")
        self._declare("research/computation/kernel")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        first = self.result_of("O001")["infrastructure_sha256"]

        self.run_check("O001")
        self.assertEqual(self.result_of("O001")["infrastructure_sha256"], first)
        (directory / "a.txt").write_text("changed\n", encoding="utf-8")
        payload = validate(self.root)
        self.assert_error_matching(payload, "infrastructure_sha256 does not match")

    def test_directory_metadata_does_not_change_fingerprint(self) -> None:
        import os

        self.new_check()
        directory = self.root / "research" / "computation" / "kernel"
        directory.mkdir()
        source = directory / "source.txt"
        source.write_text("stable\n", encoding="utf-8")
        self._declare("research/computation/kernel")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        before = self.result_of("O001")["infrastructure_sha256"]

        os.utime(directory, (1_700_000_000, 1_700_000_000))
        os.utime(source, (1_700_000_001, 1_700_000_001))
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])
        self.run_check("O001")
        self.assertEqual(self.result_of("O001")["infrastructure_sha256"], before)

    def test_changed_environment_manifest_makes_result_stale(self) -> None:
        self.new_check()
        manifest = self.root / "research" / "environment" / "environment.yml"
        manifest.write_text("name: research\ndependencies: []\n", encoding="utf-8")
        self._declare("research/environment/environment.yml")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        self.assertTrue(validate(self.root)["valid"])

        manifest.write_text("name: research-v2\ndependencies: []\n", encoding="utf-8")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "infrastructure fingerprints do not match")

        self.run_check("O001")
        refreshed = self.result_of("O001")
        self.assertEqual(
            refreshed["infrastructure"][0]["path"],
            "research/environment/environment.yml",
        )
        self.assertTrue(validate(self.root)["valid"], validate(self.root)["errors"])


if __name__ == "__main__":
    unittest.main()
