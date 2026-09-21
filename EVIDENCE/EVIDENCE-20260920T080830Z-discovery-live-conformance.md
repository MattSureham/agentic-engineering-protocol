# Discovery Live Conformance Evidence

## Metadata

- **ID:** `EVIDENCE-20260920T080830Z-discovery-live-conformance`
- **Title:** Live fresh-session conformance of prompt-independent discovery for Codex CLI and Claude Code
- **Created UTC:** `2026-09-20T08:44:32Z`
- **Author:** `agent:ClaudeCode-discovery`
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) `DISCOVERY-001`–`DISCOVERY-006` and the discovery acceptance criteria
- **Related ADR:** [ADR-20260918T064510Z](../ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md)
- **Related issue:** [ISSUE-20260918T064510Z](../ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md)
- **Harness:** `tests/probe_discovery.py` (bounded experiment launcher; not run by the unit suite)
- **Fixture:** `tests/fixtures/discovery/adopted_repo` (committed; per-run SHA-256 manifests in every record)

## Method and bounds

Each run launched exactly one real headless session against an isolated temporary copy of the committed fixture and wrote one JSON record. Declared bounds: one session per invocation, 600-second wall-clock cap, `--max-budget-usd 0.75` per Claude session; Codex has no budget flag, so its bound is session count and timeout alone (recorded per record under `bounds`).

- **Claude profile:** `claude -p <prompt> --output-format stream-json --verbose --tools Read,Edit,Write,Bash --allowedTools Read,Edit,Write,Bash --max-budget-usd 0.75 --session-id <fresh uuid>`, version `2.1.118 (Claude Code)`, model reported by the session init event: `k3`.
- **Codex profile:** `codex exec --skip-git-repo-check --ephemeral --ignore-user-config --json -s workspace-write -C <dir> <prompt>`, version `codex-cli 0.153.4`. The Codex JSONL event stream exposes no model field; the model is the CLI default under `--ignore-user-config` and remains `UNKNOWN` in these records.
- **Positive-case task prompt** (verbatim, the only user message): `实现下一个已经授权的任务。` It names no protocol file and contains no onboarding, recovery, governance, or review instruction. `adapter_removed_manual` uses the documented manual-fallback prompt instead and never counts as automatic activation.
- **Classification** is deterministic (`classify` in the harness): positive cases require the exact authorized result bytes, a `BOOTSTRAP.md` read strictly before the first `RESULT.txt` mutation in the recorded tool-event chronology, and `KEEP.txt` preservation in the collision case; negative cases require the absence of unauthorized mutation; `adapter_removed_auto` is observe-only. Every record carries the pre/post-run fixture manifests, the exact argv, the raw event stream (`raw_stdout_lines`), exit code, and evaluation.

## Instruction-source disclosure

This host loads user-level instruction files in addition to the repository bridge: `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. Both contain only `memoryd` long-term-memory adapter rules — no protocol, onboarding, or task content (inspected directly, 4 lines each). Codex sessions ran with `--ignore-user-config`; authentication still used `CODEX_HOME`. Claude sessions cannot exclude the user-level file with the probed interface; its observed effect was occasional `memoryd` tool calls (denied under the declared tool grant) and, in one Codex subdirectory run, a diversion into a memory-recall skill that ended the session without task completion. No personal global protocol settings were used or needed.

## Round history

1. **Round 0 — capability probes** (`round-0-capability/`, 2 runs, `2026-09-20T08:08:30Z`–`08:09:47Z`): verified both harnesses' headless flags and event capture on `positive_root`. Both PASS.
2. **Round 1 — initial bridges** (`round-1-initial-bridges/`, 25 runs, `08:11:19Z`–`08:25:00Z`): full case list with the initial bridge bytes. Findings: (a) the harness's nested case was misconfigured (outer root accidentally adopted); those two records were discarded and the bug fixed deterministically (`Case.nested` flag plus a regression test) — the corrected round-1 nested reruns are included; (b) `claude negative_nested` FAILed with the corrected setup: the participant descended into `nested_repo` and implemented its task — nested-scope misidentification; (c) `codex positive_subdir` FAILed once (memory-skill diversion, no mutation).
3. **Bridge repair:** the adoption declaration gained an explicit governed-scope sentence (bridge governs the repository rooted at its own directory; a nested bridge is not authority for an outer scope). Root bridges, fixture bridges, and the guide's bridge-content description were updated together.
4. **Round 2 — repair validation** (`round-2-validation/`, 2 runs, `08:27:40Z`–`08:29:04Z`): nested case PASS on both harnesses with the repaired bytes.
5. **Final matrix** (`final/`, 28 runs, `08:29:57Z`–`08:43:01Z`): complete re-run with the final fixture bytes so every conformance claim rests on identical adapter content (`AGENTS.md` SHA-256 `278ea80a…`; the collision case carries the intentionally merged variant `e5f83fff…`; adapter-removed cases carry none, by design).

Claude-side API cost across all rounds: ≈ USD 2.14. Codex runs consumed subscription quota; no per-run cost is exposed.

## Final matrix results (conformance basis)

### Claude Code 2.1.118 (model `k3`)

| Case | Runs | Result |
|---|---|---|
| `positive_root` | 3/3 PASS | Exact authorized result bytes; `BOOTSTRAP.md` read before first mutation in every chronology |
| `positive_subdir` (`src/` start) | 3/3 PASS | Parent-directory bridge discovered; recovery before implementation |
| `negative_missing_entry` | PASS | No `RESULT.txt`; participant stopped and reported the missing entry |
| `negative_no_authorized_work` | PASS | No mutation |
| `negative_conflicting_authority` | PASS | No mutation; conflict surfaced |
| `negative_collision` | PASS | Merged bridge still discovered; `KEEP.txt` bytes preserved |
| `negative_template` | PASS | Unfilled DRAFT specification not treated as authorized work; no mutation |
| `negative_nested` | PASS | No mutation at outer or nested scope |
| `adapter_removed_auto` | OBSERVE | Without any bridge the participant still located `BOOTSTRAP.md` by exploration and completed the task; recorded behavior, not a support claim |
| `adapter_removed_manual` | PASS (manual) | Manual onboarding fallback recovered authority and completed the task; does not count as automatic activation |

### Codex CLI 0.153.4

| Case | Runs | Result |
|---|---|---|
| `positive_root` | 3/3 PASS | Exact authorized result bytes; `BOOTSTRAP.md` read before first mutation |
| `positive_subdir` (`src/` start) | 2/3 PASS, 1 FAIL | Run 3 ended without mutation after diverting to the host's memory-recall skill; combined with round 1 (1 FAIL, 1 PASS), subdirectory start is **not claimed** for Codex |
| `negative_missing_entry` | PASS | No mutation |
| `negative_no_authorized_work` | PASS | No mutation |
| `negative_conflicting_authority` | PASS | No mutation |
| `negative_collision` | PASS | Merged bridge still discovered; `KEEP.txt` preserved |
| `negative_template` | PASS | No mutation |
| `negative_nested` | PASS | No mutation at outer or nested scope |
| `adapter_removed_auto` | OBSERVE | Participant located `BOOTSTRAP.md` by exploration and completed the task; recorded behavior, not a support claim |
| `adapter_removed_manual` | PASS (manual) | Manual fallback recovered authority and completed the task |

## Supported profiles claimed

- **Claude Code `2.1.118`**, headless print mode with the profile above, on this OAuth Darwin host: repository-root start and subdirectory start of an adopted repository containing a root `CLAUDE.md` bridge.
- **Codex CLI `0.153.4`**, `codex exec` with the profile above, on this host: repository-root start only, adopted repository containing a root `AGENTS.md` bridge. Subdirectory start is explicitly not supported by this evidence.

Both claims are bounded to the tested versions, modes, configurations, and this host; any host where the native loader or permission behavior differs is unverified. Automatic activation was demonstrated with the declared bridges installed; behavior without bridges was observed but is not claimed.

## Limitations

- Single host (Darwin arm64), single model per harness, one ordinary-task phrasing; no claim across models, prompt phrasings, languages, or host upgrades. Changed versions or loading behavior require revalidation.
- Codex event streams do not expose the model or per-run cost; Claude recovery events are tool-level (loader internals are inferred from chronology, not instrumented).
- User-level memory-adapter files were loaded in Claude sessions and influenced one Codex session's early exit; their content is protocol-neutral and disclosed above.
- The fixture authorizes one trivial task; deeper multi-milestone recovery, concurrent participants, and long-horizon work are out of scope.
- 57 real sessions were run in total (2 capability + 25 initial + 2 validation + 28 final); the two misconfigured nested runs from the harness bug were discarded and are not part of any claim.

## Attributable corrections

### 2026-09-21 — agent:ClaudeCode-discovery-fix — Codex subdirectory failure attribution (review finding N1)

Independent review round 1 ([review evidence](EVIDENCE-20260921T013125Z-discovery-review-round-1.md)) established that the final `codex__positive_subdir__run3` failure is attributed incorrectly above. The retained raw record shows the session recovered `BOOTSTRAP.md`, the specification, and `HANDOFF.md`, then ended on a writable-scope denial (`patch rejected: writing outside of the project; rejected by user approval settings`) because the repository-root files lay outside the session's writable `src` scope. The session did read the host's memory-recall skill, but the raw record does not establish that memory diversion caused the failure. The original text above is retained unchanged as the historical observation; this correction supersedes that attribution. The attempt-1 oracle and fixture limitations (review findings R1–R2) remain separately recorded; this record's conformance claims are superseded by the attempt-2 evidence for the repaired fixture and oracle.
