# Railsmith

Railsmith is a personal auxiliary toolset for working with coding agents.

It packages the useful bits of a strong local agent setup into something portable and reusable:

- Rails skills and review checklists as the first bundled specialism.
- Code review and PR workflow guidance.
- A configurable maintainer voice guide.
- Project-specific config spaces.
- Adapters for Codex, Claude Code, Cursor, Gemini, and generic `AGENTS.md` tools.
- Self-configuration directives agents can follow without a separate installer.

Railsmith is intentionally small. It should be easy to read, fork, extend, and point at real projects without turning into a private knowledge dump.

## Public-Safe By Default

Do not put secrets or private project data in Railsmith. Keep client-specific paths, tokens, internal URLs, Jira sites, Slack examples, and private operational details out of the public repo.

Use `projects/<name>/` for local project spaces, and keep those generic unless you deliberately maintain a private fork.

## Layout

```text
core/
  AGENTS.md                 shared agent harness rules
  references/               detailed review/PR/voice/Rails guidance
skills/
  rails-architecture/       Rails placement and architecture decisions
  rails-code-review/        Rails-focused review workflow
  rails-controller/         controller/request handling guidance
  rails-service-object/     service object guidance
  rails-pr-workflow/        branch, commit, PR, CI, publication guidance
  maintainer-voice/         voice/style guidance
adapters/
  codex/ claude/ cursor/ gemini/ generic/
projects/
  _template/                copyable project config space
profiles/
  chris/voice.md            public-safe maintainer voice profile
scripts/
  adopt                     optional preview/apply helper
  new-project               create a project space
  doctor                    sanity checks
```

## Quick Start

```sh
git clone https://github.com/montychristo/railsmith.git
cd railsmith
scripts/doctor
```

## Adopt With An Agent

Open this repository with Codex, Claude Code, Cursor, Gemini, or another coding agent and ask:

```text
Adopt Railsmith for this agent.
```

The root `AGENTS.md` tells the agent how to configure the relevant adapter and skills directly. The agent should preview target files, avoid overwriting existing config, and use symlinks or small bridge files where appropriate.

For project-specific setup, ask:

```text
Create a Railsmith project space for this repo and wire the relevant agent files.
```

## Optional Script Helpers

Nothing is written unless you pass `--apply`.

```sh
scripts/adopt --tool codex
scripts/adopt --tool claude
scripts/adopt --tool cursor
scripts/adopt --tool generic
```

Apply only when ready:

```sh
scripts/adopt --tool codex --apply --backup
```

`--backup` moves an existing target to `*.bak.<timestamp>` before linking. Without `--backup`, `--apply` refuses to replace existing files.

## Create A Project Space Manually

```sh
scripts/new-project my-rails-app /path/to/my-rails-app
```

This creates:

```text
projects/my-rails-app/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  cursor.mdc
  config.yaml
```

Project spaces are deliberately thin. They route agents to local repo guidance, commands, and conventions without turning Railsmith into a private knowledge dump.

## First Skills

- `rails-architecture`: where code belongs in a Rails app.
- `rails-code-review`: review Rails diffs and PRs.
- `rails-controller`: keep controllers thin and request specs useful.
- `rails-service-object`: use services only when they remove real complexity.
- `rails-pr-workflow`: branch, commit, PR body, CI, and publication checks.
- `maintainer-voice`: write comments, PRs, and handoffs in the maintainer's style.

## Philosophy

- Local repo patterns before generic patterns.
- Rails conventions first when working in Rails apps.
- Small, verifiable changes.
- Review comments should be actionable and evidence-backed.
- PRs should be self-contained and easy to review.
- Voice should sound human, not corporate.
