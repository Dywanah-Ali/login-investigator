# Pick the template and framework

Type: prototype
Status: resolved
Blocked by: 04
Map: [map.md](../map.md)

## Question

Choose the shadcn/ui starting point and the frontend framework together, from the candidates found
in [shadcn/ui templates and the frameworks they need](04-shadcn-templates.md).

Make a cheap, concrete artifact the author can react to: two or three candidates shown side by side
(screenshots, a rough wireframe, or a stub that runs locally), each with its framework, what it
covers of the four screens, and what the author would have to read.

Decide:

1. The template, block set or starter kit v2 starts from.
2. The framework (Next.js or Vite React), chosen because the template needs it or because it keeps
   the frontend simplest to review.
3. What the choice implies for the chart library, if the template ships one.

Record the reason for the choice, not only the choice. The answer unblocks
[Map the four screens onto the template](07-map-screens.md) and may graduate the "Chart library" fog.

## Comments

## Answer

Prototype: [research/05-template-prototype.html](../research/05-template-prototype.html), also published
at https://claude.ai/artifact/5YDdg6Th6H8hajDdhLPqqh. Three candidates side by side, each showing the four
screens as they would start, with what comes with the candidate, what v2 must build, and what must be
deleted. Decided by the author on 14 October 2026.

1. **Starting point: the official shadcn/ui pieces, composed by hand.** `dashboard-01` for the shell
   (sidebar, header) and Overview (KPI cards, chart); the official tasks table example for Alerts and
   Log explorer (TanStack Table v9, faceted filters); the official `message`, `bubble` and
   `message-scroller` components for Investigator. About 3,000 lines, all of which stay in v2.
2. **Framework: Vite, with React Router in its plain declarative mode** (four routes, no server
   rendering). Chosen because the pieces need no framework, shadcn/ui recommends none, and Vite keeps
   the frontend smallest to review.
3. **Chart library: Recharts v3 through the shadcn `chart` component.** It is what the chosen block
   ships, and every candidate used it. This closes the map's "Chart library" open item.

Reasons, not only the choice:

- Every line in the repo should be a line the author chose. Candidate B (satnaing/shadcn-admin, Vite +
  TanStack Router) arrives with about 15,000 lines of which about 12,000 are deleted; a trimmed fork is
  the hardest thing to review, and it lags the official guide (TanStack Table v8).
- Candidate C (the same official pieces plus shadcn-ui/chatbot-template on Next.js 16) has the same
  screens as A but adds a server framework with no server work to do, and three new ideas to learn
  (App Router, server versus client components, an idle second server). The chatbot template's
  transport (AI SDK `useChat`, `api/chat` route) is deleted anyway, leaving the same `message`
  components A uses.
- What v2 must build is the same in all three: the past-investigations list, the SSE reader (ticket
  06), the shared filter bar, v1's charts, the report card with links and images off, the explorer jump.

Rejected: B and C as above. Not considered further: vercel/chatbot, Kiranism starter, AI Elements
(all Next.js), assistant-ui (a library with its own runtime model).

Hands to [Map the four screens onto the template](07-map-screens.md): the pieces above are the
vocabulary for the screen mapping. Open for ticket 07 or 09: whether the Overview chart block's
interactive area chart is reused for v1's by-hour chart or replaced.
