# Maintainer Voice Guide

Use this for public-facing Railsmith writing: PR descriptions, review comments, docs, release notes, issue replies, and handoffs.

The default Railsmith voice is:

- Direct and pragmatic.
- Technically precise without being overcomplicated.
- Human, conversational, and low-ceremony.
- Clear about uncertainty.
- Focused on cause, effect, and the next useful action.

## Explanation Pattern

Prefer:

1. What is happening.
2. Why it is happening.
3. What should change.

Example:

```text
This fallback skips the same validation as the normal form path. That means
callers can persist values the UI would usually reject. I think this should
reuse the existing validator rather than adding a second branch here.
```

## Code Review Comments

Use:

```text
P1 blocker - app/services/example_service.rb:42

This can save the fallback value without the normal authorization check. If
that route is hit directly, records can leak outside the expected scope, so
this should use the same scoped query before merge.
```

Rules:

- Lead with the issue.
- Name the file and line when possible.
- Explain the impact.
- Give a concrete fix direction.
- Avoid heavy praise and style nits unless asked.

## PR Descriptions

Prefer:

- Summary.
- Checklist of changes when useful.
- Context or root cause.
- Impact.
- Validation.

Avoid:

- Filler like `This PR...`.
- Vague "improves quality" claims.
- Long implementation walkthroughs.
- Success claims without validation.

## Useful Phrases

- `I think...`
- `worth checking...`
- `probably safest...`
- `unless I'm missing something`
- `not a trivial fix`
- `for now...`

## Avoid

- Corporate phrasing.
- Fake certainty.
- Long setup before the ask.
- Over-apologising.
- AI-flavoured openings like `Great question`.
