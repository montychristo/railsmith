"""Exercise adoption against disposable repositories, never user configuration."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/adopt"


class AdoptTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "railsmith checkout"
        self.project = self.base / "rails app"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        (self.source / "scripts").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.source / "scripts/adopt")
        for name, content in {
            "core/AGENTS.md": "Shared engineering principles\n",
            "core/references/example.md": "Supporting guidance\n",
            "adapters/claude/CLAUDE.md": "Tool guidance\n",
            "skills/example/SKILL.md": "Read ../../core/references/example.md\n",
            "skills/second/SKILL.md": "Another skill\n",
        }.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def adopt(self, *arguments, include_project=True):
        command = ["bash", str(self.source / "scripts/adopt")]
        if include_project:
            command.extend(["--project", str(self.project)])
        return subprocess.run(command + list(arguments), cwd=self.project,
                              capture_output=True, text=True)

    def git(self, *arguments):
        return subprocess.run(["git", *arguments], cwd=self.project,
                              capture_output=True, text=True, check=True)

    def assert_no_installation(self):
        self.assertEqual([path.name for path in self.project.iterdir() if path.name != ".git"], [])

    def test_dry_run_writes_nothing(self):
        result = self.adopt()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY-RUN", result.stdout)
        expected_import = "@" + str(self.source / "core/AGENTS.md").replace(" ", "\\ ")
        self.assertIn(expected_import, result.stdout)
        self.assert_no_installation()

    def test_preserves_instructions_and_resolves_supporting_files(self):
        original = b"# App instructions\r\nKeep this text exactly."
        (self.project / "CLAUDE.md").write_bytes(original)
        agents = b"# Existing AGENTS\r\nUse the app's tests.\r\n"
        (self.project / "AGENTS.md").write_bytes(agents)
        local_original = b"# Local instructions\r\nKeep me too.\r\n"
        (self.project / "CLAUDE.local.md").write_bytes(local_original)
        ignore_original = b"# Existing ignores\r\n/tmp\r\n"
        (self.project / ".gitignore").write_bytes(ignore_original)
        result = self.adopt("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        bridge = (self.project / "CLAUDE.local.md").read_bytes()
        self.assertTrue(bridge.startswith(local_original))
        self.assertEqual((self.project / "CLAUDE.md").read_bytes(), original)
        self.assertTrue((self.project / ".gitignore").read_bytes().startswith(ignore_original))
        self.assertIn(b"@AGENTS.md", bridge)
        expected_import = "@" + str(self.source / "core/AGENTS.md").replace(" ", "\\ ")
        self.assertIn(expected_import.encode(), bridge)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), agents)
        skill = self.project / ".claude/skills/example"
        self.assertTrue(skill.is_symlink())
        self.assertEqual((skill / "../../core/references/example.md").resolve().read_text(),
                         "Supporting guidance\n")
        for path in ["CLAUDE.local.md", ".claude/skills/example", ".claude/skills/second"]:
            self.git("check-ignore", "-q", "--", path)
        untracked = self.git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
        self.assertEqual(set(untracked), {".gitignore", "AGENTS.md", "CLAUDE.md"})
        user_skill = self.project / ".claude/skills/user-skill/SKILL.md"
        user_skill.parent.mkdir(parents=True)
        user_skill.write_text("A shareable user skill\n")
        self.assertIn(".claude/skills/user-skill/SKILL.md",
                      self.git("ls-files", "--others", "--exclude-standard").stdout)

    def test_repeated_apply_is_idempotent(self):
        (self.project / "AGENTS.md").write_text("Existing project rules\n")
        first = self.adopt("--apply")
        self.assertEqual(first.returncode, 0, first.stderr)
        instruction = self.project / "CLAUDE.local.md"
        previous = instruction.read_bytes()
        timestamp = instruction.stat().st_mtime_ns
        ignore_previous = (self.project / ".gitignore").read_bytes()
        second = self.adopt("--apply")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("Already adopted", second.stdout)
        self.assertEqual(instruction.read_bytes(), previous)
        self.assertEqual(instruction.stat().st_mtime_ns, timestamp)
        self.assertEqual((self.project / ".gitignore").read_bytes(), ignore_previous)
        self.assertEqual(previous.count(b"@AGENTS.md"), 1)

    def test_skill_collision_is_detected_before_any_write(self):
        collision = self.project / ".claude/skills/second"
        collision.mkdir(parents=True)
        (collision / "SKILL.md").write_text("User-owned skill\n")
        original = "User-owned instructions\n"
        (self.project / "CLAUDE.md").write_text(original)
        for mode in ([], ["--apply"]):
            result = self.adopt(*mode)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("existing skill target", result.stderr)
            self.assertEqual((self.project / "CLAUDE.md").read_text(), original)
            self.assertFalse((self.project / ".claude/skills/example").exists())
            self.assertFalse((self.project / "CLAUDE.local.md").exists())
            self.assertFalse((self.project / ".gitignore").exists())

    def test_broken_symlink_is_a_collision(self):
        target = self.project / ".claude/skills/second"
        target.parent.mkdir(parents=True)
        target.symlink_to(self.base / "missing")
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(target.is_symlink())
        self.assertFalse((self.project / "CLAUDE.local.md").exists())

    def test_refuses_config_directory_symlink(self):
        outside = self.base / "outside-config"
        outside.mkdir()
        (self.project / ".claude").symlink_to(outside, target_is_directory=True)
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("configuration symlink", result.stderr)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "CLAUDE.local.md").exists())

    def test_refuses_instruction_symlink(self):
        outside = self.base / "shared-instructions.md"
        outside.write_text("Shared instructions\n")
        (self.project / "CLAUDE.local.md").symlink_to(outside)
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(), "Shared instructions\n")

    def test_missing_source_or_project_does_not_partially_install(self):
        (self.source / "core/AGENTS.md").unlink()
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing source", result.stderr)
        self.assert_no_installation()
        missing = self.adopt("--project", str(self.base / "missing"), "--apply")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("project directory does not exist", missing.stderr)

    def test_no_implicit_global_installation_or_replacement_mode(self):
        for arguments, include_project in [
            (["--apply"], False),
            (["--tool", "all", "--apply"], True),
            (["--backup", "--apply"], True),
        ]:
            with self.subTest(arguments=arguments):
                result = self.adopt(*arguments, include_project=include_project)
                self.assertNotEqual(result.returncode, 0)
                self.assert_no_installation()

    def test_malformed_managed_block_is_not_replaced(self):
        original = "Keep me\n<!-- railsmith:begin -->\nIncomplete block\n"
        (self.project / "CLAUDE.local.md").write_text(original)
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.project / "CLAUDE.local.md").read_text(), original)

    def test_tracked_local_instructions_are_never_changed(self):
        path = self.project / "CLAUDE.local.md"
        original = b"Tracked instructions\r\n"
        path.write_bytes(original)
        self.git("add", "CLAUDE.local.md")
        for mode in ([], ["--apply"]):
            result = self.adopt(*mode)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("tracked installation targets", result.stderr)
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse((self.project / ".gitignore").exists())
            self.assertFalse((self.project / ".claude").exists())

    def test_tracked_matching_skill_link_is_refused(self):
        target = self.project / ".claude/skills/example"
        target.parent.mkdir(parents=True)
        target.symlink_to(self.source / "skills/example", target_is_directory=True)
        self.git("add", ".claude/skills/example")
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tracked installation targets", result.stderr)
        self.assertFalse((self.project / "CLAUDE.local.md").exists())
        self.assertFalse((self.project / ".gitignore").exists())

    def test_nested_ignore_override_restores_original_before_creating_bridge(self):
        ignore = self.project / ".gitignore"
        original = b"# Keep existing rules\r\n/tmp\r\n"
        ignore.write_bytes(original)
        nested = self.project / ".claude/skills/.gitignore"
        nested.parent.mkdir(parents=True)
        nested.write_text("!example\n")
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("restored .gitignore", result.stderr)
        self.assertEqual(ignore.read_bytes(), original)
        self.assertFalse((self.project / "CLAUDE.local.md").exists())
        self.assertFalse((nested.parent / "example").exists())

    def test_refuses_gitignore_symlink_without_touching_referent(self):
        outside = self.base / "shared-ignore"
        outside.write_text("shared\n")
        (self.project / ".gitignore").symlink_to(outside)
        result = self.adopt("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(), "shared\n")
        self.assertFalse((self.project / "CLAUDE.local.md").exists())

    def test_existing_ignore_negation_gets_an_effective_final_exclusion(self):
        original = b"/CLAUDE.local.md\r\n!CLAUDE.local.md\r\n"
        (self.project / ".gitignore").write_bytes(original)
        result = self.adopt("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.project / ".gitignore").read_bytes().startswith(original))
        self.git("check-ignore", "-q", "--", "CLAUDE.local.md")

    def test_refuses_non_git_and_nested_targets(self):
        plain = self.base / "plain-folder"
        nested = self.project / "nested-folder"
        plain.mkdir()
        nested.mkdir()
        for target in (plain, nested):
            result = self.adopt("--project", str(target), "--apply")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("root of an existing Git working tree", result.stderr)
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
