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
            "Active exploration portfolio:",
            "Internal critiques:",
            "Final independent-verification nominations:",
            "Approved Opus verification claims:",
        ):
            self.assertIn(line, completed.stdout)

    def test_not_requested_is_not_reported_as_verification_debt(self) -> None:
        self.write_ledger(independent="not-requested")
        payload = status(self.root)
        self.assertEqual(payload["approved_independent_verification_claims"], [])

    def test_only_explicit_pending_claim_is_a_final_nomination(self) -> None:
        self.write_ledger(independent="pending")
        payload = status(self.root)
        self.assertEqual(payload["approved_independent_verification_claims"], ["C001"])

    def test_inconclusive_historical_attempt_is_not_an_approved_queue_item(self) -> None:
        self.write_ledger(independent="inconclusive")
        payload = status(self.root)
        self.assertEqual(payload["approved_independent_verification_claims"], [])

    def test_unapproved_final_candidate_comes_from_state(self) -> None:
        path = self.root / "research" / "STATE.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "## Final independent-verification nominations\n\nNone nominated.",
                "## Final independent-verification nominations\n\n- C007: candidate after convergence",
            ),
            encoding="utf-8",
        )
        payload = status(self.root)
        self.assertEqual(
            payload["final_independent_verification_nominations"],
            ["C007: candidate after convergence"],
        )

    def test_active_exploration_portfolio_comes_from_state(self) -> None:
        path = self.root / "research" / "STATE.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "## Active exploration portfolio\n\nNone.",
                "## Active exploration portfolio\n\n- W-test: D001 and D002",
            ),
            encoding="utf-8",
        )
        payload = status(self.root)
        self.assertEqual(payload["active_exploration_portfolio"], ["W-test: D001 and D002"])


if __name__ == "__main__":
    unittest.main()
