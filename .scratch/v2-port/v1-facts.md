# v1 facts found while charting

Read from `../login-investigator` on 14 October 2026. v1 is frozen, so these facts stay true.

## Size and tests

- The core (`login_investigator/`) has no Streamlit import: confirmed by grep.
- The screens in `app/` total 764 lines, including `app/screens/` (four files, 491 lines).
- pytest collects 290 tests (212 `def test_` functions; 26 parametrised). Screen tests:
  `test_app.py` (13 functions) and `test_investigator_screen.py` (18).

## Users and investigations

- Single user, no login. v1 PRD "Out of scope" lists "Sign-in to the app itself, or multiple
  users".
- v1 calls a saved line of inquiry an **investigation** in code (`investigations.py`,
  `Investigation`, `thread_id`) and a **case** on screen. The thread id is a random uuid4 hex.
- A small `investigations` table (thread_id, started_at, first_question) sits in the same SQLite
  file as the `SqliteSaver` memory.
- `build_agent` says "the checkpointer, not the agent, holds the cases". One agent per server
  process is therefore enough in v2; memory is per thread id, not per agent.

## Agent

- Streaming already exists in the core: `agent.ask()` yields pieces of kind `text` or `tool` (a
  tool starting). v2 needs a transport for that stream, not a new design.
- The incident report is written by `write_report()` with structured output, and saved into the
  investigation. The PDF is built by the core (`report_pdf.build`), so v2 needs a download endpoint.
- The tool-calls panel text is written by the core (`tool_views.describe`), which returns a pandas
  table. The API must turn that table into JSON.
- The first lines of `agent.py` say the agent produces streamed answers and an incident report, and
  is shared by the Investigator screen and the evals.

## Logic in the screen layer

Logic that lives in `app/`, not the core, and is covered today only by the 31 screen tests:

- Date range to timestamps: the end date plus one day.
- Rules run on the whole log, then filtered to the visible rows (`findings_matching`).
- Alerts sorted newest first.
- Names cut to three, plus "and N more".
- Failed share on the Overview.
- Paging of past investigations.
- The "Open in Log explorer" jump from an alert.

## Proof

- **The eval runner and the core tests call the core directly** (`evals/run.py` imports
  `login_investigator.agent`). Copied unchanged, they pass in v2 even if the API or the screens are
  broken.

## Course rule

- v1 `CLAUDE.md` lines 32-35 and `docs/PRD.md` lines 79, 105, 322: LangChain only as taught in
  class, no custom LangGraph graphs.
