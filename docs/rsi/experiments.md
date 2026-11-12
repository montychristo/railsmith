# Experiments

## RSI-001 — 2026-11-11 — retained foundation

**Problem:** the seed provided useful Rails placement rules but no executable
examples, workflow evaluation loop, separate verdict/risk contract or publication
gate for the exact staged snapshot. Adoption could replace existing instructions.
This was observed by inspecting the seed revision `6dcef03`.

**Hypothesis:** an original runnable module, safer local adoption, explicit review
contract and fail-closed staged checks provide a useful foundation for repeatable
contributions without accumulating untested prose.

**Baseline:** source inspection, not a live model comparison. No claim is made
about changes in coding speed or model defect detection.

**Success criteria:** meaningful example tests pass; adoption preserves existing
instructions and is repeatable; the scanner rejects staged sensitive material
even when the working copy has been cleaned; malformed scanner configuration
fails; an independent review identifies remaining limits.

**Candidate results:** Python's unittest runner passed 34 cases (18 repository
gate cases and 16 adoption cases). The Ruby example passed 12 tests with 400
assertions on Ruby 3.4.2 / Minitest 6.1.0. Shell syntax, repository doctor and
skill metadata validation passed. Adoption tests use disposable Git repositories;
shared instructions remain unchanged and local paths are excluded from Git.

An independent six-scenario rubric walkthrough correctly separated quality from
deployment risk, withheld a verdict with missing required evidence, rejected
contradictory blocker scores, allowed a no-change day and avoided a trivial
service wrapper. This is a manual development exercise, not a matched live-model
experiment or evidence of improved model accuracy.

**Independent review:** found and corrected a scanner path issue (symlinked
parent directories), conflicting backup guidance, and the risk of putting local
installation paths in tracked instructions. The installer now uses an ignored
local bridge. Use the commit and CI run as the exact published snapshot.

**Decision:** keep the deterministic safeguards and example; retain the guidance
as a testable foundation. Live Claude adoption and measured agent effectiveness
remain unverified. **Reassess:** first weekly review, then
whenever a real adoption, review or publication failure contradicts the guidance.

## RSI-002 — 2026-11-12 — validate structured review decisions

The baseline at `69b4c16` specified verdict and risk in prose. A local JSON
validator now derives verdict and human-review requirements and rejects
assessments with missing required verification, contradictory blockers,
mismatched snapshot IDs or action fields.

The synthetic migration assessment returned GREEN with HIGH deployment risk
and required human review. Changing only the current working-tree ID rejected
the same assessment. Fifteen CLI tests cover these cases, incomplete assessments
and malformed input. The validator checks the evidence structure and compares
caller-supplied IDs. It cannot establish that the evidence is accurate or that
the IDs were freshly captured.

Retain as an optional review check. Reassess when a real caller integrates it
or a review exposes a contradiction the validator misses.
