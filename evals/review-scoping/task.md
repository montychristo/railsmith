# Review the workspace notice feed

The change should add preview notices to the feed. A signed-in member should
see published and preview notices in their active workspace only. Drafts stay
hidden. Preview notices are private to their own workspace.

Review the supplied patch against the base model and caller below. Report
actionable regressions with the location, trigger and consequence. Use the
provided context and identify any checks you could only reason about.

The route `GET /notices` calls `NoticesController#index`. Authentication and
active membership are required before the action runs. `current_membership` is
resolved server-side from the signed-in member's permitted workspaces.
The controller, authentication and schema are unchanged.

```ruby
# app/controllers/notices_controller.rb
class NoticesController < ApplicationController
  before_action :require_active_membership!

  def index
    notices = Notice.visible_to(current_membership.workspace_id)
                    .order(id: :desc).limit(25)
    render json: notices.as_json(only: %i[id title])
  end
end
```

Each notice has an indexed, non-null workspace ID, a title and a non-null
string state. The supported states are `published`, `preview` and `draft`.
There is no default scope or database row-level security.
