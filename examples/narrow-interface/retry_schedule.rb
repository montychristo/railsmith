# A deterministic wait plan. This module does not execute or authorize retries.
module RetrySchedule
  MAX_ATTEMPTS = 1_000

  def self.delays(attempts:, initial_delay:, ceiling:, wait_budget:)
    unless attempts.is_a?(Integer) && attempts.between?(0, MAX_ATTEMPTS)
      raise ArgumentError, "attempts must be an integer between 0 and #{MAX_ATTEMPTS}"
    end
    unless initial_delay.is_a?(Integer) && initial_delay.positive?
      raise ArgumentError, "initial_delay must be a positive integer"
    end
    unless ceiling.is_a?(Integer) && ceiling >= initial_delay
      raise ArgumentError, "ceiling must be an integer at least initial_delay"
    end
    unless wait_budget.is_a?(Integer) && wait_budget >= 0
      raise ArgumentError, "wait_budget must be a non-negative integer"
    end

    remaining = wait_budget
    delay = initial_delay
    Array.new.tap do |plan|
      attempts.times do
        break if delay > remaining

        plan << delay
        remaining -= delay
        delay = [delay * 2, ceiling].min
      end
    end.freeze
  end
end
