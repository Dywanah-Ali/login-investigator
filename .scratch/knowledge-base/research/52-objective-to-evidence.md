# T52: Phase 0/1 objective-to-evidence table

Date: 2 November 2026. Status: all ten mapping rows approved; T52 decision review resolved after downstream reconciliation.
Prepared by Codex. Exact active model variant is not independently exposed in this session;
prior sessions' Astra confirmations are not asserted as this session's identity.

## Definitive scope ruling — 2 November 2026

The author confirmed reliable login investigation as the sole phase-0/1 product objective.
Bounded impact context remains. Standalone full inventory, exhaustive permission-path
presentation and reverse exposure are deferred. This supersedes the earlier E04 full-inventory
approval; E01–E10 are supporting requirements for one objective, not ten product objectives.
Prior review history remains below. No code deletion or gold/threshold change is authorised.

## Author review progress

- 2 November 2026: E01 accepted as the mapping of existing activity-explanation requirements.
  No runtime acceptance or scope change. See T52's dated review record.
- 2 November 2026: E02 accepted as the mapping of existing account-context requirements.
  Potential access, observed activity and behavioural normality remain distinct.
- 2 November 2026: E03 accepted as the mapping of existing assessment requirements.
  Applicability, competing evidence and analyst authority remain explicit; retrieval gaps stay open.
- 2 November 2026: E04 initially accepted as full potential blast radius. Superseded by
  the subsequent sole-objective ruling: retain bounded potential-impact context only.
- 2 November 2026: E05 accepted. Source-linked activity and involved-device peers are
  investigative leads, not proof of compromise. Removed shared-address context stays removed.
- 2 November 2026: E06 approved with limited controlled test cases and case-specific
  next-investigation guidance grounded in approved practice. No obligation to add every
  missing evidence source; broader response planning/automated containment deferred.
- 2 November 2026: E07 approved. Required checks are tracked in code; failures and their
  impact remain explicit, narrow lookups stay narrow and history expansion needs analyst approval.
- 2 November 2026: E08 approved. Preserve original evidence with saved answers; resolving
  a reference does not establish claim support. Full-package/display proof remains pending.
- 2 November 2026: E09 approved. Evidence cannot issue instructions; read-only tools and
  plain-text presentation remain required. Future paths still need their own security proof.
- 2 November 2026: E10 approved. Separate stage checks and complete application proof,
  with versioned evidence and retained failures. All ten rows are now reviewed and approved.

## Reading the table

A capability is proved only as far as its evidence reaches. A graph result does not prove
that the agent used it, and a valid citation does not prove that it supports the claim.

This maps the [spec](../spec.md), [principles](../../../PRINCIPLES.md) and latest
[T52 rulings](../issues/52-agent-objectives-and-reliability-review.md). The original purpose
covers what happened, potential reach and threat assessment. Phase 1 also retains spread and
shared ground in the earlier baseline. The definitive T52 ruling now narrows that scope to
login investigation with bounded impact and directly connected activity context.
The row IDs below are traceability labels, not newly approved objective numbering.

**Intended** means a written requirement. **Implemented** means source exists at the named
boundary. **Tested** means a recorded test result, with its scope and age retained.
**Demonstrated** means a saved execution or recorded author observation proves the named
behaviour. None of these implies that the whole objective passed. Source and historical
artifacts were inspected here; no fresh runtime test, service access or paid call was made.

## Analyst outcomes and required behaviour

| ID / analyst question | Required data | Core/tool responsibility | Expected analyst-facing answer |
|---|---|---|---|
| E01 Explain the activity: what happened around this login or alert? | Triggering rows; surrounding failures/successes and source/device changes; finding identity; requested window and available coverage. | Code resolves the finding, selects records and computes counts/timeline. Apply approved alert-relative ±24-hour bounds or single-event ±24 hours. Distinguish actual coverage from requested scope. | Accurate sequence and outcomes, bounded to the evidence. Missing later records never mean no later activity. No guessed replacement for an invalid finding. |
| E02 Explain account significance: whose account is this and why does its context matter? | Owner/department; evidenced role; privileged groups; sensitive asset metadata and permission paths. | Reuse account lookup and permission walks. Select relevant privilege/sensitivity facts for objective 1; mark unavailable role data explicitly. Permissions are a snapshot. | Relevant impact context with supporting records. A role is not a behavioural baseline; membership is not evidence that a resource was accessed. |
| E03 Explain the risk: what explanation best fits, and what weakens it? | E01/E02 facts; clearing/aggravating passages with person, dates and applicability; competing explanations. | Retrieve both supporting and counterevidence; preserve it through candidate fusion, ranking and package caps. Model interprets those facts under P-01/P-02. | Most supported explanation, competing evidence and unresolved questions. A travel approval can explain location without explaining separate attack activity. Analyst retains the verdict. |
| E04 Explain bounded potential impact within the login investigation. | Relevant privileged memberships, sensitive assets, supporting permission paths and snapshot basis. | Reuse deterministic graph facts; select impact context relevant to the login assessment or next action under E02. Standalone full inventory and exhaustive path presentation are deferred. | Explain consequential potential access with checkable paths and explicit limits. Never infer observed asset access or lateral movement. |
| E05 Show spread/shared ground: which directly connected activity deserves investigation? | Same-source login activity, involved devices and time-bounded device-use records for peers. | Log source pivots remain available; device relationships use evidence in the agreed window. For objective 1, select involved suspicious devices. Do not restore removed address-sharing edges/context. | What other accounts the source targeted and which accounts share relevant devices, with dates and limits. A connection is a lead, not common control or compromise. |
| E06 State uncertainty: what is missing, and what should be checked next? | Search verdicts, absent topics, weak/conflicting evidence, coverage, errors and truncation. | Preserve empty, unavailable, failed and omitted outcomes separately. Propose a reasoned history expansion and await analyst choice before collecting it. | Cannot-tell/absent-evidence explanations tied to actual limits. S4 remains unresolved. No false reassurance or invented policy/incident history. |
| E07 Complete the requested investigation without silently widening it. | Finding, user request, required-step state, tool results/errors and scope decisions. | Fixed code playbook; narrow lookups stay narrow; report gate records required completion or explicit failure. Analyst-controlled expansion. | Complete requested assessment or named incomplete checks with reasons. A polished report does not imply all evidence was collected. |
| E08 Make claims inspectable and durable. | Stable log/graph/document IDs; original artifact text, paths and scores; answer labels and saved turn identity. | Resolve labels against saved evidence; retain originals across reopen/rebuild; evidence projection/download exposes only intended fields. Graph tab draws only the saved walk. | Checkable citations, hop lines and full evidence lists; unresolved references warned. Reopened evidence reflects the original answer, not a new query. |
| E09 Keep investigation data from becoming instructions. | Untrusted log/document text, tool output and injection cases; read-only identities and fixed queries. | Fence data, keep artifacts out of model input, enforce read-only operations and safe plain-text presentation; test log and document canaries. | Legitimate evidence remains usable while malicious instructions are ignored. Quoting an injection is not obeying it. |
| E10 Make the whole capability repeatable and measurable. | Versioned world/corpus/gold; build identity; separate Port/knowledge-base exams; saved traces, scores and resource use. | Validate graph/source consistency; measure retrieval separately from interpretation; retain failures and independent score dimensions. Preserve original gates. | Reproducible evidence of what passed, failed or was never tested. No production-reliability claim from the four-case screen. |

## Evidence, present status and remaining proof

Saved-run details are indexed in the companion [evidence inventory](52-saved-evidence-inventory.md).
Owner tickets below identify existing responsibility or the T52 handoff needed; they do not
silently amend those tickets or approve a new implementation.

| ID | Current implementation and inspected evidence | What remains unproved / gap | Owner and required next evidence |
|---|---|---|---|
| E01 | **Implemented in parts:** detection, stable finding IDs and `search_logins`; `radius._period` records requested/effective bounds and warns that record bounds do not establish continuous coverage. Saved Port runs exercise login investigation. | No integrated T26 package. Omitted radius bounds currently use all available records, not T52's alert/event default. Existing search tools do not establish complete bounded case collection. | T52 reconciles scope into T26/T28; T26 proves exact trigger/surrounding selection and counts, invalid IDs and clipping. T29/T40 test live collection. T54's O1-09 tests fixed-evidence interpretation only. |
| E02 | **Implemented:** `knowledge_tools.account_tool` supplies owner, department and group kinds; Neo4j lookup returns records and paths. Privileged group kinds are recorded facts. T24 persistence evidence covers the lookup artifact. | No general structured job-role field; limited prose role evidence cannot generalise to every account. Relevant privilege/sensitive-access selection is not yet an integrated package. | T26 implements agreed selection and unavailable states. T29/T40 verify positive, absent and misleading-context cases. T52 records the selection handoff. |
| E03 | **Implemented/tested at retrieval boundary:** hybrid search and optional reranker. K01/K02/K07/K08 provide reusable document targets. **Demonstrated failure:** saved K04 retrieval loses the MFA register despite retaining the runbook. Approved O1-02/06/09/12-D have written scoring expectations, not results. | Missing candidate cannot be rescued by reranking. Merge/top-five survival and semantic applicability are separate risks. `search_corpus` agent adapter and investigation package are unbuilt. No scored O1 comparison exists. | T45 decides retrieval coverage/preservation; T25 adapter; T26 package; T39 refusal calibration; T41 switch comparison; T29/T40 end-to-end checks. T54 executes the approved reasoning screen. AUD-062/064 remain open. |
| E04 | **Implemented foundation:** graph radius returns memberships, assets, paths and snapshot basis; historical exact-set evidence remains valid for its recorded version. | Bounded selection and accurate potential-versus-observed presentation still need integrated proof. Full-inventory product delivery is deferred, not a missing release requirement. | T26 bounded context; T29/T40 selection and overclaim checks; T34 and evidence/graph tickets present selected evidence; T42 live acceptance. Preserve existing regression gold pending specific reconciliation. |
| E05 | **Implemented at core boundary:** `_device_peers` filters timestamps on both sides; `search_logins` supports source pivots. T50 removed address-sharing context. Current graph query uses all subject devices in the window. | Objective 1 needs involved-device selection, not all devices by default. No integrated related-activity collection or agent peer tool. No named end-to-end positive shared-device/spread proof found in the eight-question exam. | T52 reconciles selection semantics; T25 peer tool; T26 bounded collection; T40 positive/negative peer cases and same-source limits; T29/T42 runtime proof. Standalone peer lookup may retain its broader purpose. |
| E06 | **Partial:** graph period metadata and account unavailable/not-found states exist; K05/K06 absent-topic questions and S4 truth exist. Saved reranking scores distinguish relevance from proof that absence is detected. Approved missing-history scoring is written. | Live `none` calibration, integrated failure/omission distinction and analyst-controlled expansion are unproved. A high-ranked passage does not establish topic coverage. | T39 calibrates `none`; T26/T28 expose incomplete evidence and scope controls; T29/T40 test empty, failed, omitted, unavailable, conflicting and expansion cases. T54 O1-09 is narrower fixed-evidence proof. |
| E07 | **Intended for KB:** T28 fixed playbook/report gate. Existing Port policy is reusable, but registered tools currently contain only one KB tool, `lookup_account`. | Neither a resolved graph ticket nor a successful account call proves KB playbook completion, shortcut handling or partial-report behaviour. | T26 package; T28 enforcement; T29 process gates; T36 progress; T40 interactive cases; T42 live review. Evaluation-runner call policy does not replace application loop controls. |
| E08 | **Demonstrated narrowly:** T24 recorded close/reopen of 50 lookup artifacts; 601-byte single artifact, 16,404,480-byte SQLite file at 50 repeated lookups. Source retains `ToolMessage.artifact` while model gets briefing only. | T27 resolver, evidence panel/download and saved-walk graph presentation are unbuilt. Lookup persistence does not prove complete package persistence, rebuild-safe displayed evidence or storage scalability. Citation resolution/gold coverage do not establish semantic support. | T27 resolver; T29 citation checks; T33/T35 evidence/display/download; T34/T37/T38 presentation; T42 acceptance. AUD-065 owns broader storage review. T30 advisory judge remains non-gating. |
| E09 | **Implemented in part:** read-only account adapter, fixed parameterised Neo4j queries and data fencing. Saved Port security results are historical evidence for that exam. O1-12-D's document-injection rules are approved. | Port canaries do not prove future document retrieval, specialist handoffs or new evidence rendering are safe. Fixed-evidence screen does not prove storage permissions or UI boundaries. | T25/T26/T28 tool/workflow boundaries; T29/T40 both canaries; T33/T35/T37 plain-text/minimal-field checks. T54 separately proves its gold isolation, masking and screening behaviour. |
| E10 | **Implemented in parts:** build/integrity checks, paired-store lifecycle, retrieval-only runner and eight KB questions. Historical migration/Port results exist; T53 reports accepted native Browser access. | Full KB agent exam, phase-1 expanded questions, kept-five gate, calibration and full Langfuse integration remain unbuilt/unproved. Native Browser acceptance is not in-app Graph acceptance. 50-person/30-day target is approved but not generated. | T29 full exam; T30 advisory judge; T31 application/full-exam recording; T39/T40/T41 calibration/coverage/comparison; T42 final gate. T54 owns isolated comparison evidence only. T52 must assign any new dataset build before implementation. |

## E06 approved boundary — 2 November 2026

Use small controlled evaluation cases to distinguish missing coverage, empty results, failed
checks and omitted results. Do not expand the world to resolve every uncertainty. The separate
50-person/30-day target remains unchanged. Next-investigation guidance must combine case facts
with approved incident-response practice, identify the uncertainty addressed and distinguish
external analyst checks from available app actions. Do not imply a recommended check ran.
Curated guidance sources and relevance tests are required. Approved allocation: T45 selects
sources for author review, T26 integrates them, and T40/T29 test relevance in the app. Broad response planning and automated containment
are deferred. Analyst-controlled expansion remains in force.

## Direct implementation references

- [Tool registry](../../../backend/login_investigator/tools.py): `tools_for` exposes the three Port tools plus account lookup.
- [Account adapter](../../../backend/login_investigator/knowledge_tools.py): model briefing, full artifact, snapshot basis and unavailable/not-found distinction.
- [Graph operations](../../../backend/login_investigator/knowledge_base/neo4j_graph.py): `lookup_account`, `finding_radius`, `_device_peers`.
- [Period/radius contracts](../../../backend/login_investigator/knowledge_base/radius.py): `_period`, `Period`, `FindingRadius`, `radius_walk`.
- [Graph tests](../../../backend/tests/test_knowledge_graph.py): exact S6 radius and date filtering on both relationship sides. Test source is not a fresh passing run.
- [Eight-question exam](../../../backend/evals/knowledge_base_questions.json): K01–K08, gold and intended conclusions.
- [Lookup persistence measurement](24-persistence-evidence.md): historical measurement; its in-memory graph description predates Neo4j migration.
- [Current package ticket](../issues/26-investigate-alert-package.md), [playbook ticket](../issues/28-playbook-enforced.md), [retrieval decision ticket](../issues/45-compound-question-retrieval-design.md): remaining implementation/design boundaries.

## Reconciliation queue, not scope decisions

| Item | Recorded authority / finding | Follow-up |
|---|---|---|
| Full blast radius versus bounded context | Author confirmed objective 1 as sole scope. Standalone full inventory and reverse exposure deferred. | Reconcile T26 and presentation/evaluation requirements to bounded context; retain graph foundations and existing gold until specific revisions are approved. |
| Window and device selection | Latest T52 alert/event windows and involved-device rules differ from existing T26 default and generic radius behaviour. | Reconcile package requirements in T52; preserve generic lookup semantics unless a separate change is approved. |
| Old address/storage descriptions | Spec overview/stories still mention address peers and one store; K03 provenance mentions removed address-reuse context. Later graph rulings supersede them. | Track documentation inconsistency separately; reconcile under T46/T50 rulings. Do not edit frozen question/gold data casually. |
| Old acceptance inspection wording | T42 still names Gephi although the spec's later T46 ruling selects Neo4j Browser. | Reconcile the acceptance pointer under the existing ruling; do not claim Browser proves the future in-app Graph tab. |
| Threat/benign “verdict” wording | Older overview uses categorical verdict language; P-02 and T52 keep final verdict with the analyst. | Align approved assessment language in downstream requirements; do not invent new thresholds or silently change gold. |
| Broader case and data coverage | Existing eight questions and four-case screen omit much of E04–E10's live workflow proof. | T40 retains full phase-1 exam; T52 settles larger-data ownership, scope dispositions and any additional proposed acceptance rules. |

Reverse asset exposure and standalone full asset inventory are explicitly deferred. Broader
account investigation, behavioural baselines and endpoint telemetry are not added by this
ruling; record their applicable existing boundaries during T52 reconciliation rather than
reopening reverse exposure as a candidate for this phase. The screening and specialist comparison
approvals stand unchanged. T54 remains blocked until T52 closes.

## Verification and limits

Documentation/source audit only. Local link existence and whitespace are checked separately.
No application files, acceptance gates, gold, spec decisions, operator commands or services changed.
Historical failures remain failures. AUD-062, AUD-064, AUD-066 and AUD-076 stay open.
All ten objective-table rows are approved. Candidate dispositions and downstream
reconciliation remain separate T52 obligations; this approval does not certify runtime reliability.

## Reconciliation completed — 2 November 2026

The queue above preserves findings at mapping time. T52 is now resolved: active spec and
T26/T45, T27–T30, T34/T40/T42 criteria carry the approved boundaries. T55 owns expanded data
before T40. T34 retains author screen/API agreement. Source selection belongs to T45 for
author approval, not to a reopened T52 discussion. The remaining K03 provenance correction
belongs to T40 under B-143/B-145; T51 is resolved and excluded exam edits. Existing questions,
gold and thresholds remain unchanged. AUD-076's decision review closes; AUD-062/064/066 and
all later implementation/evaluation proof obligations remain open. Historical statements of
pending reconciliation above are superseded by this completion record.
