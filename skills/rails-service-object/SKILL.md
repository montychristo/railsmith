---
name: rails-service-object
description: Use when creating, reviewing, or refactoring Rails service objects, business operations, POROs, interactors, transactions, side effects, external API orchestration, or service specs.
---

# Rails Service Object

Use services when they remove real complexity.

Good fits:

- Multi-model operations.
- Transactions.
- External API calls.
- Side effects such as jobs, emails, audit logs, or notifications.
- Logic reused from controllers, jobs, rake tasks, or callbacks.

Poor fits:

- One Active Record call.
- Simple validations.
- Simple scopes.
- Wrapping a model method just to make it look "servicey".

Defaults:

- Define the input/output contract first.
- Keep one clear public entrypoint, usually `#call`.
- Inject external dependencies where it helps testing.
- Make transaction boundaries obvious.
- Test success, failure, and side effects.
- Follow existing app result/error conventions.

Before adding a service, ask whether a model method, scope, policy, or query object would be more obvious.
