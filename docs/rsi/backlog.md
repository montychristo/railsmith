# Improvement backlog

Ordered by useful outcomes, not a promise to manufacture one commit per row.
Reorder after evidence; keep accepted work in experiments rather than duplicating
the same instructions across documents.

| Order | Improvement | Acceptance evidence |
| --- | --- | --- |
| 1 | Teach safe job retries and uncertain external outcomes | Neutral duplicate/partial-failure example; no blind retry after an uncertain non-idempotent effect; tests prove the exact supported contract. |
| 2 | Add reproducible Rails runtime checks | Resolve versions from the target app, verify dependency locks and production asset build; distinguish build success from configured/live readiness. |
| 3 | Exercise a Turbo journey end to end | Preserve invalid form state, wait for observable navigation completion and verify persisted outcome. State accessibility/visual coverage separately. |
| 4 | Evaluate review usefulness against a baseline | Matched task/model/context/budget, clean cases and seeded faults; report false alarms and misses, not only successes. Keep unseen cases separate from development cases. |
| 5 | Make structure guidance concrete | An autoload-safe namespace move with matching tests, caller evidence and no speculative service layers. |
| 6 | Verify adoption in additional agents | Disposable project fixtures; preserve existing instructions, resolve supporting references, document actual host/version evidence. No personal config changes. |
| 7 | Reduce instruction overhead | Measure loaded bytes and repeated guidance, remove duplication, rerun motivating and counterexample cases. Do not claim token savings without measuring them. |

Weekly review: choose the next item from observed failures or missing value.
Any item may be split, retired or replaced. Automation may improve its checks;
it may not grant itself broader access or relax publication safeguards.
