# Recursive self-improvement

Railsmith improves the workflow used to build Rails applications, then uses the
same process to improve Railsmith. The unit of progress is a useful change with
evidence, not another instruction or another commit.

## One bounded loop

1. **Observe.** Choose a reproducible failure, repeated friction, missing example
   or weak check. Record whether the source is observed, reported or proposed.
2. **Bound.** State one hypothesis, acceptance criteria and a counterexample.
   Select the smallest owning layer. Define the baseline before editing.
3. **Change.** Prefer a better implementation, diagnostic or test over prose.
   Otherwise edit a focused reference or skill; keep always-loaded guidance small.
4. **Evaluate.** Run the motivating case and counterexample. Compare like with
   like: model, context, tool access and budget. Capture time or cost only when
   measured. Fixture checks do not establish live model effectiveness.
5. **Review.** A separate reviewer checks the diff, evidence, permission boundary
   and public suitability. Use the verdict/risk contract. Correct failed checks
   before publication; do not lower the bar to finish a run.
6. **Keep, revise or discard.** Record the result and a reassessment trigger.
   An inconclusive experiment is useful evidence but not an improvement claim.

## Record template

Keep concise public records in [experiments.md](experiments.md), with large
reproducers in `evals/` or `examples/`. Private source receipts remain outside
the repository and its Git history.

```text
ID / date / status:
Observed problem and evidence class:
Hypothesis and smallest change:
Baseline (revision, command, environment, result):
Success criterion and counterexample:
Candidate (revision or pending, command, actual result):
Independent review (verdict, risk, material gaps):
Decision: keep / revise / discard / inconclusive
Reassess: date or concrete trigger
```

## Daily and weekly work

A scheduled maintainer aims for one cohesive, verified improvement each day.
Choose from [the backlog](backlog.md), new public feedback or evaluation failures.
If no change earns publication, record a local no-change outcome. Never create
empty commits, cosmetic date churn, invented incidents or fabricated benchmarks.

Once a week, inspect the last seven runs: which changes reduced repeat mistakes,
which added friction, which remain untested, and which guidance should be merged
or removed. Compare accepted fixes, false alarms, incomplete runs, regressions,
and context size where available. Do not substitute stars or commit counts for
utility. Update the backlog and the evaluation cases from these observations.

The weekly pass also evaluates this loop: remove steps that add no evidence,
improve weak checks, and test one process change at a time. The loop cannot change
its source allowlist, write permissions, review gates, spending limits or schedule.
Those decisions belong to the maintainer, outside editable repository content.

## Publication boundary

Use a fresh isolated branch/worktree based on the current remote, preserve other
work, run required checks, review the exact staged contents and commit message,
and verify the remote result. Publication policy is supplied by the maintainer;
this document does not itself authorise a push, approval, merge or deployment.

Learning from an incident does not entitle an agent to publish its details.
Reconstruct the engineering problem with original neutral examples. Omit private
names, source paths, URLs, data shapes and distinctive business workflows. A
regex scan supplements human or independent-agent review; it cannot prove that
all private knowledge has been removed.
