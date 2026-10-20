# Research note 01: a use case for the knowledge base

Ticket: [01-use-case-research](../issues/01-use-case-research.md)
Date: 20 October 2026
Method: one Perplexity deep-research call (succeeded, about 4 minutes) plus seven Perplexity search
calls restricted to primary domains to verify the claims that carry weight. No secrets involved.
Sources are listed at the end; `[P]` marks a claim verified against a primary source, `[V]` marks a
vendor or practitioner claim that was not independently verified.

## 1. The question

The Login Investigator sees seven fields per event (time, user, IP, country, device, outcome,
user-agent), runs four rules (brute force, password spraying, success after failures, new-country
sign-in) and lets an agent answer questions with read-only tools over the log and an IP-reputation
lookup. The author wants a knowledge base, built around a knowledge graph with RAG in its
ecosystem, that turns a flagged row into an explained risk with organisational context. Which real
use case should it serve?

## 2. How security teams use graphs around authentication events

| Practice | Nodes | Relationships and the question they answer | Status |
|---|---|---|---|
| **SIEM entity model.** Microsoft Sentinel recognises entities in alerts (Account, Host, IP address, Security group, Cloud application, and others), merges them across data sources by strong and weak identifiers, and gives each an entity page with facts, a timeline and behavioural insights. Its investigation graph links entities and alerts. | Account, Host, IP, Application, Alert, Incident | Alert involves account; alert involves IP; incident contains alert. "Has this IP or user appeared in other alerts?" | [P] Sentinel docs: entities, entity pages |
| **Asset and identity enrichment.** Splunk Enterprise Security keeps asset and identity lookups and joins them to events. Documented identity fields include `managedBy`, `bunit`, `startDate`, `endDate`, `category`, `priority`, `watchlist`; asset fields include `owner`, `priority`, `category`, `bunit`, `country`, `ip`, `dns`, `nt_host`. UEBA uses them to pick the right entity and peer group. This is enrichment by lookup, not a graph database. | Identity, Asset | Identity managed by; asset owned by; asset has priority. "Is this a privileged person, and does the device belong to them?" | [P] Splunk ES docs |
| **Attack-path graphs.** BloodHound models directory objects as nodes (User, Group, Computer, Domain, OU, GPO) and privilege as directed edges (`MemberOf`, `AdminTo`, `HasSession`, `GenericAll`, and so on). The edge direction always means the direction of attack or privilege. A path is *possible* access, not proof it was used. | User, Group, Computer, Domain | `MemberOf`, `AdminTo`, `HasSession`. "What can this user reach through its groups?" | [P] BloodHound docs: nodes, edges, graph theory |
| **Exposure graphs.** Microsoft Exposure Management builds paths from entry points to critical assets over devices, identities, groups and cloud assets. | Identity, Group, Device, Asset, Finding | `routes traffic to`, `contains`, `affecting`. "Which critical assets lie on a path from this identity?" | [V] not independently opened |
| **Graph databases for security.** Neo4j and TigerGraph describe user, device, IP and activity graphs for tracing lateral movement that no single event would flag. Useful shape; the performance and detection claims are vendor claims. | User, Device, IP, System | `USED_DEVICE`, `CONNECTED_FROM_IP`, `ACCESSED_SYSTEM`. "Do accounts on different IPs converge on one device?" | [V] |

Common thread: **the graph holds durable relationships** (who owns what, who belongs to which
group, what a group can reach, which network an IP belongs to, which incidents touched an entity).
The event log stays the source of truth for what happened. Nobody copies every log row into the
graph.

## 3. What an analyst reaches for beyond the log row

Microsoft's published compromised-identity procedure asks, in order: which applications were
touched, MFA state, user confirmation, identity type (human, service, emergency), related accounts
and devices, and blast radius. It says to check owner and approval before disrupting a service or
break-glass account. [V, Microsoft SOP template; not opened directly]

| Knowledge | Shape | Where it lives in our design |
|---|---|---|
| **ATT&CK meaning.** T1110 Brute Force has sub-techniques .001 Password Guessing, .002 Password Cracking, .003 Password Spraying, .004 Credential Stuffing. T1078 Valid Accounts (.004 Cloud Accounts) is abuse of legitimate credentials. T1621 is MFA request generation, including MFA fatigue. Each page lists mitigations (M1036 Account Use Policies, M1032 MFA, M1018 User Account Management, M1027 Password Policies) and detection analytics. | Versioned text, exact IDs | Text corpus, keyword-heavy. Graph holds `Technique` nodes with `SUBTECHNIQUE_OF` and `MITIGATED_BY` for exact joins. A rule's mapping to a technique is "consistent with", never proven by the rule alone. [P] attack.mitre.org |
| **Threat intelligence.** Campaign reports describe infrastructure, automation and breached-credential reuse; attackers spread stuffing across many IPs, so one IP verdict is incomplete. | Dated narrative text | Text corpus, semantic. Graph holds `Report`, `Indicator`, `Campaign` with `MENTIONS` and first/last-seen. [V] Cloudflare blog |
| **Runbooks.** Brute-force, spraying, account-takeover, travel and MFA-fatigue procedures; escalation and evidence steps. The right runbook depends on account type. | Versioned text | Text corpus. Graph links `Runbook` to `AccountType` and approver. |
| **Identity and access policy.** Travel and remote-work policy, VPN exceptions, privileged-access and service-account standards, joiners-movers-leavers. | Effective-dated text plus dated facts | Policy text in the corpus; the *person's* approved travel, exception and employment status in the graph with dates. |
| **Business impact and history.** Which assets an account can reach and how critical they are; how a similar alert was resolved last time. | Facts plus narrative | Grants, criticality and owners in the graph; incident narratives in the corpus; `Incident` nodes with disposition link the two. |

**Boundary of today's log.** The log does not say which application was targeted, whether MFA
was prompted, what the account can access, or whether `device` is a stable identifier. Those facts
must come from separately generated sources or the agent must say "unknown". Keep *granted access*
distinct from *observed access*.

## 4. Where the graph wins, where text wins, and how they combine

| Question type | Best path | Why |
|---|---|---|
| "Which critical systems *could* this account reach?" | Exact account lookup, then bounded traversal over membership and grants | Multi-hop reachability. Text search cannot follow a chain. [P] BloodHound shape |
| "Which other users share this device or source network, and what incidents involved them?" | Traversal over time-qualified observed-use and incident edges, then verify in the log | A shared entity joins otherwise separate records. An IP match behind a VPN is weak evidence. [P] Sentinel investigation graph |
| "Is this account human, service or break-glass, and who owns it?" | Graph lookup | One fact, one hop. |
| "What is credential stuffing and how does it differ from spraying?" | Keyword retrieval on the ATT&CK ID, semantic as backup | A definition lives in text. [P] |
| "What does our travel policy say about a sign-in from Germany?" | Hybrid text search for the rule, graph lookup for the person's actual approval | Text supplies the rule; dated facts decide if it applies. |
| "How did we resolve the last alert on this VPN exit?" | Semantic search over incident notes, then graph pivot to shared entities | Different wording, same case. |

**Retrieval design the sources support.** Resolve exact identifiers first. Run keyword (BM25 or
Lucene full-text) and vector search over chunked, versioned documents. Fuse the two result lists
and re-rank. Then traverse from the cited chunks to their policy, technique, incident or entity
nodes. Neo4j's GraphRAG package ships exactly this shape: `HybridRetriever` (vector plus full-text
index) and `HybridCypherRetriever` (the same, followed by a Cypher traversal from the matched
node). Its full-text score is a Lucene relevance score; an explicit re-ranking stage is a separate
step. [P] neo4j-graphrag-python docs. Microsoft Azure AI Search documents the same BM25-plus-vector
fusion with reciprocal rank fusion and a semantic re-ranker. [V, not opened]

**What not to build.** Microsoft Research's GraphRAG (entity extraction from every document plus
community summaries) targets corpus-wide "what are the themes" questions and carries a large
indexing cost. Our questions are local and entity-anchored. Start with a hand-modelled graph and
bounded traversals. [V, Microsoft Research paper, not opened]

## 5. Data a credible synthetic set needs

| Component | Content |
|---|---|
| **People and accounts** | `Person` (department, role, manager, privilege level, employment status with dates, home country). Separate `Account` nodes per identity type: employee, admin, service, break-glass. `HAS_ACCOUNT`, `REPORTS_TO`, `OWNED_BY`. |
| **Access** | `Group`, `Application`/`Asset` with criticality and owner. `MEMBER_OF`, `GRANTS_ACCESS_TO`. Observed access, if any, as separate dated events. |
| **Network and devices** | `IPRange` classified corporate, VPN, residential, known-bad; `Device` with a stable ID and owner. `IP_IN_RANGE`, `USES_DEVICE`. |
| **Context facts** | `TravelApproval` with dates and countries; `PolicyException` with approver and expiry. |
| **History** | `Incident` with disposition (benign, confirmed, inconclusive), linked to accounts, IPs, devices and the ATT&CK technique it was mapped to. |
| **Text corpus** | Policies (travel, VPN, privileged access, service accounts, joiners-movers-leavers), runbooks (one per rule plus account takeover and MFA fatigue), ATT&CK technique pages for T1110 and sub-techniques, T1078, T1078.004, T1621, T1556, short threat-intel bulletins, past incident write-ups. All versioned and dated. |
| **Linked cases in the log** | A spray that never succeeds; a spray followed by a success on a privileged account; an approved trip; the same country reached through the corporate VPN; a departed employee's still-active account signing in; a service account on its normal schedule and once off-schedule. Event time, policy effective time, edge validity and incident outcome must agree. |

**Public starting points, and why none replaces our own set**

| Source | Offers | Gap for us |
|---|---|---|
| Kaggle "Synthetic Enterprise Auth Logs" (180,000 events, 498 users, 150 hosts, labelled T1078/T1021 chains, `user_role` standard or admin) | A labelled user-to-host authentication stream for lateral-movement study | No country, device, policy, HR or asset context. Host-to-host shape, not our internet-facing login shape. [V] |
| LANL "Comprehensive, Multi-Source Cyber-Security Events" | 58 days of real de-identified authentication with red-team labels | No organisational context at all; its failures only exist for users who also succeed somewhere. [V] |
| Splunk Attack Data, OTRF Security-Datasets (Mordor) | Replayable ATT&CK-scenario captures | Event schemas differ; no HR, access, travel or incident records. [V] |
| Microsoft Sentinel sample data | `SigninLogs` examples: normal sign-in, new location and device, impossible travel, Conditional Access block | A schema reference and fixture set, not an organisation. [V] |
| BloodHound CE sample collections; BadBlood generator | A realistic directory graph of users, groups, computers and permissions | No paired login timeline, travel or incidents. Good shape reference for the access part of our graph. [P] BloodHound docs; [V] BadBlood |
| OrgForge (deterministic corporate simulator with an insider-threat module and IdP authentication anomalies) | Ground-truth organisational activity paired with security telemetry | Far larger than we need; worth reading for its idea that facts come from a state machine and prose is generated on top. [V] |

Conclusion on data: generate our own, small and consistent, with a written ground truth per case.
Borrow shapes from BloodHound (access) and Sentinel (sign-in fields). Size for testing, not scale:
tens of people, a handful of groups and assets, a few dozen documents.

## 6. Candidate use cases

All three share one graph and one corpus. They differ in which relationships and documents carry
the answer, and in how much data they need. They are slices of one knowledge base, so the choice is
about which slice goes first.

### Candidate 1: Explained new-country sign-in

| | |
|---|---|
| Graph | `Person`→`Account`; `Person`→`TravelApproval`; `IP`→`IPRange`→`Network` (corporate, VPN, residential, known-bad); `Account`→`Device`; `Policy`→applies to role or account type |
| Corpus | Travel and remote-work policy, VPN exception policy, account-takeover runbook, past travel-alert resolutions |
| Questions the log-only agent cannot answer | Was this employee approved to travel there on that date? Is the IP a corporate VPN exit rather than a local ISP? Does an exception cover this account? Who can confirm the trip? How was their last overseas alert resolved? |
| Data | Home countries, managers, dated approvals, VPN and non-VPN ranges, stable device IDs, approved and unapproved cases, past dispositions |
| Value | Turns the noisiest rule into "expected" or "escalate", with the policy and the fact behind it. Mostly one-hop lookups and text search. Smallest build. |

### Candidate 2: Spray-to-compromise blast radius

| | |
|---|---|
| Graph | `Account`→`Group`→`Application`/`Asset` (criticality, owner); `Account`→`Device`; `Alert`/`Incident`→accounts, devices, IPs; `Technique` with `SUBTECHNIQUE_OF`, `MITIGATED_BY`. Grants kept separate from observed access |
| Corpus | Spraying, stuffing and takeover runbooks; ATT&CK T1110.003, T1110.004, T1078, T1078.004; asset-handling instructions; past incident write-ups |
| Questions | Which privileged accounts were among the spray targets? What critical applications could the account that later succeeded reach? Which of those was it observed using, if we have that data? Which other users and incidents share its device or source network? Who owns the highest-impact asset and what is the containment step? |
| Data | Many-account failures, a later success on a privileged account, benign controls, account-group-asset grants, owners and criticality, labelled outcomes |
| Value | Turns "success after failures" into a scoped investigation of possible versus evidenced impact. This is where multi-hop traversal clearly beats search. Medium build. |

### Candidate 3: Privileged and service-account triage

| | |
|---|---|
| Graph | `Account` with type and status; `Account`→`Person`/`Team` owner; `Account`→`Group`→`Asset`; `Account`→`Policy`; `Incident`→`Account` |
| Corpus | Privileged-access and service-account standards, joiners-movers-leavers policy, emergency-access procedure, secret-rotation runbook, postmortems |
| Questions | Is this a human, service or break-glass account? Is its owner still employed? Which workloads depend on this service identity? Who must approve disabling or rotating it? Was this pattern investigated before, and what was the outcome? |
| Data | Employment lifecycle dates, separately owned service and emergency accounts, dependencies, named approvers, dated policies, a scheduled service login and an orphaned account |
| Value | Prevents a harmful response (killing a service or locking emergency access) and surfaces the departed-employee case the rules cannot see. Medium build, graph-heavy. |

### Recommendation

Start with **Candidate 2**, folding in Candidate 1's network and travel facts, because they are
cheap once the graph exists. Reasons: it builds directly on an existing rule; it is the slice where
the graph does something text search cannot; and it is the one that most matches the author's aim
of showing the threat behind the login, not just the login. Candidate 3 follows naturally as the
second slice, since its account-type and ownership nodes are already in the graph by then.

Two safeguards to carry into the spec regardless of choice:

- Every answer cites the log events, the graph path and the document passages it used, and labels
  an ATT&CK mapping as "consistent with" until evidence supports more.
- The graph and document tools stay read-only, like the existing tools.

## 7. Broadening of slice 2 (author's ruling, 20 October 2026)

The author chose slice 2 as the first slice and accepted the broadening below, in the order
given. Each row is a later step on the same graph and corpus, not a new project. Each step gets
its own spec section, its own tickets and its own additions to the eval set before it is built.

| Order | Broadening | What it adds | Why it is cheap | Data it needs beyond slice 2 |
|---|---|---|---|---|
| 1 | **Spread.** Which other accounts were hit in the same spray, and which of them matter? | Finds the real target among the noise. | Same nodes, one more query. | None. |
| 1 | **Shared ground.** Which users share this device or this source network? | A compromised shared IP or device drags other users in. | `USES_DEVICE` and `IP_IN_RANGE` edges. | Stable device IDs; IP ranges classified. |
| 2 | **History.** Has this account, IP or device been in a past incident, and how did it end? | Stops repeated work; reveals repeat targets. | `Incident` nodes with an outcome, linked to entities. | Past incidents with dispositions and write-ups. |
| 3 | **Travel and network facts** (from slice 1). Was the user travelling? Is the IP our VPN exit? | Removes false alarms before they waste time. | `TravelApproval` and `Network` nodes. | Dated approvals; VPN and corporate ranges; policy text. |
| 3 | **Account type** (from slice 3). Person, service or break-glass? Who owns it? Is the owner still employed? | Changes the response; a service account cannot simply be locked. | A type property and an `OWNED_BY` edge on `Account`. | Account types, owners, employment dates; service-account standard. |
| 4 | **Attack path.** From this account, what is the shortest path to the most critical asset? | Shows what the attacker gains, not only what they touched. The BloodHound idea. | A path query on the existing access edges. | Enough groups and grants to make paths non-trivial. |
| 4 | **Risk score.** Combine privilege, asset criticality and attack type into one ranking. | Lets the Alerts screen sort by real risk, not by time. | A formula over facts already on the map. | A written scoring policy, agreed by the author. |
| Later | **GRC view.** Which controls and policies does this incident touch? | Same map read by a different team. | Control and policy nodes linked to assets and incidents. | A control catalogue; its own slice and spec. |

Rule for the order: a step that needs no new data comes before a step that does. Every fact added
to the map needs a written ground truth, or its answers cannot be tested.

## 8. Evidence gaps

- The Microsoft SOP template, Exposure Management schema, Azure AI Search hybrid docs and the
  Microsoft Research GraphRAG paper were cited by the deep-research pass but not opened directly.
  Their claims are marked [V] and nothing in the recommendation depends on them alone.
- Dataset descriptions (Kaggle, LANL, Splunk, OTRF, OrgForge) come from their public listings, not
  from downloading and inspecting the data.
- No source measured how much a graph improves *this* kind of small investigation. The claim that
  multi-hop questions need a graph rests on the shape of the question, not on a benchmark.

## Sources

Primary, opened in this research:

- Microsoft Sentinel, "Entities in Microsoft Sentinel": https://learn.microsoft.com/en-us/azure/sentinel/entities
- Microsoft Sentinel, "Entity pages": https://learn.microsoft.com/en-us/azure/sentinel/entity-pages
- Splunk ES, "Configure asset and identity data for UEBA": https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.3/user-and-entity-behavior-analytics/configure-asset-and-identity-data-for-ueba-in-splunk-enterprise-security
- Splunk ES, "Asset and identity fields after processing": https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.3/asset-and-identity-validation/asset-and-identity-fields-after-processing-in-splunk-enterprise-security
- BloodHound, "About nodes": https://bloodhound.specterops.io/resources/nodes/overview
- BloodHound, "About edges": https://bloodhound.specterops.io/resources/edges/overview
- BloodHound, "HasSession": https://bloodhound.specterops.io/resources/edges/has-session
- BloodHound, "AdminTo": https://bloodhound.specterops.io/resources/edges/admin-to
- BloodHound OpenGraph, "Graph theory": https://bloodhound.specterops.io/opengraph/developer/graph-theory
- MITRE ATT&CK T1110: https://attack.mitre.org/techniques/T1110/
- MITRE ATT&CK T1078: https://attack.mitre.org/techniques/T1078/
- MITRE ATT&CK T1621: https://attack.mitre.org/techniques/T1621/
- MITRE ATT&CK M1032: https://attack.mitre.org/mitigations/M1032/
- Neo4j GraphRAG Python, "User guide: RAG": https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html
- Neo4j GraphRAG Python, API: https://neo4j.com/docs/neo4j-graphrag-python/current/api.html
- Neo4j GraphRAG Python, hybrid retriever source: https://neo4j.com/docs/neo4j-graphrag-python/current/_modules/neo4j_graphrag/retrievers/hybrid.html

Secondary, cited by the deep-research pass and not opened:

- Microsoft Defender XDR, SOP documentation template: https://learn.microsoft.com/en-us/defender-xdr/sop-documentation-template
- Microsoft Entra ID Protection, "Investigate risk": https://learn.microsoft.com/en-us/entra/id-protection/howto-identity-protection-investigate-risk
- Microsoft Exposure Management schema: https://learn.microsoft.com/en-us/security-exposure-management/schemas-operators
- Azure AI Search, hybrid query: https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query
- Microsoft Research, "From Local to Global: A Graph RAG Approach": https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/
- Cloudflare, password reuse and credential stuffing: https://blog.cloudflare.com/password-reuse-rampant-half-user-logins-compromised/
- Kaggle, Synthetic Enterprise Auth Logs: https://www.kaggle.com/datasets/codewithdaniel1/synthetic-enterprise-auth-logs
- LANL auth data: https://csr.lanl.gov/data/auth/
- Splunk Attack Data: https://github.com/splunk/attack_data
- OTRF Security-Datasets: https://github.com/OTRF/Security-Datasets
- Microsoft Sentinel sample data: https://learn.microsoft.com/en-us/azure/sentinel/isv/ingest-sample-data
- BloodHound CE sample data: https://bloodhound.specterops.io/get-started/quickstart/ce-ingest-sample-data
- BadBlood: https://github.com/davidprowe/badblood
- OrgForge: https://github.com/aeriesec/orgforge
- TigerGraph, graph security monitoring: https://www.tigergraph.com/blog/network-security-monitoring-graph-database/
- Neo4j, graphs for cybersecurity: https://neo4j.com/blog/security/graphs-for-cybersecurity/
