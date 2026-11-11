# Railsmith for Claude Code

The Git-ignored `CLAUDE.local.md` adoption bridge imports the shared core from the resolved
Railsmith checkout. Follow the target repository's own instructions first.

Before editing Rails code, inspect the relevant entry point, neighboring patterns,
and tests. Invoke the smallest matching Railsmith skill; its supporting references
are relative to the original skill directory, not the target app's working directory.
Resolve symlinked skill paths before following those references.

Keep context focused: load architecture guidance for placement decisions, review
guidance for reviews, and verification guidance for the changed risk surface.
State observed behavior separately from assumptions, and never report a check as
passed unless it ran against the relevant changes.

If asked to adopt Railsmith, preview `scripts/adopt --project <target>` from the
Railsmith checkout. Apply only within the requested target. Preserve existing
instructions and skills; never replace global Claude configuration.

See the source checkout's `docs/claude-code.md` for usage and compatibility notes.
