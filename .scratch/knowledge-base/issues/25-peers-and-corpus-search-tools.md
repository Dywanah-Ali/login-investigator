# 25: Peers and corpus search as tools

Type: build
Status: ready-for-agent
Blocked by: 22, 24, 49, 50
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

The analyst asks "who else uses this laptop?" or "what does our policy say about MFA exceptions?",
and the agent answers through `find_peers` or `search_corpus`. Both follow the tracer bullet of
ticket 24: typed, read-only, fenced, short content for the model and a full artifact.

## Decisions implemented

- T05 d1 (`find_peers(account_id | device_id)` and
  `search_corpus(question, doc_type, technique_id)`; the `network` form was removed by the
  author's gate ruling of 1 November 2026), T05 d4 (content plus artifact), T05 d12
  (package caps: five chunks per search, peers paged with a `truncated` flag, full lists in the
  artifact), T03 d6 (the model picks typed options; code builds the filter; the model never writes
  one), T03 d1 (the verdict travels with the chunks).
- User stories 8, 17, 28. Spec door 3.

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

- [x] Complete the separate shared-address value-review session and record the author's scope
      ruling before any T25 implementation. Done 1 November 2026: remove everywhere; see Comments.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `find_peers` returns the users sharing a device with an account or device, from the graph,
      paged with a `truncated` flag; the full list is in the artifact. It has no network form
      and returns no address-sharing context (author, 1 November 2026).
- [ ] Optional `start` and `end` filter login-based relationships through T19's shared core.
      Omitted bounds use the available log period; results state period and coverage. Tests
      cover explicit and omitted dates. Organisation permissions remain a snapshot.
- [ ] `search_corpus` takes typed options, builds the filter in code, and returns the verdict with up
      to five chunks; the artifact records every score.
- [ ] Both are in the one tool tuple and their results are fenced.
- [ ] Agent tests use the fake model.
- [ ] The Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

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
