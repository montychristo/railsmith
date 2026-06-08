# Rails Code Review Reference

Use this when reviewing Rails code, PRs, local diffs, or patches.

## Review Focus

1. Correctness: does the changed behavior match the requirement?
2. Authorization: are policy/scoped queries applied consistently?
3. Data integrity: validations, transactions, migrations, callbacks, duplicate writes.
4. Public contracts: routes, API payloads, background jobs, events, views, config.
5. Edge cases: nil, empty, missing params, stale records, concurrency, retries, time zones.
6. Performance: N+1s, unbounded queries, missing indexes, expensive sync work.
7. Tests: request/model/service coverage for changed behavior.
8. Rails shape: controllers, models, services, queries, policies in the right places.
9. Scope: unrelated churn or speculative abstractions.

## Suggested Priority Labels

- `P0 blocker`: likely security exposure, data loss, destructive migration, or severe production break.
- `P1 blocker`: broken flow, authorization/data issue, contract break, or important changed behavior without meaningful validation.
- `P2 nice to have`: maintainability, clarity, lower-risk edge case, test coverage, or cleanup.

## Finding Shape

```text
P1 blocker - app/controllers/examples_controller.rb:42

This fallback path skips the policy scope used by the normal action. If the
route is hit directly, it can expose records outside the expected scope, so this
should reuse the existing scoped query before merge.
```

## Evidence Rules

- Check nearby code before commenting when the repo is local.
- Ground comments in file/line evidence.
- Label uncertainty honestly.
- Skip style nits unless asked.
- If there are no worthwhile findings, say that and name what was checked.
