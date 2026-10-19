# 25: Login alert severity policy

Type: research
Status: resolved
Blocked by: none

## Question

What severity policy can this synthetic authentication dataset support for the four existing
rules, before a severity column is specified or built?

Author's research go: 18 October 2026, prompt P-043. Perplexity is Codex's research tool only.
The existing rule-filter proposal uses the same four rule categories and does not need an
expanded detection catalogue. No rule-filter implementation is part of this research task.

## Scope

- Use Perplexity research and verify recommendations against high-trust primary sources.
- Separate attack classification, alert severity, confidence and investigation/report severity.
- Account for the existing rules' exact evidence and their limits. Failure-only findings cannot
  establish that there was no related successful sign-in elsewhere in the log.
- Assess simple documented defaults against context-dependent ratings. Mark every proposed
  project rating as a project policy, not an industry-mandated score.
- Identify conflicts with v1 report policy and the accepted Port scope before implementation.
- Save one cited note at `../research/25-login-alert-severity.md`.

## Acceptance

- [x] Perplexity result and connection outcome recorded without secrets.
- [x] Material claims verified against primary sources and cited in the research note.
- [x] Recommendation, alternatives, evidence gaps and scope implications documented.
- [x] No application, API contract or spec decision changed by the research.
- [x] Findings presented to the author for a design decision before implementation.

## Comments

Research is a separate follow-up to ticket 19's Alerts screen review. Ticket 19 remains open.


## Answer

Research completed on 18 October 2026. Evidence:
[25-login-alert-severity.md](../research/25-login-alert-severity.md).
Exactly one paid Perplexity research call succeeded. Material findings checked against official
Microsoft, MITRE and NIST sources. Research note's local links resolve; `git diff --check` passes.
No application, contract or spec change made during this research. No application tests needed.

Recommend deterministic rule-default review priorities: Brute force Medium, suspected password
spraying Medium, success after failures High, standalone new-country anomaly Low. These are
proposed project judgments, not source-prescribed universal values. The note transparently
records Perplexity's differing defaults and why they were not copied blindly.

An observed success does not establish attacker access. Failure-only findings do not establish
absence of related success. New ratings would differ from the current report policy, which must
remain unchanged for Parity. Resolve the table/report meaning with the author before shipping.
Rule filtering needs only the existing four categories and its own agreed API contract.

Research task resolved; recommendations are not implementation approval. Findings presented with
the evidence note for the author's design decision. Ticket 19 remains open. Stale API-documentation
caption reference logged as B-047 for follow-up, not silently fixed during this task.


### 2026-10-18 · Author accepts the recommendation

Author's ruling, verbatim: "agreed" (P-044). Approved rule defaults are Medium/Medium/High/Low
in the note's rule order. Follow-up implementation is tracked in ticket 26 after ticket 19.
The existing report policy remains unchanged; exact table/report wording and contract must be
settled before shipping. This approval does not add detection rules or change the current Port.
