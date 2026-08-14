#!/usr/bin/env python3
"""Execute dispatcher decisions through the probe-verified host CLI launch interface.

The dispatcher (scripts/run_dispatch.py) is the sole routing authority. This
root-only runner consumes its machine-readable decision, selects an eligible
participant from the durable registry (ROTATION_PARTICIPANTS.json) after
independence filtering, launches it through the probed `claude -p` interface,
classifies the result envelope, and appends every step to the append-only
ledger (ROTATION_LOG.jsonl). Participant failures — launch failure, quota
exhaustion, timeout, session error, non-advancing completion — are operational
outcomes with bounded retry/rotation and never become BLOCKED_HUMAN_AUTHORITY
transitions. The runner executes no pipeline transitions itself: launched
participants receive the dispatcher-emitted commands with their own label
substituted. Recovery re-reads the dispatcher and reconciles against the
ledger; pipeline state remains authoritative.
"""

import argparse
import datetime as dt
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from run_pipeline import ACTOR_RE, PipelineError


REGISTRY_SCHEMA = "rotation-participants/v1"
LEDGER_SCHEMA = "rotation-log/v1"
REGISTRY_PATH = "ROTATION_PARTICIPANTS.json"
LEDGER_PATH = "ROTATION_LOG.jsonl"

OUTCOMES = {
    "success_advancing", "launch_failure", "quota_exhausted",
    "session_error", "timeout", "non_advancing",
}
STOP_REASONS = {
    "terminal_no_authorized_work", "human_authority_required",
    "no_eligible_participant", "attempts_exhausted", "steps_exhausted",
    "spend_exhausted",
}

DEFAULTS_KEYS = {
    "max_attempts_per_decision", "max_steps", "max_spend_usd",
    "timeout_seconds", "max_budget_usd", "tools",
}
PARTICIPANT_KEYS = {"label", "max_budget_usd", "tools"}

BOUND_IMPLEMENTOR_RE = re.compile(
    r"^Attempt \d+ is bound to implementor label (?P<label>\S+); that participant continues it\.$"
)
REVIEWER_EXCLUDE_RE = re.compile(
    r"^The reviewer label must differ from the attempt implementor label (?P<label>\S+)\.$"
)
RECORDER_EXCLUDE_RE = re.compile(
    r"^The recorder label must differ from the attempt implementor label (?P<implementor>\S+) "
    r"and the approving reviewer label (?P<reviewer>\S+)\.$"
)
INFORMATIONAL_CONSTRAINTS = {
    "The implementer may not review or record acceptance of the same attempt.",
    "The reviewer must be independent of the authorship of the change under review.",
    "The recorder confirms acceptance preconditions from durable records and does not re-review or modify implementation.",
}
IMPLEMENTER_LABEL_RE = re.compile(
    r"^Use one valid participant label; it becomes the implementor label of attempt \d+\.$"
)


class RotationError(Exception):
    def __init__(self, rule_id: str, path: str, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.rule_id = rule_id
        self.path = path
        self.message = message
        self.exit_code = exit_code

    def render(self) -> str:
        return "ERROR {} {}: {}".format(self.rule_id, self.path, self.message)


class LaunchResult:
    def __init__(self, kind: str, returncode: Optional[int], stdout: str, stderr: str) -> None:
        self.kind = kind  # "completed", "spawn_error", or "timeout"
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_line(event: Dict[str, Any]) -> str:
    return json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def load_registry(root: Path) -> Dict[str, Any]:
    path = root / REGISTRY_PATH
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        raise RotationError("AEP-ROTATE-IO", REGISTRY_PATH, "registry is unavailable: {}".format(error))
    try:
        registry = json.loads(raw)
    except ValueError as error:
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "registry is not valid JSON: {}".format(error))
    if not isinstance(registry, dict) or registry.get("schema") != REGISTRY_SCHEMA:
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "registry schema must be {}".format(REGISTRY_SCHEMA))
    defaults = registry.get("defaults")
    if not isinstance(defaults, dict) or set(defaults) != DEFAULTS_KEYS:
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "registry defaults must contain exactly the declared bound keys")
    for key in ("max_attempts_per_decision", "max_steps", "timeout_seconds"):
        if not isinstance(defaults[key], int) or defaults[key] < 1:
            raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "default {} must be a positive integer".format(key))
    for key in ("max_spend_usd", "max_budget_usd"):
        if not isinstance(defaults[key], (int, float)) or isinstance(defaults[key], bool) or defaults[key] <= 0:
            raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "default {} must be a positive number".format(key))
    if not isinstance(defaults["tools"], str):
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "default tools must be a string")
    participants = registry.get("participants")
    if not isinstance(participants, list) or not participants:
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "registry must declare at least one participant")
    labels: List[str] = []
    for entry in participants:
        if not isinstance(entry, dict) or not set(entry) <= PARTICIPANT_KEYS or "label" not in entry:
            raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "each participant must declare a label and only known launch keys")
        label = entry["label"]
        if not isinstance(label, str) or ACTOR_RE.fullmatch(label) is None:
            raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "participant label {!r} is not a valid participant label".format(label))
        labels.append(label)
        for key in ("max_budget_usd",):
            if key in entry and (not isinstance(entry[key], (int, float)) or isinstance(entry[key], bool) or entry[key] <= 0):
                raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "participant {} must be a positive number".format(key))
        if "tools" in entry and not isinstance(entry["tools"], str):
            raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "participant tools must be a string")
    if len(set(labels)) != len(labels):
        raise RotationError("AEP-ROTATE-SCHEMA", REGISTRY_PATH, "participant labels must be unique")
    return registry


def read_ledger(root: Path) -> List[Dict[str, Any]]:
    path = root / LEDGER_PATH
    if not path.exists():
        return []
    events: List[Dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as error:
            raise RotationError("AEP-ROTATE-SCHEMA", LEDGER_PATH, "ledger line {} is not valid JSON: {}".format(number, error))
        if not isinstance(event, dict) or event.get("schema") != LEDGER_SCHEMA or event.get("event") not in {"launch", "outcome", "stop"}:
            raise RotationError("AEP-ROTATE-SCHEMA", LEDGER_PATH, "ledger line {} is not a recognized rotation event".format(number))
        events.append(event)
    return events


def append_ledger(root: Path, event: Dict[str, Any]) -> None:
    record = {"schema": LEDGER_SCHEMA, "utc": _utc_now()}
    record.update(event)
    with (root / LEDGER_PATH).open("a", encoding="utf-8") as stream:
        stream.write(_canonical_line(record))


def decision_key(decision: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], str]:
    return (decision.get("selected_milestone"), decision.get("state"), str(decision.get("role")))


def default_decide(root: Path) -> Dict[str, Any]:
    script = Path(__file__).resolve().parent / "run_dispatch.py"
    result = subprocess.run(
        [sys.executable, str(script), "--json", "--root", str(root)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False, timeout=60,
    )
    if result.returncode != 0:
        raise RotationError("AEP-ROTATE-DISPATCH", "scripts/run_dispatch.py", "dispatcher failed: {}".format(result.stderr.strip()))
    try:
        decision = json.loads(result.stdout)
    except ValueError as error:
        raise RotationError("AEP-ROTATE-DISPATCH", "scripts/run_dispatch.py", "dispatcher output is not valid JSON: {}".format(error))
    if not isinstance(decision, dict) or decision.get("schema") != "aep-dispatch-decision/v1":
        raise RotationError("AEP-ROTATE-DISPATCH", "scripts/run_dispatch.py", "dispatcher output is not a recognized decision")
    return decision


def default_launch(prompt: str, participant: Dict[str, Any], defaults: Dict[str, Any]) -> LaunchResult:
    budget = participant.get("max_budget_usd", defaults["max_budget_usd"])
    tools = participant.get("tools", defaults["tools"])
    command = [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--tools", tools,
        "--max-budget-usd", str(budget),
    ]
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            check=False, timeout=defaults["timeout_seconds"],
        )
    except subprocess.TimeoutExpired as error:
        return LaunchResult("timeout", None, error.stdout or "", error.stderr or "")
    except OSError as error:
        return LaunchResult("spawn_error", None, "", str(error))
    return LaunchResult("completed", result.returncode, result.stdout, result.stderr)


def parse_constraints(decision: Dict[str, Any]) -> Tuple[Optional[str], List[str]]:
    """Interpret the dispatcher's emitted eligibility strings; fail closed on anything unrecognized."""
    only_label: Optional[str] = None
    excluded: List[str] = []
    constraints = decision.get("eligibility")
    if not isinstance(constraints, list) or not all(isinstance(item, str) for item in constraints):
        raise RotationError("AEP-ROTATE-DECISION", "dispatcher decision", "eligibility constraints are not a string list")
    for constraint in constraints:
        bound = BOUND_IMPLEMENTOR_RE.fullmatch(constraint)
        if bound is not None:
            only_label = bound.group("label")
            continue
        reviewer = REVIEWER_EXCLUDE_RE.fullmatch(constraint)
        if reviewer is not None:
            excluded.append(reviewer.group("label"))
            continue
        recorder = RECORDER_EXCLUDE_RE.fullmatch(constraint)
        if recorder is not None:
            excluded.extend([recorder.group("implementor"), recorder.group("reviewer")])
            continue
        if constraint in INFORMATIONAL_CONSTRAINTS or IMPLEMENTER_LABEL_RE.fullmatch(constraint) is not None:
            continue
        raise RotationError("AEP-ROTATE-DECISION", "dispatcher decision", "unrecognized eligibility constraint: {}".format(constraint))
    return only_label, excluded


def select_participant(
    registry: Dict[str, Any], only_label: Optional[str], excluded: Sequence[str],
) -> List[Dict[str, Any]]:
    eligible = []
    for entry in registry["participants"]:
        if only_label is not None and entry["label"] != only_label:
            continue
        if entry["label"] in excluded:
            continue
        eligible.append(entry)
    return eligible


def build_prompt(decision: Dict[str, Any], participant_label: str) -> str:
    substituted_decision = json.loads(json.dumps(decision))
    substituted_decision["expected_commands"] = [
        [participant_label if part == "<participant-label>" else part for part in command]
        for command in decision.get("expected_commands") or []
    ]
    lines = [
        "You are participant {} in the agentic-engineering-protocol repository.".format(participant_label),
        "Read BOOTSTRAP.md first, then the {} section of ROLE_CONTRACTS.md, then HANDOFF.md and the owning issue.".format(decision.get("role_contract") or "role"),
        "Recover state only from Git and authoritative repository artifacts; do not rely on conversational memory.",
        "The accepted dispatcher emitted exactly this decision, with your label substituted for every placeholder:",
        json.dumps(substituted_decision, ensure_ascii=False, sort_keys=True, indent=2),
        "Perform exactly the emitted role and no other. The dispatcher-emitted commands with your label substituted are:",
    ]
    lines.extend(
        "- {}".format(shlex.join(command)) for command in substituted_decision["expected_commands"] or [["(none)"]]
    )
    lines.extend([
        "Produce the expected durable records, run the emitted pipeline transition commands exactly as substituted, and commit record changes.",
        "Do not perform another participant's role, do not review or accept your own attempt, and do not request routine human approval for already-authorized work.",
        "If existing repository authority is insufficient, stop and record the exact missing authority instead of improvising scope.",
    ])
    return "\n".join(lines) + "\n"


def classify(result: LaunchResult) -> Tuple[str, Optional[str], Optional[float]]:
    """Classify a launch into the probed outcome taxonomy; unrecognized shapes fail closed."""
    if result.kind == "timeout":
        return "timeout", None, None
    if result.kind == "spawn_error":
        return "launch_failure", None, None
    try:
        envelope = json.loads(result.stdout)
    except ValueError:
        return "session_error", None, None
    if not isinstance(envelope, dict) or envelope.get("type") != "result":
        return "session_error", None, None
    subtype = envelope.get("subtype")
    is_error = envelope.get("is_error")
    session_id = envelope.get("session_id")
    cost = envelope.get("total_cost_usd")
    if not isinstance(subtype, str) or not isinstance(is_error, bool):
        return "session_error", None, None
    if session_id is not None and not isinstance(session_id, str):
        return "session_error", None, None
    if cost is not None and (not isinstance(cost, (int, float)) or isinstance(cost, bool)):
        return "session_error", None, None
    if subtype == "error_max_budget_usd" and is_error:
        return "quota_exhausted", session_id, cost
    if subtype == "success" and not is_error and result.returncode == 0:
        return "success", session_id, cost
    return "session_error", session_id, cost


def _pending_launch(events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    pending: Optional[Dict[str, Any]] = None
    for event in events:
        if event["event"] == "launch":
            pending = event
        elif event["event"] == "outcome":
            pending = None
    return pending


def _attempts_used(events: List[Dict[str, Any]], key: Tuple[Optional[str], Optional[str], str]) -> int:
    return sum(
        1 for event in events
        if event["event"] == "launch" and (event.get("milestone"), event.get("state"), event.get("role")) == key
    )


def run(
    root: Path,
    decide: Optional[Callable[[], Dict[str, Any]]] = None,
    launch: Optional[Callable[[str, Dict[str, Any], Dict[str, Any]], LaunchResult]] = None,
    overrides: Optional[Dict[str, Any]] = None,
    reporter: Optional[Callable[[str], None]] = None,
) -> str:
    """Run bounded rotation; return the stop reason. All stops are clean; failures raise RotationError."""
    decide = decide or (lambda: default_decide(root))
    launch = launch or (lambda prompt, participant, defaults: default_launch(prompt, participant, defaults))
    report = reporter or (lambda line: print(line))
    registry = load_registry(root)
    defaults = dict(registry["defaults"])
    for key, value in (overrides or {}).items():
        if value is not None:
            defaults[key] = value
    events = read_ledger(root)

    pending = _pending_launch(events)
    if pending is not None:
        current = decide()
        recovered_key = (pending.get("milestone"), pending.get("state"), pending.get("role"))
        if decision_key(current) != recovered_key:
            append_ledger(root, {
                "event": "outcome", "milestone": pending.get("milestone"), "state": pending.get("state"),
                "role": pending.get("role"), "participant": pending.get("participant"),
                "attempt": pending.get("attempt"), "session_id": pending.get("session_id"),
                "outcome": "success_advancing", "cost_usd": None,
                "detail": "recovered: expected advancement landed before interruption",
            })
            report("RECOVER participant={} outcome=success_advancing".format(pending.get("participant")))
        else:
            append_ledger(root, {
                "event": "outcome", "milestone": pending.get("milestone"), "state": pending.get("state"),
                "role": pending.get("role"), "participant": pending.get("participant"),
                "attempt": pending.get("attempt"), "session_id": pending.get("session_id"),
                "outcome": "session_error", "cost_usd": None,
                "detail": "recovered: interruption left no recorded outcome and no advancement",
            })
            report("RECOVER participant={} outcome=session_error".format(pending.get("participant")))
        events = read_ledger(root)

    steps = 0
    spend = 0.0
    while True:
        decision = decide()
        role = str(decision.get("role"))
        key = decision_key(decision)
        if role == "none":
            reason = "terminal_no_authorized_work"
        elif role == "human-escalation":
            reason = "human_authority_required"
        elif role not in {"implementer", "independent-reviewer", "recorder"}:
            raise RotationError("AEP-ROTATE-DECISION", "dispatcher decision", "unrecognized role {!r}".format(role))
        else:
            reason = ""
        if not reason:
            only_label, excluded = parse_constraints(decision)
            eligible = select_participant(registry, only_label, excluded)
            if not eligible:
                reason = "no_eligible_participant"
            else:
                attempts = _attempts_used(events, key)
                if attempts >= defaults["max_attempts_per_decision"]:
                    reason = "attempts_exhausted"
                elif steps >= defaults["max_steps"]:
                    reason = "steps_exhausted"
                elif spend >= defaults["max_spend_usd"]:
                    reason = "spend_exhausted"
        if reason:
            append_ledger(root, {
                "event": "stop", "milestone": key[0], "state": key[1], "role": key[2],
                "participant": None, "attempt": None, "session_id": None,
                "outcome": reason, "cost_usd": round(spend, 6),
                "detail": "steps={} spend_usd={:.6f}".format(steps, spend),
            })
            report("STOP {} steps={} spend_usd={:.6f}".format(reason, steps, spend))
            return reason

        participant = eligible[attempts % len(eligible)]
        prompt = build_prompt(decision, participant["label"])
        append_ledger(root, {
            "event": "launch", "milestone": key[0], "state": key[1], "role": key[2],
            "participant": participant["label"], "attempt": attempts + 1, "session_id": None,
            "outcome": None, "cost_usd": None,
            "detail": "retry" if attempts and participant["label"] == eligible[(attempts - 1) % len(eligible)]["label"] else ("rotate" if attempts else "initial"),
        })
        events = read_ledger(root)
        result = launch(prompt, participant, defaults)
        outcome, session_id, cost = classify(result)
        if outcome == "success":
            advanced = decision_key(decide()) != key
            outcome = "success_advancing" if advanced else "non_advancing"
        append_ledger(root, {
            "event": "outcome", "milestone": key[0], "state": key[1], "role": key[2],
            "participant": participant["label"], "attempt": attempts + 1,
            "session_id": session_id, "outcome": outcome, "cost_usd": cost,
            "detail": "classified from probed envelope taxonomy",
        })
        events = read_ledger(root)
        steps += 1
        spend += cost or 0.0
        report("STEP {} role={} participant={} outcome={} cost_usd={}".format(steps, key[2], participant["label"], outcome, cost))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute dispatcher decisions through the probe-verified host CLI launch interface (bounded, ledgered).",
    )
    parser.add_argument("--root", default=None, help="repository root (default: parent of this script)")
    parser.add_argument("--max-steps", type=int, default=None, help="override the registry default step bound")
    parser.add_argument("--max-attempts", type=int, default=None, help="override the registry default per-decision attempt bound")
    parser.add_argument("--max-spend-usd", type=float, default=None, help="override the registry default per-invocation spend bound")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _build_parser().parse_args(argv)
    root = Path(arguments.root) if arguments.root is not None else Path(__file__).resolve().parent.parent
    overrides = {
        "max_steps": arguments.max_steps,
        "max_attempts_per_decision": arguments.max_attempts,
        "max_spend_usd": arguments.max_spend_usd,
    }
    try:
        reason = run(root, overrides=overrides)
    except RotationError as error:
        print(error.render(), file=sys.stderr)
        print("SUMMARY launched=0 errors=1", file=sys.stderr)
        return error.exit_code
    except PipelineError as error:
        print(error.render(), file=sys.stderr)
        print("SUMMARY launched=0 errors=1", file=sys.stderr)
        return error.exit_code
    except Exception as error:  # Defensive boundary: do not expose an unstable traceback as API.
        print("ERROR AEP-ROTATE-INTERNAL command: {}: {}".format(type(error).__name__, error), file=sys.stderr)
        print("SUMMARY launched=0 errors=1", file=sys.stderr)
        return 2
    print("SUMMARY stop={} errors=0".format(reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
