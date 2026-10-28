# 19: The graph, its integrity check and the S6 radius test

Type: build
Status: resolved
Blocked by: 12, 17
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The knowledge-base door in the core opens a dataset's knowledge base and builds the graph in
NetworkX from the database's tables, with chunks as nodes joined by `mentions` edges and the
`used address` edges drawn from the log. An integrity check runs every time the graph is built and
fails on the first mismatch. One core function computes a finding's blast radius, and a test proves
it gives exactly the S6 radius written in `truth.json`.

## Decisions implemented

- T02 d2 (walked in NetworkX, built in memory, named traversal functions), T02 d7 (chunks as nodes
  with `mentions` edges).
- [review ruling 1] `used address` edges come from the log, one per distinct user and address pair
  for addresses in the networks table, never copied into a table; the integrity check compares
  identities, not only counts; a chunk may have no `mentions` edge; no isolated person, group, asset
  or device.
- T05 R5 (code walks, the agent reads: one radius function, shared by the tool and the answer-key
  test). The hop-by-hop walk is a phase 4 seam, not built.
- T06 comment of 24 October 2026 (the integrity check).
- Author's ruling of 25 October 2026 at the ticket cut: the answer-key radius test lives here, at
  door 2, instead of at the generator's door.
- User stories 57, 69. Spec door 2.

## Answer

### 1. Successful sign-ins establish `used address` edges (author, 28 October 2026)

Only successful sign-ins create an account-to-address edge, still limited to addresses in the
networks table. The edge means the account successfully authenticated from that address; it does
not establish that the legitimate owner signed in, that accounts shared a device, or that an
attack spread. Failed attempts remain in the login records for investigation, but their targeted
usernames do not create these graph edges. The author chose this meaning to avoid adding noisy
target relationships to the network-use graph. During implementation, record the same filter
beside the radius in `truth.json` and apply it independently in the integrity check.

### 2. VPN pool addresses are session-assigned and reused (author, 28 October 2026)

Follow the existing remote-access policy: the synthetic VPN pool represents addresses assigned
to VPN sessions and later reused, not public VPN exit addresses. An account matching another
account's pool address at a different time establishes address reuse only, not shared-device
use, simultaneous connectivity, exposure or spread. The author agreed to review the value and
wording of S6's ten network matches before choosing a time window. Removing those matches,
changing the answer key, adding allocation telemetry and choosing a time window are not yet
approved. No dataset or application changes made by this ruling.

### 3. Address reuse is context, not exposure (author, 28 October 2026)

Retain S6's ten VPN address-reuse matches as clearly labelled supporting context, outside any
exposed-account count. Neither the graph result nor its later agent/screen presentation may
describe these matches alone as exposed accounts or attack spread. This settles the presentation
question left open in decision 2. During T19 implementation, align the answer-key structure and
tests with this distinction while preserving the expected match identities. The time window
remains undecided; no additional telemetry is approved.

### 4. User-selected dates, available log period by default (author, 28 October 2026)

The graph's login-based relationship calculations accept optional start and end times. Explicit
user dates take precedence; omitted bounds use the available log period. Results state the
requested/effective period and available coverage, so missing records are not presented as a
complete investigation. Follow the existing log tools' UTC convention: start included, end
excluded. The planned `find_peers` and `investigate_alert` tools pass these dates to the shared
core calculation (T25 and T26). Dates filter login evidence; organisation permissions remain a
snapshot, not historical permissions. This supersedes the undecided window in decisions 2 and 3
and the ticket's earlier fixed "that week" wording. S6's ten reuse matches remain expected for
the default full-log period; explicit narrower periods may return fewer or none.

### 5. Include all shared addresses, grouped by address (author, 28 October 2026)

The first independent S6 radius test exposed an omission in the planted answer key: Amelia also
shares the UK office address with 43 other accounts. The author chose to include both office and
VPN matches, grouped by address. Preserve the ten VPN matches and add the office matches in the
answer key. All remain context outside exposure counts; accounts appearing in both groups must
not be presented as distinct exposed people. This supersedes the earlier expectation of only
ten address matches overall, while preserving those ten within the VPN group. Source: B-092.

### 6. Implementation

- NetworkX 3.6.1, pinned in the backend lockfile. No new server or database schema.
- `open_knowledge_base(settings, dataset=...)` checks the stored fingerprint, builds the graph,
  independently reconciles it, then yields it. Existing storage-only callers omit `dataset`.
  Reader settings use the existing read-only database role and pool lifecycle.
- Organisation and chunk IDs are graph IDs. Directed relationships are keyed by type, allowing
  assigned-device and observed-device edges between the same nodes. Every successful sign-in
  contributes timestamped `used_address` edges for known networks and `used_device` edges for
  registered nonempty devices. Unknown successful accounts/devices fail loudly.
- The integrity checker has its own database reads, relationship mappings and CSV reading.
  It compares identities, all stored entity attributes, chunk text/metadata, typed edge sets,
  per-edge timestamps and isolation. It never calls the builder to obtain expected values.
- `kb.finding_radius(finding, start=None, end=None)` returns joined records through frozen
  result dataclasses. Spray/brute-force radius subjects are accounts successfully accessed by
  the finding's addresses in the chosen period; failed targets alone do not gain a radius.
  Both ends of a shared-device/address relationship need successful observations in the period.
  Registered device assignments and permissions remain snapshot facts.
- Requested bounds follow the log tools. Effective coverage is their intersection with record
  bounds; no overlap yields null effective bounds. The log's second-resolution last event is
  included with an exclusive end one second later. Record bounds do not imply continuous logging.
- S6's generator key now separates access paths from address-context paths, with 43 office and
  ten VPN matches. The graph recomputes them from storage and log edges, never from the key.
- The live build was rebuilt as `li_kb_fe13d09e32f4` for $0.00111362. Its reader opens 490 nodes
  and 583 edges and returns S6's two groups, seven assets, zero device peers and both context
  groups. Evidence: `evidence/19-rebuild-2026-10-28.json` and `19-live-graph-2026-10-28.json`.
- Parallel Standards and Spec reviews found zero substantive findings on each axis. See
  `reviews/19-code-review-2026-10-28.md`. Core implementation commit: `69bee51`.

## Acceptance criteria

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] One function opens a dataset's knowledge base; the graph is built in NetworkX from the tables,
      with chunk nodes and `mentions` edges.
- [x] `used address` edges are drawn from the log. The row filter (for example, successful sign-ins
      only) is fixed here and written beside the radius in `truth.json`.
- [x] The integrity check reads its sources with its own code and checks every row of the spec's
      table: node ID sets per type, the node attributes a walk reads, link edge sets by source,
      target and type, the `used address` set from the log with the same filter, chunk node IDs, and
      each chunk's `mentions` edges including an empty set. No person, group, asset or device is
      isolated.
- [x] Corruption tests: each check fails when its input is broken once; swapping two valid link
      endpoints without changing any count fails; changing an attribute a walk reads fails; a chunk
      naming no entity passes; an unused network address passes.
- [x] One core function computes a finding's radius, already joined: groups held, assets reached,
      peers with optional dates for login-based relationships, per decision 4.
- [x] Address-reuse matches are explicitly labelled supporting context and excluded from any
      exposed-account count. The result and answer-key tests preserve S6's ten expected match
      identities under the agreed context meaning for the default full-log period.
- [x] Tests prove explicit dates filter login-based relationships, omitted dates use available
      records, boundary handling follows the log tools, and results state period and coverage.
- [x] A test recomputes S6's radius from the tables through that function and matches `truth.json`
      exactly.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-28: author accepted the rules and invoked `$implement T19`. Codex implements on
  confirmed Astra. Tests use the already agreed door 2 seam: opening the knowledge base,
  independently checking integrity, and computing a finding's radius. Base: `4210144` on main;
  existing uncommitted changes are this session's approved T19 planning and audit records.

- 2026-10-28, dataset inspection during relationship discussion: the remote-access policy describes
  session-assigned, reused VPN pool addresses, not explicitly public exits. The generator places
  them in `source_ip` without a separate original-client address or allocation interval. B-091 /
  AUD-060 records the unresolved observation point. No change to these semantics is approved.
  The proposed seven-day window ending at the finding is also not agreed: S6 starts at 02:00 on
  7 October, while the planted VPN peer rows start at 11:00 that day. Check the full finding times
  and answer-key scope before proposing a final window.

- 2026-10-28: the author confirmed Codex is on Astra after the ticket's strongest-model requirement
  was presented. Relationship design is being discussed; implementation has not started.

- 2026-10-26, consequence of the author's ruling at ticket 11: `device_id` is empty on attacker rows
  and on employee sign-ins from a phone. An empty value is not a device: it makes no device edge,
  and rows with an empty device are never peers of each other by device.

- 2026-10-28, closure: implemented on author-confirmed Astra after `$implement T19`. All criteria
  verified. Final backend suite: 612 passed in 194.09 s, including 27 graph tests. Frontend:
  149 passed in 37.88 s; backend and frontend type checks clean. Frontend lint exits 0 with the
  same six AUD-009 warnings. Port API eval: 61/63 overall, 15/15 security, gates met; Q02 runs
  2 and 3 omit S2's explicit no-success outcome (B-076 / AUD-047), while reporting S6 correctly.
  No behaviour change or rerun. Eval artifact: `backend/evals/results/2026-10-28-121053-b70d0745.json`.
  Two independent review axes: zero findings each. B-091 to B-095 preserve discussion/test
  iterations. The one failed teardown's test database was removed; focused rerun and full suite
  had no teardown error. AUD-060 closed on the agreed meaning and verified implementation;
  AUD-061 stays a candidate for T44. Live graph checked as the reader; rebuild cost $0.00111362.
  All application changes are in local commit `69bee51`; closure evidence is committed locally
  afterwards. Nothing pushed. Next frontier: ticket 20; ticket 21 is also unblocked.

- 2026-10-28, Codex, follow-up licence check requested by the author: NetworkX 3.6.1;
  [official version-tagged licence](https://raw.githubusercontent.com/networkx/networkx/networkx-3.6.1/LICENSE.txt),
  opened through the web tool and checked against the installed distribution's
  `licenses/LICENSE.txt` and `METADATA` (`License-Expression: BSD-3-Clause`). Confirmed
  permission to use, modify and redistribute, including commercially. Redistribution must
  retain the copyright notice, conditions and disclaimer; developer/contributor names cannot
  be used for endorsement without permission. This verifies the previously unverified licence
  now, not a lookup claimed for the original build. It is not a dependency-wide licence or
  vulnerability audit.
