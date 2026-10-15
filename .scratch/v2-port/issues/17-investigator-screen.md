# 17: Investigator screen

**What to build:** the analyst asks a question, watches the progress line name each tool, reads the
answer as it arrives, opens "Tools used" under the answer, writes the report when the button offers
it, downloads the PDF, and reopens a past Investigation from the list the next day. An injected link
or image in an answer never becomes a link or an image.

**Blocked by:** 13 (Frontend shell and the Overview screen), 16 (Investigations API).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "The frontend", "The stream", "Security rendering". Decisions: ticket 07.

- [ ] Second column: "New investigation" and the list, newest three, three more per click, the open one always shown; the API sends the full list
- [ ] Chat with the official message components; the stream read with fetch and a stream reader, aborted on unmount; `tool` events drive the progress words per tool; input locked while answering; after `done` or `error` the Investigation is fetched again and the Turn redrawn from memory
- [ ] "Tools used" collapsible under each answer: asked and found lines, rows in a table, raw JSON behind a switch
- [ ] Visual hierarchy (spec, "The frontend"): the chat leads; the past-Investigations column and the "Tools used" panels step back, with the shared quiet styling from ticket 15
- [ ] Report button only when the Report offer says so, with its wording; "Writing the incident report…" while waiting; the report as a card with fixed fields as plain text, its severity with its label and colour, and a "Download PDF" link to the API
- [ ] Starter questions and the scope line only in an empty Investigation; the AI note by the input; "Investigate" arrival puts the prepared question in the input box without sending
- [ ] A missing model key shows the fixed 503 message on this screen only
- [ ] Allowlist markdown renderer in exactly one component: paragraphs, bold, italics, lists, headings, inline code, code blocks; links shown as plain text, images dropped, raw HTML never rendered
- [ ] Guard test: the S5 injection strings and crafted answers (markdown links, image tags, raw HTML, javascript: URLs) produce no anchor, image, script, iframe or raw HTML
- [ ] Vitest: paging of past Investigations, the renderer guard, the locked input
