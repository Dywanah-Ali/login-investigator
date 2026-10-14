# 13: Frontend shell and the Overview screen

**What to build:** the first live screen. The analyst opens the app, sees the sidebar with four
links, the "Synthetic data" badge and capture date from the API, sets filters in the toolbar, and the
Overview shows the four KPI tiles and the two charts for that view. The address bar carries the
filters, so a reload shows the same view. A filter that matches nothing shows the empty-state message.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** ready-for-human

Spec: [spec.md](../spec.md), "The frontend". Decisions: tickets 05 and 07, prototypes under `research/`.

- [x] Vite app with React Router in declarative mode and four routes; Vite's dev proxy forwards the API path to FastAPI; the README's two run commands work
  - Evidence: `frontend/src/App.tsx` (`<Routes>`, four screens), `frontend/vite.config.ts` (`server.proxy` for `/api`). A real run on 14 Oct: the API on its own port, `npm run dev`, then `curl localhost:5173/api/dataset`, `/api/overview?user=alice.k&outcome=failure` and `?from=yesterday` answered through the proxy with the contract's shapes and the fixed 422; `/alerts?user=alice.k` served the app. Port 8000 was held by another project on this machine, so the run used 8010 through `LI_API_URL`, now in the README
- [x] Official shadcn/ui pieces only: the dashboard-01 shell, KPI cards, the chart component with Recharts; no trimmed fork
  - Evidence: installed with the shadcn CLI (`radix-nova`, `components.json`): `dashboard-01`, `chart`, `select`, `popover`, `calendar`, `badge`. Block files the Overview does not use (area chart, data table, extra nav, sample data) and their packages were removed. One official file changed by the author's ruling: `ui/chart.tsx` (B-004)
- [x] Header shows the label and "Log captured …" from the dataset endpoint; nothing is hard-coded
  - Evidence: `site-header.tsx` reads `useDataset()`. Test `the header shows the label and the capture time from the dataset endpoint` feeds a different label and time and finds both
- [x] Filter toolbar (date range, outcome, country, user) under the page title; the pickers offer only the dataset's values; state lives in URL search parameters and travels on every request; a reset clears them
  - Evidence: `filter-toolbar.tsx`, `lib/filters.ts`, `hooks/use-filters.ts`. Tests: nine in `lib/filters.test.ts`; `the filters in the address travel on the request…`; `reset restores the whole log`; three toolbar tests (whole-log label, no fake date, unknown value visible: B-005, B-006). The calendar is bounded by the dataset's first and last date
- [x] Overview: four KPI tiles with labels that say what they count; failed share computed in the frontend; sign-ins per hour as stacked bars; top source IPs by failed sign-ins as horizontal bars; the block's area chart and period toggle removed
  - Evidence: `section-cards.tsx`, `hourly-chart.tsx`, `top-ips-chart.tsx`, `pages/overview.tsx`. Test `overview counts match the reply…` checks all four tiles and both chart titles. Labels from the agreed prototype (comments, point 4). The charts' drawing has no test, since the test browser has no layout. A look at the running screen on 14 Oct found half the IP labels missing (B-007), fixed and looked at again; the Outcome picker wrote `?outcome=failure` and every tile and chart redrew
- [x] One empty-state component shared by the dashboard screens
  - Evidence: `components/empty-state.tsx`. Test `an empty filter shows a clear message instead of the tiles`
- [x] Error messages are fixed text and never show exception text
  - Evidence: `lib/api.ts` (`FAILURE_TEXT`; the server's message is read for its code only), `components/failure-message.tsx`. Four tests, each feeding a planted traceback or a refused connection and asserting it is absent
- [x] Vitest with React Testing Library: failed share, singular or plural counts, the filter-to-URL mapping
  - Evidence: `lib/format.test.ts` (12), `lib/filters.test.ts` (9), `pages/overview.test.tsx` (14), `test/repository-rules.test.ts` (1): 36 passed. `npm run typecheck` clean; lint clean outside the official `ui/` files
- [x] Repository rule in place: no `dangerouslySetInnerHTML` anywhere in the frontend
  - Evidence: `test/repository-rules.test.ts` scans every file under `src` and `index.html`. It failed first on the official chart component (B-004) and passes since the author's ruling

## Comments

2026-10-14: test points agreed with the author before the build: all five (failed share, singular or
plural counts, the filters in the address, the Overview drawn with a fake API reply, the raw-HTML
scan).

2026-10-14: **Ruling: the official chart component's raw HTML.** The chart component writes its
colours with `dangerouslySetInnerHTML`. Three options were put to the author: change one line, let
the scan skip the file, or drop the component. **Ruling 2026-10-14: change one line (option A)**,
after asking what it would change. The rule stays absolute; reinstalling the component would fail
the scan test. Bug log B-004.

2026-10-14: build done on branch `ticket-13-frontend-shell`, test-first. Two-axis review run
(standards and spec). Fixed from it: a date label printing "undefined" (B-005), a filter value the
analyst could not see (B-006), the capture date hidden on narrow screens, the date label now showing
the whole log as the agreed screen does, a guard against "null of attempts", the date helpers in one
place, the screen icons in one list, the Vite template's README and icon file deleted, `LI_API_URL`
written into the README. Backend 294 passed, Pyright 0 errors. Status `ready-for-human` until the
author reviews.

Open for the author's ruling:

1. **Log fields outside tables.** The rule says log fields appear only in table cells. The agreed
   screens put IPs on the chart's axis and tooltip, and users and countries in the filter pickers.
   All are plain React text, never markup. Proposed: reword the rule to "in tables, chart labels
   and picker options, always as plain text, never through a renderer that produces markup", with a
   decisions log row.
   **Ruling 2026-10-14: reworded (option A).** `CLAUDE.md` security rules and the spec's security
   rendering section updated; spec decisions log row added.
2. **The loader's message on a bad log.** The contract sends the loader's row-problem message with
   `log_invalid`. The frontend shows its own fixed text instead, by this ticket's rule. Proposed:
   keep the fixed text and note in the contract that the message is for API clients and the server
   log, not the screen.
   **New fact, found while preparing the ruling:** the loader's row messages quote raw log values,
   so the API itself broke the contract's rule that a log field never travels inside a sentence.
   **Ruling 2026-10-14: fixed text in the API as well, done on this branch with no new ticket**,
   since the change sits in the API only and the core is untouched. Built test-first
   (`test_a_bad_row_never_sends_its_log_values_back`); contract Errors table, spec and decisions log
   updated; bug log B-008. Backend 295 passed, Pyright 0 errors.
3. **Small behaviour no line asked for.** Zero bars for quiet hours, so time is not squeezed; the
   filters follow the sidebar links between dashboard screens; an unknown address opens the
   Overview; the `LI_API_URL` dev setting. Proposed: keep all four.
   **Ruling 2026-10-14: all four kept.** The sidebar filters are still checked against v1 under
   point 4.
4. **Labels not checked against v1's code.** v1 could not be read this session. The tile labels,
   the chart titles and the empty-state text come from the agreed prototype, which says its content
   is v1's. The failed share rounds a half up (6.25% shows 6.3%); Python's own formatting would show
   6.2%. The claim "as in v1" for the sidebar filters is also unchecked. Proposed: check all of it
   against `app/screens/overview.py` and `app/shared.py` in a fresh session, before ticket 19.
   **Ruling 2026-10-14: accept the prototype as the source (option C), no check against v1's
   code.** The recommendation was a check before closing. The agreed prototype is the reference
   for the Overview's labels, chart titles and empty-state text; the failed share rounds a half up;
   the sidebar links keep the filters. Spec decisions log row added, so ticket 19's presence check
   knows the reference.
5. **Unused fields in the Overview reply.** The Overview shows no `successes`, `distinct_ips`,
   `distinct_countries`, `first_seen`, `last_seen`, and the toolbar no `row_count`. The cause is the
   contract (ticket 12), not this ticket. Proposed: decide at ticket 15, whose count tiles may use
   some of them.
   **Update while preparing the ruling:** the Log explorer has its own endpoint for its counts, so
   waiting gains nothing. **Ruling 2026-10-14: trim now (option A).** The Overview summary sends
   `total`, `failures` and `distinct_users`; the dataset facts drop `row_count`. API tests changed
   first, then the routes, the frontend types and the contract. Backend 295 passed, frontend 36,
   Pyright and the type check clean.

2026-10-14: the author clarified the "no screenshots" ruling: screenshots may be used to look at a
running screen, only never as evidence. The look found B-007, fixed.
