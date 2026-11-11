# Railsmith

Better Rails development with coding agents. Small skills, clear engineering decisions, runnable examples, and evidence that the workflow is improving.

Railsmith helps an agent find the right boundary, implement a complete operation behind a simple interface, and prove the behaviour that matters. It works with your repository's conventions and test framework. It does not impose a service-object architecture or replace your team's judgement.

## Start with one real change

```sh
git clone https://github.com/montychristo/railsmith.git
cd railsmith
scripts/doctor
```

Give your agent this request, substituting your checkout location:

```text
Read Railsmith's core/AGENTS.md from this checkout. Apply the relevant skill
to this Rails change, respecting our repo instructions. Keep the public
interface small, test the meaningful behaviour, and report verdict and risk
separately. Do not install anything or publish changes unless I ask.
```

For Claude Code, follow the [project-local setup and workflow](docs/claude-code.md). Other agents can read [the core guide](core/AGENTS.md) directly. Existing instructions and permissions remain authoritative. No account, hosted service, or model API key is required to read and use the guidance.

## Engineering direction

- **Narrow interfaces, deep modules.** Callers request a complete capability; the module owns its decisions and invariants. Small files alone do not establish good boundaries.
- **Tests that earn their keep.** Check observable behaviour, failure semantics and invariants. Use a real database or job adapter when those are the boundary being claimed.
- **Predictable Rails structure.** Follow existing naming, autoloading, test layout and result conventions. Introduce a new layer only when it removes demonstrated complexity.
- **Review with a verdict and a risk assessment.** Good code can still be risky to deploy. Missing evidence is visible, not a green result.
- **Measured improvement.** Change one practice, evaluate it, then keep, revise or remove it. Instruction volume and commit count are not success metrics.

## Choose the useful part

| Need | Start here |
| --- | --- |
| Place code or simplify a boundary | [Architecture](skills/rails-architecture/SKILL.md) |
| Implement an operation | [Service objects](skills/rails-service-object/SKILL.md) |
| Keep request handling focused | [Controllers](skills/rails-controller/SKILL.md) |
| Review a Rails change | [Code review](skills/rails-code-review/SKILL.md) |
| Prepare a reviewable contribution | [PR workflow](skills/rails-pr-workflow/SKILL.md) |
| Improve the agent workflow | [Continuous improvement](skills/rails-continuous-improvement/SKILL.md) |
| See a boundary and its tests | [Runnable examples](examples/README.md) |

## How Railsmith improves

[RSI](docs/rsi/README.md) means **recursive self-improvement** here: Railsmith applies its own review and evaluation process to its skills, examples, checks and improvement process. Changes must have a useful outcome and a way to assess it. The loop cannot grant itself new access or publication authority.

The [backlog](docs/rsi/backlog.md) gives the next improvements and their acceptance criteria. [Experiments](docs/rsi/experiments.md) distinguish observed results from proposals. [Evaluation cases](evals/README.md) are public development exercises, not an unseen benchmark or proof of model performance.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Bring a reproducible failure, a clearer example, a better check, or a measured simplification. Keep private project material out of source, fixtures, screenshots, logs and commit messages. Write original neutral examples; changing a client's name is not sufficient anonymisation.

Railsmith is early. Its deterministic checks and Ruby examples are executable; live agent effectiveness and cross-tool adoption need continued evaluation. We publish the evidence and limitations with each improvement.
