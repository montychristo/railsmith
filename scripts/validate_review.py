#!/usr/bin/env python3
"""Validate a Railsmith review assessment and derive its decision."""

import argparse
import json
from pathlib import Path
import sys


AREAS = ("functional", "code", "docs")


class AssessmentError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AssessmentError(message)


def fields(value, expected, label):
    require(isinstance(value, dict) and value.keys() == set(expected),
            f"{label} must contain exactly: {', '.join(expected)}")


def required_text(value, label):
    require(isinstance(value, str) and value.strip(), f"{label} must be nonempty text")


def snapshot(value, label):
    keys = ("base", "head", "working_tree")
    fields(value, keys, label)
    for key in keys:
        required_text(value[key], f"{label}.{key}")


def validate_verification(checks):
    require(isinstance(checks, list) and checks, "verification must list checks")
    observed = False
    for index, check in enumerate(checks):
        label = f"verification[{index}]"
        fields(check, ("check", "required", "result", "evidence"), label)
        required_text(check["check"], f"{label}.check")
        required_text(check["evidence"], f"{label}.evidence")
        require(type(check["required"]) is bool, f"{label}.required must be boolean")
        result = check["result"]
        require(result in ("observed", "unavailable", "error"), f"{label}.result is invalid")
        require(not check["required"] or result == "observed",
                f"{label} lacks required verification for a complete assessment")
        observed = observed or result == "observed"
    require(observed, "verification must include an observed check")


def quality_verdict(scores, findings):
    fields(scores, AREAS, "scores")
    for area, score in scores.items():
        label = f"scores.{area}"
        fields(score, ("value", "reason"), label)
        require(type(score["value"]) is int and 0 <= score["value"] <= 5,
                f"{label}.value must be an integer from 0 to 5")
        required_text(score["reason"], f"{label}.reason")

    require(isinstance(findings, list), "findings must be a list")
    for index, finding in enumerate(findings):
        label = f"findings[{index}]"
        fields(finding, ("area", "blocking", "evidence"), label)
        area = finding["area"]
        require(area in AREAS, f"{label}.area is invalid")
        require(type(finding["blocking"]) is bool, f"{label}.blocking must be boolean")
        required_text(finding["evidence"], f"{label}.evidence")
        require(not finding["blocking"] or scores[area]["value"] <= 2,
                f"{label} is a blocker and requires a score of 2 or below in its area")

    if min(scores["functional"]["value"], scores["code"]["value"]) <= 2:
        return "RED"
    if min(score["value"] for score in scores.values()) <= 3:
        return "AMBER"
    return "GREEN"


def decision(assessment, current_snapshot):
    require(isinstance(assessment, dict), "assessment must be an object")
    status = assessment.get("status")
    if status in ("INCOMPLETE", "ERROR"):
        fields(assessment, ("status", "reason"), "assessment")
        required_text(assessment["reason"], "assessment.reason")
        return {"status": status}

    require(status == "COMPLETE", "assessment.status is invalid")
    fields(assessment, ("status", "snapshot", "scores", "findings", "verification",
                        "deployment_risk", "material_architecture"), "assessment")
    require(current_snapshot is not None, "a complete assessment requires --current-snapshot")
    snapshot(current_snapshot, "current snapshot")
    snapshot(assessment["snapshot"], "assessment.snapshot")
    require(assessment["snapshot"] == current_snapshot,
            "assessment snapshot is stale; recheck affected conclusions")
    validate_verification(assessment["verification"])
    verdict = quality_verdict(assessment["scores"], assessment["findings"])

    risk = assessment["deployment_risk"]
    fields(risk, ("level", "reason"), "deployment_risk")
    level = risk["level"]
    require(level in ("LOW", "MEDIUM", "HIGH"), "deployment_risk.level is invalid")
    required_text(risk["reason"], "deployment_risk.reason")
    architecture = assessment["material_architecture"]
    require(type(architecture) is bool, "material_architecture must be boolean")
    require(not architecture or level != "LOW",
            "material architecture requires at least MEDIUM deployment risk")
    return {
        "status": status,
        "verdict": verdict,
        "deployment_risk": level,
        "human_review_required": architecture or level == "HIGH",
    }


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def invalid_constant(_value):
    raise AssessmentError("nonstandard JSON constant")


def read_json(path, label):
    try:
        return json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_object, parse_constant=invalid_constant)
    except AssessmentError as error:
        raise AssessmentError(f"{label}: {error}") from None
    except (OSError, ValueError, RecursionError):
        raise AssessmentError(f"{label} could not be read as JSON") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--current-snapshot", type=Path, help="Required for a complete assessment")
    args = parser.parse_args()
    try:
        assessment = read_json(args.assessment, "assessment")
        current_snapshot = None
        if args.current_snapshot is not None:
            current_snapshot = read_json(args.current_snapshot, "current snapshot")
        result = decision(assessment, current_snapshot)
    except AssessmentError as error:
        print(f"Invalid review: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result))
    return 0 if result["status"] == "COMPLETE" else 2


if __name__ == "__main__":
    sys.exit(main())
