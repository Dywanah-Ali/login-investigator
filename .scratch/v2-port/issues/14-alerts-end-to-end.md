# 14: Alerts, end to end

**What to build:** the analyst opens Alerts, sees every finding for the filtered view newest first,
clicks a row and reads its evidence in a side panel, jumps to the Log explorer with the alert's IP
and window applied, or sends the alert to the Investigator as a prepared question. "How these rules
work" explains each rule from the API's text.

**Blocked by:** 13 (Frontend shell and the Overview screen).

**Status:** ready-for-human

Spec: [spec.md](../spec.md), "The API" and "The frontend". Contract: alerts, rules guide.

- [x] `GET /api/alerts` returns the core's finding dictionary unchanged, evidence included, sorted by the core; API tests: S1 to S4 appear, newest first, filters narrow the list
  - Evidence: `backend/api/dashboard_routes.py` (`get_alerts`: `alerts_for_view`, then `to_dict()`). Seven tests in `tests/test_api_dashboard.py`: `test_s1_to_s4_appear_in_alerts_newest_first` (the order written by hand from the ground truth, S3's tie broken by rule), the contract shape with evidence, S1 cut to 20 rows, four filter cases, an empty view, a refused filter that is not echoed. Backend 304 passed; Pyright clean
- [x] The table with v1's seven columns; names cut to three plus "and N more"; the per-rule counts line; ~~severity labels and colours~~ (left out, see comments); rule titles from the rules endpoint
  - Evidence: `components/alerts-table.tsx` (TanStack Table 8 on the official shadcn `table`), `lib/alerts.ts` (`cutNames`, `countsLine`, `ruleTitles`). Tests: `shows v1's seven columns, rule titles from the rules endpoint, names cut to three` checks every header and cell; `the counts line gives the total and a count per rule title, in title order`
- [x] ~~Side panel on row click~~ A fixed details panel beside the table (author's ruling, see comments): evidence table ("Showing N of M events" when cut), "Open in Log explorer", "Investigate"
  - Evidence: `components/alert-details.tsx` (official shadcn `Card`), `pages/alerts.tsx`. Tests: the newest alert shown on first load with its row marked selected; a row click swaps in the caption, the seven evidence columns and both links; the keyboard chooses a row too; a filter change shows the newest alert of the new view, not a stale choice (B-009); no panel when nothing matches. Looked at on the running screen on 15 Oct with the real log: the panel beside the table, the swap, and the 0.3 s entry animation read from the page
- [x] "Open in Log explorer" is a plain link built from the first IP and the first and last dates
  - Evidence: `explorerLink` in `lib/alerts.ts`; two helper tests (a window across midnight, a one-day window) and the panel test reads the link's address
- [x] "Investigate" links to the Investigator with the prepared question in the address; the question is built from the rule title, first IP, first user and the window, with the contract's wording
  - Evidence: `investigateQuestion` and `investigateLink` in `lib/alerts.ts`; two helper tests and the panel test. The times read `2026-10-07 23:10:00`, see comments. Seen on the running screen: the link carries the spraying alert's question
- [x] "How these rules work" as a collapsible fed by the rules endpoint
  - Evidence: `components/rules-guide.tsx` (official shadcn `Collapsible`). Tests: collapsed at first, opens to the endpoint's text; still shown when no alert matches, as in v1
- [x] Log fields appear only in table cells
  - Evidence: test `a hostile summary, IP and username stay plain text inside cells` plants an image tag, markdown bold and a `javascript:` link in five log fields, and finds no image, no link, no bold, and every occurrence inside a `<td>`. The raw-HTML scan test still passes
- [x] Vitest: name cutting, the explorer link, the "Investigate" question
  - Evidence: `lib/alerts.test.ts` (7), `pages/alerts.test.tsx` (13), two new tests in `lib/format.test.ts`. Frontend 58 passed; `npm run typecheck` clean

## Comments

**2026-10-15, the author's rulings before the build.**

- Test points: all five. The API through the test client; three frontend helpers (name cutting, the
  explorer link, the "Investigate" question); and the Alerts screen drawn with a fake API reply, as
  ticket 13 did for the Overview.
- "Severity labels and colours" is left out of this ticket. v1's Alerts screen shows no severity and
  no finding carries one; severity exists only on the incident report card, ticket 17. Inventing one
  per rule would be new behaviour the spec rules out.

**2026-10-15, choices made during the build, for the author's review.**

- TanStack Table is pinned to version 8. npm's latest is version 9, whose interface differs from the
  official shadcn tasks example the spec chose.
- The "Investigate" question writes its times as `2026-10-07 23:10:00`, to the second. The contract
  shows `<first_seen>`, whose raw form `2026-10-07T23:10:00Z` would read "…Z UTC". The seconds stay,
  so the agent's search window holds the alert's first and last events.
- The empty state reads "No alerts match these filters. Widen the date range or reset the filters.",
  following the Overview's agreed wording (ticket 13, ruling 4) rather than v1's "press Reset
  filters".
- v1's hint "Select an alert to see its evidence." is kept under the table. The review found it
  missing.

**2026-10-15, two-axis review.** Standards: no hard violations, seven judgement calls. Fixed: direct
tests for the two time formats, one named type for the title lookup, a format per evidence column,
`NO_ALERTS` no longer exported, one comment style. Left: the fake API's six-argument row helper,
test code only. Spec: a selection that outlived a change of address (B-009, fixed test-first) and
v1's hint (restored). Open points for the author are below.

**Open points for the author.**

1. The spec's Presence row and ticket 19 still list "severity labels and colours" with no screen
   named. Proposal: name the report card (ticket 17) there, with a row in the spec's decisions log.
   - **Ruling, 15 Oct: on the report card.** Spec (two places and a decisions-log row), ticket 17
     and ticket 19 now name the card.
2. The agreed prototype showed a pager and a columns menu on the Alerts table. v1 has neither, and
   the log yields five alerts, so neither was built. Ticket 15 builds paging for the explorer.
   - **Ruling, 15 Oct: option A.** The author asked what thousands of alerts would do. The screen
     would draw every row, which a pager fixes; the reply would carry up to 20 evidence rows per
     alert, which only server paging fixes. Thousands cannot occur until log upload exists. So
     ticket 15's pager is built as one shared piece and also placed under the Alerts table; a line
     was added to ticket 15. Server paging stays out of scope, as the spec says, and is the fix if
     a dataset ever grows. No columns menu: it hides columns and does nothing for size.
3. "Alert" in the screens and the API and "finding" in the core name the same thing. Neither is in
   the glossary.
   - **Ruling, 15 Oct: option A.** `GLOSSARY.md` gains **Finding**, naming Alert as the screens'
     word for it. No code renamed: the core is v1's, untouched until Parity is proven.

**2026-10-15, ruling after the author's look at the live screen: a fixed details panel.** The
sliding panel is replaced by a details panel that stays beside the table, as the prototype drew it,
and moves below the table on narrow screens. The newest alert is shown on first load and after a
filter change; a row click swaps the content. The content fades and slides a few pixels into place
(about 0.3 s), with no motion when the system asks for reduced motion. v1's "Select an alert" hint
is dropped, since an alert is always selected. Known trade-off: the table gets about half the width
and scrolls sideways for its last columns; the evidence table scrolls too. To be judged after a
look. Spec updated with a decisions-log row.

**2026-10-15, the author after a look: the details panel 20% narrower.** It went from 40% of the
width to 32%; the table now takes 68%. Then, at the author's request, set to 28% of the content
width, the table 72%.
