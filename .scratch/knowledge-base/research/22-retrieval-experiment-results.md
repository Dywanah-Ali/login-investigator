# Small retrieval experiment: results

29 October 2026. Isolated Tier 3 diagnostic, authorized by the author after the experiment
proposal and discussion of retrieval versus investigator-model limitations.

## Main finding

Focused searches can recover missing evidence, and a broad route can recover a need omitted
from the split. But adding the broad route can also push useful focused evidence out of the
final budget. Retrieval quality depends on preserving coverage during selection, as well as
asking useful questions.

For K04, the original whole question still misses the MFA register. Two focused queries keep
both required passages inside the same final twenty-passage cap. Adding the original question
to those queries drops the register again. One prewritten, human-triggered recovery query
restores it. This is evidence for a next design experiment, not an approved production fix.

## Protocol and evidence

- [Frozen protocol](22-retrieval-experiment-protocol.md), saved before live retrieval.
- [Twelve cases and prewritten queries](22-retrieval-experiment-cases.json).
- [Read-only runner](22-retrieval-experiment.py).
- [Initial results](22-retrieval-experiment-20261029T113502902914Z-initial.json).
- [Human recovery decisions](22-retrieval-experiment-recovery-decisions.json), saved between runs.
- [Recovery results](22-retrieval-experiment-20261029T113559311990Z-recovery.json).

Seven existing document questions and five fresh variations were tested. The latter use a
familiar corpus and familiar component evidence. They are exploratory cases, not an independent
held-out set. Queries, expected passages and merger were fixed before running; none was changed
after the results. K03's graph-only question was excluded. K04 here measures only its document
needs, not its graph or generated answer.

Each query uses the unchanged search with twenty results per leg and twenty after within-query
fusion. Across queries, the experiment uses equal-weight reciprocal rank fusion with k=60,
ties by chunk ID, and twenty final unique passages. The merger does not read gold. The offline
scorer reads gold only after selection. This cross-query merger is experimental and does not
change the application's existing single-query fusion.

## Results by case

“Yes” means all predeclared required passages are in the final twenty. It does not mean an
agent answered correctly. “Unresolved” is a human assessment of a known absent topic, not an
automatic refusal result. The final column carries forward the broad-arm result when no retry
was requested.

| Case | Evidence sought | Whole question | Focused | Focused + broad | After human recovery |
| --- | --- | --- | --- | --- | --- |
| K01 | Current password length | Yes | Yes | Yes | Yes; no retry |
| K02 | MFA exceptions and approval | Yes | Yes | Yes | Yes; no retry |
| K04 | MFA context and spray procedure | No | Yes | No | Yes; one retry |
| K05 | Absent retention policy | Unresolved | Unresolved | Unresolved | Unresolved; one retry |
| K06 | Absent internal incident write-up | Unresolved | Unresolved | Unresolved | Unresolved; one retry |
| K07 | Maya's approved travel | Yes | Yes | Yes | Yes; no retry |
| K08 | James's laptop handover | Yes | Yes | Yes | Yes; no retry |
| N01 | Maya travel plus Oliver reset timeline | Yes | Yes | Yes | Yes; no retry |
| N02 | James handover plus current password length | No | Yes | Yes | Yes; no retry |
| N03 | Maya travel plus James handover; device need deliberately omitted from split | Yes | No | Yes | Yes; no retry |
| N04 | Evidence to challenge alleged Hannah MFA exemption, plus password length | Yes | Yes | Yes | Yes; no retry |
| N05 | Evidence showing October travel approval does not cover May | Yes | Yes | Yes | Yes; no retry |

Ten cases have positive evidence targets. Whole-question search covers 8/10, focused search
9/10, and focused plus broad 9/10, with different misses. The human-reviewed recovery variant
covers 10/10. The two absent-topic cases are excluded from this denominator, not passed because
their gold lists are empty. These small exploratory counts do not estimate production accuracy.

### Why K04 regressed when the broad route was added

| Required passage | Whole question | Focused | Focused + broad | With one recovery |
| --- | --- | --- | --- | --- |
| MFA register | Missing | 16 | Missing; 25 before cap | 4 |
| Spray response steps | 9 | 4 | 3 | 3 |

The neutral MFA query finds the register. However, repeated spray-related passages receive
contributions from more than one route. Equal-weight cross-query fusion ranks those above the
register, which appears in only one initial route. The broad route therefore removes evidence
that focused retrieval already recovered. This is a selection failure after retrieval, in
addition to the original whole-question candidate failure.

The recovery query was predeclared as `amelia.ward MFA requirements and approved exceptions`.
A human selected it after seeing the missing MFA evidence. That selection uses knowledge of
the expected evidence. It is not proof that an automatic planner or coverage checker would
recognize the same gap. The register establishes exception context, not who used the account.

### What the omitted-need and negative cases establish

In N03 the focused plan intentionally searches only Maya's travel. It misses James's handover.
Adding the original question brings the handover into the final list at rank 14, while retaining
travel evidence at rank 2. This demonstrates one useful broad-route rescue, not complete
protection against all planner omissions.

K05 and K06 continue returning `weak` / `not_calibrated` on every route, including recovery.
The retention retry returns account-use material; the incident retry returns ATT&CK material.
Neither supplies the requested absent organizational record. The experiment stops after its
single permitted retry and records the unresolved need. No calibrated automatic abstention
or answer generation was tested. T39 and B-099 remain unchanged.

N04 retrieves the complete current register, which lists Daniel and Amelia, not Hannah. N05
retrieves the approval explicitly covering October, not May. Those are passages an investigator
could use to challenge the questions. This experiment does not show that the current or a
stronger agent model actually does so. The October notice also cannot prove that no other
historical May approval ever existed.

## Work and cost

All arms have the same final twenty-passage limit. They do not have the same retrieval work or
context-token count. No answer model receives the passages in this experiment.

| Arm, across twelve cases | Logical searches | Query embedding tokens | Candidate occurrences before cross-query fusion | Sum of observed search seconds |
| --- | --- | --- | --- | --- |
| Whole question | 12 | 292 | 241 | 7.714 |
| Focused | 16 | 226 | 323 | 9.035 |
| Focused + broad | 28 | 518 | 564 | 16.749 |
| Broad arm + selected human recovery | 31 | 540 | 624 | 18.711 |

Candidate occurrences are per-query fused candidates before the query's final cut, counted
again when a different query retrieves them. They are not unique corpus documents or all
database rows examined. Searches were serial and identical strings were cached across arms
and cases. The time sums reuse those observed durations and are not independently measured
production latency or throughput. A matched-total-work comparison remains future work.

Actual physical calls: 26 initial embeddings, 491 tokens, $0.00000982; three recovery embeddings,
22 tokens, $0.00000044. Total: **29 calls, 513 tokens, $0.00001026**. Query caching explains why
physical calls differ from arm totals. These are embedding-provider receipts, not total system
operating cost.

## Verification and boundaries

Preflight passed before each live run: all declared gold IDs exist, IDs and planned needs are
valid, and deterministic fusion, deduplication and the twenty-passage cap hold on synthetic
lists. Both live commands exited zero. The read-only core checked graph integrity on opening.

An independent offline recomputation from saved raw candidates confirmed every final list and
coverage score, all per-leg and final limits, unchanged manifest/runner/original-eval hashes,
unchanged initial query records in the recovery artifact, and exactly three additional queries.
The dataset fingerprint matched before and after each run. Whitespace validation passed.
No application code, original eval questions, corpus, source thresholds or model settings changed.
The application test suites were not rerun for this isolated diagnostic.

The original K04 direct-retrieval gate remains failed. B-098/AUD-062 stays open. No result is
claimed for reranking into the five passages the future tool will show the model. All experiment
work remains local; nothing has been pushed.

## Proposed next decisions

The next retrieval design should test preserving space for each evidence need when merging
focused and broad routes. Simply appending more queries is not enough. This proposal requires
its own frozen comparison; no allocation rule or threshold is selected here.

The investigator-model comparison remains separate. Use the same evidence packet and tasks
for each candidate to measure judgment, including false premises, wrong dates and missing
evidence. Then evaluate tool selection and follow-up separately when the knowledge-base tools
are available. T24/T26 are not built yet, so the present app cannot support a genuine end-to-end
comparison of model-driven knowledge-base investigation. No replacement model has been selected.
