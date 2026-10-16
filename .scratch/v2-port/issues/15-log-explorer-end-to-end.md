# 15: Log explorer, end to end

**What to build:** the analyst opens the Log explorer, adds an IP to the shared filters, sees the
five count tiles and a paged table of every matching row newest first, and downloads the same rows
as CSV. A badly formed IP is refused in the browser and again by the API, and the typed value is
never shown back.

**Blocked by:** 13 (Frontend shell and the Overview screen).

**Status:** ready-for-human

Spec: [spec.md](../spec.md), "The API" and "The frontend". Contract: log explorer, CSV download.

- [x] `GET /api/explorer` returns the summary and every matching row newest first; `GET /api/explorer.csv` returns the same rows from the same core search with the contract's headers; formula-looking values keep the leading apostrophe
- [x] A bad `ip` gives a 422 naming the field, never the value; API test
- [x] Toolbar plus the IP box on this screen only; the IP validated in the browser before the request; the error message never echoes the value
- [x] Five count tiles from the summary; the table paged in the frontend; the CSV link carries the same filters
- [x] Empty view shows the shared empty state
- [x] Vitest: the bad IP message, paging
- [x] Visual hierarchy (spec, "The frontend"): the rows table leads, the count tiles step back; the quiet styling from the Alerts details panel becomes one shared piece used by both screens
- [x] The pager is one shared piece, also placed under the Alerts table (author's ruling, ticket 14, 15 Oct); the Alerts screen test checks it is there

## Comments

- 16 October 2026: author gave the go to implement ticket 15. Test seams are the HTTP API and frontend components/functions, already agreed in the spec Testing Decisions. Use test-first slices for explorer results, CSV safety, IP refusal and paging. Review against the starting HEAD `6b7ed0d`; leave the ticket awaiting the author’s visual review before resolving it.


## Answer

Implemented 16 October 2026. Awaiting the author's live visual review before resolution.

- `backend/api/dashboard_routes.py`: Explorer JSON and CSV share `explorer_rows`, calling the
  existing core search. Full matching rows are newest first. CSV keeps the core's formula protection.
- `backend/api/filters.py`: optional IP validation, fixed 422 message, no echoed input. IPv4 and IPv6
  are accepted; empty means all. Exact valid spelling is retained for the core's exact match.
- `frontend/src/pages/explorer.tsx`: shared toolbar plus an IP form, the five approved counts,
  shared empty state, fixed failures and CSV link carrying the applied filters. An invalid URL IP
  never reaches the endpoint or appears as an echoed value in the screen. Draft errors clear on Reset.
- `ExplorerTable` and `AlertsTable` use TanStack's local pagination with the shared `TablePager`,
  twenty rows per page. A new filtered view starts at page one. `QuietCard` shares the supporting
  surface between the count tiles and alert details. The table retains full contrast.

Evidence:

- Backend full suite: **323 passed**. Includes API rows/order, exact five-field summary, empty
  view, CSV matching/header/formula protection, invalid IP/no echo and IPv6 acceptance.
- Frontend full suite: **90 passed**. Includes browser IP validation, paging in both tables,
  matching CSV filters, Reset with/without applied filters, empty view, plain hostile cell text,
  IP confined to Explorer navigation and fixed API error text.
- Pyright and TypeScript checks: clean. Production build: passed. `git diff --check`: clean.
- Standards review: no documented breaches. One low-priority duplication concern fixed: pager's
  page-size label now reads the table's setting. Spec review: no findings.
- Shared quiet surface is implemented; the author still needs to judge visual hierarchy in the
  live screen. No browser automation or screenshots were used, in line with the spec.

Concerns recorded without unrelated fixes:

- Lint has no errors and six warnings. Existing: TanStack compatibility in `alerts-table.tsx`;
  Fast Refresh exports in `ui/badge.tsx`, `ui/button.tsx` and `ui/sidebar.tsx`; state-setting effect
  in `hooks/use-mobile.ts`. New: the same TanStack compatibility warning in `explorer-table.tsx`.
- Production build warns about its approximately 920 kB minified JavaScript chunk. Splitting the
  application bundle is outside this ticket.
- The existing API on port 8000 returned 404 for the new route. An isolated API on port 8001 with
  temporary memory serves the preview through Vite on port 5173. The existing server was left alone.
- The existing Pyright ignore list for frozen v1 files remains in place.
