# Design note: rule filter and default severity on Alerts (ticket 26)

Drafted 20 October 2026 for the author's review. Nothing here is built yet. Once approved, the
contract changes below are copied into `docs/api-contract.md` and a row is added to the spec's
decisions log. Inputs: [ticket 26](../issues/26-alert-rule-filter-default-severity.md),
[research 25](25-login-alert-severity.md), AUD-001 and AUD-002.

## 1. What the analyst sees

| Place | Change |
|---|---|
| Filter toolbar, Alerts only | A new **Rule** box after User: `All` (default) and the four rule titles. It sits with the other filters and is cleared by Reset |
| Alerts table | A new **Severity** column straight after Rule, showing a coloured badge with the word `Low`, `Medium` or `High` |
| Details panel | The badge again, under the rule title, with that rule's one-sentence explanation and the table/report note (section 3) |
| "How these rules work" | Each rule also lists its default severity and explanation |
| Overview, Log explorer, Investigator | No change. The rule filter belongs to Alerts, as the IP box belongs to the Log explorer |

The table stays sorted newest first. There is no sorting or filtering by severity; neither was
asked for.

## 2. The policy (approved values, P-044)

| Rule | Default | Explanation shown |
|---|---|---|
| Brute force | Medium | Repeated failures on one account need review. This finding alone does not establish whether related sign-ins succeeded. |
| Password spraying | Medium | Failures across many accounts suggest an attempt against several accounts. The log cannot verify that the same password was tried. |
| Success after repeated failures | High | A successful sign-in follows many failures on the same account and IP address. Check urgently whether it was authorized. |
| Sign-in from a new country | Low | An unfamiliar country is a useful lead. Travel, network routing, or an incomplete history may explain it. |

The explanations are research 25's wording unchanged. They meet three acceptance lines: zero
successes is never called proof that nothing succeeded; High says success was observed, not that
an attacker got in; Low still asks for review.

Severity is fixed per rule. It never rises because several findings overlap, and a language
model never assigns it.

## 3. Table severity versus report severity (decided: Option A, author, 20 October 2026, P-114)

The report's policy stays unchanged, as ruled on 18 October. So one case can show two different
levels. An isolated new-country alert shows **Low** in the table, while a report on that case
can say **Medium severity**. The screen must explain this honestly.

| Option | Table header | How the difference is explained |
|---|---|---|
| **A. Severity, labelled as the rule's default (recommended)** | Severity | The details panel says: "Rule default. This is how urgently to review this pattern. An investigation report weighs all the evidence and can rate the case higher or lower." |
| B. Rename the table measure | Review priority | The table never says "severity", so it cannot clash with the report. Departs from the approved term and from the naming in Sentinel and Defender |

Why A: it keeps the approved vocabulary and the industry's column name. The explanation sits
exactly where the analyst looks at one alert. A frontend test pins the isolated new-country
case: Low in the table, with the note visible.

## 4. Colours

Reuse the report card's existing badge colours, so one colour always means one level.

| Level | Light mode | Dark mode | Contrast light / dark |
|---|---|---|---|
| Low | blue-900 text on blue-100 | blue-200 on blue-950 | 8.5:1 / 10.4:1 |
| Medium | orange-900 on orange-100 | orange-200 on orange-950 | 8.2:1 / 11.5:1 |
| High | red-900 on red-100 | red-200 on red-950 | 8.2:1 / 11.1:1 |

All six pairs pass WCAG AAA for normal text (7:1). Computed on 20 October 2026 from the
installed Tailwind 4 colour values. The word is always visible, so the meaning survives colour
blindness. Green stays reserved for the Overview's "no alerts" state. Research 25 said amber;
the report card already uses orange, and one palette across both places is the point.

## 5. API contract changes

**`GET /api/alerts` gains one optional parameter.**

| Parameter | Type | Meaning | Invalid |
|---|---|---|---|
| `rule` | rule key | Only findings of this rule. Missing or empty means all rules | not one of the four keys. 422, message `rule is not a known rule.`, never echoing the value |

`rule` is Alerts only. The other endpoints ignore it, as they ignore `ip`. The alerts reply
shape does not change.

**`GET /api/rules` gains two fields per rule and one note.**

```json
{
  "rules": [
    {"rule": "brute_force", "title": "Brute force", "fires_when": "...", "assumption": "...",
     "severity": "medium",                      // "low" | "medium" | "high"
     "severity_reason": "Repeated failures on one account need review. ..."}
  ],
  "general_assumptions": ["..."],
  "severity_note": "Rule default. This is how urgently to review this pattern. ..."
}
```

The frontend already looks up rule titles from this reply by rule key. It looks up severity the
same way. Severity is a property of the rule, so it travels once with the rules, not once per
alert.

## 6. Where the code lives

| Layer | Change |
|---|---|
| Core | A new module `severity.py` holds the one mapping: rule, level, reason, plus the note. `dashboard.alerts_for_view` gains an optional `rule` argument |
| API | `/api/rules` adds the policy fields. `/api/alerts` validates `rule` and passes it to the core |
| Frontend | `rule` joins the address-bar filters, Alerts only. A Rule box in the toolbar. One shared severity badge used by the table, the details panel, the rules guide and the report card |

Untouched: `rules.py`, every detection threshold, `Finding`, the agent and its tools, the report
prompt and the eval grader. The agent never sees severity, so its answers and the eval results
cannot change. No paid model run is needed.

## 7. How it will be proved

| Acceptance line | Evidence |
|---|---|
| One deterministic policy | Core test: every rule has exactly one level and reason, and no unknown rule appears |
| Filter composes, resets paging, has an empty state | Core and API tests for rule plus date, outcome, country and user; frontend tests for paging reset, Reset and the empty message |
| Only four categories plus All | Frontend test reads the options from the rules reply |
| Contract before code | This note, then `docs/api-contract.md`, before any code |
| Visible accessible labels | Frontend test: the word is in the cell; contrast figures above |
| Zero successes, High wording, table versus report | Frontend tests on the explanations, including the isolated new-country case |
| Existing behaviour intact | Full backend and frontend suites, Pyright and the build all pass |
| Author review before any push | Live look at the Alerts screen in both themes |

Time estimate: about 3 to 4 hours of build and checks, then one consolidated review.

## 8. Decisions for the author

1. Option A or B in section 3. **Decided: Option A** (author, 20 October 2026, P-114).
2. Approval of this note as a whole, which unlocks the contract edit and the build.
   **Approved** (author, 20 October 2026, P-115). Contract and spec decisions log updated.
