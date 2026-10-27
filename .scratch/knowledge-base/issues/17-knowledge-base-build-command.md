# 17: The knowledge-base build command

Type: build
Status: claimed
Blocked by: 09, 11, 14
Phase: 0
Model: strongest (Fable 5.1 or Astra)

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
- [author's ruling, 25 October 2026] Table access through SQLAlchemy Core (no ORM) on the psycopg
  driver, one engine and pool shared with LangChain's `PGEngine`; tables defined in code; the
  read-only role as a second engine. Spec, "The store and the build".
- User stories 63 to 65, 68.
- [author's rulings at ticket 16, 27 October 2026] Spec, "Chunking rulings at T16": sizes for the
  five unplanned own kinds, whole runbook steps, ATT&CK cleaning of chunk text, packed procedure
  examples. Measurements in ticket 16's "Length comparison".

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] One build command loads the tables, chunks, vectors, keyword index and link table from the
      dataset folder into a fresh database through the build role.
- [ ] Chunks are cut at Markdown headings, then by token size only inside an over-long section; no
      overlap crosses a section; every chunk begins with its context header.
- [ ] Email, guidance, meeting, record and register documents chunk at 350 tokens with 30 to 50
      overlap, as policies do.
- [ ] A test proves every numbered runbook step lands whole in one chunk, on the three runbooks
      whose step sections exceed 350 tokens.
- [ ] ATT&CK chunk text holds no `## References` content, no `(Citation: ...)` marker, no link
      address and no `<code>` tag; link text stays. A test fails if any slips in. The files are
      unchanged.
- [ ] ATT&CK procedure examples are packed several to a chunk, up to 350 tokens, each example
      whole, under the field group's context header; a test proves no example is split.
- [ ] A test proves chunk IDs follow the agreed format and stay the same across rebuilds.
- [ ] Chunks sit in LangChain's PostgreSQL store table with typed filter columns (document type,
      technique ID, incident ID, version, effective date) and a JSON column.
- [ ] The link table holds mentions found by ingestion from the text. The keyword parser's output is
      recorded for one technique ID, hostname, IP address and email address.
- [ ] Door 2 tests use a fake embedder and the real PostgreSQL fixture from ticket 09. The one-string
      embedder check against OpenRouter is run once and recorded.
- [ ] A test proves the read-only role is refused a write.
- [ ] Our tables are defined and queried with SQLAlchemy Core through the engine LangChain's store
      also uses; `sqlalchemy` is pinned exactly, with its x86_64 build checked.
- [ ] The build runs on the ATT&CK pages alone; a test with one sample own document proves the own
      corpus needs no code change.
- [ ] The first real build's time and cost are measured and recorded.
- [ ] The core-boundary test covers the new modules.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-27: Codex claimed T17 at the author's request using implement and tdd. Tests use the already agreed door 2 (build/open/read the knowledge base), with a fake embedder and real PostgreSQL. Review baseline: `6be34cc8d1b4649eaba4d4d34a41537b6c8e3e90`. T18 owns fingerprint recording and the startup guard.
- 2026-10-27: The author confirmed Astra is selected. Codex initially relied on the earlier ticket read and missed the subsequently added model-confirmation criterion; implementation paused when noticed and resumed after this explicit confirmation. The first four door-2 tests cover the build/read round trip, section limits, whole numbered steps, and ATT&CK cleaning/packing. The administrator created `li_reader` and saved its password in `.env`; no password was shared in chat.
