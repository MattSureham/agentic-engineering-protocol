import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))
import probe_discovery as probe  # noqa: E402

PROTOCOL = REPOSITORY_ROOT / "protocol"
FIXTURE = probe.FIXTURE

PACKAGE_MARKDOWN = {
    "BOOTSTRAP.md",
    "PROJECT_SPEC.md",
    "HANDOFF.md",
    "HUMAN_CHECKPOINT.md",
    "PROMPTS.md",
    "EXAMPLE.md",
    "README.md",
    "ADR/TEMPLATE.md",
    "EVIDENCE/TEMPLATE.md",
    "ISSUES/TEMPLATE.md",
}

INSTALL_SNIPPET = """for name in AGENTS.md CLAUDE.md; do
  destination="$repository_target/$name"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'collision: %s exists; merge the bridge pointer into it, preserving its content\\n' "$name" >&2
  else
    cp "$bridge_reference/$name" "$destination"
  fi
done"""


class RootBridgeTests(unittest.TestCase):
    def test_both_bridges_exist_as_regular_files(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            path = REPOSITORY_ROOT / name
            self.assertTrue(path.is_file() and not path.is_symlink(), name)

    def test_bridge_content_properties(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (REPOSITORY_ROOT / name).read_text(encoding="utf-8")
            self.assertIn("formally adopts", text, name)
            self.assertIn("BOOTSTRAP.md", text, name)
            self.assertIn("PROJECT_SPEC.md", text, name)
            self.assertIn("HANDOFF.md", text, name)
            self.assertIn("missing or unreadable", text, name)
            self.assertIn("no protocol authority", text, name)
            self.assertIn("governs the repository rooted", text, name)

    def test_bridges_stay_thin(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            raw = (REPOSITORY_ROOT / name).read_bytes()
            self.assertLess(len(raw), 4000, name)
            self.assertLess(len(raw.decode("utf-8").splitlines()), 60, name)

    def test_bridges_do_not_restate_normative_semantics(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (REPOSITORY_ROOT / name).read_text(encoding="utf-8")
            for marker in ("DISCOVERY-00", "MILESTONE-", "accepted ADRs →", "→ contracts"):
                self.assertNotIn(marker, text, name)


class PackageInventoryTests(unittest.TestCase):
    def test_package_remains_exactly_ten_markdown_files(self) -> None:
        found = {
            path.relative_to(PROTOCOL).as_posix()
            for path in PROTOCOL.rglob("*.md")
        }
        self.assertEqual(found, PACKAGE_MARKDOWN)

    def test_package_contains_no_bridge_files(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            self.assertFalse((PROTOCOL / name).exists(), name)


class PackageGuidanceTests(unittest.TestCase):
    def test_guide_documents_discovery_bridges(self) -> None:
        text = (PROTOCOL / "README.md").read_text(encoding="utf-8")
        self.assertIn("## Discovery bridges", text)
        self.assertIn("not an eleventh core file", text)
        self.assertIn("is not a support claim", text)
        self.assertIn("never overwrite", text)
        self.assertIn(INSTALL_SNIPPET, text)

    def test_quick_start_uses_bridge_with_prompt_as_fallback(self) -> None:
        text = (PROTOCOL / "README.md").read_text(encoding="utf-8")
        self.assertIn("Install the one-time discovery bridge", text)
        self.assertIn("manual fallback", text)

    def test_onboarding_prompt_marked_as_manual_fallback(self) -> None:
        text = (PROTOCOL / "PROMPTS.md").read_text(encoding="utf-8")
        section = text.split("## Fresh implementor or onboarding", 1)[1]
        self.assertIn("manual fallback", section)
        self.assertIn("never counts as automatic-activation evidence", section)

    def test_package_bootstrap_disclaims_bridge_authority(self) -> None:
        text = (PROTOCOL / "BOOTSTRAP.md").read_text(encoding="utf-8")
        self.assertIn("peripheral adapter artifacts", text)
        self.assertIn("never protocol authority", text)

    def test_root_readme_references_bridges(self) -> None:
        text = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("AGENTS.md", text)
        self.assertIn("CLAUDE.md", text)


class BridgeInstallationTests(unittest.TestCase):
    def run_snippet(self, target: Path) -> subprocess.CompletedProcess:
        script = (
            'repository_target="%s"\nbridge_reference="%s"\n%s\n'
            % (target, REPOSITORY_ROOT, INSTALL_SNIPPET)
        )
        return subprocess.run(
            ["sh", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=False,
        )

    def test_fresh_install_copies_reference_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge install ") as temporary:
            target = Path(temporary)
            completed = self.run_snippet(target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for name in ("AGENTS.md", "CLAUDE.md"):
                self.assertEqual(
                    (target / name).read_bytes(),
                    (REPOSITORY_ROOT / name).read_bytes(),
                    name,
                )

    def test_collision_preserves_existing_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge merge ") as temporary:
            target = Path(temporary)
            existing = b"# Existing instructions\n\nKeep me.\n"
            (target / "AGENTS.md").write_bytes(existing)
            completed = self.run_snippet(target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("collision", completed.stderr)
            self.assertEqual((target / "AGENTS.md").read_bytes(), existing)
            self.assertTrue((target / "CLAUDE.md").is_file())


class FixtureTests(unittest.TestCase):
    def test_fixture_structure(self) -> None:
        for relative in (
            "BOOTSTRAP.md", "PROJECT_SPEC.md", "HANDOFF.md",
            "AGENTS.md", "CLAUDE.md", "src/note.txt",
        ):
            self.assertTrue((FIXTURE / relative).is_file(), relative)

    def test_fixture_spec_authorizes_expected_task(self) -> None:
        spec = (FIXTURE / "PROJECT_SPEC.md").read_text(encoding="utf-8")
        self.assertIn("T-001", spec)
        self.assertIn("AUTHORIZED", spec)
        self.assertIn(probe.EXPECTED_RESULT_BYTES.decode("utf-8").strip(), spec)
        self.assertIn("No other work is authorized", spec)

    def test_fixture_bootstrap_defines_stop_rules(self) -> None:
        bootstrap = (FIXTURE / "BOOTSTRAP.md").read_text(encoding="utf-8")
        self.assertIn("conflict", bootstrap)
        self.assertIn("no task is authorized", bootstrap)

    def test_fixture_bridges_point_to_canonical_entry(self) -> None:
        for name in ("AGENTS.md", "CLAUDE.md"):
            text = (FIXTURE / name).read_text(encoding="utf-8")
            self.assertIn("BOOTSTRAP.md", text, name)
            self.assertIn("missing or unreadable", text, name)


class ProbeHarnessDeterministicTests(unittest.TestCase):
    def copy_fixture(self, root: Path) -> Path:
        root.mkdir(parents=True, exist_ok=True)
        case_dir = root / "repo"
        shutil.copytree(str(FIXTURE), str(case_dir))
        return case_dir

    def test_case_transforms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep discovery transforms ") as temporary:
            root = Path(temporary)
            missing = self.copy_fixture(root / "a")
            probe.CASES["negative_missing_entry"].transform(missing)
            self.assertFalse((missing / "BOOTSTRAP.md").exists())

            no_work = self.copy_fixture(root / "b")
            probe.CASES["negative_no_authorized_work"].transform(no_work)
            self.assertIn("No task is currently authorized", (no_work / "PROJECT_SPEC.md").read_text(encoding="utf-8"))

            collision = self.copy_fixture(root / "c")
            probe.CASES["negative_collision"].transform(collision)
            merged = (collision / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("MUST NOT be modified", merged)
            self.assertIn("BOOTSTRAP.md", merged)
            self.assertTrue((collision / "KEEP.txt").is_file())

            removed = self.copy_fixture(root / "d")
            probe.CASES["adapter_removed_auto"].transform(removed)
            self.assertFalse((removed / "AGENTS.md").exists())
            self.assertFalse((removed / "CLAUDE.md").exists())
            self.assertTrue((removed / "BOOTSTRAP.md").is_file())

            outer = root / "outer"
            outer.mkdir()
            probe.CASES["negative_nested"].transform(outer)
            self.assertFalse((outer / "BOOTSTRAP.md").exists())
            self.assertTrue((outer / "nested_repo" / "BOOTSTRAP.md").is_file())
            self.assertTrue((outer / "README.md").is_file())

    def classify_with(self, case_name: str, result_bytes, tool_events) -> dict:
        with tempfile.TemporaryDirectory(prefix="aep discovery classify ") as temporary:
            root = Path(temporary) / "repo"
            if case_name == "negative_nested":
                root.mkdir()
                probe.CASES["negative_nested"].transform(root)
                if result_bytes is not None:
                    (root / probe.EXPECTED_RESULT_PATH).write_bytes(result_bytes)
            else:
                shutil.copytree(str(FIXTURE), str(root))
                probe.CASES[case_name].transform(root)
                if result_bytes is not None:
                    (root / probe.EXPECTED_RESULT_PATH).write_bytes(result_bytes)
            return probe.classify(probe.CASES[case_name], root, tool_events)

    def test_classify_positive_pass_requires_recovery_first(self) -> None:
        events = [
            {"seq": 0, "tool": "Read", "target": "/repo/BOOTSTRAP.md"},
            {"seq": 1, "tool": "Read", "target": "/repo/PROJECT_SPEC.md"},
            {"seq": 2, "tool": "Write", "target": "/repo/RESULT.txt"},
        ]
        evaluation = self.classify_with("positive_root", probe.EXPECTED_RESULT_BYTES, events)
        self.assertEqual(evaluation["classification"], "PASS")

    def test_classify_positive_fails_without_recovery(self) -> None:
        events = [{"seq": 0, "tool": "Write", "target": "/repo/RESULT.txt"}]
        evaluation = self.classify_with("positive_root", probe.EXPECTED_RESULT_BYTES, events)
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_classify_positive_fails_on_wrong_content(self) -> None:
        events = [
            {"seq": 0, "tool": "Read", "target": "/repo/BOOTSTRAP.md"},
            {"seq": 1, "tool": "Write", "target": "/repo/RESULT.txt"},
        ]
        evaluation = self.classify_with("positive_root", b"wrong\n", events)
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_classify_negative_cases(self) -> None:
        for name in ("negative_missing_entry", "negative_no_authorized_work", "negative_template"):
            self.assertEqual(self.classify_with(name, None, [])["classification"], "PASS", name)
            self.assertEqual(
                self.classify_with(name, probe.EXPECTED_RESULT_BYTES, [])["classification"],
                "FAIL",
                name,
            )

    def test_classify_nested_rejects_scope_confusion(self) -> None:
        self.assertTrue(probe.CASES["negative_nested"].nested)
        evaluation = self.classify_with("negative_nested", None, [])
        self.assertEqual(evaluation["classification"], "PASS")
        self.assertIn("outer_result_created", evaluation)
        self.assertEqual(
            self.classify_with("negative_nested", probe.EXPECTED_RESULT_BYTES, [])["classification"],
            "FAIL",
        )

    def test_classify_adapter_removed_auto_is_observe_only(self) -> None:
        evaluation = self.classify_with("adapter_removed_auto", probe.EXPECTED_RESULT_BYTES, [])
        self.assertEqual(evaluation["classification"], "OBSERVE")

    def test_build_argv_shapes(self) -> None:
        claude_argv = probe.build_argv("claude", probe.TASK_PROMPT, Path("/tmp/x"), "0.75")
        self.assertIn("stream-json", claude_argv)
        self.assertIn("--max-budget-usd", claude_argv)
        self.assertNotIn("--bare", claude_argv)
        codex_argv = probe.build_argv("codex", probe.TASK_PROMPT, Path("/tmp/x"), "0.75")
        self.assertIn("--skip-git-repo-check", codex_argv)
        self.assertIn("--json", codex_argv)
        self.assertIn("workspace-write", codex_argv)

    def test_event_extraction_claude(self) -> None:
        lines = [
            json.dumps({"type": "system", "subtype": "init", "model": "m"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": "/r/BOOTSTRAP.md"}},
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False,
                        "total_cost_usd": 0.1, "permission_denials": []}),
        ]
        extracted = probe.extract_claude_events(lines)
        self.assertEqual(extracted["model"], "m")
        self.assertEqual(extracted["tool_events"][0]["target"], "/r/BOOTSTRAP.md")
        self.assertEqual(extracted["result"]["subtype"], "success")

    def test_event_extraction_codex(self) -> None:
        lines = [
            json.dumps({"type": "turn_context", "model": "gpt"}),
            json.dumps({"item": {"type": "command_execution", "command": "cat BOOTSTRAP.md"}}),
            json.dumps({"item": {"type": "file_change", "changes": [{"path": "/r/RESULT.txt"}]}}),
            json.dumps({"item": {"type": "agent_message", "text": "done"}}),
        ]
        extracted = probe.extract_codex_events(lines)
        self.assertEqual(extracted["model"], "gpt")
        self.assertEqual(len(extracted["tool_events"]), 2)
        self.assertEqual(extracted["result"]["last_message"], "done")


if __name__ == "__main__":
    unittest.main()
