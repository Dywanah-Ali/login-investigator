# T52 saved evidence inventory

Inspected 2 November 2026 by Codex. Read-only source and saved-result inspection for
the objective-to-evidence mapping. No model calls, service checks or test reruns.
These are historical observations and present source contracts, not fresh runtime proof.

## Saved results inspected directly

| Evidence | Exact observation | What it establishes and what remains unproved |
|---|---|---|
| [T22 first live retrieval](../../../backend/evals/results/2026-10-29-102711-909238-retrieval-0180733adbd4.json) | 5/8 pass. K04 misses `reg-mfa-exceptions@1.6#mfa-exception-register/active-exceptions/1`; its exact graph records and paths pass. K05 and K06 expect `none` but receive `weak`. | A compound question can lose relevant evidence even when the graph is correct. Does not prove an agent answer or a completed investigation. |
| [T23 first live reranked retrieval](../../../backend/evals/results/2026-10-29-150414-681065-retrieval-0331ac624577.json) | 5/8 pass, with the same three failed questions. K04's response-steps passage is fused rank 9 and first among the retained passages, score 0.5157425. The MFA gold is absent from candidates. K06's highest score is 0.64585793; K05's is 0.106142916. | Reranking promotes a found passage but cannot restore the missing one. These scores alone cannot establish a safe absence threshold. AUD-062/AUD-064 remain open. |
| [T49 Neo4j retrieval regression](../../../backend/evals/results/2026-11-01-103813-673055-retrieval-7d7cff5dcc5c.json) | 5/8 pass: K01/K02/K03/K07/K08 pass, K04/K05/K06 fail. K04 retains 20 candidates and 5 passages. Its walk contains exactly 2 groups, 7 assets and 9 paths, with no missing/extra graph IDs or paths. | Historical exact-set graph evidence and unchanged retrieval limitations. This run precedes T50: its integrity record still contains 141 `used_address` edges. It cannot certify the current graph after their removal. |
| [T49 Port API exam](../../../backend/evals/results/2026-11-01-104006-806272-13987838.json) | 60/63 overall, 15/15 security, no execution errors. Q04 fails 0/3 solely on `flags amelia.ward as possibly compromised (S6)`. All three answers contain 3 successful sign-ins. All required reputation checks pass and the corresponding tool calls are saved. Run 1 recommends securing Amelia; run 2 names other accounts to secure; run 3 recommends monitoring Amelia. | Existing Port gates pass while a particular attribution obligation remains failed. Do not classify every Q04 failure as only a wording/grader defect. These are Port questions, not phase-1 package, retrieval, citation or document-injection proof. AUD-066 remains open. |
| [T24 live lookup](24-live-lookup.json) | Saved question, answer and tool record show `lookup_account(account_id="amelia.ward")`, owner Amelia Ward, department IT, All Staff baseline group and IT Admins privileged group. | One real agent selection and answer using organisation context. No radius, corpus search, complete playbook or saved evidence panel is exercised by this artifact. |

T23's final live result and reranker-off result were also inspected for their labels and
summaries: [final on](../../../backend/evals/results/2026-10-29-151556-711492-retrieval-813793dbc769.json)
and [off](../../../backend/evals/results/2026-10-29-151808-470796-retrieval-69e31e22b772.json)
both report 5/8. Their summary tie is not a completed switch-selection experiment under
the agreed second retrieval check and refusal requirements.

## Current implementation inspected

| Source | Implemented boundary | Consequence for the mapping |
|---|---|---|
| [Tool registry](../../../backend/login_investigator/tools.py), `tools_for` | Registers the three Port tools plus `account_tool`. | The working agent does not yet receive the planned `investigate_alert`, `find_peers` or `search_corpus` tools through this registry. Core functions existing elsewhere do not establish agent integration. |
| [Account adapter](../../../backend/login_investigator/knowledge_tools.py), `account_tool` | Returns short content plus a full artifact; labels snapshot permissions and historical uncertainty; returns unavailable without a knowledge base and not-found for an absent account. | Implemented account evidence seam, with bounded status semantics. Not the proposed complete case-file contract. |
| [Neo4j query implementation](../../../backend/login_investigator/knowledge_base/neo4j_graph.py), `finding_radius` and `_device_peers` | Joins memberships to assets; for spraying/brute-force selects accounts with successful sign-ins from finding addresses inside the period. Device peers require both accounts' device use inside the time bounds. No address-sharing query. | Supports potential permission reach and dated device relationships. These records do not establish actual asset access, actor identity or compromise. Defaults are passed to the existing period helper, not a new T52 automatic investigation-window workflow. |
| [Direct retrieval runner](../../../backend/evals/retrieval.py), `evaluate_retrieval` | Runs integrity, search and named graph requests directly. Saves query, request, search and walk. Execution does not read gold fields. | Separates retrieval from answer generation. Does not test model tool choice or final answer support. |
| [Retrieval scorer](../../../backend/evals/scoring.py), `score_retrieval` | Checks gold chunks against the first 20 saved candidates; checks graph IDs/paths as exact sets; checks expected retrieval verdicts. | No separate check of the retained five is implemented here. A saved candidate or resolving citation is not proof of semantic claim support. |

## Test source and historical measurement boundaries

- [Graph tests](../../../backend/tests/test_knowledge_graph.py) include S6 gold groups,
  assets, device peers and paths; snapshot labelling; absent address context/edges; date
  bounds and out-of-coverage handling. These tests were read, not executed in this review.
  The S6 default case has no device peers, so it is not a positive shared-device witness.
- [Paired lifecycle test source](../../../backend/tests/test_paired_lifecycle.py) contains
  artifact preservation and separate investigation checks. Source assertions establish
  intended regression coverage, not a new passing run.
- [T24 persistence report](24-persistence-evidence.md) records a historical fake-model
  measurement: 601-byte standalone artifact, SQLite sizes 20,480 / 40,960 / 811,008 /
  16,404,480 bytes at 0 / 1 / 10 / 50 lookups, and 0.0181-second reopen preserving 50
  artifacts. This review read the report, not its original disposable database. It does
  not establish full-package storage behaviour, concurrency capacity or the later evidence
  panel. AUD-065 remains deferred under its existing trigger.

## Limits

The inventory is a targeted inspection, not an exhaustive certification. Existing failures
remain recorded with their original scores. No threshold, gold, prompt, data or application
code changed. The four-case T52 screen has no scored runtime evidence in these artifacts.
Its future fixed-evidence results cannot replace live retrieval, tool enforcement, complete
saved/displayed evidence, phase-1 exam or author screen acceptance.
