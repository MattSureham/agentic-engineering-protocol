import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPOSITORY_ROOT / "scripts"
ROTATION = SCRIPTS / "run_rotation.py"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_rotation as rotation  # noqa: E402
from test_run_dispatch import DispatchRepository  # noqa: E402


def make_decision(
    role: str,
    state: Optional[str] = "AUTHORIZED",
    milestone: Optional[str] = "MILESTONE-20260814T099999Z-fixture",
    eligibility: Optional[List[str]] = None,
    commands: Optional[List[List[str]]] = None,
) -> Dict[str, Any]:
    return {
        "schema": "aep-dispatch-decision/v1",
        "selected_milestone": milestone,
        "state": state,
        "issue": "ISSUES/fixture.md" if milestone else None,
        "authority_digest": "d" * 64 if milestone else None,
        "role": role,
        "role_contract": "ROLE_CONTRACTS.md#{}".format(role) if role != "none" else None,
        "host_adapter": "manual",
        "reason": "fixture decision",
        "eligibility": eligibility if eligibility is not None else [],
        "expected_records": [],
        "expected_commands": commands if commands is not None else [],
    }


def envelope(subtype: str, is_error: bool, cost: float = 0.01, session: str = "sess-1", returncode: int = 0) -> rotation.LaunchResult:
    payload = {
        "type": "result",
        "subtype": subtype,
        "is_error": is_error,
        "session_id": session,
        "total_cost_usd": cost,
        "result": "OK" if not is_error else None,
    }
    return rotation.LaunchResult("completed", returncode, json.dumps(payload), "")


class RotationHarness:
    def __init__(self, participants: int = 3) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="aep rotation ")
        self.root = Path(self.temporary.name) / "rotation root"
        self.root.mkdir()
        labels = ["agent:p{}".format(index + 1) for index in range(participants)]
        self.registry = {
            "schema": rotation.REGISTRY_SCHEMA,
            "defaults": {
                "max_attempts_per_decision": 2,
                "max_steps": 8,
                "max_spend_usd": 5.0,
                "timeout_seconds": 5,
                "max_budget_usd": 0.25,
                "tools": "",
            },
            "participants": [{"label": label} for label in labels],
        }
        self.write_registry(self.registry)
        (self.root / rotation.LEDGER_PATH).write_text("", encoding="utf-8")
        self.decision = make_decision("none", state=None, milestone=None)
        self.script: List[Any] = []
        self.launches: List[str] = []
        self.prompts: List[str] = []
        self.report_lines: List[str] = []

    def cleanup(self) -> None:
        self.temporary.cleanup()

    def write_registry(self, registry: Dict[str, Any]) -> None:
        (self.root / rotation.REGISTRY_PATH).write_text(json.dumps(registry, indent=2), encoding="utf-8")

    def decide(self) -> Dict[str, Any]:
        return self.decision

    def launch(self, prompt: str, participant: Dict[str, Any], defaults: Dict[str, Any]) -> rotation.LaunchResult:
        self.launches.append(participant["label"])
        self.prompts.append(prompt)
        action = self.script.pop(0) if self.script else envelope("success", False)
        if callable(action):
            return action(prompt, participant)
        return action

    def run(self, overrides: Optional[Dict[str, Any]] = None) -> str:
        return rotation.run(
            self.root, decide=self.decide, launch=self.launch,
            overrides=overrides, reporter=self.report_lines.append,
        )

    def ledger(self) -> List[Dict[str, Any]]:
        return rotation.read_ledger(self.root)

    def ledger_lines(self) -> List[str]:
        return (self.root / rotation.LEDGER_PATH).read_text(encoding="utf-8").splitlines()

    def outcomes(self) -> List[str]:
        return [event["outcome"] for event in self.ledger() if event["event"] == "outcome"]

    def advance_to(self, decision: Dict[str, Any], result: Optional[rotation.LaunchResult] = None):
        def action(prompt: str, participant: Dict[str, Any]) -> rotation.LaunchResult:
            self.decision = decision
            return result if result is not None else envelope("success", False)
        return action


class RotationRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = RotationHarness()

    def tearDown(self) -> None:
        self.harness.cleanup()

    def test_terminal_decision_stops_without_launch(self) -> None:
        reason = self.harness.run()
        self.assertEqual(reason, "terminal_no_authorized_work")
        self.assertEqual(self.harness.launches, [])
        stop = self.harness.ledger()[-1]
        self.assertEqual(stop["event"], "stop")
        self.assertEqual(stop["outcome"], "terminal_no_authorized_work")

    def test_human_escalation_decision_stops_without_launch(self) -> None:
        self.harness.decision = make_decision("human-escalation", state="BLOCKED_HUMAN_AUTHORITY")
        reason = self.harness.run()
        self.assertEqual(reason, "human_authority_required")
        self.assertEqual(self.harness.launches, [])
        self.assertNotIn("BLOCKED", json.dumps(self.harness.outcomes()))

    def test_reviewer_independence_excludes_implementor(self) -> None:
        self.harness.decision = make_decision(
            "independent-reviewer", state="AWAITING_PEER_REVIEW",
            eligibility=[
                "The reviewer label must differ from the attempt implementor label agent:p1.",
                "The reviewer must be independent of the authorship of the change under review.",
            ],
        )
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        reason = self.harness.run()
        self.assertEqual(reason, "terminal_no_authorized_work")
        self.assertEqual(self.harness.launches, ["agent:p2"])

    def test_recorder_excludes_implementor_and_reviewer(self) -> None:
        self.harness.decision = make_decision(
            "recorder", state="AWAITING_PEER_REVIEW",
            eligibility=[
                "The recorder label must differ from the attempt implementor label agent:p1 and the approving reviewer label agent:p2.",
                "The recorder confirms acceptance preconditions from durable records and does not re-review or modify implementation.",
            ],
        )
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        self.harness.run()
        self.assertEqual(self.harness.launches, ["agent:p3"])

    def test_bound_implementor_label_is_the_only_candidate(self) -> None:
        self.harness.decision = make_decision(
            "implementer", state="IN_PROGRESS",
            eligibility=[
                "Attempt 1 is bound to implementor label agent:p3; that participant continues it.",
                "The implementer may not review or record acceptance of the same attempt.",
            ],
        )
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        self.harness.run()
        self.assertEqual(self.harness.launches, ["agent:p3"])

    def test_exhausted_pool_stops_without_escalation(self) -> None:
        harness = RotationHarness(participants=1)
        try:
            harness.decision = make_decision(
                "independent-reviewer", state="AWAITING_PEER_REVIEW",
                eligibility=["The reviewer label must differ from the attempt implementor label agent:p1."],
            )
            reason = harness.run()
            self.assertEqual(reason, "no_eligible_participant")
            self.assertEqual(harness.launches, [])
            stop = harness.ledger()[-1]
            self.assertEqual(stop["outcome"], "no_eligible_participant")
        finally:
            harness.cleanup()

    def test_unrecognized_constraint_fails_closed(self) -> None:
        self.harness.decision = make_decision(
            "independent-reviewer", state="AWAITING_PEER_REVIEW",
            eligibility=["The reviewer label must be approved by an operator."],
        )
        with self.assertRaises(rotation.RotationError):
            self.harness.run()
        self.assertEqual(self.harness.launches, [])

    def test_prompt_substitutes_participant_label(self) -> None:
        self.harness.decision = make_decision(
            "implementer", state="AUTHORIZED",
            eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
            commands=[["python3", "scripts/run_pipeline.py", "transition", "--milestone", "M", "--actor", "<participant-label>", "--to", "READY"]],
        )
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        self.harness.run()
        self.assertEqual(len(self.harness.prompts), 1)
        prompt = self.harness.prompts[0]
        self.assertIn("--actor agent:p1", prompt)
        self.assertNotIn("<participant-label>", prompt)
        self.assertIn("ROLE_CONTRACTS.md#implementer", prompt)


class RotationFailureTaxonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = RotationHarness()
        self.harness.decision = make_decision(
            "implementer", state="AUTHORIZED",
            eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
        )

    def tearDown(self) -> None:
        self.harness.cleanup()

    def _failure_then_advance(self, failure: rotation.LaunchResult) -> str:
        self.harness.script = [
            failure,
            self.harness.advance_to(make_decision("none", state=None, milestone=None)),
        ]
        return self.harness.run()

    def test_quota_exhaustion_is_a_participant_failure(self) -> None:
        reason = self._failure_then_advance(envelope("error_max_budget_usd", True, cost=0.002, returncode=1))
        self.assertEqual(reason, "terminal_no_authorized_work")
        self.assertEqual(self.harness.outcomes(), ["quota_exhausted", "success_advancing"])
        self.assertNotIn("BLOCKED", json.dumps(self.harness.ledger()))

    def test_unparseable_envelope_is_session_error(self) -> None:
        self._failure_then_advance(rotation.LaunchResult("completed", 0, "not json", ""))
        self.assertEqual(self.harness.outcomes()[0], "session_error")

    def test_unknown_error_subtype_fails_closed(self) -> None:
        self._failure_then_advance(envelope("error_during_execution", True, returncode=1))
        self.assertEqual(self.harness.outcomes()[0], "session_error")

    def test_spawn_failure_is_launch_failure(self) -> None:
        self._failure_then_advance(rotation.LaunchResult("spawn_error", None, "", "claude: command not found"))
        self.assertEqual(self.harness.outcomes()[0], "launch_failure")

    def test_timeout_is_timeout(self) -> None:
        self._failure_then_advance(rotation.LaunchResult("timeout", None, "", ""))
        self.assertEqual(self.harness.outcomes()[0], "timeout")

    def test_non_advancing_success_is_a_participant_failure(self) -> None:
        self._failure_then_advance(envelope("success", False))
        self.assertEqual(self.harness.outcomes()[0], "non_advancing")

    def test_retry_rotates_to_the_next_eligible_participant(self) -> None:
        self._failure_then_advance(envelope("success", False))
        self.assertEqual(self.harness.launches, ["agent:p1", "agent:p2"])
        launches = [event for event in self.harness.ledger() if event["event"] == "launch"]
        self.assertEqual([event["attempt"] for event in launches], [1, 2])
        self.assertEqual(launches[1]["detail"], "rotate")


class RotationBoundsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = RotationHarness()
        self.harness.decision = make_decision(
            "implementer", state="AUTHORIZED",
            eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
        )

    def tearDown(self) -> None:
        self.harness.cleanup()

    def test_attempts_exhausted_stops_and_is_durable_across_restart(self) -> None:
        self.harness.script = [envelope("success", False)]  # non-advancing
        reason = self.harness.run(overrides={"max_attempts_per_decision": 1})
        self.assertEqual(reason, "attempts_exhausted")
        self.assertEqual(len(self.harness.launches), 1)
        again = self.harness.run(overrides={"max_attempts_per_decision": 1})
        self.assertEqual(again, "attempts_exhausted")
        self.assertEqual(len(self.harness.launches), 1)

    def test_steps_bound_stops_even_when_advancing(self) -> None:
        self.harness.script = [
            self.harness.advance_to(make_decision(
                "implementer", state="READY",
                eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
            )),
        ]
        reason = self.harness.run(overrides={"max_steps": 1})
        self.assertEqual(reason, "steps_exhausted")
        self.assertEqual(len(self.harness.launches), 1)

    def test_spend_bound_stops_before_next_launch(self) -> None:
        self.harness.script = [
            self.harness.advance_to(
                make_decision(
                    "implementer", state="READY",
                    eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
                ),
                result=envelope("success", False, cost=0.02),
            ),
        ]
        reason = self.harness.run(overrides={"max_spend_usd": 0.005})
        self.assertEqual(reason, "spend_exhausted")
        self.assertEqual(len(self.harness.launches), 1)
        stop = self.harness.ledger()[-1]
        self.assertAlmostEqual(stop["cost_usd"], 0.02)


class RotationRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = RotationHarness()
        self.harness.decision = make_decision(
            "implementer", state="AUTHORIZED",
            eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
        )

    def tearDown(self) -> None:
        self.harness.cleanup()

    def _crash(self, advance: bool):
        def action(prompt: str, participant: Dict[str, Any]) -> rotation.LaunchResult:
            if advance:
                self.harness.decision = make_decision("none", state=None, milestone=None)
            raise KeyboardInterrupt()
        return action

    def test_recovery_records_advancement_without_duplicate_launch(self) -> None:
        self.harness.script = [self._crash(advance=True)]
        with self.assertRaises(KeyboardInterrupt):
            self.harness.run()
        self.assertEqual([e["event"] for e in self.harness.ledger()], ["launch"])
        reason = self.harness.run()
        self.assertEqual(reason, "terminal_no_authorized_work")
        events = self.harness.ledger()
        recovered = events[1]
        self.assertEqual(recovered["event"], "outcome")
        self.assertEqual(recovered["outcome"], "success_advancing")
        launches = [e for e in events if e["event"] == "launch"]
        self.assertEqual(len(launches), 1)

    def test_recovery_without_advancement_records_session_error_and_rotates(self) -> None:
        self.harness.script = [self._crash(advance=False)]
        with self.assertRaises(KeyboardInterrupt):
            self.harness.run()
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        reason = self.harness.run()
        self.assertEqual(reason, "terminal_no_authorized_work")
        self.assertEqual(self.harness.outcomes()[0], "session_error")
        self.assertEqual(self.harness.launches, ["agent:p1", "agent:p2"])
        attempts = [e["attempt"] for e in self.harness.ledger() if e["event"] == "launch"]
        self.assertEqual(attempts, [1, 2])

    def test_crash_resume_matches_failure_resume_sequence(self) -> None:
        terminal = make_decision("none", state=None, milestone=None)
        self.harness.script = [self._crash(advance=False)]
        with self.assertRaises(KeyboardInterrupt):
            self.harness.run()
        self.harness.script = [self.harness.advance_to(terminal)]
        self.harness.run()
        crashed_sequence = [
            (e.get("participant"), e.get("outcome"))
            for e in self.harness.ledger() if e["event"] in {"launch", "outcome"}
        ]

        clean = RotationHarness()
        try:
            clean.decision = make_decision(
                "implementer", state="AUTHORIZED",
                eligibility=["Use one valid participant label; it becomes the implementor label of attempt 1."],
            )
            clean.script = [
                rotation.LaunchResult("completed", 0, "garbage", ""),
                clean.advance_to(terminal),
            ]
            clean.run()
            clean_sequence = [
                (e.get("participant"), e.get("outcome"))
                for e in clean.ledger() if e["event"] in {"launch", "outcome"}
            ]
        finally:
            clean.cleanup()
        self.assertEqual(crashed_sequence, clean_sequence)

    def test_ledger_is_append_only_with_required_fields(self) -> None:
        self.harness.script = [self.harness.advance_to(make_decision("none", state=None, milestone=None))]
        self.harness.run()
        lines_after_first = self.harness.ledger_lines()
        self.harness.run()
        self.assertEqual(self.harness.ledger_lines()[: len(lines_after_first)], lines_after_first)
        outcome = next(e for e in self.harness.ledger() if e["event"] == "outcome")
        for field in ("participant", "session_id", "outcome", "cost_usd", "utc"):
            self.assertIn(field, outcome)
        self.assertEqual(outcome["session_id"], "sess-1")
        self.assertEqual(outcome["cost_usd"], 0.01)


class RotationRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = RotationHarness()

    def tearDown(self) -> None:
        self.harness.cleanup()

    def test_duplicate_labels_rejected(self) -> None:
        self.harness.registry["participants"].append({"label": "agent:p1"})
        self.harness.write_registry(self.harness.registry)
        with self.assertRaises(rotation.RotationError):
            self.harness.run()

    def test_wrong_schema_rejected(self) -> None:
        self.harness.registry["schema"] = "other/v9"
        self.harness.write_registry(self.harness.registry)
        with self.assertRaises(rotation.RotationError):
            self.harness.run()

    def test_empty_participants_rejected(self) -> None:
        self.harness.registry["participants"] = []
        self.harness.write_registry(self.harness.registry)
        with self.assertRaises(rotation.RotationError):
            self.harness.run()


class RotationCliTests(unittest.TestCase):
    def test_cli_consumes_the_real_dispatcher_and_stops_at_terminal(self) -> None:
        repository = DispatchRepository()
        try:
            target = repository.advance_to_review()
            repository.record_round(target, "APPROVED", 0)
            result = repository.run(
                "transition", "--milestone", repository.milestones[0]["id"],
                "--actor", "agent:recorder", "--to", "ACCEPTED",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            repository.commit("accepted")
            (repository.root / rotation.REGISTRY_PATH).write_text(
                (REPOSITORY_ROOT / rotation.REGISTRY_PATH).read_text(encoding="utf-8"), encoding="utf-8"
            )
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            completed = subprocess.run(
                [sys.executable, str(ROTATION), "--root", str(repository.root)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False, env=environment,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn("stop=terminal_no_authorized_work", completed.stdout)
            ledger = (repository.root / rotation.LEDGER_PATH).read_text(encoding="utf-8")
            self.assertIn('"terminal_no_authorized_work"', ledger)
            self.assertNotIn("claude -p", completed.stdout)
        finally:
            repository.cleanup()


if __name__ == "__main__":
    unittest.main()
