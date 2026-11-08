# 55: The 50-person, 30-day investigation dataset

Type: design, then build
Status: ready-for-agent
Blocked by: 52
Blocks: 40
Phase: 0/1 supporting data, before the expanded phase 1 exam
Rigour: Tier 3

## Ownership and scope

Author approved this separate data ticket on 2 November 2026 through T52's ownership ruling.
It owns the existing 50-person/30-day target: generator changes, realistic surrounding login
activity, varied investigation cases, competing documents, corpus/truth consistency and
compatibility evidence. Ownership approval is not implementation approval.

Preserve the existing stories and frozen Port exam. The seven-day generator is the current
baseline, not evidence that the expanded target exists. Exact dates, row/document counts,
new scenario details and compatibility strategy must be agreed before application/data edits.
Do not manufacture evidence to make every investigation resolvable. Thirty days of data does
not establish a behavioural baseline or authorise endpoint telemetry. Account-impact context
stays bounded under the sole login-investigation objective.

T54's four approved controlled screening fixtures remain independent. T40 uses the expanded
world only after this ticket supplies accepted consistency and compatibility evidence.

## Acceptance criteria

- [ ] Author ruling, 8 November 2026: extend used_device to include both successful and failed
      sign-in records with a known nonempty device identity as part of this dataset expansion.
      Carry the change through graph construction, independent integrity verification, dated
      relationship queries and affected evidence/truth checks. Design the representation so
      outcomes remain distinguishable or resolvable from source records; failed attempts must
      not become claims of successful access, physical-human use or authentication to the device.
      Keep assigned_device separate and missing device IDs unlinked. Demonstrate a failure-only
      account/device pair and mixed outcomes in the requested window. Reconcile affected graph
      expectations explicitly; no silent rewrite of frozen questions/gold or gate relaxation.

- [ ] Record an author-approved design covering date range, surrounding activity, case/document
      changes, generator/truth ownership and preservation of existing stories before build.
      Propose any necessary gold/question revision separately; none is implied by this ticket.
- [ ] Record the build model under the map's applicable model guidance before implementation.
- [ ] Generate a reproducible 50-person dataset covering the agreed 30-day period. Record its
      identity, counts and actual coverage. Do not imply complete telemetry from record bounds.
- [ ] Verify agreement among organisation tables, login records, documents, truth and graph
      sources, including controlled ambiguity and missing evidence where intended.
- [ ] Preserve original stories and demonstrate compatibility with the unchanged Port exam;
      retain failures rather than weakening thresholds or rewriting gold to hide them.
- [ ] Hand T40 versioned dataset/corpus/truth identities and case provenance. Keep screening
      fixtures distinct from application acceptance data and the refusal-tuning file.
- [ ] Update the admin manual for any changed generation/rebuild/check command and test the
      commands as written. Run applicable backend/frontend/type/review and eval checks under
      the standing spec rules before acceptance. Keep evidence on this ticket.

## Comments

- 2026-11-08 — Author approved broadening used_device to cover failed attempts as well as
  successful sign-ins, scheduled with the planned seven-to-thirty-day expansion. T45 verified
  that the current builder and independent checker filter to success only. This is a future
  semantic/build change, not a claim of current support. Exact representation and compatibility
  belong in this ticket's pre-build design; no immediate graph/data rebuild authorised.

- 2026-11-02 — Author approved the allocation in chat: T45 selects guidance sources for
  review, T26 integrates approved guidance, and a separate ticket owns this dataset. This
  ticket materialises that last responsibility; no data generation or build has started.
