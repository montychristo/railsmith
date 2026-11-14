# Job redelivery after an uncertain write

A print provider starts a new print for every submission. If it prints and
its reply is lost, a job that records success only after the reply can print
again when the queue redelivers it.

The [job](app/jobs/print_document_job.rb) takes the ID of an existing print
request. The [model](app/models/print_request.rb) changes that request from
`pending` to `unconfirmed` with one conditional PostgreSQL update. Only the
delivery that changed a row can call the provider. The update commits before
that call, so the model rejects execution inside an Active Record transaction.
When the provider replies, the job saves its receipt and marks the request
`submitted`. Missing, submitted and unconfirmed requests are skipped.

Use the same durable request ID on every delivery of the same operation. The
example assumes the request's document stays fixed and its row and state are
retained while any delivery can still arrive. The provider adapter must also
disable automatic submission retries.

An `unconfirmed` request may already have printed, or the worker may have died
before sending it. Surface this state for reconciliation with provider evidence
before anyone authorizes another submission. This deliberately trades automatic
recovery for at most one automatic submission per request. The sample covers
neither request creation and enqueue reliability nor provider reconciliation.
See the [Rails 8.1 Active Job guide](https://guides.rubyonrails.org/v8.1/active_job_basics.html)
for queue and retry behavior and [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
for HTTP retry constraints.

## Run the tests

Use Ruby 3.4 and a disposable PostgreSQL 16 database. Set
`RAILSMITH_EXAMPLE_DATABASE_URL` to its URL with a role that can create schemas.
The [tests](test/print_document_job_test.rb) run serialized Active Job deliveries
against PostgreSQL and a fake printer. They exercise two deliveries while a
provider call is in progress, a lost reply, and a failed local receipt write.
They use no queue backend or real printer.

```sh
gem install minitest --no-document
gem install 'activerecord:~> 8.1.0' 'activejob:~> 8.1.0' --no-document
gem install pg -v '~> 1.6' --no-document
ruby examples/job-redelivery/test/print_document_job_test.rb
```
