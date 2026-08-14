# Host Capability Probe

## Metadata

- **ID:** `EVIDENCE-20260814T092504Z-host-capability-probe`
- **Title:** Establish the host programmatic launch capability boundary from live probes before authorizing participant rotation
- **Captured UTC:** `2026-08-14T09:25:04Z`
- **Recorded by:** `ClaudeCode/root`
- **Claim supported or challenged:** The current host exposes a genuine, durable programmatic agent-launch interface (Claude Code CLI `claude -p` headless sessions at version `2.1.118`) with machine-readable result envelopes, budget caps, budget-exhaustion signaling distinguishable from authority gaps, and resumable session identity; no `paseo` binary or project exists on this host.
- **Related requirements:** Root [`PROJECT_SPEC.md`](../PROJECT_SPEC.md), Automated role dispatch phase execution boundary and Host adapter and participant rotation phase
- **Related ADRs/issues:** [`ADR-20260814T092504Z-host-adapter-rotation`](../ADR/ADR-20260814T092504Z-host-adapter-rotation.md); [`ISSUE-20260814T092504Z-host-adapter-rotation`](../ISSUES/ISSUE-20260814T092504Z-host-adapter-rotation.md); [`ADR-20260814T051405Z-automated-role-dispatch`](../ADR/ADR-20260814T051405Z-automated-role-dispatch.md)
- **Repository revision/state:** Clean synchronized `cc19209ec5a95e769f80834ec614f1db95c4c690`; dispatcher emitting the terminal `ROLE none` decision after acceptance of both authorized milestones
- **Environment:** Darwin; Claude Code CLI `2.1.118` at `/opt/homebrew/bin/claude`; OAuth/subscription host (no API-key configuration probed)

## Method

- **Procedure:** Probe the host for the launch surfaces named in the owner direction, then run three minimal live headless sessions in an isolated scratch directory (`/tmp/aep-host-probe`, not part of the repository) with tools disabled and budget caps, capturing stdout JSON envelopes, stderr, and exit codes.
- **Exact commands/inputs:**
  1. Presence probe: `command -v paseo; command -v claude; ls ~/Projects; claude --version 2>&1`
  2. Launch probe: `cd /tmp/aep-host-probe && claude -p "Reply with exactly: PROBE_OK" --output-format json --tools "" --max-budget-usd 0.25`
  3. Budget-exhaustion probe: `claude -p "Write a long essay about the history of computing, at least 5000 words." --output-format json --tools "" --max-budget-usd 0.0001`
  4. Resume probe: `claude -p --resume 061ab4bb-3e5c-4706-af6e-a51e7d021706 "Reply with exactly: RESUME_OK" --output-format json --tools "" --max-budget-usd 0.25`
- **Exit status:** Presence probe: `paseo` not found (exit `1` from `command -v`), `claude` found, version `2.1.118`. Launch probe exit `0`. Budget probe exit `1`. Resume probe exit `0`. All three stderr captures were zero bytes.
- **Repeatability:** Re-run the four commands on the same host; JSON envelopes are per-run (session IDs, costs, durations vary) but `type`/`subtype`/`is_error` behavior is the claim being supported.

## Raw observations

- No `paseo` executable exists on `PATH`, and no `paseo` project exists under `~/Projects`. No Paseo/session API of any kind was verified; none may be assumed.
- Launch probe returned a single JSON envelope on stdout: `type: "result"`, `subtype: "success"`, `is_error: false`, `result: "PROBE_OK"`, `session_id: "061ab4bb-3e5c-4706-af6e-a51e7d021706"`, `total_cost_usd: 0.020788`, `terminal_reason: "completed"`, exit `0`.
- Budget-exhaustion probe returned `type: "result"`, `subtype: "error_max_budget_usd"`, `is_error: true`, `errors: ["Reached maximum budget ($0.0001)"]`, `total_cost_usd: 0.002623`, exit `1`. Quota/budget exhaustion is therefore machine-distinguishable from both success and from any authority gap.
- Resume probe against the first session's `session_id` returned `subtype: "success"`, `result: "RESUME_OK"`, the **same** `session_id` (`061ab4bb-3e5c-4706-af6e-a51e7d021706`), exit `0`. Session identity is durable and addressable across invocations.
- `--tools ""` restricted the launched session to a text-only reply; `--max-budget-usd` bounded spend; both flags behaved as documented in `claude --help`.

## Capability interpretation

- **CONFIRMED:** The host can launch a complete agent session programmatically with a structured result envelope, exit-code signaling, per-session identity, and spend caps. This is a genuine durable launch interface, so the accepted dispatch ADR's "manual adapter in v1" boundary has a real implementable successor.
- **CONFIRMED:** Budget/quota exhaustion is a distinct, machine-readable participant-failure class (`error_max_budget_usd`, exit `1`, `is_error: true`) and must never be mapped to `BLOCKED_HUMAN_AUTHORITY`.
- **CONFIRMED:** Sessions are resumable by ID, supporting interruption recovery patterns where a participant session must be re-entered.
- **INFERRED:** A root-only adapter driving this CLI with the dispatcher's emitted decision satisfies the owner direction without any assumed API. Facts: launch, envelope, failure signal, and resume are probed; the dispatcher emits machine-readable decisions; the registry/ledger design requires only files.
- **UNKNOWN:** Rate limits, concurrency behavior, long-running session stability, nested-invocation constraints, behavior under revoked/expired host authentication, and portability to any other host or CLI version. These remain outside the authorized slice and must not be relied upon.

## Limitations and residual uncertainty

- Probes ran three minimal sessions on one host with one CLI version (`2.1.118`); envelope shape is a host behavior observation, not a stability guarantee across upgrades. An adapter must fail closed on unrecognized envelope shapes.
- OAuth/subscription authentication was ambient; probe results do not establish behavior under other authentication modes.
- Probe sessions ran with `--tools ""`; tool-permission behavior of launched working sessions (for example permission prompts in headless mode) was not probed and must be handled conservatively by the adapter's failure taxonomy.
- Total probe spend was under $0.03.

## Integrity and provenance

- **Artifact location:** This file; raw envelopes retained during the session at `/tmp/aep-host-probe/probe-{success,budget,resume}.{json,err}` (scratch, not committed).
- **Provenance:** Captured live by `ClaudeCode/root` on `2026-08-14` between the dispatcher's terminal `ROLE none` observation and the specification-evolution recording for the rotation milestone.
