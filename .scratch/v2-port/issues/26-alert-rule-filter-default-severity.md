# 26: Rule filter and default severity on Alerts

Type: task
Status: ready-for-human
Blocked by: 19 (resolved)

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

- [x] Rule filter composes with existing filters, preserves meaningful URL state, resets paging,
  supports reset and displays a clear empty state. Evidence: `test_dashboard.py` and
  `test_api_dashboard.py` rule tests; `alerts.test.tsx` "the Rule filter (ticket 26)".
- [x] Only the existing four categories are offered, with All rules as the default. Evidence:
  options test reads All plus four titles from the rules reply; unknown keys refused (422).
- [x] One deterministic policy provides the approved default and an explanation for each rule.
  Evidence: `backend/login_investigator/severity.py`, `test_severity.py`.
- [x] API contract is written before implementation and the frontend reads the defined API fields.
  Evidence: commit fe28a37 precedes the code; `/api/rules` test pins the new fields.
- [x] Severity labels are visible as text and use the agreed accessible visual treatment.
  Evidence: table and panel tests read the words; contrast 8.2:1 or better (design note §4).
- [x] Zero successful rows in a failure-only finding is never presented as proof no login succeeded.
  Evidence: `test_a_failure_only_rule_never_claims_that_nothing_succeeded`.
- [x] High means urgent review of observed success, not confirmed attacker access. Evidence:
  `test_high_asks_for_an_urgent_check_and_never_claims_a_compromise` and the frontend High test.
- [x] Table defaults and report assessment have the agreed explicit distinction (Option A). Evidence:
  the isolated new-country panel test shows Low with the note.
- [x] Meaningful API and frontend checks pass; report behaviour and existing findings stay intact.
  Evidence: 413 backend tests, Pyright clean, 149 frontend tests, type check and build pass; lint
  unchanged at six AUD-009 warnings. Agent, report prompt, rules and grader untouched.
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
- 20 October 2026. Built test-first in three slices: core, API, screen. Checked live in both
  themes on a separate server pair. Two-axis review: Standards found no hard violations and seven
  judgement calls; Spec found four test or wording gaps. Fixed: glossary entry "Rule severity",
  route helper, clearer type names, one helper for screen-only filters, typed colour map, badge
  in the rules guide, and frontend tests for four options, High and a rule's empty state. Kept:
  the report card's own "X severity" words, because its scale adds None and Critical; it shares
  the colours, not the badge component, which corrects the note's §6 wording. Status
  `ready-for-human`: awaiting the author's live review.
