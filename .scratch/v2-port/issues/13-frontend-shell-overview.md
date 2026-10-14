# 13: Frontend shell and the Overview screen

**What to build:** the first live screen. The analyst opens the app, sees the sidebar with four
links, the "Synthetic data" badge and capture date from the API, sets filters in the toolbar, and the
Overview shows the four KPI tiles and the two charts for that view. The address bar carries the
filters, so a reload shows the same view. A filter that matches nothing shows the empty-state message.

**Blocked by:** 12 (API foundation and the Overview endpoint).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "The frontend". Decisions: tickets 05 and 07, prototypes under `research/`.

- [ ] Vite app with React Router in declarative mode and four routes; Vite's dev proxy forwards the API path to FastAPI; the README's two run commands work
- [ ] Official shadcn/ui pieces only: the dashboard-01 shell, KPI cards, the chart component with Recharts; no trimmed fork
- [ ] Header shows the label and "Log captured …" from the dataset endpoint; nothing is hard-coded
- [ ] Filter toolbar (date range, outcome, country, user) under the page title; the pickers offer only the dataset's values; state lives in URL search parameters and travels on every request; a reset clears them
- [ ] Overview: four KPI tiles with labels that say what they count; failed share computed in the frontend; sign-ins per hour as stacked bars; top source IPs by failed sign-ins as horizontal bars; the block's area chart and period toggle removed
- [ ] One empty-state component shared by the dashboard screens
- [ ] Error messages are fixed text and never show exception text
- [ ] Vitest with React Testing Library: failed share, singular or plural counts, the filter-to-URL mapping
- [ ] Repository rule in place: no `dangerouslySetInnerHTML` anywhere in the frontend
