"""Claim/obligation links and the structural computational gate."""

from __future__ import annotations

import unittest

from tests.support import (
    FAILING_CHECK,
    INCONCLUSIVE_CHECK,
    PASSING_CHECK,
    WorkspaceTestCase,
    validate,
)


VERIFICATION_REPORT = """---
claim_id: "C001"
outcome: "verified"
date: "2026-02-01"
verifier: "verifier-anthropic"
verifier_model: "anthropic/claude-sonnet-4-6"
originating_models: ["openai/gpt-5.6-sol"]
source_artifacts: ["research/claims/ledger.yaml"]
---

# Verification report for C001

## Claim tested

The frozen ledger statement was quoted verbatim at the start of the attempt.

## Independence statement

Originating model differs from the verifier model; no code or data was shared.

## Reconstruction

An alternate route reproduced the stated relation from the primary artifacts.

## Falsification attempts

Extreme regimes, sign variants, and an alternate interpretation were attempted.

## Checks

- Dimensions and units: consistent under the declared convention
- Signs and normalization: unchanged under the alternate route
- Symmetries and conservation laws: preserved in the tested regime
- Limiting or exactly soluble cases: agreed with the soluble limit
- Computational reproducibility and convergence: no applicable machine check
- Hidden parameter dependence: none detected in the tested domain

## Computational evidence reviewed

No applicable machine-checkable component exists; the plan records that judgment.

## Sufficiency of computational obligations

Absence of obligations is accepted here because the claim is purely definitional.

## Missing or adversarial checks

A counterexample search would add nothing given the definitional character.

## Computational independence

Nothing computational was shared because no computation supports this claim.

## Findings

No failure was found; residual uncertainty concerns the regime boundary only.

## Outcome

verified, on the basis of an independent alternate reconstruction.

## Required follow-up

Revisit if the regime boundary is widened beyond the stated domain.
"""


class BidirectionalLinkTests(WorkspaceTestCase):
    def test_consistent_links_validate(self) -> None:
        self.write_ledger(computational_checks='["O001"]')
        self.new_check("--claim", "C001")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_claim_listing_an_obligation_that_does_not_target_it_fails(self) -> None:
        self.write_ledger(computational_checks='["O001"]')
        self.new_check()  # no --claim, so O001 targets nothing
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "obligation 'O001' does not target C001")

    def test_active_obligation_not_listed_by_its_claim_fails(self) -> None:
        self.write_ledger()
        self.new_check("--claim", "C001")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "does not list 'O001' under evidence.computational_checks")

    def test_unknown_obligation_reference_fails(self) -> None:
        self.write_ledger(computational_checks='["O009"]')
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "references unknown obligation 'O009'")

    def test_superseded_obligation_need_not_be_listed(self) -> None:
        self.write_ledger()
        self.new_check("--claim", "C001")
        self.edit_spec("O001", {"status: active": "status: superseded"})
        payload = validate(self.root)
        self.assert_no_error_matching(payload, "computational_checks")


class ComputationalGateTests(WorkspaceTestCase):
    GATE = "checks.computational_verification cannot be passed"

    def test_pending_required_obligation_blocks_passed(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, self.GATE)

    def test_failed_required_obligation_blocks_passed(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001")
        self.implement("O001", FAILING_CHECK)
        self.run_check("O001")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, self.GATE)

    def test_inconclusive_required_obligation_blocks_passed(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001")
        self.implement("O001", INCONCLUSIVE_CHECK)
        self.run_check("O001")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, self.GATE)

    def test_all_required_obligations_passing_allows_the_gate(self) -> None:
        self.write_ledger(computational_checks='["O001", "O002"]', computational="passed")
        self.new_check("--claim", "C001")
        self.new_check("--claim", "C001")
        for obligation in ("O001", "O002"):
            self.implement(obligation, PASSING_CHECK)
            self.run_check(obligation)
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_optional_failing_obligation_does_not_block_the_gate(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001", "--optional")
        self.implement("O001", FAILING_CHECK)
        self.run_check("O001")
        payload = validate(self.root)
        self.assert_no_error_matching(payload, self.GATE)

    def test_superseded_failing_obligation_does_not_block_the_gate(self) -> None:
        self.write_ledger(computational_checks='["O001"]', computational="passed")
        self.new_check("--claim", "C001")
        self.implement("O001", FAILING_CHECK)
        self.run_check("O001")
        self.edit_spec("O001", {"status: active": "status: superseded"})
        self.run_check("O001")  # refresh hashes after the spec edit
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])
        self.assertTrue((self.root / "research" / "checks" / "O001" / "result.json").is_file())


class VerifiedStatusTests(WorkspaceTestCase):
    def _write_report(self) -> None:
        directory = self.root / "research" / "results" / "verification"
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "C001-2026-02-01.md").write_text(VERIFICATION_REPORT, encoding="utf-8")

    def test_verified_claim_with_unsatisfied_required_obligation_fails(self) -> None:
        self._write_report()
        self.write_ledger(
            status="verified",
            computational_checks='["O001"]',
            verification='["research/results/verification/C001-2026-02-01.md"]',
            dimensional="passed",
            limiting="passed",
            computational="not-applicable",
            independent="passed",
        )
        self.new_check("--claim", "C001")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "verified status requires every active required obligation")

    def test_claim_without_obligations_can_still_be_verified(self) -> None:
        self._write_report()
        self.write_ledger(
            status="verified",
            verification='["research/results/verification/C001-2026-02-01.md"]',
            dimensional="passed",
            limiting="passed",
            computational="not-applicable",
            independent="passed",
        )
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])

    def test_verified_requires_an_explicit_computational_verification_state(self) -> None:
        self._write_report()
        self.write_ledger(
            status="verified",
            verification='["research/results/verification/C001-2026-02-01.md"]',
            dimensional="passed",
            limiting="passed",
            computational="pending",
            independent="passed",
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(
            payload, "verified status requires an explicit passing computational_verification check"
        )

    def test_verified_claim_with_all_required_obligations_passing_is_allowed(self) -> None:
        self._write_report()
        self.write_ledger(
            status="verified",
            computational_checks='["O001"]',
            verification='["research/results/verification/C001-2026-02-01.md"]',
            dimensional="passed",
            limiting="passed",
            computational="passed",
            independent="passed",
        )
        self.new_check("--claim", "C001")
        self.implement("O001", PASSING_CHECK)
        self.run_check("O001")
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])


class LedgerSchemaTests(WorkspaceTestCase):
    def test_old_schema_version_is_rejected(self) -> None:
        path = self.root / "research" / "claims" / "ledger.yaml"
        path.write_text("schema_version: 1\nclaims: []\n", encoding="utf-8")
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "schema_version must be 2")

    def test_legacy_check_field_is_rejected(self) -> None:
        self.write_ledger()
        path = self.root / "research" / "claims" / "ledger.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "computational_verification: pending", "numerical_reproduction: pending"
            ),
            encoding="utf-8",
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "missing required field 'computational_verification'")

    def test_missing_computational_checks_evidence_is_rejected(self) -> None:
        self.write_ledger()
        path = self.root / "research" / "claims" / "ledger.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").replace("      computational_checks: []\n", ""),
            encoding="utf-8",
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "missing required field 'computational_checks'")


if __name__ == "__main__":
    unittest.main()
