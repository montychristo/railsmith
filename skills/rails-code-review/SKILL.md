---
name: rails-code-review
description: Review a Rails diff or PR for evidenced defects and return a quality verdict, separate deployment risk, and verification gaps.
---

# Rails Code Review

Use this for Rails-focused code reviews.

Read:

- `../../core/references/rails-code-review.md`
- `../../docs/voice.md` or a selected profile when drafting comments
- Repo-local guidance before commenting

Defaults:

- Lead with verdict and separate deployment risk, then actionable findings. Use the referenced contract; do not invent a second scoring scheme.
- Prioritise correctness, authorization, data integrity, public contracts, edge cases, performance, tests, and scope.
- Inspect nearby implementation and specs when available.
- Ground findings in file/line evidence.
- Do not approve, request changes, post comments, merge, or mutate PR state unless explicitly asked.
- If there are no worthwhile findings, say that clearly and name what was checked.
