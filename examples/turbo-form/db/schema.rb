ActiveRecord::Schema[8.1].define do
  create_table :notes, force: :cascade do |t|
    t.string :title, null: false
    t.text :body
  end
end
