# Map the four screens onto the template

Type: prototype
Status: resolved
Blocked by: 01, 05
Map: [map.md](../map.md)

## Question

With the template chosen in [Pick the template and framework](05-pick-template.md), agree with the
author how each v1 screen maps onto it. v1's screen content is agreed in
`../login-investigator/docs/ui-design.md` and stays the same; only the shell changes.

For each screen make a rough prototype (wireframe or stub) and decide:

| Screen | Must keep from v1 |
|---|---|
| Overview | Four KPI tiles, sign-ins per hour, top IPs by failed sign-ins |
| Alerts | Table of findings, evidence of the selected alert, "Open in Log explorer", "How these rules work" |
| Log explorer | Filterable table with the IP search on top of the shared filters |
| Investigator | Chat, tool-calls panel under each answer, incident report card with PDF download, list of past Investigations, starter questions |
| Shared | Sidebar navigation, the shared filters on the three dashboard screens only, the "Synthetic data" label and capture date, empty-state messages |

Also decide where the shared filter state lives in the frontend and how it travels with each request,
which [Screen-layer logic](01-screen-layer-logic.md) feeds.

Security rules the prototype must show: log fields only inside tables; agent answers and the report
card rendered with links and images off. This ticket may graduate the "Security rendering in React"
fog into a ticket.

## Comments

## Answer

Prototype: [research/07-screens-prototype.html](../research/07-screens-prototype.html), also published
at https://claude.ai/artifact/XLhRJSY2pXJ4Jz94DJzpff. The four screens drawn onto the chosen shell
(ticket 05) with v1's agreed content, and option buttons where a layout choice was open. Decided with
the author on 14 October 2026; four questions, all answered with the recommended option.

### Layout decisions

| # | Decision | Choice | Reason |
|---|---|---|---|
| 1 | Where the shared filters live | A **toolbar** under the page title on Overview, Alerts and Log explorer. The sidebar is navigation only | Each region does one job. The Investigator has no toolbar, so it is visibly unfiltered |
| 2 | Where an alert's evidence opens | A **side panel** (shadcn Sheet) that slides in on row click: evidence table, "Open in Log explorer", "Investigate" | Detail must not push the list away. Same pattern as dashboard-01's row details |
| 3 | Where the filter state lives | **In the URL** as search parameters (`from`, `to`, `outcome`, `country`, `user`, plus `ip` on the explorer). Each API request carries the same parameters | The address describes the screen: shareable, reload-safe, testable. "Open in Log explorer" is a plain link |
| 4 | Where past investigations sit | A **second column inside the Investigator page**, with "New investigation" and the list | The sidebar does one job on every screen |

### Screen by screen

**Shared shell.** dashboard-01's sidebar (four navigation links) and header. The header carries the
"Synthetic data" badge and "Log captured 8 Oct 2026, 09:00 UTC" (from the dataset-facts response).
One empty-state component for the three dashboard screens.

**Overview.** The block's four KPI cards with v1's figures (failed share computed in the frontend from
the two raw numbers). Sign-ins per hour as stacked bars (Recharts BarChart via the shadcn `chart`
component); top source IPs by failed sign-ins as horizontal bars. The block's interactive area chart
and its 7d/30d/90d toggle are removed, since the toolbar holds the date range. This settles the
question handed over from ticket 05.

**Alerts.** The tasks example's table with v1's seven columns, sorted newest first by the core; the
frontend cuts names to three and adds "and N more", and computes the per-rule counts line. Evidence
in the side panel. "How these rules work" as a Collapsible, its text served by the API from the same
source as `rules.py`. "Investigate" links to the Investigator; what the link carries is for ticket 09.

**Log explorer.** The toolbar plus the IP box on this screen only; the IP is validated in the browser
before the request and refused again by the API; the typed value is never echoed. Five count tiles
from the core's summary. The same table pattern, paged instead of v1's scroll box (presentation,
frontend). CSV download is an API endpoint taking the same filter parameters, so file and table come
from one core search.

**Investigator.** Second column: "New investigation" and the list (newest three, three more per
click, the open one always shown; paging in the frontend, the API sends the full list). Chat with the
official `message`, `bubble` and `message-scroller` components; stream over SSE (ticket 06), `tool`
events drive the progress line and the Tools used panel. Tools used: a Collapsible under each answer
with the core's Asked and Found lines, rows in a table, raw JSON behind a Switch. Report: a Card with
the fixed fields and a "Download PDF" link to the API; the report button shows only when the core's
report offer says so, with its wording. Starters and the scope line only in an empty investigation;
input locked and a progress line while answering; the AI note by the input.

### Security rendering (graduates the fog, no new ticket)

Decided with the author on 14 October 2026, after the author asked whether formatted answers could be
made safe. The rule is "nothing that fetches or navigates", not "no formatting".

- **Agent chat answers: allowlist markdown.** A small renderer (react-markdown or equivalent) with an
  explicit list of allowed elements: paragraphs, bold, italics, bullet and numbered lists, headings,
  inline code and code blocks. Links and images are not on the list, so a link in the answer shows as
  plain text with its address visible and is never followed; an image is dropped. Raw HTML in the
  text is never rendered. This is a change from v1, which showed answers as plain text.
- **Report card: fixed fields as plain text**, unchanged from v1. The fields are structured output,
  not free text.
- **Log fields only in table cells.** React escapes text content by default; the rule is kept by
  never passing a log field through any renderer that produces markup.
- **Guard: a test, not a convention.** Feed the planted S5 injection strings and a few crafted
  answers (markdown links, image tags, raw HTML, javascript: URLs) through the renderer and assert
  the output holds no `<a>`, `<img>`, `<script>`, `<iframe>` or raw HTML. Runs with the parity set on
  every change (ticket 08). Plus a repository rule: no `dangerouslySetInnerHTML` anywhere in the
  frontend, and the renderer is used in exactly one component.
- Residual risk, accepted: an answer can use headings or bold to look like part of the page. That
  is cosmetic and leaks nothing.

### Hand-offs

- [The API contract](09-api-contract.md): filter parameters as URL search parameters on every
  dashboard endpoint and the CSV endpoint; dataset facts (capture date, date range, countries, users);
  alerts list with raw lists and numbers; rules guide text; investigations list in full; the report
  offer with the investigation; PDF download; what the "Investigate" link carries.
- [What proves Parity](08-parity.md): frontend tests for name cutting, counts, paging, the explorer
  link, the IP error message, and the renderer guard test with the injection strings.
