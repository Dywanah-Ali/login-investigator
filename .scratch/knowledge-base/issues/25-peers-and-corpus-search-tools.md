# 25: Search and read documentary evidence

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 22, 24, 45, 49, 50, 58
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

The researcher retrieves threat knowledge, organisation rules, case context or approved
investigation practice through four purpose-specific interfaces over T58's shared retrieval.
An exact-reference reader returns identified source content and necessary context without
substituting a similar or newer document. This slice is verifiable through the core/tool
boundary before T59's worker and T60's public chat integration.

## Approved ownership — 8 November 2026

The author approved the seven-slice to-tickets plan. T57 takes peer/account/activity evidence;
this ticket owns documentary interfaces, purpose eligibility, exact reading and the approved
source catalogue. It consumes T58 ranking and T57 shared contracts. IC-05–07 and IC-09–11 are
inherited. T45 remains the parent design; no application build is authorised by this handoff.
Historical references below to the old combined peer/corpus scope are superseded by this split.

## Required pre-build gate

Author ruling, 1 November 2026: hold all T25 implementation for a separate dedicated session
reviewing the investigative value of shared network-address context, especially shared VPN exit
addresses. The author doubts that address sharing alone helps an investigation. Context labels
and exclusion from exposure counts do not establish its usefulness.

Identify the concrete investigation question this serves and any additional evidence needed to
make it meaningful. The author must explicitly decide whether to retain, narrow or remove this
part before build work begins. Record that decision here and make any author-approved spec and
decision-log changes. No outcome is assumed; this gate does not itself change the feature scope.
The corpus-search portion is not separately authorized to start during this hold.

**Gate closed, 1 November 2026:** the author ruled that sharing an address answers no
investigation question in this app, added no allocation evidence (AUD-073) and removed
address-sharing context everywhere. Spec and decision-log rows updated. T50 performs the
removal; this ticket now waits for T50. See the three dated Comments below.

## Acceptance criteria

- [x] Shared-address value review completed on 1 November 2026: remove address-sharing
      context everywhere. The historical ruling remains below; T50 performed its removal.
- [ ] Before build, record the model selected under this ticket's Model line and the map's
      guidance, with the author's confirmation. Ticket planning is not build release.
- [ ] Expose the four documentary purposes through centrally registered, research-only tools.
      Bind each operation to trusted task, subject, applicability time and source context.
      Typed model refinements cannot enlarge permissions, add subjects or change required work.
- [ ] Consume T58's paired-build search, five-result limit and stage receipts. Preserve corpus
      and graph routes internally, every recorded score, purpose overlap, historical applicability, necessary
      conditions and competing material. No duplicate ranking implementation or combined-five cap.
- [ ] Implement the extensible approved-source catalogue for the three runbook versions and exact
      investigation sections selected in T45. Enforce mixed-content exclusions, prerequisites
      and source-version approval on search and exact reading. Existing corpus presence is not
      approval. New supported runbooks use content registration, not new tools or agents.
      Source eligibility cannot add mandatory procedure steps. Do not rewrite or ingest sources
      merely to complete this interface; any real source write follows its separate approval.
- [ ] Exact reads use code-issued source/section references and snapshot-bound continuations.
      Support passage, section and outline scopes where the source representation permits them;
      missing context is explicit. No arbitrary paths/URLs, guessed section identity or silent
      latest-version substitution. Distinguish prepared passage text from source-document text.
- [ ] Preserve returned original content, source identity, task attribution and code-owned receipts.
      Keep empty, irrelevant/uncalibrated, failed, unavailable, denied and truncated outcomes
      distinct. Outline metadata is not substantive case evidence. Fencing applies to all results.
- [ ] Verify each purpose and exact reading through the core/tool boundary, including cross-purpose
      policy/exception retrieval, changed or missing versions, forbidden sections, stale
      continuations, unavailable source context and malicious source instructions. Keep original
      gold and record actual model delivery separately from saved artifacts for T29.
- [ ] Define and test bounded exact-read/context policies within the approved guarantees;
      material scope/gate changes need author ruling, routine numeric values do not.
      Document and test catalogue registration/operator tasks when introduced.
- [ ] Agent plumbing tests use a fake model; the existing Port evaluation gate passes when
      the changed behaviour is integrated. T29 retains knowledge-base application acceptance.
- [ ] Apply the current proportional-testing and proof rules: focused affected-behaviour tests,
      relevant types/lint, one scoped review and applicable existing agent evaluations. Fake-model
      tests prove plumbing; evaluation proves model behaviour. Older standing safety-net wording
      does not require full suites after every edit or an extra review campaign. Record third-party
      documentation/version checks and test any changed admin commands.

## Comments

- 2026-11-08 — Author approved moving peer retrieval to T57 and making T25 the documentary
  interface/catalogue/reader owner over T58. T59 consumes these tools; T26 uses the same core
  for baseline searches. Existing commentary is retained as decision history.

- 2026-11-08 — Author approved research-only exposure of investigative retrieval tools in
  T45. The earlier criterion placing these tools in the one tuple now means central registration
  with research-role exposure, not direct chat access. Final interfaces and per-task restrictions
  remain blocked by T45; no build release.

- 2026-11-08 — Author approved keeping T45 as decisions only, followed by scoped LangGraph
  orchestration research and the agreed design review before two additional build tickets are
  defined. This ticket retains peer/search tool ownership pending explicit reconciliation.
  The proposed research-agent ticket consumes shared tool/core capabilities rather than
  duplicating them. Final tool exposure and dependencies must be reconciled before build.

- 2026-11-07 — Author approved T45 before T25 to settle compound and cross-subject
  retrieval responsibilities before building the search tool interface. T45 now blocks
  this ticket. Its rulings must be reconciled here before implementation; no tool split,
  retrieval policy or separate peer-tool implementation is approved by this sequencing change.

- 2026-10-26, consequence of the author's ruling at ticket 11: `device_id` is empty on attacker rows
  and on employee sign-ins from a phone. `find_peers` never treats an empty device as shared, so two
  sign-ins from unregistered machines are not peers by device.

- 2026-10-30 — Author-approved architecture review: T46 blocks further graph integration.
  This combined ticket stays on hold; its corpus-search portion has not been split out.
  If migration is chosen, T46 must add the required migration blockers before it closes.

- 2026-10-30 — T46 resolved with an approved migration. T49 now blocks this ticket until
  the replacement is accepted. Closing the architecture decision does not release this hold.

- 2026-11-01 — After T49 closure and walkthrough, the author required a separate session to
  review shared-address value, particularly VPN addresses, as a gate before T25. The migration
  dependency is resolved; this new author decision gate remains open.

- 2026-11-01 — Gate session, question 1 (which investigation question does sharing an address
  answer?). Author's ruling: **none** in our app. Reason: the documented use, "who else did a
  suspicious address touch?", is already answered by `search_logins(ip=...)` and the spray
  finding, and `find_peers(network)` cannot reach the attacker's address (not in the networks
  table, failures create no edges). Co-users of the office and VPN addresses cannot single anyone
  out: 43 of 50 accounts share the UK office, and without allocation records a VPN match cannot be
  tied to a moment. "Is this address normal for this account?" was set aside as a different
  capability that does not use sharing; it would need its own ruling. Evidence:
  [research note 25](../research/25-shared-address-value.md). Questions 2 (added evidence) and 3
  (retain, narrow or remove) remain open; no spec change yet.

- 2026-11-01 — Gate session, question 2 (what added evidence would make sharing meaningful?).
  The missing piece is the VPN gateway's session allocation record. Author's ruling: **add
  nothing now**; record the gap as a possible phase 3 feature (AUD-073), since the scope ruling
  keeps this initiative to phases 0 and 1. Question 3 (retain, narrow or remove) remains open.

- 2026-11-01 — Gate session, question 3. Author's ruling: **remove everywhere**. Drop the
  network form of `find_peers`, and remove address-sharing context from the radius, the answer
  key, the tests and the spec through a separate cleanup ticket. Reason: an output ruled useless
  should not stay in the system, since the model repeats what it is given (T43), and kept code
  is maintained and tested for ever. This reverses the 28 October 2026 rulings that kept the
  context as labelled supporting context (T19 decisions 3 and 5). Account and device peers and
  corpus search are unaffected. Spec, decision-log, T25/T26 criteria changes and the cleanup
  ticket await the author's approval of the proposed edits; the gate closes when they are recorded.

- 2026-11-01 — Author approved all ten proposed edits. Spec (answer key, VPN meaning, address
  grouping, relationship dates, tool list) and decision log updated; T26 criterion updated;
  [T50](50-remove-address-sharing-context.md) opened and blocks this ticket and T26; map noted.
  Gate closed.
