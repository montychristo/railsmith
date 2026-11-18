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

## RSI-003 — 2026-11-13 — demonstrate database uniqueness under contention

The [database example](../../examples/database-contention/README.md) tests
one reading-list entry per book. A forced interleaving of two check-then-insert
callers without an index produced two rows. With a composite unique index and
a targeted conflict handler, PostgreSQL reported the second writer blocked
before commit. The writers then reported one addition and one duplicate, with
one committed row. Distinct pairs succeeded, a direct duplicate failed, and
the database rejected a null key.

Retain the fixture in CI. All three cases passed on PostgreSQL 16 with Active
Record 8.1, including ten seeded reruns. This covers one committed race at
read-committed isolation. Reassess when the supported database version changes
or the test fails to observe contention.

## RSI-004 — 2026-11-14 — hold an uncertain submission on job redelivery

The [print job example](../../examples/job-redelivery/README.md) exercises
serialized Active Job deliveries with PostgreSQL and a fake printer. The
mark-success-after-reply baseline printed twice when the first reply was lost.
A committed conditional update limited the candidate to one submission per
request after a lost reply or a failed receipt write. A second connection saw
the claim during submission. A new request for the same document succeeded,
and execution inside a transaction was rejected before printing.

Retain the six cases in CI. Unconfirmed requests require reconciliation and
may represent zero or one print. Reassess if an example adds a provider with
documented idempotency or a reliable lookup API.

## RSI-005 — 2026-11-15 — check production build artifacts

The PR workflow gave no production build procedure at `6529609`. In a
disposable Rails 8.1.4.1 and Propshaft 1.3.2 app, the version command and
production precompile both succeeded with a missing stylesheet. Bundler 2.6.2
also rewrote a stale lockfile during an ordinary local install.

The [build reference](../../core/references/rails-runtime-checks.md) reproduced
the fingerprinted stylesheet on Ruby 3.4.2. Its manifest check rejected the
missing asset despite successful precompilation. Frozen install rejected an
out-of-sync Gemfile before precompilation and left the lockfile unchanged.
A local setting that disabled frozen mode was rejected before install.

Retain as an on-demand check for build changes. The exercise used one pipeline
and a disposable app. Reassess when another pipeline needs a worked example.

## RSI-006 — 2026-11-16 — verify each shell entrypoint

The weekly review of RSI-001 through RSI-005 found a recurring evidence gap:
an individual check can pass while the behaviour it appears to cover fails.
The contention, redelivery and build examples each exposed such a gap.
Their synthetic results and the review validator's results establish tool and
fixture behaviour. Agent false alarms, missed findings and host adoption
still need matched evaluations or host-specific checks.

At `01f4012`, the shell command shared by CI and two guides accepted faults
in its second and third arguments. On Bash 3.2, only a fault in the first
script returned a nonzero status. Doctor already parsed scripts with
recognized shell shebangs, so the standalone step was redundant. In disposable
Git fixtures, the old doctor accepted missing entrypoints or malformed
entrypoints without shebangs. The candidate rejects both for each of the three
paths, in the working tree and in the index. A repaired working copy still
leaves a staged failure visible.

Keep one gate in doctor and one contributor checklist. Linking to that
checklist removed 369 bytes from the root agent instructions. Reassess when
an entrypoint changes or the workflow misses a syntax fault.

## RSI-007 — 2026-11-17 — exercise review findings on real queries

At `cfeecb5`, the review controls described expected decisions without a patch
or an executable example of the reported behavior. The
[workspace notice cases](../../evals/review-scoping/README.md) give reviewers the
same request and caller context with one patch at a time. The assessor can
record a missed finding and an unsupported scoping finding separately.

On Active Record 8.1.4.1 and SQLite 3.53.2, the unchanged query returned only
the caller's published notice for either workspace. Patch A also returned the other workspace's
preview, while patch B returned only the local published and preview notices.
Substituting A for B in a scratch copy made the oracle fail on the clean
control. A clean patch pinned to one workspace also failed when called from
the other workspace. This run exercised query behavior. Live reviewer detection and
false-alarm rates remain unmeasured.

Keep the cases for development. Reassess with matched attempts and unseen
cases before drawing conclusions about guidance effectiveness.

## RSI-008 — 2026-11-18 — test a Turbo Drive form in the browser

At `1533f30`, Railsmith had no browser example for Turbo form validation.
The [note form](../../examples/turbo-form/README.md) now tests response status,
draft retention, navigation and the saved row on Rails 8.1.4.1, Turbo Rails
2.0.23 and headless Chrome 157. The request and system tests passed.

In disposable copies, a 200 failure response prevented the validation error
from rendering. Removing Turbo left the request test green but failed the
browser assertion that the original document survived submission.

Keep the example in CI. It covers one Chrome journey with SQLite. Reassess
when a frame or stream needs a different test design.
