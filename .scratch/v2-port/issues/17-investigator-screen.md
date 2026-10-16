# 17: Investigator screen

**What to build:** the analyst asks a question, watches the progress line name each tool, reads the
answer as it arrives, opens "Tools used" under the answer, writes the report when the button offers
it, downloads the PDF, and reopens a past Investigation from the list the next day. An injected link
or image in an answer never becomes a link or an image.

**Blocked by:** 13 (Frontend shell and the Overview screen), 16 (Investigations API).

**Status:** ready-for-human

Spec: [spec.md](../spec.md), "The frontend", "The stream", "Security rendering". Decisions: ticket 07.

- [x] Second column: "New investigation" and the list, newest three, three more per click, the open one always shown; the API sends the full list
- [x] Chat with the official message components; the stream read with fetch and a stream reader, aborted on unmount; `tool` events drive the progress words per tool; input locked while answering; after `done` or `error` the Investigation is fetched again and the Turn redrawn from memory
- [x] "Tools used" collapsible under each answer: asked and found lines, rows in a table, raw JSON behind a switch
- [ ] Visual hierarchy (spec, "The frontend"): the chat leads; the past-Investigations column and the "Tools used" panels step back, with the shared quiet styling from ticket 15
- [x] Report button only when the Report offer says so, with its wording; "Writing the incident report…" while waiting; the report as a card with fixed fields as plain text, its severity with its label and colour, and a "Download PDF" link to the API
- [x] Starter questions and the scope line only in an empty Investigation; the AI note by the input; "Investigate" arrival puts the prepared question in the input box without sending
- [x] A missing model key shows the fixed 503 message on this screen only
- [x] Allowlist markdown renderer in exactly one component: paragraphs, bold, italics, lists, headings, inline code, code blocks; links shown as plain text, images dropped, raw HTML never rendered
- [x] Guard test: the S5 injection strings and crafted answers (markdown links, image tags, raw HTML, javascript: URLs) produce no anchor, image, script, iframe or raw HTML
- [x] Vitest: paging of past Investigations, the renderer guard, the locked input


## Comments

- 16 October 2026: author requested `implement T17`. Test seams are the frontend screen and
  answer component, already agreed in the ticket and spec. Review baseline: `af6120a`.
  Implementation and automated checks are complete. The visual hierarchy checkbox remains open
  for the author's review. No spec changes or pushes.

## Answer

Implemented on 16 October 2026. Awaiting the author's live screen review before resolving.

- The Investigator route uses the official shadcn message components. The chat leads a quiet
  history column and quiet tool panels. History shows three more per click and retains the open
  Investigation. Selection is kept in the address so a saved Investigation can be reopened.
- Create-then-ask uses fetch and a stream reader. Input and selection controls lock during asks
  and report writing. Tool names map to the original progress wording. Done, error and interrupted
  streams reload saved history. Leaving the screen or selecting another ID through browser
  history aborts the operation. Creation transfers ownership before changing its address.
- Tools show core-produced asked/found text, ordered table cells and raw JSON behind a switch.
  Report offers retain the core's wording. Reports use fixed plain-text fields, severity labels
  and colours, and numbered PDF links. Prepared questions are never sent automatically.
- One allowlist answer component supports the agreed markdown. Link addresses remain visible as
  non-clickable text. Images and raw HTML are dropped. Report and tool fields bypass markdown.

Evidence:

- Frontend full suite: **103 passed**. Thirteen added tests cover paging, prepared arrival,
  locked input, progress/text streaming, authoritative memory redraw, tool evidence/raw switch,
  report writing/PDF, fixed 503 and stream errors, unmount cancellation, fragmented UTF-8/SSE,
  browser navigation during both answers and reports, markdown formatting and S5 rendering guards.
- Backend full suite: **351 passed**. Core and API remain unchanged.
- TypeScript and Pyright: clean. Lint: no errors and only six existing warnings. Production
  build passed. `git diff --check` passed.
- Standards review: prompt-log gap and possible lifecycle duplication corrected. Re-review clear.
- Spec review: browser-navigation race corrected and covered by failing-then-passing regressions.
  Re-review clear. B-016 through B-020 retain findings and iterations.
- Read-only preview smoke: `/investigator` and the transformed screen module return 200 through
  the isolated Vite preview. Investigation requests return the contracted 503 because this
  environment has no model key. No model calls or existing Investigation records were changed.

Concerns and remaining acceptance:

- Author to review the visual hierarchy, narrow layout and live Investigation flow. No browser
  automation or screenshots were used, in line with the spec. Automated screen tests use the real
  frontend with responses supplied at the HTTP boundary. A live model run has not been performed.
- Preview: http://127.0.0.1:5174/investigator, API on 8002, temporary memory at
  `/tmp/login-investigator-t17-preview.sqlite`. Existing previews on 5173/8000/8001 were left alone.
- Set `OPENROUTER_API_KEY` in `.env` and restart the preview API for live agent review. Never paste
  a key into chat. The current fixed missing-setting screen is working as specified.
- Existing lint warnings: TanStack compatibility in both tables, Fast Refresh exports in badge,
  button and sidebar, and the mobile hook's state-setting effect. The production build still
  warns about the main JavaScript chunk, now approximately 1,050 kB minified.
- Seven existing dependency advisories remain separate maintenance work, recorded in B-017.
