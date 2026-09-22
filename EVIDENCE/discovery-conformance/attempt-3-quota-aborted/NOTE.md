# Attempt-3 quota-aborted codex launches

Recorded by agent:ClaudeCode-discovery-fix-3, 2026-09-22.

These seven records are preserved aborted launches, not conformance results. On the first attempt-3 codex matrix launch, every session exited within seconds with the host's account-level usage-limit error ("You've hit your usage limit … try again at 2:49 PM") in the raw stream. The matrix driver was stopped immediately; the in-plan cases not yet launched were deferred until after the declared reset time.

These records establish only that the launches occurred and failed on quota. They are excluded from the attempt-3 conformance matrix and from every support claim. They are retained so that no launched session is discarded or unreconstructible (review finding N3 from round 1).

## Second window (appended 2026-09-22, agent:ClaudeCode-discovery-fix-3)

After the 14:50 reset the codex matrix completed and `positive_root` reruns reached 3 evaluated PASS; the account quota was then exhausted a second time mid-rerun ("try again at 7:50 PM"), aborting `negative_collision` runs 2–3 and `adapter_removed_manual` runs 2–3 (fast exit-1 launches with the same usage-limit error in the raw stream). Those four records joined this quarantine; the affected cases are deferred to the next reset window.
