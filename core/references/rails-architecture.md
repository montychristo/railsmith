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

## Narrow interface, deep implementation

A caller should request a complete capability without coordinating its internal
steps. State accepted inputs, result/error shape, owned invariants and side
effects before introducing the boundary. Hide incidental decisions, not facts
callers need to handle failure safely.

Depth is useful logic behind a simple interface, not a target class length.
Apply the deletion test: if removing a wrapper only removes indirection, prefer
removing it. If removal spreads ordering, validation or recovery decisions into
callers, the boundary may be earning its place.

Keep pure decisions separate from persistence and transport when that makes
their behaviour easier to prove. Do not make callers assemble a collection of
tiny helpers into the actual operation. See the original
[retry schedule example](../../examples/narrow-interface/README.md).

## Structure and testing

Use the app's existing namespace and folder conventions, with matching test
paths and Zeitwerk-compatible constant names. Group a capability where its
owner is clear; avoid a parallel framework, generic `utils` dumping ground, or
new folder for every class.

Test the public contract deeply: ordinary results, boundary values, malformed
external inputs, invariants, partial failure and repeated execution where
relevant. Keep tests resilient to internal rearrangement. Real database races,
transaction behaviour and queue delivery need their own integration evidence;
mocked calls cannot establish them.

### Move an existing class into a namespace

In an app with `app/presenters` as a standard autoload root, move an existing
note heading presenter into the notes namespace without changing its interface:

| | Before | After |
| --- | --- | --- |
| File | `app/presenters/note_heading.rb` | `app/presenters/notes/note_heading.rb` |
| Constant | `NoteHeading` | `Notes::NoteHeading` |
| Focused test | `test/presenters/note_heading_test.rb` | `test/presenters/notes/note_heading_test.rb` |
| View call | `NoteHeading.call(@note)` | `Notes::NoteHeading.call(@note)` |

Find references to the old constant, including templates and string lookups.
Preserve the focused test's input and expected output as you update the
reference it calls. Keep the request test on the same route and assert the
rendered heading. Run both tests before and after the move and run the
autoload check. In a Rails app using Minitest with these paths:

```sh
bin/rails zeitwerk:check
bin/rails test test/presenters/notes/note_heading_test.rb test/integration/note_heading_test.rb
```

Moving only the file fails eager loading because Zeitwerk expects
`Notes::NoteHeading`. Leaving the view on `NoteHeading` can pass eager loading
and the focused test, then fail when a request renders the template.
Check the app's configured roots and inflections when deriving the constant.
See the [Rails autoloading guide](https://guides.rubyonrails.org/v8.1/autoloading_and_reloading_constants.html#project-structure).
