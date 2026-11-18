require "test_helper"

class NotesResponsesTest < ActionDispatch::IntegrationTest
  test "invalid submissions render 422 and successful writes redirect with 303" do
    get new_note_path
    token = css_select('input[name="authenticity_token"]').sole["value"]
    params = { authenticity_token: token, note: { title: "", body: "Check the garden gate." } }

    post notes_path, params: params
    assert_response :unprocessable_content
    assert_select "li", text: "Title can't be blank"

    params[:note] = { title: "Garden" }
    post notes_path, params: params
    assert_response :see_other
  end
end
