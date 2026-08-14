import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any, Dict, List


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPOSITORY_ROOT / "scripts"
DISPATCH = SCRIPTS / "run_dispatch.py"
ROLE_CONTRACTS = REPOSITORY_ROOT / "ROLE_CONTRACTS.md"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_dispatch as dispatch  # noqa: E402
from test_run_pipeline import PipelineRepository  # noqa: E402


DECISION_KEYS = {
    "schema", "selected_milestone", "state", "issue", "authority_digest",
    "role", "role_contract", "host_adapter", "reason", "eligibility",
    "expected_records", "expected_commands",
}
TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
BLOCKER_ISSUE = "ISSUES/ISSUE-20260814T030099Z-human-blocker.md"


class DispatchRepository(PipelineRepository):
    def decide(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(DISPATCH)] + list(arguments) + ["--root", str(self.root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )

    def decision(self, index: int = 0) -> Dict[str, Any]:
        result = self.decide("--json")
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        return json.loads(result.stdout)

    def worktree_bytes(self) -> Dict[str, bytes]:
        snapshot: Dict[str, bytes] = {}
        for path in sorted(self.root.rglob("*")):
            if path.is_file() and ".git" not in path.relative_to(self.root).parts:
                snapshot[str(path.relative_to(self.root))] = path.read_bytes()
        return snapshot

    def advance_to_review(self, index: int = 0) -> str:
        self.begin(index=index)
        self.commit("in progress")
        target = self.make_target(index=index)
        result = self.submit(target, index=index)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
        self.commit("submission")
        return target

    def record_round(self, target: str, disposition: str, material: int, index: int = 0) -> None:
        self.add_review(target, disposition, material, index=index)
        self.commit("review round")


class DispatchRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DispatchRepository()

    def tearDown(self) -> None:
        self.repository.cleanup()

    def test_authorized_routes_to_implementer(self) -> None:
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "implementer")
        self.assertEqual(decision["state"], "AUTHORIZED")
        self.assertEqual(decision["role_contract"], "ROLE_CONTRACTS.md#implementer")
        self.assertEqual(len(decision["expected_commands"]), 1)
        self.assertIn("--to", decision["expected_commands"][0])
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "READY")

    def test_ready_routes_to_implementer(self) -> None:
        milestone_id = self.repository.milestones[0]["id"]
        result = self.repository.run("transition", "--milestone", milestone_id, "--actor", "agent:implementor", "--to", "READY")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.repository.commit("ready")
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "implementer")
        self.assertEqual(decision["state"], "READY")
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "IN_PROGRESS")
        self.assertIn("attempt 1", decision["reason"])

    def test_in_progress_routes_to_bound_implementer(self) -> None:
        self.repository.begin()
        self.repository.commit("in progress")
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "implementer")
        self.assertEqual(decision["state"], "IN_PROGRESS")
        self.assertTrue(any("agent:implementor" in item for item in decision["eligibility"]))
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "AWAITING_PEER_REVIEW")
        self.assertIn("--target", command)

    def test_awaiting_review_without_round_routes_to_reviewer(self) -> None:
        target = self.repository.advance_to_review()
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "independent-reviewer")
        self.assertEqual(decision["state"], "AWAITING_PEER_REVIEW")
        self.assertEqual(decision["expected_commands"], [])
        self.assertTrue(any("agent:implementor" in item and "differ" in item for item in decision["eligibility"]))
        self.assertTrue(any(target in item for item in decision["expected_records"]))

    def test_approved_round_routes_to_recorder(self) -> None:
        target = self.repository.advance_to_review()
        self.repository.record_round(target, "APPROVED", 0)
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "recorder")
        self.assertEqual(decision["role_contract"], "ROLE_CONTRACTS.md#recorder-and-coordinator")
        self.assertTrue(any("agent:implementor" in item and "agent:reviewer" in item for item in decision["eligibility"]))
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "ACCEPTED")

    def test_changes_required_round_routes_to_reviewer_completion(self) -> None:
        target = self.repository.advance_to_review()
        self.repository.record_round(target, "CHANGES_REQUIRED", 1)
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "independent-reviewer")
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "CHANGES_REQUIRED")

    def test_stale_round_routes_to_reviewer(self) -> None:
        self.repository.advance_to_review()
        self.repository.record_round("a" * 40, "APPROVED", 0)
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "independent-reviewer")
        self.assertIn("different revision", decision["reason"])
        self.assertEqual(decision["expected_commands"], [])

    def test_changes_required_state_routes_to_implementer(self) -> None:
        target = self.repository.advance_to_review()
        self.repository.record_round(target, "CHANGES_REQUIRED", 1)
        result = self.repository.run(
            "transition", "--milestone", self.repository.milestones[0]["id"],
            "--actor", "agent:reviewer", "--to", "CHANGES_REQUIRED",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.repository.commit("changes required")
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "implementer")
        self.assertEqual(decision["state"], "CHANGES_REQUIRED")
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "IN_PROGRESS")
        self.assertIn("attempt 2", decision["reason"])

    def test_blocked_state_routes_to_human_escalation(self) -> None:
        result = self.repository.run(
            "transition", "--milestone", self.repository.milestones[0]["id"],
            "--actor", "agent:implementor", "--to", "BLOCKED_HUMAN_AUTHORITY",
            "--blocker-issue", BLOCKER_ISSUE,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.repository.commit("blocked")
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "human-escalation")
        self.assertEqual(decision["state"], "BLOCKED_HUMAN_AUTHORITY")
        self.assertEqual(decision["role_contract"], "ROLE_CONTRACTS.md#human-escalation")
        self.assertTrue(any("human technical owner" in item for item in decision["eligibility"]))

    def test_blocked_review_disposition_routes_to_human_escalation(self) -> None:
        target = self.repository.advance_to_review()
        self.repository.record_round(target, "BLOCKED", 0)
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "human-escalation")
        command = decision["expected_commands"][0]
        self.assertEqual(command[command.index("--to") + 1], "BLOCKED_HUMAN_AUTHORITY")
        self.assertIn("--blocker-issue", command)

    def test_accepted_milestone_routes_to_terminal(self) -> None:
        target = self.repository.advance_to_review()
        self.repository.record_round(target, "APPROVED", 0)
        result = self.repository.run(
            "transition", "--milestone", self.repository.milestones[0]["id"],
            "--actor", "agent:recorder", "--to", "ACCEPTED",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.repository.commit("accepted")
        decision = self.repository.decision()
        self.assertEqual(decision["role"], "none")
        self.assertIsNone(decision["selected_milestone"])
        self.assertIsNone(decision["state"])
        self.assertIsNone(decision["role_contract"])
        self.assertIn("terminal wait state", decision["reason"])
        self.assertEqual(decision["expected_commands"], [])

    def test_selection_follows_dependency_order(self) -> None:
        repository = DispatchRepository(milestone_count=2)
        try:
            decision = repository.decision()
            self.assertEqual(decision["selected_milestone"], repository.milestones[0]["id"])
            self.assertEqual(decision["role"], "implementer")
        finally:
            repository.cleanup()


class DispatchOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DispatchRepository()

    def tearDown(self) -> None:
        self.repository.cleanup()

    def test_decision_shape_is_bounded(self) -> None:
        decision = self.repository.decision()
        self.assertEqual(set(decision), DECISION_KEYS)
        self.assertEqual(decision["schema"], "aep-dispatch-decision/v1")
        self.assertEqual(decision["host_adapter"], "manual")

    def test_output_is_byte_identical_for_identical_state(self) -> None:
        first_json = self.repository.decide("--json")
        second_json = self.repository.decide("--json")
        self.assertEqual(first_json.returncode, 0)
        self.assertEqual(first_json.stdout, second_json.stdout)
        first_text = self.repository.decide()
        second_text = self.repository.decide()
        self.assertEqual(first_text.stdout, second_text.stdout)

    def test_output_carries_no_timestamps(self) -> None:
        for arguments in ((), ("--json",)):
            result = self.repository.decide(*arguments)
            self.assertEqual(result.returncode, 0)
            self.assertIsNone(TIMESTAMP_RE.search(result.stdout))

    def test_dispatch_mutates_nothing(self) -> None:
        before = self.repository.worktree_bytes()
        status_before = self.repository.git("status", "--porcelain")
        result = self.repository.decide("--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.repository.worktree_bytes(), before)
        self.assertEqual(self.repository.git("status", "--porcelain"), status_before)

    def test_human_output_lists_role_and_contract(self) -> None:
        result = self.repository.decide()
        self.assertEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        self.assertEqual(lines[0], "ROLE implementer")
        self.assertTrue(any(line.startswith("ROLE_CONTRACT ROLE_CONTRACTS.md#") for line in lines))
        self.assertIn("EXPECTED_COMMANDS", lines)

    def test_invalid_root_is_an_error(self) -> None:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, str(DISPATCH), "--root", str(self.repository.root / "missing")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=environment,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertTrue(completed.stderr.startswith("ERROR AEP-PIPE-IO"))

    def test_role_contract_anchors_exist(self) -> None:
        headings = re.findall(r"^##+ (.+)$", ROLE_CONTRACTS.read_text(encoding="utf-8"), re.MULTILINE)
        slugs = {
            re.sub(r"[^\w\s-]", "", heading.strip().lower()).replace(" ", "-")
            for heading in headings
        }
        for anchor in dispatch.ROLE_ANCHORS.values():
            self.assertIn(anchor, slugs)


if __name__ == "__main__":
    unittest.main()
