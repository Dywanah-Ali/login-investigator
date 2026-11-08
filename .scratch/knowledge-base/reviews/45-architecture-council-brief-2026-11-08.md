# T45 architecture council brief

8 November 2026. Single pre-implementation review explicitly agreed by the author.

## Shared brief

Login Investigator v2 is a local FastAPI/React login-investigation application with plain Python
core, PostgreSQL passage search, Neo4j graph references, and LangChain 1.3.1/LangGraph 1.2.4
with SQLite checkpointing. T45 designs an approved chat/research split: chat constructs bounded
assignments and interprets evidence; research alone receives investigative retrieval tools;
code owns identity/scope/facts/required checks and validates/assembles results; the analyst owns
the verdict. The author approved a thin explicit LangGraph parent workflow, isolated
per-invocation create_agent research workers, persistent parent conversation and normal chat
clarification. No Deep Agents, extra supervisor or new service. Requests/results have stable
code IDs and per-task/subject accounting. Retrieval combines up to 20 corpus plus 20 additional
unique graph candidates before common ranking, keeps five passages per search without a second
combined five cap, and preserves source identity, important conditions and competing evidence.
Oversized passages may be temporarily split for scoring, reunited as one parent result and
delivered with original content. Review this design for material failure modes and useful
simplification before implementation. It affects future investigator behaviour and saved
cases, not a current production rollout. Code, inference, data writes, deployment and dependency
changes are out of scope. Existing requirements/gold/gates stand. Numeric limits and routine
failure details are delegated implementation work, not grounds for another approval tour.

## Authority and inspection

- Read `docs/investigator-contract.md` and `PRINCIPLES.md` for the inherited requirements.
- `.scratch/knowledge-base/issues/45-compound-question-retrieval-design.md`: current consolidated
  request, response, planned capability interfaces, latest approved execution policies and
  orchestration section. Historical drafts/next steps are not current requirements.
- `.scratch/knowledge-base/research/45-langgraph-orchestration-2026-11-08.md`: evidence,
  recommendation now approved, limitations and current-code integration findings.
- `.scratch/knowledge-base/spec.md`: approved scope and code-built full-investigation package.
  Earlier tool/middleware wording still needs final reconciliation; distinguish an unresolved
  ownership decision from a demonstrated contradictory implementation.
- Read source narrowly if needed: `backend/login_investigator/agent.py`,
  `backend/api/investigation_routes.py`, and shared core. No secrets or private memory files.

## Review boundaries

Return 3–5 sharpest points, one-line stance, one most important message and a 1–10 dimension
score. Label facts, inferred risks and unknowns. Identify P0/P1 blockers only when the design
itself creates a material failure; put lower observations in a ledger. Do not demand production
infrastructure, exhaustive testing, mutation suites or numeric cap approvals for this planning
ticket. Name the cheapest focused check for the principal risk, as a proposal for the existing
build/evaluation owners, not a paid experiment or new gate to run now.

Known unfinished T45 work: exact full-procedure task/search mapping and T25/T26 ownership;
prompt examples; E06 guidance-source selection; original retrieval-gate/keyword dispositions;
numeric budgets, source adapters and runtime compatibility. These must retain explicit owners
before implementation/acceptance. Do not claim they are done, automatically fatal, or waived.

Reviewers are independent and read-only. Only the Researcher uses web primary sources;
Logician uses no web. No reviewer edits files, starts services or runs inference. The parent
verifies findings and delivers one Judge verdict. No further review round without the author.
