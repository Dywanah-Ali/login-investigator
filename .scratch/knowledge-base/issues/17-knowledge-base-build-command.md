# 17: The knowledge-base build command

Type: build
Status: resolved
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

- [x] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [x] One build command loads the tables, chunks, vectors, keyword index and link table from the
      dataset folder into a fresh database through the build role.
- [x] Chunks are cut at Markdown headings, then by token size only inside an over-long section; no
      overlap crosses a section; every chunk begins with its context header.
- [x] Email, guidance, meeting, record and register documents chunk at 350 tokens with 30 to 50
      overlap, as policies do.
- [x] A test proves every numbered runbook step lands whole in one chunk, on the three runbooks
      whose step sections exceed 350 tokens.
- [x] ATT&CK chunk text holds no `## References` content, no `(Citation: ...)` marker, no link
      address and no `<code>` tag; link text stays. A test fails if any slips in. The files are
      unchanged.
- [x] ATT&CK procedure examples are packed several to a chunk, up to 350 tokens, each example
      whole, under the field group's context header; a test proves no example is split.
- [x] A test proves chunk IDs follow the agreed format and stay the same across rebuilds.
- [x] Chunks sit in LangChain's PostgreSQL store table with typed filter columns (document type,
      technique ID, incident ID, version, effective date) and a JSON column.
- [x] The link table holds mentions found by ingestion from the text. The keyword parser's output is
      recorded for one technique ID, hostname, IP address and email address.
- [x] Door 2 tests use a fake embedder and the real PostgreSQL fixture from ticket 09. The one-string
      embedder check against OpenRouter is run once and recorded.
- [x] A test proves the read-only role is refused a write.
- [x] Our tables are defined and queried with SQLAlchemy Core through the engine LangChain's store
      also uses; `sqlalchemy` is pinned exactly, with its x86_64 build checked.
- [x] The build runs on the ATT&CK pages alone; a test with one sample own document proves the own
      corpus needs no code change.
- [x] The first real build's time and cost are measured and recorded.
- [x] The core-boundary test covers the new modules.
- [x] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-10-27: Codex claimed T17 at the author's request using implement and tdd. Tests use the already agreed door 2 (build/open/read the knowledge base), with a fake embedder and real PostgreSQL. Review baseline: `6be34cc8d1b4649eaba4d4d34a41537b6c8e3e90`. T18 owns fingerprint recording and the startup guard.
- 2026-10-27: The author confirmed Astra is selected. Codex initially relied on the earlier ticket read and missed the subsequently added model-confirmation criterion; implementation paused when noticed and resumed after this explicit confirmation. The first four door-2 tests cover the build/read round trip, section limits, whole numbered steps, and ATT&CK cleaning/packing. The administrator created `li_reader` and saved its password in `.env`; no password was shared in chat.

## Answer

Resolved on 27 October 2026. Implementation, independent review and the final safety net pass.
The late model-confirmation process exception is preserved in Comments.

### Build and access

- Command from `backend/`: `uv run python -m scripts.build_knowledge_base`.
  Uses `LI_DATASET_DIR` or the default dataset, with optional `--dataset-dir`, `--state-file`
  and `--report`. `--check-embedder` performs the separate one-string provider check.
- Core entry points: `build_knowledge_base` loads an empty database, `rebuild_knowledge_base`
  creates a fresh one and publishes it, and `open_knowledge_base` exposes named read functions.
  The eight organisation tables, LangChain chunk table, GIN keyword index and mention table
  share one SQLAlchemy async engine through psycopg and `PGEngine.from_engine`.
- Local `.knowledge-base.json` names the successful database and dataset, contains no credentials,
  and is git-ignored. Publication is atomic. A failed new database is dropped. Previous successful
  databases remain for inspection, reported by name; automatic reclamation is AUD-057.
- The administrator ran `backend/setup/postgres-reader-setup.sql`. A separate reader engine
  authenticates as `li_reader`; tests prove reads succeed and writes, schema creation and temp
  table creation fail. Builder identity, privileged roles and role memberships are rejected as
  readers. The new embedding factory joins the session-wide no-real-keys test guard.
- T18 owns fingerprint recording and the application startup guard. No API or agent behaviour
  changed in T17.

### Chunking and identifiers

- Headings define sections, with actual heading depths and fenced code tracked. Ordinary current
  kinds target 350 body tokens with 40-token overlap within a section. Context headers are
  prepended afterwards and included in both embedding and keyword text. Numbered runbook steps
  and ATT&CK procedure examples are packed whole. An individually oversized example fails loudly.
- ATT&CK references, inline citation markers, link addresses and code tags are excluded from
  searchable text. Visible link labels remain; source files stay byte-identical. Independent
  literal expectations supplement the whole-corpus preservation checks.
- Chunk IDs are `<doc-slug>@<version>#<heading-slugs>/<ordinal>`, with ordinals starting at 1.
  The full heading ancestry is the path. Duplicate addresses fail before storage rather than
  allowing the library's upsert to replace evidence.
- Typed metadata: document type, technique ID, incident ID, version and effective date. Remaining
  source metadata and all mentioned technique IDs are JSON. The source technique is the scalar
  technique ID for ATT&CK techniques; otherwise a sole mentioned technique can occupy that field.
  Organisation mentions resolve literal IDs, usernames, display names, hostnames, group names,
  asset names and network labels/addresses to existing row IDs. Front-matter owners create no
  account links. Near-matches are rejected, and chunks without organisation mentions are valid.

### Measured evidence

- First real build: **40 documents, 320 chunks, 257 organisation mention links**, 1,536-dimensional
  vectors and a working GIN keyword index. **18.479 seconds total**, 55,681 embedding tokens in
  five requests, **$0.00111362** reported by OpenRouter. [Full report](../evidence/17-first-build-2026-10-27.json).
- One-string provider check: 1,536 dimensions, seven tokens, one request, **$0.00000014**,
  5.601 seconds. [Report](../evidence/17-embedder-check-2026-10-27.json).
- The reviewed parser reproduces the live build's 320 passage IDs and texts exactly without
  another paid embedding call. [Comparison](../evidence/17-parser-live-build-check-2026-10-27.json).
- PostgreSQL parser evidence is in the first-build report: `T1110.003` is a file token;
  `LT-DHUGHES` is indexed whole and in parts, with stemming; `203.0.113.10` is a version token;
  the email remains an email token. Exact entity lookup therefore uses stored IDs, not stemming.
- Pinned dependencies: `langchain-postgres==0.0.19`, `langchain-text-splitters==1.1.2`,
  `tiktoken==0.14.0`, `sqlalchemy==2.1.6`; existing `psycopg==3.3.6` stays pinned.
  SQLAlchemy's installed wheel is pure Python (`py3-none-any`), imported and exercised on x86_64.
- Two-axis review: two Standards findings and one Spec finding, all fixed and independently
  confirmed closed. [Review record](../reviews/17-code-review-2026-10-27.md).
- B-084 to B-088 retain the real failure/fix iterations. The process exception for the late model
  confirmation is recorded above, rather than represented as having happened before the start.


### Final safety net

- Final backend suite: **571 passed**, 265.79 seconds. An earlier full run passed 569 tests
  before the two review regression cases were added; the final run includes both.
- Frontend: **149 passed**, 41.76 seconds, run after the backend suite with one worker (B-066).
- Backend Pyright: **0 errors, 0 warnings**. Frontend TypeScript check: exit 0.
- Frontend lint: exit 0 with the same six existing warnings (AUD-009), untouched by T17.
- Port API eval: **63/63 overall, 15/15 security**; both gates pass. Q02 and Q04 each pass 3/3.
  Prompt version remains `b70d0745`. One passing Q02 response took 93.6 seconds.
  [Saved run](../../../backend/evals/results/2026-10-27-160038-b70d0745.json).
- Core-boundary and no-real-keys tests are included in the backend suite. Tests use fake
  embeddings; the separately recorded live build and probe are the only T17 embedding calls.
- Implementation commits: `d77b451`, followed by review corrections in `93fbd02`.
  This closure record and saved evaluation are committed separately. Nothing was pushed.
