---
name: rails-controller
description: Use when working on Rails controllers, params, REST actions, redirects/renders, request specs, authorization, response handling, Turbo/HTML/JSON branching, or controller review.
---

# Rails Controller

Use this for controller work and request specs.

Defaults:

- Controllers handle HTTP, params, auth, authorization, delegation, and response.
- Keep business logic out of controller actions.
- Prefer RESTful actions and conventional route shapes.
- Keep authorization explicit and consistent with nearby controllers.
- Use strong params or the app's equivalent pattern.
- Prefer request specs for behavior.
- Keep user-facing copy in the app's existing I18n/copy pattern.

Review checklist:

- Does every data access path use the expected authorization/scope?
- Are params constrained before being passed deeper?
- Does the action delegate domain behavior to model/service/query objects?
- Are success and failure responses covered?
- Are redirects, status codes, flash, Turbo, or JSON responses consistent with nearby code?
