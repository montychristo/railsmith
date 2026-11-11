# Claude Code in a Rails repository

Railsmith supplies reusable engineering guidance. Your app owns its business rules,
commands, conventions and release permissions.

From a Railsmith checkout, preview adoption into an existing app:

```sh
scripts/adopt --project /path/to/rails-app
scripts/adopt --project /path/to/rails-app --apply
```

Python 3 and Git are required; the target must be the app's Git repository root.
The default is a dry run. The installer adds a marked bridge to `CLAUDE.local.md`,
imports an existing `AGENTS.md`, and links skill directories under `.claude/skills/`.
It leaves `CLAUDE.md` and `AGENTS.md` unchanged and preserves existing local content.
Tracked installation targets, existing skills and conflicting symlinks are refused
before any write. Repeating the same command makes no further changes.

The installer appends exact exclusions for the local bridge and installed skill
links to `.gitignore`, preserving its previous contents. It verifies Git actually
ignores those paths before creating them. If nested ignore rules override the
exclusions, it restores `.gitignore` and stops. No `.git` or global config is edited.

The bridge contains the resolved Railsmith location. If you move that checkout,
review and remove its old installer-created skill links before rerunning adoption.
Generated paths and links are machine-specific and Git-ignored. The added
`.gitignore` rules contain no machine paths and can be committed. For shared team
setup, agree a portable repository layout and
review its bridge separately. Remove only the marked block and installer-created
links to undo adoption; preserve any pre-existing `CLAUDE.local.md` content. Remove
the added ignore entries only when those paths no longer need exclusion.

## A useful working loop

1. Name the observable behavior and inspect the app's existing implementation.
2. Select the relevant architecture, controller, service or review skill.
3. Keep the public interface small; put complexity behind that boundary.
4. Exercise failure paths and invariants through the public interface. For jobs,
   include repeated execution; for database changes, include realistic constraints.
5. Review with a verdict, risk, concrete findings and verification evidence.
6. Record a reusable lesson only when evidence justifies changing future work.

For example: “Use Railsmith to review this job's retry behavior. Identify observable
failure modes, propose the smallest regression check, and report verdict plus risk.”

## Compatibility

Claude Code documents project skills at `.claude/skills/<name>/SKILL.md`; skill
content is loaded when invoked. See the official [skills guide](https://code.claude.com/docs/en/skills).
Its [memory guide](https://code.claude.com/docs/en/memory) describes `@` imports.
The installer escapes spaces in import paths; quoted paths do not load. Claude
may request approval for these external imports on first use.
Claude loads `CLAUDE.local.md` alongside shared instructions. The local import
bridge keeps shared instructions explicit across versions with
different native `AGENTS.md` support. Documentation checked 11 November 2026;
installer tests do not demonstrate behavior in an installed Claude session.

The installer now supports project-local Claude adoption only. Legacy global
installation, `--tool all`, other tool modes and `--backup` are refused. The other
adapters remain available for a reviewed project-local setup; no global settings
are migrated automatically.
