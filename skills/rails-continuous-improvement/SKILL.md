---
name: rails-continuous-improvement
description: Improve a Rails agent workflow or skill from observed failures, repeated friction, or evaluation evidence; define a measurable change and decide whether to keep it.
---

# Rails continuous improvement

Use for improving how development happens, not as extra ceremony for every edit.
Read [the RSI loop](../../docs/rsi/README.md) and its record template.

1. Identify a concrete recurring mistake, missing capability or weak evaluation.
   Distinguish an application defect from environment or harness failure.
2. State one hypothesis and the observable result that would justify the change.
   Capture the baseline before editing. If it is unavailable, say so.
3. Fix the lowest useful layer: code/check/error message, example, focused
   reference, then skill instructions. Edit the existing rule before adding one.
4. Exercise the motivating case and a relevant counterexample. For instructions,
   compare independent baseline and candidate attempts with the same task,
   context and budget where practical; disclose what was actually evaluated.
5. Review correctness, context cost and public suitability independently of the
   authoring pass. Keep, revise or discard the change from that evidence.
6. Record the outcome and next reassessment in the owning repository. Promote
   only reusable lessons; retire stale or duplicative instructions.

Use original synthetic examples in public material. Private code, domains,
operational receipts and source pointers stay outside public Git history.
Do not expand access, permissions, spending or publication authority as part of
improving the loop. A scheduled run can finish without a commit when it found
no justified improvement.
