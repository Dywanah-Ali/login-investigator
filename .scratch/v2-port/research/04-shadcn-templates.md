# Research: shadcn/ui templates and the frameworks they need

Ticket: [04-shadcn-templates](../issues/04-shadcn-templates.md)
Date: 14 October 2026
Sources: ui.shadcn.com documentation pages, the shadcn-ui/ui repository, and each candidate's own
repository (README, LICENSE, package.json, file tree) read through the GitHub API. Line counts are
`wc -l` on the raw files where given exactly, and bytes divided by 33 where marked "approx".

## 1. What shadcn/ui supports today

Source: https://ui.shadcn.com/docs/installation

- The installation page lists seven paths under "Choose Your Framework": **Next.js, Vite, TanStack
  Start, Laravel, React Router, Astro, and React (Manual)**.
- The only guidance on choosing is "Choose the setup that matches your starting point" and
  "Recommended for new projects: use shadcn/create to build your preset visually and generate the
  right setup command for your framework." There is **no recommendation for single-page apps and
  no preference for Next.js** anywhere on the page.
- The blocks pages (https://ui.shadcn.com/blocks and /blocks/sidebar) say the blocks "Work with all
  React frameworks. Open Source. Free forever." The shadcn-ui/ui repository is MIT licensed
  (GitHub API, pushed 13 October 2026, about 125k stars).
- **Vite path** (https://ui.shadcn.com/docs/installation/vite): `pnpm dlx shadcn@latest init -t vite`
  scaffolds a new project, or `pnpm create vite@latest` (React + TypeScript) then
  `pnpm add tailwindcss @tailwindcss/vite`, the `@/*` path alias in `tsconfig.json`,
  `tsconfig.app.json` and `vite.config.ts`, then `pnpm dlx shadcn@latest init` and
  `pnpm dlx shadcn@latest add button`. Tailwind v4 (`@import "tailwindcss"`). The page does not
  mention React Router; routing is left to the project.
- **React Router path** (https://ui.shadcn.com/docs/installation/react-router): starts from
  `pnpm create react-router@latest`, which is React Router's framework mode (a Vite plugin with
  file-based routes, https://reactrouter.com/start/modes). It renders on the server unless
  `react-router.config.ts` sets `ssr: false`; React Router's own docs say "If you're looking to
  build a Single Page App, disable server rendering" with that flag
  (https://reactrouter.com/start/framework/rendering).
- Implication for v2: a plain SPA that talks to FastAPI is first-class in shadcn/ui through the
  Vite path, with any client router (React Router in declarative or data mode, or TanStack Router)
  added separately. Next.js is one option among seven, not the recommended one.

## 2. Candidates

### 2.1 Official dashboard block `dashboard-01`

- URL: https://ui.shadcn.com/blocks (first block). Install: `npx shadcn@latest add dashboard-01`.
- Maintainer and licence: shadcn, part of shadcn-ui/ui, MIT. Repo last pushed 13 October 2026.
- Framework: none required. The installed files import only `react`, `recharts`,
  `@tanstack/react-table`, `@dnd-kit/*`, `lucide-react` and `@/components/ui/*`; there is no
  `next/*` import in any of the ten files (grep of the raw files). The CLI places `page.tsx` at the
  target for the host framework.
- Covers: **Overview** (four KPI cards in `section-cards.tsx`, an interactive area chart in
  `chart-area-interactive.tsx`), a **sidebar** with grouped navigation and a user menu, a site
  header, and one **data table** (`data-table.tsx`) with sorting, column visibility, pagination,
  row selection, tabs and drag-to-reorder. That table is a reasonable base for Alerts and Log
  explorer, but it is heavier than needed (drag and drop, inline row drawer with a chart). No
  chat. One page only, no router wiring.
- Chart library: Recharts v3 through the shadcn `chart` component (ChartContainer, ChartTooltip).
- Size: 10 files, **1,762 lines** exact (`page.tsx` 40, `app-sidebar` 181, `chart-area-interactive`
  291, `data-table` 816, `section-cards` 102, `site-header` 30, four nav files 302). Plus
  `data.json` (12.8 KB) and the `ui/` components the CLI pulls in.

### 2.2 Official sidebar blocks `sidebar-01` to `sidebar-16`

- URL: https://ui.shadcn.com/blocks/sidebar. Install: `npx shadcn@latest add sidebar-07` etc.
- Sixteen variants, each a page plus `app-sidebar.tsx` and nav files. Relevant ones for v2:
  `sidebar-01` (navigation grouped by section), `sidebar-07` (collapses to icons),
  `sidebar-08` (inset layout with secondary navigation), `sidebar-16` (paired with a sticky header).
- Same maintainer, licence and framework story as `dashboard-01` (it already uses the same sidebar
  pattern). Covers only the shell, no screens. Roughly 300 to 450 lines each.

### 2.3 Official data table guide and the "tasks" example

- Guide: https://ui.shadcn.com/docs/components/data-table. shadcn deliberately ships **no data-table
  component**: "instead of a data-table component, I thought it would be more helpful to provide a
  guide on how to build your own." Built on **TanStack Table v9** (`@tanstack/react-table`) over the
  basic `<Table />`. The guide walks through sorting, filtering, pagination, row selection, column
  visibility, row actions and cell formatting, with reusable column-header, pagination and
  view-options components.
- Example: https://ui.shadcn.com/examples/tasks, source in
  `apps/v4/app/(app)/examples/tasks` of shadcn-ui/ui. Shows a 100-row task table with faceted
  Status and Priority filters, a text filter, column visibility, row actions and pagination.
- Size: 11 files, **921 lines** exact. Of these, `page.tsx` (67 lines) is Next.js specific (reads
  the JSON with `fs` and `next/image`); the ten component files (854 lines) import only React,
  TanStack Table and `@/components/ui/*` and port to any framework unchanged.
- Fit: the closest match to **Alerts** and **Log explorer** (a filterable table with faceted
  filters is what v1's log explorer does). Chart library: none.

### 2.4 Official chat components and `shadcn-ui/chatbot-template`

- shadcn/ui now ships chat building blocks as ordinary components: `message`
  (https://ui.shadcn.com/docs/components/message, `pnpm dlx shadcn@latest add message`), `bubble`,
  `marker`, and the headless `@shadcn/react` package with `MessageScroller` and `Questionnaire`
  (https://ui.shadcn.com/docs/react/message-scroller). These have no stated framework requirement.
- Template: https://github.com/shadcn-ui/chatbot-template. Maintainer shadcn, **MIT** (LICENSE
  file, copyright 2026 shadcn). Created 11 August 2026, pushed 28 September 2026, about 1.1k stars.
- Framework: **Next.js 16** App Router (package.json `next 16.3.6`), AI SDK v7 (`ai`,
  `@ai-sdk/react`) and the Vercel AI Gateway for the model call; the backend is
  `app/api/chat/route.ts`. No chat history list, no sidebar, no charts, no tables.
- Covers: the **Investigator** chat surface only (message list, prompt form, streaming, markdown,
  tool-call parts, suggestions). The past-investigations list would be added.
- Size: 40 TypeScript files, approx 2,850 lines in total; 25 are app files (approx 1,050 lines,
  `chat.tsx` is 144 lines) and 15 are `components/ui/*` copies.
- Note: the UI pieces (`chat.tsx`, `chat-message.tsx`, `prompt-form.tsx`, `parts/*`) are plain
  React over the `message`, `bubble` and `message-scroller` components and could be copied into a
  Vite app, but the streaming hook (`useChat`) expects an AI SDK stream, not a plain FastAPI JSON
  response, so the transport would be rewritten.

### 2.5 `vercel/chatbot` (formerly vercel/ai-chatbot)

- URL: https://github.com/vercel/chatbot. Maintainer Vercel, **Apache 2.0** (LICENSE, copyright
  2024 Vercel). Pushed 8 July 2026, about 21k stars.
- Framework: **Next.js 16** App Router with React Server Components and Server Actions, AI SDK v7,
  Neon Postgres for history, Vercel Blob, Auth.js, Vercel AI Gateway (README features list).
- Covers: Investigator chat **with a history sidebar** (`components/chat/sidebar-history.tsx`,
  `sidebar-history-item.tsx`, `app/(chat)/api/history/route.ts`). No KPI cards, charts or data
  tables.
- Size: 153 TypeScript files, approx 18,000 lines; 131 app files (approx 15,700 lines). Far more
  than v2 needs, and its persistence, auth and model layers all live in Next.js server code that
  v2 would replace with FastAPI.

### 2.6 `satnaing/shadcn-admin`

- URL: https://github.com/satnaing/shadcn-admin. Maintainer satnaing (community), **MIT**. Pushed
  10 September 2026, latest release v2.2.1 on 6 November 2025, about 15.7k stars.
- Framework: **Vite 8 + TanStack Router** (README stack: "UI: ShadcnUI, Build Tool: Vite, Routing:
  TanStack Router, Type Checking: TypeScript, Linting: ESLint & Prettier, Icons: Lucide, Tabler;
  Auth (partial): Clerk"). A client-side SPA, no server rendering.
- Covers: **Overview** (dashboard with KPI cards and bar and area charts, `features/dashboard`,
  5 files, approx 640 lines), **two table pages** (`features/tasks` 17 files approx 1,650 lines and
  `features/users` 19 files approx 2,180 lines, both TanStack Table v8 with faceted filters, bulk
  actions and CRUD dialogs), a **chats page** (`features/chats`, 3 files approx 570 lines, a
  user-to-user messaging mock with a conversation list on the left, which is the shape of
  Investigator plus its history list), plus settings, auth and error pages.
- Chart library: plain **Recharts** (`recharts ^3.8.1`), imported directly without the shadcn
  `chart` wrapper.
- Size: 234 TypeScript files, approx 17,800 lines; 204 app files (approx 15,000 lines). Trimming
  the unused features (apps, auth, Clerk, settings, users, RTL, errors) is the first task.

### 2.7 `Kiranism/next-shadcn-dashboard-starter`

- URL: https://github.com/Kiranism/next-shadcn-dashboard-starter. Community, **MIT**. Pushed
  11 September 2026, about 7.1k stars.
- Framework: **Next.js 16**, TanStack Table v8, Recharts 3.8 (package.json). Dashboard, tables,
  forms, auth (Clerk) and billing. No chat. Not inspected further because it needs Next.js and
  carries auth and billing v2 does not want.

### 2.8 Chat component kits (not templates)

- **Vercel AI Elements** (https://github.com/vercel/ai-elements, Apache 2.0, pushed 1 September
  2026). A shadcn registry of chat components (conversation, message, prompt input, reasoning,
  sources). Its own setup docs list as prerequisites "Next.js 14+ (App Router recommended)",
  shadcn/ui initialised and the AI SDK. Next.js is a stated requirement.
- **Blazity/shadcn-chatbot-kit** (https://github.com/Blazity/shadcn-chatbot-kit, MIT, pushed
  26 February 2026, about 800 stars). A shadcn registry (`npx shadcn@latest add
  https://shadcn-chatbot-kit.vercel.app/r/chat.json`) with `chat.tsx` (8.9 KB) and
  `chat-message.tsx` (11 KB). Its docs state no framework requirement beyond shadcn/ui, but the
  examples use `useChat` from the Vercel AI SDK. Smaller and less active than the official pieces.
- **assistant-ui** (https://github.com/assistant-ui/assistant-ui, MIT, pushed 14 October 2026,
  about 12.5k stars). A React chat library with shadcn-styled components. README: the CLI
  "scaffolds a Next.js app or adds the styled components to an existing project"; runtimes include
  the AI SDK, LangGraph and LangChain (`@assistant-ui/react-langgraph`), a data-stream runtime and
  "any custom HTTP backend". The most backend-neutral kit, but it is a dependency with its own
  runtime model, which is more to understand than a few copied components.

## 3. Comparison against v2's four screens

| Candidate | Framework | Overview | Alerts table | Log explorer table | Investigator chat + history | Charts | Code to read |
|---|---|---|---|---|---|---|---|
| dashboard-01 (official) | any React | yes | partial (one table) | partial | no | Recharts v3 via `chart` | 1,762 lines |
| sidebar-07 / 08 (official) | any React | shell only | no | no | no | none | ~400 lines |
| tasks example (official) | any (page.tsx is Next) | no | yes | yes (faceted filters) | no | none | 921 lines |
| message + message-scroller (official) | any React | no | no | no | chat surface only | none | a few hundred |
| shadcn-ui/chatbot-template | Next.js 16 | no | no | no | chat, no history | none | ~1,050 app lines |
| vercel/chatbot | Next.js 16 | no | no | no | yes, with history | none | ~15,700 app lines |
| satnaing/shadcn-admin | Vite + TanStack Router | yes | yes | yes | chat layout with list (mock) | Recharts direct | ~15,000 app lines |
| Kiranism starter | Next.js 16 | yes | yes | yes | no | Recharts | large, not counted |
| AI Elements | Next.js required | no | no | no | chat surface | none | registry |
| assistant-ui | any React, Next CLI | no | no | no | chat surface, runtimes | none | library |

## 4. Findings that matter for the pick (ticket 05)

1. shadcn/ui does not push Next.js. Seven setups are equal in the docs, and the blocks are
   advertised as working with all React frameworks. The official dashboard block has no Next.js
   import at all. A Vite SPA is a fully supported, documented path.
2. No single template covers all four screens. The two that come closest are the **official
   pieces composed by hand** (dashboard-01 for the shell and Overview, the tasks example for the
   two tables, `message` + `message-scroller` for the chat) at about 3,000 lines in total, and
   **shadcn-admin**, which has every screen shape including a chat page with a conversation list
   but arrives with 15,000 lines of which most would be deleted.
3. Every chat **template** (shadcn's own, Vercel's) is Next.js plus the AI SDK, with the model
   call inside Next.js server routes. v2's model call lives in FastAPI, so these templates would be
   stripped down to their UI anyway. The official `message`, `bubble` and `message-scroller`
   components give that UI without the Next.js wrapper.
4. Chart library: everything in this space uses **Recharts**. Official blocks use Recharts v3
   through the shadcn `chart` component, which "does not wrap Recharts". This answers the map's
   "Chart library" open item unless the author objects.
5. Table library: **TanStack Table** everywhere. The official guide is now on v9; shadcn-admin and
   the Kiranism starter are still on v8.
6. Reading load for the author: the composed official route is roughly 3,000 lines, all of it
   code that ends up in v2. The shadcn-admin route is about 15,000 lines to read before deciding
   what to delete, plus TanStack Router and Clerk to understand.
