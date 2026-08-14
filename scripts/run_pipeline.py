#!/usr/bin/env python3
"""Advance specification-authorized milestones through deterministic gates.

PROJECT_SPEC.md and accepted ADRs remain authoritative. This root-only helper
validates a narrow operational projection stored in an issue; it never creates
scope, performs review, commits, pushes, uses the network, or invokes agents.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from validate_protocol import validate_repository


CONTRACT_BEGIN = "<!-- AEP-AUTHORIZED-MILESTONES-V1:BEGIN -->"
CONTRACT_END = "<!-- AEP-AUTHORIZED-MILESTONES-V1:END -->"
STATE_BEGIN = "<!-- AEP-PIPELINE-STATE-V1:BEGIN -->"
STATE_END = "<!-- AEP-PIPELINE-STATE-V1:END -->"
CONTRACT_SCHEMA = "aep-authorized-milestones/v1"
STATE_SCHEMA = "aep-pipeline-state/v1"
STATUS_SCHEMA = "aep-pipeline-status/v1"
EVIDENCE_SCHEMA = "aep-pipeline-verification/v1"

CONTRACT_KEYS = {"schema", "milestones"}
MILESTONE_KEYS = {
    "id", "order", "title", "issue", "depends_on", "scope",
    "allowed_paths", "acceptance_checks", "review",
}
CHECK_KEYS = {"id", "argv", "timeout_seconds"}
STATE_KEYS = {
    "schema", "milestone_id", "authority_digest", "state", "attempt",
    "implementor", "base_revision", "target_revision",
    "verification_evidence", "review_references", "events",
}
EVENT_KEYS = {"sequence", "utc", "actor", "from", "to", "reason"}

STATES = {
    "AUTHORIZED", "READY", "IN_PROGRESS", "AWAITING_PEER_REVIEW",
    "CHANGES_REQUIRED", "ACCEPTED", "BLOCKED_HUMAN_AUTHORITY",
}
TRANSITIONS = {
    ("AUTHORIZED", "READY"),
    ("READY", "IN_PROGRESS"),
    ("IN_PROGRESS", "AWAITING_PEER_REVIEW"),
    ("AWAITING_PEER_REVIEW", "CHANGES_REQUIRED"),
    ("CHANGES_REQUIRED", "IN_PROGRESS"),
    ("AWAITING_PEER_REVIEW", "ACCEPTED"),
}
ISSUE_STATUS = {
    "AUTHORIZED": "INVESTIGATING",
    "READY": "INVESTIGATING",
    "IN_PROGRESS": "IMPLEMENTING",
    "AWAITING_PEER_REVIEW": "REVIEW",
    "CHANGES_REQUIRED": "IMPLEMENTING",
    "ACCEPTED": "CLOSED",
    "BLOCKED_HUMAN_AUTHORITY": "BLOCKED",
}
DISPOSITIONS = {"APPROVED", "CHANGES_REQUIRED", "BLOCKED"}
FULL_REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ACTOR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9:._/@+-]{0,127}$")
METADATA_RE = re.compile(r"^- \*\*(?P<key>[^*]+):\*\*\s+`?(?P<value>[^`\n]+)`?\s*$", re.MULTILINE)
REVIEW_HEADING_RE = re.compile(r"^### (?P<utc>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z) — (?P<reviewer>\S.*?)\s*$", re.MULTILINE)


class PipelineError(Exception):
    def __init__(self, rule_id: str, path: str, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.rule_id = rule_id
        self.path = path
        self.message = message
        self.exit_code = exit_code

    def render(self) -> str:
        return "ERROR {} {}: {}".format(self.rule_id, self.path, self.message)


class DuplicateJSONKey(ValueError):
    pass


@dataclass(frozen=True)
class Milestone:
    raw: Mapping[str, Any]
    digest: str

    @property
    def milestone_id(self) -> str:
        return str(self.raw["id"])

    @property
    def issue(self) -> str:
        return str(self.raw["issue"])


@dataclass
class Context:
    root: Path
    milestones: List[Milestone]
    states: Dict[str, Dict[str, Any]]
    issue_texts: Dict[str, str]


@dataclass(frozen=True)
class ReviewRound:
    utc: str
    reviewer: str
    target: str
    material_findings: int
    disposition: str

    @property
    def reference_fragment(self) -> str:
        heading = "{} — {}".format(self.utc, self.reviewer).lower()
        return re.sub(r"[^a-z0-9 _-]", "", heading).replace(" ", "-")


class StableArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print("ERROR AEP-PIPE-CLI command: {}".format(message), file=sys.stderr)
        print("SUMMARY advanced=0 errors=1", file=sys.stderr)
        raise SystemExit(2)


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return result or "milestone"


def _pairs_no_duplicates(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey("duplicate JSON key {!r}".format(key))
        result[key] = value
    return result


def _json_load(text: str, path: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_pairs_no_duplicates)
    except (json.JSONDecodeError, DuplicateJSONKey) as error:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "invalid JSON: {}".format(error), 2)


def _extract_json_block(text: str, begin: str, end: str, path: str) -> Any:
    begin_count = text.count(begin)
    end_count = text.count(end)
    if begin_count != 1 or end_count != 1:
        raise PipelineError(
            "AEP-PIPE-SCHEMA", path,
            "expected exactly one marker pair; found begin={} end={}".format(begin_count, end_count),
            2,
        )
    start = text.index(begin) + len(begin)
    finish = text.index(end)
    if finish <= start:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "marker order is invalid", 2)
    body = text[start:finish]
    match = re.fullmatch(r"\s*```json\n(?P<json>.*)\n```\s*", body, re.DOTALL)
    if match is None:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "marked content must be one fenced json block", 2)
    return _json_load(match.group("json"), path)


def _read_text(path: Path, display: str) -> str:
    if path.is_symlink() or not path.is_file():
        raise PipelineError("AEP-PIPE-IO", display, "expected a regular non-symlink file", 2)
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise PipelineError("AEP-PIPE-IO", display, "cannot read UTF-8 text: {}".format(error), 2)


def _metadata(text: str, path: str) -> Dict[str, str]:
    heading = text.find("## Metadata")
    next_heading = "\n## "
    heading_length = len("## Metadata")
    if heading < 0:
        heading = text.find("# Specification status")
        next_heading = "\n# "
        heading_length = len("# Specification status")
    if heading < 0:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "metadata/status section is missing", 2)
    finish = text.find(next_heading, heading + heading_length)
    section = text[heading:] if finish < 0 else text[heading:finish]
    result: Dict[str, str] = {}
    for match in METADATA_RE.finditer(section):
        key = match.group("key")
        if key in result:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "duplicate metadata field {!r}".format(key), 2)
        result[key] = match.group("value").strip()
    return result


def _require_keys(value: Any, expected: Iterable[str], path: str, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise PipelineError("AEP-PIPE-SCHEMA", path, "{} must be a JSON object".format(label), 2)
    found = set(value)
    wanted = set(expected)
    if found != wanted:
        raise PipelineError(
            "AEP-PIPE-SCHEMA", path,
            "{} keys differ: missing={} unexpected={}".format(
                label, sorted(wanted - found), sorted(found - wanted)
            ), 2,
        )
    return value


def _require_string(value: Any, path: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PipelineError("AEP-PIPE-SCHEMA", path, "{} must be a nonempty string".format(label), 2)
    return value


def _require_string_list(value: Any, path: str, label: str, allow_empty: bool = True) -> List[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise PipelineError("AEP-PIPE-SCHEMA", path, "{} must be {}string array".format(label, "a nonempty " if not allow_empty else "a "), 2)
    for item in value:
        _require_string(item, path, label + " item")
    if len(set(value)) != len(value):
        raise PipelineError("AEP-PIPE-SCHEMA", path, "{} contains duplicate values".format(label), 2)
    return value


def _safe_relative(value: str, path: str, label: str, allow_directory: bool = False) -> str:
    _require_string(value, path, label)
    if (
        "\\" in value or value.startswith("/") or value.startswith("./")
        or "//" in value or "\x00" in value or re.match(r"^[A-Za-z]:", value)
        or any(ord(character) < 32 for character in value)
    ):
        raise PipelineError("AEP-PIPE-SCOPE", path, "{} is not a portable relative path: {!r}".format(label, value), 2)
    directory = value.endswith("/")
    if directory:
        value_for_parts = value[:-1]
        if not allow_directory:
            raise PipelineError("AEP-PIPE-SCOPE", path, "{} must name a file".format(label), 2)
    else:
        value_for_parts = value
    raw_parts = value_for_parts.split("/")
    if not value_for_parts or any(part in ("", ".", "..") for part in raw_parts):
        raise PipelineError("AEP-PIPE-SCOPE", path, "{} escapes or is ambiguous: {!r}".format(label, value), 2)
    return value


def _canonical_digest(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _parse_contract_text(text: str, path: str) -> List[Milestone]:
    metadata = _metadata(text, path)
    if metadata.get("Status") != "ACCEPTED":
        raise PipelineError("AEP-PIPE-AUTH", path, "specification status is not ACCEPTED")
    contract = _require_keys(_extract_json_block(text, CONTRACT_BEGIN, CONTRACT_END, path), CONTRACT_KEYS, path, "contract")
    if contract["schema"] != CONTRACT_SCHEMA:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "unsupported contract schema {!r}".format(contract["schema"]), 2)
    entries = contract["milestones"]
    if not isinstance(entries, list):
        raise PipelineError("AEP-PIPE-SCHEMA", path, "milestones must be an array", 2)

    milestones: List[Milestone] = []
    identifiers: set = set()
    orders: set = set()
    issues: set = set()
    for index, raw_value in enumerate(entries):
        label = "milestones[{}]".format(index)
        raw = _require_keys(raw_value, MILESTONE_KEYS, path, label)
        milestone_id = _require_string(raw["id"], path, label + ".id")
        if milestone_id in identifiers:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "duplicate milestone id {!r}".format(milestone_id), 2)
        identifiers.add(milestone_id)
        order = raw["order"]
        if not isinstance(order, int) or isinstance(order, bool) or order < 1 or order in orders:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "milestone order must be a unique positive integer", 2)
        orders.add(order)
        _require_string(raw["title"], path, label + ".title")
        issue = _safe_relative(raw["issue"], path, label + ".issue")
        if issue in issues:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "duplicate owning issue {!r}".format(issue), 2)
        issues.add(issue)
        dependencies = _require_string_list(raw["depends_on"], path, label + ".depends_on")
        _require_string_list(raw["scope"], path, label + ".scope", allow_empty=False)
        allowed = _require_string_list(raw["allowed_paths"], path, label + ".allowed_paths", allow_empty=False)
        for allowed_path in allowed:
            _safe_relative(allowed_path, path, label + ".allowed_paths", allow_directory=True)
        if not any(issue == candidate or (candidate.endswith("/") and issue.startswith(candidate)) for candidate in allowed):
            raise PipelineError("AEP-PIPE-SCOPE", path, "owning issue is outside allowed_paths", 2)
        checks = raw["acceptance_checks"]
        if not isinstance(checks, list) or not checks:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "{} acceptance_checks must be nonempty".format(label), 2)
        check_ids: set = set()
        for check_index, check_value in enumerate(checks):
            check = _require_keys(check_value, CHECK_KEYS, path, "{}.acceptance_checks[{}]".format(label, check_index))
            check_id = _require_string(check["id"], path, label + ".acceptance_checks.id")
            if check_id in check_ids:
                raise PipelineError("AEP-PIPE-SCHEMA", path, "duplicate acceptance check id {!r}".format(check_id), 2)
            check_ids.add(check_id)
            _require_string_list(check["argv"], path, label + ".acceptance_checks.argv", allow_empty=False)
            timeout = check["timeout_seconds"]
            if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 3600:
                raise PipelineError("AEP-PIPE-SCHEMA", path, "acceptance timeout must be an integer from 1 through 3600", 2)
        if raw["review"] != "INDEPENDENT":
            raise PipelineError("AEP-PIPE-AUTH", path, "pipeline milestones require review INDEPENDENT")
        milestones.append(Milestone(raw=raw, digest=_canonical_digest(raw)))

    by_id = {item.milestone_id: item for item in milestones}
    for milestone in milestones:
        for dependency in milestone.raw["depends_on"]:
            if dependency not in by_id:
                raise PipelineError("AEP-PIPE-SCHEMA", path, "unknown dependency {!r}".format(dependency), 2)
            if by_id[dependency].raw["order"] >= milestone.raw["order"]:
                raise PipelineError("AEP-PIPE-SCHEMA", path, "dependency {!r} must have a lower order".format(dependency), 2)
    ordered = sorted(milestones, key=lambda item: (item.raw["order"], item.milestone_id))
    return ordered


def _parse_state(text: str, milestone: Milestone) -> Dict[str, Any]:
    path = milestone.issue
    state = dict(_require_keys(_extract_json_block(text, STATE_BEGIN, STATE_END, path), STATE_KEYS, path, "pipeline state"))
    if state["schema"] != STATE_SCHEMA:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "unsupported state schema {!r}".format(state["schema"]), 2)
    if state["milestone_id"] != milestone.milestone_id:
        raise PipelineError("AEP-PIPE-AUTH", path, "state milestone_id does not match its contract")
    if state["authority_digest"] != milestone.digest:
        raise PipelineError("AEP-PIPE-AUTH", path, "state authority_digest does not match accepted contract")
    if state["state"] not in STATES:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "unsupported milestone state {!r}".format(state["state"]), 2)
    if not isinstance(state["attempt"], int) or isinstance(state["attempt"], bool) or state["attempt"] < 0:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "attempt must be a nonnegative integer", 2)
    for nullable in ("implementor", "base_revision", "target_revision"):
        if state[nullable] is not None:
            _require_string(state[nullable], path, nullable)
    for revision_field in ("base_revision", "target_revision"):
        value = state[revision_field]
        if value is not None and FULL_REVISION_RE.fullmatch(value) is None:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "{} must be a full lowercase Git revision".format(revision_field), 2)
    _require_string_list(state["verification_evidence"], path, "verification_evidence")
    _require_string_list(state["review_references"], path, "review_references")
    events = state["events"]
    if not isinstance(events, list) or not events:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "events must be a nonempty array", 2)
    previous: Optional[str] = None
    for index, event_value in enumerate(events):
        event = _require_keys(event_value, EVENT_KEYS, path, "events[{}]".format(index))
        if event["sequence"] != index + 1:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "event sequence must be contiguous from 1", 2)
        _require_string(event["actor"], path, "event actor")
        _require_string(event["reason"], path, "event reason")
        if not isinstance(event["utc"], str) or UTC_RE.fullmatch(event["utc"]) is None:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "event utc must be second-precision UTC", 2)
        if index == 0:
            if event["from"] is not None or event["to"] != "AUTHORIZED":
                raise PipelineError("AEP-PIPE-SCHEMA", path, "first event must be null to AUTHORIZED", 2)
        else:
            if event["from"] != previous or not _legal_transition(previous, event["to"]):
                raise PipelineError("AEP-PIPE-SCHEMA", path, "event {} records an illegal transition".format(index + 1), 2)
        previous = event["to"]
    if previous != state["state"]:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "final event does not match current state", 2)
    if state["state"] in {"IN_PROGRESS", "AWAITING_PEER_REVIEW", "CHANGES_REQUIRED", "ACCEPTED"}:
        if state["implementor"] is None or state["base_revision"] is None or state["attempt"] < 1:
            raise PipelineError("AEP-PIPE-SCHEMA", path, "active state lacks implementor/base/attempt", 2)
    if state["state"] in {"AWAITING_PEER_REVIEW", "CHANGES_REQUIRED", "ACCEPTED"} and state["target_revision"] is None:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "review state lacks target_revision", 2)
    return state


def _validate_state_references(root: Path, milestone: Milestone, state: Mapping[str, Any]) -> None:
    evidence_records: List[Mapping[str, Any]] = []
    for reference in state["verification_evidence"]:
        _safe_relative(reference, milestone.issue, "verification evidence reference")
        if not reference.startswith("EVIDENCE/") or not reference.endswith(".json"):
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "verification evidence must reference EVIDENCE/*.json")
        path = root / PurePosixPath(reference)
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root.resolve())
        except (OSError, ValueError) as error:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "verification evidence does not resolve safely: {}".format(error))
        if path.is_symlink() or not resolved.is_file():
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "verification evidence is not a regular non-symlink file")
        record = _json_load(_read_text(resolved, reference), reference)
        if not isinstance(record, dict):
            raise PipelineError("AEP-PIPE-STATE", reference, "verification evidence must be a JSON object")
        expected = {
            "schema": EVIDENCE_SCHEMA,
            "milestone_id": milestone.milestone_id,
            "authority_digest": milestone.digest,
            "result": "PASS",
        }
        for key, value in expected.items():
            if record.get(key) != value:
                raise PipelineError("AEP-PIPE-STATE", reference, "evidence field {!r} does not match state authority".format(key))
        if FULL_REVISION_RE.fullmatch(str(record.get("target_revision", ""))) is None:
            raise PipelineError("AEP-PIPE-STATE", reference, "evidence target_revision is invalid")
        evidence_records.append(record)

    for reference in state["review_references"]:
        prefix = milestone.issue + "#"
        if not reference.startswith(prefix) or not reference[len(prefix):]:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "review reference must identify a section in the owning issue")

    if state["state"] in {"AWAITING_PEER_REVIEW", "CHANGES_REQUIRED", "ACCEPTED"}:
        if not evidence_records or evidence_records[-1]["target_revision"] != state["target_revision"]:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "review state lacks matching successful verification evidence")
    if state["state"] == "ACCEPTED" and not state["review_references"]:
        raise PipelineError("AEP-PIPE-STATE", milestone.issue, "accepted state lacks a durable review reference")


def _legal_transition(source: str, target: str) -> bool:
    if target == "BLOCKED_HUMAN_AUTHORITY":
        return source not in {"ACCEPTED", "BLOCKED_HUMAN_AUTHORITY"}
    return (source, target) in TRANSITIONS


def _resolve_owned_path(root: Path, relative: str) -> Path:
    _safe_relative(relative, "PROJECT_SPEC.md", "issue")
    root_resolved = root.resolve()
    candidate = root / PurePosixPath(relative)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise PipelineError("AEP-PIPE-IO", relative, "cannot resolve owning issue: {}".format(error), 2)
    try:
        resolved.relative_to(root_resolved)
    except ValueError:
        raise PipelineError("AEP-PIPE-SCOPE", relative, "owning issue escapes repository", 2)
    if candidate.is_symlink() or not resolved.is_file():
        raise PipelineError("AEP-PIPE-SCOPE", relative, "owning issue must be a regular non-symlink file", 2)
    return resolved


def _structural_gate(root: Path) -> None:
    findings = validate_repository(root)
    if not findings:
        return
    first = findings[0]
    operational = any(item.kind in {"ERROR", "UNSUPPORTED"} for item in findings)
    raise PipelineError(
        "AEP-PIPE-STRUCTURE", first.path,
        "structural validator returned {} finding(s); first: {}".format(len(findings), first.render()),
        2 if operational else 1,
    )


def _load_context(root: Path) -> Context:
    if not root.exists() or not root.is_dir():
        raise PipelineError("AEP-PIPE-IO", str(root), "repository root is not a directory", 2)
    root = root.resolve()
    _structural_gate(root)
    spec_text = _read_text(root / "PROJECT_SPEC.md", "PROJECT_SPEC.md")
    milestones = _parse_contract_text(spec_text, "PROJECT_SPEC.md")
    states: Dict[str, Dict[str, Any]] = {}
    issue_texts: Dict[str, str] = {}
    for milestone in milestones:
        issue_path = _resolve_owned_path(root, milestone.issue)
        issue_text = _read_text(issue_path, milestone.issue)
        metadata = _metadata(issue_text, milestone.issue)
        expected_id = PurePosixPath(milestone.issue).stem
        if metadata.get("ID") != expected_id:
            raise PipelineError("AEP-PIPE-SCHEMA", milestone.issue, "issue ID must match its filename", 2)
        if metadata.get("Milestone") != milestone.milestone_id:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "issue Milestone metadata does not match the contract")
        if metadata.get("Review") != milestone.raw["review"]:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "issue Review metadata does not match the contract")
        state = _parse_state(issue_text, milestone)
        _validate_state_references(root, milestone, state)
        _validate_revision_references(root, milestone, state)
        expected_status = ISSUE_STATUS[state["state"]]
        if metadata.get("Status") != expected_status:
            raise PipelineError(
                "AEP-PIPE-STATE", milestone.issue,
                "issue status {!r} does not match state {} (expected {})".format(metadata.get("Status"), state["state"], expected_status),
            )
        states[milestone.milestone_id] = state
        issue_texts[milestone.milestone_id] = issue_text
    return Context(root=root, milestones=milestones, states=states, issue_texts=issue_texts)


def _dependencies_satisfied(context: Context, milestone: Milestone) -> bool:
    return all(context.states[dependency]["state"] == "ACCEPTED" for dependency in milestone.raw["depends_on"])


def _selected(context: Context) -> Optional[str]:
    for milestone in context.milestones:
        state = context.states[milestone.milestone_id]["state"]
        if state != "ACCEPTED" and _dependencies_satisfied(context, milestone):
            return milestone.milestone_id
    return None


def _status_payload(context: Context) -> Dict[str, Any]:
    selected = _selected(context)
    return {
        "schema": STATUS_SCHEMA,
        "specification_status": "ACCEPTED",
        "structural_validation": "PASS",
        "selected_milestone": selected,
        "milestones": [
            {
                "id": milestone.milestone_id,
                "order": milestone.raw["order"],
                "issue": milestone.issue,
                "authority_digest": milestone.digest,
                "state": context.states[milestone.milestone_id]["state"],
                "dependencies_satisfied": _dependencies_satisfied(context, milestone),
                "selected": milestone.milestone_id == selected,
            }
            for milestone in context.milestones
        ],
    }


def _git(root: Path, arguments: Sequence[str], check: bool = True) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            ["git"] + list(arguments), cwd=str(root), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, check=False, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise PipelineError("AEP-PIPE-GIT", ".git", "cannot execute local Git query: {}".format(error), 2)
    if check and result.returncode != 0:
        message = (result.stderr or result.stdout).strip() or "Git command failed"
        raise PipelineError("AEP-PIPE-GIT", ".git", message, 2)
    return result


def _head(root: Path) -> str:
    value = _git(root, ["rev-parse", "HEAD"]).stdout.strip()
    if FULL_REVISION_RE.fullmatch(value) is None:
        raise PipelineError("AEP-PIPE-GIT", ".git", "HEAD did not resolve to a full revision", 2)
    return value


def _validate_revision_references(root: Path, milestone: Milestone, state: Mapping[str, Any]) -> None:
    for field in ("base_revision", "target_revision"):
        revision = state[field]
        if revision is None:
            continue
        result = _git(root, ["cat-file", "-e", revision + "^{commit}"], check=False)
        if result.returncode != 0:
            raise PipelineError("AEP-PIPE-STATE", milestone.issue, "{} does not resolve to a local commit".format(field))


def _require_clean(root: Path) -> None:
    output = _git(root, ["status", "--porcelain", "--untracked-files=all"]).stdout
    if output:
        paths = sorted(line[3:] for line in output.splitlines() if len(line) >= 4)
        raise PipelineError("AEP-PIPE-GIT", ".git", "working tree is not clean: {}".format(", ".join(paths[:8])))


def _target_revision(root: Path, supplied: str) -> str:
    if FULL_REVISION_RE.fullmatch(supplied) is None:
        raise PipelineError("AEP-PIPE-TARGET", ".git", "target must be a full lowercase 40-character commit")
    resolved = _git(root, ["rev-parse", "--verify", supplied + "^{commit}"]).stdout.strip()
    if resolved != supplied:
        raise PipelineError("AEP-PIPE-TARGET", ".git", "target does not resolve to the supplied commit")
    return resolved


def _path_allowed(path: str, allowed: Sequence[str]) -> bool:
    return any(path == candidate or (candidate.endswith("/") and path.startswith(candidate)) for candidate in allowed)


def _verify_target_scope(context: Context, milestone: Milestone, state: Mapping[str, Any], target: str) -> None:
    if target != _head(context.root):
        raise PipelineError("AEP-PIPE-TARGET", ".git", "submission target must equal current HEAD")
    base = state["base_revision"]
    ancestor = _git(context.root, ["merge-base", "--is-ancestor", base, target], check=False)
    if ancestor.returncode != 0:
        raise PipelineError("AEP-PIPE-TARGET", ".git", "base_revision is not an ancestor of target")
    names = _git(context.root, ["diff", "--name-only", "{}..{}".format(base, target)]).stdout.splitlines()
    outside = sorted(name for name in names if not _path_allowed(name, milestone.raw["allowed_paths"]))
    if outside:
        raise PipelineError("AEP-PIPE-SCOPE", ".git", "target changes paths outside milestone scope: {}".format(", ".join(outside)))
    spec_at_target = _git(context.root, ["show", "{}:PROJECT_SPEC.md".format(target)]).stdout
    target_milestones = _parse_contract_text(spec_at_target, "{}:PROJECT_SPEC.md".format(target))
    target_by_id = {item.milestone_id: item for item in target_milestones}
    target_contract = target_by_id.get(milestone.milestone_id)
    if target_contract is None or target_contract.digest != milestone.digest:
        raise PipelineError("AEP-PIPE-AUTH", "PROJECT_SPEC.md", "target does not contain the accepted milestone contract digest")


def _bounded_output(value: str, limit: int = 16384) -> Tuple[str, bool]:
    if len(value.encode("utf-8")) <= limit:
        return value, False
    encoded = value.encode("utf-8")[:limit]
    return encoded.decode("utf-8", errors="replace"), True


def _run_checks(root: Path, milestone: Milestone) -> Tuple[List[Dict[str, Any]], bool]:
    records: List[Dict[str, Any]] = []
    all_passed = True
    environment = os.environ.copy()
    sensitive_fragments = (
        "TOKEN", "SECRET", "PASSWORD", "PASSWD", "CREDENTIAL", "API_KEY",
        "PRIVATE_KEY", "ACCESS_KEY", "SESSION", "COOKIE", "AUTH",
    )
    for name in list(environment):
        if any(fragment in name.upper() for fragment in sensitive_fragments):
            environment.pop(name, None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for check in milestone.raw["acceptance_checks"]:
        record: Dict[str, Any] = {
            "id": check["id"],
            "argv": check["argv"],
            "timeout_seconds": check["timeout_seconds"],
            "exit_code": None,
            "timed_out": False,
            "stdout": "",
            "stderr": "",
            "stdout_truncated": False,
            "stderr_truncated": False,
        }
        try:
            result = subprocess.run(
                check["argv"], cwd=str(root), shell=False, env=environment,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                check=False, timeout=check["timeout_seconds"],
            )
            record["exit_code"] = result.returncode
            record["stdout"], record["stdout_truncated"] = _bounded_output(result.stdout)
            record["stderr"], record["stderr_truncated"] = _bounded_output(result.stderr)
            if result.returncode != 0:
                all_passed = False
        except subprocess.TimeoutExpired as error:
            record["timed_out"] = True
            stdout = error.stdout.decode("utf-8", errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
            stderr = error.stderr.decode("utf-8", errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
            record["stdout"], record["stdout_truncated"] = _bounded_output(stdout)
            record["stderr"], record["stderr_truncated"] = _bounded_output(stderr)
            all_passed = False
        except OSError as error:
            record["stderr"] = "{}: {}".format(type(error).__name__, error)
            all_passed = False
        records.append(record)
    return records, all_passed


def _atomic_write(path: Path, data: bytes, replace: bool) -> None:
    path.parent.mkdir(parents=False, exist_ok=True)
    if not replace and path.exists():
        raise PipelineError("AEP-PIPE-IO", path.as_posix(), "refusing to overwrite existing evidence", 2)
    old_mode = path.stat().st_mode & 0o777 if replace and path.exists() else 0o644
    descriptor = -1
    temporary_name = ""
    try:
        descriptor, temporary_name = tempfile.mkstemp(prefix=".aep-pipeline-", dir=str(path.parent))
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if not replace and path.exists():
            raise PipelineError("AEP-PIPE-IO", path.as_posix(), "evidence path appeared concurrently", 2)
        os.replace(temporary_name, str(path))
        temporary_name = ""
    except PipelineError:
        raise
    except OSError as error:
        raise PipelineError("AEP-PIPE-IO", path.as_posix(), "atomic write failed: {}".format(error), 2)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary_name:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass


def _write_verification_evidence(
    context: Context,
    milestone: Milestone,
    state: Mapping[str, Any],
    target: str,
    actor: str,
    checks: List[Dict[str, Any]],
    passed: bool,
    utc: str,
) -> str:
    stamp = utc.replace("-", "").replace(":", "")
    name = "EVIDENCE-{}-{}-attempt-{}.json".format(stamp, _slug(milestone.milestone_id), state["attempt"])
    relative = "EVIDENCE/" + name
    payload = {
        "schema": EVIDENCE_SCHEMA,
        "id": name[:-5],
        "recorded_utc": utc,
        "participant": actor,
        "milestone_id": milestone.milestone_id,
        "authority_digest": milestone.digest,
        "base_revision": state["base_revision"],
        "target_revision": target,
        "environment": {
            "python": sys.version.split()[0],
            "platform": sys.platform,
        },
        "structural_validator": {"result": "PASS", "finding_count": 0},
        "checks": checks,
        "result": "PASS" if passed else "FAIL",
        "limitations": [
            "Participant labels are recorded assertions, not authenticated identities.",
            "Passing deterministic checks does not establish semantic correctness or review adequacy.",
        ],
    }
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _atomic_write(context.root / relative, encoded, replace=False)
    return relative


def _replace_metadata(text: str, field: str, value: str, path: str) -> str:
    pattern = re.compile(r"^- \*\*" + re.escape(field) + r":\*\*.*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "metadata field {!r} must appear exactly once".format(field), 2)
    return pattern.sub("- **{}:** `{}`".format(field, value), text, count=1)


def _replace_state_block(text: str, state: Mapping[str, Any], path: str) -> str:
    start = text.index(STATE_BEGIN)
    finish = text.index(STATE_END, start) + len(STATE_END)
    replacement = STATE_BEGIN + "\n```json\n" + json.dumps(state, ensure_ascii=False, indent=2) + "\n```\n" + STATE_END
    return text[:start] + replacement + text[finish:]


def _append_section_line(text: str, heading: str, line: str, path: str) -> str:
    marker = "## " + heading
    start = text.find(marker)
    if start < 0 or text.find(marker, start + 1) >= 0:
        raise PipelineError("AEP-PIPE-SCHEMA", path, "section {!r} must appear exactly once".format(heading), 2)
    next_heading = text.find("\n## ", start + len(marker))
    end = len(text) if next_heading < 0 else next_heading
    body = text[start:end].rstrip()
    return text[:start] + body + "\n\n" + line + "\n" + text[end:].lstrip("\n")


def _append_activity(text: str, utc: str, actor: str, source: str, target: str, reason: str, path: str) -> str:
    safe_reason = reason.replace("|", "\\|").replace("\n", " ")
    line = "| `{}` | `{}` | `{}` | `{}` | {} |".format(utc, actor, source, target, safe_reason)
    return _append_section_line(text, "Activity history", line, path)


def _updated_issue_text(
    context: Context,
    milestone: Milestone,
    state: Dict[str, Any],
    source: str,
    target: str,
    actor: str,
    utc: str,
    reason: str,
    evidence: Optional[str] = None,
    blocker: Optional[Tuple[str, str]] = None,
) -> str:
    text = context.issue_texts[milestone.milestone_id]
    text = _replace_metadata(text, "Status", ISSUE_STATUS[target], milestone.issue)
    text = _replace_metadata(text, "Updated UTC", utc, milestone.issue)
    text = _replace_state_block(text, state, milestone.issue)
    if evidence is not None:
        line = "- **Pipeline verification `{}`:** [`{}`](../{}) — deterministic structural and accepted-command gates passed for `{}`.".format(
            utc, evidence, evidence, state["target_revision"]
        )
        text = _append_section_line(text, "Verification", line, milestone.issue)
    if blocker is not None:
        blocker_path, condition = blocker
        replacements = {
            "Blocked from": source,
            "Blocker": "Linked human-authority issue {}".format(blocker_path),
            "Unblock owner": "Human technical owner",
            "Unblock condition": condition,
        }
        for field, value in replacements.items():
            pattern = re.compile(r"^- \*\*" + re.escape(field) + r":\*\*.*$", re.MULTILINE)
            if len(pattern.findall(text)) != 1:
                raise PipelineError("AEP-PIPE-SCHEMA", milestone.issue, "blocker field {!r} must appear exactly once".format(field), 2)
            text = pattern.sub("- **{}:** `{}`".format(field, value), text, count=1)
    text = _append_activity(
        text, utc, actor, ISSUE_STATUS[source], ISSUE_STATUS[target],
        "Pipeline {} -> {}. {}".format(source, target, reason), milestone.issue,
    )
    if not text.endswith("\n"):
        text += "\n"
    return text


def _append_event(state: Dict[str, Any], source: str, target: str, actor: str, utc: str, reason: str) -> None:
    state["state"] = target
    state["events"].append({
        "sequence": len(state["events"]) + 1,
        "utc": utc,
        "actor": actor,
        "from": source,
        "to": target,
        "reason": reason,
    })


def _parse_latest_review(text: str, path: str) -> ReviewRound:
    section_start = text.find("## Independent review rounds")
    if section_start < 0:
        raise PipelineError("AEP-PIPE-REVIEW", path, "Independent review rounds section is missing", 2)
    section_end = text.find("\n## ", section_start + 1)
    section = text[section_start:] if section_end < 0 else text[section_start:section_end]
    headings = list(REVIEW_HEADING_RE.finditer(section))
    if not headings:
        raise PipelineError("AEP-PIPE-REVIEW", path, "no durable independent review round is recorded")
    heading = headings[-1]
    body = section[heading.end():]

    def field(name: str) -> str:
        pattern = re.compile(r"^- \*\*" + re.escape(name) + r":\*\*\s+`?(?P<value>[^`\n]+)`?\s*$", re.MULTILINE)
        matches = list(pattern.finditer(body))
        if len(matches) != 1:
            raise PipelineError("AEP-PIPE-REVIEW", path, "latest review must contain exactly one {!r} field".format(name), 2)
        return matches[0].group("value").strip()

    target = field("Reviewed target")
    if FULL_REVISION_RE.fullmatch(target) is None:
        raise PipelineError("AEP-PIPE-REVIEW", path, "reviewed target must be a full lowercase Git revision", 2)
    material_text = field("Open material findings")
    if not re.fullmatch(r"\d+", material_text):
        raise PipelineError("AEP-PIPE-REVIEW", path, "open material findings must be a nonnegative integer", 2)
    disposition = field("Disposition")
    if disposition not in DISPOSITIONS:
        raise PipelineError("AEP-PIPE-REVIEW", path, "unsupported disposition {!r}".format(disposition), 2)
    return ReviewRound(
        utc=heading.group("utc"), reviewer=heading.group("reviewer").strip(),
        target=target, material_findings=int(material_text), disposition=disposition,
    )


def _closure_complete(text: str, path: str) -> None:
    start = text.find("## Closure checklist")
    if start < 0:
        raise PipelineError("AEP-PIPE-REVIEW", path, "Closure checklist section is missing", 2)
    body = text[start:]
    boxes = re.findall(r"^- \[(?P<mark>[ xX])\] ", body, re.MULTILINE)
    if not boxes or any(mark == " " for mark in boxes):
        raise PipelineError("AEP-PIPE-REVIEW", path, "all closure checklist items must be checked before acceptance")


def _post_target_drift(context: Context, milestone: Milestone, target: str) -> None:
    head = _head(context.root)
    if head == target:
        return
    names = _git(context.root, ["diff", "--name-only", "{}..{}".format(target, head)]).stdout.splitlines()
    safe_exact = {milestone.issue, "HANDOFF.md", "HUMAN_CHECKPOINT.md"}
    unsafe = []
    for name in names:
        record_only = name in safe_exact or name.startswith("EVIDENCE/") or (
            name.startswith("ISSUES/") and name.endswith(".md") and name != "ISSUES/TEMPLATE.md"
        )
        if not record_only:
            unsafe.append(name)
    if unsafe:
        raise PipelineError("AEP-PIPE-TARGET", ".git", "implementation changed after reviewed target: {}".format(", ".join(sorted(unsafe))))


def _human_blocker(root: Path, relative: str) -> Tuple[str, str]:
    _safe_relative(relative, "command", "blocker issue")
    if not relative.startswith("ISSUES/") or not relative.endswith(".md"):
        raise PipelineError("AEP-PIPE-BLOCKER", relative, "blocker must be a repository issue path")
    path = _resolve_owned_path(root, relative)
    text = _read_text(path, relative)
    metadata = _metadata(text, relative)
    if metadata.get("Status") != "BLOCKED" or metadata.get("Authority") != "HUMAN":
        raise PipelineError("AEP-PIPE-BLOCKER", relative, "blocker issue must have Status BLOCKED and Authority HUMAN")
    match = re.search(r"^- \*\*Unblock condition:\*\*\s+`?(?P<value>[^`\n]+)`?\s*$", text, re.MULTILINE)
    if match is None or match.group("value").strip().upper() in {"", "NONE", "UNKNOWN", "PENDING"}:
        raise PipelineError("AEP-PIPE-BLOCKER", relative, "blocker issue needs a nonempty observable Unblock condition")
    return relative, match.group("value").strip()


def _find_milestone(context: Context, milestone_id: str) -> Milestone:
    matches = [item for item in context.milestones if item.milestone_id == milestone_id]
    if not matches:
        raise PipelineError("AEP-PIPE-AUTH", "PROJECT_SPEC.md", "milestone {!r} is not authorized".format(milestone_id))
    return matches[0]


def _commit_issue(context: Context, milestone: Milestone, text: str) -> None:
    # Recheck the source bytes immediately before replacement. This detects
    # cooperating writers without claiming a general concurrent-writer lock.
    path = context.root / milestone.issue
    current = _read_text(path, milestone.issue)
    if current != context.issue_texts[milestone.milestone_id]:
        raise PipelineError("AEP-PIPE-CONFLICT", milestone.issue, "owning issue changed during transition")
    _atomic_write(path, text.encode("utf-8"), replace=True)


def _transition(context: Context, arguments: argparse.Namespace) -> str:
    milestone = _find_milestone(context, arguments.milestone)
    state = json.loads(json.dumps(context.states[milestone.milestone_id]))
    source = state["state"]
    target_state = arguments.to
    if arguments.target is not None and target_state != "AWAITING_PEER_REVIEW":
        raise PipelineError("AEP-PIPE-CLI", "command", "--target is valid only for AWAITING_PEER_REVIEW", 2)
    if arguments.blocker_issue is not None and target_state != "BLOCKED_HUMAN_AUTHORITY":
        raise PipelineError("AEP-PIPE-CLI", "command", "--blocker-issue is valid only for BLOCKED_HUMAN_AUTHORITY", 2)
    if not _legal_transition(source, target_state):
        raise PipelineError("AEP-PIPE-STATE", milestone.issue, "transition {} -> {} is not permitted".format(source, target_state))
    if not _dependencies_satisfied(context, milestone):
        raise PipelineError("AEP-PIPE-AUTH", milestone.issue, "milestone dependencies are not accepted")
    actor = _require_string(arguments.actor, "command", "actor")
    if ACTOR_RE.fullmatch(actor) is None:
        raise PipelineError("AEP-PIPE-CLI", "command", "actor must be a bounded portable participant label", 2)
    utc = _utc_now()
    reason = "Validated transition {} to {}.".format(source, target_state)
    evidence: Optional[str] = None
    blocker: Optional[Tuple[str, str]] = None

    if target_state == "READY":
        _require_clean(context.root)
        if _selected(context) != milestone.milestone_id:
            raise PipelineError("AEP-PIPE-AUTH", milestone.issue, "milestone is not the next dependency-satisfied contract")
    elif target_state == "IN_PROGRESS":
        _require_clean(context.root)
        state["attempt"] += 1
        state["implementor"] = actor
        state["base_revision"] = _head(context.root)
        state["target_revision"] = None
        reason = "Implementation attempt {} began from immutable base {}.".format(state["attempt"], state["base_revision"])
    elif target_state == "AWAITING_PEER_REVIEW":
        if arguments.target is None:
            raise PipelineError("AEP-PIPE-CLI", "command", "--target is required for AWAITING_PEER_REVIEW", 2)
        _require_clean(context.root)
        target = _target_revision(context.root, arguments.target)
        _verify_target_scope(context, milestone, state, target)
        _structural_gate(context.root)
        checks, passed = _run_checks(context.root, milestone)
        evidence = _write_verification_evidence(context, milestone, state, target, actor, checks, passed, utc)
        if not passed:
            raise PipelineError("AEP-PIPE-VERIFY", evidence, "accepted verification command failed; state did not advance")
        state["target_revision"] = target
        state["verification_evidence"].append(evidence)
        reason = "Immutable target {} passed structural and accepted deterministic checks; evidence {}.".format(target, evidence)
    elif target_state in {"CHANGES_REQUIRED", "ACCEPTED"}:
        _require_clean(context.root)
        review = _parse_latest_review(context.issue_texts[milestone.milestone_id], milestone.issue)
        if review.reviewer == state["implementor"]:
            raise PipelineError("AEP-PIPE-REVIEW", milestone.issue, "reviewer label equals implementor label")
        if review.target != state["target_revision"]:
            raise PipelineError("AEP-PIPE-REVIEW", milestone.issue, "latest review target does not match verified target")
        reference = "{}#{}".format(milestone.issue, review.reference_fragment)
        if reference not in state["review_references"]:
            state["review_references"].append(reference)
        if target_state == "CHANGES_REQUIRED":
            if review.disposition != "CHANGES_REQUIRED" or review.material_findings < 1:
                raise PipelineError("AEP-PIPE-REVIEW", milestone.issue, "CHANGES_REQUIRED needs that exact disposition and at least one open material finding")
            reason = "Independent review {} recorded {} open material finding(s); within-scope fixes are required.".format(reference, review.material_findings)
        else:
            if review.disposition != "APPROVED" or review.material_findings != 0:
                raise PipelineError("AEP-PIPE-REVIEW", milestone.issue, "ACCEPTED requires disposition APPROVED and zero open material findings")
            _closure_complete(context.issue_texts[milestone.milestone_id], milestone.issue)
            _post_target_drift(context, milestone, state["target_revision"])
            _structural_gate(context.root)
            reason = "Independent review {} approved the verified target with zero open material findings.".format(reference)
    elif target_state == "BLOCKED_HUMAN_AUTHORITY":
        _require_clean(context.root)
        if arguments.blocker_issue is None:
            raise PipelineError("AEP-PIPE-CLI", "command", "--blocker-issue is required for BLOCKED_HUMAN_AUTHORITY", 2)
        blocker = _human_blocker(context.root, arguments.blocker_issue)
        reason = "Human authority is required; linked blocker {} defines the unblock condition.".format(blocker[0])

    _append_event(state, source, target_state, actor, utc, reason)
    updated = _updated_issue_text(
        context, milestone, state, source, target_state, actor, utc, reason,
        evidence=evidence, blocker=blocker,
    )
    _commit_issue(context, milestone, updated)
    return "PASS {} {} -> {} issue={}\n".format(milestone.milestone_id, source, target_state, milestone.issue)


def _build_parser() -> argparse.ArgumentParser:
    parser = StableArgumentParser(description="Validate and record gates for milestones already authorized by PROJECT_SPEC.md.")
    parser.add_argument("--root", dest="global_root", default=None, help="repository root (default: parent of this script)")
    subparsers = parser.add_subparsers(dest="command", required=True, parser_class=StableArgumentParser)

    status = subparsers.add_parser("status", help="show deterministic authorized milestone state")
    status.add_argument("--root", default=None, help="repository root")
    status.add_argument("--json", action="store_true", help="emit canonical JSON")

    transition = subparsers.add_parser("transition", help="validate and record one lifecycle transition")
    transition.add_argument("--root", default=None, help="repository root")
    transition.add_argument("--milestone", required=True, help="authorized milestone ID")
    transition.add_argument("--actor", required=True, help="attributable participant label (not authenticated)")
    transition.add_argument("--to", required=True, choices=sorted(STATES), help="destination state")
    transition.add_argument("--target", default=None, help="full immutable Git target for review submission")
    transition.add_argument("--blocker-issue", default=None, help="linked BLOCKED/HUMAN issue for human escalation")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    root_argument = arguments.root if getattr(arguments, "root", None) is not None else arguments.global_root
    root = Path(root_argument) if root_argument is not None else Path(__file__).resolve().parent.parent
    try:
        context = _load_context(root)
        if arguments.command == "status":
            payload = _status_payload(context)
            if arguments.json:
                print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            else:
                print("PASS authorized milestone status (milestones={} selected={})".format(
                    len(context.milestones), payload["selected_milestone"] or "NONE"
                ))
                for item in payload["milestones"]:
                    print("{} order={} state={} dependencies={}{}".format(
                        item["id"], item["order"], item["state"],
                        "SATISFIED" if item["dependencies_satisfied"] else "WAITING",
                        " selected" if item["selected"] else "",
                    ))
            return 0
        sys.stdout.write(_transition(context, arguments))
        return 0
    except PipelineError as error:
        print(error.render(), file=sys.stderr)
        print("SUMMARY advanced=0 errors=1", file=sys.stderr)
        return error.exit_code
    except Exception as error:  # Defensive boundary: do not expose an unstable traceback as API.
        print("ERROR AEP-PIPE-INTERNAL command: {}: {}".format(type(error).__name__, error), file=sys.stderr)
        print("SUMMARY advanced=0 errors=1", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
