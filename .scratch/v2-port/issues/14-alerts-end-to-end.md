# 14: Alerts, end to end

**What to build:** the analyst opens Alerts, sees every finding for the filtered view newest first,
clicks a row and reads its evidence in a side panel, jumps to the Log explorer with the alert's IP
and window applied, or sends the alert to the Investigator as a prepared question. "How these rules
work" explains each rule from the API's text.

**Blocked by:** 13 (Frontend shell and the Overview screen).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "The API" and "The frontend". Contract: alerts, rules guide.

- [ ] `GET /api/alerts` returns the core's finding dictionary unchanged, evidence included, sorted by the core; API tests: S1 to S4 appear, newest first, filters narrow the list
- [ ] The table with v1's seven columns; names cut to three plus "and N more"; the per-rule counts line; severity labels and colours; rule titles from the rules endpoint
- [ ] Side panel on row click: evidence table ("Showing N of M events" when cut), "Open in Log explorer", "Investigate"
- [ ] "Open in Log explorer" is a plain link built from the first IP and the first and last dates
- [ ] "Investigate" links to the Investigator with the prepared question in the address; the question is built from the rule title, first IP, first user and the window, with the contract's wording
- [ ] "How these rules work" as a collapsible fed by the rules endpoint
- [ ] Log fields appear only in table cells
- [ ] Vitest: name cutting, the explorer link, the "Investigate" question
