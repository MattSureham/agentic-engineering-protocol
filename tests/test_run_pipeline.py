import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PIPELINE = REPOSITORY_ROOT / "scripts" / "run_pipeline.py"
SCRIPTS = REPOSITORY_ROOT / "scripts"
SOURCE_PROTOCOL = REPOSITORY_ROOT / "protocol"
SOURCE_HANDOFF = REPOSITORY_ROOT / "HANDOFF.md"
sys.path.insert(0, str(SCRIPTS))
import run_pipeline as pipeline  # noqa: E402


INTERVENING_ISSUE = "ISSUES/ISSUE-20260814T030050Z-intervening-authority.md"


class PipelineRepository:
    def __init__(self, milestone_count: int = 1, failing_check: bool = False) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="aep pipeline ")
        self.root = Path(self.temporary.name) / "repository with spaces"
        self.root.mkdir()
        shutil.copytree(str(SOURCE_PROTOCOL), str(self.root / "protocol"))
        shutil.copy2(str(SOURCE_HANDOFF), str(self.root / "HANDOFF.md"))
        (self.root / "ISSUES").mkdir()
        (self.root / "EVIDENCE").mkdir()
        (self.root / "work").mkdir()
        self.milestones = [self._milestone(index + 1, failing_check and index == 0) for index in range(milestone_count)]
        self._write_spec("ACCEPTED")
        for milestone in self.milestones:
            self._write_issue(milestone)
        self._write_blocker()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Pipeline Test")
        self.git("config", "user.email", "pipeline@example.invalid")
        self.commit("fixture baseline")

    def cleanup(self) -> None:
        self.temporary.cleanup()

    def _milestone(self, order: int, failing_check: bool) -> Dict[str, Any]:
        milestone_id = "MILESTONE-20260814T03000{}Z-fixture-{}".format(order, order)
        depends = [] if order == 1 else ["MILESTONE-20260814T03000{}Z-fixture-{}".format(order - 1, order - 1)]
        command = "raise SystemExit(7)" if failing_check else "raise SystemExit(0)"
        return {
            "id": milestone_id,
            "order": order,
            "title": "Fixture milestone {}".format(order),
            "issue": "ISSUES/ISSUE-20260814T03000{}Z-fixture-{}.md".format(order, order),
            "depends_on": depends,
            "scope": ["Exercise fixture milestone {}".format(order)],
            "allowed_paths": [
                "ISSUES/ISSUE-20260814T03000{}Z-fixture-{}.md".format(order, order),
                "EVIDENCE/",
                "work/",
            ],
            "acceptance_checks": [
                {
                    "id": "fixture-check",
                    "argv": [sys.executable, "-c", command],
                    "timeout_seconds": 10,
                }
            ],
            "review": "INDEPENDENT",
        }

    def _write_spec(self, status: str) -> None:
        contract = {"schema": pipeline.CONTRACT_SCHEMA, "milestones": self.milestones}
        text = """# Fixture specification

# Specification status

- **Status:** `{status}`

# Authorized milestones

{begin}
```json
{contract}
```
{end}
""".format(
            status=status,
            begin=pipeline.CONTRACT_BEGIN,
            contract=json.dumps(contract, indent=2),
            end=pipeline.CONTRACT_END,
        )
        (self.root / "PROJECT_SPEC.md").write_text(text, encoding="utf-8")

    def _initial_state(self, milestone: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "schema": pipeline.STATE_SCHEMA,
            "milestone_id": milestone["id"],
            "authority_digest": pipeline._canonical_digest(milestone),
            "state": "AUTHORIZED",
            "attempt": 0,
            "implementor": None,
            "base_revision": None,
            "target_revision": None,
            "verification_evidence": [],
            "review_references": [],
            "events": [
                {
                    "sequence": 1,
                    "utc": "2026-08-14T03:00:00Z",
                    "actor": "human:fixture-owner",
                    "from": None,
                    "to": "AUTHORIZED",
                    "reason": "Accepted fixture specification.",
                }
            ],
        }

    def _write_issue(self, milestone: Dict[str, Any]) -> None:
        state = self._initial_state(milestone)
        issue_id = Path(milestone["issue"]).stem
        text = """# Fixture issue

## Metadata

- **ID:** `{issue_id}`
- **Title:** `Fixture`
- **Status:** `INVESTIGATING`
- **Severity:** `MEDIUM`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-14T03:00:00Z`
- **Updated UTC:** `2026-08-14T03:00:00Z`
- **Requirements:** `PROJECT_SPEC.md`
- **ADRs:** `NONE`
- **Evidence:** `NONE YET`
- **Milestone:** `{milestone_id}`

## Problem

Fixture.

## Verification

No verification yet.

## Pipeline state

{state_begin}
```json
{state}
```
{state_end}

## Self-review

- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES`

No independent review round has been recorded.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-14T03:00:00Z` | `human:fixture-owner` | `NONE` | `AUTHORIZED` | Accepted fixture. |

## Closure checklist

- [x] Expected behavior is authoritative.
- [x] Change is recorded.
- [x] Verification is linked.
- [x] Independent review is approved.
- [x] Authority is recorded.
""".format(
            issue_id=issue_id,
            milestone_id=milestone["id"],
            state_begin=pipeline.STATE_BEGIN,
            state=json.dumps(state, indent=2),
            state_end=pipeline.STATE_END,
        )
        (self.root / milestone["issue"]).write_text(text, encoding="utf-8")

    def _write_blocker(self) -> None:
        text = """# Human blocker

## Metadata

- **ID:** `ISSUE-20260814T030099Z-human-blocker`
- **Status:** `BLOCKED`
- **Authority:** `HUMAN`

## Blocker

- **Blocked from:** `OPEN`
- **Blocker:** `Owner decision missing`
- **Unblock owner:** `Human technical owner`
- **Unblock condition:** `Owner records the required product decision in PROJECT_SPEC.md.`
"""
        (self.root / "ISSUES" / "ISSUE-20260814T030099Z-human-blocker.md").write_text(text, encoding="utf-8")

    def run(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(PIPELINE)] + list(arguments) + ["--root", str(self.root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )

    def git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git"] + list(arguments), cwd=str(self.root), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, check=False,
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        return result.stdout.strip()

    def commit(self, message: str) -> str:
        self.git("add", "--all")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def issue_path(self, index: int = 0) -> Path:
        return self.root / self.milestones[index]["issue"]

    def configure_check(self, argv: List[str], timeout_seconds: int = 10) -> None:
        self.milestones[0]["acceptance_checks"][0]["argv"] = argv
        self.milestones[0]["acceptance_checks"][0]["timeout_seconds"] = timeout_seconds
        self._write_spec("ACCEPTED")
        self._write_issue(self.milestones[0])
        self.commit("configure acceptance check")

    def failure_evidence(self) -> Dict[str, Any]:
        records = list((self.root / "EVIDENCE").glob("*.json"))
        if len(records) != 1:
            raise AssertionError("expected one evidence record, found {}".format(len(records)))
        return json.loads(records[0].read_text(encoding="utf-8"))

    def state(self, index: int = 0) -> Dict[str, Any]:
        text = self.issue_path(index).read_text(encoding="utf-8")
        return pipeline._extract_json_block(text, pipeline.STATE_BEGIN, pipeline.STATE_END, self.milestones[index]["issue"])

    def begin(self, index: int = 0, actor: str = "agent:implementor") -> None:
        milestone_id = self.milestones[index]["id"]
        result = self.run("transition", "--milestone", milestone_id, "--actor", actor, "--to", "READY")
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        self.commit("ready")
        result = self.run("transition", "--milestone", milestone_id, "--actor", actor, "--to", "IN_PROGRESS")
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)

    def make_target(self, index: int = 0, value: str = "implementation\n") -> str:
        (self.root / "work" / "milestone-{}.txt".format(index + 1)).write_text(value, encoding="utf-8")
        return self.commit("implementation target")

    def submit(self, target: str, index: int = 0, actor: str = "agent:implementor") -> subprocess.CompletedProcess:
        return self.run(
            "transition", "--milestone", self.milestones[index]["id"],
            "--actor", actor, "--to", "AWAITING_PEER_REVIEW", "--target", target,
        )

    def add_review(
        self,
        target: str,
        disposition: str,
        material: int,
        index: int = 0,
        reviewer: str = "agent:reviewer",
        utc: str = "2026-08-14T03:30:00Z",
    ) -> None:
        path = self.issue_path(index)
        text = path.read_text(encoding="utf-8")
        round_text = """
### {utc} — {reviewer}

- **Reviewed target:** `{target}`
- **Open material findings:** `{material}`
- **Scope:** `Fixture target`
- **Commands or procedures:** `Fixture review`
- **Specification compliance:** `Checked`
- **Correctness and regression findings:** `NONE`
- **Architecture and complexity findings:** `NONE`
- **Material findings and resolution conditions:** `NONE or fixture`
- **Limitations:** `Fixture only`
- **Residual risks:** `NONE`
- **Evidence:** `Inline fixture`
- **Disposition:** `{disposition}`
- **Prior-round resolution:** `FIRST ROUND or resolved`

""".format(utc=utc, reviewer=reviewer, target=target, material=material, disposition=disposition)
        text = text.replace("\n## Blocker", "\n" + round_text + "## Blocker", 1)
        path.write_text(text, encoding="utf-8")

    def write_intervening_issue(
        self,
        path: str = INTERVENING_ISSUE,
        authority: str = "HUMAN",
        review: str = "INDEPENDENT",
        status: str = "OPEN",
        unblock: str = "SATISFIED - owner decision recorded in this issue",
    ) -> None:
        text = """# Intervening authority record

## Metadata

- **ID:** `ISSUE-20260814T030050Z-intervening-authority`
- **Status:** `{status}`
- **Authority:** `{authority}`
- **Review:** `{review}`

## Independent review rounds

- **Required:** `YES`

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `human:fixture-owner`
- **Unblock condition:** `{unblock}`
""".format(status=status, authority=authority, review=review, unblock=unblock)
        (self.root / path).write_text(text, encoding="utf-8")

    def add_intervening_review(
        self,
        target: str,
        disposition: str = "APPROVED",
        material: int = 0,
        reviewer: str = "agent:intervening-reviewer",
        utc: str = "2026-08-14T03:25:00Z",
        path: str = INTERVENING_ISSUE,
    ) -> None:
        issue_path = self.root / path
        text = issue_path.read_text(encoding="utf-8")
        round_text = """
### {utc} — {reviewer}

- **Reviewed immutable state:** `{target}` (fixture intervening amendment).
- **Open material findings:** **{material}**.
- **Disposition:** **{disposition}**.

""".format(utc=utc, reviewer=reviewer, target=target, material=material, disposition=disposition)
        text = text.replace("\n## Blocker", "\n" + round_text + "## Blocker", 1)
        issue_path.write_text(text, encoding="utf-8")

    def add_registry(self, entries: Any, index: int = 0, schema: str = pipeline.INTERVENING_SCHEMA) -> None:
        block = {"schema": schema, "entries": entries}
        path = self.issue_path(index)
        text = path.read_text(encoding="utf-8")
        registry = (
            pipeline.INTERVENING_BEGIN + "\n```json\n" + json.dumps(block, indent=2) + "\n```\n" + pipeline.INTERVENING_END
        )
        text = text.replace("\n## Self-review", "\n## Intervening authority\n\n" + registry + "\n\n## Self-review", 1)
        path.write_text(text, encoding="utf-8")


class AuthorizedMilestonePipelineTests(unittest.TestCase):
    def fixture(self, *arguments: Any, **keywords: Any) -> PipelineRepository:
        fixture = PipelineRepository(*arguments, **keywords)
        self.addCleanup(fixture.cleanup)
        return fixture

    @staticmethod
    def snapshot(root: Path) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for path in sorted(root.rglob("*")):
            if ".git" in path.relative_to(root).parts or not path.is_file():
                continue
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        return result

    def test_status_is_deterministic_read_only_and_machine_readable(self) -> None:
        fixture = self.fixture()
        before = self.snapshot(fixture.root)
        first = fixture.run("status", "--json")
        second = fixture.run("status", "--json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual((first.stdout, first.stderr), (second.stdout, second.stderr))
        payload = json.loads(first.stdout)
        self.assertEqual(payload["schema"], pipeline.STATUS_SCHEMA)
        self.assertEqual(payload["selected_milestone"], fixture.milestones[0]["id"])
        self.assertEqual(before, self.snapshot(fixture.root))

    def test_draft_specification_is_not_authority_and_does_not_mutate(self) -> None:
        fixture = self.fixture()
        fixture._write_spec("DRAFT")
        before = self.snapshot(fixture.root)
        result = fixture.run("status")
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PIPE-AUTH", result.stderr)
        self.assertEqual(before, self.snapshot(fixture.root))

    def test_malformed_duplicate_and_unsupported_contracts_fail_closed(self) -> None:
        mutations = []

        def duplicate_key(fixture: PipelineRepository) -> None:
            path = fixture.root / "PROJECT_SPEC.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace('"schema": "aep-authorized-milestones/v1",', '"schema": "aep-authorized-milestones/v1",\n  "schema": "aep-authorized-milestones/v1",', 1)
            path.write_text(text, encoding="utf-8")

        def duplicate_marker(fixture: PipelineRepository) -> None:
            path = fixture.root / "PROJECT_SPEC.md"
            path.write_text(path.read_text(encoding="utf-8") + pipeline.CONTRACT_BEGIN + "\n", encoding="utf-8")

        def unsupported_schema(fixture: PipelineRepository) -> None:
            path = fixture.root / "PROJECT_SPEC.md"
            path.write_text(path.read_text(encoding="utf-8").replace(pipeline.CONTRACT_SCHEMA, "aep-authorized-milestones/v2"), encoding="utf-8")

        def duplicate_milestone(fixture: PipelineRepository) -> None:
            duplicate = json.loads(json.dumps(fixture.milestones[0]))
            duplicate["issue"] = "ISSUES/ISSUE-20260814T030098Z-duplicate.md"
            duplicate["order"] = 2
            fixture.milestones.append(duplicate)
            fixture._write_spec("ACCEPTED")

        mutations.extend([duplicate_key, duplicate_marker, unsupported_schema, duplicate_milestone])
        for mutate in mutations:
            with self.subTest(mutation=mutate.__name__):
                fixture = PipelineRepository()
                try:
                    mutate(fixture)
                    before = self.snapshot(fixture.root)
                    result = fixture.run("status")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("AEP-PIPE-SCHEMA", result.stderr)
                    self.assertEqual(before, self.snapshot(fixture.root))
                finally:
                    fixture.cleanup()

    def test_contract_rejects_path_escape_dependency_order_and_digest_drift(self) -> None:
        cases = ("path", "dependency", "digest")
        for case in cases:
            with self.subTest(case=case):
                fixture = PipelineRepository(milestone_count=2)
                try:
                    if case == "path":
                        fixture.milestones[0]["allowed_paths"].append("../escape")
                        fixture._write_spec("ACCEPTED")
                    elif case == "dependency":
                        fixture.milestones[0]["depends_on"] = [fixture.milestones[1]["id"]]
                        fixture._write_spec("ACCEPTED")
                    else:
                        path = fixture.issue_path()
                        text = path.read_text(encoding="utf-8").replace(
                            pipeline._canonical_digest(fixture.milestones[0]), "0" * 64, 1
                        )
                        path.write_text(text, encoding="utf-8")
                    result = fixture.run("status")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("AEP-PIPE-", result.stderr)
                finally:
                    fixture.cleanup()

    def test_structural_validator_is_reused(self) -> None:
        fixture = self.fixture()
        (fixture.root / "protocol" / "EXAMPLE.md").unlink()
        result = fixture.run("status")
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PIPE-STRUCTURE", result.stderr)
        self.assertIn("AEP-PKG-001", result.stderr)

    def test_full_lifecycle_accepts_reviewed_target(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        target = fixture.make_target()
        submitted = fixture.submit(target)
        self.assertEqual(submitted.returncode, 0, submitted.stderr)
        state = fixture.state()
        self.assertEqual(state["state"], "AWAITING_PEER_REVIEW")
        self.assertEqual(state["target_revision"], target)
        self.assertEqual(len(state["verification_evidence"]), 1)
        evidence = fixture.root / state["verification_evidence"][0]
        self.assertEqual(json.loads(evidence.read_text(encoding="utf-8"))["result"], "PASS")
        fixture.commit("review handoff")
        fixture.add_review(target, "APPROVED", 0)
        fixture.commit("independent review")
        accepted = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "ACCEPTED",
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertEqual(fixture.state()["state"], "ACCEPTED")

    def test_material_findings_drive_fix_and_rereview(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        first_target = fixture.make_target()
        self.assertEqual(fixture.submit(first_target).returncode, 0)
        fixture.commit("first handoff")
        fixture.add_review(first_target, "CHANGES_REQUIRED", 1)
        fixture.commit("first review")
        changes = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "CHANGES_REQUIRED",
        )
        self.assertEqual(changes.returncode, 0, changes.stderr)
        fixture.commit("changes required")
        resumed = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        second_target = fixture.make_target(value="fixed\n")
        self.assertNotEqual(first_target, second_target)
        self.assertEqual(fixture.submit(second_target).returncode, 0)
        fixture.commit("second handoff")
        fixture.add_review(second_target, "APPROVED", 0, utc="2026-08-14T03:40:00Z")
        fixture.commit("second review")
        accepted = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "ACCEPTED",
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        state = fixture.state()
        self.assertEqual(state["state"], "ACCEPTED")
        self.assertEqual(state["attempt"], 2)
        self.assertEqual(len(state["verification_evidence"]), 2)
        self.assertEqual(len(state["review_references"]), 2)

    def test_second_authorized_milestone_selected_after_acceptance(self) -> None:
        fixture = self.fixture(milestone_count=2)
        fixture.begin()
        target = fixture.make_target()
        self.assertEqual(fixture.submit(target).returncode, 0)
        fixture.commit("handoff")
        fixture.add_review(target, "APPROVED", 0)
        fixture.commit("review")
        result = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "ACCEPTED",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        status = fixture.run("status", "--json")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(json.loads(status.stdout)["selected_milestone"], fixture.milestones[1]["id"])

    def test_out_of_scope_target_is_rejected_without_evidence(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        (fixture.root / "outside.txt").write_text("not authorized\n", encoding="utf-8")
        target = fixture.commit("out of scope")
        before = fixture.issue_path().read_bytes()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PIPE-SCOPE", result.stderr)
        self.assertEqual(before, fixture.issue_path().read_bytes())
        self.assertEqual(list((fixture.root / "EVIDENCE").iterdir()), [])

    def intervening_fixture(self, **issue_keywords: Any) -> Tuple[PipelineRepository, str, str, str]:
        fixture = self.fixture()
        fixture.begin()
        base = fixture.git("rev-parse", "HEAD")
        fixture.write_intervening_issue(**issue_keywords)
        (fixture.root / "OTHER").mkdir(exist_ok=True)
        (fixture.root / "OTHER" / "amendment.md").write_text("separately authorized\n", encoding="utf-8")
        reviewed = fixture.commit("separately authorized intervening amendment")
        fixture.add_intervening_review(reviewed)
        tip = fixture.commit("intervening review persistence")
        return fixture, base, reviewed, tip

    @staticmethod
    def registry_entry(base: str, tip: str, issue: str = INTERVENING_ISSUE) -> Dict[str, str]:
        return {
            "issue": issue,
            "from": base,
            "to": tip,
            "recorded_utc": "2026-08-14T03:20:00Z",
            "recorded_by": "agent:coordinator",
        }

    def test_intervening_authority_excludes_verified_independent_range(self) -> None:
        fixture, base, _reviewed, tip = self.intervening_fixture()
        fixture.add_registry([self.registry_entry(base, tip)])
        target = fixture.make_target()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = fixture.state()
        self.assertEqual(state["state"], "AWAITING_PEER_REVIEW")
        evidence = json.loads((fixture.root / state["verification_evidence"][0]).read_text(encoding="utf-8"))
        exclusions = {item["path"]: item for item in evidence["scope_exclusions"]}
        self.assertEqual(sorted(exclusions), [INTERVENING_ISSUE, "OTHER/amendment.md"])
        for item in exclusions.values():
            self.assertEqual(item["covering_issues"], [INTERVENING_ISSUE])
            self.assertEqual(item["commit_count"], 1 if item["path"] == "OTHER/amendment.md" else 2)

    def test_intervening_self_entry_excludes_only_its_own_issue_file(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        base = fixture.git("rev-parse", "HEAD")
        fixture.write_intervening_issue(review="SELF")
        tip = fixture.commit("human authority record")
        fixture.add_registry([self.registry_entry(base, tip)])
        target = fixture.make_target()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 0, result.stderr)
        state = fixture.state()
        evidence = json.loads((fixture.root / state["verification_evidence"][0]).read_text(encoding="utf-8"))
        self.assertEqual([item["path"] for item in evidence["scope_exclusions"]], [INTERVENING_ISSUE])

    def test_intervening_self_entry_cannot_exclude_substantive_paths(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        base = fixture.git("rev-parse", "HEAD")
        fixture.write_intervening_issue(review="SELF")
        (fixture.root / "OTHER").mkdir()
        (fixture.root / "OTHER" / "smuggle.md").write_text("not reviewable\n", encoding="utf-8")
        tip = fixture.commit("self record with substantive change")
        fixture.add_registry([self.registry_entry(base, tip)])
        target = fixture.make_target()
        before = fixture.issue_path().read_bytes()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PIPE-SCOPE", result.stderr)
        self.assertIn("OTHER/smuggle.md", result.stderr)
        self.assertNotIn(INTERVENING_ISSUE, result.stderr)
        self.assertEqual(before, fixture.issue_path().read_bytes())
        self.assertEqual(list((fixture.root / "EVIDENCE").iterdir()), [])

    def test_intervening_authority_requires_human_authority_and_owner_decision(self) -> None:
        cases = (
            ("foreign_authority", {"authority": "AGENT"}),
            ("unsupported_review_class", {"review": "NONE"}),
            ("blocked_self_record", {"review": "SELF", "status": "BLOCKED"}),
            ("pending_unblock", {"review": "SELF", "unblock": "PENDING"}),
        )
        for name, keywords in cases:
            with self.subTest(case=name):
                fixture, base, _reviewed, tip = self.intervening_fixture(**keywords)
                fixture.add_registry([self.registry_entry(base, tip)])
                target = fixture.make_target()
                before = fixture.issue_path().read_bytes()
                result = fixture.submit(target)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("AEP-PIPE-SCOPE", result.stderr)
                self.assertEqual(before, fixture.issue_path().read_bytes())
                self.assertEqual(fixture.state()["state"], "IN_PROGRESS")

    def test_intervening_authority_fails_closed_on_unverified_ranges(self) -> None:
        def unregistered(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def no_registry(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def unapproved(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_intervening_review(reviewed, disposition="CHANGES_REQUIRED", material=1, utc="2026-08-14T03:26:00Z")
            new_tip = fixture.commit("adverse intervening review")
            fixture.add_registry([self.registry_entry(base, new_tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def open_findings(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_intervening_review(reviewed, material=1, utc="2026-08-14T03:26:00Z")
            new_tip = fixture.commit("findings intervening review")
            fixture.add_registry([self.registry_entry(base, new_tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def reviewer_is_implementor(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_intervening_review(reviewed, reviewer="agent:implementor", utc="2026-08-14T03:26:00Z")
            new_tip = fixture.commit("self-labelled intervening review")
            fixture.add_registry([self.registry_entry(base, new_tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def review_target_not_ancestor(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.git("checkout", "-b", "side")
            (fixture.root / "OTHER" / "side.md").write_text("side\n", encoding="utf-8")
            side = fixture.commit("side branch work")
            fixture.git("checkout", "main")
            fixture.add_intervening_review(side, utc="2026-08-14T03:26:00Z")
            new_tip = fixture.commit("review of non-ancestor target")
            fixture.add_registry([self.registry_entry(base, new_tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def post_review_substantive(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            (fixture.root / "OTHER" / "more.md").write_text("late\n", encoding="utf-8")
            new_tip = fixture.commit("post-review substantive change")
            fixture.add_registry([self.registry_entry(base, new_tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def overlapping_attribution(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([self.registry_entry(base, tip)])
            (fixture.root / "OTHER" / "amendment.md").write_text("attempt overwrote\n", encoding="utf-8")
            return fixture.commit("attempt touches intervening path"), 1, "AEP-PIPE-SCOPE"

        def swapped_range(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([self.registry_entry(tip, base)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def empty_range(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([self.registry_entry(tip, tip)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def tip_not_ancestor_of_target(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.git("checkout", "-b", "side")
            (fixture.root / "OTHER" / "side.md").write_text("side\n", encoding="utf-8")
            side = fixture.commit("side branch work")
            fixture.git("checkout", "main")
            fixture.add_registry([self.registry_entry(base, side)])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def non_issue_owner(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([self.registry_entry(base, tip, issue="work/milestone-1.txt")])
            return fixture.make_target(), 1, "AEP-PIPE-SCOPE"

        def missing_owner_issue(fixture: PipelineRepository, base: str, reviewed: str, tip: str) -> Tuple[str, int, str]:
            fixture.add_registry([self.registry_entry(base, tip, issue="ISSUES/ISSUE-20260814T030051Z-missing.md")])
            return fixture.make_target(), 2, "AEP-PIPE-IO"

        mutations = [
            unregistered, no_registry, unapproved, open_findings, reviewer_is_implementor,
            review_target_not_ancestor, post_review_substantive, overlapping_attribution,
            swapped_range, empty_range, tip_not_ancestor_of_target, non_issue_owner, missing_owner_issue,
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate.__name__):
                fixture, base, reviewed, tip = self.intervening_fixture()
                target, code, token = mutate(fixture, base, reviewed, tip)
                before = fixture.issue_path().read_bytes()
                result = fixture.submit(target)
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertIn(token, result.stderr)
                self.assertEqual(before, fixture.issue_path().read_bytes())
                self.assertEqual(fixture.state()["state"], "IN_PROGRESS")
                self.assertEqual(list((fixture.root / "EVIDENCE").iterdir()), [])

    def test_malformed_intervening_registry_fails_closed(self) -> None:
        def bad_schema(fixture: PipelineRepository, base: str, tip: str) -> None:
            fixture.add_registry([self.registry_entry(base, tip)], schema="aep-intervening-authority/v2")

        def entries_not_list(fixture: PipelineRepository, base: str, tip: str) -> None:
            fixture.add_registry({"issue": INTERVENING_ISSUE})

        def extra_entry_key(fixture: PipelineRepository, base: str, tip: str) -> None:
            entry = self.registry_entry(base, tip)
            entry["paths"] = ["OTHER/"]
            fixture.add_registry([entry])

        def missing_entry_key(fixture: PipelineRepository, base: str, tip: str) -> None:
            entry = self.registry_entry(base, tip)
            del entry["recorded_by"]
            fixture.add_registry([entry])

        def short_revision(fixture: PipelineRepository, base: str, tip: str) -> None:
            fixture.add_registry([self.registry_entry(base[:12], tip)])

        def bad_recorded_by(fixture: PipelineRepository, base: str, tip: str) -> None:
            entry = self.registry_entry(base, tip)
            entry["recorded_by"] = "not a label!!"
            fixture.add_registry([entry])

        def bad_recorded_utc(fixture: PipelineRepository, base: str, tip: str) -> None:
            entry = self.registry_entry(base, tip)
            entry["recorded_utc"] = "yesterday"
            fixture.add_registry([entry])

        mutations = [bad_schema, entries_not_list, extra_entry_key, missing_entry_key, short_revision, bad_recorded_by, bad_recorded_utc]
        for mutate in mutations:
            with self.subTest(mutation=mutate.__name__):
                fixture, base, _reviewed, tip = self.intervening_fixture()
                mutate(fixture, base, tip)
                target = fixture.make_target()
                before = fixture.issue_path().read_bytes()
                result = fixture.submit(target)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("AEP-PIPE-SCHEMA", result.stderr)
                self.assertEqual(before, fixture.issue_path().read_bytes())

    def test_failed_check_preserves_evidence_without_advancing(self) -> None:
        fixture = self.fixture(failing_check=True)
        fixture.begin()
        target = fixture.make_target()
        before = fixture.issue_path().read_bytes()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AEP-PIPE-VERIFY", result.stderr)
        self.assertEqual(before, fixture.issue_path().read_bytes())
        evidence_paths = list((fixture.root / "EVIDENCE").glob("*.json"))
        self.assertEqual(len(evidence_paths), 1)
        self.assertEqual(json.loads(evidence_paths[0].read_text(encoding="utf-8"))["result"], "FAIL")
        self.assertEqual(fixture.state()["state"], "IN_PROGRESS")

    def test_repository_mutations_fail_with_evidence_without_advancing(self) -> None:
        cases = (
            (
                "untracked",
                [sys.executable, "-c", "from pathlib import Path; Path('work/check-side-effect.txt').write_text('changed\\n')"],
                "worktree-clean",
            ),
            (
                "ignored",
                [sys.executable, "-c", "from pathlib import Path; Path('.DS_Store').write_text('ignored\\n')"],
                "worktree-clean",
            ),
            (
                "head",
                ["git", "commit", "--allow-empty", "-m", "accepted-check-side-effect"],
                "head-unchanged",
            ),
            (
                "authority bytes",
                [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; import subprocess; p=Path('PROJECT_SPEC.md'); p.write_text(p.read_text()+'\\n'); subprocess.run(['git','update-index','--skip-worktree','PROJECT_SPEC.md'],check=True)",
                ],
                "authority-source-unchanged",
            ),
            (
                "issue bytes",
                [],
                "issue-source-unchanged",
            ),
        )
        for label, argv, expected_failure in cases:
            with self.subTest(case=label):
                fixture = PipelineRepository()
                try:
                    if label == "ignored":
                        (fixture.root / ".gitignore").write_text(".DS_Store\n__pycache__/\n", encoding="utf-8")
                    if label == "issue bytes":
                        issue = fixture.milestones[0]["issue"]
                        argv = [
                            sys.executable,
                            "-c",
                            "from pathlib import Path; import subprocess; p=Path({!r}); p.write_text(p.read_text()+'\\n'); subprocess.run(['git','update-index','--skip-worktree',{!r}],check=True)".format(issue, issue),
                        ]
                    fixture.configure_check(argv)
                    fixture.begin()
                    target = fixture.make_target()
                    result = fixture.submit(target)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn("AEP-PIPE-VERIFY", result.stderr)
                    self.assertEqual(fixture.state()["state"], "IN_PROGRESS")
                    evidence = fixture.failure_evidence()
                    self.assertEqual(evidence["result"], "FAIL")
                    postconditions = {item["id"]: item["result"] for item in evidence["repository_postconditions"]}
                    self.assertEqual(postconditions[expected_failure], "FAIL")
                    self.assertEqual(
                        list(postconditions),
                        ["head-unchanged", "worktree-clean", "authority-source-unchanged", "issue-source-unchanged"],
                    )
                finally:
                    fixture.cleanup()

    def test_review_submission_refuses_preexisting_ignored_artifact(self) -> None:
        fixture = self.fixture()
        (fixture.root / ".gitignore").write_text(".DS_Store\n", encoding="utf-8")
        fixture.commit("ignore local metadata")
        fixture.begin()
        target = fixture.make_target()
        issue_before = fixture.issue_path().read_bytes()
        (fixture.root / ".DS_Store").write_text("preexisting ignored metadata\n", encoding="utf-8")
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("AEP-PIPE-GIT", result.stderr)
        self.assertIn(".DS_Store", result.stderr)
        self.assertEqual(issue_before, fixture.issue_path().read_bytes())
        self.assertEqual(list((fixture.root / "EVIDENCE").iterdir()), [])
        self.assertEqual(fixture.state()["state"], "IN_PROGRESS")

    def test_evidence_directory_must_be_an_owned_real_directory(self) -> None:
        for case in ("missing", "regular", "symlink"):
            with self.subTest(case=case):
                fixture = PipelineRepository()
                try:
                    evidence = fixture.root / "EVIDENCE"
                    evidence.rmdir()
                    outside = Path(fixture.temporary.name) / "outside evidence"
                    outside.mkdir()
                    if case == "regular":
                        evidence.write_text("not a directory\n", encoding="utf-8")
                    elif case == "symlink":
                        try:
                            evidence.symlink_to(outside, target_is_directory=True)
                        except OSError as error:
                            self.skipTest("symlinks unavailable: {}".format(error))
                    before = self.snapshot(fixture.root)
                    result = fixture.run("status")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("AEP-PIPE-", result.stderr)
                    self.assertEqual(before, self.snapshot(fixture.root))
                    self.assertEqual(list(outside.iterdir()), [])
                finally:
                    fixture.cleanup()

    def test_transition_time_evidence_symlink_is_rejected_before_write(self) -> None:
        fixture = self.fixture()
        outside = Path(fixture.temporary.name) / "outside transition evidence"
        outside.mkdir()
        command = (
            "from pathlib import Path; "
            "p=Path('EVIDENCE'); p.rmdir(); p.symlink_to(Path({!r}), target_is_directory=True)"
        ).format(str(outside))
        fixture.configure_check([sys.executable, "-c", command])
        fixture.begin()
        target = fixture.make_target()
        before_issue = fixture.issue_path().read_bytes()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("AEP-PIPE-SCOPE", result.stderr)
        self.assertEqual(before_issue, fixture.issue_path().read_bytes())
        self.assertEqual(fixture.state()["state"], "IN_PROGRESS")
        self.assertEqual(list(outside.iterdir()), [])

    def test_generated_issue_markdown_keeps_tables_and_headings_separated(self) -> None:
        fixture = self.fixture()
        issue = fixture.issue_path()
        text = issue.read_text(encoding="utf-8")
        text = text.replace(
            "|---|---|---|---|---|\n| `2026-08-14T03:00:00Z`",
            "|---|---|---|---|---|\n\n| `2026-08-14T03:00:00Z`",
        )
        issue.write_text(text, encoding="utf-8")
        fixture.commit("legacy split table")
        fixture.begin()
        target = fixture.make_target()
        result = fixture.submit(target)
        self.assertEqual(result.returncode, 0, result.stderr)
        updated = issue.read_text(encoding="utf-8")
        activity = updated.split("## Activity history\n", 1)[1].split("\n## Closure checklist", 1)[0]
        self.assertNotIn("\n\n|", activity)
        self.assertTrue(all(not line or line.startswith("|") for line in activity.splitlines()))
        self.assertIn("| `agent:implementor` | `IMPLEMENTING` | `REVIEW` |", activity)
        self.assertIn("\n\n## Closure checklist", updated)
        verification = updated.split("## Verification\n", 1)[1].split("\n## Pipeline state", 1)[0]
        self.assertIn("**Pipeline verification", verification)
        self.assertIn("\n\n## Pipeline state", updated)

    def test_unavailable_and_timed_out_checks_are_failures_with_evidence(self) -> None:
        cases = (
            (["aep-command-that-does-not-exist"], 10, "FileNotFoundError"),
            ([sys.executable, "-c", "import time; time.sleep(2)"], 1, None),
        )
        for argv, timeout, expected_stderr in cases:
            with self.subTest(argv=argv):
                fixture = PipelineRepository()
                try:
                    fixture.configure_check(argv, timeout)
                    fixture.begin()
                    target = fixture.make_target()
                    before = fixture.issue_path().read_bytes()
                    result = fixture.submit(target)
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(before, fixture.issue_path().read_bytes())
                    records = list((fixture.root / "EVIDENCE").glob("*.json"))
                    self.assertEqual(len(records), 1)
                    payload = json.loads(records[0].read_text(encoding="utf-8"))
                    self.assertEqual(payload["result"], "FAIL")
                    check = payload["checks"][0]
                    if expected_stderr is None:
                        self.assertTrue(check["timed_out"])
                    else:
                        self.assertIn(expected_stderr, check["stderr"])
                finally:
                    fixture.cleanup()

    def test_tampered_evidence_reference_fails_status(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        target = fixture.make_target()
        self.assertEqual(fixture.submit(target).returncode, 0)
        state = fixture.state()
        evidence = fixture.root / state["verification_evidence"][0]
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        payload["result"] = "FAIL"
        evidence.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        before = self.snapshot(fixture.root)
        status = fixture.run("status")
        self.assertEqual(status.returncode, 1)
        self.assertIn("AEP-PIPE-STATE", status.stderr)
        self.assertEqual(before, self.snapshot(fixture.root))

    def test_review_gate_rejects_identity_target_vocabulary_and_material_mismatch(self) -> None:
        cases: Sequence[Tuple[str, str, int, str, str]] = (
            ("same reviewer", "APPROVED", 0, "agent:implementor", "same"),
            ("wrong target", "APPROVED", 0, "agent:reviewer", "wrong"),
            ("informal", "APPROVED WITH FINDINGS", 0, "agent:reviewer", "same"),
            ("material approved", "APPROVED", 1, "agent:reviewer", "same"),
            ("blocked", "BLOCKED", 0, "agent:reviewer", "same"),
        )
        for label, disposition, material, reviewer, target_mode in cases:
            with self.subTest(case=label):
                fixture = PipelineRepository()
                try:
                    fixture.begin()
                    target = fixture.make_target()
                    self.assertEqual(fixture.submit(target).returncode, 0)
                    fixture.commit("handoff")
                    review_target = "0" * 40 if target_mode == "wrong" else target
                    fixture.add_review(review_target, disposition, material, reviewer=reviewer)
                    fixture.commit("review")
                    before = fixture.issue_path().read_bytes()
                    result = fixture.run(
                        "transition", "--milestone", fixture.milestones[0]["id"],
                        "--actor", "agent:coordinator", "--to", "ACCEPTED",
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("AEP-PIPE-REVIEW", result.stderr)
                    self.assertEqual(before, fixture.issue_path().read_bytes())
                finally:
                    fixture.cleanup()

    def test_unchecked_closure_prevents_acceptance(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        target = fixture.make_target()
        self.assertEqual(fixture.submit(target).returncode, 0)
        fixture.commit("handoff")
        fixture.add_review(target, "APPROVED", 0)
        path = fixture.issue_path()
        path.write_text(path.read_text(encoding="utf-8").replace("- [x] Change is recorded.", "- [ ] Change is recorded."), encoding="utf-8")
        fixture.commit("review incomplete closure")
        result = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "ACCEPTED",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("closure checklist", result.stderr)

    def test_post_target_implementation_drift_prevents_acceptance(self) -> None:
        fixture = self.fixture()
        fixture.begin()
        target = fixture.make_target()
        self.assertEqual(fixture.submit(target).returncode, 0)
        fixture.commit("handoff")
        fixture.add_review(target, "APPROVED", 0)
        (fixture.root / "work" / "milestone-1.txt").write_text("drift\n", encoding="utf-8")
        fixture.commit("unreviewed drift")
        result = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:coordinator", "--to", "ACCEPTED",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("implementation changed after reviewed target", result.stderr)

    def test_human_escalation_requires_durable_human_blocker(self) -> None:
        fixture = self.fixture()
        missing = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "BLOCKED_HUMAN_AUTHORITY",
            "--blocker-issue", "ISSUES/missing.md",
        )
        self.assertNotEqual(missing.returncode, 0)
        success = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "BLOCKED_HUMAN_AUTHORITY",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(fixture.state()["state"], "BLOCKED_HUMAN_AUTHORITY")
        self.assertIn("**Status:** `BLOCKED`", fixture.issue_path().read_text(encoding="utf-8"))

    def _enter_blocked(self, fixture: PipelineRepository) -> None:
        fixture.begin()
        fixture.commit("in progress")
        result = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "BLOCKED_HUMAN_AUTHORITY",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        fixture.commit("blocked")

    @staticmethod
    def _resolve_blocker(fixture: PipelineRepository) -> None:
        path = fixture.root / "ISSUES" / "ISSUE-20260814T030099Z-human-blocker.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("- **Status:** `BLOCKED`", "- **Status:** `OPEN`"), encoding="utf-8")
        fixture.commit("owner decision recorded")

    def test_blocked_resume_requires_recorded_owner_decision(self) -> None:
        fixture = self.fixture()
        self._enter_blocked(fixture)
        before = self.snapshot(fixture.root)
        unresolved = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(unresolved.returncode, 1)
        self.assertIn("AEP-PIPE-BLOCKER", unresolved.stderr)
        self.assertEqual(before, self.snapshot(fixture.root))
        self._resolve_blocker(fixture)
        resumed = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        state = fixture.state()
        self.assertEqual(state["state"], "IN_PROGRESS")
        self.assertEqual(state["attempt"], 1)
        self.assertEqual(state["implementor"], "agent:implementor")
        self.assertIn("ISSUE-20260814T030099Z-human-blocker.md", state["events"][-1]["reason"])
        text = fixture.issue_path().read_text(encoding="utf-8")
        self.assertIn("**Status:** `IMPLEMENTING`", text)
        self.assertIn("- **Blocked from:** `NOT BLOCKED`", text)
        self.assertIn("- **Unblock condition:** `NONE`", text)

    def test_blocked_resume_requires_entry_blocker_and_clean_tree(self) -> None:
        fixture = self.fixture()
        self._enter_blocked(fixture)
        self._resolve_blocker(fixture)
        missing_flag = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
        )
        self.assertEqual(missing_flag.returncode, 2)
        self.assertIn("AEP-PIPE-CLI", missing_flag.stderr)
        other = fixture.root / "ISSUES" / "ISSUE-20260814T030098Z-other.md"
        other.write_text(
            "# Other\n\n## Metadata\n\n- **Status:** `OPEN`\n- **Authority:** `HUMAN`\n\n"
            "## Blocker\n\n- **Unblock condition:** `Owner decided.`\n",
            encoding="utf-8",
        )
        fixture.commit("other resolved issue")
        mismatch = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030098Z-other.md",
        )
        self.assertEqual(mismatch.returncode, 1)
        self.assertIn("does not match the recorded entry blocker", mismatch.stderr)
        (fixture.root / "work" / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        dirty = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(dirty.returncode, 1)
        self.assertIn("AEP-PIPE-GIT", dirty.stderr)
        fixture.commit("clean again")
        resumed = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertEqual(fixture.state()["state"], "IN_PROGRESS")

    def test_blocker_flag_rejected_for_ordinary_in_progress(self) -> None:
        fixture = self.fixture()
        ready = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "READY",
        )
        self.assertEqual(ready.returncode, 0, ready.stderr)
        fixture.commit("ready")
        result = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "IN_PROGRESS",
            "--blocker-issue", "ISSUES/ISSUE-20260814T030099Z-human-blocker.md",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("AEP-PIPE-CLI", result.stderr)
        self.assertEqual(fixture.state()["state"], "READY")

    def test_blocked_resume_still_rejects_blocked_target_states(self) -> None:
        fixture = self.fixture()
        self._enter_blocked(fixture)
        self._resolve_blocker(fixture)
        for target in ("READY", "AWAITING_PEER_REVIEW", "ACCEPTED", "CHANGES_REQUIRED"):
            with self.subTest(target=target):
                before = self.snapshot(fixture.root)
                result = fixture.run(
                    "transition", "--milestone", fixture.milestones[0]["id"],
                    "--actor", "agent:implementor", "--to", target,
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("AEP-PIPE-STATE", result.stderr)
                self.assertEqual(before, self.snapshot(fixture.root))

    def test_issue_conflict_is_detected_before_atomic_replacement(self) -> None:
        fixture = self.fixture()
        context = pipeline._load_context(fixture.root)
        milestone = context.milestones[0]
        path = fixture.issue_path()
        concurrent = path.read_text(encoding="utf-8") + "\nConcurrent note.\n"
        path.write_text(concurrent, encoding="utf-8")
        with self.assertRaises(pipeline.PipelineError) as raised:
            pipeline._commit_issue(context, milestone, context.issue_texts[milestone.milestone_id])
        self.assertEqual(raised.exception.rule_id, "AEP-PIPE-CONFLICT")
        self.assertEqual(path.read_text(encoding="utf-8"), concurrent)

    def test_invalid_transition_and_invocation_do_not_mutate(self) -> None:
        fixture = self.fixture()
        before = self.snapshot(fixture.root)
        invalid = fixture.run(
            "transition", "--milestone", fixture.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "ACCEPTED",
        )
        self.assertEqual(invalid.returncode, 1)
        self.assertEqual(before, self.snapshot(fixture.root))
        invocation = subprocess.run(
            [sys.executable, str(PIPELINE), "transition"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        self.assertEqual(invocation.returncode, 2)
        self.assertIn("AEP-PIPE-CLI", invocation.stderr)


if __name__ == "__main__":
    unittest.main()
