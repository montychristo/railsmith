# Improvement backlog

Ordered by useful outcomes, not a promise to manufacture one commit per row.
Reorder after evidence; keep accepted work in experiments rather than duplicating
the same instructions across documents.

| Order | Improvement | Acceptance evidence |
| --- | --- | --- |
| 1 | Evaluate review usefulness against a baseline | Matched task/model/context/budget, clean cases and seeded faults; report false alarms and misses, not only successes. Keep unseen cases separate from development cases. |
| 2 | Verify adoption in additional agents | Disposable project fixtures; preserve existing instructions, resolve supporting references, document actual host/version evidence. No personal config changes. |
| 3 | Reduce instruction overhead | Measure loaded bytes and repeated guidance, remove duplication, rerun motivating and counterexample cases. Do not claim token savings without measuring them. |

The [16 November review](experiments.md#rsi-006--2026-11-16--verify-each-shell-entrypoint)
prioritized review effectiveness because the existing checks establish fixture and
tool behaviour while matched agent results are still missing.

The [workspace notice cases](../../evals/review-scoping/README.md) provide
a verified seeded defect and clean control for development. Matched review
attempts and unseen cases remain open.

Choose the next item from observed failures or missing value.
Any item may be split, retired or replaced. Automation may improve its checks;
it may not grant itself broader access or relax publication safeguards.
