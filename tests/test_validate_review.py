"""Check the review decision contract through its local command-line interface."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
CHECKER = ROOT / "scripts/validate_review.py"


class ReviewValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.assessment_path = Path(directory.name) / "assessment.json"
        self.snapshot_path = Path(directory.name) / "snapshot.json"
        self.assessment = json.loads((EVALS / "review-assessment.json").read_text())
        self.current_snapshot = json.loads((EVALS / "review-snapshot.json").read_text())

    def run_validator(self, raw_assessment=None, include_snapshot=True):
        self.assessment_path.write_text(
            json.dumps(self.assessment) if raw_assessment is None else raw_assessment
        )
        self.snapshot_path.write_text(json.dumps(self.current_snapshot))
        command = [sys.executable, str(CHECKER), str(self.assessment_path)]
        if include_snapshot:
            command.extend(["--current-snapshot", str(self.snapshot_path)])
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def assert_invalid(self, message, raw_assessment=None):
        result = self.run_validator(raw_assessment)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertIn(message, result.stderr)
        return result

    def test_high_risk_migration_can_be_green_and_requires_human_review(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "status": "COMPLETE",
            "verdict": "GREEN",
            "deployment_risk": "HIGH",
            "human_review_required": True,
        })

    def test_quality_thresholds_are_independent_of_low_risk(self):
        self.assessment["deployment_risk"] = {"level": "LOW", "reason": "Small reversible change."}
        for area, value, expected in (
            ("functional", 0, "RED"), ("code", 2, "RED"), ("functional", 3, "AMBER"),
            ("docs", 2, "AMBER"), ("docs", 3, "AMBER"), ("docs", 5, "GREEN"),
        ):
            with self.subTest(area=area, value=value):
                score = self.assessment["scores"][area]
                score["value"] = value
                result = self.run_validator()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), {
                    "status": "COMPLETE",
                    "verdict": expected,
                    "deployment_risk": "LOW",
                    "human_review_required": False,
                })
                score["value"] = 4

    def test_blocking_finding_requires_matching_area_score(self):
        self.assessment["findings"] = [{
            "area": "code", "blocking": True,
            "evidence": "The retry can commit the same adjustment twice.",
        }]
        self.assessment["scores"]["functional"]["value"] = 2
        self.assert_invalid("requires a score of 2 or below in its area")
        self.assessment["scores"]["functional"]["value"] = 4
        self.assessment["scores"]["code"]["value"] = 2
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["verdict"], "RED")

    def test_blocking_docs_finding_cannot_yield_green(self):
        self.assessment["findings"] = [{
            "area": "docs", "blocking": True, "evidence": "The recovery steps are missing.",
        }]
        self.assert_invalid("requires a score of 2 or below in its area")
        self.assessment["scores"]["docs"]["value"] = 2
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["verdict"], "AMBER")

    def test_required_verification_unavailable_or_errored_rejects_complete(self):
        for result in ("unavailable", "error"):
            with self.subTest(result=result):
                self.assessment["verification"][0]["result"] = result
                self.assert_invalid("lacks required verification")

    def test_complete_assessment_requires_an_observation(self):
        self.assessment["verification"] = self.assessment["verification"][1:]
        self.assert_invalid("must include an observed check")

    def test_observation_can_be_a_test_failure(self):
        self.assessment["verification"][0]["evidence"] = "Regression failed: total changed."
        self.assessment["scores"]["functional"]["value"] = 2
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["verdict"], "RED")

    def test_incomplete_and_error_withhold_decision_and_return_nonzero(self):
        for status in ("INCOMPLETE", "ERROR"):
            with self.subTest(status=status):
                self.assessment = {"status": status, "reason": "Caller context could not be read."}
                result = self.run_validator(include_snapshot=False)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(json.loads(result.stdout), {"status": status})
                self.assessment["deployment_risk"] = "LOW"
                self.assert_invalid("must contain exactly")

    def test_stale_base_head_or_working_tree_rejects_review(self):
        for key, original in self.current_snapshot.items():
            with self.subTest(changed=key):
                self.current_snapshot[key] = "changed"
                self.assert_invalid("assessment snapshot is stale")
                self.current_snapshot[key] = original

    def test_caller_must_supply_all_snapshot_ids(self):
        result = self.run_validator(include_snapshot=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("requires --current-snapshot", result.stderr)
        del self.current_snapshot["working_tree"]
        self.assert_invalid("current snapshot must contain exactly")

    def test_material_architecture_requires_human_review_and_at_least_medium_risk(self):
        self.assessment["material_architecture"] = True
        self.assessment["deployment_risk"] = {"level": "LOW", "reason": "Expected small footprint."}
        self.assert_invalid("requires at least MEDIUM")
        self.assessment["deployment_risk"]["level"] = "MEDIUM"
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["human_review_required"])

    def test_rejects_supplied_verdict_and_action_fields(self):
        for field in ("verdict", "approve", "merge", "deploy", "human_review_required"):
            with self.subTest(field=field):
                self.assessment[field] = True
                self.assert_invalid("must contain exactly")
                del self.assessment[field]

    def test_rejects_boolean_out_of_range_and_fractional_scores(self):
        for value in (True, -1, 6, 4.5):
            with self.subTest(value=value):
                self.assessment["scores"]["code"]["value"] = value
                self.assert_invalid("must be an integer from 0 to 5")

    def test_requires_reasons_and_finding_evidence(self):
        self.assessment["scores"]["code"]["reason"] = " "
        self.assert_invalid("scores.code.reason must be nonempty")
        self.assessment["scores"]["code"]["reason"] = "The example covers retries."
        self.assessment["findings"] = [{"area": "code", "blocking": False, "evidence": ""}]
        self.assert_invalid("findings[0].evidence must be nonempty")
        self.assessment["findings"] = []
        self.assessment["deployment_risk"]["reason"] = ""
        self.assert_invalid("deployment_risk.reason must be nonempty")

    def test_rejects_invalid_json_and_duplicate_keys_without_echoing_input(self):
        result = self.assert_invalid(
            "duplicate JSON field", '{"example-secret": 1, "example-secret": 2}',
        )
        self.assertNotIn("example-secret", result.stderr)
        self.assert_invalid("could not be read as JSON", "{")
        self.assert_invalid("nonstandard JSON constant", '{"status": NaN}')
