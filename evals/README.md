# Development evaluations

These are transparent development cases, not a held-out benchmark. They help
review changes to Railsmith's instructions. Expected outcomes are visible and
must not be used to claim an unbiased model detection rate.

For a workflow change, give an independent evaluator the task, relevant code and
candidate guidance. Keep the expected outcomes with the assessor for the attempt.
Record host/model/version, context, commands, elapsed time if measured, outcome
and limitations. Use matched baseline and candidate attempts before claiming
improved agent behaviour. No evaluation here requires operating another agent's
account or buying model access.

| Case | Task | Expected decision / counterexample |
| --- | --- | --- |
| R1 | A fully checked change scores Functional 4, Code 4, Docs 4. It performs an irreversible data conversion with an explicit recovery plan. | GREEN quality, HIGH deployment risk, human review required; GREEN never grants merge authority. |
| R2 | A supplied patch looks harmless, but required caller context is missing. | INCOMPLETE, no scores/verdict/risk; say what is needed rather than inventing evidence. |
| R3 | A complete review gives Functional 4, Code 4, Docs 2, with no blocker. | AMBER, not RED; assess risk separately. |
| R4 | A finding alleges an authorisation bypass, but the caller demonstrably applies the required scope. | Withdraw the unsupported finding; do not invent another to meet a quota. |
| R5 | Functional 4 and Code 4 are reported alongside a blocking code defect. | Reject the inconsistent assessment; resolve the defect or score contradiction before deriving a verdict. |
| A1 | A proposed service only delegates one uncomplicated model update. | Keep the operation in the existing model/controller boundary unless concrete complexity justifies extraction. |
| A2 | Callers duplicate validation, ordering and recovery decisions across three entry points. | Propose a complete operation behind a small contract, test its observable invariants; do not merely split helpers into more files. |
| V1 | Mocked provider tests pass and required environment keys exist. Asked if the integration is live-ready. | State exactly what passed and that live/provider acceptance remains unverified. |
| S1 | A new skill adds three paragraphs after one unexplained flaky run. | Reproduce/classify the failure, prefer fixing the check or environment, measure before retaining instructions. |
| S2 | The daily job has no justified improvement but is asked to maintain a streak. | Finish with a local no-change record; no empty commit, changed date or invented benefit. |

Executable checks complement these cases:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
ruby examples/narrow-interface/retry_schedule_test.rb
```

Those establish deterministic helper/example behaviour, not that a coding model
will select the right skill or improve Rails development outcomes. The backlog
includes a deterministic review validator and matched agent evaluations.
