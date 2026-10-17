# Research: how the agent's tools get the same data as the dashboards

Ticket: [22-agent-tools-follow-settings](../issues/22-agent-tools-follow-settings.md). Researched 17 October
2026 against primary sources: the LangChain and LangGraph docs (docs.langchain.com,
reference.langchain.com), the FastAPI and Starlette docs, and the installed library source in
`backend/.venv/lib/python3.12/site-packages/` (langchain 1.3.1, langchain-core 1.4.0, langgraph 1.2.4,
fastapi 0.143.1, Python 3.12.14). Every claim about how the installed code behaves was also run in a
throwaway probe outside the repo. Nothing in the repo was changed.

## 1. The question and the constraints

**The question.** The API loads the log once at startup from `Settings.log_path`, runs the rules once,
and keeps both in `Services.dataset` (`backend/api/services.py`, `start`, lines 51-77). The agent's
three tools do not use that. They load their own copy through `@cache def _log(): return load_log()`
and `_all_findings()`, and call `lookup(ip)` with its default folder
(`backend/login_investigator/tools.py`, lines 27-36 and 141). With default settings both read the same
file. With `LI_LOG_PATH` or `LI_REPUTATION_DIR` set, the screens and the agent read different data and
nothing warns. What is the best way to give the tools the API's data, so they provably read the same
thing?

**The hard constraints** (from the task and the spec):

1. What the model sees must not change: each tool's name, description and arguments. The eval runner
   fingerprints exactly `[t.name, t.description, t.args]` (`backend/evals/run.py`, line 52).
2. The core package `login_investigator` must not import FastAPI (`backend/tests/test_core_boundary.py`)
   and should not know the API's setting names.
3. The copied v1 tests pass unchanged. `test_tools.py` calls each tool directly as
   `tool.invoke(args)` with a plain dict and no agent around it (`backend/tests/test_tools.py`, line 23).
   `test_agent.py` calls `build_agent(model, memory)` with two arguments (lines 66, 135, 160).
4. Build the seams, not the features: one place for the tool list; the model and agent made in one
   function each.

## 2. Findings per option

### What the libraries do with "hidden" tool parameters (applies to options C and E)

These facts decide most of the comparison, so they come first.

- **A tool's `args` hides injected parameters.** `BaseTool.args` is built from `tool_call_schema`,
  which drops every parameter whose type is marked as injected
  (`langchain_core/tools/base.py`, lines 567-609). The model's schema is built the same way. So an
  injected parameter does not change `t.args`. Probe: a copy of a tool with `runtime: ToolRuntime`
  added had `args == ['ip', 'limit']`, the same as without it.
- **Only a bare `ToolRuntime` counts as injected.** The check accepts `ToolRuntime` or
  `ToolRuntime[...]`, and `Annotated[..., InjectedToolArg]`. It does not accept `ToolRuntime | None`
  (`langchain_core/tools/base.py`, lines 1430-1475).
- **The docs agree the runtime parameter is hidden.** "At call time, ToolNode injects the value
  automatically; the parameter is not included in the tool schema sent to the model." Also, `config`
  and `runtime` are reserved parameter names, and older patterns (`InjectedState`, `InjectedStore`,
  `InjectedToolCallId`) should move to `ToolRuntime`.
  Source: https://docs.langchain.com/oss/python/langchain/tools ("Reserved argument names", "Access
  context", "Migrate from older injection patterns").
- **How the agent fills it.** For each tool call, the tool node builds a `ToolRuntime` whose `context`
  is the run's context (`langgraph/prebuilt/tool_node.py`, lines 793-826). It finds the parameter with
  `get_type_hints`, so it still works in a file that starts with `from __future__ import annotations`,
  as `tools.py` does (lines 1967-2030). A parameter named `runtime` is always treated as the runtime
  (lines 2003-2004).
- **A tool node runs one turn's tool calls in parallel threads** (`executor.map`,
  `langgraph/prebuilt/tool_node.py`, lines 821-824). So whatever data the tools read must be safe to
  read from several threads at once.

### Option A: a setter in the core, called once at startup

**What it is.** `tools.py` gains one function, for example
`use_dataset(frame, findings, reputation_dir)`. The API's `start()` calls it once, with the frame and
findings it already built and the folder from its settings. The tools read that data when it is set.
When nothing has been set (the v1 tests, the eval runner's direct mode), they fall back to today's
lazy load of the default file.

**Sketch.**

```python
# login_investigator/tools.py
@dataclass(frozen=True)
class _Data:
    frame: pd.DataFrame
    findings: tuple
    reputation_dir: Path

_given: _Data | None = None          # set once at startup by the API; None in v1 tests

def use_dataset(frame, findings, reputation_dir) -> None:
    global _given
    _given = _Data(frame, tuple(findings), Path(reputation_dir))   # one assignment: atomic swap

def forget_dataset() -> None:        # for the API's shutdown and for tests
    global _given
    _given = None

@cache
def _default_log():
    return load_log()

def _log():
    return _given.frame if _given else _default_log()
# _all_findings() and the folder passed to lookup(ip, saved_dir=...) follow the same pattern.

# api/services.py, in start(), after the dataset is built:
tools.use_dataset(frame, dataset.findings, settings.reputation_dir)
```

**Constraints.**
1. Names, descriptions and arguments: unchanged. The three tool functions keep their exact signatures
   and docstrings; only private helpers change.
2. Core independence: the core takes a frame, a list and a folder. It never sees a setting name or a
   FastAPI object.
3. v1 tests: unchanged and passing, through the fallback. `build_agent` keeps its signature.
   `test_api_startup.py` counts `loader.load_log` once per process (lines 43-52); the tools never
   call it in the API, so the count stays honest.
4. Seams: the tool list is still the one `TOOLS` tuple; `build_agent` is still the one factory.

**Same data, provably.** The tools hold the very object the dashboards use. A test can assert identity
(`tools._log() is services.dataset.frame`), which is stronger than "read the same file".

**Concurrency.** FastAPI runs the lifespan "before the application starts receiving requests"
(https://fastapi.tiangolo.com/advanced/events/), so the data is written once before any reader
exists, then only read. Swapping in one frozen object means a reader never sees half of an update.
The core only builds filter masks and new frames from the log; a search of `search.py` and `rules.py`
found no in-place writes. That pandas reads are thread-safe here is my inference from that, not a
pandas guarantee.

**Risks.** It is process-wide state, the thing LangChain's docs say runtime context exists to avoid
("Instead of hardcoding values or using global state, you can inject runtime dependencies",
https://docs.langchain.com/oss/python/langchain/runtime). Three concrete dangers:

- **Test leaks.** A test that starts the app with a temporary log would leave the tools pointing at it
  for every later test in the same run. Fix: the lifespan calls `forget_dataset()` after `yield`, and
  any test that sets data resets it with a fixture.
- **Two apps in one process:** the last one started wins. This does not happen today; it would matter
  only if tests ran two apps at the same time.
- **A failed log silently falls back.** If the configured log fails validation, `start()` builds no
  dataset (`services.py`, lines 58-65). Under a naive setter the tools would then quietly load the
  *default* file, which is exactly the bug this ticket closes. The design must say what the tools do
  then (see open question 1).

### Option B: the core reads the same environment variables

**What it is.** `tools.py` reads `LI_LOG_PATH` and `LI_REPUTATION_DIR` itself.

**Constraints.**
1. Names and arguments: unchanged.
2. Core independence: **fails the spirit.** The core would know the API's setting names, and two
   places would have to keep the names and defaults in step.
3. v1 tests: pass, since nothing is set during them.
4. Seams: weakened. Configuration would be read in two places.

**Same data, provably: no.** The tools would load a second copy, so "same data" would only mean "same
file at load time". Worse, the API does not always take its settings from the environment. The
startup tests build settings from a plain dict, `Settings.from_env({"LI_LOG_PATH": ...})`, without
touching the real environment (`backend/tests/test_api_startup.py`, lines 45, 70, 91). Under option B
the tools would read a different log from the dashboards in exactly those tests. It would also run the
rules twice per process, against the ticket-12 rule that each seam is called once.

**Official guidance.** None of the sources recommend it. Verdict: rejected.

### Option C: LangChain's runtime context (`context_schema`, `ToolRuntime`)

**What it is.** This is the mechanism the LangChain docs recommend. `create_agent(...,
context_schema=Context)` declares a context shape (`langchain/agents/factory.py`, lines 697-716 and
781). Each `agent.stream(..., context=Context(...))` passes it in, and a tool reads
`runtime.context`. The docs call this "dependency injection for your tools and middleware" and list
"db connections, or other dependencies" as typical content
(https://docs.langchain.com/oss/python/langchain/runtime,
https://docs.langchain.com/oss/python/concepts/context). Since LangGraph 0.6, this context replaces
the older habit of putting such values in `config["configurable"]`: "`config_schema` is deprecated in
v0.6.0 ... Please use `context_schema` instead"
(https://reference.langchain.com/python/langgraph/graph/state/StateGraph).

**Sketch.**

```python
@tool
def search_logins(user: str | None = None, ..., *, runtime: ToolRuntime[ToolData]) -> str:
    frame = runtime.context.frame if runtime.context else _default_log()
    ...
# agent.ask(...) would need a new argument to pass context=... into agent.stream
```

**What the probe found in the installed versions.**

| Form of the parameter | `t.args` / model schema | `tool.invoke({...})` with no agent, as `test_tools.py` does | Inside the agent with `context=` |
|---|---|---|---|
| `runtime: ToolRuntime` (required) | unchanged | **fails**: `ValidationError: runtime Field required` | context arrives |
| `runtime: ToolRuntime \| None = None` (optional) | **crashes**: `PydanticInvalidForJsonSchema` | works, context is `None` | context arrives |
| required, but the agent run without `context=` | unchanged | (as above) | `runtime.context` is `None` |

The context is not written into the checkpoint. After a run, neither the checkpoint (outside the
messages) nor its metadata held the context value.

**Constraints.**
1. Names and arguments: the required form keeps them. The optional form **breaks** `t.args`, so the
   eval fingerprint crashes and the model's tool schema cannot be built.
2. Core independence: fine. The context is a plain dataclass.
3. v1 tests: **fails.** The required form makes every direct `tool.invoke({...})` in `test_tools.py`
   raise. The only form that keeps the tests working is the one that breaks constraint 1. Getting
   round this would mean two copies of each tool, one for the tests and one for the agent. The tests
   would then no longer test what the agent runs.
4. Seams: `agent.ask` (core) and `write_report` would need a new context argument, and so would
   every caller (routes, eval runner).

**Also noticed.** `tools.py` starts with `from __future__ import annotations`. Because of it, the
helper that hides injected values from callbacks finds nothing to hide: `_injected_args_keys` is
empty in the probe. That helper reads the raw signature
(`langchain_core/tools/structured.py`, lines 254-263, used by `base.py`, lines 803-819). The runtime
object, with the whole conversation state, could then show up in tool-start callback inputs. This is
a likely tracing problem for the later tracing week. I inferred it from the source and did not test it
with a tracer.

**Verdict.** It is the officially recommended mechanism. In this codebase it cannot meet constraints 1
and 3 together. Worth revisiting only if the copied tests may ever change.

### Option D: a tool factory with closures, `make_tools(data)`

**What it is.** The three tools are defined inside a function that receives the data. The module-level
`TOOLS` is built by the same function from the lazy default. The API builds its own set and passes it
to `build_agent(model, checkpointer, tools=...)`, with a default so the tests' two-argument call still
works.

**Sketch.**

```python
def make_tools(data) -> tuple[BaseTool, ...]:
    @tool
    def search_logins(user: str | None = None, ...) -> str:
        """...same docstring..."""
        result = search_core(data.frame(), ...)
        ...
    return (find_suspicious_activity, search_logins, lookup_ip_reputation)

TOOLS = make_tools(_DefaultData())          # lazy default file, for v1 tests and the eval runner
find_suspicious_activity, search_logins, lookup_ip_reputation = TOOLS
```

**The surprise.** Moving a tool's function inside another function changes its description. `@tool`
takes the docstring and calls `textwrap.dedent` on it
(`langchain_core/tools/structured.py`, lines 212-238). The docstring's first line has no indent, so
dedent removes nothing, and every later line keeps its source indentation. The probe:

```
module level: 'Search by ip.\n\n    Args:\n        ip: An IP. ...'
in a factory: 'Search by ip.\n\n        Args:\n            ip: An IP. ...'
```

The real tools carry this indentation today: `lookup_ip_reputation.description` ends in
`'\n\n    Args:\n        ip: One IPv4 ...'`. So a plain factory changes the text the model reads
and the eval fingerprint, which breaks constraint 1. It can be worked around, for example by passing
each description explicitly. But that is one more clever step in a file the author reviews and does
not write.

**Constraints.**
1. Names and arguments: unchanged. Descriptions: **changed** unless worked around.
2. Core independence: fine.
3. v1 tests: pass if the module-level names stay and `build_agent` gets an optional third argument.
4. Seams: fine. `make_tools` is the one place the list is made.

**Same data, provably, and concurrency.** Best of all options. Each tool holds its data by
construction, with no shared state, no reset and no leak between tests.

**Cost.** Every line of the three tools moves into a function. The whole v1 file shows as changed in
a diff, in a file the spec keeps as close to v1 as possible until Parity.

**Verdict.** The cleanest pattern, but here it brings a hidden change to what the model reads and a
large diff. Second choice.

### Option E: `RunnableConfig` "configurable", or `InjectedToolArg`

**`config: RunnableConfig` parameter.** Probe: it is hidden from `t.args`. A direct
`tool.invoke({...})` works, with an empty config. Inside the agent, a value in
`{"configurable": {...}}` reaches the tool. So it passes constraints 1 and 3. Against it:

- The docs list `config` as reserved "for passing RunnableConfig to tools internally" and point to
  `ToolRuntime` instead (https://docs.langchain.com/oss/python/langchain/tools).
- LangGraph moved static run data from `configurable` to `context` in 0.6 (reference above).
- LangGraph copies every text, number or true/false value in `configurable` into the metadata of
  every checkpoint (`langgraph/checkpoint/base/__init__.py`, lines 757-775). A folder path passed as
  text would be written into the SQLite memory file at every step. A DataFrame or a `Path` would not
  be copied.
- Like option C, `agent.ask` and every caller would need to pass the value on each call.

**`Annotated[..., InjectedToolArg]` with a default.** Hidden from `t.args`, and direct calls work. But
inside the agent the probe got `None`: the tool node fills only state, store, runtime and the tool
call ID. A plain `InjectedToolArg` is a marker for code that calls tools by hand. It does not deliver
data by itself.

**Verdict.** It works, but it is the deprecated route. It also adds a per-call argument to the core
and puts text values in the memory file. Rejected.

### What FastAPI says about sharing startup-loaded resources

- The lifespan is the recommended place to load resources "shared among requests", with "loading a
  shared machine learning model" as the example. It runs once, before requests are taken
  (https://fastapi.tiangolo.com/advanced/events/). `create_app` already does this
  (`backend/api/app.py`, lines 21-25).
- `app.state` is "the same object for the entire application ... You normally wouldn't use this in
  FastAPI, for most of the cases you would instead use FastAPI dependencies"
  (https://fastapi.tiangolo.com/reference/fastapi/). Starlette also offers lifespan state: the lifespan
  yields a dict, and each request gets a shallow copy as `request.state`
  (https://starlette.dev/lifespan/).
- Dependencies (`Depends`) are solved by FastAPI "whenever a new request arrives", for path operations
  and their sub-dependencies (https://fastapi.tiangolo.com/tutorial/dependencies/). The FastAPI docs
  say nothing about code outside a request. The agent's tools run inside the agent's own worker
  threads, where FastAPI cannot inject anything.

The conclusion is mine, drawn from those three points. The data has to be handed over in our own
code: once at startup (A, D) or on every call (C, E). The current route side (lifespan, then
`app.state.services`, then a `Depends`) already follows FastAPI's guidance and does not need to change.

## 3. Comparison

| | Names, descriptions, args unchanged | Core free of the API and its setting names | v1 tests unchanged | Same data, provably | Concurrency | Matches official guidance |
|---|---|---|---|---|---|---|
| **A** setter at startup | Yes | Yes | Yes (fallback) | Yes, same object | Safe: written once before requests, then read only | Partly. FastAPI's lifespan, yes; LangChain advises against global state |
| **B** core reads env vars | Yes | No | Yes | No: a second copy, and wrong when settings come from a dict | Safe | No |
| **C** runtime context | Required form yes; optional form crashes `t.args` | Yes | No: required form breaks direct `invoke` | Yes, per call | Safe, per run | Yes, LangChain's recommended way |
| **D** tool factory | Args yes; **descriptions change** unless worked around | Yes | Yes, with an optional `build_agent` argument | Yes, by construction | Best: no shared state | Yes, plain dependency injection |
| **E** `configurable` / `InjectedToolArg` | Yes | Yes | Yes | `configurable` yes; `InjectedToolArg` delivers nothing | Safe | No: deprecated route since LangGraph 0.6 |

## 4. Recommendation

**Option A: one setter in the core, called once from `start()`, with the lazy default kept as the
fallback. Add three guards: reset at shutdown, an explicit answer for a failed log, and an identity
test.**

Why:

- It is the only option that meets all four hard constraints with no workaround. The three tool
  functions, their docstrings and their signatures stay as v1 wrote them. The diff touches only
  private helpers, so the copied tests and the eval fingerprint prove Parity as before.
- It gives the strongest "same data" proof. The agent's tools read the very frame and findings the
  dashboards read, and a test can check that with `is`.
- It keeps the seams the spec asks for. The API still asks the core for "a dataset". The core takes
  plain values and knows nothing of settings. The tool list and the agent factory stay single.
- The officially recommended mechanism (C) and the cleanest pattern (D) were both checked against the
  installed code, and each breaks a hard constraint here. C breaks the copied tests or the tool
  schema. D silently changes the text the model reads.

How to build it safely:

1. `use_dataset(frame, findings, reputation_dir)` stores one frozen object in a single assignment.
   `forget_dataset()` clears it.
2. The lifespan in `api/app.py` calls `forget_dataset()` after `yield`, so no test leaves data
   behind.
3. When the configured log fails validation, the tools must not fall back to the default file. They
   should return their usual short `error` result instead. This needs the author's ruling (open
   question 1).
4. Tests for the ticket's criteria. Start the app with `LI_LOG_PATH` set to a small temporary log, and
   check that `search_logins` reports that log's counts and that the tools' frame `is`
   `services.dataset.frame`. Start it with `LI_REPUTATION_DIR` set to a temporary folder holding one
   saved response, and check that `lookup_ip_reputation` answers `"source": "saved"` from it.

Risks of the recommendation:

- **It is global state.** The guards above limit it, but a future test that skips the reset could
  leak data into later tests. The test-order leak is the main thing a reviewer should look for.
- **One dataset per process.** If a later week wants several datasets side by side, for example the
  eval runner's API mode running against two logs at once, the setter stops being enough. The move
  then is option D with explicit descriptions, or option C if the copied tests may change by then.
  Both need a decisions-log row.
- **The silent fallback.** If step 3 is skipped, a bad log brings back exactly the bug this ticket
  closes.

## 5. Open questions for the author

1. **When the configured log fails validation, what should the agent do?** Options: (a) build the agent
   anyway, and the log tools return a short error such as "The log failed validation" while the IP
   lookup still works (recommended: a failure stays inside the part it belongs to, as with the missing
   model key); (b) do not build the agent, so the Investigation endpoints answer 503 as they do for a
   missing key; (c) fall back to the default file (not recommended: it is the bug).
2. **Should the reset at shutdown be required and tested?** Recommended yes. It is the guard against
   the test-order leak.
3. **Is the eval runner's direct mode staying on the default file?** It never sets a dataset, so it
   uses the fallback. Ticket 18's API mode would go through `start()` and follow the settings. Worth
   one line in ticket 18.
4. **Noticed, out of scope.** The tool descriptions carry the docstrings' source indentation. Python
   3.13 strips that indentation when it compiles a docstring
   (https://docs.python.org/3/whatsnew/3.13.html, "Other Language Changes"; I did not test this). So a
   move to Python 3.13 would change the text the model reads and the eval fingerprint, with no code
   change. The project pins `>=3.12` and runs 3.12.14 today. Possibly a ticket: pin the minor version,
   or record that a Python upgrade needs a new eval run.
5. **Noticed, out of scope.** If the tools ever take a `ToolRuntime`, the `from __future__ import
   annotations` line in `tools.py` stops LangChain hiding that object from callback inputs (option C,
   "Also noticed"). Relevant to the tracing week.
