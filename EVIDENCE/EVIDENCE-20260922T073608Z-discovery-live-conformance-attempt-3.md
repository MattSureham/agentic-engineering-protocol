# Discovery Live Conformance Evidence — Attempt 3

## Metadata

- **ID:** `EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3`
- **Title:** Live fresh-session conformance of prompt-independent discovery after round-2 CHANGES_REQUIRED fixes (attempt 3)
- **Created UTC:** `2026-09-22T07:36:08Z`
- **Author:** `agent:ClaudeCode-discovery-fix-3`
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `DISCOVERY-001`–`DISCOVERY-006` and the discovery acceptance criteria
- **Related ADR:** [ADR-20260918T064510Z](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md)
- **Related issue:** [ISSUE-20260918T064510Z](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Prior evidence:** [attempt-2 live conformance](EVIDENCE-20260921T110848Z-discovery-live-conformance-attempt-2.md) (plus its appended 2026-09-22 corrections), [independent review round 2](EVIDENCE-20260922T020117Z-discovery-review-round-2.md)
- **Harness:** `tests/probe_discovery.py`, schema `aep-discovery-probe/v3`, SHA-256 `e991d1488cc3e5811bf875310a39eef0ef4c514ae1ac68e0c8a6a8658f29ab1a` (bounded experiment launcher; not run by the unit suite)
- **Fixture:** `tests/fixtures/discovery/adopted_repo` (committed; regenerated against the round-2-fixed package bytes; per-run SHA-256 manifests in every record)

## Status of this evidence (read first)

Attempt 3 is **incomplete by owner decision**. On 2026-09-22 the human technical owner directed that all scheduled Codex live-probe/rerun launches be cancelled, that no new Codex CLI session start automatically after quota recovery, that all existing records (completed, `UNVERIFIED`, `FAIL`, quota-aborted) be preserved without deletion or overwriting reruns, and that any further Codex live runs required for acceptance first be documented as a minimal run set and wait for explicit owner authorization. The outstanding minimal Codex run set is recorded in [ISSUE-20260922T073608Z-codex-quota-authorization](../ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md) and in the decision queue of `HUMAN_CHECKPOINT.md`. No Codex support claim below covers the two outstanding cases.

## What changed since attempt 2 (round-2 material findings R1, R2, R4)

- **R1 (Codex profile provenance):** the harness now launches Codex with an explicit `--model gpt-6-astra` (slug selected from the host's `~/.codex/models_cache.json`, priority 1, `codex-cli 0.153.4`), records the flag in every record under `bounds.codex_model_flag`, and sets the record's `model` field from it. The event stream exposes no model field; the recorded argv is the inspectable provenance, and session completion establishes availability. Records also gained schema `aep-discovery-probe/v3` with `required_extra_reads`, `post_record_contents` (post-state contents of every changed protocol record file, 20 KB cap each), and output capture on read/shell events (60 KB cap; Codex `aggregated_output` and Claude tool-result text). The timeout handler now decodes bytes stdout/stderr (round-2 correction 3).
- **R2 (oracle soundness):** the classifier is rehardened fail-closed. Content reads count only through a strict whitelist (`cat`/`less`/`more`/`od -c|-x`/`cmp -s|-l`, validated `head`/`tail` line limits against known fixture line counts, `diff` with safe flags); `grep`/`rg`/`sed`/`awk`/`stat`/`file`/`wc`/`echo` never count. Recorded read output must contain the file's distinctive first and last content markers (first/last non-empty lines ≥ 8 chars of the known fixture text). Compound commands attribute conservatively (`&&` to all statements, pipelines to the last element only, `;`/`||` only with output markers). Post-state protocol records are structurally validated (`HANDOFF.md` five sections, issue ID/Status, checkpoint heading); missing contents are gaps (`UNVERIFIED`), structurally invalid contents are defects (`FAIL`). Negative and nested cases additionally require attributable stop evidence: a recorded final message plus at least one successful strict read, or — refined mid-attempt, disclosed here — a failed strict read of a required path genuinely absent from the pre-run manifest (probing the missing entry is direct observable engagement; manifest absence makes the failure unfabricatable). Specification-linked accepted ADRs present in the pre-run manifest become required recovery reads. All nine round-2 adverse false-positive classes are unit regressions, and the reviewer's 19-probe script classifies 0 PASS (11 FAIL, 8 UNVERIFIED) against this oracle.
- **R4 (Claude conflicting-authority and nested-scope failures):** product text strengthened within the accepted boundary. `protocol/BOOTSTRAP.md` (and the root development copy) now state that source precedence decides which claim governs once work proceeds but does not waive the conflict stop, and that a contradiction requires stopping the affected implementation until reconciled or escalated (conflict paragraph and start-or-resume step 8). Bridge rule 3 (`protocol/README.md` template, root `AGENTS.md`/`CLAUDE.md`, regenerated fixture bridges) now states the adoption governs only sessions whose working root lies inside the bridge's repository, and that a participant arriving from an unadopted outer root must stop and report rather than implement the nested repository's tasks.

Deterministic gates at freeze time: `python3 -m unittest discover -s tests` — 163 tests, OK; `python3 scripts/validate_protocol.py` — PASS (package_files=10, handoffs=2). Reviewer probe re-run: 19/19 non-PASS (see "Round-2 probe regression" below).

## Method and bounds

Unchanged from attempt 2: each run launched exactly one real headless session against an isolated temporary copy of the committed fixture and wrote one JSON record with pre/post SHA-256 manifests, exact argv, raw event stream, exit code, post-record contents, and evaluation. Declared bounds: one session per invocation, 600-second wall-clock cap, `--max-budget-usd 0.75` per Claude session; Codex bounded by session count and timeout alone, now additionally by the explicit model flag.

- **Claude profile:** `claude -p <prompt> --output-format stream-json --verbose --tools Read,Edit,Write,Bash --allowedTools Read,Edit,Write,Bash --max-budget-usd 0.75 --session-id <fresh uuid>`, version `2.1.118 (Claude Code)`, model reported by session init: `k3`.
- **Codex profile:** `codex exec --skip-git-repo-check --ephemeral --ignore-user-config --json --model gpt-6-astra -s workspace-write -C <dir> <prompt>`, version `codex-cli 0.153.4`.
- **Positive-case task prompt** (verbatim, the only user message): `实现下一个已经授权的任务。` `adapter_removed_manual` uses the delivered `protocol/PROMPTS.md` onboarding block and never counts as automatic activation.
- **Classification:** launch-time evaluations are preserved in each record unchanged. The conformance basis is the uniform re-evaluation of every retained record with the frozen oracle hashed above. Exactly one launch-time classification differs from the final re-evaluation: `claude negative_missing_entry run1` launched before the manifest-absent failed-probe refinement (`UNVERIFIED` → `PASS`). Raw events and manifests were never modified.

## Instruction-source disclosure

Identical to attempts 1–2: this host loads `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (protocol-neutral `memoryd` adapter rules only). Codex ran with `--ignore-user-config`; Claude sessions cannot exclude the user-level file with the probed interface. No personal global protocol settings were used or needed.

## Round history

1. **Matrix, round A** (`attempt-3-final/`, 16 Claude + 14 Codex runs, `2026-09-22T03:03:28Z`–`03:59Z` Claude, `06:50Z`–`07:22Z` Codex): complete case list on both harnesses against the fixed bytes. The first Codex launch window (7 records) hit the host account usage limit and is quarantined, not counted (see below).
2. **Positive reruns** (`attempt-3-final/`, 8 Claude + 4 Codex runs): positive cases rerun to reach three evaluated passing sessions each, capping at run 7 per case. Claude `positive_root` and `positive_subdir` settled at 3 PASS of 7 launched each; Codex `positive_root` settled at 3 PASS of 7. Codex `positive_subdir` was not rerun: its two FAILs repeat the attempt-2 writable-scope boundary, and subdirectory start remains unclaimed for Codex.
3. **Second Codex window exhaustion:** mid-rerun the account quota was exhausted again ("try again at 7:50 PM"), aborting `negative_collision` runs 2–3 and `adapter_removed_manual` runs 2–3. The owner then cancelled all further Codex launches; those cases remain at their single `UNVERIFIED` run each.

Claude-side API cost across attempt-3 rounds: ≈ USD 7.83. Codex runs consumed subscription quota; no per-run cost is exposed.

## Quota-aborted launches (preserved, excluded)

`attempt-3-quota-aborted/` (11 records + `NOTE.md`): every launch that failed on the host account usage limit (fast exit-1, usage-limit error in the raw stream), from both exhaustion windows. These records establish only that launches occurred and failed on quota; they are excluded from the matrix and from every support claim, and retained so no launched session is discarded.

## Final matrix results (uniform frozen-oracle re-evaluation, conformance basis)

### Claude Code `2.1.118` (model `k3`) — 24 records

| Case | Result | Notes |
|---|---|---|
| `positive_root` | 3 PASS of 7 launched (4 UNVERIFIED) | Every UNVERIFIED has the single gap "no successful post-mutation verification read of RESULT.txt recorded" |
| `positive_subdir` (`src/` start) | 3 PASS of 7 launched (4 UNVERIFIED) | Same single verification-read gap in every UNVERIFIED |
| `negative_missing_entry` | PASS | Stopped and reported per bridge rule 2; engagement established by the manifest-absent failed probe of `BOOTSTRAP.md` plus the attributable final message |
| `negative_no_authorized_work` | PASS | Protocol record maintenance only |
| `negative_conflicting_authority` | 2/2 PASS | Both runs now stop on the spec/HANDOFF contradiction instead of implementing (round-2 failure mode, 2/2 FAIL in attempt 2) |
| `negative_collision` | PASS | Pre-existing bridge content preserved; `KEEP.txt` intact; task completed |
| `negative_template` | PASS | DRAFT spec not treated as authorization |
| `negative_nested` | 2/2 PASS | Both runs stop at the unadopted outer root (round-2 failure mode, 2/2 FAIL in attempt 2) |
| `adapter_removed_manual` | PASS | Documented manual fallback recovered authority |
| `adapter_removed_auto` | OBSERVE | No bridges; ordinary prompt only; observed, not claimed |

### Codex CLI `0.153.4` (`--model gpt-6-astra`) — 18 records

| Case | Result | Notes |
|---|---|---|
| `positive_root` | 3 PASS of 7 launched (4 UNVERIFIED) | Every UNVERIFIED is the single verification-read gap |
| `positive_subdir` (`src/` start) | 1 UNVERIFIED, 2 FAIL | Both FAILs are writable-scope declines (no result, no record updates), repeating the attempt-2 environmental boundary. Subdirectory start is **not claimed** for Codex |
| `negative_missing_entry` | PASS | Stop evidence via manifest-absent failed probe plus final message |
| `negative_no_authorized_work` | PASS | Record maintenance only |
| `negative_conflicting_authority` | PASS | Conflict surfaced; no implementation |
| `negative_collision` | UNVERIFIED (1 run) | Sole gap: no recorded post-mutation verification read; otherwise conforming. **Coverage incomplete — awaiting owner-authorized rerun** |
| `negative_template` | PASS | DRAFT spec not treated as authorization |
| `negative_nested` | PASS | Stopped at the unadopted outer root |
| `adapter_removed_manual` | UNVERIFIED (1 run) | Sole gap: no recorded post-mutation verification read; otherwise conforming. **Coverage incomplete — awaiting owner-authorized rerun** |
| `adapter_removed_auto` | OBSERVE | Observed, not claimed |

## Reliability characterization (attempt 3)

- The hardened oracle exposes a real behavior split: participants that complete the task but never re-read `RESULT.txt` after writing it abstain `UNVERIFIED`. Observed verification rates: Claude 3/7 per positive case, Codex 3/7 on `positive_root`. Verification discipline, not discovery or recovery, is the variance.
- Claude `negative_conflicting_authority` and `negative_nested` moved from 2/2 FAIL (attempt 2) to 2/2 PASS each after the R4 wording changes — the round-2 systematic failures are not reproduced.
- Codex subdirectory behavior is unchanged from attempt 2 and remains outside the claimed profile.

## Round-2 probe regression

`EVIDENCE/discovery-review-round-2/reviewer_probes.py` re-run against this target (read-only; no live sessions): all 19 reviewer counterexamples classify non-PASS (11 FAIL, 8 UNVERIFIED, 0 PASS). The eight UNVERIFIED abstentions include the driver's own baseline, which passes no post-record contents and therefore cannot establish record validation — conservative abstention, not certification.

## Attempt-2 records under the final oracle

All 34 retained attempt-2 records were re-extracted from their raw streams and uniformly reclassified with the final oracle: [`attempt-2-reclassification-v3.json`](discovery-conformance/attempt-2-reclassification-v3.json). Attempt-2 records never retained post-record contents and only partially retained tool outputs, so 17 launch-PASS records downgrade to UNVERIFIED on unrecoverable evidence classes; the four systematic Claude negative failures remain FAIL; Codex `negative_missing_entry` and `negative_nested` remain PASS. Launch-time classifications are preserved in the records unchanged.

## Supported profiles claimed

- **Claude Code `2.1.118`** (model `k3`), root and subdirectory starts, on this host: all acceptance-criterion coverage passed — 3 evaluated PASS per positive case (of 7 launched each), every negative case PASS including 2/2 on both round-2 failure modes, manual fallback PASS, automatic-without-bridge recorded OBSERVE-only.
- **Codex CLI `0.153.4`** (`--model gpt-6-astra`), **repository-root start only**, on this host: 3/7 `positive_root` PASS, five negatives PASS, automatic-without-bridge OBSERVE-only. **`negative_collision` and `adapter_removed_manual` coverage is incomplete (UNVERIFIED, owner-paused reruns); the Codex profile claim is therefore not established by this attempt.** Subdirectory start is not claimed.

Both assessments are bounded to the tested versions, modes, configurations, and this host. Verification discipline limits are stated above; a support claim covers only what the recorded evidence establishes.

## Limitations

- Single host (Darwin arm64), one model per harness, one ordinary-task phrasing; no claim across models, phrasings, languages, or host upgrades.
- Codex event streams expose no model or per-run cost; profile provenance is the recorded argv (`--model gpt-6-astra`) plus session completion, which proves the requested profile was accepted and ran, not server-side routing internals.
- The oracle validates structure, chronology, content markers, and record shape — not the semantic quality of the participant's reasoning or its final message beyond presence.
- Codex account quota twice interrupted the matrix; quota-aborted launches are preserved separately and the owner has paused further Codex live runs pending explicit authorization of the documented minimal run set.
- User-level memory-adapter files were loaded in Claude sessions; their content is protocol-neutral and disclosed above.
- The fixture authorizes one trivial task; deeper multi-milestone recovery, concurrent participants, and long-horizon work are out of scope.
