#!/usr/bin/env python3
"""Check repository structure and common publication leaks; never a privacy proof."""

import argparse
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


REQUIRED_FILES = (
    "README.md", "AGENTS.md", "core/AGENTS.md", "docs/voice.md",
    "profiles/chris/voice.md", "adapters/codex/AGENTS.md",
    "adapters/claude/CLAUDE.md", "adapters/cursor/rules/railsmith.mdc",
)
MAX_FILE_BYTES = 2 * 1024 * 1024
DEFAULT_PATTERNS = (
    r"/(?:Users|home)/[^\s/]+", r"[A-Za-z]:\\Users\\[^\s\\]+",
    r"\batlassian\.net\b", r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----",
    r"\bxox[baprs]-[A-Za-z0-9-]+", r"\bgh[pousr]_[A-Za-z0-9]{20,}",
    r"\bgithub_[p]at_[A-Za-z0-9_]{20,}", r"\bAKIA[A-Z0-9]{16}\b",
    r"\bsk-[A-Za-z0-9_-]{20,}",
)


class CheckError(Exception):
    pass


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False,
    )
    if result.returncode:
        # Git diagnostics can contain private paths or values.
        raise CheckError("Git could not read the repository snapshot")
    return result.stdout


def patterns():
    rules = [re.compile(pattern) for pattern in DEFAULT_PATTERNS]
    extra = os.environ.get("RAILSMITH_PRIVATE_SCAN_PATTERN", "")
    if extra:
        try:
            rules.append(re.compile(extra, re.IGNORECASE))
        except re.error:
            raise CheckError("Invalid private scan pattern configuration") from None
    for term in os.environ.get("RAILSMITH_PRIVATE_TERMS", "").splitlines():
        if term.strip():
            rules.append(re.compile(re.escape(term.strip()), re.IGNORECASE))
    return rules


def index_entries(root):
    entries = {}
    for record in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, oid, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise CheckError("Unmerged index entries require resolution")
        path = raw_path.decode("utf-8")
        entries[path] = (mode, oid)
    return entries


def snapshot(root, staged, rules):
    entries = index_entries(root)
    if staged:
        paths = entries
    else:
        paths = {
            path.decode("utf-8")
            for path in git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0")
            if path
        }
    files = {}
    for path in sorted(paths):
        if any(rule.search(path) for rule in rules):
            raise CheckError("Private pattern detected in a file path (value withheld)")
        label = repr(path)
        if staged:
            mode, oid = entries[path]
            if mode not in ("100644", "100755"):
                raise CheckError(f"Unsupported index entry {label}; review required")
            size = int(git(root, "cat-file", "-s", oid))
            if size > MAX_FILE_BYTES:
                raise CheckError(f"File exceeds scan size limit: {label}")
            content = git(root, "cat-file", "blob", oid)
        else:
            target = root / path
            # lstat on the final file alone would follow symlinked parents.
            for parent in target.parents:
                if parent == root:
                    break
                if parent.is_symlink():
                    raise CheckError(f"Unsupported parent directory for {label}; symlinks are not followed")
            try:
                details = target.lstat()
            except FileNotFoundError:
                # A tracked deletion has no working-tree payload to scan.
                continue
            if not stat.S_ISREG(details.st_mode):
                raise CheckError(f"Unsupported file type {label}; symlinks are not followed")
            if details.st_size > MAX_FILE_BYTES:
                raise CheckError(f"File exceeds scan size limit: {label}")
            content = target.read_bytes()
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise CheckError(f"Non-UTF-8 content in {label}; review required") from None
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", text):
            raise CheckError(f"Binary/control content in {label}; review required")
        if any(rule.search(text) for rule in rules):
            raise CheckError(f"Private pattern detected in {label} (value withheld)")
        files[path] = text
    return files


def validate(files):
    for path in REQUIRED_FILES:
        if path not in files:
            raise CheckError(f"Missing required file: {path}")
    skills = [path for path in files if re.fullmatch(r"skills/[^/]+/SKILL\.md", path)]
    if not skills:
        raise CheckError("No skill metadata found")
    for path in skills:
        text = files[path]
        if not text.startswith("---\n") or "\n---" not in text[4:]:
            raise CheckError(f"Missing front matter: {path}")
        metadata = text.split("---", 2)[1]
        if not all(re.search(rf"^{key}:[ \t]*[^ \t\r\n]+", metadata, re.MULTILINE) for key in ("name", "description")):
            raise CheckError(f"Missing skill metadata: {path}")
    for path, text in files.items():
        if not path.startswith("scripts/"):
            continue
        if text.startswith(("#!/usr/bin/env bash", "#!/bin/bash", "#!/bin/sh")):
            result = subprocess.run(["bash", "-n"], input=text, text=True, capture_output=True)
            if result.returncode:
                raise CheckError(f"Shell syntax error: {path}")
        elif path.endswith(".py"):
            try:
                compile(text, path, "exec")
            except SyntaxError:
                raise CheckError(f"Python syntax error: {path}") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--staged", action="store_true", help="Validate all index paths and blobs, ignoring working-tree edits")
    args = parser.parse_args()
    try:
        files = snapshot(args.root, args.staged, patterns())
        validate(files)
    except (CheckError, OSError, UnicodeError, ValueError) as error:
        message = str(error) if isinstance(error, CheckError) else "Could not read or validate the complete snapshot"
        print(f"FAIL: {message}", file=sys.stderr)
        return 1
    mode = "index" if args.staged else "working tree"
    print(f"doctor passed: {len(files)} files checked ({mode}); content review still required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
