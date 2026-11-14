require "active_job"
require "active_record"
require "minitest/autorun"
require "securerandom"
require_relative "../app/models/print_request"
require_relative "../app/jobs/print_document_job"
require_relative "../db/migrate/20261114000000_create_print_requests"

ActiveJob::Base.logger = nil

# A non-idempotent provider. Every submission represents a new print.
class Printer
  class ReplyLost < StandardError; end

  class << self
    attr_reader :prints
    attr_accessor :after_print

    def reset
      @prints = []
      @after_print = nil
    end

    def submit(document_id)
      @prints << document_id
      receipt = "receipt-#{@prints.length}"
      after_print&.call
      receipt
    end
  end
end

class PrintAfterSuccessJob < ActiveJob::Base
  def perform(request_id)
    request = PrintRequest.find(request_id)
    return if request.status == "submitted"

    receipt = Printer.submit(request.document_id)
    request.update!(status: "submitted", provider_receipt: receipt)
  end
end

class PrintDocumentJobTest < Minitest::Test
  def setup
    Printer.reset
    @schema = "railsmith_example_#{SecureRandom.hex(8)}"
    @pool = ActiveRecord::Base.establish_connection(
      url: ENV.fetch("RAILSMITH_EXAMPLE_DATABASE_URL"),
      schema_search_path: @schema,
      pool: 2,
      connect_timeout: 5,
      variables: { statement_timeout: "5s", lock_timeout: "4s" }
    )
    @pool.with_connection do |connection|
      connection.execute("CREATE SCHEMA #{connection.quote_column_name(@schema)}")
      @schema_created = true
      unless connection.schema_search_path == @schema
        raise "Unexpected search path for the disposable test schema"
      end
      ActiveRecord::Migration.suppress_messages { CreatePrintRequests.new.migrate(:up) }
    end
    PrintRequest.reset_column_information
    @request = PrintRequest.create!(document_id: 42)
    @delivery = PrintDocumentJob.new(@request.id).serialize
  end

  def teardown
    @pool.with_connection { |connection| connection.drop_schema(@schema) } if @schema_created
  ensure
    @pool&.disconnect!
  end

  def test_marking_success_only_after_the_reply_can_print_twice
    delivery = PrintAfterSuccessJob.new(@request.id).serialize
    Printer.after_print = -> { raise Printer::ReplyLost }
    assert_raises(Printer::ReplyLost) { deliver(delivery) }
    assert_equal "pending", @request.reload.status

    Printer.after_print = nil
    deliver(delivery)
    assert_equal [42, 42], Printer.prints
  end

  def test_lost_reply_leaves_an_unconfirmed_request_without_resubmitting
    Printer.after_print = -> { raise Printer::ReplyLost }
    assert_raises(Printer::ReplyLost) { deliver }
    assert_equal "unconfirmed", @request.reload.status
    assert_nil @request.provider_receipt

    deliver
    assert_equal [42], Printer.prints
    assert_equal "unconfirmed", @request.reload.status
  end

  def test_failed_local_success_write_does_not_reopen_submission
    @pool.with_connection do |connection|
      connection.add_check_constraint(
        :print_requests, "status <> 'submitted'", name: "fixture_blocks_success"
      )
    end
    assert_raises(ActiveRecord::CheckViolation) { deliver }
    assert_equal "unconfirmed", @request.reload.status

    @pool.with_connection do |connection|
      connection.remove_check_constraint(:print_requests, name: "fixture_blocks_success")
    end
    deliver
    assert_equal [42], Printer.prints
    assert_equal "unconfirmed", @request.reload.status
    assert_nil @request.provider_receipt
  end

  def test_duplicate_on_another_connection_sees_the_committed_claim
    Printer.after_print = lambda do
      Printer.after_print = nil
      duplicate = Thread.new do
        state = PrintRequest.find(@request.id).status
        deliver
        state
      end
      if duplicate.join(8)
        assert_equal "unconfirmed", duplicate.value
      else
        duplicate.kill.join(2)
        flunk "Duplicate job did not finish"
      end
    end

    deliver
    assert_equal [42], Printer.prints
    assert_equal "submitted", @request.reload.status
    assert_equal "receipt-1", @request.provider_receipt
  end

  def test_completed_delivery_is_skipped_but_a_new_request_for_the_same_document_works
    deliver
    deliver
    assert_equal [42], Printer.prints

    another = PrintRequest.create!(document_id: @request.document_id)
    deliver(PrintDocumentJob.new(another.id).serialize)
    assert_equal [42, 42], Printer.prints
    assert_equal "receipt-2", another.reload.provider_receipt
  end

  def test_outer_transaction_is_rejected_before_any_print
    PrintRequest.transaction do
      assert_raises(ArgumentError) { deliver }
      raise ActiveRecord::Rollback
    end
    assert_empty Printer.prints
    assert_equal "pending", @request.reload.status
  end

  private

  def deliver(delivery = @delivery)
    ActiveJob::Base.execute(delivery.deep_dup)
  end
end
