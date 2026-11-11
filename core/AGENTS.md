# Railsmith Core Harness

Use this as the shared rule set for Railsmith-assisted agent work.

## Precedence

Follow the most specific applicable instruction:

1. Direct user instructions in the current thread.
2. Repo-local `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or equivalent.
3. Project space guidance in `projects/<name>/`.
4. This core harness.
5. Tool defaults.

## Working Rules

- Keep Railsmith public-safe: no secrets, private URLs, private project names, or internal credentials.
- Read repo-local guidance before editing.
- Prefer the target app's existing patterns over generic advice.
- Keep changes scoped and verifiable.
- Use `rg`/`rg --files` for local search when available.
- Use `gh` for GitHub PR/CI context when available.
- Do not use agent/tool prefixes in branch names.
- Run relevant tests or checks before claiming work is complete.

## Self-Configuration

When the user asks to adopt, install, configure, or sync Railsmith, configure the harness directly instead of asking the user to run scripts.

- Use the root `AGENTS.md` Harness Bootstrap Directive as the source of truth.
- Preview target paths before writing.
- Preserve active instructions and safeguards with an additive project-local bridge. A backup is not a substitute for keeping them active.
- Prefer symlinks to keep adapters and skills updated from this repo.
- Treat `scripts/adopt` and `scripts/new-project` as optional helpers, not required steps.

## Rails Defaults

When working in Rails apps:

- Controllers handle HTTP, params, auth, authorization, delegation, and response.
- Models own persistence, associations, validations, scopes, and simple domain behavior.
- Services are for orchestration, side effects, multi-model flows, external APIs, or transactions.
- Prefer complete capabilities behind narrow public interfaces. Keep internal sequencing and invariants inside the owning module; use existing result/error conventions.
- Query objects are for complex read models, not simple scopes.
- Policies own authorization.
- User-facing copy should follow the app's existing I18n convention.
- Prefer request specs for controller behavior.
- Prefer model/service specs for domain behavior.
- Exercise failure semantics and durable invariants, not private helper call counts. Use database/job integration checks when those behaviours are claimed.
- Keep one canonical source for each engineering rule and route to it; do not duplicate whole guides across adapters.

## Skill Routing

- Rails architecture or placement decisions: `skills/rails-architecture`.
- Rails code review: `skills/rails-code-review`.
- Controllers and request specs: `skills/rails-controller`.
- Service objects: `skills/rails-service-object`.
- PRs, branches, commits, CI, publication: `skills/rails-pr-workflow`.
- Voice/style for review comments, PRs, docs, handoffs: `skills/maintainer-voice`.
- Repeated agent failures, skill improvement or RSI: `skills/rails-continuous-improvement`.

## Browser Verification

Do not foreground a user's browser during routine verification. Prefer background browser contexts, screenshots, DOM snapshots, `curl`, tests, and logs.

## Completion

Do not say work is done without fresh evidence:

1. Identify the command or check that proves it.
2. Run it.
3. Read the output and exit code.
4. Report the result and any gaps.

For reviews, use the verdict and independent deployment-risk contract in
`core/references/rails-code-review.md`. A review result never grants publication,
approval, merge or deployment permission.
