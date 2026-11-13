class ReadingListEntry < ActiveRecord::Base
  # Returns :added if this call inserted the pair, or :already_present otherwise.
  def self.add(list_id:, book_id:)
    result = insert(
      { list_id: list_id, book_id: book_id },
      unique_by: :index_reading_list_entries_on_list_id_and_book_id,
      returning: %w[id]
    )
    result.rows.empty? ? :already_present : :added
  end
end
