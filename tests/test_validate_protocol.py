import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Tuple


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate_protocol.py"
SOURCE_PROTOCOL = REPOSITORY_ROOT / "protocol"
SOURCE_HANDOFF = REPOSITORY_ROOT / "HANDOFF.md"


class StructuralProtocolValidatorTests(unittest.TestCase):
    def make_repository(self) -> Tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory(prefix="aep validator ")
        root = Path(temporary.name) / "repository with spaces"
        root.mkdir()
        shutil.copytree(str(SOURCE_PROTOCOL), str(root / "protocol"))
        shutil.copy2(str(SOURCE_HANDOFF), str(root / "HANDOFF.md"))
        return temporary, root

    def run_validator(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--root", str(root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def snapshot(self, root: Path) -> Dict[str, Tuple[str, str]]:
        state: Dict[str, Tuple[str, str]] = {}
        for current, directory_names, file_names in os.walk(str(root), topdown=True, followlinks=False):
            current_path = Path(current)
            for name in sorted(directory_names + file_names):
                path = current_path / name
                relative = path.relative_to(root).as_posix()
                if path.is_symlink():
                    state[relative] = ("symlink", os.readlink(str(path)))
                elif path.is_dir():
                    state[relative] = ("directory", "")
                elif path.is_file():
                    state[relative] = ("file", hashlib.sha256(path.read_bytes()).hexdigest())
                else:
                    state[relative] = ("other", "")
        return state

    def append_readme(self, root: Path, text: str) -> None:
        readme = root / "protocol" / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + text, encoding="utf-8")

    def test_current_repository_passes(self) -> None:
        result = self.run_validator(REPOSITORY_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "PASS structural protocol validation (package_files=10 handoffs=2)\n")
        self.assertEqual(result.stderr, "")

    def test_isolated_copy_with_spaces_is_deterministic_and_read_only(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        before = self.snapshot(root)
        first = self.run_validator(root)
        second = self.run_validator(root)
        after = self.snapshot(root)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual((first.stdout, first.stderr), (second.stdout, second.stderr))
        self.assertEqual(before, after)

    def test_missing_and_unexpected_entries_fail_manifest(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        (root / "protocol" / "EXAMPLE.md").unlink()
        (root / "protocol" / "EXTRA.md").write_text("extra\n", encoding="utf-8")
        result = self.run_validator(root)
        repeated = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertEqual((result.stdout, result.stderr), (repeated.stdout, repeated.stderr))
        self.assertIn("AEP-PKG-001 protocol/EXAMPLE.md: required package file is missing", result.stdout)
        self.assertIn("AEP-PKG-001 protocol/EXTRA.md: unexpected package file", result.stdout)

    def test_non_regular_expected_entry_fails(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        example = root / "protocol" / "EXAMPLE.md"
        example.unlink()
        example.mkdir()
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PKG-001 protocol/EXAMPLE.md: required package file is missing", result.stdout)
        self.assertIn("AEP-PKG-001 protocol/EXAMPLE.md: unexpected package directory", result.stdout)

    def test_symlinked_package_entry_fails(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        example = root / "protocol" / "EXAMPLE.md"
        example.unlink()
        try:
            example.symlink_to(root / "protocol" / "README.md")
        except OSError as error:
            self.skipTest("symlinks unavailable: {}".format(error))
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PKG-002 protocol/EXAMPLE.md: symlinks are forbidden", result.stdout)

    def test_symlinked_bundle_root_fails_without_scanning_target(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        moved = root / "outside protocol"
        (root / "protocol").rename(moved)
        (moved / "README.md").write_bytes(b"\xff\n")
        try:
            (root / "protocol").symlink_to(moved, target_is_directory=True)
        except OSError as error:
            self.skipTest("symlinks unavailable: {}".format(error))
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PKG-002 protocol: bundle root must not be a symlink", result.stdout)
        self.assertNotIn("AEP-MD-001", result.stdout)

    def test_markdown_byte_and_fence_invariants_fail(self) -> None:
        mutations = {
            "invalid UTF-8": (lambda path: path.write_bytes(path.read_bytes() + b"\xff\n"), "AEP-MD-001"),
            "missing final newline": (lambda path: path.write_bytes(path.read_bytes().rstrip(b"\n")), "AEP-MD-002"),
            "trailing whitespace": (lambda path: path.write_bytes(path.read_bytes() + b"bad  \n"), "AEP-MD-003"),
            "unclosed fence": (lambda path: path.write_bytes(path.read_bytes() + b"```text\n"), "AEP-MD-004"),
        }
        for label, (mutate, rule_id) in mutations.items():
            with self.subTest(label=label):
                temporary, root = self.make_repository()
                try:
                    mutate(root / "protocol" / "README.md")
                    result = self.run_validator(root)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(rule_id, result.stdout)
                finally:
                    temporary.cleanup()

    def test_broken_and_escaping_links_fail(self) -> None:
        cases = {
            "missing": "\n[broken](missing.md)\n",
            "parent escape": "\n[outside](../HANDOFF.md)\n",
            "absolute": "\n[absolute](/tmp/outside.md)\n",
            "file URI": "\n[file](file:///tmp/outside.md)\n",
            "drive absolute": "\n[drive](C:/outside.md)\n",
            "blockquote live link": "\n> [quoted](missing.md)\n",
        }
        for label, link in cases.items():
            with self.subTest(label=label):
                temporary, root = self.make_repository()
                try:
                    self.append_readme(root, link)
                    result = self.run_validator(root)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("AEP-MD-005", result.stdout)
                finally:
                    temporary.cleanup()

    def test_symlink_escape_fails(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        outside = root / "outside ADR"
        outside.mkdir()
        shutil.copy2(str(root / "protocol" / "ADR" / "TEMPLATE.md"), str(outside / "TEMPLATE.md"))
        shutil.rmtree(str(root / "protocol" / "ADR"))
        try:
            (root / "protocol" / "ADR").symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest("symlinks unavailable: {}".format(error))
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PKG-002 protocol/ADR: symlinks are forbidden", result.stdout)
        self.assertIn("AEP-MD-005", result.stdout)

    def test_supported_links_and_code_examples_pass(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.append_readme(
            root,
            """

Unicode 雪 [query with nested parentheses](README.md?example=(one))
[angle destination](<README.md> "title")
[fragment only](#section)
[external](https://example.com/a_(b))
[mail](mailto:protocol@example.com)
[custom scheme](x:resource)
`[inline code](missing.md)`

```markdown
[backtick fence](missing.md)
```

~~~markdown
[tilde fence](missing.md)
~~~

> ```markdown
> [blockquote fence](missing.md)
> ```

- ```markdown
  [list fence](missing.md)
  ```

`multiline code span
[multiline code link](missing.md)
ends here`
""",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unicode_space_and_parentheses_target_is_resolved(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        target = root / "protocol" / "雪 copy(one).md"
        target.write_text("target\n", encoding="utf-8")
        self.append_readme(root, "\n[encoded target](%E9%9B%AA%20copy(one).md)\n")
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PKG-001 protocol/雪 copy(one).md: unexpected package file", result.stdout)
        self.assertNotIn("AEP-MD-005", result.stdout)

    def test_indented_link_like_syntax_returns_unsupported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.append_readme(root, "\n- item\n\n    [nested content](missing.md)\n")
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNSUPPORTED AEP-MD-006", result.stdout)
        self.assertIn("indented line", result.stdout)

    def test_inline_code_does_not_span_blank_block_boundary(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.append_readme(root, "\n`literal opener\n\n[live](missing.md)`\n")
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("VIOLATION AEP-MD-005", result.stdout)

    def test_malformed_inline_link_returns_unsupported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.append_readme(root, "\n[unfinished](README.md\n")
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNSUPPORTED AEP-MD-006", result.stdout)

    def test_reference_style_links_return_unsupported(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        self.append_readme(root, "\n[guide][guide]\n\n[guide]: README.md\n")
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("UNSUPPORTED AEP-MD-006", result.stdout)
        self.assertIn("unsupported=", result.stdout)

    def test_handoff_section_shape_failures(self) -> None:
        mutations = {
            "missing": lambda text: text.replace("## Archived Summary", "### Archived Summary", 1),
            "duplicate": lambda text: text + "\n## Next Action\n\nDuplicate.\n",
            "reordered": lambda text: text.replace("## Active Issues", "## SWAP", 1).replace("## Next Action", "## Active Issues", 1).replace("## SWAP", "## Next Action", 1),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                temporary, root = self.make_repository()
                try:
                    handoff = root / "HANDOFF.md"
                    handoff.write_text(mutate(handoff.read_text(encoding="utf-8")), encoding="utf-8")
                    result = self.run_validator(root)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("AEP-HANDOFF-001", result.stdout)
                finally:
                    temporary.cleanup()

    def test_fenced_handoff_headings_do_not_affect_structure(self) -> None:
        temporary_valid, root_valid = self.make_repository()
        self.addCleanup(temporary_valid.cleanup)
        valid_handoff = root_valid / "HANDOFF.md"
        valid_handoff.write_text(
            valid_handoff.read_text(encoding="utf-8") + "\n```markdown\n## Next Action\n```\n",
            encoding="utf-8",
        )
        valid_result = self.run_validator(root_valid)
        self.assertEqual(valid_result.returncode, 0, valid_result.stdout + valid_result.stderr)

        temporary_missing, root_missing = self.make_repository()
        self.addCleanup(temporary_missing.cleanup)
        missing_handoff = root_missing / "HANDOFF.md"
        text = missing_handoff.read_text(encoding="utf-8").replace("## Next Action", "### Next Action", 1)
        missing_handoff.write_text(text + "\n```markdown\n## Next Action\n```\n", encoding="utf-8")
        missing_result = self.run_validator(root_missing)
        self.assertEqual(missing_result.returncode, 1)
        self.assertIn("AEP-HANDOFF-001", missing_result.stdout)
        self.assertIn("AEP-HANDOFF-003", missing_result.stdout)

    def test_handoff_snapshot_field_and_next_action_failures(self) -> None:
        temporary, root = self.make_repository()
        self.addCleanup(temporary.cleanup)
        handoff = root / "HANDOFF.md"
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace("**Evidence cutoff:**", "**Evidence window:**", 1),
            encoding="utf-8",
        )
        result = self.run_validator(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-HANDOFF-002", result.stdout)

        temporary_empty, root_empty = self.make_repository()
        self.addCleanup(temporary_empty.cleanup)
        empty_handoff = root_empty / "HANDOFF.md"
        text = empty_handoff.read_text(encoding="utf-8")
        start = text.index("## Next Action") + len("## Next Action")
        end = text.index("## Recent Activity", start)
        empty_handoff.write_text(text[:start] + "\n\n" + text[end:], encoding="utf-8")
        empty_result = self.run_validator(root_empty)
        self.assertEqual(empty_result.returncode, 1)
        self.assertIn("AEP-HANDOFF-003", empty_result.stdout)

    def test_missing_and_symlinked_root_handoff_fail(self) -> None:
        temporary_missing, root_missing = self.make_repository()
        self.addCleanup(temporary_missing.cleanup)
        (root_missing / "HANDOFF.md").unlink()
        missing_result = self.run_validator(root_missing)
        self.assertEqual(missing_result.returncode, 1)
        self.assertIn("AEP-HANDOFF-001 HANDOFF.md: HANDOFF file is missing", missing_result.stdout)

        temporary_link, root_link = self.make_repository()
        self.addCleanup(temporary_link.cleanup)
        outside = root_link / "outside handoff.md"
        (root_link / "HANDOFF.md").rename(outside)
        try:
            (root_link / "HANDOFF.md").symlink_to(outside)
        except OSError as error:
            self.skipTest("symlinks unavailable: {}".format(error))
        link_result = self.run_validator(root_link)
        self.assertEqual(link_result.returncode, 1)
        self.assertIn("AEP-HANDOFF-001 HANDOFF.md: HANDOFF must not be a symlink", link_result.stdout)

    def test_missing_root_is_tool_error(self) -> None:
        missing = REPOSITORY_ROOT / "does-not-exist-for-validator-test"
        result = self.run_validator(missing)
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR AEP-TOOL-001", result.stdout)

    def test_cli_usage_error_has_stable_summary(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--unknown-option"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("ERROR AEP-TOOL-001 command:", result.stderr)
        self.assertIn("SUMMARY violations=0 unsupported=0 errors=1", result.stderr)


if __name__ == "__main__":
    unittest.main()
