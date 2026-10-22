# 05: How the knowledge base reaches the agent

Type: research, then grilling (retyped 22 October 2026; see the first comment)
Status: claimed
Blocked by: 02, 04

## Question

Which new read-only tools does the investigator agent get, what does each return, and how do
they fit the Port's seams (tool list from one place, model and agent created in one function,
data access in the core)?

## Scope

- Candidate tools: look up an account's context (owner, privilege, groups, reachable assets with
  criticality and owners); find who shares a device or source network; search the corpus with
  citations; expand a spray alert into its targets. Decide how many tools, and whether graph
  traversal and text search are separate tools or one.
- Return shapes: what the agent sees, what it must cite, and the rule that an ATT&CK mapping is
  "consistent with" until evidence supports more.
- Whether the four detection rules change at all (expected: no), and whether the Alerts API
  gains a context field or the agent alone carries the explanation.
- Injection stance: graph and corpus content is untrusted data, like log fields. How the system
  prompt and the tool outputs say so.

## Acceptance

- [ ] Tool list, inputs and return shapes decided.
- [ ] Seam placement decided: where tools live, how they get the store.
- [ ] Untrusted-data rule written for graph and corpus content.
- [ ] Decision recorded here under `## Answer`.

## Comments

### 22 October 2026: objective and the playbook stance (author and Claude, before research)

The author asked for this ticket to be taken slowly, as the most important one of the
initiative, and for a research note to ground the grilling. The ticket is therefore retyped
from `grilling` to `research, then grilling`, in three stages: an objectives talk in plain
English (this comment), a research note at `../research/05-agent-tools.md`, then the grilling
one question at a time.

**The purpose of the agent, agreed as the starting point of everything.** The agent exists to
turn a flagged login into an explained, evidence-backed answer to three questions: what
happened, who and what it can reach, and whether it is actually a threat. The author accepts all
three parts and rules that **"explained" is the core**. The word stays open-ended on purpose;
what the ticket shapes is how the agent gets there.

**The playbook stance (author's ruling).** The agent follows a pre-planned investigation for a
flagged login. That plan is its main objective. It may divert a little, or take a shortcut, when
the user's question does not need the whole plan. The Port already holds this shape in
miniature: `backend/login_investigator/investigation_policy.py` is a `before_model` middleware
that refuses to let the agent answer about findings until every attacker address in those
findings has been searched in the log, and steps aside when the question names one attack type
or one address.

**The principle.** The plan lives in code, not only in the prompt. A prompt says "investigate
thoroughly"; code says "you may not answer until these steps have run". Only the second can be
tested and put in the eval.

**The playbook as a first sketch, to be refined by research and grilling.**

| Step | Question the step answers | Tool it needs |
|---|---|---|
| 1 | What happened in the log | The Port's existing tools |
| 2 | Whose account, what privilege, which groups | Account context |
| 3 | What it can reach, and how sensitive that is | Reachable assets |
| 4 | Who else shares its device or network | Peers |
| 5 | Is there a document that explains it away | Corpus search for the "cleared by" document |
| 6 | Is there a document that makes it worse | Corpus search for policy, exception register, ATT&CK |
| 7 | Say it, cite it, or say you cannot tell | Refusal verdict from ticket 03 |

Steps 5 and 6 separate an explained alert from a flagged row. Step 7 is where ticket 03's three
verdicts apply.

**Consequences for this ticket.**

1. Each tool is justified by the step it serves. No step, no tool.
2. The plan needs a defined shortcut rule, like the Port's narrow-question test, so that a
   question such as "who owns this device" does not run every step.
3. Ticket 06 can test the plan itself: did the agent run the steps a flagged login requires, not
   only was the final answer right.

**Caution carried into the design.** The plan is a floor, not a ceiling. The Port's policy adds
missing steps and never removes the agent's own; that stance is kept, so the agent can follow a
lead it finds mid-plan.

**Entry point (author's ruling, same discussion).** The explained alert is something the user
asks for in chat, never something the app produces unasked. The app flags, the user hires, the
agent investigates; "investigator" is the name on the door. This keeps the MVP scale.
Consequences: the chat question is the only trigger of the playbook; the shortcut rule is a
classification of the question (full investigation versus narrow lookup), which must be sturdier
than the Port's text test once more tool types exist; ticket 07's screen is the chat with
citations shown well, not a per-alert panel; nothing runs, and nothing is spent, unless asked.
Noted for ticket 07, not decided: an "investigate" button on an alert row that drops a
pre-written question into the chat, so the account, address and rule name reach the agent
exactly rather than guessed from prose.

**Shape of the answer (author's ruling, same discussion).** Conversation first, then report, as
the Port already does. The user steers with questions and gets short answers; the report at the
end is built from what the conversation found. The playbook therefore guarantees the required
steps have run **before the report is written**, not before every chat answer. A chat answer may
be partial; a report may not. Where the Port's policy gates the model on every turn, the new
plan has two gates: a light one per turn (answer only what the tools returned, cite or refuse)
and a full one at report time (every playbook step for the investigated alert has run, or the
report says which step could not be completed and why).

**Who walks the graph (author's ruling, same discussion).** Code walks, the agent reads. For
phase 1's fixed questions (groups, reachable assets with sensitivity and owner, peers by device
and network) one core function computes the radius in NetworkX and returns it already joined;
the agent explains what came back and cannot get the radius wrong, only describe it badly. The
same function is what ticket 04's `truth.json` test recomputes, so tool and answer key share one
implementation. The hop-by-hop walk (raw neighbours, the agent chains calls) is kept as a seam
for phase 4's attack paths, not built now.

**Who writes the corpus search (author's ruling, same discussion).** Both, with a clear split.
The playbook step uses a code-derived search: the tool takes an alert, not a query, and code
builds the clearing search (step 5) and the aggravating search (step 6) from the alert's record
(account, department, rule, dates, device) and returns both lists with their ticket 03
verdicts. A free `search_corpus` with typed filters stays for follow-up questions. The author
noted that a code-derived query is "a pre-defined user query" with full control; that control
is what makes it testable, since ticket 06 can run the recipe on every alert in the answer key
with no model in the loop.

**How code-derived queries are triggered without reading the chat (author's question, same
discussion).** The code never reads the chat, and keyword matching is ruled out as unreliable.
The model translates prose into a typed tool call; the code acts only on the typed call. The
user types anything; the model decides whether to call `investigate_alert` and with which
alert, or a narrow tool, or none (tool selection, the job the agent already does in the Port);
the code receives a typed alert identifier, looks up the record in the core and derives the
searches from the record; the model explains what came back. The Port's policy already follows
this rule ("log text never sets policy": it inspects tool calls and tool results).

**Candidate decision for the grilling: a stable finding identifier.** Today a `Finding` in
`rules.py` carries a rule, a summary, addresses, users, counts and evidence, but no ID. Without
one the model must describe an alert by its parts, which is where misnaming creeps in. Giving
every finding a stable identifier, computed from its rule and content so the same log always
yields the same IDs, lets the model call `investigate_alert("F-0006")` and lets ticket 07's
investigate button pass the ID with no prose at all. This touches the Port's core and its
Alerts API shape, so it is a grilling question, not a ruling yet.

**Research questions for the note.**

1. How agents consume a graph plus text in practice: few typed tools, one router tool, or a
   sub-agent; what Neo4j GraphRAG, LangChain and LangGraph agents actually ship.
2. Return shapes that make citation checkable: record IDs and chunk IDs the answer layer of the
   eval can verify.
3. Prompt injection through tool outputs: current guidance on wrapping retrieved text as data,
   and what has been shown to fail. Parked here from the discussion (author, 22 October 2026):
   whether a system-prompt sentence suffices or every tool result is also fenced and labelled
   with its source; the corpus is not hostile today but the design assumes it may be.
4. Cost and efficiency: tool calls per question, token budgets, keeping gpt-4o-mini within a
   sensible number of calls. Parked here from the discussion (author, 22 October 2026):
   whether `investigate_alert` bundles playbook steps 2 to 6 into one call returning one joined
   package (cheaper, deterministic) or the steps stay separate calls the policy enforces (the
   user watches the investigation unfold, as the Port streams tool calls today, and can ask
   mid-way); what the sources say about granularity of tools for small models.
5. Plan-driven agents in LangGraph: where the plan lives (middleware, graph nodes, prompt), how
   the shortcut rule is expressed, and how the design keeps room for phases 2 to 4 and the GRC
   view without building them.
