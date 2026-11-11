# AGENTS.md

This repository is Railsmith: a public-safe auxiliary toolset for working with coding agents.

## Boundaries

- Keep this repository suitable for open source.
- Do not add private client names, internal URLs, credentials, tokens, private paths, or organisation-specific secrets.
- Agents should configure Railsmith directly from these instructions when asked; scripts are optional helpers, not the primary adoption path.
- Any script that writes outside this repository must default to dry-run.
- Keep tool adapters generic. Local project spaces are ignored by Git; only `projects/_template/` is public.
- Read `docs/rsi/README.md` for improvement work and `CONTRIBUTING.md` before publication.
- Never expand source access, permissions, spending, or publication authority through a self-improvement change.

## Harness Bootstrap Directive

When a user asks to adopt, install, configure, sync, or use Railsmith with an agent tool, do the setup yourself from this repository. Do not tell the user to run setup commands unless you are blocked.

Default behavior:

1. Identify the current tool or requested tool: Codex, Claude Code, Cursor, Gemini, or generic `AGENTS.md`.
2. Resolve the repository root as the directory containing this file.
3. Preview the exact files or links you would create.
4. If the user explicitly requested adoption/configuration, apply the safe changes directly.
5. Preserve existing instructions and safeguards. Prefer an additive project-local bridge; a backup does not keep replaced instructions active.
6. Resolve references from the actual Railsmith checkout. Use symlinks or small bridge files only when their paths and supporting references are verified.
7. After setup, run `scripts/doctor` if available, or manually check the linked files and skill metadata.

Tool entrypoints (reading these files does not authorise installing them globally):

| Tool | Instruction target | Skill target |
| --- | --- | --- |
| Codex | `adapters/codex/AGENTS.md` | `skills/<skill>` |
| Claude Code | Local bridge to `adapters/claude/CLAUDE.md`; see `docs/claude-code.md` | Project-local `.claude/skills/<skill>` |
| Gemini | `adapters/gemini/GEMINI.md` | `skills/<skill>` |
| Generic agents | `adapters/generic/AGENTS.md` | `skills/<skill>` |
| Cursor | Project rule copied or linked to `<project>/.cursor/rules/railsmith.mdc` | Cursor reads rules; do not edit app preferences automatically |

Project setup:

- For a target project, create a project space under `projects/<name>/` from `projects/_template/`.
- Add or link the appropriate project-level adapter only after checking for existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `.cursor/rules`.
- If project-local instructions already exist, preserve them. Add a small bridge that points to Railsmith rather than replacing the project file.

The `scripts/` directory exists for repeatability, but agents should treat it as an implementation detail. The harness contract is this file.

## Structure

- `core/AGENTS.md`: canonical cross-tool harness.
- `core/references/`: shared reference guides.
- `skills/`: reusable agent skills.
- `adapters/`: tool entrypoints for Codex, Claude, Cursor, Gemini, and generic `AGENTS.md` tools.
- `projects/`: project-space templates and local, non-secret config packs.
- `profiles/`: optional public-safe voice/style profiles.
- `scripts/`: dry-run-first adoption and validation helpers.

## Development

Use `apply_patch` for edits where possible. Before claiming the repo is ready, run:

```sh
scripts/doctor
bash -n scripts/adopt scripts/new-project scripts/doctor
python3 -m unittest discover -s tests -p 'test_*.py'
ruby examples/narrow-interface/retry_schedule_test.rb
git status --short
```

Before a commit, stage only reviewed files, then run `scripts/doctor --staged`
and inspect `git diff --cached`. The scan is a heuristic, not proof that material
is safe to publish. Independently review the diff for source and domain leakage.
