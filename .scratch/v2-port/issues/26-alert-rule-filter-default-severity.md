# 26: Rule filter and default severity on Alerts

Type: task
Status: ready-for-agent
Blocked by: 19

## Author-approved direction

Approved on 18 October 2026, prompt P-044, following research ticket 25.
This is an enhancement after Parity, not an additional condition for closing the Port.

- Rule filter: All rules plus the four existing rule categories. No new detection rules.
- Deterministic default severity per rule, meaning review priority rather than confidence,
  confirmed compromise, or assessed business impact.

| Rule | Approved default |
| --- | --- |
| Brute force | Medium |
| Password spraying | Medium |
| Success after repeated failures | High |
| Sign-in from a new country | Low |

Research evidence: [25-login-alert-severity.md](../research/25-login-alert-severity.md).
These are project policy defaults, not industry-mandated scores.

## Before implementation

- Finish ticket 19's Parity acceptance.
- Write the filter input, severity output and policy home into a reviewed contract/design note.
  The core owns the meaning; the API and screen consume it.
- Agree the exact severity-column explanation and table/report distinction with the author.
  The existing report policy is not changed by this approval. In particular, an isolated
  new-country finding's default Low can differ from the report's current Medium criterion;
  resolve the user-facing explanation before shipping. No silent prompt or grader changes.
- Agree badge treatment on the existing screen. Research proposed blue/amber/red with visible
  words; the current approval establishes severity values, not an unreviewed screen implementation.

## Acceptance

- [ ] Rule filter composes with existing filters, preserves meaningful URL state, resets paging,
  supports reset and displays a clear empty state.
- [ ] Only the existing four categories are offered, with All rules as the default.
- [ ] One deterministic policy provides the approved default and an explanation for each rule.
- [ ] API contract is written before implementation and the frontend reads the defined API fields.
- [ ] Severity labels are visible as text and use the agreed accessible visual treatment.
- [ ] Zero successful rows in a failure-only finding is never presented as proof no login succeeded.
- [ ] High means urgent review of observed success, not confirmed attacker access.
- [ ] Table defaults and report assessment have the agreed explicit distinction.
- [ ] Meaningful API and frontend checks pass; report behaviour and existing findings stay intact.
- [ ] Author reviews the live change before any push.

## Comments

This ticket records the approved follow-up. It is blocked on the Port closing and is not started.
Perplexity remains a Codex development tool only. No Perplexity integration in the application.

- 20 October 2026. Started on branch `ticket-26-rule-filter-severity`. The author agreed that no
  new research is needed, because ticket 25 covered it; the open items are decisions (P-112,
  P-113). Design note drafted: [26-design-note.md](../research/26-design-note.md). Badge
  colours reuse the report card's blue, orange and red; all six pairs measured at 8.2:1 or
  better.
- 20 October 2026. Author chose **Option A** for the table/report distinction (P-114): the
  column stays "Severity", and the details panel explains that it is the rule's default review
  urgency while a report weighs all the evidence and can rate the case differently. Approval of
  the note as a whole is pending.
- 20 October 2026. Author approved the design note as a whole (P-115). `docs/api-contract.md`
  and the spec's decisions log updated before any code. Build started.
