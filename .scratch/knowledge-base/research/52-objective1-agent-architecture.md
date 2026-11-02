# T52: One investigator or an orchestrator with specialists?

Date: 2 November 2026. Researcher: Codex, Astra.
Status: research and design candidates; no architecture, scope or evaluation-policy approval.

## Finding

The proposed analyst-facing orchestrator has a direct security-investigation analogue. It is a
credible candidate, not an automatic consequence of having six workflow steps. The strongest
reason for additional reasoning agents is a distinct judgement task, independent challenge,
or genuinely different tools/context. Counting logins and traversing known permission paths
remain code responsibilities under P-01.

Recommendation: keep one analyst-facing investigator in either design. Compare the existing
code-enforced evidence workflow plus one reasoning agent with a bounded specialist variant.
Do not assign one agent to each case-file section merely for symmetry. A document-applicability
specialist or an independent evidence challenger is more promising than a counting agent.
This is a proposed evaluation direction, not permission to build a prototype.

## Sources and what they establish

Discovery: web search in the research agent; parent Perplexity discovery supplemented it.
The six primary sources below were opened and inspected. No vendor system was executed and
no benchmark was reproduced. This review inspected documented architectures, not source code.

| Source | Established pattern | Limit for our decision |
|---|---|---|
| [Google Cloud SOC reference architecture](https://docs.cloud.google.com/architecture/agentic-ai-orchestrate-security-ops-workflows) | A root coordinator receives analyst requests, delegates to a Tier 1 analyst and threat-intelligence researcher, checks structured findings, and returns a report. It uses shared artifacts, runbooks and an iteration exit condition. | This is the closest interface analogue. It spans multiple security systems and provides architecture/sample guidance, not a controlled comparison proving superiority for login investigation. |
| [Microsoft DTDA architecture paper](https://arxiv.org/html/2605.20896v1), sections 3–5 | Builds an evidence timeline before bounded planner/executor investigation. LLM stages use explicit schemas, grounding requirements and deterministic validation. | Strong implementation description, but broad incident gap discovery differs from our analyst-led login objective. Its planner is not proof that every collection step needs an agent. |
| [AIDA alert-triage research](https://arxiv.org/html/2610.10608v1), sections V–VII | Separates a proposed assessment, independent challenge and adjudication over an append-only evidence ledger. Its Executor explicitly contains no LLM. The authors report improved triage on their benchmark. | Promising evidence for separating reasoning roles. Results remain within one dataset family; a documented miss occurs when all roles receive incomplete evidence. Analyst usability remains future work. Its automated Judge is not our analyst-owned verdict or existing advisory evaluation judge. |
| [AWS investigative-agent guide](https://docs.aws.amazon.com/security-ir/latest/userguide/ai-investigative-agent.html) | Describes contextual questions, read-only evidence gathering, cross-service correlation, a timeline, summaries and auditability. | A useful workflow reference. The singular product name does not establish the number of internal agents. No single-versus-multiple-agent comparison is disclosed. |
| [Azure orchestration guidance](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) | Advises choosing complexity according to need; specialization can reduce prompt/tool overload, while orchestration adds latency, costs and failure modes. Calls for output validation and testing of agents plus the whole system. | General architecture guidance rather than evidence from our domain/data. |
| [Anthropic multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) | Independent contexts and parallel exploration help broad research. Reports substantial token consumption and discusses delegation, compression and coordination problems. | Engineering experience outside security; neither its quality improvement nor its token multiplier transfers to our app. |

## Fair comparison for objective 1

The following is our assessment derived from those sources and the agreed local requirements.

| Candidate | How it would work | Potential benefit | Main concern |
|---|---|---|---|
| A. Code-enforced workflow plus one reasoning agent | Core functions gather the bounded case file. One analyst-facing agent interprets the complete evidence and requests approved follow-ups. | Facts and coverage have one enforcement path. The analyst gets an integrated explanation. | One reasoning context may overlook competing evidence or struggle with a large, mixed package. |
| B. Orchestrator plus bounded specialists | The front agent delegates defined reasoning questions over the same case file. Specialists return cited findings and limitations; the front agent reconciles them. | Focused instructions, narrower tools, independent examination and separate context budgets. | Handoffs can omit evidence, duplicate work or propagate unsupported conclusions. More roles do not create missing evidence. |
| C. Bounded planner/executor | A planner chooses follow-up questions; typed code executes allowed queries within enforced limits. | Useful if investigation paths genuinely depend on intermediate discoveries. | More autonomy than the current fixed-playbook design; requires explicit policy decisions, stopping conditions and evidence of benefit. |

All three can run independent data queries concurrently. Parallel tool execution alone does not
require multiple reasoning agents. Conversely, a specialist can be worthwhile without running
concurrently if its isolated judgement addresses a measured weakness.

## A credible specialist variant to evaluate

Keep exact selection, arithmetic, query execution and access-path construction in core code.
Potential specialist responsibilities are:

- **Evidence applicability:** assess whether a retrieved approval or exception actually explains
  the account, device, event and period under investigation. Return supporting passages,
  conflicts and applicability limits rather than a bare benign/malicious label.
- **Independent challenge:** inspect a proposed assessment against the source evidence for
  overlooked alternatives, unjustified dismissal, missing data and potential-reach overclaims.
  A separate context can test the explanation without inheriting its full reasoning history.
- **Front investigator:** remain the analyst's contact, explain evidence-backed agreements and
  unresolved disagreements, and propose any additional history for analyst approval.

These are candidate roles, not a recommendation to adopt all three. They should not become a
majority vote. An unresolved contradiction must remain visible; the front agent must be able
to inspect underlying records and passages instead of trusting specialist prose alone.

## Requirements common to either architecture

These are implementation proposals to review, not newly approved requirements:

1. Use one versioned case file with source identifiers, requested/effective coverage, statuses
   and omissions. Keep factual records distinct from model interpretations. Preserve revisions.
2. Give each reasoning task a defined input/output contract: task, permitted evidence, claims,
   citations, counterevidence and unresolved gaps. Validate structure and source references.
3. Enforce window, entity and query limits in code. No specialist or orchestrator may bypass
   analyst-controlled expansion. Record approval scope so resumed work respects it.
4. Treat logs, passages and specialist outputs as untrusted evidence at every receiving boundary.
   Delegation must not promote injected text into instructions. Restrict tools by role and
   test malicious content travelling through handoffs as well as direct tool responses.
5. Bound retries and reasoning rounds; preserve failed or incomplete tasks and end with an
   appropriately limited assessment. Shared mutable state needs controlled writes, not
   competing agents silently overwriting findings.

These proposals extend existing project principles. They do not require a new hosting service,
agent framework, identity platform, MCP connection or data source.

## How to choose without guessing

Use the same agreed cases, evidence access and outcome rubric across candidates. Include benign
twins, inapplicable clearing documents, empty searches, failed checks, conflicting passages,
missing history, malicious retrieved text and unsupported compromise/access premises. Measure
critical-evidence coverage, claim support, correct uncertainty, false reassurance, scope adherence,
saved evidence fidelity, elapsed time, token cost and failure/retry frequency. Run repeated trials.

Control for model choice and extra compute: distinguish an improvement from independent roles
from an improvement obtained merely by giving a system more calls or tokens. Test components and
the final answer; a specialist's correct finding can still be lost in synthesis. No thresholds
are set by this research, and the existing advisory judge retains its agreed role.

Prefer A if it meets agreed quality requirements with predictable coverage. Prefer a bounded B
if it reliably repairs consequential errors, contains prompt/tool complexity or improves evidence
handling enough to justify coordination costs. Consider C only if fixed collection demonstrably
misses necessary adaptive inquiries within the approved scope. None has yet been measured here.

## Next decision

Discuss which specific judgement deserves a separate context, then authorize the smallest fair
comparison if useful. Reconcile any selected architecture with T05, T26, T28, T30 and the spec
before implementation. The user's proposal remains open and supported as a credible candidate.
