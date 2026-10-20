# 01: Use-case research for the knowledge base

Type: research
Status: resolved
Blocked by: none

## Question

Which real use case should the Login Investigator's knowledge base serve, so that a knowledge graph
with RAG inside its ecosystem adds context about the threat behind a login pattern, rather than
being a demonstration of RAG?

Author's research go: 20 October 2026. Folder name `knowledge-base` chosen by the author.

## Scope

- Use the Perplexity research tools, then verify material claims against high-trust primary
  sources (vendor documentation, MITRE, NIST, peer-reviewed or well-known practitioner sources).
- Answer four questions:
  1. How do security teams use a knowledge graph around authentication events (identity graphs,
     user and entity behaviour, lateral movement, attack paths)?
  2. What knowledge do analysts reach for when they investigate a login alert (ATT&CK techniques,
     threat-intel reports, runbooks, policies, past incidents)? This is what the RAG part would
     search.
  3. Where does graph traversal win over text search, and where does text search win?
  4. What entities, relationships and text would a credible synthetic dataset need?
- Deliver two or three candidate use cases, each with: the graph (nodes and relationships), the
  text corpus, the questions it answers, the data it needs, and what value it adds to the app.
- Save one cited note at `../research/01-use-case-research.md`.

## Acceptance

- [x] Perplexity result and connection outcome recorded without secrets.
- [x] Material claims verified against primary sources and cited in the research note.
- [x] Two or three candidate use cases documented with graph, corpus, questions, data and value.
- [x] No application, API contract or spec decision changed by the research.
- [ ] Findings presented to the author for a use-case decision before any spec is written.

## Comments

## Answer

Research completed on 20 October 2026. Evidence:
[01-use-case-research.md](../research/01-use-case-research.md).
One Perplexity deep-research call succeeded (about 4 minutes) and seven domain-restricted search
calls verified the load-bearing claims against Microsoft Sentinel, Splunk ES, BloodHound, MITRE
ATT&CK and Neo4j GraphRAG documentation. Claims not opened directly are marked [V] in the note.
No application, contract or spec change was made.

Findings: security products keep durable relationships in a graph (accounts, groups, grants,
assets, networks, incidents) and leave the event log as the source of truth. Analysts reach for
ATT&CK text, runbooks, policies and past incidents, which suit hybrid text search, and for
ownership, access and approval facts, which suit graph lookup and traversal. Neo4j's GraphRAG
package ships the hybrid-then-traverse shape directly. No public dataset pairs logins with
organisational context, so the project generates its own small consistent set.

Three candidate slices of one knowledge base are documented: (1) explained new-country sign-in,
(2) spray-to-compromise blast radius, (3) privileged and service-account triage. Recommendation:
start with candidate 2 and fold in candidate 1's network and travel facts. The choice is the
author's and precedes any spec.
