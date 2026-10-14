# shadcn/ui templates and the frameworks they need

Type: research
Status: resolved
Blocked by: none
Map: [map.md](../map.md)

## Question

Which shadcn/ui templates, blocks or starter kits fit an app that is an admin dashboard (KPI cards,
charts, two data tables, a sidebar) joined to an AI chat with a history list? For each candidate,
record from primary sources:

- Name, URL, licence, maintainer and last update.
- The framework it requires: Next.js, Vite with React Router, or other.
- Which of v2's four screens it covers out of the box: Overview (KPI cards and charts), Alerts
  (table of findings), Log explorer (filterable table), Investigator (chat with past investigations).
- The chart library it ships, if any.
- How much code the author would have to read to understand it (rough file and line counts).

Also record, from the official shadcn/ui documentation, which frameworks shadcn/ui supports today
and whether any is recommended for a plain single-page app with no server rendering.

The brief's candidates from memory, to verify: the official dashboard block, the data table
pattern, the "tasks" table example, an AI chatbot template built on shadcn/ui, the official sidebar
blocks.

Save findings to `research/04-shadcn-templates.md` in this effort's folder. This ticket's answer is
the input to [Pick the template and framework](05-pick-template.md).

## Comments

## Answer

Full findings: [research/04-shadcn-templates.md](../research/04-shadcn-templates.md).

- shadcn/ui's installation docs list seven equal setups (Next.js, Vite, TanStack Start, Laravel,
  React Router, Astro, manual React) and recommend none; the blocks "work with all React
  frameworks". A Vite SPA is a fully documented path, so Next.js is not required.
- No template covers all four screens. The official pieces compose to about 3,000 lines:
  `dashboard-01` (sidebar, KPI cards, Recharts chart, one table; 1,762 lines, no Next.js import),
  the tasks example for the two filterable tables (921 lines, only its page.tsx is Next-specific),
  and the new official `message`, `bubble` and `message-scroller` components for the chat.
- satnaing/shadcn-admin (MIT, Vite + TanStack Router, about 15,000 app lines) has every screen
  shape including a chat page with a conversation list, but most of it would be deleted.
- Every chat template (shadcn-ui/chatbot-template MIT, vercel/chatbot Apache 2.0, AI Elements) is
  Next.js plus the AI SDK with the model call in Next.js routes, which v2 replaces with FastAPI.
- Charts: Recharts v3 everywhere, through shadcn's `chart` component. Tables: TanStack Table
  (official guide on v9).

