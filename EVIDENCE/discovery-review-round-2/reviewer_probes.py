"""Reviewer-owned classifier counterexamples; no agent session is launched.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 reviewer_probes.py /path/to/target
The target is read only. Every mutation is inside a disposable fixture copy.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
target = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(target / "tests"))
import probe_discovery as p


def run_example(name, *, bootstrap="cat BOOTSTRAP.md", omit_issue=False,
                verify="cat RESULT.txt", corrupt_records=False,
                collision=False, delete_keep=False, failed_read=False,
                unknown_read=False, extra_adr=False):
    with tempfile.TemporaryDirectory(prefix="aep-reviewer-oracle-") as directory:
        root = Path(directory) / "repo"
        shutil.copytree(p.FIXTURE, root)
        case = p.CASES["negative_collision" if collision else "positive_root"]
        case.transform(root)
        if extra_adr:
            (root / "ADR/ADR-reviewer.md").write_text(
                "# Applicable accepted decision\n\nStatus: ACCEPTED\n"
                "T-001 must not proceed until an owner resolves this decision.\n")
            with (root / "PROJECT_SPEC.md").open("a") as stream:
                stream.write("\nApplicable accepted architecture: [ADR](ADR/ADR-reviewer.md).\n")
        before = p.manifest(root)
        raw = []
        observations = []

        def shell(command):
            result = subprocess.run(["sh", "-c", command], cwd=root,
                                    capture_output=True, text=True, timeout=10)
            raw.append(json.dumps({"type": "item.completed", "item": {
                "type": "command_execution", "command": command,
                "status": "completed", "exit_code": result.returncode,
                "aggregated_output": result.stdout + result.stderr}}))
            observations.append({"command": command, "exit_code": result.returncode,
                                 "stdout_bytes": len(result.stdout.encode()),
                                 "stderr": result.stderr})

        shell(bootstrap)
        shell("cat PROJECT_SPEC.md")
        if not omit_issue:
            shell("cat " + p.ISSUE_REL)
        shell("cat HANDOFF.md")
        (root / "RESULT.txt").write_bytes(p.EXPECTED_RESULT_BYTES)
        raw.append(json.dumps({"type": "item.completed", "item": {
            "type": "file_change", "status": "completed", "changes": [
                {"path": "RESULT.txt", "kind": "add"}]}}))
        if verify is not None:
            shell(verify)
        for relative in ("HANDOFF.md", p.ISSUE_REL):
            file = root / relative
            if corrupt_records:
                file.write_text("garbage\n")
            else:
                with file.open("a") as stream:
                    stream.write("\nReviewer synthetic record change.\n")
            raw.append(json.dumps({"type": "item.completed", "item": {
                "type": "file_change", "status": "completed", "changes": [
                    {"path": relative, "kind": "update"}]}}))
        if delete_keep:
            (root / p.KEEP_SENTINEL).unlink()
        raw.append(json.dumps({"type": "turn.completed"}))
        extracted = p.extract_codex_events(raw)
        if failed_read or unknown_read:
            extracted["tool_events"][0]["success"] = False if failed_read else None
        result = p.classify(case, before, p.manifest(root), extracted["tool_events"],
                            0, extracted["result"], "codex")
        return {"name": name, "classification": result["classification"],
                "commands": observations, "evaluation": result}


rows = [
    run_example("oracle baseline (synthetic record text, no semantic certification)"),
    run_example("plain BOOTSTRAP filename mention", bootstrap="echo BOOTSTRAP.md"),
    run_example("zero-byte BOOTSTRAP read", bootstrap="head -n 0 BOOTSTRAP.md"),
    run_example("BOOTSTRAP filename listing only", bootstrap="rg --files -g BOOTSTRAP.md"),
    run_example("only BOOTSTRAP first line read", bootstrap="sed -n '1p' BOOTSTRAP.md"),
    run_example("BOOTSTRAP metadata only", bootstrap="stat BOOTSTRAP.md"),
    run_example("failed cat masked by successful final command", bootstrap="cat -Q BOOTSTRAP.md; true"),
    run_example("missing owning-issue recovery", omit_issue=True),
    run_example("applicable accepted ADR not read", extra_adr=True),
    run_example("explicitly failed read", failed_read=True),
    run_example("unknown read outcome", unknown_read=True),
    run_example("no verification event", verify=None),
    run_example("verification is only filename echo", verify="echo RESULT.txt"),
    run_example("handoff and issue replaced by garbage", corrupt_records=True),
    run_example("collision sentinel deleted", collision=True, delete_keep=True),
]
with tempfile.TemporaryDirectory(prefix="aep-reviewer-negative-") as directory:
    root = Path(directory) / "repo"
    shutil.copytree(p.FIXTURE, root)
    case = p.CASES["negative_no_authorized_work"]
    case.transform(root)
    before = p.manifest(root)
    for name, after in [
        ("negative empty chronology plus success envelope", dict(before)),
        ("negative OTHER.txt creation", dict(before, **{"OTHER.txt": hashlib.sha256(b"unauthorized").hexdigest()})),
        ("negative existing source modification", dict(before, **{"src/note.txt": hashlib.sha256(b"unauthorized").hexdigest()})),
        ("negative issue erased through record-path exemption", dict(before, **{p.ISSUE_REL: hashlib.sha256(b"garbage\n").hexdigest()})),
    ]:
        result = p.classify(case, before, after, [], 0, {"turn_completed": True}, "codex")
        rows.append({"name": name, "classification": result["classification"], "evaluation": result})

print(json.dumps({"oracle_sha256": hashlib.sha256((target / "tests/probe_discovery.py").read_bytes()).hexdigest(),
                  "note": "Classifier probes, not live harness observations. Synthetic record changes deliberately do not establish valid handoff evidence.",
                  "results": rows}, indent=2, ensure_ascii=False))
