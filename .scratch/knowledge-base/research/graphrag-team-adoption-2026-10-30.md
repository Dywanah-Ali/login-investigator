# GraphRAG choices among product teams

Date: 30 October 2026
Scope: discussion research requested by the author. No architecture decision or migration is approved.
Method: Perplexity search over named primary case studies, checked against the existing T02 planning note. A bounded search, not a market survey. A broader Perplexity research request was started and terminated before completion once the bounded evidence was sufficient; findings below rely only on the specific sources inspected.

## Finding

The inspected evidence does not establish what most medium-sized companies or teams prefer. No representative survey segmented by company size, engineering-team size, and GraphRAG engine was established in this search. Public case-study counts cannot supply that missing denominator.

There is concrete evidence of product teams building graph-plus-vector retrieval with Neo4j and Memgraph, and an internal legal/compliance GraphRAG application using FalkorDB. These examples support a shortlist, not a market-share ranking. Company headcount and implementation-team headcount were not verified, so none is labelled medium-sized here.

## Specific deployments

| Builder or organisation | Confirmed technology and use | Deployment evidence | Limits of evidence |
|---|---|---|---|
| Lettria | Neo4j for graph retrieval and Qdrant for vector retrieval over financial/ESG reports. The case describes 45 reports and more than 15,000 pages. | Lettria's own case study says a hybrid GraphRAG solution was deployed for a banking group. | Client anonymised and described as a large international banking group. Builder/team size, database edition, and hosting model not established. Vendor-reported outcomes are not independent benchmarks. |
| Precina Health | Memgraph plus Qdrant in its Provider-Patient CoPilot. Vector search locates information and graph traversal connects patient context. | Memgraph's 17 October 2024 account reports a presentation by Precina's chief technology officer describing current use. | Vendor-hosted customer account. Staffing, edition, hosting model, and rollout scale not established. No clinical outcome claim is evaluated or repeated here. |
| SERGAS Group | FalkorDB knowledge graph, read-only retrieval tools exposed through MCP, and a Claude Skill for legal/compliance questions. | An engineering leader's first-person case study, published by FalkorDB on 21 July 2026, describes the skill shipped to the company workspace and the graph on the internal network. | Vendor-hosted first-person account. Staffing, database edition, and contractual licence not established. Internal network does not by itself establish which commercial deployment package is used. |

Sources:

- [Lettria: GraphRAG for financial and ESG reports](https://www.lettria.com/case-study/graphrag-for-complex-financial-esg-reports). The page contains an unrelated testimonial naming another company; it is not treated as identifying the banking client.
- [Precina Health's Memgraph and GraphRAG system](https://memgraph.com/blog/precina-health-memgraph-graphrag-type-2-diabetes-care).
- [SERGAS: legal GraphRAG delivered as a Claude Skill](https://www.falkordb.com/case-studies/legal-graphrag-claude-skill-falkordb/).

## What this does and does not tell us

1. A split graph/vector architecture is a real deployment pattern, demonstrated by Lettria and Precina. Our separation of structured relationships and document retrieval is not inherently unusual.
2. The cited teams give practical reasons for choices, including retrieval needs, support, development experience, and latency. This is qualitative evidence, not a measured ranking of providers.
3. Public usage of a product does not prove use of its Community/free edition. None of these case studies establishes that Neo4j Community's security limits, or a competitor's free-edition limits, were overcome without payment.
4. No qualifying medium-team production GraphRAG case for Apache AGE or PostgreSQL plus NetworkX was established in this bounded search. That is an evidence gap, not proof of non-use or technical unsuitability.
5. General graph database customers, tutorial repositories, supported database adapters, and Microsoft GraphRAG framework usage must not be counted as proof of a particular production graph database deployment.
6. Large-company examples cannot answer the medium-company question without evidence of the actual delivery team's size and operating constraints.

## Implication for this project

Use Neo4j as a comparison baseline and Memgraph/FalkorDB as demonstrated alternatives. This is an inference for evaluating options, not an adoption ranking. Keep Apache AGE on a technical-fit shortlist if Cypher within PostgreSQL becomes valuable; the inspected case studies do not establish its market adoption.

The current PostgreSQL plus NetworkX choice remains governed by T02. That decision addressed a small deterministic graph, repeatable evaluation builds, the installed database, and maintenance burden. These case studies do not invalidate it. A future choice should compare the exact edition's read-only enforcement, build isolation, restore path, expected traversal workload, and cost rather than customer-logo counts.

Local context: [T02 research](02-store-and-retrieval-provider.md), [T02 decision](../issues/02-store-and-retrieval-provider.md), and [initiative map](../map.md).
