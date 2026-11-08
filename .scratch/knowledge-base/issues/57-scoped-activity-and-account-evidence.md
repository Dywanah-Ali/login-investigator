# 57: Retrieve scoped activity and account evidence

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 45
Phase: 0

## What to build

A bounded request for login activity, account significance or connected activity returns
source-bound records, paths, code-computed facts and explicit coverage limits through the
shared core and restricted tool boundary. This is a working evidence slice, not a schema-only
ticket. It supplies the reusable non-documentary capabilities for T26 and T59.

Author approved this ownership on 8 November 2026 through to-tickets. T45 is the parent design;
IC-01–04 and IC-07–11, with P-01–03, are inherited. Planning approval is not build release.
Select the build model under the map's model guidance before implementation.

## Acceptance criteria

- [ ] Implement the shared request/evidence contract needed by this slice: six intents,
      task/subject compatibility, code-generated identifiers, strict variants, source binding,
      operation receipts and per-subject outcomes. Other slices extend the same contract;
      they do not invent parallel envelopes. Reject invalid references and distinguish missing
      identity from source unavailability. Demonstrate a valid request through real core operations.
- [ ] Resolve exact findings and dataset-bound login events without guessing identity. Retain
      existing finding-discovery capability through a bounded code-controlled resolution path;
      discovery cannot grant chat direct investigative tool access or silently select an
      ambiguous target. Preserve required source-reputation enrichment and its cache/time limits.
- [ ] Retrieve exact activity, bounded surrounding activity and coverage. Derive default windows
      and explicit authorised ranges under IC-03; establish endpoint semantics and dataset-owned
      reference time without using answer gold. Preserve separate anchors, failures/successes,
      counts over the scoped population, sampling limits and unknown continuous coverage.
- [ ] Return account owner/role/groups and bounded relevant permission paths using shared graph
      functions. Define deterministic relevance selection before coding it. Preserve snapshot
      limitations; no full inventory, invented rights or inference of observed access.
- [ ] Own the peer capability transferred from T25: account/device narrow lookups and involved-device
      activity with dated links, selection basis, pagination and full returned evidence in artifacts.
      Derive same-source activity from login records. Empty device IDs never establish a link.
      Selection and truncation are distinct; no restored address-sharing graph context.
      Preserve explicit-date and omitted-date narrow-peer behaviour: omitted bounds disclose
      the available-log period. This must not replace activity-anchored investigation defaults
      or authorise expanding an already bounded assignment.
- [ ] Use current graph semantics honestly, including log evidence or explicit gaps for failed
      attempts not represented by current device edges. T55 owns the later failed-login edge
      expansion and 30-day dataset; this ticket does not require that future rebuild or change gold.
- [ ] Bind calls to trusted scope and snapshot, fence untrusted results and retain all task/subject
      attribution. Code owns outcomes and counts. Define task-level required operations here;
      T26 composes the full procedure from them. Tool names are replaceable; approved capabilities
      and existing reputation/security requirements are not.
- [ ] Verify exact-record identity, default/explicit windows, counts versus samples, missing role,
      device selection, failed/unavailable/no-match distinctions and scope rejection at the core/tool
      boundary. Reuse exact graph regression evidence as applicable; do not treat a bounded
      selected subset as the full graph gold. T29 owns integrated application acceptance.
- [ ] Apply focused tests and relevant types/lint, the single scoped review and applicable existing
      evaluation gates. Model behaviour needs evaluation evidence; fake-model tests prove plumbing.
      No new mutation suite, mandatory real-host campaign or duplicate full-suite run is added.
      Record library/version/documentation behaviour checks before integration. Update and test
      admin instructions only where operator tasks change.

## Comments

- 2026-11-08 — Approved handoff: T57 owns activity/account/connected evidence and the shared
  contract foundation. T58 owns document ranking, T25 document interfaces, T26 full-procedure
  composition, T59 worker execution and T60 application integration. No application code or
  source data changed during ticket creation; runtime proof remains outstanding.
