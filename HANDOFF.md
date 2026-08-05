# Collaboration Protocol

Every participant must read this file before starting work and leave it safe for a replacement participant to continue without chat history.

- Update shared current-state fields only when supported by repository evidence, and add a new activity entry for the change.
- Add or update only records attributable to your work. Do not silently rewrite or delete another participant's findings or activity.
- Preserve prior evidence and authorship. Record disagreements as new evidence rather than overwriting history.
- Prefix material claims with `CONFIRMED`, `INFERRED`, or `UNKNOWN`.
- Repository evidence takes precedence over assumptions and summaries. Record verification only when it was actually performed.
- Keep `Current State` as the present snapshot and `Recent Activity` as the explanation of how it changed.
- Leave exactly one bounded item under `Next Action` before stopping.
- Reconcile every non-terminal background task before relying on it; mark a missing process or remote reference `ORPHANED`.
- Propose protocol changes with motivation and compatibility notes in this file, and wait for explicit approval before adopting them.

## Current State

### Repository snapshot

- **CONFIRMED — Source material:** Root `BOOTSTRAP.md` and root `PROJECT_SPEC.md` remain the unchanged governing inputs; this handoff records development state.
- **CONFIRMED — Product state:** Reusable Agent-Native Engineering Protocol v1, the owner-authorized continuity clarification, and MIT licensing are implemented, validated, committed, and published. The isolated pilot completed at target review-record commit `3a8f3922f47dec16144493482bd2b7a150ef5b0a`; its implementation issue is `CLOSED` after independent disposition `APPROVED`.
- **CONFIRMED — Version control:** This directory is an independent Git repository on branch `main`, tracking `origin/main`. The immutable protocol release commit is `a6270ebeb02f936184895dcad32269d8a16a0da5` (`feat: publish agentic engineering protocol v1`).
- **CONFIRMED — Remote:** Public repository `MattSureham/agentic-engineering-protocol` at `https://github.com/MattSureham/agentic-engineering-protocol`, authenticated account `MattSureham`, default branch `main`, remote name `origin`.
- **CONFIRMED — Handoff commit identity:** The remote-aware release HANDOFF is contained by follow-up commit `99ed41874157b0da537b1399bef907c82454fb1e` (`docs: finalize release handoff`). Takeover checks directly verified that local HEAD, `origin/main`, and GitHub `refs/heads/main` matched before pilot edits; the earlier chat-response reference is non-durable and is not relied on.
- **CONFIRMED — Governing documents:** Root `BOOTSTRAP.md` is the collaboration mechanism for developing this repository; root `PROJECT_SPEC.md` is the authoritative product specification.
- **CONFIRMED — Approved architecture:** Keep the root governing documents unchanged and build a copy-ready package under `protocol/` using risk-tiered review and hybrid issue/evidence records.
- **CONFIRMED — Review requirement:** The first complete protocol draft must receive a read-only independent-agent review before the implementation issue closes.
- **CONFIRMED — Real-repository validation:** One bounded local Python 3.9 pilot exercised quick-start migration, context-free implementation, evidence, HANDOFF, and independent review successfully. This establishes only that no material defect was observed within that target and scope; broader portability remains `UNKNOWN`.
- **CONFIRMED — Unresolved design questions:** No architecture question remains. Pilot issue `AEP-20260805T041340Z-readme-migration-gap` records one `LOW` reusable-package usability defect; target-specific review limitations and one reconciled participant-lifecycle omission do not imply protocol defects.

### Prior-art disposition

- **CONFIRMED — Retained:** Certainty labels, five-part HANDOFF shape, exactly one next action, preserved disagreement/evidence, background-task reconciliation, bounded archival, and explicit protocol evolution.
- **CONFIRMED — Redesigned:** HANDOFF is operational continuity rather than canonical product truth; participants reconcile shared snapshots from evidence while preserving authored activity; meaningful issue/evidence detail lives in separate records.
- **CONFIRMED — Removed:** Initialization-task wording, single-file centralization, application-specific examples, vendor assumptions, and the ambiguous claim that undifferentiated repository evidence outranks every other source.
- **CONFIRMED — Generalized:** Human authority boundaries, peer roles, failure recovery, risk-tiered independent review, portable evidence schemas, timestamp identifiers, and version-control-optional operation.

### Constraints

- Preserve the existing root `BOOTSTRAP.md` and `PROJECT_SPEC.md` byte-for-byte.
- Keep the deliverable Markdown- and filesystem-based, language-, framework-, vendor-, CI-, and model-neutral.
- Do not add a CLI, daemon, database, or orchestrator. The only external-repository scope currently authorized is the local-only, non-production fixture at `/Users/matthew/Projects/aep-protocol-pilot`; it has no remote and must not be pushed. No other parent directory or unrelated repository is in scope.
- Do not claim successful verification without recording the command, result, and limitations.

### Verification performed

- `rg --files -g '!**/.git/**' | sort` listed only `BOOTSTRAP.md` and `PROJECT_SPEC.md` before this file was created.
- `wc -l BOOTSTRAP.md PROJECT_SPEC.md` reported 190 and 457 lines respectively.
- `shasum -a 256 BOOTSTRAP.md PROJECT_SPEC.md` reported:
  - `BOOTSTRAP.md`: `8fcfc3fe52608a1b42305bb12696d3f151be468bbbf638918cf93b651414dfe6`
  - `PROJECT_SPEC.md`: `13169319e2be028c470ca96925002b25c000c58ba3a4c5420e652d291df139dd`
- `rg --files protocol | sort` confirmed the six expected core files.
- `wc -l` reported 652 total lines across the six core files.
- `rg -n '^#|^## '` confirmed the expected primary sections, including all five HANDOFF sections.
- Before the later license and release-metadata additions, `rg --files | sort` confirmed the then-approved 14-file state; the published release subsequently contained 16 files as recorded below.
- `wc -l README.md protocol/*.md protocol/*/TEMPLATE.md` reported 1,041 lines across the root README and reusable package.
- Targeted `rg` checks confirmed all five reusable prompt headings and all required human-checkpoint sections.
- A Markdown validator checked 11 deliverable Markdown files, 28 relative links with zero missing targets, final newlines, trailing whitespace, and balanced code fences.
- A clean copy of `protocol/` at `/tmp/aep-protocol-test.YsZLWh` contained exactly the 10 approved package files and passed entry-file/onboarding-heading checks.
- A requirement-coverage assertion pass reported 20/20 checks satisfied across precedence, authority, peer review, evidence, lifecycle, drift, complexity, interruption handling, prompts, onboarding, and the synthetic example.
- Portability scans found no named language, framework, CI, model dependency, project-specific forbidden term, or unfinished TODO/TBD/FIXME/XXX marker.
- Independent reviewer `/root/independent_review` read all 10 package files and the full authoritative specification, checked links/fences/file types/coupling, and returned five findings with disposition `CHANGES REQUIRED`.
- Post-review assertions passed 18/18 targeted checks covering all five findings plus precedence, lifecycle, drift, prompts, failure handling, portability, and unfinished markers.
- Revised-package validation checked the exact 10-file inventory, 23 package-relative links with zero missing, balanced fences, whitespace, five-section HANDOFF order, dependency names, and a clean copy at `/tmp/aep-protocol-rereview.5BZvqz`.
- Follow-up reviewer confirmed all five original findings resolved, inventoried 10 regular files/no symlinks, rechecked links/fences/lifecycles, and recorded aggregate reviewed-state SHA-256 `ecad67529678284dff4ec4121ab5264cd668446f3d15a4066af3fbe2d389c2ec`; disposition remained `CHANGES_REQUIRED` for one new review-policy inconsistency. The aggregation command was not preserved, so the digest is attributed reviewer evidence rather than independently reproducible evidence.
- Final-candidate assertions passed 11/11 checks for risk-tiered README language, `SELF` eligibility/evidence/closure semantics, retained independent-review categories, and preservation of every prior fix; all 23 package-relative links still resolve.
- Final reviewer re-read the authoritative specification and all 10 protocol files/1,059 lines, verified inventory/no symlinks/links/fences/rule consistency, recorded aggregate SHA-256 `60e4ee3261d40bcc71f84101c09a11db3515cdd2be4dd32cbcdfaa9fe3f989ed`, and returned `APPROVED` with no material findings. The unrecorded aggregation procedure prevents independent reproduction; current package state is instead identified reproducibly by Git tree `935cdb22f4472daa61b91d64f26f8893c4046fbf`.
- Final local validation passed 23/23 semantic requirements/consistency assertions; exact 10-file inventory; zero symlinks; 23 relative links with zero missing; Markdown final-newline/whitespace/fence checks; both five-section/one-action HANDOFF schemas; dependency-name scan; UTF-8/ASCII file checks; and an isolated copy at `/tmp/aep-protocol-final.8OU7vo`.
- At the pre-Git final-validation checkpoint, a dedicated Markdown linter was `NOT AVAILABLE` and history/commit verification was not possible because Git metadata did not yet exist. Later release-preparation and takeover checks below supersede only the Git limitation; a dedicated Markdown linter remains unavailable and is not counted as passed.
- Release-preparation validation passed 19/19 continuity/compatibility assertions, including unchanged seven-level precedence, HANDOFF semantics, Human Authority Boundary, review policy, issue lifecycle, evidence, complexity, failure, and prompt rules.
- The updated package retained exactly 10 files, zero symlinks, 23 resolvable relative links, valid Markdown newline/whitespace/fence structure, no named implementation dependency, and an isolated copy at `/tmp/aep-release-prep.gncUzQ`.
- Root governing files remained distinct and byte-stable at their recorded hashes. The MIT license and minimal release `.gitignore` passed structural checks. A dedicated Markdown linter remained `NOT AVAILABLE` and was not counted as passed.
- Git was initialized explicitly with `git init -b main`. The staged release inventory matched all 16 intended files exactly; ignore probes covered OS/editor/cache/temp paths without ignoring `EVIDENCE/result.log`; credential-pattern scanning found no matches.
- `git diff --cached --check` initially identified extra EOF blank lines in root `README.md` and `protocol/EVIDENCE/TEMPLATE.md`; both were removed and the rerun passed with no whitespace errors.
- At the pre-creation checkpoint, `gh api user` returned `MattSureham`, no local remote existed, and GitHub reported `MattSureham/agentic-engineering-protocol` absent. Target absence and race-safety are attributed historical observations that cannot be reconstructed after creation; current remote identity/state was independently reverified during takeover.
- `gh repo create` created `https://github.com/MattSureham/agentic-engineering-protocol` as `PUBLIC` without auto-push and installed the exact HTTPS `origin` URL. The first push created `main`, set upstream tracking, and verified local and remote release SHA equality at `a6270ebeb02f936184895dcad32269d8a16a0da5`.
- Takeover release verification at `2026-08-05T03:50:52Z` confirmed a clean root worktree, local and remote `main` at `99ed41874157b0da537b1399bef907c82454fb1e`, and unchanged protocol Git tree `935cdb22f4472daa61b91d64f26f8893c4046fbf`.
- Pilot initialization created local-only target commits `0491081c7d700ac354b3031342308d6b29d12aca` (seed) and `abb8ce26e31dc90d676ec9df9c7fb69003e68e7a` (protocol initialization), with no remote. Preflight found only the expected `README.md` collision; the application README was preserved and the unmodified protocol guide was copied to `PROTOCOL_GUIDE.md`.
- The target baseline command `python3 -m unittest discover -s tests -v` ran five tests and exited `1` with exactly one failure: encounter order was sorted as `['alpha', 'beta', 'gamma']` instead of `['beta', 'alpha', 'gamma']`.
- Coordinator verification at target HEAD `6a2c0e5d6f3959de7e0648d5ee8494626fff12f0` independently confirmed a clean worktree, the one-expression review diff, five passing tests, `git diff --check`, 52 Markdown links with zero missing, balanced fences/final newlines/whitespace, no symlinks/dependency manifests/remotes, ordered HANDOFF sections, and exactly one independent-review Next Action.
- Final coordinator verification at target HEAD `3a8f3922f47dec16144493482bd2b7a150ef5b0a` confirmed a clean local worktree, no remote, issue `CLOSED`, independent disposition `APPROVED`, five passing tests, commit-ranged `git diff --check`, 56 Markdown links with zero missing, no Markdown integrity findings, no symlinks or dependency manifests, the five ordered HANDOFF sections, and exactly one terminal target action. Root `protocol/` remained byte-unchanged at Git tree `935cdb22f4472daa61b91d64f26f8893c4046fbf`.

### Background tasks

### TASK-20260805T040313Z-pilot-implementation-edges

- **Purpose:** Independently probe target correctness, edge cases, mutation sensitivity, and post-target drift for the parent reviewer.
- **Owner:** `/root/pilot_reviewer`; reviewer child `/root/pilot_reviewer/implementation_edges`.
- **Start time:** `UNKNOWN` exact UTC; spawned after `2026-08-05T04:03:13Z` and completed before `2026-08-05T04:07:54Z`.
- **Process or remote reference:** Collaboration task `/root/pilot_reviewer/implementation_edges`.
- **Query/recovery:** Query the child reference with collaboration agent-status; terminal result is also synthesized in the parent review round.
- **Last observation:** `2026-08-05T04:17:16Z` — coordinator re-queried the terminal collaboration tree.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Child reported no high/medium finding, one low test-sensitivity limitation, 5,253 randomized/edge cases, direct identity/equality checks, and clean target scope; parent expanded and persisted the accepted review round.

### TASK-20260805T040313Z-pilot-authority-contracts

- **Purpose:** Independently audit target authority, contract coverage, evidence precision, and closure eligibility for the parent reviewer.
- **Owner:** `/root/pilot_reviewer`; reviewer child `/root/pilot_reviewer/authority_contracts`.
- **Start time:** `UNKNOWN` exact UTC; spawned after `2026-08-05T04:03:13Z` and completed before `2026-08-05T04:07:54Z`.
- **Process or remote reference:** Collaboration task `/root/pilot_reviewer/authority_contracts`.
- **Query/recovery:** Query the child reference with collaboration agent-status; terminal result is also synthesized in the parent review round.
- **Last observation:** `2026-08-05T04:17:16Z` — coordinator re-queried the terminal collaboration tree.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Child reported no high/medium finding, low fresh-result test coverage and historical diff-scope limitations, direct adversarial checks, and no authority/architecture contradiction; parent persisted both limitations.

### TASK-20260805T040210Z-pilot-independent-review

- **Purpose:** Independently review accepted REQ-ORDER-001, exact target commit `0606979a57d821e3777d1b81e0834512d9a184d0`, tests, evidence, and protocol records.
- **Owner:** `Codex/root`; reviewer `/root/pilot_reviewer`.
- **Start time:** `2026-08-05T04:02:10Z`.
- **Process or remote reference:** Collaboration task `/root/pilot_reviewer`.
- **Query/recovery:** Query `/root/pilot_reviewer` with the collaboration agent-status or wait mechanism; durable review is appended in the target issue.
- **Last observation:** `2026-08-05T04:07:54Z` — review and terminal target HANDOFF committed; terminal report subsequently received.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Target review-record commit `3a8f3922f47dec16144493482bd2b7a150ef5b0a`; complete issue review round with disposition `APPROVED`; terminal target HANDOFF; coordinator rerun recorded above.

### TASK-20260805T035313Z-fresh-pilot-implementor

- **Purpose:** Initialize live protocol records and implement accepted `REQ-ORDER-001` in the isolated pilot fixture.
- **Owner:** `Codex/root`; implementor `/root/pilot_implementor`.
- **Start time:** `2026-08-05T03:53:13Z`.
- **Process or remote reference:** Collaboration task `/root/pilot_implementor`.
- **Query/recovery:** Query `/root/pilot_implementor` with the collaboration agent-status or wait mechanism; all durable work belongs in `/Users/matthew/Projects/aep-protocol-pilot`.
- **Last observation:** `2026-08-05T03:59:52Z` — target review handoff committed; terminal report subsequently received.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Target commits `0606979a57d821e3777d1b81e0834512d9a184d0` and `6a2c0e5d6f3959de7e0648d5ee8494626fff12f0`; target issue, two evidence records, and HANDOFF; coordinator rerun recorded above.

### TASK-20260805T021914Z-independent-review

- **Purpose:** Read-only independent review of the complete protocol against root `PROJECT_SPEC.md`.
- **Owner:** `Codex/root`; reviewer `/root/independent_review`.
- **Start time:** `UNKNOWN` exact UTC; spawned between `2026-08-05T02:14:40Z` and `2026-08-05T02:19:14Z`.
- **Process or remote reference:** Collaboration task `/root/independent_review`.
- **Query/recovery:** Query `/root/independent_review` with the collaboration agent-status or wait mechanism.
- **Last observation:** `2026-08-05T02:27:44Z` — final report received.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Independent-review findings recorded in Recent Activity at `2026-08-05T02:27:44Z`; disposition `CHANGES REQUIRED`.

### TASK-20260805T023258Z-independent-rereview

- **Purpose:** Read-only follow-up review of all corrections and the complete revised protocol.
- **Owner:** `Codex/root`; reviewer `/root/independent_review`.
- **Start time:** `2026-08-05T02:32:58Z` recorded immediately after triggering follow-up.
- **Process or remote reference:** Collaboration task `/root/independent_review`, follow-up round 2.
- **Query/recovery:** Query `/root/independent_review` with the collaboration agent-status or wait mechanism.
- **Last observation:** `2026-08-05T02:39:10Z` — final follow-up report received.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Follow-up findings recorded in Recent Activity at `2026-08-05T02:39:10Z`; five prior findings resolved, one new medium finding, disposition `CHANGES_REQUIRED`.

### TASK-20260805T024052Z-final-review

- **Purpose:** Final read-only independent review of risk-tiered review semantics and regression scan.
- **Owner:** `Codex/root`; reviewer `/root/independent_review`.
- **Start time:** `2026-08-05T02:40:52Z` recorded immediately after triggering review round 3.
- **Process or remote reference:** Collaboration task `/root/independent_review`, follow-up round 3.
- **Query/recovery:** Query `/root/independent_review` with the collaboration agent-status or wait mechanism.
- **Last observation:** `2026-08-05T02:43:13Z` — final report received.
- **State:** `SUCCEEDED`
- **Terminal evidence:** Final-review entry at `2026-08-05T02:43:13Z`; disposition `APPROVED`, no material findings.

When a task is started, record: stable ID, purpose, owner, start time, process or remote reference, query/recovery command, last observation, state, and terminal evidence. Allowed states are `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, and `ORPHANED`.

## Active Issues

### AEP-20260805T041340Z-readme-migration-gap

- **Status:** `OPEN`
- **Severity:** `LOW`
- **Owner:** `UNASSIGNED`
- **Authority:** `HUMAN` — any protocol-evolution change must be proposed with motivation and compatibility notes and explicitly approved before adoption.
- **Review:** `SELF` for investigation/proposal only; reclassify if the eventual change alters protocol semantics or gates.
- **Problem:** The quick start correctly prohibits overwriting existing protocol files but copies package `README.md` to the conventional application `README.md` path and supplies no canonical merge or alternate-name procedure for established repositories.
- **Evidence:** Pilot preflight found the collision before copy. Safe continuation required a coordinator-invented migration: preserve application `README.md`, copy the byte-identical guide as `PROTOCOL_GUIDE.md`, and add navigation links. See `PILOT_EVIDENCE.md`.
- **Resolution state:** Unresolved usability friction. No reusable source was changed during the pilot.

### AEP-20260805T035052Z-real-repository-pilot

- **Status:** `CLOSED`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN` — the technical owner authorized the isolated target and accepted `REQ-ORDER-001` at `2026-08-05T03:48:23Z`.
- **Review:** `INDEPENDENT` — the seeded public behavior change requires a different participant to approve the reviewed target state.
- **Problem:** Validate quick-start migration, fresh-agent continuity, implementation, evidence, handoff, and independent review in one bounded non-production software repository.
- **Evidence:** Complete target revision chain, commands, results, task references, findings, and limitations are consolidated in root `PILOT_EVIDENCE.md`; target issue and evidence remain inspectable at the authorized local path.
- **Resolution state:** Complete. Context-free implementation and coordinator checks passed; a different fresh reviewer returned `APPROVED`, closed the target issue, and recorded two low non-blocking limitations. Final coordinator verification passed without changing the target.

### AEP-20260805T020501Z-protocol-v1

- **Status:** `CLOSED`
- **Severity:** `HIGH`
- **Owner:** `Codex/root`
- **Problem:** Produce the standalone reusable protocol defined by `PROJECT_SPEC.md` without conflating it with the current root collaboration mechanism.
- **Evidence:** Root `PROJECT_SPEC.md`; approved implementation plan; repository inventory and hashes recorded above.
- **Resolution state:** Complete. All recorded findings are resolved, final validation passed, and independent review round 3 returned `APPROVED`.

### AEP-20260805T031247Z-release-preparation

- **Status:** `CLOSED`
- **Severity:** `MEDIUM`
- **Owner:** `Codex/root`
- **Authority:** `HUMAN` — explicitly approved by the technical owner in the release-preparation request and approved plan.
- **Review:** `SELF` — the continuity wording clarifies existing behavior and does not change source precedence, authority boundaries, review gates, lifecycle, or evidence semantics.
- **Problem:** Add the agent-identity-independent continuity principle, license and validate the release, initialize this directory as its own Git repository, publish a new public GitHub remote safely, and leave the pilot as the sole next action.
- **Evidence:** User-approved release-preparation plan; preflight inspection at `2026-08-05T03:12:47Z`; attributed pre-creation account/target-absence checks; published commits and current remote state recorded above. The historical target-absence observation cannot be reconstructed after creation.
- **Resolution state:** Complete. Documentation and semantic validation passed; the intended release and follow-up handoff were committed and pushed. Takeover checks independently verified current local/remote equality at `99ed41874157b0da537b1399bef907c82454fb1e`; this replaces reliance on the non-durable release response.

## Next Action

Investigate `AEP-20260805T041340Z-readme-migration-gap` and prepare a protocol-evolution proposal with compatibility and migration consequences; do not edit reusable `protocol/` source before explicit owner approval.

## Recent Activity

### 2026-08-05T04:17:16Z — Codex/root — Pilot Coordinator and Verification Agent

- **Task:** Reconcile independent approval, run terminal verification, classify pilot findings, and close the bounded pilot without modifying reusable source.
- **Context inspected:** Independent reviewer report and subreview findings; target review-record commit, issue, HANDOFF, implementation, tests, evidence, Git history/status/remotes; root governing hashes, protocol tree, current HANDOFF, and pilot evidence.
- **Actions performed:** Terminalized the independent-review task; reran final target and root checks; closed `AEP-20260805T035052Z-real-repository-pilot`; created the sole reusable-package defect issue for README migration friction; distinguished target test/evidence limitations from protocol defects; reconciled stale root Current State claims; finalized `PILOT_EVIDENCE.md`.
- **Files modified:** Root `HANDOFF.md` and `PILOT_EVIDENCE.md` only during final reconciliation. Target state was inspected but not changed; root `protocol/` remained unchanged.
- **Findings:** `CONFIRMED` — independent disposition `APPROVED`, no material target finding, no prohibited complexity, and no post-review product drift. `LOW` protocol usability defect — established-repository README adoption needs an undocumented migration. `LOW` target-only limitations — accepted tests do not explicitly lock equality-vs-identity or fresh-result identity, and implementor diff wording overstated its historical command scope; reviewer directly verified current behavior and commit-range whitespace. `LOW` participant-lifecycle omission — the reviewer used two terminal child review tasks while target HANDOFF claimed no background work; the coordinator recovered and recorded both terminal references above, so no live task remains. `UNKNOWN` — generalization beyond this fixture.
- **Verification performed:** Clean target `3a8f3922f47dec16144493482bd2b7a150ef5b0a`; five-test pass; issue `CLOSED`/review `APPROVED`; commit-ranged whitespace pass; 56 links/zero missing; Markdown integrity, HANDOFF order/one terminal action, remotes/dependencies/symlinks; unchanged root protocol Git tree and governing hashes; root `git diff --check`.
- **Issues created or updated:** Closed `AEP-20260805T035052Z-real-repository-pilot`; created `AEP-20260805T041340Z-readme-migration-gap`; terminalized `TASK-20260805T040210Z-pilot-independent-review` as `SUCCEEDED`.
- **Remaining uncertainty:** Broader language/repository portability and whether the owner wants the LOW README migration gap addressed.
- **Recommended next action:** Prepare the bounded protocol-evolution proposal named under Next Action without changing reusable source.

### 2026-08-05T04:02:10Z — Codex/root — Pilot Coordinator and Verification Agent

- **Task:** Reconcile the context-free implementor and gate the exact state for independent review.
- **Context inspected:** Implementor report; target Git history/status/remotes; accepted specification; exact parent-to-target diff; live issue, evidence, and HANDOFF records; tests; Markdown structure and links; dependency and symlink inventory.
- **Actions performed:** Marked the implementor task `SUCCEEDED`; reran its critical claims directly; confirmed the issue remains `REVIEW`; queued a different context-free reviewer for target commit `0606979a57d821e3777d1b81e0834512d9a184d0`.
- **Files modified:** Root `HANDOFF.md` and `PILOT_EVIDENCE.md`; no target or reusable protocol file changed during coordinator verification.
- **Findings:** `CONFIRMED` — the implementation change is exactly `sorted(set(values))` to `list(dict.fromkeys(values))`; tests/specification are unchanged. `CONFIRMED` — all five accepted tests pass, target records are structurally complete, and prohibited complexity/remotes are absent. `UNKNOWN` — independent-review disposition remains pending.
- **Verification performed:** Clean target HEAD `6a2c0e5d6f3959de7e0648d5ee8494626fff12f0`; scoped Git diff; five-test pass; `git diff --check`; 52 Markdown links/zero missing; final-newline/whitespace/fence checks; HANDOFF order/one action; empty remote, dependency-manifest, and symlink scans.
- **Issues created or updated:** Advanced `AEP-20260805T035052Z-real-repository-pilot` to `REVIEW`; terminalized implementor task and queued `TASK-20260805T040210Z-pilot-independent-review`.
- **Remaining uncertainty:** Independent reviewer findings, final closure consistency, and terminal pilot defect set.
- **Recommended next action:** Run and receive the context-free independent reviewer.

### 2026-08-05T03:53:13Z — Codex/root — Pilot Coordinator

- **Task:** Initialize the owner-authorized isolated pilot and make the fresh implementor resumable before spawn.
- **Context inspected:** Root governing files and HANDOFF; clean local/remote release state; protocol tree and copied-file hashes; target-path absence; Python/Git availability; target copy collisions; seed tests and local Git state.
- **Actions performed:** Created `/Users/matthew/Projects/aep-protocol-pilot` as a local `main` repository with no remote; committed the non-production Python fixture; preflighted all ten package paths; preserved the application README, migrated the package guide to `PROTOCOL_GUIDE.md`, copied the other protocol artifacts, persisted the accepted target specification, committed initialization, and recorded the implementor task.
- **Files modified:** Root `HANDOFF.md`; isolated target source, tests, README, and adopted protocol files. No reusable source under root `protocol/` changed.
- **Findings:** `CONFIRMED` — the raw quick-start copy would collide with a conventional application `README.md`; deliberate migration required an undocumented alternate filename. `CONFIRMED` — the seeded implementation violates accepted encounter order in exactly one of five tests. `CONFIRMED` — the earlier unnamed-target/scope ambiguity is resolved by the owner's explicit isolated-fixture authorization.
- **Verification performed:** Root release/tree checks; exact destination preflight; byte comparison for the nine unmodified copied artifacts; 25 target Markdown links with zero missing; `git diff --check`; target baseline test command exited `1` with one expected failure; target remote list empty and both initialization commits captured.
- **Issues created or updated:** Created `AEP-20260805T035052Z-real-repository-pilot`; queued `TASK-20260805T035313Z-fresh-pilot-implementor`.
- **Remaining uncertainty:** Fresh-agent protocol compliance, minimal fix, target evidence quality, independent review disposition, and terminal portability/usability findings.
- **Recommended next action:** Run and receive the context-free implementor, then inspect its durable target state directly.

### 2026-08-05T03:17:25Z — Codex/root — Release Preparer

- **Task:** Create the guarded public GitHub release and leave a remote-complete handoff without starting the pilot.
- **Context inspected:** Clean initial commit, authenticated GitHub identity, explicit target absence, local remotes, intended remote URL, public visibility, default branch, local/remote branch SHAs, and user-authorized release metadata.
- **Actions performed:** Created initial commit `a6270ebeb02f936184895dcad32269d8a16a0da5`; reverified account `MattSureham` and target absence; created public `MattSureham/agentic-engineering-protocol` without auto-push; verified `origin`; pushed `main`; composed this remote-aware final handoff for the follow-up metadata commit and push.
- **Files modified:** This HANDOFF only after the immutable protocol release commit; remote GitHub repository and `origin` created as explicitly authorized.
- **Findings:** Remote creation was race-safe and did not overwrite an existing repository. GitHub reports the expected identity, public visibility, URL, and `main` default branch.
- **Verification performed:** Initial tree clean; release commit hash captured; `gh api user` identity; explicit pre-create absence; post-create `nameWithOwner`, `PUBLIC`, URL, and `defaultBranch=main`; exact HTTPS origin; upstream tracking; `git rev-parse HEAD` equaled `git ls-remote origin refs/heads/main` at the release commit. Final handoff-commit equality is verified after this file is committed and pushed.
- **Issues created or updated:** Closed `AEP-20260805T031247Z-release-preparation` contingent on the immediately following final handoff commit/push verification; any failure must supersede this entry with a blocker.
- **Remaining uncertainty:** The deliberately deferred real-repository pilot; dedicated Markdown linter remains unavailable; Markdown/Git cannot authenticate human or agent identities by themselves.
- **Recommended next action:** Run the bounded independent fresh-agent pilot stated under Next Action; do not begin another implementation/review cycle before that pilot.

### 2026-08-05T03:15:58Z — Codex/root — Release Preparer

- **Task:** Initialize the independent local Git repository and gate the exact initial release contents.
- **Context inspected:** Local and parent Git boundaries, intended repository inventory, ignore policy, staged paths/statistics, staged whitespace, credential-like token patterns, and Git identity availability.
- **Actions performed:** Initialized branch `main`; staged the 16 intended release files explicitly; removed only the two EOF blank lines reported by Git's whitespace check; restaged and revalidated.
- **Files modified:** Root `README.md`, `protocol/EVIDENCE/TEMPLATE.md`, and this HANDOFF; Git metadata created under this repository only.
- **Findings:** No credentials, caches, OS junk, editor metadata, parent files, symlinks, or unexpected paths are staged. `EVIDENCE/result.log` remains trackable because evidence logs are intentionally not ignored.
- **Verification performed:** Exact 16/16 staged inventory; staged name/status/stat review; ignore-rule probes; credential-pattern scan with no matches; `git diff --cached --check` final pass; branch `main`; configured Git author identity.
- **Issues created or updated:** Advanced `AEP-20260805T031247Z-release-preparation`; it remains `IMPLEMENTING` until local/remote release completion.
- **Remaining uncertainty:** Initial commit hash, immediate GitHub account/repository recheck, remote creation and visibility, both pushes, and final remote HEAD.
- **Recommended next action:** Create the initial release commit, then perform the guarded GitHub pre-creation check.

### 2026-08-05T03:14:33Z — Codex/root — Implementor and Self-Reviewer

- **Task:** Add and reconcile the approved continuity principle, MIT license, and release ignore rules; verify the reusable bundle remains coherent and self-contained.
- **Context inspected:** README opening/philosophy, normative BOOTSTRAP entry and attribution rules, truth precedence, HANDOFF semantics, authority/review/lifecycle/evidence rules, package inventory, license text, and source hashes.
- **Actions performed:** Added the English continuity principles and single Chinese tagline to `protocol/README.md`; added the normative identity/session-independent continuity rule and provenance clarification to `protocol/BOOTSTRAP.md`; added root MIT `LICENSE` and minimal `.gitignore`.
- **Files modified:** `protocol/README.md`, `protocol/BOOTSTRAP.md`, `LICENSE`, `.gitignore`, and this HANDOFF.
- **Findings:** The principle clarifies existing architecture. Agent labels remain necessary for provenance, independent review, and approvals, but neither identity nor session owns truth or continuity. Git history is optional provenance and does not change truth precedence.
- **Verification performed:** 19/19 semantic/compatibility assertions; 10/10 package files; zero symlinks; 23/23 relative links; Markdown newline/whitespace/fence checks; dependency-name scan; unchanged root-source hashes; distinct root/reusable governing files; license/ignore structure; isolated bundle copy at `/tmp/aep-release-prep.gncUzQ`. Dedicated Markdown linter: `NOT AVAILABLE`.
- **Issues created or updated:** Advanced `AEP-20260805T031247Z-release-preparation`; review remains `SELF` because no authority, lifecycle, or review gate changed.
- **Remaining uncertainty:** Exact staged Git content, credential scan, commit identity/hash, GitHub pre-creation recheck, remote creation, and push.
- **Recommended next action:** Initialize Git on `main`, stage the intended release, and inspect it before committing.

### 2026-08-05T03:12:47Z — Codex/root — Release Preparer

- **Task:** Begin the owner-authorized final repository and release-preparation pass without starting the real-repository pilot.
- **Context inspected:** Root collaboration protocol and HANDOFF, reusable README/BOOTSTRAP continuity semantics, complete filesystem inventory, local/parent Git state, governing-source hashes, Git configuration, GitHub CLI authentication, and target remote existence.
- **Actions performed:** Reconfirmed the workspace boundary and opened `AEP-20260805T031247Z-release-preparation`; no product, Git, or remote mutation preceded this entry.
- **Files modified:** This HANDOFF only.
- **Findings:** The requested principle is compatible with existing precedence, HANDOFF, Human Authority Boundary, risk-tiered review, issue lifecycle, and evidence rules. Git history must be described as optional provenance rather than a new truth tier. Participant identity remains audit metadata, not continuity ownership.
- **Verification performed:** Root and parent both returned `not a git repository`; the intended 14 Markdown files were the only filesystem entries; root `BOOTSTRAP.md` and `PROJECT_SPEC.md` retained SHA-256 values `8fcfc3fe52608a1b42305bb12696d3f151be468bbbf638918cf93b651414dfe6` and `13169319e2be028c470ca96925002b25c000c58ba3a4c5420e652d291df139dd`. Planning preflight also confirmed `gh` authenticated as `MattSureham` and the target repository absent; both external facts require immediate pre-creation recheck.
- **Issues created or updated:** Created `AEP-20260805T031247Z-release-preparation` in `IMPLEMENTING` state.
- **Remaining uncertainty:** Post-edit semantic validation, staged-content safety, commit hashes, and remote creation/push outcome.
- **Recommended next action:** Apply the approved documentation, MIT license, and `.gitignore` changes and validate them.

### 2026-08-05T02:44:31Z — Codex/root — Verification Agent

- **Task:** Run final end-to-end verification and close the v1 implementation issue only on a full pass.
- **Context inspected:** Entire final package, root source hashes, both HANDOFF schemas, all independent-review resolutions, portability assumptions, and isolated-copy entry points.
- **Actions performed:** Ran the final semantic, structural, portability, file-type, source-integrity, and clean-copy suite; closed the issue; left one bounded real-repository pilot action.
- **Files modified:** This HANDOFF only.
- **Findings:** All available checks passed. No unresolved design question remains. Dedicated Markdown linting, Git history validation, and an empirical real-repository pilot remain unavailable/not performed and are not claimed as passed.
- **Verification performed:** 23/23 semantic assertions; 10/10 exact package files; zero symlinks; 23/23 relative links; final-newline/whitespace/fence integrity; exact five-section/one-action structure in both HANDOFFs; no named language/framework/CI/model dependency; UTF-8/ASCII files; clean copy at `/tmp/aep-protocol-final.8OU7vo`; unchanged root source hashes.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `VERIFYING` to `CLOSED`.
- **Remaining uncertainty:** Behavior during a real external-repository pilot; Markdown cannot enforce identity, approval, or participant compliance.
- **Recommended next action:** Run the bounded non-production pilot described under Next Action.

### 2026-08-05T02:43:13Z — Codex/root — Review Coordinator

- **Task:** Reconcile final independent review round 3.
- **Context inspected:** Reviewer report for the final candidate, prior resolution history, and reviewed-state evidence.
- **Actions performed:** Marked final review terminal and moved the implementation issue to final verification.
- **Files modified:** This HANDOFF only.
- **Findings:** No material findings. Reviewer confirmed risk-tiered README wording, explicit `SELF` eligibility/evidence/outcomes, conditional closure, and preservation of all earlier fixes.
- **Verification performed:** Reviewer read root `PROJECT_SPEC.md` and all 10 protocol files/1,059 lines; verified inventory, absence of symlinks, links, fences, review semantics, authority routing, debt retention, approval provenance, and portability assumptions. Aggregate reviewed-state SHA-256: `60e4ee3261d40bcc71f84101c09a11db3515cdd2be4dd32cbcdfaa9fe3f989ed`.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `REVIEW` to `VERIFYING`; terminalized `TASK-20260805T024052Z-final-review` as `SUCCEEDED`/`APPROVED`.
- **Remaining uncertainty:** Final local validation and real-project pilot behavior.
- **Recommended next action:** Run final end-to-end validation and close only on full pass.

### 2026-08-05T02:40:52Z — Codex/root — Implementor and Verification Agent

- **Task:** Resolve the round-2 review-policy inconsistency and submit the final candidate for independent review.
- **Context inspected:** README philosophy/workflow wording, normative review classification, issue metadata and closure gates, all prior fixes, and reviewer resolution condition.
- **Actions performed:** Made README explicitly risk-tiered; limited `SELF` to local reversible contract-preserving work; defined mandatory self-review state/scope/evidence/findings/limitations/risks/outcome fields; added conditional `SELF` and `INDEPENDENT` closure gates; launched review round 3.
- **Files modified:** `protocol/BOOTSTRAP.md`, `protocol/ISSUES/TEMPLATE.md`, `protocol/README.md`, and this HANDOFF.
- **Findings:** `SELF` needs a distinct `COMPLETE` outcome that is clearly attributable self-verification and cannot satisfy an independent-review gate.
- **Verification performed:** 11/11 targeted final-candidate assertions; all 23 package-relative links; Markdown fence/whitespace checks; unchanged root-source hashes.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `IMPLEMENTING` to `REVIEW`; recorded `TASK-20260805T024052Z-final-review` as `RUNNING`.
- **Remaining uncertainty:** Final independent disposition and real-project pilot behavior.
- **Recommended next action:** Receive final independent review round 3.

### 2026-08-05T02:39:10Z — Codex/root — Review Coordinator

- **Task:** Reconcile follow-up independent review round 2.
- **Context inspected:** Reviewer report for the revised package and each prior-finding resolution.
- **Actions performed:** Marked the follow-up task terminal, accepted independent confirmation that all five first-round findings are resolved, and returned the issue to `IMPLEMENTING` for one new medium finding.
- **Files modified:** This HANDOFF only.
- **Findings:** README says meaningful changes universally receive independent review, while normative risk-tiered rules permit `review: SELF`. The issue template has independent-review rounds but no explicit self-review record or closure semantics.
- **Verification performed:** Reviewer re-read the full root spec and all package files, computed aggregate reviewed-state hash `ecad67529678284dff4ec4121ab5264cd668446f3d15a4066af3fbe2d389c2ec`, confirmed 10 regular files/no symlinks, and rechecked links, fences, authority routing, review states, provenance, complexity, lifecycle, and tooling assumptions.
- **Issues created or updated:** Kept `AEP-20260805T020501Z-protocol-v1` open and moved it from `REVIEW` to `IMPLEMENTING`.
- **Remaining uncertainty:** Whether final risk-tiered wording and self-review semantics pass independent review.
- **Recommended next action:** Correct the review-policy inconsistency and add self-review completion fields.

### 2026-08-05T02:32:58Z — Codex/root — Implementor and Verification Agent

- **Task:** Resolve all first-round independent-review findings and submit the revised package for follow-up review.
- **Context inspected:** Each reviewer finding and resolution condition, related normative rules, templates, prompts, example, and source-precedence requirements.
- **Actions performed:** Routed product/contract decisions exclusively through accepted specification changes and architecture through ADRs; made accepted uncovered complexity remain an open debt issue; added append-only, standardized review rounds; added complete human approval provenance; changed the example next action to tooling investigation; clarified that DRAFT requirements cannot authorize implementation; launched follow-up review.
- **Files modified:** `protocol/BOOTSTRAP.md`, `protocol/PROJECT_SPEC.md`, `protocol/HANDOFF.md`, `protocol/ISSUES/TEMPLATE.md`, `protocol/ADR/TEMPLATE.md`, `protocol/HUMAN_CHECKPOINT.md`, `protocol/PROMPTS.md`, `protocol/README.md`, `protocol/EXAMPLE.md`, and this HANDOFF.
- **Findings:** The high-severity flaw required separating product authority from architecture authority throughout the workflow, not merely changing the example. Review evidence also required repeatable rounds so follow-up approval cannot erase first-round findings.
- **Verification performed:** 18/18 targeted post-review assertions; exact 10-file package inventory; 23 package link targets; Markdown whitespace/fence checks; dependency-name scan; clean-copy revalidation; unchanged root-source hashes.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `IMPLEMENTING` to `REVIEW`; recorded `TASK-20260805T023258Z-independent-rereview` as `RUNNING`.
- **Remaining uncertainty:** Follow-up reviewer disposition and real-repository pilot behavior.
- **Recommended next action:** Receive the follow-up independent-review report.

### 2026-08-05T02:27:44Z — Codex/root — Review Coordinator

- **Task:** Receive and triage the authorized independent review.
- **Context inspected:** Final report from fresh reviewer `/root/independent_review`, which inspected root `PROJECT_SPEC.md` and all ten package files without implementor context or file edits.
- **Actions performed:** Reconciled the reviewer background task to `SUCCEEDED`, classified every finding as material, and returned the implementation issue to `IMPLEMENTING`.
- **Files modified:** This HANDOFF only.
- **Findings:** `HIGH` — product/public-contract/specification decisions could incorrectly be resolved by a lower-precedence ADR alone. `MEDIUM` — accepted but uncovered complexity could disappear from active tracking. `MEDIUM` — issue/ADR templates lacked repeatable review scope, commands, limitations, residual risks, and standardized disposition. `MEDIUM` — checkpoint approval response lacked responder, UTC time, and durable authority reference. `LOW` — the example called executable-test implementation safe without establishing authorized tooling.
- **Verification performed:** Reviewer read the 457-line authoritative spec and all 10 package files, resolved links, checked fences and file types, scanned coupling, and audited every required workflow area. Reviewer could not inspect Git history or run a Markdown linter because neither was available, and did not perform the already-completed clean-copy write test.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `REVIEW` back to `IMPLEMENTING`; all five findings are tracked within this issue.
- **Remaining uncertainty:** Correctness of the forthcoming fixes and follow-up reviewer disposition.
- **Recommended next action:** Apply and verify all five independent-review corrections.

### 2026-08-05T02:19:14Z — Codex/root — Implementor and Verification Agent

- **Task:** Self-audit the complete package and start an independent read-only review.
- **Context inspected:** Every package artifact, root product requirements, source-truth statements, lifecycle vocabularies, relative links, portability assumptions, and clean-copy behavior.
- **Actions performed:** Replaced one non-resolving instructional HANDOFF link with plain placeholder path text; ran structural, requirement-coverage, portability, and isolated-copy checks; launched a fresh independent reviewer with no inherited implementor context.
- **Files modified:** `protocol/HANDOFF.md` and this HANDOFF.
- **Findings:** The first link check correctly rejected the nonexistent placeholder `ISSUES/file.md`; after correction, all 28 actual relative links resolved. No other self-audit contradiction or missing requirement was found.
- **Verification performed:** Required-file check (10/10); Markdown check (11 files, 28 links, zero missing); clean-copy entry check; 20/20 requirement assertions; dependency/project-term/unfinished-marker scans; unchanged root-source hashes. The first combined validator was blocked before execution because its temporary cleanup command was forbidden; the no-cleanup rerun then exposed and verified the link fix.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `VERIFYING` to `REVIEW`; recorded background task `TASK-20260805T021914Z-independent-review`.
- **Remaining uncertainty:** Independent reviewer findings and real-project pilot behavior remain unknown.
- **Recommended next action:** Receive and triage the independent review report.

### 2026-08-05T02:14:40Z — Codex/root — Implementor

- **Task:** Complete the human-facing documentation, reusable prompts, adoption guide, and synthetic initialization example.
- **Context inspected:** Core protocol contracts, product deliverable list, approved duplication policy, and root collaboration requirements.
- **Actions performed:** Added the human checkpoint template, five role prompts, full package README, synthetic minimal example, and root contributor README.
- **Files modified:** `protocol/HUMAN_CHECKPOINT.md`, `protocol/PROMPTS.md`, `protocol/README.md`, `protocol/EXAMPLE.md`, root `README.md`, and this HANDOFF.
- **Findings:** The prompts can stay transportable by directing participants to the normative BOOTSTRAP. A single synthetic walkthrough demonstrates initialization without maintaining a duplicate example repository or asserting fabricated test success.
- **Verification performed:** Confirmed the 14-file inventory, document line counts, five required prompt headings, all checkpoint sections, and unchanged source-document hashes.
- **Issues created or updated:** Moved `AEP-20260805T020501Z-protocol-v1` from `IMPLEMENTING` to `VERIFYING`.
- **Remaining uncertainty:** Cross-document consistency, all relative links, clean-copy behavior, and independent-review findings remain unverified.
- **Recommended next action:** Run the systematic requirements and portability audit.

### 2026-08-05T02:10:37Z — Codex/root — Implementor

- **Task:** Implement the reusable protocol's normative workflow and core record schemas.
- **Context inspected:** Approved architecture, root product specification, initialized HANDOFF, and the ownership/precedence requirements for each artifact.
- **Actions performed:** Added the copy-ready BOOTSTRAP, PROJECT_SPEC and HANDOFF templates, plus ADR, issue, and evidence templates.
- **Files modified:** `protocol/BOOTSTRAP.md`, `protocol/PROJECT_SPEC.md`, `protocol/HANDOFF.md`, `protocol/ADR/TEMPLATE.md`, `protocol/ISSUES/TEMPLATE.md`, `protocol/EVIDENCE/TEMPLATE.md`, and this HANDOFF.
- **Findings:** A single normative BOOTSTRAP can define the shared lifecycle while templates remain focused on their owned data. HANDOFF can remain compact by indexing meaningful issue and evidence files.
- **Verification performed:** Confirmed file inventory, total line counts, and required Markdown section headings. No behavioral dry run or independent review has occurred yet.
- **Issues created or updated:** Advanced `AEP-20260805T020501Z-protocol-v1`; it remains `IMPLEMENTING`.
- **Remaining uncertainty:** Cross-document links, prompt sufficiency, clean-copy portability, and independent-review findings remain unverified.
- **Recommended next action:** Add the supporting human, prompt, onboarding, and example documents.

### 2026-08-05T02:05:01Z — Codex/root — Implementor

- **Task:** Initialize collaboration continuity before implementing the reusable protocol.
- **Context inspected:** Root `BOOTSTRAP.md`, root `PROJECT_SPEC.md`, repository inventory, filesystem metadata, and approved architecture choices.
- **Actions performed:** Confirmed the initial repository state and created this HANDOFF using the existing root protocol.
- **Files modified:** `HANDOFF.md` only.
- **Findings:** The repository began with exactly two source documents and no Git metadata. The reusable package must remain separate from the root governing BOOTSTRAP.
- **Verification performed:** File inventory, line counts, UTC timestamp capture, and SHA-256 hashes as recorded under `Current State`.
- **Issues created or updated:** Created `AEP-20260805T020501Z-protocol-v1` in `IMPLEMENTING` state.
- **Remaining uncertainty:** Portability and fresh-agent usability remain unverified until the package is drafted, dry-run in a clean directory, and independently reviewed.
- **Recommended next action:** Create the core reusable protocol files and schemas.

## Archived Summary

No activity has been archived.
