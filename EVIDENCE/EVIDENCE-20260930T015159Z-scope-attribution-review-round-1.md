# Evidence — Scope-attribution amendment independent review round 1

## Metadata

- **ID:** `EVIDENCE-20260930T015159Z-scope-attribution-review-round-1`
- **Captured UTC:** `2026-09-30T01:51:59Z`; retained runs began at `01:54:48Z` and `01:59:06Z`.
- **Recorded by:** `agent:Codex-scope-review-20260930`, fresh independent participant; no authorship of the implementation under review. Implementor attribution in the owning issue is `agent:ClaudeCode-discovery-fix-3`. Label inequality is not authenticated identity.
- **Reviewed target:** `6e39cea8ac46d909709ddaeeda1aa8d2df59ce08`.
- **Comparison parent:** `ebfab74c40f0fa858f4297ff7d10db74f7de8bd8`.
- **Claim challenged:** the amendment implements fail-closed, independently authorized intervening-work attribution without laundering attempt-owned changes.
- **Requirements:** accepted [PROJECT_SPEC](../PROJECT_SPEC.md), especially `PIPELINE-002`, `PIPELINE-005`, `PIPELINE-007`, `PIPELINE-010`, and root [BOOTSTRAP](../BOOTSTRAP.md) authority/review boundaries.
- **Accepted ADR:** [ADR-20260814T015817Z](../ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md), amended decision 7.
- **Owning issue:** [ISSUE-20260929T020157Z](../ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md).
- **Environment:** macOS 26.3 arm64; Python 3.9.6; Git 2.50.1 (Apple Git-155).
- **Disposition:** `CHANGES_REQUIRED`.
- **Open material findings:** `5` (R1–R5 below; IDs are local to this owning issue, not discovery review findings).

## Recovery, authority and scope

Read BOOTSTRAP completely; recovered accepted specification, ADR, owning issue/owner decision, issue-level review contract, pipeline/dispatcher state, actual implementation/tests, relevant intervening issues/evidence, and HANDOFF from repository records. No conversation or memory supplied implementation conclusions.

The owner decision recorded `2026-09-29T02:01:57Z` and the accepted specification/ADR authorize this bounded amendment, not a new milestone. Its issue explicitly uses the ordinary contract-evolution review path, as did the blocked-exit amendment. Consequently the dispatcher still selects the discovery **implementer**, state `IN_PROGRESS`, attempt 3; it does **not** dispatch this ordinary issue's review. HANDOFF and the owning issue request amendment review before any discovery resubmission. This discrepancy is not permission to execute the emitted discovery command. No milestone transition is appropriate for this review; its issue returns to `IMPLEMENTING` with this disposition.

At orientation, `main`, `origin/main`, and direct remote `refs/heads/main` all equalled the exact target; the worktree was clean. Read-only commands:

```sh
git status --short --branch
git rev-parse HEAD origin/main
git ls-remote --exit-code origin refs/heads/main
git show --format=fuller --stat 6e39cea
git diff 6e39cea^ 6e39cea
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_pipeline.py status --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
```

The local/tracking/direct refs check completed at approximately `2026-09-30T01:52Z`; all returned `6e39cea8ac46d909709ddaeeda1aa8d2df59ce08`. Target changed exactly eight intended root files: specification, pipeline ADR, implementation, pipeline tests, the new owning issue, discovery issue registry, HANDOFF, and checkpoint. No reusable-package file, bridge, discovery oracle, or live record changed in this amendment. There was no post-target drift at review start.

## Reproducible procedure and raw results

Run from any retained clone containing the target and evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py . --suite
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-1/reviewer_checks.py . --supplemental
```

Both commands exited `0`: that means the reproduction procedure completed, **not** that the amendment conforms. The [reviewer-owned harness](scope-attribution-review-round-1/reviewer_checks.py) extracts the exact target with `git archive`, imports its fixture helpers and implementation from that extraction, and performs all test transitions in disposable local Git repositories. It never transitions the source repository. Git fixture SHAs vary with commit timestamps; relationships, contents, exits and outcomes are the reproducible assertions. The real-case audit only reads the source repository; its two authority issues must still equal their target versions or the script refuses to reuse their current contents.

Raw retained output is [primary-results.json](scope-attribution-review-round-1/primary-results.json) and [supplemental-results.json](scope-attribution-review-round-1/supplemental-results.json). The latter adds cases without replacing earlier observations. The primary command independently ran, inside the target extraction:

| Exact argv after `python3` | Concise output | Exit |
|---|---|---|
| `-m unittest discover -s tests -p test_run_pipeline.py -v` | `Ran 33 tests in 32.849s` / `OK` | 0 |
| `-m unittest discover -s tests -v` | `Ran 178 tests in 43.110s` / `OK` | 0 |
| `scripts/validate_protocol.py` | `PASS structural protocol validation (package_files=10 handoffs=2)` | 0 |

There are 22 additional fixture scenarios: two positive controls advanced; nine expected refusals refused without any file/state mutation; eleven unsafe cases incorrectly advanced to `AWAITING_PEER_REVIEW`. All preserve the original attempt base; base preservation alone does not prove sound attribution.

| Case(s) | Required result | Observed result | Classification |
|---|---|---|---|
| `positive_independent`, `positive_self` | Advance | Advance, exclusions emitted | Confirmed controls |
| `unapproved_review`, `wrong_authority`, `identity_conflict`, `wrong_range` | Refuse | Exit 1, no mutation | Confirmed controls |
| `partial_coverage`, `self_substantive`, `AGENTS_after_valid_range` | Refuse | Exit 1, no mutation | Confirmed controls |
| `dirty_authority`, `unrecorded_file` | Refuse | `AEP-PIPE-GIT`, no mutation | Confirmed controls |
| `merge_post_review`, `merge_hidden_attempt_touch` | Refuse | Exit 0, state advanced | R1 |
| `wide_range_attempt_AGENTS`, `same_issue_registry`, `overlapping_unrelated_ranges` | Refuse | Exit 0, state advanced | R2 |
| `ambiguous_count`, `ambiguous_target`, `blocked_independent` | Refuse | Exit 0, state advanced | R3 |
| `malformed_in_scope`, `null_registry_in_scope` | Refuse | Exit 0, state advanced | R4 |
| `self_awaiting_decision` | Refuse | Exit 0, state advanced | R5 |

These findings concern recorded, inspectable contradictions and missing bindings, not cryptographic authentication or a demand for automatic natural-language judgment. No live agent, network probe, new dependency, or discovery-conformance rerun was used.

## Material findings and required follow-up

### R1 — HIGH — Git merge handling violates complete touch coverage and post-review restrictions

At target `scripts/run_pipeline.py:744–745`, `_commit_paths` uses `diff-tree` without merge-parent handling. In `merge_post_review`, it returns `[]` for a merge that changes `OTHER/amendment.md` to `unreviewed substantive merge edit`. A direct first-parent diff shows that substantive change. The range therefore passes the post-review record-only gate at lines 793–805 even though its final substantive bytes were never reviewed.

Separately, line 845 uses path-limited `git rev-list` without preserving full history. In `merge_hidden_attempt_touch`, an attempt-owned commit changes the same path on the main branch, outside the registered side-branch range. Resolving the merge to the reviewed branch's bytes makes Git simplify away that attempt commit. The scope gate counts only one touch and advances, while full-history enumeration shows the unregistered touch and merge. This violates the explicit **every touching commit** rule even though the final bytes match the reviewed side.

**Required follow-up:** account conservatively for all reachable attempt-window touches, including merge resolutions and parents, and apply the post-review record-only restriction to merges. Refuse any unaccounted or ambiguous touch before evidence/state mutation. Retain both adversarial cases and positive merge/range controls as regression evidence; preserve base/history rather than rewriting it.

### R2 — HIGH — Ancestry is treated as separate scope authority, allowing attempt-work laundering

At lines 765–805, an entry's HUMAN metadata and an ancestor APPROVED target make **every path in its caller-selected range** excludable. There is no binding between that range and the issue's separately authorized/reviewed implementation scope, nor a check that the referenced issue differs from the current milestone issue.

`wide_range_attempt_AGENTS` commits an explicitly unauthorized attempt-owned `AGENTS.md` change before a legitimately scoped intervention. That intervention's owner decision and review expressly exclude AGENTS.md. Expanding `from` to include the earlier attempt commit nevertheless excludes AGENTS.md and advances. `same_issue_registry` uses the milestone's own issue as its alleged intervening authority and also advances an unauthorized AGENTS.md change; review cannot expand that milestone's allowed paths. `overlapping_unrelated_ranges` obtains two purported covering issues for the first intervention even though the second issue expressly authorizes/reviews only its own different path. Merely being an ancestor of a reviewed tree is not evidence that unrelated work belonged to that issue's review scope.

**Required follow-up:** require durable, independently verifiable scope/range provenance for a **separate** owning issue; bind excluded commits/paths to that authority and reviewed scope, reject self-reference and unverifiable/contradictory overlaps, and prevent backward-expanded ranges from absorbing attempt work. Do not widen discovery allowed_paths or add ad-hoc exceptions. If the chosen representation changes accepted authority or architecture, propose it to the owner first; this review authorizes no new trust model.

### R3 — HIGH — Ambiguous or unresolved review records are accepted as approval

At lines 726–739, `_tolerant_latest_review` searches for the first hash and first digit sequence instead of establishing one unambiguous reviewed target and one nonnegative count. `**0 resolved; 1 still open**.` is read as zero open findings; a target field containing two full hashes joined with `or` is read as its first hash. Both advance. The INDEPENDENT branch also accepts an issue whose status remains `BLOCKED` alongside an APPROVED round (`blocked_independent`), rather than refusing the conflicting unresolved-work signals.

**Required follow-up:** accept documented prose formatting only when target, count, latest applicable round, disposition and issue-resolution signals are unambiguous and mutually consistent. Reject mixed counts, competing revisions and unresolved/contradictory records before mutation. Keep compatibility with the real blocked-exit review's unambiguous formatting; do not rewrite its authored review to hide the parser gap.

### R4 — MEDIUM — Present malformed registries can be silently ignored

At lines 838–842, registry parsing and verification run only if the net diff has an out-of-scope path. `malformed_in_scope` submits a wholly in-scope target with an unsupported registry schema and advances. Additionally, lines 672–674 conflate an absent block and a present JSON `null`: `_parse_intervening_registry` returns `[]` for the latter. The null case also advances. This directly contradicts both PIPELINE-010 and ADR decision 7's explicit malformed-registry rejection rule.

**Required follow-up:** validate every present registry at submission, independently of whether it is needed for exclusions; distinguish absence from invalid/null content, with deterministic schema refusals and no mutation. Add in-scope as well as out-of-scope malformed-entry tests.

### R5 — MEDIUM — SELF exclusion does not require a recorded owner decision

At lines 807–817, any non-BLOCKED status and any nonempty unblock string other than four exact sentinel words passes. `self_awaiting_decision` contains no owner-decision record and expressly says `Awaiting owner approval; decision NOT RECORDED`, yet its own issue file is excluded and submission advances. Authority HUMAN identifies who must decide; it is not evidence that they did decide. The own-file restriction works (the substantive-path control refuses), so this finding is narrower than a SELF code-path bypass.

**Required follow-up:** require a positive, attributable, durable decision reference/signal satisfying the SELF entry's authority gate; absence, pending authority and contradictory status/decision records must refuse. Keep exclusion limited to the referenced issue itself. This does not reopen the already reviewed blocked-exit implementation: the new general registry is being checked against PIPELINE-010's stricter exclusion requirement. The prior review's disclosed semantic-judgment limitation does not supply the missing decision in this reproduction.

## Actual discovery-case attribution

This is a read-only historical-candidate audit, **not** submission of `9f72d3d` (which is not current HEAD) or acceptance of discovery conformance. The frozen amendment's registry is evaluated against candidate `9f72d3de57085525a8ddf8a3b14bf1a3161e26e8`, preserving base `88fa8359ec3a62f200096d0d96bd04a88ebd118a`.

- Entry A: [blocked-exit issue](../ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md), HUMAN/INDEPENDENT, `ea2d39389dc1f5e0a3fc2682f26a51e693ac51fe..79063cb2201517567c3a8fe9702fd59ca41e9e5d`. Latest recorded round `2026-09-24T01:19:04Z`, reviewer `agent:ClaudeCode-blocked-exit-review-20260924`, APPROVED/0, target `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3`. The actual scope of that review includes the amendment and resume. Its reviewer states fresh-instance independence from `agent:ClaudeCode-discovery-fix-3`. Review target is an ancestor of range tip; the only post-review commit `79063cb` changes HANDOFF, checkpoint, the authority issue and its review evidence only. The [prior evidence](EVIDENCE-20260924T011904Z-blocked-exit-review-round-1.md) was inspected for provenance, not re-adjudicated.
- Entry B: [quota-authority issue](../ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md), HUMAN/SELF, `88fa8359ec3a62f200096d0d96bd04a88ebd118a..9f72d3de57085525a8ddf8a3b14bf1a3161e26e8`. Actual owner decisions are present, beginning `2026-09-23T01:32:06Z`, followed by bounded authorizations/outcomes. This entry can account only for that issue file, not code/specification/live execution authority. Its final historical sentence claiming a standing review submission is stale; later scope-refusal records and machine state refute it.

Independent enumeration uses `git rev-list base..candidate` **without a path limit**, then inspects every commit with `git diff-tree --root -m --no-commit-id --name-only -r COMMIT`. The raw JSON records each full commit and range. All six paths are covered:

| Out-of-scope path | All observed touching commits (abbreviated here; full values in JSON) | Entry |
|---|---|---|
| `PROJECT_SPEC.md` | `47a0cb4` | A |
| `ADR/ADR-20260814T015817Z-authorized-milestone-pipeline.md` | `47a0cb4` | A |
| `scripts/run_pipeline.py` | `47a0cb4` | A |
| `tests/test_run_pipeline.py` | `47a0cb4` | A |
| `ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md` | `610c672`, `47a0cb4`, `79063cb` | A |
| `ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md` | `39bae36`, `610c672`, `c1215a5`, `80fe4cb`, `9f72d3d` | B |

Removing A leaves exactly the first five paths uncovered; removing B leaves its own issue uncovered. Although the ranges overlap in commits, their actual **excludable out-of-scope path sets are disjoint**, so these two entries do not create the ambiguous ownership reproduced in R2. A new AGENTS.md change after an unchanged legitimate range refuses in the fixture control; the broader claim that registry smuggling is impossible is refuted by R1/R2. Real-case success therefore does not establish the general contract.

## Confirmed strengths, alignment and non-material observations

- **CONFIRMED:** PIPELINE-010 and ADR decision 7 express the same owner-approved invariants. No unauthorized change to the state set, transition table, target==HEAD check, discovery contract JSON, authority digest, attempt number/base/event history or discovery scope was found in the target diff. The reviewed implementation is root-only, standard-library, and generic in its identifiers; no current six-path, issue-ID or commit-ID special cases were found. The defects are general proof failures, not hard-coded current-case exceptions.
- **CONFIRMED:** the existing suite exercises useful straight-line positives, unapproved/latest adverse rounds, wrong authority, malformed ranges, exact-label conflicts, partial coverage, SELF substantive-path refusal and no-mutation failure paths. Independent controls reproduce those protections. The tests do not cover the eleven false-advance cases above.
- **CONFIRMED:** `git diff --check 6e39cea^ 6e39cea` returned 0; `git ls-tree -r 6e39cea protocol` shows ten mode-100644 Markdown files, unchanged from parent. Accepted intervening commits remain ancestors of target; the original discovery state object is equal before/after this amendment. No rewrite, rebase or revert of the accepted intervention appears in the inspected append-only chain. No whole-repository historical-authorship guarantee is claimed.
- **O1 — LOW, non-material continuity correction:** target HANDOFF still describes run-9/manual-fallback coverage as outstanding in Unverified complexity, while newer durable run-10/refusal records supersede it; its scope-amendment status is OPEN despite being at review. The quota issue's old submitted sentence is also stale. This review reconciles the shared HANDOFF snapshot and owning amendment lifecycle, preserving authored historical narratives. It does not independently certify any discovery live outcome.
- **O2 — LOW, non-material audit friction:** `scope_exclusions` contains only path, covering issue(s) and touch count, not exact entry/range/review/decision provenance. For the actual unambiguous A/B case, submission target/base plus the committed registry and issue records allow reconstruction, so this is not by itself an untraceable-evidence finding. R2 shows why ambiguous entries cannot be approved on this summary alone. Follow-up should make each verified attribution traceable to its exact range, touching commits and authority/review decision; this evidence supplies that mapping for the historical case.
- **O3 — LOW, non-material inherited role wording:** ROLE_CONTRACTS Implementer output still says target's **parent** is attempt base, whereas accepted pipeline semantics use an ancestor and PIPELINE-010 explicitly preserves intervening history. This predates this amendment; specification/ADR precedence is clear and no base rewrite is authorized. Reconcile the subordinate wording through an authorized documentation follow-up; this reviewer does not change role contracts.

## Limitations, corrections and final boundary

- Recorded authority and reviewer labels are operational evidence, not authenticated identity. Generic semantic adequacy still requires independent review; no cryptographic trust model is proposed.
- No discovery conformance, bridge installation, live-agent session, historical discovery oracle probe, host capability or external quota was re-reviewed/run. Full deterministic unit tests were run as requested; those do not launch live agents.
- Dedicated Markdown linters: `command -v markdownlint markdownlint-cli2` returned exit 1 with no output; NOT RUN. Structural validator, local link/fence/newline checks and `git diff --check` provide bounded checks, not cross-host portability evidence.
- Initial scratch merge-fixture exploration hit a `FileNotFoundError` after Git removed an empty EVIDENCE directory on branch switch. The retained harness creates fixture parent directories explicitly and independently reproduces the merge defects. That scratch harness error is not product evidence. Additional scratch exploration found conservative refusal when two disjoint valid ranges separately cover successive touches of one path (the implementation requires one range to cover all touches); this is a coverage limitation, not counted as a fail-open finding or an established acceptance promise.
- Implementation summaries claiming universally fail-closed provenance/no smuggling are contradicted by R1–R5; original authored claims remain historical, not silently rewritten. This record supplies exact reproducible commands and outputs missing from the prior real-case summary.
- No implementation/specification/ADR/product/bridge/test change, third registry entry, discovery resubmission, machine-state transition, acceptance, issue closure, next-role execution, or publication is performed by this review. Reviewer-owned evidence, the issue round and current-state reconciliation are the only changes.
- **Required next action:** implementer reworks R1–R5 within the accepted amendment authority, verifies the corrected target and obtains a new independent review. Discovery submission remains withheld. Any new scope/trust/architecture decision must go to the owner first.

## Governance closeout evidence

Separate post-write reads showed the actual issue status, reviewed target, finding count/disposition, current HANDOFF state/Next Action, and retained supplemental results. Exact command and output: [governance-readback.txt](scope-attribution-review-round-1/governance-readback.txt). The evidence harness and primary JSON also received separate `sed` reads after creation; no write was fused with its verification read.

The reviewer executed the exact body now retained as [check_governance.py](scope-attribution-review-round-1/check_governance.py); at that checkpoint it exited 0 with:

```text
PASS governance: review=CHANGES_REQUIRED material=5 issue=IMPLEMENTING
PASS HANDOFF: five ordered sections; one bounded Next Action; authored history preserved
PASS pipeline: IN_PROGRESS attempt=3 target=null original state unchanged registry_entries=2
PASS review-only diff; regular files; local file links=133; fences/newlines/trailing whitespace
PASS retained reproductions: 22 scenarios; 11 false advances; 9 no-mutation refusals; 2 positives
PASS accepted intervening commits remain ancestors of immutable target
```

Reproduce at this review-record checkout (the link count grows when this appendix adds links):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 EVIDENCE/scope-attribution-review-round-1/check_governance.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/run_dispatch.py --json
git diff --check
git diff --exit-code 6e39cea -- BOOTSTRAP.md PROJECT_SPEC.md ADR scripts tests protocol AGENTS.md CLAUDE.md ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md
```

The structural validator returned `PASS structural protocol validation (package_files=10 handoffs=2)`; diff checks returned 0. Dispatcher remains `role=implementer`, `state=IN_PROGRESS`, discovery attempt 3 bound to `agent:ClaudeCode-discovery-fix-3`; emitted submission command was not executed. This ordinary amendment has no pipeline transition to record. The first scratch governance check falsely failed a history-suffix assertion because its Git-output helper stripped the final newline; normalizing both compared strings corrected the check. No historical content was changed to make that assertion pass. No implementation pass is inferred from governance validation.
