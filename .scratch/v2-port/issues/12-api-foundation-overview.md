# 12: API foundation and the Overview endpoint

**What to build:** a FastAPI server that starts from configuration, loads the Dataset once, and
answers the dataset facts, the rules guide and the Overview for any filter. A tester can call the
three endpoints and get exactly the shapes in the contract, and a bad filter is refused without its
value being echoed.

**Blocked by:** 11 (Core: the logic that moved from the screens).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "The API". Contract: `docs/api-contract.md` (ground rules, base path and
configuration, shared filter parameters, dataset facts, overview, rules guide, errors).

- [ ] The API is a separate package beside the core; routes validate, call the core, shape the reply, and hold no analysis
- [ ] Configuration from environment variables as the contract lists them, with the contract's defaults
- [ ] At startup the log is loaded once, the rules run once on the whole log, the memory opened once and the agent built once, each in exactly one place; a missing model key does not stop the server
- [ ] `GET /api/dataset`, `GET /api/rules` and `GET /api/overview` return the contract's shapes and nothing more (no `sample`, no `truncated`)
- [ ] Shared filters validated at the boundary: bad date, `from` after `to`, bad outcome each give a 422 with the one error shape, naming the field and never the value
- [ ] One error shape for every status, replacing FastAPI's default; a dataset that fails validation at startup makes the dataset endpoints answer 500 `log_invalid`
- [ ] API tests with FastAPI's test client: shapes, empty view is not an error, validation, memory opened once and agent built once per process
- [ ] The core boundary test still passes
