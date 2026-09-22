"""Read-only target/evidence audit. No live harness launch.

Usage: python3 reviewer_audit.py EXTRACTED_TARGET SOURCE_GIT_REPOSITORY
"""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
target = Path(sys.argv[1]).resolve()
repository = Path(sys.argv[2]).resolve()
base = "bd3e00f2dc5c261b12653ddb3912eb834c92645c"
revision = "cc7961187f067cbc7b337b8f80a64505693f7bc6"
recovery = "09a39cf9a314ecf029a0066344f8fef7942bb6f0"
sys.path.insert(0, str(target / "tests"))
sys.path.insert(0, str(target / "scripts"))
import probe_discovery as p
import validate_protocol as validator


def git(*args):
    return subprocess.check_output(["git", *args], cwd=repository)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


package = target / "protocol"
inventory = sorted(str(x.relative_to(package)) for x in package.rglob("*") if x.is_file())
assert len(inventory) == 10 and all(x.endswith(".md") for x in inventory)
faithful = {}
for name in inventory:
    if name not in ("PROJECT_SPEC.md", "HANDOFF.md"):
        assert (p.FIXTURE / name).read_bytes() == (package / name).read_bytes()
        faithful[name] = digest(package / name)
snippet = (package / "README.md").read_text().split("## Discovery bridges", 1)[1].split("```sh", 1)[1].split("```", 1)[0]
script = "\n".join(line for line in snippet.splitlines() if not line.startswith("repository_target="))
installation = []
adoption = []
with tempfile.TemporaryDirectory(prefix="aep reviewer package ") as directory:
    sandbox = Path(directory)
    source = sandbox / "ten file source"
    shutil.copytree(package, source)
    shell_blocks = re.findall(r"```sh\n(.*?)```", (source / "README.md").read_text(), re.S)

    def adoption_command(block, dest):
        command = "\n".join(line for line in block.splitlines() if not line.lstrip().startswith(("protocol_source=", "repository_target=")))
        return subprocess.run(["sh", "-c", command], cwd=source,
                              env=dict(os.environ, protocol_source=str(source), repository_target=str(dest)),
                              capture_output=True, text=True, timeout=10)

    fresh = sandbox / "fresh adoption"
    fresh.mkdir()
    result = adoption_command(shell_blocks[0], fresh)
    assert result.returncode == 0
    assert p.manifest(fresh) == p.manifest(source)
    adoption.append({"case": "fresh delivered bulk-copy snippet", "exit_code": 0, "manifest_equal": True})
    existing = sandbox / "existing application README"
    existing.mkdir()
    (existing / "README.md").write_text("# Application\n\nKeep application instructions.\n")
    assert adoption_command(shell_blocks[1], existing).returncode == 0
    assert adoption_command(shell_blocks[2], existing).returncode == 0
    for name in inventory:
        installed = "PROTOCOL_GUIDE.md" if name == "README.md" else name
        assert (existing / installed).read_bytes() == (source / name).read_bytes()
    assert (existing / "README.md").read_text() == "# Application\n\nKeep application instructions.\n"
    assert not validator._validate_markdown_file(existing, existing, existing / "PROTOCOL_GUIDE.md")
    adoption.append({"case": "existing README delivered preflight/copy snippets", "exit_code": 0, "mapping_and_preservation": "PASS"})
    blocked = sandbox / "normative collision"
    blocked.mkdir()
    (blocked / "BOOTSTRAP.md").write_text("Existing authority\n")
    before = p.manifest(blocked)
    result = adoption_command(shell_blocks[0], blocked)
    assert result.returncode == 1 and p.manifest(blocked) == before
    adoption.append({"case": "normative collision aborts before copying", "exit_code": 1, "unchanged": True})
    for case in ("fresh", "regular collision", "dangling symlink collision", "directory collision"):
        dest = sandbox / case
        shutil.copytree(source, dest)
        bridge = dest / "AGENTS.md"
        if case == "regular collision":
            bridge.write_bytes(b"# Existing instructions\n\nPreserve this exact text.\n")
        elif case == "dangling symlink collision":
            bridge.symlink_to("nonexistent-destination")
        elif case == "directory collision":
            bridge.mkdir()
        result = subprocess.run(["sh", "-c", script], cwd=source,
                                env=dict(os.environ, repository_target=str(dest)),
                                capture_output=True, text=True, timeout=10)
        assert result.returncode == 0
        if case == "fresh":
            for name in ("AGENTS.md", "CLAUDE.md"):
                assert (dest / name).read_bytes() == (p.FIXTURE / name).read_bytes()
                assert not validator._validate_markdown_file(dest, dest, dest / name)
        elif case == "regular collision":
            assert bridge.read_bytes() == b"# Existing instructions\n\nPreserve this exact text.\n"
        elif case == "dangling symlink collision":
            assert bridge.is_symlink() and not bridge.exists()
            assert os.readlink(bridge) == "nonexistent-destination"
        else:
            assert bridge.is_dir() and not list(bridge.iterdir())
        assert (dest / "CLAUDE.md").read_bytes() == (p.FIXTURE / "CLAUDE.md").read_bytes()
        installation.append({"case": case, "exit_code": result.returncode,
                             "collision_reported": "collision:" in result.stderr,
                             "preservation_checks": "PASS"})

spec = (target / "PROJECT_SPEC.md").read_text()
contract = json.loads(spec.split("<!-- AEP-AUTHORIZED-MILESTONES-V1:BEGIN -->", 1)[1].split("```json", 1)[1].split("```", 1)[0])
milestone = next(m for m in contract["milestones"] if m["id"] == "MILESTONE-20260918T064510Z-prompt-independent-discovery-v1")
changed = git("diff", "--name-only", base, revision).decode().splitlines()
assert all(any(n == a or (a.endswith("/") and n.startswith(a)) for a in milestone["allowed_paths"]) for n in changed)
assert git("rev-parse", revision + "^").decode().strip() == base
post_target = git("diff", "--name-only", revision, recovery).decode().splitlines()
assert set(post_target) == {
    "HANDOFF.md", milestone["issue"],
    "EVIDENCE/EVIDENCE-20260922T012257Z-milestone-20260918t064510z-prompt-independent-discovery-v1-attempt-2.json"}
historical = git("ls-tree", "-r", "--name-only", base, "EVIDENCE/discovery-conformance").decode().splitlines()
assert len(historical) == 57
for path in historical:
    assert git("show", base + ":" + path) == (target / path).read_bytes()
original_evidence = "EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md"
assert (target / original_evidence).read_bytes().startswith(git("show", base + ":" + original_evidence))
assert not git("diff", "--name-only", base, revision, "PROJECT_SPEC.md", "ADR", "ROLE_CONTRACTS.md", "scripts", "ROTATION_PARTICIPANTS.json", "ROTATION_LOG.jsonl")
symlinks = [str(f.relative_to(target)) for f in target.rglob("*") if f.is_symlink()]
assert not symlinks
markdown = sorted(target.rglob("*.md"))
findings = [f.render() for path in markdown for f in validator._validate_markdown_file(target, target, path)]
assert not findings, findings

rows = []
for path in sorted((target / "EVIDENCE/discovery-conformance").glob("attempt-2-*/*.json")):
    record = json.loads(path.read_text())
    case = p.CASES[record["case"]]
    with tempfile.TemporaryDirectory() as directory:
        dest = Path(directory) / "repo"
        if case.nested:
            dest.mkdir()
        else:
            shutil.copytree(p.FIXTURE, dest)
        case.transform(dest)
        assert p.manifest(dest) == record["pre_run_manifest"], path
    assert record["prompt"] == (case.prompt or p._manual_onboarding_prompt()), path
    assert record["stdout_line_count"] == len(record["raw_stdout_lines"]), path
    extracted = (p.extract_claude_events if record["harness"] == "claude" else p.extract_codex_events)(record["raw_stdout_lines"])
    assert extracted["result"] == record["session_result"], path
    frozen_raw = p.classify(case, record["pre_run_manifest"], record["post_run_manifest"],
                            extracted["tool_events"], record["exit_code"], extracted["result"], record["harness"])
    frozen_stored = p.classify(case, record["pre_run_manifest"], record["post_run_manifest"],
                               record["tool_events"], record["exit_code"], record["session_result"], record["harness"])
    rows.append({"record": str(path.relative_to(target)), "record_sha256": digest(path),
                 "launch_classification": record["evaluation"]["classification"],
                 "frozen_from_raw": frozen_raw["classification"],
                 "frozen_from_stored_events": frozen_stored["classification"],
                 "raw_extraction_equals_stored": extracted["tool_events"] == record["tool_events"],
                 "fixture_manifest_and_prompt_match": True,
                 "model": record.get("model"), "exit_code": record["exit_code"],
                 "raw_line_count": len(record["raw_stdout_lines"]),
                 "manifest_diff": p.manifest_diff(record["pre_run_manifest"], record["post_run_manifest"])})
assert len(rows) == 34
print(json.dumps({"target": revision, "base": base, "recovery": recovery,
                  "oracle_sha256": digest(target / "tests/probe_discovery.py"),
                  "package_inventory": inventory, "verbatim_fixture_files": faithful,
                  "bridge_sha256": {name: digest(p.FIXTURE / name) for name in ("AGENTS.md", "CLAUDE.md")},
                  "installations": installation, "changed_path_count": len(changed),
                  "adoption_snippets": adoption,
                  "all_changed_paths_allowed": True, "post_target_record_only_paths": post_target,
                  "historical_raw_records_unchanged": len(historical),
                  "protected_authority_and_machinery_unchanged": True,
                  "markdown_files_checked": len(markdown), "markdown_findings": findings,
                  "target_symlinks": symlinks,
                  "launch_counts": dict(Counter(r["launch_classification"] for r in rows)),
                  "frozen_counts": dict(Counter(r["frozen_from_raw"] for r in rows)),
                  "records": rows}, indent=2, ensure_ascii=False))
