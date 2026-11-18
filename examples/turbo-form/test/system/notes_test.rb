require "test_helper"

class NotesTest < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome

  test "correcting an invalid note preserves the draft and saves it through Turbo" do
    body = "Check the garden gate."
    visit new_note_path
    # A native form submission would replace this document.
    page.execute_script("window.noteFormDocument = true")
    fill_in "Body", with: body
    click_button "Save note"

    assert_selector "li", text: "Title can't be blank", exact_text: true
    assert_field "Body", with: body
    assert_equal true, page.evaluate_script("window.noteFormDocument"),
      "Expected Turbo Drive to render validation errors in the existing document"
    assert_equal 0, Note.count

    fill_in "Title", with: "Garden"
    click_button "Save note"

    assert_selector "h1", exact_text: "Garden"
    assert_selector "p", exact_text: body
    assert_equal true, page.evaluate_script("window.noteFormDocument"),
      "Expected Turbo Drive to render the destination in the existing document"
    note = Note.sole
    assert_current_path note_path(note)
    assert_equal ["Garden", body], [note.title, note.body]
  end
end
