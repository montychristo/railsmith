# Rails PR Workflow

Use this for branch names, commits, PR descriptions, CI, and publication.

## Branches

Avoid agent/tool prefixes such as `codex/`, `claude/`, `cursor/`, or `ai/`.

Ticketed work:

```text
TICKET-123/short-kebab-description
```

No ticket:

```text
fix/short-kebab-description
feat/short-kebab-description
```

## Commits

Ticketed:

```text
TICKET-123: Add billing retry audit log
```

No ticket:

```text
fix(billing): handle empty retry payload
```

Use imperative mood.

## PR Body

Use the target repo's template when present. If no template exists:

```md
### Summary

- [x] Change one
- [x] Change two

### Context

What problem this solves and why.

### Impact

User, maintainer, data, or deployment impact.

### Validation

- `bundle exec rspec ...` - passed
- `bundle exec rubocop` - passed
```

## Before Review

- Rebase or update from the target branch if the repo expects it.
- Run relevant tests.
- Run style/security checks where relevant.
- Self-review the diff.
- Check for private data in the PR body, screenshots, logs, and commits.
