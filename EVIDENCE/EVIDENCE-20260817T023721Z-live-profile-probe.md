# Live Tool-Enabled Profile Probe

## Metadata

- **ID:** `EVIDENCE-20260817T023721Z-live-profile-probe`
- **Title:** Establish the minimal tool-enabled headless launch profile, including permission behavior, from live probes before the runner relies on it
- **Captured UTC:** `2026-08-17T02:37:21Z`
- **Recorded by:** `agent:ClaudeCode-live`
- **Claim supported or challenged:** On this host (Claude Code CLI `2.1.118`), the minimal profile that lets a headless launched participant perform the role contracts is `--tools "Read,Edit,Write,Bash"` with a matching `--allowedTools "Read,Edit,Write,Bash"` grant; headless permission denial is machine-readable (success-shaped envelope with a non-empty `permission_denials` array and absent work product), and the probed budget-exhaustion class is unchanged under the widened profile.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Live invocation and autonomy demonstration phase (`LIVE-001`–`LIVE-004`)
- **Related ADRs/issues:** [`ADR-20260817T021218Z-autonomy-end-state`](../ADR/ADR-20260817T021218Z-autonomy-end-state.md); [`ISSUE-20260817T021218Z-live-invocation`](../ISSUES/ISSUE-20260817T021218Z-live-invocation.md); [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md)
- **Repository revision/state:** Attempt-1 `IN_PROGRESS` chain on milestone 4; original probe record [`EVIDENCE-20260814T092504Z-host-capability-probe`](EVIDENCE-20260814T092504Z-host-capability-probe.md) remains the boundary for everything not re-probed here
- **Environment:** Darwin; Claude Code CLI `2.1.118` at `/opt/homebrew/bin/claude`; OAuth/subscription host (no API-key configuration probed)

## Method

- **Procedure:** Run five minimal live headless sessions in an isolated scratch directory (`/tmp/aep-live-probe`, not part of the repository) with a two-line fixture file, budget caps on every launch, capturing stdout JSON envelopes, stderr, exit codes, and on-disk side effects. No probe touched repository state.
- **Exact commands/inputs:**
  1. Flag surface probe (no quota): `claude --version`; `claude --help` (permission-related flags enumerated: `--allowedTools`, `--disallowedTools`, `--permission-mode`, `--dangerously-skip-permissions`, `--tools`).
  2. Read probe, no grant: `claude -p "Read the file fixture.txt in the current directory and reply with its exact contents and nothing else." --output-format json --tools "Read,Edit,Write,Bash" --max-budget-usd 0.25`
  3. Edit+shell probe, no grant: `claude -p "Do exactly these three steps: 1) Use the Edit tool to change LINE_TWO to LINE_TWO_EDITED in fixture.txt. 2) Use the Bash tool to run: wc -l fixture.txt. 3) Reply with exactly: EDIT_DONE and the wc output." --output-format json --tools "Read,Edit,Write,Bash" --max-budget-usd 0.25`
  4. Edit+shell probe, explicit grant: same prompt with `--allowedTools "Read,Edit,Write,Bash"` added.
  5. Write probe, explicit grant: `claude -p "Use the Write tool to create a new file named created.txt containing exactly: CREATED_BY_PROBE. Then reply with exactly: WRITE_DONE." --output-format json --tools "Read,Edit,Write,Bash" --allowedTools "Read,Edit,Write,Bash" --max-budget-usd 0.25`
  6. Budget probe, widened profile: `claude -p "Write a long essay about the history of computing, at least 5000 words." --output-format json --tools "Read,Edit,Write,Bash" --allowedTools "Read,Edit,Write,Bash" --max-budget-usd 0.0001`
- **Exit status:** Flag probe: version `2.1.118`. Read probe exit `0`. Edit+shell without grant exit `0` (work product absent). Edit+shell with grant exit `0`. Write probe exit `0`. Budget probe exit `1`. All stderr captures were zero bytes.
- **Repeatability:** Re-run the commands on the same host; envelope values (session IDs, costs, durations) vary per run, but `type`/`subtype`/`is_error`/`permission_denials` behavior and on-disk side effects are the claim being supported.

## Raw observations

- Read probe without any grant succeeded: `type: "result"`, `subtype: "success"`, `is_error: false`, `permission_denials: []`, result contained the exact fixture contents, exit `0`. Read-only operation was permitted ambiently on this host.
- Edit+shell probe without a grant returned a **success-shaped** envelope — `subtype: "success"`, `is_error: false`, exit `0` — but with `permission_denials: [{"tool_name": "Edit", "tool_input": {"file_path": "/private/tmp/aep-live-probe/fixture.txt", ...}}]` non-empty, the fixture **unchanged on disk**, and a prose result describing the blocked edit. Headless denial is silent at the exit/subtype level and machine-readable only through the `permission_denials` field.
- Edit+shell probe with `--allowedTools "Read,Edit,Write,Bash"` executed both tools: the fixture on disk became `LINE_TWO_EDITED`, the result contained `EDIT_DONE` and the `wc -l` output, `permission_denials: []`, `subtype: "success"`, exit `0`.
- Write probe with the same grant created `created.txt` on disk containing exactly `CREATED_BY_PROBE`; `permission_denials: []`, `subtype: "success"`, exit `0`.
- Budget probe under the widened profile returned `subtype: "error_max_budget_usd"`, `is_error: true`, `errors: ["Reached maximum budget ($0.0001)"]`, exit `1` — the originally probed quota class is unchanged with tools enabled.
- No interactive prompt appeared in any probe; headless mode denies rather than prompts when a grant is missing.

## Capability interpretation

- **CONFIRMED:** The minimal verified live profile is `--tools "Read,Edit,Write,Bash"` plus `--allowedTools "Read,Edit,Write,Bash"`: it covers the role contracts' read, edit, write-new-record, and shell (checks, Git, pipeline transitions) capabilities, includes no network tool, and requires no `--permission-mode` or `--dangerously-skip-permissions` flag.
- **CONFIRMED:** Headless permission denial is a distinct machine-readable participant-failure shape: `subtype: "success"`, `is_error: false`, exit `0`, non-empty `permission_denials`, work product absent. An adapter that checked only subtype/exit code would misread a denied launch as success; the runner must classify a non-empty `permission_denials` array as a participant failure (`permission_denied`) and must fail closed on a malformed `permission_denials` field.
- **CONFIRMED:** The budget-exhaustion class (`error_max_budget_usd`, `is_error: true`, exit `1`) behaves identically under the widened profile; the existing taxonomy's quota class remains valid.
- **CONFIRMED:** Ambient permission behavior is tool-dependent on this host (Read permitted without grant, Edit denied without grant), so the profile must grant explicitly rather than rely on ambient settings.
- **INFERRED:** Conforming the runner to this profile is a bounded change: add `allowed_tools` to the registry (schema `rotation-participants/v2`), pass `--allowedTools` when non-empty, and extend the envelope classifier with the denial shape. Facts: the launcher is flag-driven and stub-injectable; the new envelope field is probed; the taxonomy already fails closed on unrecognized shapes.
- **UNKNOWN:** Rate limits, concurrency behavior, long-running session stability, envelope stability across CLI versions, behavior under other authentication modes, and any tool outside the four probed (including all network tools). These remain prohibited and fail closed.

## Limitations and residual uncertainty

- Probes ran five minimal sessions on one host with one CLI version (`2.1.118`); the profile is a host behavior observation, not a stability guarantee across upgrades. The runner must fail closed on unrecognized envelope shapes.
- Ambient host settings participated in the no-grant probes; behavior on a host with different settings may differ, and only the explicit-grant profile is relied upon.
- Multi-turn long-running sessions, `--resume` under the widened profile, and denied-Bash denial shapes were not probed; anything outside the recorded observations stays unverified.
- Total probe spend was under $0.15.

## Integrity and provenance

- **Artifact location:** This file; raw envelopes retained during the session at `/tmp/aep-live-probe/probe-{deny,edit-nogrant,edit-grant,write-grant,budget}.{json,err}` (scratch, not committed).
- **Provenance:** Captured live by `agent:ClaudeCode-live` on `2026-08-17` during milestone-4 attempt 1 (`IN_PROGRESS`, implementor `agent:ClaudeCode-live`), after the `IN_PROGRESS` transition and before any runner reliance on the widened profile.
