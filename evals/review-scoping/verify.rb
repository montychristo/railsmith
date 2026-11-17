require "active_record"
require "fileutils"
require "tmpdir"

ActiveRecord::Base.establish_connection(adapter: "sqlite3", database: ":memory:")

ActiveRecord::Schema.define do
  suppress_messages do
    create_table :notices do |table|
      table.references :workspace, null: false
      table.string :title, null: false
      table.string :state, null: false
    end
  end
end

load File.join(__dir__, "notice.rb")
[1, 2].each do |workspace_id|
  %w[published preview draft].each do |state|
    Notice.create!(workspace_id: workspace_id, title: "#{workspace_id} #{state}", state: state)
  end
end

{
  "base" => {
    1 => ["1 published"],
    2 => ["2 published"],
  },
  "a" => {
    1 => ["2 preview", "1 preview", "1 published"],
    2 => ["2 preview", "2 published", "1 preview"],
  },
  "b" => {
    1 => ["1 preview", "1 published"],
    2 => ["2 preview", "2 published"],
  },
}.each do |variant, expected_by_workspace|
  Dir.mktmpdir("review-scoping") do |root|
    model = File.join(root, "app/models/notice.rb")
    FileUtils.mkdir_p(File.dirname(model))
    FileUtils.cp(File.join(__dir__, "notice.rb"), model)
    if variant != "base"
      patch = File.join(__dir__, "#{variant}.diff")
      system("git", "apply", "--whitespace=error", patch, chdir: root, exception: true)
    end

    load model
    expected_by_workspace.each do |workspace_id, expected|
      actual = Notice.visible_to(workspace_id).order(id: :desc).limit(25).pluck(:title)
      label = "#{variant}, workspace #{workspace_id}"
      abort "#{label}: expected #{expected.inspect}, got #{actual.inspect}" unless actual == expected
      puts "#{label}: #{actual.inspect}"
    end
  end
end
