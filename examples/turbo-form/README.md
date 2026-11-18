# Test a Turbo Drive form

The [notes controller](app/controllers/notes_controller.rb) renders the invalid
note with HTTP 422. When the note saves, it redirects with HTTP 303 to its show
page. Both responses follow the [Turbo Drive form contract](https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission).

Use Ruby 3.4, Bundler and Chrome with a matching ChromeDriver available to
Selenium. The example uses a local SQLite test database and a temporary Chrome
profile. From the example directory, run:

```sh
bundle install
RAILS_ENV=test bin/rails db:prepare
bin/rails test:all
```

The [request test](test/integration/notes_responses_test.rb) checks HTTP status
codes. The [system test](test/system/notes_test.rb) submits a note with a body
and a blank title. It waits for the validation message, checks the body is
still present, and confirms no row was saved. After correcting the title, it
waits for the destination heading and compares the URL and displayed content
with a fresh read of the only saved row. Capybara waits for these observable
changes without a fixed sleep. A marker in the JavaScript window also survives
both submits, so ordinary full-page navigation cannot satisfy the test.

To check what the browser catches, change the failure render to status 200 in a
disposable copy and run `bin/rails test:system`. The validation message should
never appear. Removing the Turbo script instead leaves the request test green,
but the browser loses its window marker after the first submission.

This exercises one Turbo Drive form in headless Chrome. It does not cover
Turbo Frames or Streams, other browsers, visual layout, or an accessibility audit.
See the [Rails system testing guide](https://guides.rubyonrails.org/v8.1/testing.html#system-testing)
for adapting the test to an existing application.
