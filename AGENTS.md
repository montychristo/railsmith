# AGENTS.md

This repository is Railsmith: a public-safe auxiliary toolset for working with coding agents.

## Boundaries

- Keep this repository suitable for open source.
- Do not add private client names, internal URLs, credentials, tokens, private paths, or organisation-specific secrets.
- Agents should configure Railsmith directly from these instructions when asked; scripts are optional helpers, not the primary adoption path.
- Any script that writes outside this repository must default to dry-run.
- Keep tool adapters generic. Project-specific details belong in `projects/`.

## Harness Bootstrap Directive

When a user asks to adopt, install, configure, sync, or use Railsmith with an agent tool, do the setup yourself from this repository. Do not tell the user to run setup commands unless you are blocked.

Default behavior:

1. Identify the current tool or requested tool: Codex, Claude Code, Cursor, Gemini, or generic `AGENTS.md`.
2. Resolve the repository root as the directory containing this file.
3. Preview the exact files or links you would create.
4. If the user explicitly requested adoption/configuration, apply the safe changes directly.
5. Never overwrite existing user config. If a target exists, create a backup with a timestamp or ask before replacing it.
6. Prefer symlinks when the tool supports normal filesystem files; use small bridge files when symlinks are inappropriate.
7. After setup, run `scripts/doctor` if available, or manually check the linked files and skill metadata.

Tool targets:

| Tool | Instruction target | Skill target |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` -> `adapters/codex/AGENTS.md` | `~/.codex/skills/<skill>` -> `skills/<skill>` |
| Claude Code | `~/.claude/CLAUDE.md` -> `adapters/claude/CLAUDE.md` | `~/.claude/skills/<skill>` -> `skills/<skill>` |
| Gemini | `~/.gemini/GEMINI.md` -> `adapters/gemini/GEMINI.md` | `~/.gemini/skills/<skill>` -> `skills/<skill>` |
| Generic agents | `~/.agents/AGENTS.md` -> `adapters/generic/AGENTS.md` | `~/.agents/skills/<skill>` -> `skills/<skill>` |
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
git status --short
```
