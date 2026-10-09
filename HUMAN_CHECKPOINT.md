# Human Checkpoint

This is an owner synchronization summary, not project truth. Read [BOOTSTRAP](BOOTSTRAP.md); requirements live in [PROJECT_SPEC](PROJECT_SPEC.md), architecture in accepted ADRs.

## Reviewer update — 2026-10-09T01:54:25Z

Prepared by `agent:Codex-scope-review-20261009`, independently reviewing only amendment rework `4dda31e9945000b51e950f4ac01ec7f82ffb15bf`. Prior authored sections are retained as history.

- **CHANGES_REQUIRED — three material findings remain:** R2 HIGH: issue-file introduction and Git-derived paths do not bind effective separate authority; post-introduction foreign work, unauthoritative drafts, delete/re-add and mixed-merge cases still advance. R3 HIGH: example-only approval and a malformed latest BLOCKED round still lead to approval. R5 MEDIUM: contracted negation and contradictory/duplicated SATISFIED conditions still pass SELF authority. [Owning round](ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [full evidence](EVIDENCE/EVIDENCE-20261009T015211Z-scope-attribution-review-round-3.md) specify required follow-up.
- **Verified improvements:** 49 pipeline / 194 full target tests and validator pass; all original 42 reviewer scenarios conform, R1/R4 show no regression in bounded checks, honest A/B still cover the six historical paths. But nine of 15 new variants falsely advance, so these successes cannot establish general safety.
- **Boundary:** amendment stays IMPLEMENTING for bounded rework and fresh review. Discovery remains IN_PROGRESS attempt 3, target null, original digest/base/events, two entries; no amendment machine state exists and no transition applies. No implementation fix, live session, discovery submission, registry addition, acceptance/closure, recorder/coordinator or push performed.
- **Owner decision requested now: NONE for repairs that satisfy the already accepted invariants.** Any new architecture/trust/scope decision must be escalated; this review adopts none. Reviewer stops after durable disposition and governance validation.

## Implementer update — 2026-10-08T03:08:54Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after reworking the scope-attribution amendment per your directive to resolve the still-open round-2 findings; not an acceptance record. Prior sections are preserved as history.

- **The three open round-2 findings are addressed on a new immutable target, within your ten approved invariants and with all history preserved** (`6e39cea`, `4f5e387`, and both rounds of review records untouched; no amend or rewrite). On `4dda31e9945000b51e950f4ac01ec7f82ffb15bf`: **R2** — a registry entry's declared exclusion scope must now be exact file paths (directory prefixes refuse) equal to the range's Git-derived substantive work, and every substantive range commit must descend from or equal the owning issue record's introduction commit, so a widened range or declaration can no longer absorb attempt-owned changes made before the separate authority existed; **R3** — review provenance must be uniquely determinable: exactly one unfenced review-rounds section, a strictly latest round, exactly one boundary-delimited full revision (a 41-hex token refuses), a bare nonnegative integer finding count (unknown/negated prose refuses), and a status from the fixed resolved-status vocabulary (`UNRESOLVED`/missing/`BLOCKED` refuse); **R5** — fenced examples are stripped and every recorded owner-decision heading must carry a nonempty, human-attributed, positive-verb body with no negated/pending/awaiting language, plus a `SATISFIED`-prefixed unblock condition. SELF entries still declare no paths and exclude only their own issue file. The independently resolved R1/R4 mechanisms are untouched. **Whether these corrections resolve the findings is for fresh independent round 3 to judge — I claim no resolution.**
- **Verification:** **194 tests OK, validator PASS, discovery reviewer probes 19/19 non-PASS.** All 20 round-2 reviewer variants are now deterministic regression tests: the 11 previous false advances refuse, the 7 refusals are preserved, and the 2 positive controls still advance. The round-2 reviewer's own harness, retargeted at the new commit, reports zero requirement violations across all 42 scenarios, every refusal preserving files/state. Read-only re-evaluation verifies both real registry entries unchanged (Entry A declared scope equals its derived substantive work; Entry B decision parses as effective); entry removal still loses five/one paths; discovery contract block, digest, and machine state are byte-identical.
- **Owner decision requested now: NONE for the rework itself** — it implements your directive within the already accepted invariants. **Stopped at the independent-review boundary:** the amendment awaits a fresh independent round 3 (reviewer label differing from `agent:ClaudeCode-discovery-fix-3`) on `4dda31e9945000b51e950f4ac01ec7f82ffb15bf`; I did not self-review or self-accept. Discovery remains IN_PROGRESS attempt 3 with no submitted target; resubmission stays deferred until the amendment is legally accepted. No live session, no transition, no third registry entry.

## Reviewer update — 2026-10-08T02:04:10Z

Prepared by `agent:Codex-scope-review-20261008`, independently reviewing only scope-attribution amendment rework `4f5e38744340fb7597222bf31483eb67187e2bbf`. Prior sections remain attributed history, not current approval.

- **CHANGES_REQUIRED, three open material findings:** R2 HIGH — arbitrary declared paths/widened ranges still absorb attempt-owned changes despite conflicting separate authority; R3 HIGH — ambiguous counts/target tokens/review sections and unresolved status still pass; R5 MEDIUM — pending/empty/example owner-decision headings still authorize SELF own-file exclusion. R1 merge/history and R4 present-registry validation fixes pass independent bounded verification. [Owning round](ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [commands/raw evidence](EVIDENCE/EVIDENCE-20261008T020134Z-scope-attribution-review-round-2.md) contain required follow-up.
- **Correction to the implementer's 2026-09-30 all-resolved claim:** 42 pipeline and 187 full target tests pass, validator passes, and all 22 original v2-adapted reviewer scenarios now conform; nevertheless 11 of 20 new variants falsely advance. The real A/B entries still legitimately cover the six historical paths. Passing those examples does not prove general authority binding or unambiguous acceptance.
- **Current state:** amendment stays IMPLEMENTING for bounded R2/R3/R5 rework and fresh review. Discovery remains IN_PROGRESS attempt 3, target null, original digest/base/events, two unchanged entries. No amendment pipeline state exists, so no pipeline transition is applicable to this disposition. No implementation fix, live probe, discovery resubmission, third registry, acceptance, closure, recorder/coordinator or publication performed.
- **Owner decision requested now: NONE for repairs within the accepted invariants.** Escalate any proposed new architecture, scope or trust-boundary decision; this review authorizes none. The reviewer stops after durable disposition and governance verification.

## Implementer update — 2026-09-30T03:14:19Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after reworking the scope-attribution amendment per your directive to resolve all round-1 findings; not an acceptance record. Prior sections are preserved as history.

- **All five round-1 material findings (R1–R5) are resolved on a new immutable target, without shrinking your ten approved invariants and with all history preserved** (`6e39cea` and the round-1 review records are untouched; no amend or rewrite). The registry is now `aep-intervening-authority/v2`: entries declare their exclusion scope (`paths`) bound to verified acceptance; validation runs on every submission (a present malformed/null registry refuses even for in-scope targets); review records must unambiguously record exactly one reviewed revision and one finding count, with non-blocked status consistency for both classes; SELF records require a durable `### Owner decision recorded <UTC>` heading and may exclude only their own issue file; independently reviewed ranges must be clean of foreign substantive paths and entries' exclusion scopes pairwise disjoint; touching-commit accounting is merge-aware across all parents with no path-limited history simplification, closing the merge blind spots; exclusions record touching commits and covering-entry provenance for the eventual reviewer. PIPELINE-010 and ADR decision 7 carry strengthened text and change-record rows.
- **The reviewer's counterexamples are now deterministic regression tests** (merge-post-review hiding, merge-hidden attempt touch, wide-range absorption, self-reference, cross-entry claims, overlapping scopes, ambiguous records, blocked INDEPENDENT, SELF without decision, in-scope malformed/null registries) plus a positive record-only merge control: **187 tests OK, validator PASS, discovery reviewer probes 19/19 non-PASS**. The discovery registry was migrated to v2 (same owning issues and ranges; Entry A declares the four amendment paths, Entry B declares none); the read-only re-evaluation still covers all six refused paths with zero uncovered and remains fail-closed under entry removal.
- **Owner decision requested now: NONE for the rework itself** — it implements your directive within the already accepted invariants. **Stopped at the independent-review boundary:** the amendment awaits a fresh independent round 2 (reviewer label differing from `agent:ClaudeCode-discovery-fix-3`); I did not self-review or self-accept. Discovery remains IN_PROGRESS attempt 3 with no submitted target; resubmission stays deferred until the amendment is legally accepted. No live session, no transition, no third registry entry.

## Reviewer update — 2026-09-30T01:59:49Z

Prepared by `agent:Codex-scope-review-20260930`, independently reviewing only the scope-attribution amendment `6e39cea8ac46d909709ddaeeda1aa8d2df59ce08`. Prior sections are preserved as history, not current approval.

- **CHANGES_REQUIRED, five open material findings:** R1 HIGH merge-history/post-review bypasses; R2 HIGH unbound/self-referential/contradictory registry ranges can launder attempt-owned AGENTS.md changes; R3 HIGH ambiguous or unresolved review records pass; R4 MEDIUM malformed registries ignored for in-scope targets; R5 MEDIUM SELF own-file exclusion without an owner-decision record. [Owning round](ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md) and [reproducible evidence](EVIDENCE/EVIDENCE-20260930T015159Z-scope-attribution-review-round-1.md) contain exact resolution conditions.
- **Existing tests pass, but do not prove fail-closed behavior:** frozen-target 33 pipeline / 178 full deterministic tests and validator pass; 22 reviewer fixtures show 11 unsafe advances. The actual two entries do cover the six historical paths, confirmed by independent per-commit enumeration, but that valid case does not remedy the general counterexamples.
- **Current state:** amendment issue returns to IMPLEMENTING through its ordinary issue-level review path. Discovery remains IN_PROGRESS attempt 3, original digest/base/history, no submitted target; no machine transition or third registry entry occurred. The dispatcher still reports discovery implementer, but resubmission remains deferred pending amendment fixes and approval.
- **Owner decision requested now: NONE for fixes that implement the already accepted invariants.** New scope, architecture or trust-boundary changes would require your approval; this review does not adopt any. No implementation change, live session, discovery-conformance re-review, acceptance, closure, recorder/coordinator action or publication was performed.

## Implementer update — 2026-09-29T02:44:00Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after implementing your approved scope-accounting amendment; not an acceptance record. Prior sections remain historical.

- **Your approved amendment is implemented** per the ten recorded invariants, tracked in [ISSUE-20260929T020157Z-pipeline-scope-intervening-authority](ISSUES/ISSUE-20260929T020157Z-pipeline-scope-intervening-authority.md): PIPELINE-010 in `PROJECT_SPEC.md` (the milestone contract block is untouched — all digests unchanged), ADR-20260814T015817Z decision 7 amended with a status-history row, and `scripts/run_pipeline.py` now verifies an optional fail-closed `aep-intervening-authority/v1` registry on the milestone issue. INDEPENDENT entries require a verifiable APPROVED independent round (zero open material findings, reviewed target ancestor-or-equal of the range tip, post-review commits restricted to record-keeping, reviewer label differing from the implementor); SELF entries can exclude only their own issue file. A path outside `allowed_paths` is excluded only when every commit touching it belongs to a verified range, and every exclusion is recorded in the submission evidence for the milestone's reviewer.
- **The real case is proven without any state change:** the discovery issue now registers Entry A (blocked-exit amendment, INDEPENDENT) and Entry B (quota-authorization record, SELF). A read-only evaluation using the pipeline's own verification functions shows all six previously refused paths covered by verified ranges, zero uncovered; with Entry A removed the amendment paths are uncovered (fail-closed); a hypothetical unauthorized `AGENTS.md` change is uncoverable (no smuggling). **178 tests OK** (6 new deterministic registry test groups), validator PASS, reviewer probes 19/19 non-PASS, frozen oracle unchanged. No live session, no transition, no machine-state edit.
- **Stopped at the independent-review boundary:** the amendment changes accepted pipeline verification semantics, so per `Review: INDEPENDENT` it needs a fresh independent review (same path as the blocked-exit amendment). I did not self-review or self-accept. Discovery resubmission is deferred until that review is APPROVED and a third registry entry covers this amendment's own commits — the current scope gate is not bypassed.

## Implementer update — 2026-09-29T01:35:13Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after executing your final single-session authorization; not an acceptance record. Prior sections remain historical.

- **Run 10: evaluated PASS.** Your authorized single `codex adapter_removed_manual` session on revision `a834108` (frozen oracle hash verified unchanged; 1/1 session, no retry) classified PASS with zero defects: the participant completed the write first, then ran the verification read as a separate standalone `cat` invocation with content-visible output — exactly what the refined instruction requires. Uniform frozen-oracle re-evaluation of all 50 records is clean apart from the previously disclosed historical refinement; 172 tests OK, validator PASS, reviewer probes 19/19 non-PASS. **Acceptance criteria 1–5 are now established** for both first-slice supported profiles (Claude root+subdirectory; Codex root only).
- **Review submission refused by the deterministic scope gate — owner decision needed.** The pipeline transition `IN_PROGRESS → AWAITING_PEER_REVIEW` (target `9f72d3d`) failed `AEP-PIPE-SCOPE` with no state advance: the attempt-3 base→target diff includes six paths outside the milestone's accepted `allowed_paths` — the blocked-exit amendment (`PROJECT_SPEC.md` PIPELINE-009, ADR decision 5, `run_pipeline.py`, `test_run_pipeline.py`) and its two record issues (quota authorization, blocked-exit), all separately owner-approved and independently reviewed, but landed while the milestone was BLOCKED_HUMAN_AUTHORITY. Since the target must equal HEAD, no in-scope target can exclude them. Widening `allowed_paths` changes the accepted milestone digest that the digest-binding gate checks — a specification-evolution decision only you can make.
- **Stopped at the boundary:** the milestone remains IN_PROGRESS attempt 3; no machine state was edited, no scope self-extended, no review submission stands, and no further live session will be launched without your explicit authorization. The evidence boundary (50 records + this refusal) is preserved for independent review once you decide the disposition.

## Implementer update — 2026-09-28T02:15:19Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after your directed offline refinement; no live session was launched. Prior sections remain historical.

- **Refinement delivered per your instruction.** The delivered verification instructions now explicitly require: (1) the mutation/write completes first; (2) the exact-artifact post-change verification read runs as a **separate subsequent command or tool invocation**; (3) that invocation's recorded output shows the actual content; (4) write and verification read MUST NOT be merged into one compound shell command. Applied to root `BOOTSTRAP.md`, `protocol/BOOTSTRAP.md`, and the `protocol/PROMPTS.md` manual fallback; fixture resynchronized byte-identically; two deterministic regression tests prove both delivered BOOTSTRAPs and the actually-launched manual fallback prompt carry the separate-invocation requirement.
- **Verification:** 172 unit tests OK, structural validator PASS, reviewer adverse probes 19/19 non-PASS; frozen oracle untouched (`e991d148…`); acceptance criteria unchanged; run 9 and all prior UNVERIFIED/PASS/quota evidence preserved unmodified — nothing reclassified, no history rewritten.
- **Stopped as directed:** no live session launched and none will be without your new explicit authorization. A further evaluated `codex adapter_removed_manual` PASS on this delivered-byte revision is the remaining gap before review submission; the disposition is yours.

## Implementer update — 2026-09-28T02:02:06Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after executing your single-session authorization; not an acceptance record. Prior sections remain historical.

- **Your authorized single session ran exactly once; result UNVERIFIED, zero defects.** Run 9 (`codex adapter_removed_manual`, 2026-09-28T01:51:27Z–01:53:56Z, exit 0, frozen oracle hash verified unchanged pre-launch) ended with the sole gap "no successful post-mutation verification read of `RESULT.txt` recorded". Per your stop condition, no second session was launched.
- **What happened:** the participant *did* follow the new instruction and performed a content-visible post-change read — but fused it into the same single shell command that created the file (one `zsh -lc` containing the write heredoc, then `cat RESULT.txt`, `od -An -tx1 RESULT.txt`, then a byte assertion). The frozen fail-closed oracle can only credit a read that stands as a separately attributable command; it conservatively abstains on reads fused into the mutating event (and `od -An -tx1`'s flags are outside its accepted set). The recorded output does show the content — this is an attribution boundary of the reviewer-required conservative design, not a missing verification behavior. No oracle change, no reclassification, no review submission. Uniform re-evaluation of all 49 records is clean apart from the previously disclosed historical refinement; details in the [attempt-3 evidence](EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md).
- **Owner decision requested now (disposition):** acceptance criterion 5 remains unmet (`adapter_removed_manual`: 7 UNVERIFIED runs, all otherwise conforming). Options: authorize a further explicitly bounded Codex session (e.g., additionally instructing the read as a separately executed command), amend the claim through specification evolution, route the oracle attribution boundary to independent review, or direct an alternative disposition. **No participant launches any live session or submits the milestone for review until you decide.**

## Implementer update — 2026-09-28T01:43:10Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after diagnosing the systematic verification-read gap per your instruction; no live sessions were launched. Prior sections remain historical.

- **Root cause: delivered-instruction gap (not a probe bug, not an oracle defect).** All six `codex adapter_removed_manual` runs verified `RESULT.txt` after mutation — but only via Python hash/byte assertions whose recorded output never shows the file's content. The reviewer-hardened fail-closed oracle counts only strict content reads (`cat`/`od`/whitelist) with content-visible output; every PASS in this attempt contains one. The delivered texts required verification generically but never specified the inspectable form for exact-artifact tasks, so the behavior was left to participant habit.
- **Fix (within accepted milestone scope; no requirement, acceptance-criteria, or oracle change — probe hash `e991d148…` unchanged):** `protocol/BOOTSTRAP.md` and root `BOOTSTRAP.md` now MUST-require a post-change read whose recorded output shows the artifact's actual content for exact-artifact expectations; the `PROMPTS.md` manual fallback requires the same; the fixture is resynchronized; three deterministic regression tests prove the delivered texts (including the manual fallback prompt actually launched) carry the requirement. **170 unit tests OK, validator PASS, reviewer probes 19/19 non-PASS.** All prior PASS/UNVERIFIED/quota evidence is preserved unmodified and no record was reclassified.
- **Owner decision requested now (resource authorization):** exactly one evaluated `codex adapter_removed_manual` PASS against the updated delivered bytes remains before review submission. Minimal live set: a bounded batch for that single case (observed failure mode now instruction-addressed; sizing is your call — the previous batch consumed 5 sessions on this case). No participant launches any live session until you authorize.

## Implementer update — 2026-09-28T01:28:45Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after executing your authorized bounded Codex batch; not an acceptance record. Prior sections remain historical.

- **Your authorized batch is executed and fully consumed (6/6 sessions):** `codex negative_collision` run 4 — **evaluated PASS** under the frozen v3 oracle (verification read recorded; `KEEP.txt` intact; case stopped immediately). `codex adapter_removed_manual` runs 4–8 — **5 sessions, all UNVERIFIED** with the sole gap "no successful post-mutation verification read of `RESULT.txt`" (otherwise conforming every run). The 6-session cap was reached without a PASS; execution stopped per your recorded bounds. No quota error occurred; no record was discarded; no wakeup or auto-relaunch was created; the budget was not expanded.
- **Verification:** uniform frozen-oracle re-evaluation of all 48 attempt-3 records — no flips beyond the previously disclosed refinement; reviewer probe regression 19/19 non-PASS. Details in the [attempt-3 evidence 2026-09-28 batch section](EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md) and [ISSUE-20260922T073608Z execution outcome](ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md).
- **Owner decision requested now (exhausted-budget disposition):** `adapter_removed_manual` still lacks one evaluated PASS after 6 total runs, so acceptance criterion 5 keeps the milestone out of review submission. Options: authorize a new explicitly bounded batch, amend the claim through specification evolution, or direct an alternative disposition. **No participant launches any Codex session or submits the milestone for review until you decide.**

## Reviewer update — 2026-09-24T01:19:04Z

Prepared by `agent:ClaudeCode-blocked-exit-review-20260924` after a fresh independent review of the blocked-exit amendment and the discovery-milestone resume; not an acceptance record. Prior sections remain historical.

- **APPROVED, 0 open material findings.** Round 1 on immutable target `9e8f6b285b8e9f47022c7c3fb4ba67d5341601b3` (amendment `47a0cb4` + resume `9e8f6b2`) confirms: the single `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` edge matches your approved bounds; exit requires the entry blocker's durably recorded decision with fail-closed identity matching; attempt 3/implementor/base were preserved; the transition was pipeline-executed, not hand-edited; the 2026-09-22 ROTATE-004 correction is appended and attributable, not rewritten. Full suite (167 tests) and validator independently re-run: both PASS. [Round and evidence](EVIDENCE/EVIDENCE-20260924T011904Z-blocked-exit-review-round-1.md).
- **Non-material observations:** PIPELINE-009's literal "every milestone state" phrasing includes terminal `ACCEPTED` (your bound was "blocking state"; intent clear); entry-side quota-rationale rejection remains spec-level, as deliberately scoped; machine gates check durable recording signals only (disclosed).
- **Owner decision requested now: NONE.** Your armed Codex budget (2 cases, ≤6 sessions) remains unconsumed and still awaits your distinct "execute now" instruction; the reviewer launched nothing and performed no implementer/recorder/coordinator duties. The amendment issue stays OPEN for ordinary closure.

## Implementer update — 2026-09-23T03:13:39Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after implementing the owner-approved blocked-exit amendment; not an acceptance record. Prior sections remain historical.

- **Your approved amendment is implemented** (`47a0cb4`): `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` resume gated on the entry blocker issue's recorded owner decision, attempt preserved, decision cited in the transition reason. PROJECT_SPEC gained PIPELINE-009 (every enterable state must have a verifiable exit; unblock authorizes no separately gated execution or resource consumption; quota/participant failures alone never produce `BLOCKED_HUMAN_AUTHORITY`) and ADR-20260814T015817Z decision 5 carries the amendment plus a status-history row. Four new deterministic tests; 167 tests OK, validator PASS. Per the amendment issue's `Review: INDEPENDENT`, an independent review of the amendment is still outstanding.
- **Milestone resumed:** the discovery milestone is `IN_PROGRESS` (attempt 3 continues) after the validated transition citing your recorded decision. **No Codex session has been launched** — the unblock resolves only the authority blocker; your armed budget (2 cases, ≤6 sessions) still awaits your distinct "execute the authorized Codex supplementary verification now" instruction.
- **Owner decision requested now: NONE.** Next action remains yours alone: issue the explicit Codex execution trigger when you choose, or direct otherwise.

## Implementer update — 2026-09-23T01:32:06Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after recording the owner's bounded authorization; not an acceptance record. Prior sections remain historical.

- **Your bounded authorization is persisted** in [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md): only `codex negative_collision` and `codex adapter_removed_manual`, one evaluated PASS each then stop, ≤6 new Codex sessions total, failures preserved without unbounded retry, no repetition inflation, no wakeups/auto-relaunch, no specification change. **No Codex session has been launched or scheduled** — execution awaits your distinct "execute the authorized Codex supplementary verification now" instruction.
- **Owner decision requested now (contract gap):** the accepted pipeline contract (ADR-20260814T015817Z decision 5, PROJECT_SPEC `PIPELINE-003`) defines entry into `BLOCKED_HUMAN_AUTHORITY` but **no exit edge** — `run_pipeline.py` refuses every transition out, and machine state blocks are never hand-edited. Your authorization satisfies the human gate, but the milestone stays machine-blocked until the contract is amended. The proposed minimal amendment (add `BLOCKED_HUMAN_AUTHORITY → IN_PROGRESS` gated on the blocker issue's recorded owner decision) is in [ISSUE-20260923T013206Z-pipeline-blocked-exit](ISSUES/ISSUE-20260923T013206Z-pipeline-blocked-exit.md) and needs your approval/amendment/rejection.
- **Self-correction disclosed:** the 2026-09-22 entry into `BLOCKED_HUMAN_AUTHORITY` misapplied `ROTATE-004` (quota exhaustion is a participant failure and must not produce that state); the genuine gate was your resource directive, now satisfied. The correction fixes the record, not the machine state.

## Implementer update — 2026-09-22T07:36:08Z

Prepared by `agent:ClaudeCode-discovery-fix-3` after discovery attempt 3; not an acceptance record. Prior sections remain historical.

- **Owner decision requested:** authorize the minimal remaining Codex live run set in [ISSUE-20260922T073608Z-codex-quota-authorization](ISSUES/ISSUE-20260922T073608Z-codex-quota-authorization.md) — `codex negative_collision` and `codex adapter_removed_manual` reruns to one evaluated PASS each, estimated 2–6 sessions in one bounded batch. Per your 2026-09-22 directive, no Codex live session will launch without your explicit recorded authorization. The milestone is not submitted for review while this coverage is outstanding.
- **Round-2 material findings addressed:** R1 (explicit `--model gpt-6-astra` recorded per session), R2 (oracle rehardened; the reviewer's 19 adverse probes classify 0 PASS; 163 unit tests OK), R4 (conflict-stop/scope wording fixed in product text and bridges; both prior failure modes now PASS 2/2 each). Details and honest bounds in the [attempt-3 evidence](EVIDENCE/EVIDENCE-20260922T073608Z-discovery-live-conformance-attempt-3.md).
- **Claude coverage complete** (3 evaluated PASS per positive case of 7 launched; all negatives PASS; manual fallback PASS). **Codex root coverage incomplete**: `positive_root` 3/7 PASS and five negatives PASS, but the two cases above are UNVERIFIED with a sole verification-read gap after two account-quota exhaustions. Eleven quota-aborted launches are preserved, not discarded.
- All attempt-2 records were uniformly reclassified under the final oracle with disclosed downgrades; attempt-2 evidence received append-only attributable corrections. No self-review, acceptance, or review submission occurred.

## Reviewer update — 2026-09-22T02:01:17Z

Prepared by `agent:Codex-discovery-review-20260922` after a fresh independent review of target `cc7961187f067cbc7b337b8f80a64505693f7bc6`. This supersedes the historical support/resolution assertions below; it is not acceptance.

- **CHANGES_REQUIRED**, with three material findings: R1's remaining Codex effective model/configuration provenance, R2's independently reproduced oracle false positives, and new R4's required Claude conflicting-authority/nested failures (2/2 each). R3 portable installation is closed; full-package fixture/bridge fidelity is verified. [Round and evidence](EVIDENCE/EVIDENCE-20260922T020117Z-discovery-review-round-2.md).
- Accepted PROJECT_SPEC explicitly requires both harnesses and forbids silently narrowing the milestone. Codex root-only directory scope is valid, but observed root success is not a complete profile certification while provenance and oracle proof remain inadequate. Claude positives cannot cancel its required negative failures; leaving it unsupported does not permit milestone acceptance.
- **Owner decision required now: NONE.** Existing milestone authority permits product recovery/adoption wording, scoped bridge, oracle/test and evidence fixes that implement current requirements. A proposal to drop a harness/negative, change authority/gates or introduce a new trust/architecture mechanism would require owner-approved specification evolution; this reviewer makes no such proposal or change.
- Target checks passed 151 tests and validator; 19 local probes expose nine adverse false positives. All 34 attempt-2 records were checked against fixture bytes and uniformly reclassified from raw events; original failures/timeouts and characterization reruns remain separate. Earlier evidence is retained. No new live session, implementation repair, approval, closure or recorder work was performed.
- After round commit `7d4b01a`, the reviewer recorded CHANGES_REQUIRED event 8 at `2026-09-22T02:09:43Z`, reconciled the snapshot and stopped. Dispatcher selects an implementer for attempt 3, which has not begun. Four deferrals and the unstarted autonomy demonstration remain unchanged. No publication was performed.

## Implementer update — 2026-09-21T11:20:00Z

Prepared by `agent:ClaudeCode-discovery-fix` after discovery attempt 2; not an acceptance record. Prior sections remain historical.

- All three material findings were fixed within the accepted milestone scope and are implementor-resolved pending a fresh independent review: R1 (fixture rebuilt as a faithful adopted instance of the delivered ten-file package, bridges generated by the shipped installer), R2 (fail-closed oracle; the reviewer's five adverse inputs now classify non-PASS and are regression tests), R3 (self-contained create-or-merge installer embedded in `protocol/README.md`, package-only installation proven by tests).
- Attempt-2 live program: 34 bounded fresh sessions against the repaired fixture. **Codex CLI root start now satisfies the acceptance criteria. Claude Code does not**: it passes all positive cases but systematically fails two negative cases (`negative_conflicting_authority`, `negative_nested`, 2/2 each). Per acceptance criterion 5, milestone acceptance is prevented unless the independent reviewer adjudicates otherwise. [Attempt-2 evidence](EVIDENCE/EVIDENCE-20260921T110848Z-discovery-live-conformance-attempt-2.md).
- Deterministic gates at freeze: 151 tests OK, validator PASS.
- No new owner decision is requested for these bounded fixes; whether remedying the Claude negative-case behavior crosses the Human Authority Boundary (protocol-text semantics) is flagged for the reviewer. No acceptance or self-review occurred.

## Reviewer update — 2026-09-21T01:31:25Z

Prepared by `agent:Codex-discovery-review-20260921` to reconcile the completed independent review, not to record milestone acceptance. The implementation-phase checkpoint below remains historical; its pending-review and support-confidence statements are superseded by this update and the [owning issue](ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md).

- Round 1 on immutable target `074678d080fc6c1d57d2912314ae21296b618612` is **CHANGES_REQUIRED**, with three open material findings: R1 HIGH (full delivered protocol/bridge not verified by live evidence), R2 HIGH (oracle false positives), R3 MEDIUM (installation not self-contained/incorrect mapping). [Reviewer evidence](EVIDENCE/EVIDENCE-20260921T013125Z-discovery-review-round-1.md) preserves the completed checks and resolution conditions.
- Deterministic target checks passed 124 tests and the structural validator; these results do not establish discovery acceptance. Final fixture bytes are consistent across the matrix but differ from the distributed reference bridges.
- Non-material corrections: final Codex subdirectory run 3 hit a writable-scope denial, not the summary's memory-diversion cause; HANDOFF's issue/live-session fields were stale; two discarded misconfigured runs remain an explicit evidence gap. Codex's root-only boundary is compatible with its subdirectory 2/3 result, but does not resolve the material findings.
- After round commit `d8a7f0b`, the reviewer recorded CHANGES_REQUIRED at `2026-09-21T01:38:51Z`. Attempt remains 1 at the same target; the issue's IMPLEMENTING state is the fix-required mapping, not a claim that attempt 2 has begun. Dispatcher selects implementer next. No fix, closure, acceptance or next-role action has occurred.
- No new product/architecture authority is requested for bounded fixes under the existing milestone. The four deferrals and unstarted autonomy demonstration remain unchanged. This reviewer publishes only review-owned governance/evidence records, then stops.

## Checkpoint metadata

- **Generated UTC:** `2026-09-20T08:44:32Z` (discovery attempt 1 implemented and verified; independent review pending)
- **Prepared by:** `agent:ClaudeCode-discovery`, preserving all prior authority decisions
- **Period covered:** Discovery milestone attempt 1 implementation and live conformance from published `25a78bc`
- **Specification status reviewed:** `ACCEPTED`; DISCOVERY-001–006 unchanged — implementation now exists and awaits independent review, not yet accepted
- **Implementation/reference state:** Root discovery bridges (`AGENTS.md`/`CLAUDE.md`), evolved package adoption guidance, deterministic tests, live probe harness and fixture added within the milestone's allowed paths; ten-file reusable package inventory unchanged; demonstration remains AUTHORIZED attempt 0 at order 6
- **Prior checkpoint:** Exact prior owner summary remains recoverable with `git show 25a78bc:HUMAN_CHECKPOINT.md`; prior accepted decisions/reviews are not rewritten

## System mental model

The product remains a Markdown-first, repository-native engineering protocol. Its root development instance is separately governed from the reusable ten-file package. The seven-tier truth hierarchy, authority/review distinction, evidence ownership, lifecycle and role separation remain unchanged.

Discovery is a new **entry** requirement: a supported fresh participant must find the adopted protocol from normal repository startup/interaction with only an ordinary work request. Discovery never grants implementation authority. Pipeline/dispatcher/rotation are existing root execution mechanisms after recovery, not a substitute for entry discovery.

## Material changes since the prior checkpoint

| Change | Reason and authority | Consequence |
|---|---|---|
| DISCOVERY-001–006 plus explicit onboarding/plug-and-play supersession | Owner reports real usage failure and approved the requirement/authority plan; [gap analysis](EVIDENCE/EVIDENCE-20260918T064510Z-discovery-authority-analysis.md) distinguishes verified repository gaps from the unreproduced external incident | Onboarding prompt becomes fallback/diagnostic, not a normal supported-host prerequisite; no retroactive support claim |
| Four-layer discovery boundary | [Accepted ADR](ADR/ADR-20260918T064510Z-protocol-discovery-boundary.md), owner-approved before implementation | Repository-native authority → scoped adoption signal → subordinate host adapter; unsupported hosts retain manual fallback |
| First implementation/conformance scope | Owner selected Codex CLI plus Claude Code | Both require real fresh-session evidence; neither is currently certified by this record |
| Discovery-first scheduling | Owner explicitly chose new work before the unstarted demonstration | New order-5 contract; demonstration order 5→6 and digest rebinding only; first four accepted entries/digests and all old ADR originals remain unchanged |
| Discovery attempt 1 implementation | Accepted milestone scope; executed by `agent:ClaudeCode-discovery` | Root `AGENTS.md`/`CLAUDE.md` thin bridges with a governed-scope rule; package quick start installs a one-time bridge and demotes the onboarding prompt to manual fallback; deterministic tests plus bounded live harness and fixture |
| First live conformance evidence | [Live conformance evidence](EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md): 57 bounded fresh sessions | Claude Code `2.1.118` passed root and subdirectory starts plus all negative cases; Codex CLI `0.153.4` passed root start and negatives but not subdirectory start reliably (2/3), which is not claimed; a nested-scope failure found in round 1 was repaired by the bridge scope sentence and re-verified |

## Architecture decisions

- **Accepted now:** `ADR-20260918T064510Z-protocol-discovery-boundary` defines responsibilities and compatibility. It does not make AGENTS.md, CLAUDE.md, a hook, a skill or any other host convention normative protocol authority.
- **Retained:** Root adoption, authorized pipeline, dispatch, rotation and autonomy ADRs; source precedence and role/state-machine interfaces.
- **Implementation boundary:** Thin repository-local entry bridges, necessary root/package adoption/onboarding guidance, deterministic/real conformance tests and durable records. Ten Markdown core files remain self-contained; peripheral host artifacts preserve existing instructions. No global personal configuration or new infrastructure is required.
- **Escalation boundary:** A needed security/trust, dependency, scope or architecture change not covered by this contract requires owner authority. Routine work within the accepted milestone does not.
- **Proposed/disputed decisions:** None pending within the accepted slice. Specific host loading details must be verified before reliance, not invented.

## Complexity and architecture drift

New complexity is limited to the two thin root bridges, scoped adoption guidance, the deterministic/live discovery test pair with its fixture, and maintained conformance evidence, owned by the [discovery issue](ISSUES/ISSUE-20260918T064510Z-prompt-independent-discovery.md). No pipeline, dispatcher, rotation, or runtime interface change was made.

The reusable package no longer requires per-task onboarding on verified profiles: adoption installs a one-time bridge, and the onboarding prompt remains as documented manual fallback. The attempt-1 target awaits independent review including the authority boundary and root/product alignment; nothing is accepted yet.

## Assumptions and uncertainty that changed

| Certainty | Statement | Consequence |
|---|---|---|
| CONFIRMED | Existing onboarding/launcher prompts contain explicit protocol reminders | Their success does not establish task-independent discovery |
| CONFIRMED | Owner approved initial two-harness scope and discovery-first order | Requirements, ADR and contracts now carry durable authority |
| CONFIRMED | Claude Code root/subdirectory and Codex CLI root activation are demonstrated on the probed host with final fixture bytes | Support claims are bounded to those tested profiles; Codex subdirectory start is explicitly not claimed |
| UNKNOWN | Exact external incident reproduction | Report is attributed to owner; no trace or external repository evidence fabricated |
| UNKNOWN | Cross-host/version reliability | Changed versions or loading behavior require revalidation before claims move |
| UNKNOWN | Unattended AUTONOMY-004 demonstration | Still unperformed; component acceptance and discovery conformance cannot substitute for it |

## Confidence and verification

- The full deterministic suite passes 124 tests (exit `0`) and `validate_protocol.py` passes on Darwin arm64/Python 3.9.6.
- [Live conformance evidence](EVIDENCE/EVIDENCE-20260920T080830Z-discovery-live-conformance.md) records 57 bounded fresh sessions with per-run JSON records, fixture manifests and tool-event chronologies; the 28-run final matrix used identical final fixture bytes.
- This checkpoint accompanies the attempt-1 implementation target; publication equality of local/cached/direct remote refs must be established from Git.
- No independent review or recorder acceptance exists for this target; the implementer stopped at the review boundary and made no self-approval.
- Dedicated Markdown linters are unavailable; full CommonMark, external URLs and fragment targets are outside the performed structural checks. Original incident reproduction, authenticated identity, concurrent writers, scale and production readiness are not established.

## Human attention required

No further routine decision is required to implement the accepted discovery milestone. The owner has approved the requirement and abstract architecture, two-harness initial scope, priority change and phase stop boundary. Escalate only if implementation exposes authority not covered by those records; do not convert a failed probe or ordinary fix/re-review loop into redundant human approval.

Four prior deferrals remain BLOCKED: concurrent-writer guarantees, authenticated identity/approval, large-scale coordination and external tracker integration. Nothing here resolves or expands them.

## No human attention required

The independent reviewer follows the dispatcher and role contract for the frozen attempt-1 target; fixes stay within the accepted scope or escalate. The implementer has stopped at the review boundary.

The demonstration retains its original lifecycle acceptance conditions: when selected later, runner-launched participants must perform the complete lifecycle; no manual transition is authorized as a shortcut to its evidence.

## Next checkpoint trigger

- **Trigger:** Missing authority, material review ambiguity, proposed boundary expansion, conformance evidence unable to support the intended contract, or milestone acceptance
- **Expected owner action before then:** NONE; the next participant is the independent reviewer of the attempt-1 target, followed by the recorder lifecycle per the existing contract.
