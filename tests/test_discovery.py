import hashlib
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

BRIDGE_NAMES = ("AGENTS.md", "CLAUDE.md")

sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
import validate_protocol as validator  # noqa: E402


def guide_text() -> str:
    return (PROTOCOL / "README.md").read_text(encoding="utf-8")


def guide_section() -> str:
    return guide_text().split("## Discovery bridges", 1)[1]


def extract_snippet() -> str:
    return guide_section().split("```sh", 1)[1].split("```", 1)[0]


def extract_bridge_body() -> str:
    snippet = extract_snippet()
    return snippet.split("cat <<'BRIDGE_BODY'\n", 1)[1].split("\nBRIDGE_BODY", 1)[0] + "\n"


def canonical_bridge_bytes(name: str) -> bytes:
    return ("# Agent discovery bridge (%s)\n\n" % name + extract_bridge_body()).encode("utf-8")


def run_snippet(target: Path) -> subprocess.CompletedProcess:
    lines = [l for l in extract_snippet().splitlines() if not l.startswith("repository_target=")]
    script = 'repository_target="%s"\n%s\n' % (target, "\n".join(lines))
    return subprocess.run(
        ["sh", "-c", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=False,
    )


class RootBridgeTests(unittest.TestCase):
    def test_both_bridges_exist_as_regular_files(self) -> None:
        for name in BRIDGE_NAMES:
            path = REPOSITORY_ROOT / name
            self.assertTrue(path.is_file() and not path.is_symlink(), name)

    def test_bridge_content_properties(self) -> None:
        for name in BRIDGE_NAMES:
            text = (REPOSITORY_ROOT / name).read_text(encoding="utf-8")
            self.assertIn("formally adopts", text, name)
            self.assertIn("BOOTSTRAP.md", text, name)
            self.assertIn("PROJECT_SPEC.md", text, name)
            self.assertIn("HANDOFF.md", text, name)
            self.assertIn("missing or unreadable", text, name)
            self.assertIn("no protocol authority", text, name)
            self.assertIn("governs the repository rooted", text, name)

    def test_bridges_stay_thin(self) -> None:
        for name in BRIDGE_NAMES:
            raw = (REPOSITORY_ROOT / name).read_bytes()
            self.assertLess(len(raw), 4000, name)
            self.assertLess(len(raw.decode("utf-8").splitlines()), 60, name)

    def test_bridges_do_not_restate_normative_semantics(self) -> None:
        for name in BRIDGE_NAMES:
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
        for name in BRIDGE_NAMES:
            self.assertFalse((PROTOCOL / name).exists(), name)


class PackageGuidanceTests(unittest.TestCase):
    def test_guide_documents_discovery_bridges(self) -> None:
        text = guide_text()
        self.assertIn("## Discovery bridges", text)
        self.assertIn("not an eleventh core file", text)
        self.assertIn("is not a support claim", text)
        self.assertIn("never overwrite", text)

    def test_installation_is_self_contained(self) -> None:
        snippet = extract_snippet()
        self.assertNotIn("bridge_reference", snippet)
        self.assertNotIn("agentic-engineering-protocol", snippet)
        self.assertIn("cat <<'BRIDGE_BODY'", snippet)
        self.assertIn("install_bridge AGENTS.md", snippet)
        self.assertIn("install_bridge CLAUDE.md", snippet)
        self.assertIn("collision", snippet)

    def test_embedded_bridge_body_is_portable(self) -> None:
        body = extract_bridge_body()
        self.assertIn("formally adopts", body)
        self.assertIn("BOOTSTRAP.md", body)
        self.assertIn("missing or unreadable", body)
        self.assertIn("governs the repository rooted", body)
        self.assertNotIn("protocol/", body)
        self.assertNotIn("development of this repository", body)
        self.assertNotIn("copy-ready product", body)

    def test_guide_no_longer_references_development_bridges_as_source(self) -> None:
        self.assertNotIn("are the reference bridge content", guide_text())

    def test_quick_start_uses_bridge_with_prompt_as_fallback(self) -> None:
        text = guide_text()
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
    def test_fresh_install_writes_embedded_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge install ") as temporary:
            target = Path(temporary)
            completed = run_snippet(target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for name in BRIDGE_NAMES:
                self.assertEqual((target / name).read_bytes(), canonical_bridge_bytes(name), name)

    def test_installation_needs_only_the_package(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge isolated ") as temporary:
            sandbox = Path(temporary)
            package_only = sandbox / "package"
            shutil.copytree(str(PROTOCOL), str(package_only))
            target = sandbox / "adopting"
            target.mkdir()
            snippet = (
                package_only.joinpath("README.md").read_text(encoding="utf-8")
                .split("## Discovery bridges", 1)[1]
                .split("```sh", 1)[1].split("```", 1)[0]
            )
            lines = [l for l in snippet.splitlines() if not l.startswith("repository_target=")]
            script = 'repository_target="%s"\n%s\n' % (target, "\n".join(lines))
            completed = subprocess.run(
                ["sh", "-c", script], cwd=str(package_only),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for name in BRIDGE_NAMES:
                self.assertEqual((target / name).read_bytes(), canonical_bridge_bytes(name), name)

    def test_installed_bridges_resolve_links_in_adopted_layout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge validate ") as temporary:
            target = Path(temporary)
            shutil.copytree(str(PROTOCOL), str(target), dirs_exist_ok=True)
            completed = run_snippet(target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            for name in BRIDGE_NAMES:
                findings = validator._validate_markdown_file(target, target, target / name)
                self.assertEqual(findings, [], name)

    def test_collision_preserves_existing_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aep bridge merge ") as temporary:
            target = Path(temporary)
            existing = b"# Existing instructions\n\nKeep me.\n"
            (target / "AGENTS.md").write_bytes(existing)
            completed = run_snippet(target)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn("collision", completed.stderr)
            self.assertEqual((target / "AGENTS.md").read_bytes(), existing)
            self.assertEqual((target / "CLAUDE.md").read_bytes(), canonical_bridge_bytes("CLAUDE.md"))


class FixtureTests(unittest.TestCase):
    def test_fixture_is_a_faithful_adopted_instance(self) -> None:
        for relative in PACKAGE_MARKDOWN | {"src/note.txt", probe.ISSUE_REL} | set(BRIDGE_NAMES):
            self.assertTrue((FIXTURE / relative).is_file(), relative)

    def test_fixture_package_files_match_delivered_bytes(self) -> None:
        for relative in (
            "BOOTSTRAP.md", "PROMPTS.md", "EXAMPLE.md", "README.md",
            "HUMAN_CHECKPOINT.md", "ADR/TEMPLATE.md",
            "EVIDENCE/TEMPLATE.md", "ISSUES/TEMPLATE.md",
        ):
            self.assertEqual(
                (FIXTURE / relative).read_bytes(),
                (PROTOCOL / relative).read_bytes(),
                relative,
            )

    def test_fixture_bridges_match_delivered_installation(self) -> None:
        for name in BRIDGE_NAMES:
            self.assertEqual((FIXTURE / name).read_bytes(), canonical_bridge_bytes(name), name)

    def test_fixture_spec_authorizes_expected_task(self) -> None:
        spec = (FIXTURE / "PROJECT_SPEC.md").read_text(encoding="utf-8")
        self.assertIn("`ACCEPTED`", spec)
        self.assertIn("T-001", spec)
        self.assertIn("AUTHORIZED", spec)
        self.assertIn(probe.EXPECTED_RESULT_BYTES.decode("utf-8").strip(), spec)
        self.assertIn("No other work is authorized", spec)
        self.assertIn(probe.ISSUE_REL.split("/", 1)[1], spec)

    def test_fixture_handoff_has_five_sections(self) -> None:
        text = (FIXTURE / "HANDOFF.md").read_text(encoding="utf-8")
        for section in ("Current State", "Active Issues", "Next Action", "Recent Activity", "Archived Summary"):
            self.assertIn("## %s" % section, text)
        self.assertIn("T-001", text)

    def test_fixture_issue_records_self_review_gate(self) -> None:
        text = (FIXTURE / probe.ISSUE_REL).read_text(encoding="utf-8")
        self.assertIn("`AGENT`", text)
        self.assertIn("`SELF`", text)
        self.assertIn("`OPEN`", text)

    def test_manual_fallback_prompt_is_the_delivered_prompt(self) -> None:
        prompt = probe._manual_onboarding_prompt()
        delivered = (PROTOCOL / "PROMPTS.md").read_text(encoding="utf-8")
        self.assertIn("Read BOOTSTRAP.md completely", prompt)
        self.assertNotIn("[repository]", prompt)
        block = delivered.split("## Fresh implementor or onboarding", 1)[1].split("```text", 1)[1].split("```", 1)[0].strip()
        expected = block.replace("[repository]", "this repository").replace(
            "[task/scope, or the highest-priority safe active issue]",
            "the highest-priority safe active issue",
        )
        self.assertEqual(prompt, expected)


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
            spec = (no_work / "PROJECT_SPEC.md").read_text(encoding="utf-8")
            self.assertIn("No task is currently authorized", spec)
            self.assertIn("`ACCEPTED`", spec)

            collision = self.copy_fixture(root / "c")
            probe.CASES["negative_collision"].transform(collision)
            merged = (collision / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("MUST NOT be modified", merged)
            self.assertIn("BOOTSTRAP.md", merged)
            self.assertEqual((collision / "KEEP.txt").read_bytes(), probe.KEEP_SENTINEL_BYTES)

            removed = self.copy_fixture(root / "d")
            probe.CASES["adapter_removed_auto"].transform(removed)
            self.assertFalse((removed / "AGENTS.md").exists())
            self.assertFalse((removed / "CLAUDE.md").exists())
            self.assertTrue((removed / "BOOTSTRAP.md").is_file())

            template = self.copy_fixture(root / "e")
            probe.CASES["negative_template"].transform(template)
            templated = (template / "PROJECT_SPEC.md").read_text(encoding="utf-8")
            self.assertIn("`DRAFT`", templated)
            self.assertEqual(
                (template / "PROJECT_SPEC.md").read_bytes(),
                (PROTOCOL / "PROJECT_SPEC.md").read_bytes(),
            )

            outer = root / "outer"
            outer.mkdir()
            probe.CASES["negative_nested"].transform(outer)
            self.assertFalse((outer / "BOOTSTRAP.md").exists())
            self.assertTrue((outer / "nested_repo" / "BOOTSTRAP.md").is_file())
            self.assertTrue((outer / "README.md").is_file())


def base_manifest() -> dict:
    return {
        "BOOTSTRAP.md": "sha-bootstrap",
        "PROJECT_SPEC.md": "sha-spec",
        "HANDOFF.md": "sha-handoff",
        probe.ISSUE_REL: "sha-issue",
        "AGENTS.md": "sha-agents",
        "CLAUDE.md": "sha-claude",
        "README.md": "sha-readme",
        "src/note.txt": "sha-note",
    }


def read(seq: int, path: str, success=True) -> dict:
    return {"seq": seq, "tool": "Read", "target": "/repo/%s" % path, "kind": "read", "success": success}


def write(seq: int, path: str) -> dict:
    return {"seq": seq, "tool": "Write", "target": "/repo/%s" % path, "kind": "mutation", "success": True}


def shell(seq: int, command: str, success=True) -> dict:
    return {"seq": seq, "tool": "Bash", "target": command, "kind": "shell", "success": success}


GOOD_RECOVERY_EVENTS = [
    read(0, "BOOTSTRAP.md"),
    read(1, "PROJECT_SPEC.md"),
    read(2, probe.ISSUE_REL),
    read(3, "HANDOFF.md"),
]

CLAUDE_SUCCESS = {"subtype": "success", "is_error": False}
CODEX_SUCCESS = {"turn_completed": True, "last_message": "done"}


def positive_post(pre: dict) -> dict:
    post = dict(pre)
    post[probe.EXPECTED_RESULT_PATH] = probe.EXPECTED_RESULT_SHA256
    post["HANDOFF.md"] = "sha-handoff-updated"
    post[probe.ISSUE_REL] = "sha-issue-updated"
    return post


def positive_events() -> list:
    return GOOD_RECOVERY_EVENTS + [
        write(4, probe.EXPECTED_RESULT_PATH),
        shell(5, 'od -c "/repo/RESULT.txt"'),
        write(6, "HANDOFF.md"),
        write(7, probe.ISSUE_REL),
    ]


class OracleTests(unittest.TestCase):
    def classify(self, case_name, pre, post, events, harness="claude",
                 exit_code=0, session_result=None) -> dict:
        if session_result is None:
            session_result = CLAUDE_SUCCESS if harness == "claude" else CODEX_SUCCESS
        return probe.classify(
            probe.CASES[case_name], pre, post, events, exit_code, session_result, harness,
        )

    def test_positive_pass_requires_complete_evidence(self) -> None:
        pre = base_manifest()
        evaluation = self.classify("positive_root", pre, positive_post(pre), positive_events())
        self.assertEqual(evaluation["classification"], "PASS", evaluation)

    def test_positive_pass_codex_shell_reads(self) -> None:
        pre = base_manifest()
        events = [
            shell(0, "/bin/zsh -lc 'cat BOOTSTRAP.md'"),
            shell(1, "/bin/zsh -lc 'cat PROJECT_SPEC.md %s HANDOFF.md'" % probe.ISSUE_REL),
            {"seq": 2, "tool": "file_change", "target": "/repo/RESULT.txt", "kind": "mutation", "success": True},
            shell(3, "/bin/zsh -lc \"python3 -c 'from pathlib import Path; assert Path(\\\"RESULT.txt\\\").read_bytes()'\""),
            {"seq": 4, "tool": "file_change", "target": "/repo/HANDOFF.md", "kind": "mutation", "success": True},
            {"seq": 5, "tool": "file_change", "target": "/repo/%s" % probe.ISSUE_REL, "kind": "mutation", "success": True},
        ]
        evaluation = self.classify("positive_root", pre, positive_post(pre), events, harness="codex")
        self.assertEqual(evaluation["classification"], "PASS", evaluation)

    def test_adverse_filename_mention_is_not_recovery(self) -> None:
        pre = base_manifest()
        events = [shell(0, "echo BOOTSTRAP.md"), write(1, probe.EXPECTED_RESULT_PATH)]
        evaluation = self.classify("positive_root", pre, positive_post(pre), events)
        self.assertNotEqual(evaluation["classification"], "PASS")

    def test_adverse_read_without_success_or_full_recovery(self) -> None:
        pre = base_manifest()
        events = [read(0, "BOOTSTRAP.md", success=None), write(1, probe.EXPECTED_RESULT_PATH)]
        evaluation = self.classify("positive_root", pre, positive_post(pre), events)
        self.assertNotEqual(evaluation["classification"], "PASS")

    def test_adverse_collision_sentinel_deleted(self) -> None:
        pre = base_manifest()
        pre[probe.KEEP_SENTINEL] = hashlib.sha256(probe.KEEP_SENTINEL_BYTES).hexdigest()
        post = positive_post(pre)
        del post[probe.KEEP_SENTINEL]
        evaluation = self.classify("negative_collision", pre, post, positive_events())
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_adverse_negative_unauthorized_mutation(self) -> None:
        pre = base_manifest()
        post = dict(pre)
        post["OTHER.txt"] = "sha-other"
        events = [write(0, "OTHER.txt")]
        evaluation = self.classify("negative_no_authorized_work", pre, post, events)
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_negative_fails_on_authority_or_deliverable_mutation(self) -> None:
        pre = base_manifest()
        post = dict(pre)
        post["PROJECT_SPEC.md"] = "sha-defaced"
        evaluation = self.classify("negative_no_authorized_work", pre, post, [])
        self.assertEqual(evaluation["classification"], "FAIL")
        post = dict(pre)
        post[probe.EXPECTED_RESULT_PATH] = probe.EXPECTED_RESULT_SHA256
        evaluation = self.classify("negative_conflicting_authority", pre, post, [])
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_negative_allows_record_maintenance_mutation(self) -> None:
        pre = base_manifest()
        post = dict(pre)
        post["HANDOFF.md"] = "sha-handoff-note"
        post["ISSUES/ISSUE-20260921T095950Z-contradiction.md"] = "sha-new-issue"
        evaluation = self.classify("negative_no_authorized_work", pre, post, [])
        self.assertEqual(evaluation["classification"], "PASS")

    def test_adverse_negative_without_session_evidence_is_unverified(self) -> None:
        pre = base_manifest()
        evaluation = self.classify(
            "negative_no_authorized_work", pre, dict(pre), [], exit_code=None, session_result={},
        )
        self.assertEqual(evaluation["classification"], "UNVERIFIED")

    def test_positive_fails_on_wrong_content(self) -> None:
        pre = base_manifest()
        post = positive_post(pre)
        post[probe.EXPECTED_RESULT_PATH] = "sha-wrong"
        evaluation = self.classify("positive_root", pre, post, positive_events())
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_positive_fails_when_recovery_read_follows_mutation(self) -> None:
        pre = base_manifest()
        events = [
            read(0, "BOOTSTRAP.md"),
            read(1, "PROJECT_SPEC.md"),
            write(2, probe.EXPECTED_RESULT_PATH),
            read(3, probe.ISSUE_REL),
            read(4, "HANDOFF.md"),
            shell(5, "cat RESULT.txt"),
            write(6, "HANDOFF.md"),
            write(7, probe.ISSUE_REL),
        ]
        evaluation = self.classify("positive_root", pre, positive_post(pre), events)
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_positive_unverified_without_verification_event(self) -> None:
        pre = base_manifest()
        events = GOOD_RECOVERY_EVENTS + [
            write(4, probe.EXPECTED_RESULT_PATH),
            write(5, "HANDOFF.md"),
            write(6, probe.ISSUE_REL),
        ]
        evaluation = self.classify("positive_root", pre, positive_post(pre), events)
        self.assertEqual(evaluation["classification"], "UNVERIFIED")

    def test_positive_unverified_with_empty_chronology(self) -> None:
        pre = base_manifest()
        evaluation = self.classify("positive_root", pre, positive_post(pre), [])
        self.assertEqual(evaluation["classification"], "UNVERIFIED")

    def test_positive_fails_on_unexpected_mutation(self) -> None:
        pre = base_manifest()
        post = positive_post(pre)
        post["README.md"] = "sha-defaced"
        evaluation = self.classify("positive_root", pre, post, positive_events())
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_positive_fails_without_handoff_or_issue_update(self) -> None:
        pre = base_manifest()
        post = dict(pre)
        post[probe.EXPECTED_RESULT_PATH] = probe.EXPECTED_RESULT_SHA256
        evaluation = self.classify("positive_root", pre, post, positive_events())
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_positive_unverified_when_session_incomplete(self) -> None:
        pre = base_manifest()
        evaluation = self.classify(
            "positive_root", pre, positive_post(pre), positive_events(),
            session_result={"subtype": "error_max_budget_usd", "is_error": True},
        )
        self.assertEqual(evaluation["classification"], "UNVERIFIED")

    def test_negative_cases_pass_only_on_completed_noop(self) -> None:
        pre = base_manifest()
        for name in ("negative_missing_entry", "negative_no_authorized_work", "negative_template"):
            evaluation = self.classify(name, pre, dict(pre), GOOD_RECOVERY_EVENTS)
            self.assertEqual(evaluation["classification"], "PASS", name)

    def test_negative_missing_entry_still_passes_with_no_reads(self) -> None:
        pre = base_manifest()
        evaluation = self.classify("negative_missing_entry", pre, dict(pre), [])
        self.assertEqual(evaluation["classification"], "PASS")

    def test_nested_rejects_scope_confusion(self) -> None:
        pre = {"README.md": "sha-outer", "nested_repo/BOOTSTRAP.md": "sha-nested"}
        evaluation = self.classify("negative_nested", pre, dict(pre), [])
        self.assertEqual(evaluation["classification"], "PASS")
        post = dict(pre)
        post["nested_repo/RESULT.txt"] = probe.EXPECTED_RESULT_SHA256
        evaluation = self.classify("negative_nested", pre, post, [])
        self.assertEqual(evaluation["classification"], "FAIL")

    def test_adapter_removed_auto_is_observe_only(self) -> None:
        pre = base_manifest()
        evaluation = self.classify("adapter_removed_auto", pre, positive_post(pre), positive_events())
        self.assertEqual(evaluation["classification"], "OBSERVE")

    def test_shell_read_detection(self) -> None:
        self.assertTrue(probe.is_shell_read("/bin/zsh -lc 'cat BOOTSTRAP.md'", "BOOTSTRAP.md"))
        self.assertTrue(probe.is_shell_read("cat PROJECT_SPEC.md HANDOFF.md", "HANDOFF.md"))
        self.assertFalse(probe.is_shell_read("echo BOOTSTRAP.md", "BOOTSTRAP.md"))
        self.assertFalse(probe.is_shell_read("cat /etc/BOOTSTRAP.md.bak", "BOOTSTRAP.md"))
        self.assertFalse(probe.is_shell_read("cat BOOTSTRAP.md > copy.txt", "BOOTSTRAP.md"))
        self.assertFalse(probe.is_shell_read("sed -i '' s/a/b/ BOOTSTRAP.md", "BOOTSTRAP.md"))

    def test_python_write_idioms_are_mutations(self) -> None:
        for command in (
            "/bin/zsh -lc \"python3 - <<'PY'\nPath('RESULT.txt').write_bytes(b'x')\nPY\"",
            "python3 -c \"Path('HANDOFF.md').write_text('x')\"",
            "python3 -c \"open('RESULT.txt','w').write('x')\"",
        ):
            self.assertTrue(probe.SHELL_WRITE_PATTERN.search(command), command)
        for command in (
            "python3 -c \"print(Path('RESULT.txt').read_bytes())\"",
            "python3 - <<'PY'\nprint('a->b')\nPY",
            "ls RESULT.txt 2>&1; ls src",
            "cat BOOTSTRAP.md 2>/dev/null",
            "printf 'x\\n' | cmp - RESULT.txt && echo ok",
        ):
            self.assertFalse(probe.SHELL_WRITE_PATTERN.search(command), command)

    def test_unwrap_shell(self) -> None:
        self.assertEqual(probe.unwrap_shell("/bin/zsh -lc 'cat BOOTSTRAP.md'"), "cat BOOTSTRAP.md")
        self.assertEqual(probe.unwrap_shell('bash -c "cat HANDOFF.md"'), "cat HANDOFF.md")
        self.assertEqual(probe.unwrap_shell("cat BOOTSTRAP.md"), "cat BOOTSTRAP.md")

    def test_references_path_boundaries(self) -> None:
        self.assertTrue(probe.references_path("/repo/BOOTSTRAP.md", "BOOTSTRAP.md"))
        self.assertTrue(probe.references_path("cat ../BOOTSTRAP.md", "BOOTSTRAP.md"))
        self.assertFalse(probe.references_path("/repo/BOOTSTRAP.md.bak", "BOOTSTRAP.md"))
        self.assertFalse(probe.references_path("MYBOOTSTRAP.md", "BOOTSTRAP.md"))
        self.assertTrue(probe.references_path("/repo/%s" % probe.ISSUE_REL, probe.ISSUE_REL))

    def test_build_argv_shapes(self) -> None:
        claude_argv = probe.build_argv("claude", probe.TASK_PROMPT, Path("/tmp/x"), "0.75")
        self.assertIn("stream-json", claude_argv)
        self.assertIn("--max-budget-usd", claude_argv)
        self.assertNotIn("--bare", claude_argv)
        codex_argv = probe.build_argv("codex", probe.TASK_PROMPT, Path("/tmp/x"), "0.75")
        self.assertIn("--skip-git-repo-check", codex_argv)
        self.assertIn("--json", codex_argv)
        self.assertIn("workspace-write", codex_argv)

    def test_event_extraction_claude_pairs_outcomes(self) -> None:
        lines = [
            json.dumps({"type": "system", "subtype": "init", "model": "m"}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "/r/BOOTSTRAP.md"}},
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": "ok"},
            ]}}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t2", "name": "Write", "input": {"file_path": "/r/RESULT.txt"}},
            ]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t2", "is_error": True, "content": "denied"},
            ]}}),
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t3", "name": "Bash", "input": {"command": "od -c /r/RESULT.txt"}},
            ]}}),
            json.dumps({"type": "result", "subtype": "success", "is_error": False,
                        "total_cost_usd": 0.1, "permission_denials": []}),
        ]
        extracted = probe.extract_claude_events(lines)
        self.assertEqual(extracted["model"], "m")
        events = extracted["tool_events"]
        self.assertEqual([e["kind"] for e in events], ["read", "mutation", "shell"])
        self.assertEqual([e["success"] for e in events], [True, False, None])
        self.assertEqual(extracted["result"]["subtype"], "success")

    def test_event_extraction_codex_completed_only(self) -> None:
        lines = [
            json.dumps({"type": "turn_context", "model": "gpt"}),
            json.dumps({"type": "item.started", "item": {"type": "command_execution",
                        "command": "cat BOOTSTRAP.md", "status": "in_progress"}}),
            json.dumps({"type": "item.completed", "item": {"type": "command_execution",
                        "command": "cat BOOTSTRAP.md", "exit_code": 0, "status": "completed"}}),
            json.dumps({"type": "item.completed", "item": {"type": "command_execution",
                        "command": "git status", "exit_code": 128, "status": "failed"}}),
            json.dumps({"type": "item.completed", "item": {"type": "file_change", "status": "completed",
                        "changes": [{"path": "/r/RESULT.txt", "kind": "add"},
                                    {"path": "/r/HANDOFF.md", "kind": "update"}]}}),
            json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "done"}}),
            json.dumps({"type": "turn.completed"}),
        ]
        extracted = probe.extract_codex_events(lines)
        self.assertEqual(extracted["model"], "gpt")
        events = extracted["tool_events"]
        self.assertEqual(len(events), 4)
        self.assertEqual(events[0]["kind"], "shell")
        self.assertIs(events[0]["success"], True)
        self.assertIs(events[1]["success"], False)
        self.assertEqual([e["kind"] for e in events[2:]], ["mutation", "mutation"])
        self.assertTrue(extracted["result"]["turn_completed"])
        self.assertEqual(extracted["result"]["last_message"], "done")

    def test_session_completed_rules(self) -> None:
        self.assertTrue(probe.session_completed("claude", 0, CLAUDE_SUCCESS))
        self.assertFalse(probe.session_completed("claude", 0, {"subtype": "success", "is_error": True}))
        self.assertFalse(probe.session_completed("claude", 1, CLAUDE_SUCCESS))
        self.assertTrue(probe.session_completed("codex", 0, CODEX_SUCCESS))
        self.assertFalse(probe.session_completed("codex", 0, {}))
        self.assertFalse(probe.session_completed("codex", None, CODEX_SUCCESS))


if __name__ == "__main__":
    unittest.main()
