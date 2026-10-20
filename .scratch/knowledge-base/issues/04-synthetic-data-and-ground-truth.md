# 04: Synthetic organisation, corpus and ground truth

Type: grilling
Status: open
Blocked by: 02

## Question

How is the synthetic organisation generated (people, accounts, groups, assets, devices,
networks), how does it stay consistent with the existing authentication log and its four rules,
and where does the written ground truth live so every eval question has a gold answer?

## Scope

- Size: tens of people, a handful of groups and assets, a few dozen documents. Enough to test,
  not to impress.
- Linked cases from research note 01, section 5: a spray that never succeeds; a spray followed by
  a success on a privileged account; shared device and shared network cases. Travel, service
  accounts and incidents are later phases and are not generated now, but the generator must leave
  room for them.
- Whether the existing log is kept as is and the organisation is generated to match it, or the
  log is regenerated alongside the organisation from one source of truth.
- The text corpus: which policies and runbooks are written, which ATT&CK pages are included and
  how (copied text with version, or fetched), and how documents are dated and versioned.
- Where generated data and ground truth live in the repo, and how a dataset is swapped (the API
  asks the core for "a dataset").

## Acceptance

- [ ] Generation approach, size and linked cases decided and recorded.
- [ ] Ground-truth format decided: one file that every eval question points at.
- [ ] Relationship to the existing log decided without breaking the Port's tests and eval.
- [ ] Decision recorded here under `## Answer`.

## Comments
