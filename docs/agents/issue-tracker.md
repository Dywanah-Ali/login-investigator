# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The spec is `.scratch/<feature-slug>/spec.md`
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`, never a single combined tickets file
- Triage state is recorded as a `Status:` line near the top of each issue file. The role strings are `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human` and `wontfix`. Wayfinder tickets use `claimed` and `resolved` instead (see below)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Documentation lookup evidence

For both Claude and Codex, record third-party library or API documentation lookups in the
relevant ticket under `## Comments`. For the current initiative, tickets live in
`.scratch/knowledge-base/issues/`. Keep one short dated note per lookup with the library and
version (or API version when available), a link to the documentation consulted, and the
specific behaviour checked. Name Context Hub or another lookup tool when used.

Example format:

> YYYY-MM-DD — Agent: library/version; documentation: [page title](URL), via lookup tool;
> checked: the function or behaviour relevant to this ticket.

When reusing an earlier lookup, link to its ticket note and state why it applies to this version
and behaviour. If documentation is unavailable, record that limitation and any alternative
evidence, such as installed source or a live check. Do not describe tests or source inspection
as a documentation lookup. Record only work actually performed; do not backfill assumed
lookups into completed tickets. No separate documentation log is needed.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
