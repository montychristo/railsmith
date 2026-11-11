require "minitest/autorun"
require_relative "retry_schedule"

class RetryScheduleTest < Minitest::Test
  def test_exponential_waits_plateau_at_the_ceiling
    assert_equal [3, 6, 10, 10, 10], plan(attempts: 5, initial_delay: 3, ceiling: 10)
  end

  def test_budget_admits_a_complete_wait_at_the_exact_boundary
    assert_equal [2, 4, 8], plan(wait_budget: 14)
    assert_equal [2, 4], plan(wait_budget: 13)
  end

  def test_budget_never_shortens_a_wait_to_squeeze_in_another_attempt
    assert_equal [2, 4], plan(wait_budget: 7)
  end

  def test_zero_attempts_and_insufficient_budget_return_an_empty_plan
    assert_empty plan(attempts: 0)
    assert_empty plan(wait_budget: 0)
    assert_empty plan(wait_budget: 1)
  end

  def test_a_ceiling_equal_to_the_initial_delay_gives_a_constant_schedule
    assert_equal [5, 5, 5], plan(initial_delay: 5, ceiling: 5, wait_budget: 16)
  end

  def test_large_values_remain_exact_without_float_rounding
    initial = 10**30
    assert_equal [initial, initial * 2], plan(initial_delay: initial, ceiling: initial * 4, wait_budget: initial * 3)
  end

  def test_the_attempt_limit_bounds_output_size
    result = plan(attempts: 1_000, initial_delay: 1, ceiling: 1, wait_budget: 1_001)
    assert_equal 1_000, result.length
    assert_equal 1_000, result.sum
    assert_raises(ArgumentError) { plan(attempts: 1_001) }
  end

  def test_rejects_malformed_policy_values_instead_of_coercing_them
    invalid = {
      attempts: [-1, 1.0, "2", nil, true],
      initial_delay: [0, -1, 2.0, "2", nil, true],
      ceiling: [0, 1, 8.0, "8", nil, true],
      wait_budget: [-1, 20.0, "20", nil, true]
    }
    invalid.each do |field, values|
      values.each do |value|
        assert_raises(ArgumentError, "#{field}=#{value.inspect}") { plan(**{ field => value }) }
      end
    end
  end

  def test_validates_the_whole_policy_even_when_no_attempt_is_requested
    assert_raises(ArgumentError) { plan(attempts: 0, initial_delay: 0) }
    assert_raises(ArgumentError) { plan(attempts: 0, ceiling: 1) }
    assert_raises(ArgumentError) { plan(attempts: 0, wait_budget: -1) }
  end

  def test_callers_cannot_mutate_a_returned_plan
    result = plan
    assert_predicate result, :frozen?
    assert_raises(FrozenError) { result << 99 }
    assert_equal [2, 4, 8, 8], plan
  end

  def test_a_larger_budget_only_extends_the_existing_prefix
    0.upto(40) do |budget|
      smaller = plan(wait_budget: budget)
      larger = plan(wait_budget: budget + 1)
      assert_equal smaller, larger.take(smaller.length)
    end
  end

  def test_policy_invariants_across_a_range_of_inputs
    [1, 3, 7].product([0, 1, 8], [0, 1, 7, 20, 100]).each do |initial, attempts, budget|
      ceiling = initial * 3
      result = plan(attempts: attempts, initial_delay: initial, ceiling: ceiling, wait_budget: budget)

      assert_operator result.length, :<=, attempts
      assert_operator result.sum, :<=, budget
      assert result.all? { |delay| delay.between?(initial, ceiling) }
      assert result.each_cons(2).all? { |first, second| first <= second }
      assert_equal result, plan(attempts: attempts, initial_delay: initial, ceiling: ceiling, wait_budget: budget)
    end
  end

  private

  def plan(**overrides)
    RetrySchedule.delays(**{ attempts: 4, initial_delay: 2, ceiling: 8, wait_budget: 100 }.merge(overrides))
  end
end
