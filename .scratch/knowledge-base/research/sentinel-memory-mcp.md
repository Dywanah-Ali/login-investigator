# Microsoft Sentinel Memory MCP

Date: 1 November 2026
Scope: short discussion research requested by the author. No integration or architecture change approved.
Method: bounded web search of Microsoft primary sources. No tenant connection or hands-on test.

## Verified findings

Microsoft's Foundry catalog lists **Microsoft Sentinel Memory (PrPr)** as a remote MCP collection at `https://sentinel.microsoft.com/mcp/memory`. Its lifecycle is Preview, and its description explicitly says it is in testing mode. Authentication options listed are OAuth 2.0 and Agent Identity. The listing gives 15 June 2026 as its release date. This is not evidence of general availability or unrestricted tenant access.

The collection provides durable knowledge across investigations: natural-language search, retrieval and deletion by identifier, and insertion or updating of observations. The service summarizes observations and creates embeddings for later recall. Listed memory categories include incidents, alerts, cases, analyst notes, standard operating procedures, and agent artifacts. Described uses include reusing prior findings, consulting procedures, inspecting a particular memory, and removing stale material. These are published capabilities, not independently measured results.

Source: [Microsoft Foundry Memory catalog listing](https://ai.azure.com/catalog/tools/ms-sentinel-memory/version/1/apiCenter/registry-prod-bl/eastus?flight=unauth_catalog_filtering).

The broader Sentinel MCP offering exposes security tools through a hosted interface using Microsoft Entra identity. The public tool overview separately lists data exploration, Security Copilot agent creation, and triage collections. Memory is therefore a particular collection, not another name for all Sentinel MCP capabilities. The inspected tool overview does not yet list Memory.

Sources: [Sentinel MCP overview](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-overview), [tool collections](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-tools-overview).

## Limits of the public evidence

The catalog's documentation link, `https://aka.ms/mcp/sentinel-memory`, was inaccessible through the research browser. This check did not establish Memory-specific onboarding, licensing or pricing, retention, data residency, detailed access controls, audit coverage, quotas, or general tenant availability. Prerequisites documented for other collections should not be assumed to apply unchanged to Memory. The name's “PrPr” suffix is left uninterpreted; Preview and testing mode are the explicit verified status labels.

The general Sentinel MCP application card discusses model-dependent output quality and incomplete or stale security data. It does not resolve the Memory-specific questions above. Source: [Microsoft's application card](https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-mcp-responsible-ai-faq).

## Assessment for Login Investigator

The useful architecture principle is to separate remembering a conversation from retaining reusable investigative knowledge. A conversation checkpoint helps resume one discussion. A searchable case notebook helps a different investigation recover relevant earlier findings. MCP supplies a standard way for an agent to access the notebook; it does not by itself establish that a remembered conclusion is true.

Illustrative use: a new password-spray case retrieves an earlier analyst-confirmed explanation of a similar pattern and the evidence that supported it. The agent must still check the current case. Repeated similarity is not proof that the new event has the same cause.

My assessment: the concept is valuable for a security team with repeated investigations. For this project, it is an architectural reference for the later history phase, not a demonstrated replacement for the current Neo4j relationship queries or PostgreSQL document retrieval. Its published write and delete operations also exceed this project's current read-only agent-tool policy.

Before any future adoption, evaluate source provenance, separation of observations from conclusions, analyst correction, expiry, permissions, and resistance to poisoned memories. These are proposed evaluation criteria, not claims that Microsoft lacks these controls. Automatically preserving a mistaken conclusion can make subsequent investigations confidently repeat it.

Recommendation: learn from the pattern now. Revisit the service only if a future approved history use case and a Sentinel environment make it relevant. Do not change the current initiative on the strength of a preview catalog entry.

Local context: [initiative map](../map.md), which scopes the current work to phases 0 and 1 and places history in phase 2; the repository's AGENTS.md read-only agent-tool rule.
