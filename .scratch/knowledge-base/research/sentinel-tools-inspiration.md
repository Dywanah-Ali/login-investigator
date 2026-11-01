# Microsoft Sentinel tools as inspiration

Date: 1 November 2026
Scope: short research requested by the author. Ideas only; no implementation, integration, or spec change approved.
Method: Microsoft documentation reviewed online. No tenant connection or hands-on verification.

## Assessment

The most useful principle is to organise tools around investigation questions. A tool should return the evidence needed to answer a bounded question. Tool count alone adds no investigative value.

These five areas are relevant to Login Investigator. The examples and recommendations below are our assessment, not claims about existing app behaviour.

| Area | Verified Microsoft capability | Inspiration for our app |
|---|---|---|
| Graph investigation | Preview graph tools include `find_blastradius`, `find_walkable_paths`, and `find_exposure_perimeter`. They examine outward propagation, traversability between entities, and incoming connections respectively. [Source](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-data-exploration-tool) | Our current blast-radius work overlaps the outward view. A useful future inverse question is: “Which accounts can reach payroll, and through which grants?” Distinguish an access path from evidence that an attacker actually used it. Attack-path semantics require a later agreed scope. |
| Entity analysis | `analyze_user_entity` analyses authentication, anomalies, and organisational activity. It starts a job whose result is retrieved with `get_entity_analysis`. [Source](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-data-exploration-tool) | Package the account's evidence around “Is this account compromised?” rather than presenting disconnected log rows. Our existing investigation package already follows much of this pattern. A useful comparison is whether each verdict clearly separates observed facts, interpretation, and missing data. |
| Triage evidence pivots | Triage tools retrieve user-related alerts and machines, device alerts, signed-in users, and device vulnerabilities. They also fetch incident and alert evidence and run advanced hunting queries. [Source](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-triage-tool) | Investigate “The login succeeded on this device. What else happened there?” A future device evidence bundle could combine sign-ins and endpoint alerts. Shared-device sign-in evidence alone does not prove compromise or lateral movement. Endpoint telemetry would need new synthetic ground truth or a later real-data source. |
| Behavioural baselines | Sentinel UEBA compares current activity with historical entity profiles and peer or organisational patterns. [Source](https://learn.microsoft.com/en-us/azure/sentinel/identify-threats-with-entity-behavior-analytics) Its newer anomalies-on-behaviors feature is explicitly preview and emits explainable first-seen, high-volume, uncommon-value, and threat-intelligence insights. [Source](https://learn.microsoft.com/en-us/azure/sentinel/ueba-anomalies-on-behaviors) | Ask “Is this unusual for this account?” A bounded future version could show prior successful device use and observed login times over an explicit history window. Explain the comparison and sample size. An unfamiliar device alone must not become a malicious verdict. |
| Custom query tools | Custom MCP tools are preview. Microsoft lets administrators save verified, optionally parameterised KQL queries as named tools and collections. [Source](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-create-custom-tool) | Preserve expert investigative queries as tested tools such as “show successful sign-ins after this spray.” This supports our existing typed, read-only core-function approach. MCP would be useful later if multiple external clients need these capabilities; the internal app does not need MCP merely to follow this principle. |

## Additional useful capability

UEBA behavioural peers are a comparison population for normal activity. Our shared-device peers answer a relationship question. They should keep separate meanings even if a later feature uses both.

Data exploration includes `search_tables` to discover relevant schemas and `query_lake` to query the Sentinel lake. This is useful inspiration for a future app with many event sources. With one known login dataset, dynamic table discovery offers little immediate advantage. Source: [data exploration](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-data-exploration-tool).

## Adoption constraints

- These are services over Microsoft security data. Connecting them does not automatically make our local Neo4j graph or synthetic login files available to them.
- Data exploration requires Sentinel data lake access and relevant security roles. Graph access additionally requires Defender onboarding and Exposure Management read access. Graph querying is metered. The user analyser requires Security Copilot Contributor, consumes Security Compute Units, has a seven-day maximum window, and requires particular tables and Entra user identities. Source: [data exploration prerequisites and limits](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-data-exploration-tool).
- Triage requires Defender XDR, Defender for Endpoint, or Sentinel onboarded to Defender. Its documented limits include home-tenant access, no Sentinel workspace selection, and no Sentinel lake querying through this collection. Source: [triage prerequisites and limits](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-triage-tool).
- Custom tools require Sentinel data lake and Defender licences. Creation and use have different role requirements. Source: [custom tools prerequisites](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-create-custom-tool).
- The inspected overview lists data exploration, Security Copilot agent creation, and triage as available collections. This does not establish universal access or general availability for every subtool. Graph and custom-tool preview labels are explicit. Source: [tool collection overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-tools-overview).

## Recommendation

Study graph exposure questions and explainable baselines first as future product ideas. Use custom query tools as an architecture reference now. Entity analysis and triage can help assess the completeness of our existing evidence packages. Keep direct Sentinel integration separate until an actual Sentinel-backed use case exists.

The current phase 0 and 1 scope stays unchanged. These research ideas do not reopen parked audit entries or approve later history, context, or attack-path features.
