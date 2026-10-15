# 15: Log explorer, end to end

**What to build:** the analyst opens the Log explorer, adds an IP to the shared filters, sees the
five count tiles and a paged table of every matching row newest first, and downloads the same rows
as CSV. A badly formed IP is refused in the browser and again by the API, and the typed value is
never shown back.

**Blocked by:** 13 (Frontend shell and the Overview screen).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "The API" and "The frontend". Contract: log explorer, CSV download.

- [ ] `GET /api/explorer` returns the summary and every matching row newest first; `GET /api/explorer.csv` returns the same rows from the same core search with the contract's headers; formula-looking values keep the leading apostrophe
- [ ] A bad `ip` gives a 422 naming the field, never the value; API test
- [ ] Toolbar plus the IP box on this screen only; the IP validated in the browser before the request; the error message never echoes the value
- [ ] Five count tiles from the summary; the table paged in the frontend; the CSV link carries the same filters
- [ ] Empty view shows the shared empty state
- [ ] Vitest: the bad IP message, paging
- [ ] The pager is one shared piece, also placed under the Alerts table (author's ruling, ticket 14, 15 Oct); the Alerts screen test checks it is there
