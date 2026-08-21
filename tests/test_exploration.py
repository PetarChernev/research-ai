"""Breadth-wave derivation allocation and internal-critique validation."""

from __future__ import annotations

import json
import unittest

from tests.support import WorkspaceTestCase, run_script, validate


CRITIQUE = """---
review_kind: internal-critique
target_artifacts: ["research/derivations/D001.md"]
outcome: revision-required
independent: false
reviewer: internal-critic-openai
reviewer_model: openai/gpt-5.6-sol
originating_models: ["openai/gpt-5.6-sol"]
created_at: "2026-08-22T00:00:00Z"
---

# Internal critique

## Scope and independence

This is a same-model internal critique of one frozen derivation, not independent verification.

## Frozen target

The exact target is D001 under its recorded assumptions and validity regime.

## Load-bearing inference

The central algebraic transition controls whether the proposed conclusion follows.

## Reconstruction

The transition can be reconstructed directly, subject to one missing domain condition.

## Falsification attempts

The zero limit, sign reversal, and boundary case were attacked without repairing the source.

## Findings

The omitted domain condition requires a revision before the result can be relied upon.

## Machine-check candidates

Test the central identity in its declared domain and reject samples outside that domain.

## Outcome

revision-required
"""


class DerivationPortfolioTests(WorkspaceTestCase):
    def test_batch_preallocates_distinct_derivations(self) -> None:
        payload = self.new_derivations(
            [
                {"title": "Constructive route", "charter": "Build the object directly."},
                {"title": "No-go route", "charter": "Search for a decisive obstruction."},
            ],
            wave="initial-map",
        )
        self.assertEqual(payload["wave"], "initial-map")
        self.assertEqual(
            [item["id"] for item in payload["derivations"]], ["D001", "D002"]
        )
        for item in payload["derivations"]:
            text = (self.root / item["path"]).read_text(encoding="utf-8")
            self.assertIn('exploration_wave: "initial-map"', text)
            self.assertIn("producer_model: \"openai/gpt-5.6-sol\"", text)
            self.assertIn("## Branch charter", text)
        report = validate(self.root)
        self.assertTrue(report["valid"], report["errors"])

    def test_later_batch_continues_the_stable_ids(self) -> None:
        branch = [{"title": "First", "charter": "Take the first route."}]
        self.new_derivations(branch)
        payload = self.new_derivations(branch, wave="W-next")
        self.assertEqual(payload["derivations"][0]["id"], "D002")

    def test_unknown_target_claim_is_rejected_without_partial_files(self) -> None:
        completed = run_script(
            "new_derivations.py",
            [
                "--wave",
                "W-bad",
                "--branches-json",
                json.dumps(
                    [
                        {"title": "Valid", "charter": "A valid branch."},
                        {
                            "title": "Invalid",
                            "charter": "References an absent claim.",
                            "target_claims": ["C999"],
                        },
                    ]
                ),
                "--json",
            ],
            self.root,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(list((self.root / "research" / "derivations").glob("D*.md")), [])


class InternalCritiqueTests(WorkspaceTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.new_derivations(
            [{"title": "Target", "charter": "Produce a frozen target."}]
        )

    def write_critique(self, content: str = CRITIQUE) -> None:
        path = self.root / "research" / "critiques" / "D001-2026-08-22-openai-01.md"
        path.write_text(content, encoding="utf-8")

    def test_valid_internal_critique_is_counted(self) -> None:
        self.write_critique()
        payload = validate(self.root)
        self.assertTrue(payload["valid"], payload["errors"])
        self.assertEqual(payload["counts"]["critiques"], 1)

    def test_internal_critique_cannot_claim_independence(self) -> None:
        self.write_critique(CRITIQUE.replace("independent: false", "independent: true"))
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "must set independent: false")

    def test_internal_critique_cannot_use_verification_outcome(self) -> None:
        self.write_critique(
            CRITIQUE.replace("outcome: revision-required", "outcome: verified").replace(
                "\nrevision-required\n", "\nverified\n"
            )
        )
        payload = validate(self.root)
        self.assertFalse(payload["valid"])
        self.assert_error_matching(payload, "invalid internal critique outcome 'verified'")


if __name__ == "__main__":
    unittest.main()
