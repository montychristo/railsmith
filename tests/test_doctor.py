"""Exercise publication checks against disposable Git repositories."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "scripts/check_repository.py"
REQUIRED = (
    "README.md", "AGENTS.md", "core/AGENTS.md", "docs/voice.md",
    "profiles/chris/voice.md", "adapters/codex/AGENTS.md",
    "adapters/claude/CLAUDE.md", "adapters/cursor/rules/railsmith.mdc",
)


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.env = {
            key: value for key, value in os.environ.items()
            if not key.startswith(("GIT_", "RAILSMITH_PRIVATE_"))
        }
        self.git("init", "-q")
        for path in REQUIRED:
            self.write(path, "# Public guide\n")
        self.write("skills/example/SKILL.md", "---\nname: example\ndescription: Example skill\n---\n")
        self.git("add", ".")

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode() if isinstance(content, str) else content)

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args], env=self.env,
            capture_output=True, check=True,
        )

    def check(self, staged=False, env=None, root=None):
        args = [sys.executable, str(CHECKER), str(root or self.root)]
        if staged:
            args.append("--staged")
        return subprocess.run(args, env={**self.env, **(env or {})}, text=True, capture_output=True)

    def assert_failed(self, result, message):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def test_benign_working_tree_and_index_pass(self):
        self.assertEqual(self.check().returncode, 0)
        self.assertEqual(self.check(staged=True).returncode, 0)

    def test_home_path_rejected_without_echoing_content(self):
        private_path = "/" + "Users" + "/example/private"
        self.write("notes.md", private_path)
        result = self.check()
        self.assert_failed(result, "Private pattern detected")
        self.assertNotIn(private_path, result.stderr)

    def test_credential_marker_rejected(self):
        self.write("key.txt", "-----BEGIN " + "PRIVATE KEY-----")
        self.assert_failed(self.check(), "Private pattern detected")

    def test_staged_secret_cannot_be_hidden_by_safe_working_copy(self):
        self.write("notes.md", "sk-" + "a" * 30)
        self.git("add", "notes.md")
        self.write("notes.md", "Public replacement\n")
        self.assertEqual(self.check().returncode, 0)
        self.assert_failed(self.check(staged=True), "Private pattern detected")

    def test_unstaged_secret_does_not_change_index_scan(self):
        self.write("notes.md", "Public content\n")
        self.git("add", "notes.md")
        self.write("notes.md", "sk-" + "b" * 30)
        self.assert_failed(self.check(), "Private pattern detected")
        self.assertEqual(self.check(staged=True).returncode, 0)

    def test_extra_private_terms_are_literal_case_insensitive_and_not_printed(self):
        self.write("notes.md", "Synthetic.Client+Name\n")
        result = self.check(env={"RAILSMITH_PRIVATE_TERMS": "other term\nsynthetic.client+name"})
        self.assert_failed(result, "Private pattern detected")
        self.assertNotIn("Synthetic.Client", result.stderr)

    def test_extra_regex_extends_default_rules(self):
        self.write("notes.md", "sk-" + "c" * 30)
        result = self.check(env={"RAILSMITH_PRIVATE_SCAN_PATTERN": "unrelated"})
        self.assert_failed(result, "Private pattern detected")

    def test_invalid_regex_fails_closed(self):
        result = self.check(env={"RAILSMITH_PRIVATE_SCAN_PATTERN": "["})
        self.assert_failed(result, "Invalid private scan pattern")

    def test_private_path_name_is_checked_and_withheld(self):
        self.write("sensitive-client/notes.md", "Public content\n")
        result = self.check(env={"RAILSMITH_PRIVATE_TERMS": "sensitive-client"})
        self.assert_failed(result, "file path")
        self.assertNotIn("sensitive-client", result.stderr)

    def test_binary_and_non_utf8_files_fail_closed(self):
        for content in (b"\x00binary", b"\xff\xfe"):
            with self.subTest(content=content):
                self.write("asset.bin", content)
                self.assertNotEqual(self.check().returncode, 0)
                self.git("add", "asset.bin")
                self.assertNotEqual(self.check(staged=True).returncode, 0)

    def test_symlinks_are_rejected_without_following_targets(self):
        (self.root / "link.md").symlink_to("missing-private-file")
        self.assert_failed(self.check(), "symlinks are not followed")
        self.git("add", "link.md")
        self.assert_failed(self.check(staged=True), "Unsupported index entry")

    def test_symlinked_parent_directory_is_not_followed(self):
        docs = self.root / "docs"
        moved = self.root / "moved-docs"
        docs.rename(moved)
        docs.symlink_to(moved, target_is_directory=True)
        self.assert_failed(self.check(), "symlinks are not followed")

    def test_ignored_files_are_excluded_but_forced_index_entries_are_checked(self):
        self.write(".gitignore", ".local/\n")
        self.write(".local/notes.md", "sk-" + "d" * 30)
        self.assertEqual(self.check().returncode, 0)
        self.git("add", "-f", ".local/notes.md")
        self.assert_failed(self.check(staged=True), "Private pattern detected")

    def test_staged_deletion_has_no_blob_to_scan(self):
        self.write("extra.md", "sk-" + "e" * 30)
        self.git("add", "extra.md")
        self.git("rm", "--cached", "extra.md")
        self.assertEqual(self.check(staged=True).returncode, 0)

    def test_missing_required_file_and_metadata_fail(self):
        (self.root / "README.md").unlink()
        self.assert_failed(self.check(), "Missing required file")
        self.write("README.md", "# Public guide\n")
        self.write("skills/example/SKILL.md", "---\nname: example\n---\n")
        self.assert_failed(self.check(), "Missing skill metadata")
        self.write("skills/example/SKILL.md", "---\ndescription: \nname: example\n---\n")
        self.assert_failed(self.check(), "Missing skill metadata")

    def test_shell_syntax_uses_staged_content(self):
        self.write("scripts/example", "#!/usr/bin/env bash\nif\n")
        self.git("add", "scripts/example")
        self.write("scripts/example", "#!/usr/bin/env bash\ntrue\n")
        self.assertEqual(self.check().returncode, 0)
        self.assert_failed(self.check(staged=True), "Shell syntax error")

    def test_git_error_fails_closed(self):
        outside = self.root / "not-a-repository"
        result = self.check(root=outside)
        self.assert_failed(result, "Git could not read")

    def test_spaces_and_newlines_in_paths_are_not_split(self):
        self.write("notes with space\nand newline.md", "Public content\n")
        self.git("add", ".")
        self.assertEqual(self.check(staged=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
