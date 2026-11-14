class CreatePrintRequests < ActiveRecord::Migration[8.1]
  def change
    create_table :print_requests do |table|
      table.bigint :document_id, null: false
      table.string :status, default: "pending", null: false
      table.string :provider_receipt
    end
  end
end
