# 17: The knowledge-base build command

Type: build
Status: ready-for-agent
Blocked by: 09, 11, 14
Phase: 0

## What to build

One build command reads the dataset folder and builds the knowledge base in a fresh PostgreSQL
database: the organisation's tables, the corpus cut into chunks with a context header, their
vectors, their keyword index, and the chunk-to-entity link table. The build runs as a build role;
the agent will read through a role that can only read. The command works on the ATT&CK pages alone,
and the own corpus flows in with no code change once ticket 16 delivers it.

## Decisions implemented

- T02 d1 (one store), T02 d5 and d6 (fresh database per build, the files are the truth, full
  rebuild), T02 d7 (chunk storage in LangChain's PostgreSQL store with typed filter columns),
  T02 d8 (two read-only locks; the build uses a separate role).
- T03 d2 (`openai/text-embedding-3-small` through OpenRouter at 1,536 dimensions, context-length
  check off, model and length in one configuration place), T03 d3 (structure-first chunking with a
  context header), T03 d4 (identifiers as typed columns plus a chunk-to-entity link table).
- Spec "The IDs": chunk ID `<doc-slug>@<version>#<section-path>/<ordinal>`; [spec ruling] the running
  app's database is built once by an explicit command; [spec ruling] door 2 uses a fake embedder.
- Pinned versions: `langchain-postgres` 0.0.19, `langchain-text-splitters` and `tiktoken` exactly.
- User stories 63 to 65, 68.

## Acceptance criteria

- [ ] One build command loads the tables, chunks, vectors, keyword index and link table from the
      dataset folder into a fresh database through the build role.
- [ ] Chunks are cut at Markdown headings, then by token size only inside an over-long section; no
      overlap crosses a section; every chunk begins with its context header.
- [ ] A test proves chunk IDs follow the agreed format and stay the same across rebuilds.
- [ ] Chunks sit in LangChain's PostgreSQL store table with typed filter columns (document type,
      technique ID, incident ID, version, effective date) and a JSON column.
- [ ] The link table holds mentions found by ingestion from the text. The keyword parser's output is
      recorded for one technique ID, hostname, IP address and email address.
- [ ] Door 2 tests use a fake embedder and the real PostgreSQL fixture from ticket 09. The one-string
      embedder check against OpenRouter is run once and recorded.
- [ ] A test proves the read-only role is refused a write.
- [ ] The build runs on the ATT&CK pages alone; a test with one sample own document proves the own
      corpus needs no code change.
- [ ] The first real build's time and cost are measured and recorded.
- [ ] The core-boundary test covers the new modules.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
