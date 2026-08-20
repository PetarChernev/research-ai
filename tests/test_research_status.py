"""Status reporting surfaces computational verification state."""

from __future__ import annotations

import unittest

from tests.support import (
    FAILING_CHECK,
    INCONCLUSIVE_CHECK,
    PASSING_CHECK,
    WorkspaceTestCase,
    run_script,
    status,
)


class ComputationalStatusTests(WorkspaceTestCase):
    def test_baseline_reports_an_uninitialized_plan(self) -> None:
        computation = status(self.root)["computational_verification"]
        self.assertTrue(computation["plan_exists"])
        self.assertFalse(computation["plan_initialized"])
        self.assertEqual(computation["obligations_total"], 0)

    def test_obligations_are_counted_by_state(self) -> None:
        self.write_ledger(computational_checks='["O001", "O002", "O003", "O004"]')
        for _ in range(4):
            self.new_check("--claim", "C001")
        self.implement("O001", PASSING_CHECK)
        self.implement("O002", FAILING_CHECK)
        self.implement("O003", INCONCLUSIVE_CHECK)
        for obligation in ("O001", "O002", "O003"):
            self.run_check(obligation)
        self.edit_spec("O004", {"status: active": "status: superseded"})

        computation = status(self.root)["computational_verification"]
        self.assertEqual(computation["active_obligations"], ["O001", "O002", "O003"])
        self.assertEqual(computation["superseded_obligations"], ["O004"])
        self.assertEqual(computation["failed_obligations"], ["O002"])
        self.assertEqual(computation["inconclusive_obligations"], ["O003"])
        self.assertEqual(
            computation["required_active_by_outcome"],
            {"failed": ["O002"], "inconclusive": ["O003"], "passed": ["O001"]},
        )
        self.assertEqual(computation["pending_required_obligations"], [])
        self.assertEqual(computation["claims_blocked_by_required_checks"], ["C001"])

    def test_pending_required_obligation_is_reported(self) -> None:
        self.write_ledger(computational_checks='["O001"]')
        self.new_check("--claim", "C001")
        computation = status(self.root)["computational_verification"]
        self.assertEqual(computation["pending_required_obligations"], ["O001"])
        self.assertEqual(computation["claims_blocked_by_required_checks"], ["C001"])
        gaps = computation["computational_verification_gaps"]
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["claim"], "C001")
        self.assertEqual(gaps[0]["obligations"], ["O001"])

    def test_error_outcome_is_reported(self) -> None:
        self.write_ledger(computational_checks='["O001"]')
        self.new_check("--claim", "C001")
        self.run_check("O001")  # unimplemented scaffold -> execution error
        computation = status(self.root)["computational_verification"]
        self.assertEqual(computation["error_obligations"], ["O001"])
        self.assertEqual(computation["claims_blocked_by_required_checks"], ["C001"])

    def test_settled_claim_reports_no_gap(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        computation = status(self.root)["computational_verification"]
        self.assertEqual(computation["computational_verification_gaps"], [])
        self.assertEqual(computation["claims_blocked_by_required_checks"], [])

    def test_human_readable_output_mentions_obligations(self) -> None:
        completed = run_script("research_status.py", [], self.root)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        for line in (
            "Computation plan:",
            "Machine-check obligations:",
            "Required active obligations by outcome:",
            "Failed/inconclusive/error obligations:",
            "Claims blocked by pending required checks:",
            "Computational verification gaps:",
        ):
            self.assertIn(line, completed.stdout)


if __name__ == "__main__":
    unittest.main()
