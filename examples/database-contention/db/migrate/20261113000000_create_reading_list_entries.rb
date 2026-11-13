class CreateReadingListEntries < ActiveRecord::Migration[8.1]
  def change
    create_table :reading_list_entries do |table|
      table.bigint :list_id, null: false
      table.bigint :book_id, null: false
      table.index %i[list_id book_id], unique: true
    end
  end
end
