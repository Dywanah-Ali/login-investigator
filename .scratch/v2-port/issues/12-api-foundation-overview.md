# 12: API foundation and the Overview endpoint

**What to build:** a FastAPI server that starts from configuration, loads the Dataset once, and
answers the dataset facts, the rules guide and the Overview for any filter. A tester can call the
three endpoints and get exactly the shapes in the contract, and a bad filter is refused without its
value being echoed.

**Blocked by:** 11 (Core: the logic that moved from the screens).

**Status:** resolved

Spec: [spec.md](../spec.md), "The API". Contract: `docs/api-contract.md` (ground rules, base path and
configuration, shared filter parameters, dataset facts, overview, rules guide, errors).

- [x] The API is a separate package beside the core; routes validate, call the core, shape the reply, and hold no analysis
  - Evidence: `backend/api/` (`app.py`, `settings.py`, `services.py`, `filters.py`, `errors.py`, `dashboard_routes.py`). `git diff main -- backend/login_investigator` is empty. Each route calls core functions (`summarize`, `hourly_counts`, `top_failed_ips`, `alerts_for_view`, `RULE_GUIDE`) and only picks and formats fields
- [x] Configuration from environment variables as the contract lists them, with the contract's defaults
  - Evidence: `api/settings.py` reads `LI_LOG_PATH`, `LI_MEMORY_PATH`, `LI_REPUTATION_DIR`, defaulting to the core's own paths; the keys stay with the core, as in v1; the port is uvicorn's `--port`. Two tests in `test_api_startup.py`. Gap: `LI_REPUTATION_DIR` and `LI_LOG_PATH` do not reach the agent's tools (comments)
- [x] At startup the log is loaded once, the rules run once on the whole log, the memory opened once and the agent built once, each in exactly one place; a missing model key does not stop the server
  - Evidence: `api/services.py`, `start`. `test_each_seam_is_called_once_per_process` counts all five seams at exactly 1 over five requests; `test_a_missing_model_key_leaves_the_dashboards_working`. A real uvicorn run with no key logged "The agent is unavailable" and served all three endpoints
- [x] `GET /api/dataset`, `GET /api/rules` and `GET /api/overview` return the contract's shapes and nothing more (no `sample`, no `truncated`)
  - Evidence: `test_api_dashboard.py` asserts each reply's exact field set; the Overview summary has eight fields, without `sample`, `sample_shown` or `truncated`. Top failed IPs pinned to S1 (150 failures, 1 account) and S2 (88, 35) from the ground truth
- [x] Shared filters validated at the boundary: bad date, `from` after `to`, bad outcome each give a 422 with the one error shape, naming the field and never the value
  - Evidence: `test_a_bad_filter_is_refused_naming_the_field_never_the_value`, 8 cases, each asserting a hostile or wrong value is absent from the reply. Dates must be exactly `YYYY-MM-DD` (bug log B-002)
- [x] One error shape for every status, replacing FastAPI's default; a dataset that fails validation at startup makes the dataset endpoints answer 500 `log_invalid`
  - Evidence: `api/errors.py`; `test_api_errors.py` (404, 405, 500 with the exception text hidden); `test_a_log_that_fails_validation_makes_the_dataset_endpoints_answer_log_invalid`; `test_a_missing_log_file_does_not_reveal_where_the_server_looked` (B-003). Three codes not in the contract's table: comments
- [x] API tests with FastAPI's test client: shapes, empty view is not an error, validation, memory opened once and agent built once per process
  - Evidence: 27 API tests in three files, all passing. Replays of v1's screen tests: "overview counts match the core", "a filter change updates every screen consistently", "an empty filter shows a clear message", "reset restores the whole log"
- [x] The core boundary test still passes
  - Evidence: `test_core_boundary.py`, 4 passed. Full suite 14 Oct: 294 passed (267 before, 27 new). Pyright: 0 errors, with `api` checked in full

## Comments

2026-10-14: build done on branch `ticket-12-api-foundation`, test-first, six slices, at the two seams
the author approved (the HTTP API, and startup seen from outside). Two-axis review run (standards and
spec). Fixed from it: lenient date parsing (B-002), the server path in a missing-file message
(B-003), the reset replay test added, the agent's build no longer hidden by the missing-key catch,
two unclear names. Status `ready-for-human` until the author reviews.

Open for the author's ruling:

1. **Three error codes the contract's table lacks.** `method_not_allowed` (405), `internal_error`
   (500, unexpected failure) and `http_error` (any other framework status). `not_found` is also used
   for an unknown path, not only an unknown investigation. Proposed: add them to the contract's
   Errors table, with a decisions log row.
   **Ruling 2026-10-14: added to the contract.** Errors table and spec decisions log updated.
2. **The missing-file message.** The contract says `log_invalid` carries the loader's message. For a
   missing file the API now sends fixed text instead (B-003). Proposed: note this in the contract.
   **Ruling 2026-10-14: noted in the contract.** Errors table and spec decisions log updated.
3. **An empty date box.** An empty `user=` or `country=` means "all", but an empty `from=` is a 422.
   The frontend (ticket 13) can omit empty parameters, or the API can treat empty as "all" for every
   filter. Proposed: treat empty as "all" everywhere, as the contract's "missing means all".
   **Ruling 2026-10-14: empty means "all" for every filter.** Built test-first
   (`test_an_empty_box_means_all_as_a_missing_one_does`); every filter is now checked in
   `api/filters.py`. Contract and spec decisions log updated. Full suite 294 passed.
4. **The agent's tools ignore `LI_LOG_PATH` and `LI_REPUTATION_DIR`.** They read the core's default
   log and reputation folder through `tools.py`. Dashboards and agent could then read different
   logs. Wiring it changes a core file, which the spec keeps unchanged until Parity. Matters for
   ticket 16 and the eval runner's API mode (ticket 18), which sets only `LI_MEMORY_PATH`.
   **Ruling 2026-10-14: a new ticket, done before ticket 18.** Ticket 22 created; ticket 18 is now
   blocked by it. The note in `api/settings.py` points to ticket 22, which removes it.

2026-10-14: the author approved ("approved"). Status set to `resolved`. Merged into `main` locally;
nothing pushed. Follow-up: ticket 22 (the agent's tools follow the configured paths), before 18.
