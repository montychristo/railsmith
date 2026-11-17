class Notice < ActiveRecord::Base
  def self.visible_to(workspace_id)
    where(workspace_id: workspace_id, state: "published")
  end
end
