---
name: rails-architecture
description: Use when deciding where Rails code belongs, reviewing architecture, choosing between models/services/queries/policies/forms/components/jobs, or refactoring Rails organization.
---

# Rails Architecture

Use this for Rails code placement and architecture decisions.

Read:

- `../../core/references/rails-architecture.md`
- Repo-local guidance before applying generic advice

Defaults:

- Local app patterns first.
- Rails conventions before bespoke abstractions.
- Keep controllers thin.
- Keep model validations and simple domain behavior in models.
- Use services for real orchestration, side effects, transactions, external APIs, or multi-model flows.
- Use query objects only when a scope would not stay readable.
- Avoid unrelated refactors.
