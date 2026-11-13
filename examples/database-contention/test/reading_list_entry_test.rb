require "active_record"
require "minitest/autorun"
require "securerandom"
require_relative "../app/models/reading_list_entry"
require_relative "../db/migrate/20261113000000_create_reading_list_entries"

class ReadingListEntryTest < Minitest::Test
  PAIR = { list_id: 1, book_id: 10 }.freeze
  CHECKPOINT_TIMEOUT = 5
  WORKER_TIMEOUT = 12

  def setup
    @schema = "railsmith_example_#{SecureRandom.hex(8)}"
    @pool = ActiveRecord::Base.establish_connection(
      url: ENV.fetch("RAILSMITH_EXAMPLE_DATABASE_URL"),
      schema_search_path: @schema,
      pool: 2,
      checkout_timeout: CHECKPOINT_TIMEOUT,
      connect_timeout: CHECKPOINT_TIMEOUT,
      variables: { statement_timeout: "10s", lock_timeout: "8s" }
    )

    @pool.with_connection do |connection|
      connection.execute("CREATE SCHEMA #{connection.quote_column_name(@schema)}")
      @schema_created = true
      unless connection.schema_search_path == @schema
        raise "Unexpected search path for the disposable test schema"
      end
      ActiveRecord::Migration.suppress_messages do
        CreateReadingListEntries.new.migrate(:up)
      end
    end
    ReadingListEntry.reset_column_information
  end

  def teardown
    @pool.with_connection { |connection| connection.drop_schema(@schema) } if @schema_created
  ensure
    @pool&.disconnect!
  end

  def test_check_then_insert_can_duplicate_a_pair
    @pool.with_connection do |connection|
      connection.remove_index(:reading_list_entries, %i[list_id book_id])
    end
    checked = Queue.new
    resume = Queue.new

    @pool.with_connection do |connection|
      worker = Thread.new do
        @pool.with_connection do |other|
          add_if_missing do
            checked << other.select_value("SELECT pg_backend_pid()")
            checkpoint(resume)
          end
        end
      end

      begin
        refute_equal connection.select_value("SELECT pg_backend_pid()"), checkpoint(checked)
        assert add_if_missing
      ensure
        resume << true
        finish(worker)
      end
    end

    assert_equal 2, ReadingListEntry.where(PAIR).count
  end

  def test_unique_index_resolves_two_overlapping_inserts
    started = Queue.new
    worker = nil

    @pool.with_connection do |connection|
      writer_pid = connection.select_value("SELECT pg_backend_pid()")

      begin
        connection.transaction(isolation: :read_committed) do
          assert_equal :added, ReadingListEntry.add(**PAIR)
          worker = Thread.new do
            @pool.with_connection do |other|
              started << other.select_value("SELECT pg_backend_pid()")
              ReadingListEntry.add(**PAIR)
            end
          end
          contender_pid = checkpoint(started)
          refute_equal writer_pid, contender_pid
          assert_blocked_by(connection, contender_pid, writer_pid)
        end
      ensure
        contender_result = finish(worker) if worker
      end

      assert_equal :already_present, contender_result
    end

    assert_equal 1, ReadingListEntry.where(PAIR).count
  end

  def test_index_protects_direct_writes_and_allows_distinct_pairs
    assert_equal :added, ReadingListEntry.add(**PAIR)
    assert_equal :added, ReadingListEntry.add(list_id: 2, book_id: 10)
    assert_equal :added, ReadingListEntry.add(list_id: 1, book_id: 11)
    assert_raises(ActiveRecord::RecordNotUnique) { ReadingListEntry.insert!(PAIR) }
    assert_raises(ActiveRecord::NotNullViolation) { ReadingListEntry.add(list_id: nil, book_id: 10) }
    assert_equal 3, ReadingListEntry.count
  end

  private

  def add_if_missing
    return false if ReadingListEntry.exists?(PAIR)

    yield if block_given?
    ReadingListEntry.create!(PAIR)
  end

  def checkpoint(queue)
    queue.pop(timeout: CHECKPOINT_TIMEOUT) || flunk("Worker did not reach the checkpoint")
  end

  def finish(worker)
    return worker.value if worker.join(WORKER_TIMEOUT)

    worker.kill.join(CHECKPOINT_TIMEOUT)
    flunk("Worker did not finish")
  end

  def assert_blocked_by(connection, contender_pid, writer_pid)
    deadline = Process.clock_gettime(Process::CLOCK_MONOTONIC) + CHECKPOINT_TIMEOUT
    loop do
      return if connection.select_value(
        "SELECT #{Integer(writer_pid)} = ANY(pg_blocking_pids(#{Integer(contender_pid)}))"
      )
      flunk("PostgreSQL did not report the contender waiting for the writer") if
        Process.clock_gettime(Process::CLOCK_MONOTONIC) >= deadline

      sleep 0.01
    end
  end
end
