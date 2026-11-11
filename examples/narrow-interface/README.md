# A narrow interface with deep tests

A retry policy has rules worth owning in one place: exponential waits, a cap, a total waiting budget, strict inputs and a limit on the size of a plan. A job should not duplicate those rules every time it handles a transient failure.

[`RetrySchedule`](retry_schedule.rb) exposes one operation:

```ruby
waits = RetrySchedule.delays(
  attempts: 5,
  initial_delay: 3,
  ceiling: 10,
  wait_budget: 30
)
# => [3, 6, 10, 10]
```

All durations are integer seconds. The first retry waits `initial_delay`; each subsequent wait doubles until `ceiling`. The result is the longest prefix that fits the waiting budget and attempt count. A partial wait is never substituted to fit another retry. An exact fit is allowed. The returned array is frozen.

The contract rejects invalid inputs with `ArgumentError`, including numeric strings and fractional seconds. `attempts` is between zero and 1,000; the limit prevents an accidental unbounded allocation. The initial delay must be positive, the ceiling at least that delay, and the budget non-negative. The entire policy is validated even for zero attempts. Ruby integer arithmetic preserves large values without float rounding.

## Rails placement and caller responsibility

Place the file at `app/models/retry_schedule.rb` in a Rails application: it is a plain Ruby policy object and needs no Active Record superclass. If the repository already groups these objects in `app/policies`, keep that established structure and verify autoloading. Use the containing capability's namespace when the policy belongs to one feature. Do not create a new folder hierarchy solely for this file.

The caller supplies its policy once, keeps track of the retry index, and passes the selected delay to the existing job scheduler. The module neither owns job persistence nor calls a provider. A job still decides whether an operation is safe to retry and handles exhausted attempts. In particular, a network timeout does not prove a remote write failed; reconcile an uncertain write before scheduling another attempt.

This is a **waiting** budget, not a wall-clock deadline: execution time and queue latency are outside it. Production retry policy may also need jitter, provider-directed backoff and durable attempt accounting. Add those only when the caller's requirements justify them, with tests for the changed contract. Do not layer this plan over an existing scheduler's retry mechanism without deciding which mechanism owns attempts.

## Run and assess

From the repository root, with Ruby and Minitest available:

```sh
ruby examples/narrow-interface/retry_schedule_test.rb
```

The [tests](retry_schedule_test.rb) verify exact boundary outcomes, plateau behavior, input rejection, immutable results, integer precision, prefix stability and policy invariants across a range of inputs. They interact only through the public operation. No database, Rails boot or network is needed.

These checks establish calculation behavior. They do not establish Active Job scheduling, queue delivery, durable retry counts, concurrency, real deadlines or provider idempotency. Test those at their owning boundary when integrating the policy.

The example is small because the problem is bounded. Its useful depth is the set of rules callers can rely on without learning the implementation; splitting each rule into another service would widen the interface without improving ownership.
