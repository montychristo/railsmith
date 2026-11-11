# Contributing to Railsmith

Make one useful Rails development task easier or more reliable. Describe the
problem, why the change helps, how to verify it and what remains unproven.
Use the repository's existing structure; prefer updating a reference over
adding another always-loaded instruction.

## Check a contribution

From the repository root, with Bash, Git, Python 3 and Ruby with Minitest:

```sh
scripts/doctor
bash -n scripts/adopt scripts/new-project scripts/doctor
python3 -m unittest discover -s tests -p 'test_*.py'
ruby examples/narrow-interface/retry_schedule_test.rb
git diff --check
```

After staging only the intended files, run `scripts/doctor --staged` and inspect
`git diff --cached --check` plus the complete staged diff. Scan failures block
publication. The scanner catches known patterns, not every secret or piece of
private knowledge; a separate content review is required. Never weaken the
gate just to make a daily run pass.

## Evidence

Runnable examples must test behaviour that matters. Guidance changes should
exercise a realistic development case and a counterexample; label a rubric
walkthrough as such, not a live model benchmark. Use
[RSI records](docs/rsi/README.md) for changes to the workflow itself. Add links
to public authoritative sources when behaviour depends on an external version.

Do not add company names, private repository paths, real incident payloads,
customer details, operational URLs or copied proprietary code. Create neutral
examples from the underlying engineering problem. Check commit messages and
test diagnostics as well as files. Public sources still need attribution and
compatible reuse terms; a link is usually better than copying a manual.

## Publication

Use the review contract in [the review reference](core/references/rails-code-review.md).
Commit and push only with the repository owner's applicable authorisation.
Respect protected branches; do not change access settings or bypass protections.
Verify the remote commit and CI result before claiming publication complete.
An uncertain push must be reconciled by reading remote state before any retry.
Review every outgoing commit and its message, not only the final tree: material
added then deleted in an unpublished intermediate commit would still be pushed.
