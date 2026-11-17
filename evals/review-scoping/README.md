# Workspace notice review cases

These are public development cases. The expected outcomes below are for the
assessor. Send each reviewer [the task](task.md), [the base model](notice.rb)
and just one patch ([A](a.diff) or [B](b.diff)). Identify the base model as
`app/models/notice.rb`. Use a context where the reviewer cannot read this page, the other patch or
the oracle. Use the same patch filename in each attempt.

To compare guidance, use a fresh attempt for each patch and each guidance
version. Keep the task, model, tool access and budget fixed. Record the two
guidance revisions and preserve the raw reports before scoring. Public cases
can guide development. Use unseen cases for a separate effectiveness check.

| Patch | Expected result | How to score |
| --- | --- | --- |
| A | The unscoped preview operand lets a workspace 1 member see a workspace 2 preview's ID and title. | Count a detection when the report connects the unscoped operand to a foreign preview in the feed. Count a miss when that chain is absent. |
| B | Each operand is constrained to the active workspace. Only local published and preview notices reach the feed. | Count a claim of cross-workspace exposure as a false alarm. |

Record incomplete attempts separately. Record any additional reported
regressions and adjudicate them on their evidence. With one seeded defect and
one clean control, report counts and the individual results.

## Verify the case evidence

With Ruby 3.4, Active Record 8.1, sqlite3 2.x and Git installed, run from the
repository root:

```sh
ruby evals/review-scoping/verify.rb
```

The script applies the supplied patches in temporary directories and evaluates
the resulting model queries with an in-memory SQLite database. It checks the
exact returned titles for both workspaces as callers, using published, preview
and draft rows in each workspace. It exercises the relation used by the
controller. Authentication, request routing and serialization are supplied as
review context. See [Active Record's `or` method](https://api.rubyonrails.org/v8.1.0/classes/ActiveRecord/QueryMethods.html#method-i-or).
