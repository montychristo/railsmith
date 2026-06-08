# Rails Architecture Reference

Use this when deciding where code should live in a Rails app.

## Placement Heuristic

- Controller: HTTP concerns, params, auth, authorization, delegation, response.
- Model: persistence, associations, validations, scopes, simple domain behavior.
- Service: orchestration, side effects, multi-model flows, external APIs, transactions.
- Query object: complex read models and reporting queries.
- Policy: authorization.
- Form object: multi-model or multi-step form state.
- Component/helper/presenter: display logic, not business rules.
- Job: async work and retries.
- Mailer: email composition and delivery.

## Rails Defaults

Prefer:

- Boring naming.
- Existing app conventions.
- Thin controllers.
- Model validations over controller validation branches.
- Request specs for controller behavior.
- Focused model/service specs for domain behavior.
- Small methods with visible contracts.

Avoid:

- Service objects that wrap a single Active Record call.
- Query objects for simple scopes.
- Callback chains that hide important behavior.
- Unrelated refactors mixed into feature work.
- New result shapes or folder conventions without local precedent.

## Decision Questions

Before adding a new abstraction, ask:

- Does the surrounding app already have a pattern for this?
- Is this code hard to test where it currently lives?
- Is there real orchestration, or just one model operation?
- Does the abstraction make the controller/model easier to understand?
- Can the next maintainer predict where this code lives?
