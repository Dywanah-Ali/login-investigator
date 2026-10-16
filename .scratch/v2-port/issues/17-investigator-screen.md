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

### Follow-up: basic live smoke, 16 October 2026

The author configured `.env` and requested a basic live frontend test without opening that file.
The file was not opened, printed or edited. Git confirms it is ignored. After restarting the
isolated API, its Investigation list returns 200 through the frontend preview.

One live question was submitted through the real React screen in Vitest's DOM environment,
using real HTTP through the Vite proxy and the configured model. The input locked; the answer
arrived and was saved; the report offer appeared. The agent used two sign-in-log tool calls.
Tool evidence tables displayed and the saved Investigation reopened with identical answer and
evidence. An initial temporary-test assumption about one tool call was corrected; the corrected
smoke passed against the saved answer, without another model request. See B-021/B-022 and P-017.
The temporary test was removed from the regular suite after the smoke run.

This supersedes the earlier missing-key preview limitation and "no live model run" note.
The preview is ready at http://127.0.0.1:5174/investigator. AbuseIPDB, report generation and PDFs
were not exercised in this narrow smoke. Comprehensive evaluations remain T18 work and final
live acceptance remains T19 work. Author visual approval for T17 is still pending.

### Follow-up: restore the approved layout, 16 October 2026

The author supplied the approved artifact and screenshot, showing that history belongs on the
**left inside the page**, with chat on its right. Compared the implementation with ticket 07's
saved `research/07-screens-prototype.html`. This is a correction to the existing approval, not a
spec change. B-023 and P-018 record the finding and iteration.

- Restored the narrow left history column, quiet entries and selected-entry outline/tint.
- Removed the outer chat card and visible repeated first-question heading. Compact message bubbles
  align analyst questions right and agent answers left. The official bubble and message-scroller
  components now accompany the existing official message components as agreed in ticket 07.
- The composer keeps the question and Send button together. The AI note is directly below it.
- Tool evidence uses a quiet left rule and compact spacing; report cards have compact fields and
  a severity accent. Security rendering, report offers, input locking and API requests are unchanged.
- Message scrolling follows the active answer, allows reading earlier turns, and offers a
  scroll-to-end control. Provider state resets when selecting another Investigation.

The visual hierarchy checkbox remains open for the author's review. Existing screen and renderer
checks pass; final build and review evidence follows. No browser automation or screenshot capture.

Correction evidence:

- Full frontend suite: **103 passed**. TypeScript clean. Lint has no errors and only the six
  existing warnings. Production build passed; the existing bundle warning remains, with the main
  JavaScript chunk approximately 1,076 kB minified after adding the official scroller.
- Standards review: clear. Spec review: clear after explicitly comparing the saved approved
  prototype's left-column arrangement, message proportions and composer structure.
- Read-only preview smoke: the Investigator route and transformed page, bubble and scroller
  modules all return 200 on port 5174. No additional model request was made.
- `git diff --check`: clean. Layout correction committed locally as `f016aa4`. Nothing pushed.
- Source review and component checks do not establish final pixel proportions or scrolling feel.
  The author's visual acceptance remains pending.

### First author review comment: Send on port 5173, 16 October 2026

The author reported that typing enabled Send but sending did not start a new Investigation.
Confirmed the author was using the original port 5173 preview, whose proxy target lacked the
Investigation routes (404). Port 5174 already worked. Restarted the workspace's Vite process on
5173 with `LI_API_URL=http://127.0.0.1:8002`, preserving the existing API and temporary memory.
The author's original address now works. See B-024 and P-019.

A full React screen smoke, using real HTTP and a short live model question, passed at the exact
port 5173 address: typed question appears, input locks, answer is saved, report offer appears and
input unlocks. No application-code or `.env` change. The normal screen test suite now uses
StrictMode and includes a manually typed new-question check. Temporary live tests were removed
so normal tests do not make paid calls. No browser or visual acceptance is claimed.

Current author preview: http://127.0.0.1:5173/investigator. Port 5174 remains available and uses
the same current API. Further review comments are handled one at a time; T17 remains ready-for-human.

### Response review: tool count and report reveal, 16 October 2026

The author confirmed the repaired port 5173 preview works, then requested a count on Tools used
and automatic scrolling to the end of a generated report. B-025/B-026 and P-020 record both.

- The toggle now reads `Tools used (N)` for that answer. N counts calls, including repeated calls
  to the same tool. Reopened history uses the same component and count.
- A newly saved report requests the existing scroller's scroll-to-end action even if the reader
  has moved upward. The component resets with the Investigation's scroller provider. It does not
  repeatedly jump after later evidence toggles or manual scrolling.
- Screen regressions cover one/two calls and overflowing report content. The report test failed
  before the fix, passes afterward, and verifies that scrolling back still works.
- Backend, API contract and rendering boundary are unchanged. No extra live model request or
  `.env` access. Visual acceptance remains with the author; no browser automation was used.

Final validation and review evidence follows.

Response-correction evidence:

- Full frontend suite: **105 passed**. TypeScript clean. Lint has no errors and only the six
  existing warnings. Production build passed with the existing main-chunk warning.
- Standards review: clear. Spec review: clear for the count and explicit report-reveal request.
- Correction committed locally as `a75d1a6`. `git diff --check` passed. Nothing pushed.
- The scroll regression uses the real component with supplied DOM geometry. Browser scrolling
  and overall visual approval remain the author's review step on port 5173.

### Chat styling and empty-state review, 16 October 2026

The author requested distinct pink user messages and research-led improvement of scope/starter
placement. The research skill saved a primary-source note at
[17-chat-empty-state.md](../research/17-chat-empty-state.md). B-027/B-028 and P-021 record the
findings, direct author instruction and resulting design choices.

- Soft rose user bubbles differ from neutral agent answers in both themes. Visible speaker
  labels and existing alignment provide additional cues. Calculated normal-text contrast exceeds
  4.5:1 in both themes. No error/severity meaning is attached to the user-message surface.
- A stable-height chat viewport contains the empty-state welcome, original read-only scope and
  three starter cards. Cards wrap on narrow screens and still populate the input without sending.
- The welcome disappears after Send. Empty-state scrolling starts at the top; ordinary chat and
  explicit new-report scrolling keep their established behaviour. Composer and AI note remain below.
- The approved left history column, API contract, security rendering and agent behaviour are unchanged.
  These are refinements requested directly during the author's T17 review; no new feature scope.
- Focused component checks pass, including the new inside-viewport starter interaction regression.
  No browser automation or screenshot capture. Visual acceptance remains pending.

Final validation and review evidence follows.

Chat-refinement evidence:

- Full frontend suite: **106 passed**. TypeScript clean. Lint has no errors and only the six
  existing warnings. Production build passed with its existing main-chunk warning.
- Standards review: clear, including bubble class precedence and scrolling lifecycle.
- Spec review: clear for the author's requested speaker distinction and inside-chat welcome.
- Primary-source research and the applied colour/contrast calculation are recorded in
  [17-chat-empty-state.md](../research/17-chat-empty-state.md).
- Implementation committed locally as `db4df51`. `git diff --check` clean. Nothing pushed.
- The author checks the resulting colours, proportions and empty-state feel on port 5173 next.
