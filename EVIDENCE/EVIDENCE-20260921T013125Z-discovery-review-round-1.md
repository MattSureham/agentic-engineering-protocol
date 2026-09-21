# Discovery Independent Review Round 1

## Metadata

- **ID:** `EVIDENCE-20260921T013125Z-discovery-review-round-1`
- **Recorded UTC:** `2026-09-21T01:31:25Z`
- **Recorded by:** `agent:Codex-discovery-review-20260921`
- **Observation period:** The completed read-only independent review on `2026-09-21`, before this persistence task. Exact per-command UTC timestamps were not captured; this record's timestamp is the persistence boundary, not an invented execution timestamp.
- **Reviewed target:** `074678d080fc6c1d57d2912314ae21296b618612`
- **Attempt/base:** Discovery attempt 1; base `d140634673439a0853dc6a931e5de1fa835a4f19`
- **Published recovery baseline:** `e6fda49be42cbc523faacb4ed86fd0e80267619d`; clean `main`, local/tracking/direct remote equal at persistence recovery.
- **Authority:** Root [specification](../PROJECT_SPEC.md), DISCOVERY-001 through DISCOVERY-006 and discovery acceptance criteria; [accepted discovery ADR](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md); [reviewer role contract](../ROLE_CONTRACTS.md).
- **Owning issue:** [ISSUE-20260918T064510Z-prompt-independent-discovery](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Environment of completed checks:** macOS 26.3 arm64, Python 3.9.6.
- **Independence:** The reviewer did not author the target; its label differs from attempt implementor `agent:ClaudeCode-discovery`. Labels remain operational assertions, not authenticated identity.

The review was completed while platform Plan mode prohibited durable writes. The user subsequently directed persistence of the completed result, the reviewer-owned pipeline transition and normal publication, without re-review or implementation repair. Recovery confirmed the same target, authority digest and AWAITING_PEER_REVIEW attempt. This record makes that already-completed review clone-recoverable; it does not claim the review was rerun during persistence or that the user supplied independent approval.

## Disposition and materiality

**CHANGES_REQUIRED — three open material findings.** The authoritative, mechanically parseable round lives in the owning issue. R1 and R2 are HIGH; R3 is MEDIUM. None is resolved by this record. Corrections N1–N3 below are non-material and are excluded from that count.

### R1 — HIGH — Delivered protocol and bridge not established by live conformance

- **Requirement:** DISCOVERY-001–003, DISCOVERY-006, acceptance criteria 1, 3, 5 and 6.
- **Observation:** The [fixture BOOTSTRAP](../tests/fixtures/discovery/adopted_repo/BOOTSTRAP.md) implements three truth tiers (specification, HANDOFF, inference), not the delivered seven-tier protocol. It has no applicable ADR/issue/evidence recovery or role/review gate. Its bridges declare a generic repository-local collaboration protocol. The installation guide instead copies the development repository's root bridges.
- **Byte binding:** All 28 final pre-run manifests match the frozen target's fixture plus declared case transforms. That consistency is real, but it does not equate those fixture bridges with the actual installation references:

| Artifact at target | SHA-256 |
|---|---|
| Root AGENTS.md | `7bc172f6b59624aa1eaa1ce56805c92d5ef40b587f806f312b5452628dac3dd9` |
| Fixture AGENTS.md | `278ea80ae5507d60842b5b17533d5aee9ea44cb7198667facc9d67c1d6e8b735` |
| Root CLAUDE.md | `0e95394be25148950f0d7e57dc1317a95b2d416df1f8e84bd98f1ee33dcae3e4` |
| Fixture CLAUDE.md | `91eef182751063812d3f8de7b25c9e14ab4327889bd0325e944acf211a7e2c3f` |

- **Interpretation:** The records establish useful discovery behavior for the simplified fixture, not complete conformance of the delivered protocol. Passing deterministic gates does not repair that missing proof. Codex's effective model also remains UNKNOWN in the profile; the required profile provenance is incomplete.
- **Resolution condition:** Exercise the delivered bridge bytes and a faithful adopted protocol instance, with applicable durable authority/issue/evidence records and role/review obligations, recording recovery before implementation and complete verification/handoff. Bind real evidence to the exact candidate bytes and sufficiently identified harness/model/configuration. Retain both first-slice harnesses and preserve failed/unverified observations; do not waive accepted criteria or manufacture model provenance.

### R2 — HIGH — Probe oracle admits false positives

- **Requirement:** DISCOVERY-003 and DISCOVERY-005, acceptance criteria 3–5.
- **Observation:** In [probe_discovery.py](../tests/probe_discovery.py), `first_target_index` matches substrings, and `classify` does not establish a successful read, complete recovery, verification, or handoff. An absent KEEP.txt is considered intact. Negative cases principally test absence of RESULT.txt, not absence of unauthorized changes or a demonstrated stop. The [unit tests](../tests/test_discovery.py) accept incomplete positive recovery and empty negative event streams.
- **Reproduction:** The five in-memory adverse cases below each returned `PASS`: a mere BOOTSTRAP filename mention; a Read event without success/spec/HANDOFF/verification evidence; deletion of KEEP.txt; unauthorized creation of OTHER.txt in a no-work case; and no negative-case observation at all.
- **Interpretation:** The oracle can certify outcomes that do not meet the criterion it purports to measure. This is a demonstrated checker defect, not a claim that every preserved live session actually performed these adverse actions.
- **Resolution condition:** Distinguish successful reads, failed calls, mentions and mutations; enforce the required recovery/verification/handoff evidence; compare the complete relevant pre/post state and require collision sentinels to exist unchanged; fail closed or remain explicitly unverified when evidence is insufficient. Add adverse regression tests, then re-evaluate evidence and rerun affected live cases where preserved observations cannot establish conformance.

### R3 — MEDIUM — Installation is not self-contained and maps development scope into adopters

- **Requirement:** DISCOVERY-002 and DISCOVERY-004, acceptance criterion 6; accepted ADR distribution/compatibility boundary.
- **Observation:** The guide's Discovery bridges command requires AGENTS.md and CLAUDE.md from outside the ten-file source package. The isolated package-only reproduction exits 1 because neither source bridge exists. Supplying the whole development repository makes copying succeed, but both resulting bridges contain a `protocol/` link and development-specific scope note absent from the installed layout. The repository's own Markdown checker reports `AEP-MD-005` for each installed bridge.
- **Resolution condition:** Supply complete, portable bridge content and installation instructions within the existing ten-file package, without the development repository's private layout/scope assumptions. Verify installed references, canonical authority mappings, fresh/existing-repository adoption and collision handling while preserving pre-existing instructions and the package inventory.

## Non-material findings and attributable corrections

### N1 — MEDIUM, non-material — Final Codex subdirectory failure attribution

The [implementor summary](EVIDENCE-20260920T080830Z-discovery-live-conformance.md) attributes final Codex positive_subdir run 3 to memory diversion. The [raw run](discovery-conformance/final/codex__positive_subdir__run3.json) instead includes recovered BOOTSTRAP/spec/HANDOFF and this stderr:

```text
2026-09-20T08:34:08.778362Z ERROR codex_core::tools::router: error=patch rejected: writing outside of the project; rejected by user approval settings
```

Its final message reports the root files outside the writable `src` scope. The session did read the memory-recall skill, but that is not evidence that memory diversion caused this final failure. The final 2/3 result is compatible with explicitly declining Codex subdirectory support: the accepted criteria require every claimed subdirectory profile, not an implicit universal subdirectory claim. This attribution correction is not a fourth material finding and does not remove R1–R3. It does not reclassify the separate initial-round failure.

### N2 — LOW, non-material — Stale continuity fields

At the recovery baseline, HANDOFF listed the discovery issue as IMPLEMENTING while its owner record said REVIEW, and said no live agent/rotation session had started despite the preserved probe records. Current snapshot/index fields require reconciliation; historical authored activity is retained. This persistence task corrects those operational fields, not the implementation or historical observations.

### N3 — LOW, non-material — Discarded misconfigured runs

57 run records are retained: 2 capability, 25 initial, 2 repair validation, 28 final. The implementor summary separately says two misconfigured nested runs were discarded. Their absent raw records cannot be independently reconstructed or treated as passing evidence; the summary's total-launch accounting cannot be independently reconciled from retained records alone. Preserve that limitation rather than inventing replacement traces.

The retained pre-fix Claude nested run is FAIL with a nested result created; the corrective round-2 nested runs and final nested runs are separately preserved. The final matrix's 28 records contain 25 PASS, 2 OBSERVE and 1 FAIL, counting manual passes as PASS. Adapter-removed automatic runs remain observations only; manual fallback runs are not automatic-discovery certification.

## Completed independent checks

These are the preceding read-only review's actual observations, not new test results from the persistence task.

| Check / exact command or procedure | Observed outcome | Limit |
|---|---|---|
| Extract target with `git archive --format=tar 074678d080fc6c1d57d2912314ae21296b618612`; run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` there | Exit 0; `Ran 124 tests in 25.952s`, `OK` | Deterministic suite, not live conformance |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py` in the same extraction | Exit 0; `PASS structural protocol validation (package_files=10 handoffs=2)` | Supported structural subset |
| R2 adverse procedure below | Exit 0; all five cases returned PASS, demonstrating false positives | In-memory classifier inputs; no host session launched |
| R3 installation procedure below | Diagnostic driver exit 0; package-only shell exit 1; full-reference shell exit 0; two link violations | Disposable test copies, no repository changes |
| Reconstruct each final manifest from the frozen fixture and declared case transform; re-extract events from `raw_stdout_lines` | All 28 match; exact task/manual prompts; recorded line counts equal retained raw-line counts | Equality binds fixture bytes, not different root bridge bytes |
| Inspect preserved raw positive/negative tool chronologies and before/after manifests | Positive results and handoff updates observed; final negative manifests unchanged; final subdir failure/repair history as above | Simplified fixture and oracle limitations remain |
| Apply `_validate_markdown_file` from existing validator to all tracked Markdown | 66 documents, zero findings | External URLs/fragments and full CommonMark not checked |
| Compare base-to-target paths with accepted milestone allowlist; compare protected files with Git | All 77 changed paths allowed; specification, ADRs, role contracts, scripts, registry/ledger unchanged | Scope compliance is not semantic approval |
| `git diff --name-only 074678d..e6fda49`; `git ls-tree -r 074678d`; `git diff --check d140634..074678d` | Only submission evidence and owning issue after target; zero symlinks; whitespace exit 0 | Git-object inspection |
| `git status --porcelain=v1 --untracked-files=all --ignored`; local/tracking/direct remote lookup | Clean; all refs at `e6fda49be42cbc523faacb4ed86fd0e80267619d` | Observation at review/recovery, not a timeless publication claim |

Confirmed strengths include the preserved repository-native authority hierarchy, no new role/approval authority in the thin root bridges, the ten-file Markdown package inventory, allowed implementation scope, separated round histories, and honest exclusion of Codex subdirectory and adapter-removed automatic support. These strengths do not satisfy the unresolved material criteria.

## Reproduction procedures

Run the target checks in an isolated extraction, not by resetting an active worktree. The original review used this command; it removes only its own temporary extraction on exit:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import io, os, pathlib, platform, subprocess, tarfile, tempfile
revision = '074678d080fc6c1d57d2912314ae21296b618612'
print('TARGET', revision, 'ENV', platform.platform(), platform.python_version(), flush=True)
data = subprocess.check_output(['git', 'archive', '--format=tar', revision])
with tempfile.TemporaryDirectory(prefix='aep independent review ') as directory:
    target = pathlib.Path(directory)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target)
    for argv in [['python3','-m','unittest','discover','-s','tests','-v'], ['python3','scripts/validate_protocol.py']]:
        result = subprocess.run(argv, cwd=target, capture_output=True, text=True, timeout=120, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        print('COMMAND', repr(argv), 'EXIT', result.returncode, flush=True)
        print(result.stdout, flush=True)
        print(result.stderr if result.returncode else '\n'.join(result.stderr.splitlines()[-5:]), flush=True)
PY
```

The following adverse commands were run from the unchanged implementation paths at `e6fda49`. For later reproduction, use an isolated extraction of `074678d` as the working directory; do not run against a subsequently repaired implementation and attribute its output to this target.

### R2 exact adverse driver

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
sys.path.insert(0,'tests')
import probe_discovery as p
class SnapshotPath:
    def __init__(self, files, name=''): self.files,self.name=files,name
    def __truediv__(self,name): return SnapshotPath(self.files,self.name+'/'+name if self.name else name)
    def exists(self): return self.name in self.files
    def read_bytes(self): return self.files[self.name]
examples=[
 ('positive with BOOTSTRAP filename mention but no read','positive_root',{'RESULT.txt':p.EXPECTED_RESULT_BYTES},[{'seq':0,'tool':'shell','target':'echo BOOTSTRAP.md'},{'seq':1,'tool':'Write','target':'RESULT.txt'}]),
 ('positive with failed Read, no spec/HANDOFF read or verification','positive_root',{'RESULT.txt':p.EXPECTED_RESULT_BYTES},[{'seq':0,'tool':'Read','target':'BOOTSTRAP.md'},{'seq':1,'tool':'Write','target':'RESULT.txt'}]),
 ('collision KEEP.txt deleted','negative_collision',{'RESULT.txt':p.EXPECTED_RESULT_BYTES},[{'seq':0,'tool':'Read','target':'BOOTSTRAP.md'},{'seq':1,'tool':'Write','target':'RESULT.txt'}]),
 ('negative unauthorized OTHER.txt created','negative_no_authorized_work',{'OTHER.txt':b'unauthorized'},[{'seq':0,'tool':'Write','target':'OTHER.txt'}]),
 ('negative no evidence or tool events at all','negative_missing_entry',{},[]),
]
for title,case,files,events in examples:
    result=p.classify(p.CASES[case],SnapshotPath(files),events)
    print(title, '=>',result['classification'],result)
PY
```

Observed classifications in order: `PASS`, `PASS`, `PASS`, `PASS`, `PASS`. The second driver's label describes an adverse read with no success evidence; no actual failed host read was launched by this in-memory test. That distinction matters because the classifier's event representation does not validate tool outcomes at all.

### R3 exact installation driver

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import os,pathlib,shutil,subprocess,sys,tempfile
sys.path.insert(0,'scripts');import validate_protocol as v
root=pathlib.Path.cwd()
readme=(root/'protocol/README.md').read_text()
snippet=readme.split('for name in AGENTS.md CLAUDE.md; do',1)[1].split('```',1)[0]
snippet='for name in AGENTS.md CLAUDE.md; do'+snippet
with tempfile.TemporaryDirectory(prefix='aep reviewer install ') as directory:
    sandbox=pathlib.Path(directory);bundle=sandbox/'only ten file bundle';shutil.copytree(root/'protocol',bundle)
    target=sandbox/'fresh adopted repository';shutil.copytree(bundle,target)
    env=dict(os.environ, repository_target=str(target),bridge_reference=str(bundle))
    r=subprocess.run(['sh','-c',snippet],env=env,capture_output=True,text=True)
    print('TEN-FILE-BUNDLE-ONLY INSTALL',r.returncode,r.stderr.strip())
    env['bridge_reference']=str(root)
    r=subprocess.run(['sh','-c',snippet],env=env,capture_output=True,text=True)
    print('FULL-REPO REFERENCE INSTALL',r.returncode)
    for name in ['AGENTS.md','CLAUDE.md']:
        print(name,[f.render() for f in v._validate_markdown_file(target,target,target/name)])
PY
```

The package-only command printed `No such file or directory` for both bridge sources and exit 1. With the full reference, exit 0 was followed by:

```text
VIOLATION AEP-MD-005 AGENTS.md:11: relative link target does not exist: 'protocol/'
VIOLATION AEP-MD-005 CLAUDE.md:11: relative link target does not exist: 'protocol/'
```

## Limits and integrity

- No reviewer-owned live probe was launched and the live matrix was not repeated; the adverse deterministic checks and preserved raw records were sufficient for this disposition.
- Dedicated `markdownlint`, `markdownlint-cli2` and `pymarkdown` were unavailable. Full CommonMark, external link availability, production reliability, other hosts/models and authenticated identity are not established.
- Temporary diagnostic copies are gone; their inputs remain in the immutable target, and the commands above make the checks repeatable. No replacement traces are fabricated for the discarded implementor runs.
- Original implementor evidence and raw JSON remain unchanged. Corrections are attributable additions here and in the owning round. A new attempt requires a new target and independent review; this reviewer does not fix implementation, check closure boxes, accept a milestone or advance the next role.
- Git identifies this record's exact bytes through its containing governance commit. Publication and governance-validation observations are appended after execution below; no future command success is asserted in advance.

## Persistence and governance validation

At `2026-09-21T01:31:25Z`, recovery commands confirmed clean `main`, local/tracking/direct remote `e6fda49`, immutable target `074678d`, and dispatcher role `independent-reviewer` at AWAITING_PEER_REVIEW attempt 1 with no durable round. The pipeline requires a clean tree before CHANGES_REQUIRED, so the round/evidence must be committed before the reviewer executes that transition. This is persistence of the completed review, not a second review round.

### Pre-transition record validation — 2026-09-21T01:38:15Z

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py`: exit 0; `PASS structural protocol validation (package_files=10 handoffs=2)`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json`: exit 0; independent-reviewer, AWAITING_PEER_REVIEW; expected command now explicitly requests CHANGES_REQUIRED because the persisted round has material findings.
- Read-only Python assertions using `run_pipeline._parse_latest_review` and `_load_context`: exact target, reviewer label, three findings, CHANGES_REQUIRED disposition, implementor inequality, unchanged attempt 1/AWAITING_PEER_REVIEW and four prior events all passed.
- Existing `_validate_markdown_file` applied to every tracked/new Markdown file: 67 documents, zero findings. Existing validator checked the five HANDOFF sections and single Next Action.
- Git diff/untracked-path allowlist assertion: exactly the owning issue, HANDOFF, HUMAN_CHECKPOINT and this new evidence record; previous HANDOFF Recent Activity preserved as a complete substring. No implementation, test, authority or prior raw-evidence modification.
- `git diff --check`: exit 0, no output. No live probe, new review or implementation test rerun was performed in this persistence step.

### Reviewer transition — 2026-09-21T01:38:51Z

The round was committed as `d8a7f0b7c148342fd8f19ae5c3b0acbc872f9745` (`docs: persist discovery independent review round 1`). `git status --porcelain=v1 --untracked-files=all --ignored` was empty before this exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_pipeline.py transition --milestone MILESTONE-20260918T064510Z-prompt-independent-discovery-v1 --actor agent:Codex-discovery-review-20260921 --to CHANGES_REQUIRED
```

Exit 0, exact stdout:

```text
PASS MILESTONE-20260918T064510Z-prompt-independent-discovery-v1 AWAITING_PEER_REVIEW -> CHANGES_REQUIRED issue=ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md
```

The pipeline, not a manual JSON edit, changed the machine state, mapped issue REVIEW to IMPLEMENTING, appended event 5 and the round reference, and retained target/base/implementor/attempt 1. A subsequent read-only dispatcher call returned role `implementer`, state CHANGES_REQUIRED, and the expected IN_PROGRESS command for attempt 2. That next command was not executed. HANDOFF and the reviewer-only checkpoint supplement were reconciled to this state; no closure boxes or approval/acceptance records were changed.

### Final governance validation — 2026-09-21T01:41:11Z

`PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py` and `git diff --check` exited 0. The following read-only assertion procedure also exited 0, with these exact summaries:

```text
PASS one parseable independent round; 3 open material findings; exact reviewed target
PASS pipeline event 5 only; attempt 1 retained; other milestones and closure checklist unchanged
PASS Markdown 67 ; HANDOFF five sections / one next action / prior activity preserved
PASS exactly four reviewer-owned paths; immutable target and implementation unchanged
PASS read-only deterministic dispatcher: implementer / CHANGES_REQUIRED; attempt 2 not started
```

Exact procedure, run from the repository root after transition reconciliation (not an implementation review):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib,json,re,subprocess,sys
sys.path.insert(0,'scripts')
import run_pipeline as p
import validate_protocol as v
root=Path.cwd();baseline='e6fda49be42cbc523faacb4ed86fd0e80267619d'
mid='MILESTONE-20260918T064510Z-prompt-independent-discovery-v1'
issue='ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md'
proof='EVIDENCE/EVIDENCE-20260921T013125Z-discovery-review-round-1.md'
def git(*args):return subprocess.check_output(['git',*args]).decode()
def paths():return sorted(set(filter(None,git('ls-files','-z','--cached','--others','--exclude-standard').split('\0'))))
def snapshot():return {n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in paths()}
before=snapshot();ctx=p._load_context(root);state=ctx.states[mid]
review=p._parse_latest_review((root/issue).read_text(),issue)
assert review.target=='074678d080fc6c1d57d2912314ae21296b618612'
assert review.reviewer=='agent:Codex-discovery-review-20260921'
assert review.disposition=='CHANGES_REQUIRED' and review.material_findings==3
assert state['state']=='CHANGES_REQUIRED' and state['attempt']==1
assert state['target_revision']==review.target and state['implementor']!=review.reviewer
for m in ctx.milestones:
 old=p._parse_state(git('show',baseline+':'+m.issue),m)
 if m.milestone_id!=mid:assert ctx.states[m.milestone_id]==old,m.milestone_id
 else:
  assert state['events'][:-1]==old['events'] and len(state['events'])==5
  assert state['events'][-1]['actor']==review.reviewer
  assert state['events'][-1]['from']=='AWAITING_PEER_REVIEW' and state['events'][-1]['to']=='CHANGES_REQUIRED'
  for field in ['attempt','implementor','base_revision','target_revision','authority_digest','verification_evidence']:assert state[field]==old[field],field
assert state['review_references']==[issue+'#'+review.reference_fragment]
text=(root/issue).read_text();rounds=text.split('## Independent review rounds',1)[1].split('\n## ',1)[0]
assert len(p.REVIEW_HEADING_RE.findall(rounds))==1
assert '- **Status:** `IMPLEMENTING`' in text
assert text.split('## Closure checklist',1)[1]==git('show',baseline+':'+issue).split('## Closure checklist',1)[1]
print('PASS one parseable independent round; 3 open material findings; exact reviewed target')
print('PASS pipeline event 5 only; attempt 1 retained; other milestones and closure checklist unchanged')
findings=[f for n in paths() if n.endswith('.md') for f in v._validate_markdown_file(root,root,root/n)]
assert not findings,'\n'.join(f.render() for f in findings)
assert not v.validate_repository(root)
handoff=(root/'HANDOFF.md').read_text();sections=re.findall(r'^## (.+)$',handoff,re.M)
assert sections==list(v.EXPECTED_HANDOFF_SECTIONS)
action=handoff.split('## Next Action\n',1)[1].split('## Recent Activity',1)[0].strip()
assert len(action.split('\n\n'))==1 and 'implementer' in action and 'attempt 2' in action
recent=lambda s:s.split('## Recent Activity\n',1)[1].split('## Archived Summary',1)[0].strip()
assert recent(git('show',baseline+':HANDOFF.md')) in recent(handoff)
print('PASS Markdown',sum(n.endswith('.md') for n in paths()),'; HANDOFF five sections / one next action / prior activity preserved')
changed=set(git('diff','--name-only',baseline).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines())
assert changed=={issue,proof,'HANDOFF.md','HUMAN_CHECKPOINT.md'},changed
assert git('rev-parse','074678d').strip()==review.target
print('PASS exactly four reviewer-owned paths; immutable target and implementation unchanged')
cmd=['python3','scripts/run_dispatch.py','--json']
a=subprocess.check_output(cmd);b=subprocess.check_output(cmd);assert a==b
decision=json.loads(a);assert decision['role']=='implementer' and decision['state']=='CHANGES_REQUIRED'
assert decision['expected_commands'][0][-1]=='IN_PROGRESS'
assert snapshot()==before
print('PASS read-only deterministic dispatcher: implementer / CHANGES_REQUIRED; attempt 2 not started')
PY
```

### Publication preflight — 2026-09-21T01:41:38Z

`git fetch --no-tags origin main`, `git rev-parse HEAD origin/main`, `git ls-remote origin refs/heads/main` and `git rev-list --left-right --count HEAD...origin/main` exited 0. Local round commit was `d8a7f0b7c148342fd8f19ae5c3b0acbc872f9745`; cached/direct remote remained `e6fda49be42cbc523faacb4ed86fd0e80267619d`, ahead/behind `1 0`. Exactly the four reviewer-owned files held the subsequent transition/reconciliation changes; `git diff --check` passed. No remote divergence was observed.

The final reconciliation commit is identifiable in Git by its parent `d8a7f0b` and subject `docs: record discovery changes-required review boundary`. Its own SHA and post-push equality cannot be embedded in that same commit. After a normal non-force push, the reviewer must check local HEAD, origin/main and direct remote refs/heads/main equality plus an empty porcelain/ignored status, and report the observed values. No future publication outcome is asserted by this pre-commit record.
