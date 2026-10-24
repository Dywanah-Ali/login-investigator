# 07: What the screen shows for an explained alert

Type: prototype
Status: resolved
Blocked by: 05

## Question

Where and how does the explanation appear: in the Alerts details panel, in the Investigator
answer, or both? What does the analyst see for blast radius, spread and shared ground, and how
are citations shown?

## Scope

- A rough prototype in the style of `.scratch/v2-port/research/07-screens-prototype.html`, using
  the Port's shell and shadcn/ui pieces.
- Candidates: a "Context" section in the Alerts details panel fed by a new API field; an
  "Investigate" handover that pre-asks the agent the blast-radius question; both.
- Citations: how a graph path and a document passage are shown as plain text, with the Port's
  rule that log, graph and corpus fields never pass through a markup renderer.
- The API contract change, if any, written before the build.

## Acceptance

- [ ] Prototype reviewed with the author and the placement chosen.
- [ ] API contract addition drafted, if the Alerts panel gains context.
- [ ] Decision recorded here under `## Answer`.

## Comments

**2026-10-24, claimed. How the question has narrowed, and the order of work.**

Ticket 05 settled most of the ticket's original question before this ticket started: the chat is
the screen (R3), the Alerts API gains a finding ID and no context field (decision 16), nothing
runs unless the user asks (entry-point ruling). The "Context section in the Alerts details panel"
candidate is therefore closed. The Port already has an Investigate button in the alert details
panel that opens the Investigator with a pre-written question; the only change there is that the
question carries the finding ID, so the agent calls `investigate_alert` on exactly that alert.

What remains is how the chat shows an explained alert well. Four design decisions were identified:

1. Where a citation lands: footnotes under the answer, an expandable card per citation, or a side
   evidence panel built from the saved artifact.
2. How a graph path is written as plain text, since graph fields never pass through a markup
   renderer.
3. How the three radii (groups, assets, peers) are shown: counts in the answer with lists in the
   evidence panel, or full tables in the answer.
4. What the user sees while the playbook runs, and whether those progress lines stay or collapse
   once the answer arrives.

Considered and leaning against: the judge's reason on the screen (ticket 06, decision 6). It is a
smoke alarm for the eval, not information for an analyst; showing it would teach the user to trust
a signal that is not a gate.

**Order of work (author's ruling, 24 October 2026).** The author cannot decide any of the four
from a description and must see them first. So the prototype comes before the grilling, not after:
every option is drawn as a toggle in one HTML file, the author reviews it in the browser, and the
grilling runs with the picture in front of them, one question at a time with a plain heading each.
Prototype: `../research/07-explained-alert-prototype.html`.

**Grilling, 24 October 2026, with the prototype open.** Running record; the Answer section
consolidates it at resolution.

1. Where a citation lands: **evidence panel** (author overruled Claude's recommendation of
   footnotes). A right-hand column lists every cited record and passage for the conversation,
   built from the saved artifact; clicking a label highlights its row.
2. Graph path as text: **one line per hop**, an indented list, each hop a short sentence
   carrying its own citation label, so a click on a hop lights its record in the panel.
3. The three radii: **counts first**. Three tiles in the answer (number, worst item, a "See
   list" link); the full lists of groups, assets and peers live in the evidence panel.
4. Progress: streamed per step while the tool runs (ticket 05, decision 2); **collapses into
   the Tools used drawer** once the answer arrives. The report's "Not checked" line keeps a
   failed step visible without the drawer. Refined after Claude raised AUD-027 (the author
   rejected a growing list of progress lines in the Port and kept one changing status line):
   **the five steps stack while the investigation tool runs, as an exception for this tool
   only**; the Port's tools keep their single line. The author's reasoning: Claude Code itself
   mixes a single line for short work with a stacked list for long work, and the stack is a
   signal that the agent chose the full investigation rather than a quick lookup. Claude had
   first recommended one line with the step inside it, and changed its recommendation on that
   argument.
5. The artifact is **viewable in the panel and downloadable as JSON** from it. The download
   carries only what the panel shows: records, passages, scores, verdicts. Never prompt text,
   never the memory file.
6. Citation letters: **L for log, G for graph, D for document**, numbered per answer ([L1],
   [G1], [D1]). Ticket 05 fixed the idea of short labels, not the letters; the prototype's A
   and S are replaced.
7. The finding ID **shows as a column** on the Alerts table, first column, so the analyst can
   name a finding in chat and match it to the report and the panel.
   **Author's condition on the build (24 October 2026):** before the progress display is built,
   the build ticket starts with a short research step into how Anthropic and OpenAI document
   streaming progress for multi-step agent work (their official docs and reference apps), and
   records the patterns borrowed, so the implementation is reliable and friendly to use rather
   than invented here. The author also noted that mixed progress styles (a single line for short
   work, a stacked list for long work) are what Claude Code itself shows and reads well.
8. The judge's reason **stays off the screen** in this initiative. Reopen as its own ticket once
   the judge's agreement with human labels is measured (ticket 06, decision 6).
9. Raised by the author before the ticket closed: the new parts of the answer carry more weight
   than the prose and need a **visual hierarchy** so the eye finds them. Claude proposed a
   five-level ranking; the author accepted it and added that citation tags take a calm link
   blue so they read as clickable. Recorded as decision 9 in the Answer.

## Answer

Resolved 24 October 2026 after a prototype review and an eight-point grilling with the prototype
open, one question at a time, plus a ninth decision the author raised from the prototype. The prototype is
[`07-explained-alert-prototype.html`](../research/07-explained-alert-prototype.html); its
defaults now show the chosen set, with the rejected options still available as buttons for the
record.

**Placement.** The chat is the screen, as ticket 05 ruled. The Alerts details panel gains no
context section. The Port's Investigate button keeps its job and its pre-written question now
carries the finding ID. The Alerts table shows the finding ID as its first column.

| # | Decision | Why |
|---|---|---|
| 1 | **Citations land in an evidence panel.** A third column on the right of the chat lists every cited record and passage for the conversation, built from the saved artifact. Clicking a label in the answer highlights its row. Footnotes and expandable chips are not taken. | The author's choice over Claude's recommendation of footnotes. One place for all proof across turns; the panel is the eval's artifact made visible. |
| 2 | **A graph path is one line per hop**: an indented list, each hop a short sentence carrying its own citation label. No arrows, no table, no drawing. | Readable aloud; each hop lights its own record in the panel. Graph values stay plain text. |
| 3 | **Radii as counts first.** Three tiles in the answer (number, worst item, "See list"); the full lists of groups, assets and peers live in the evidence panel. | Keeps the chat readable; the panel exists for the detail. |
| 4 | **Progress stacks per step while the investigation tool runs, then collapses into Tools used.** An exception to the Port's single-status-line rule (AUD-027), for this tool only; the Port's tools keep their one line. The report's "Not checked" line keeps a failed step visible without the drawer. **Build condition:** the build ticket begins with a research step into how Anthropic and OpenAI document streaming progress for multi-step agents, and records the patterns borrowed. | The stack signals that the full playbook ran. Mixed styles read well, as Claude Code itself shows. |
| 5 | **The artifact is viewable in the panel and downloadable as JSON** from it, carrying only what the panel shows. | The file exists for the eval; the button makes a case handable. |
| 6 | **Citation letters are L (log), G (graph), D (document)**, numbered per answer. | First letter of each source; plain for analysts, the model and the eval. |
| 7 | **The finding ID shows as the first column** of the Alerts table. | An ID nobody sees is an ID nobody uses. |
| 8 | **The judge's reason stays off the screen.** | A smoke alarm, not analyst information; reopen when its agreement with labels is measured (AUD-043). |
| 9 | **A visual hierarchy for the answer, few things loud and the rest quiet** (author's addition after reviewing the prototype). Ranked: (1) the verdict and the "Cleared by" line are the one coloured surface per answer, red tint for threat, green for benign, amber for "cannot tell", the same colours as the report card; (2) the "Not checked" warning and an unverified citation are amber and never hidden; (3) the radii tiles and the path block are bordered boxes on the normal background, structure without colour; (4) citation tags are small and monospace in the app's link colour, a calm light blue, so they read as clickable without flashing; (5) prose stays plain. No new colours enter the app: red, green and amber already exist in the severity badges. Exact shades and the dark-mode check are settled at build with the author's screenshot review, under the screens rule. The prototype's dashed orange marks "new in this initiative" for review and is not a design. | The answer now carries a verdict, radii, a path, tags and warnings; if they all look alike the analyst reads a wall, and if they all shout nothing stands out. |

### API contract addition (draft, for the spec)

Two changes to `docs/api-contract.md`, to be made when the spec is written. Nothing else in the
contract moves.

1. **Alerts.** Each alert gains `"finding_id": "F-0006"` (ticket 05, decision 16). The Investigate
   link's question becomes `Investigate finding <finding_id>: <rule title>, <first IP> against
   <N accounts | first user> from <first_seen> to <last_seen> UTC.` Still frontend-built, still
   no API involvement beyond the new field.
2. **Investigations: reopen.** Each turn gains `"evidence"`: the resolved citations for that
   turn, built in the API from the artifacts the checkpointer saved, never from the model's text.
   One entry per label the answer used, in order of first use:

   ```json
   "evidence": [
     {"label": "G1", "kind": "graph", "id": "mem-0117",
      "title": "membership mgarcia → IT Admins", "text": null, "score": null},
     {"label": "D1", "kind": "document", "id": "reg-mfa-exceptions#7",
      "title": "MFA exception register v3, row 7", "text": "| mgarcia | service migration | …",
      "score": 0.81},
     {"label": "L1", "kind": "log", "id": "rows:2026-10-06T03:24:17Z/mgarcia",
      "title": "2 of 42 rows", "text": "03:24:17 UTC mgarcia 185.220.101.4 success, mfa none",
      "score": null},
     {"label": "D2", "kind": "search", "id": null,
      "title": "Clearing documents: none above the threshold", "text": null, "score": 0.31,
      "verdict": "none"}
   ],
   "radii": {"groups": [...], "assets": [...], "peers": [...]},   // the full lists, or null
   "unresolved": ["D9"]                                           // labels that failed twice
   ```

   `text` is document or log text and renders as plain text only. `kind` is one of `log`,
   `graph`, `document`, `search`. `radii` is present only on turns where the investigation tool
   ran. A separate `GET /api/investigations/{id}/artifact.json` serves the same payload for the
   whole conversation as a download, `Content-Disposition: attachment`; it carries nothing from
   the prompt or the memory file beyond these fields.
3. **Investigations: ask.** A new stream event `step` with
   `{"call_id": "…", "step": 3, "of": 5, "name": "peers", "phase": "start" | "end" | "error"}`,
   emitted only by the investigation tool. The Port's `tool` events are unchanged. The frontend
   stacks `step` events for the active `call_id` and keeps the single status line for every
   other tool.

### Considered, not taken

- Footnotes under the answer and expandable chips in the sentence (decision 1).
- Arrow chain and hop table for paths (decision 2). The arrow chain may return in phase 4 if
  attack paths grow long.
- Full tables for the radii in the answer (decision 3).
- One status line with the step inside it (decision 4), Claude's first recommendation.
- Letters L, A, S (decision 6).
- The judge's reason on the screen (decision 8).

### Hand-offs

- **The spec (`mp-to-spec`):** the API additions above; the evidence panel as a shadcn piece in
  the Port's shell (a third column that collapses under the chat on narrow screens); the step
  stack and its collapse; the finding ID column; the download endpoint; the build condition on
  decision 4; the visual hierarchy of decision 9 as a named rule the build ticket checks with a
  screenshot review.
- **Phase 0 build:** the `evidence` resolver in the API is the same code the eval's `cites`
  check uses (ticket 06, decision 5), so screen and exam cannot disagree.
- **Phase 1 acceptance:** the author accepts the live screen on S6 and on one twin, with the
  panel showing every citation the eval's gold set names.

### Acceptance

- [x] Prototype reviewed with the author and the placement chosen (decisions 1 to 4, 7).
- [x] API contract addition drafted (the section above; the Alerts panel gains no context, the
      reopen and ask replies gain evidence, radii and step events).
- [x] Decision recorded here under `## Answer`.
