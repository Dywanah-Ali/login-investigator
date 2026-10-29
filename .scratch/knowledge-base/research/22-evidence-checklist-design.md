# Evidence checklist and selection: proposed design

29 October 2026. Tier 3 design exploration. The author asked to work on tracking evidence needs
and preserving support before comparing investigator models. This note proposes a design;
it does not amend the spec, start T23/T26, or approve an application implementation.

## Principle

Keep the question being investigated attached to its evidence throughout the process.
Focused search and recovery are two attempts to satisfy the same need. A new search should
not erase earlier candidates or silently give that need a larger share of the final answer.

There are three separate facts to track:

1. We retrieved a passage while searching for this need.
2. A reviewer judged that the passage supports, challenges or fails to resolve the need.
3. The passage survived selection into the evidence actually shown to the investigator.

Only the first and third are directly observable bookkeeping. The second requires judgment
about the passage's contents and applicability. Search rank alone cannot establish it.

## One checklist, two kinds of work

For K04, the full investigation needs account reach, MFA context and the response procedure.
Account reach uses graph results; the latter two use documents. The previous experiments
tested only the document portion. A broad discovery route also looks for overlooked needs.

| Need | Retrieved material | Review must establish | If selected evidence is inadequate |
| --- | --- | --- | --- |
| Account reach | Membership and asset paths | Identity, relationship meaning and available snapshot/period | Identify missing graph data; do not replace it with generic documents |
| MFA context | MFA register, policy and relevant records | Named account, applicable period, approval versus actual authentication behavior | Revisit stored candidates first; then one bounded targeted search if still needed |
| Response procedure | Spray runbook | Applicable procedure and the relevant steps | Select the relevant saved passage or search again if it was never retrieved |
| Broad discovery | Candidates from the original question or finding-derived broad query | Whether something useful lies outside the planned checklist | Propose a new need explicitly; do not mark the existing plan complete merely because its own entries are filled |

The register supports approved-exception context. It does not prove who performed the sign-ins
or that a configuration was applied correctly at the event time. Broad discovery is a search
route, not a required evidence need that can be marked answered.

## Proposed flow

1. Establish mandatory needs from the agreed finding-driven playbook. Retain each need's
   identity, scope and source requirements. Additional model-proposed needs require a separate
   ownership decision under T05/T26.
2. Search each planned need. Store all bounded candidates with the queries and routes that
   retrieved them. Store a passage once and preserve all its associations. Broad-route findings
   stay available for review rather than being forced into a possibly incomplete checklist.
3. Review whether candidates actually address the needs. For an initial prototype, make this
   human review explicit. A future model assessment must cite existing passage IDs and state
   what the passage supports or challenges. Code checks ID existence and scope metadata; it
   cannot certify semantic truth just by validating the shape of the assessment.
4. Select a compact packet while preserving reviewed support for each need and material
   contradictions. One passage may support multiple needs. Keep a trace of what was excluded.
   If the support cannot fit, report the capacity gap rather than silently dropping a need or
   exceeding the agreed cap. The exact selection policy is still a decision to test.
5. Recheck coverage of the actual selected packet. If the needed support was retrieved but
   excluded, repair selection using the existing pool before issuing a new search. If the
   stored candidates do not answer the need, try a bounded alternative query or authorized
   source. Reassess the resulting evidence; a completed retry is not a completed need.
6. Stop with the support, contradictions and remaining gaps visible. Missing retrieved support
   is not proof that a fact does not exist. T39's calibrated search verdict remains separate.

Reviewed support may be revised when newer or contradictory evidence arrives. Preservation
must not permanently lock in an incorrect assessment or suppress contradictions. A claim that
is narrowed or rejected needs evidence too, as the false-premise and wrong-period cases show.

## Small interface, internal bookkeeping

Proposed module: assemble evidence for a finite investigation plan. The caller supplies the
plan, authorized scope and resource budget. The module returns the selected evidence, its
source references, per-need review records and unresolved gaps. Retrieval, caching, selection
and bounded recovery stay inside this module rather than being duplicated across tools.
This is a proposed interface, not an implemented contract or new agent tool.

Internally keep three independent dimensions rather than one misleading `done` flag:

| Dimension | Suggested information |
| --- | --- |
| Retrieval | Queries attempted, source failures, candidate IDs, source/version metadata |
| Assessment | Unreviewed, supported, partial, conflicting or unsupported; reviewer and cited passage IDs; statement being supported |
| Selection | Which reviewed passages were selected; which were excluded; which needs no longer have their support in the packet |

These labels are design vocabulary only, not replacements for `weak`, `found` or `none`.
The reason for stopping is recorded independently: work complete, missing data, failed source,
retry limit or resource limit. A failure to access a source must not look like a successful
search with no support.

Recovery stays attached to its original need. Multiple retries must not become multiple
independent voting routes that overwhelm other needs. Code enforces total query, candidate,
time and context limits and keeps entity/time/access scope intact. If there are more needs
than the packet can represent, return explicit partial coverage or use a separately approved
staged investigation; do not silently enlarge the final context.

For the current scope, T26 still constructs searches from finding records, not raw chat.
Direct free-form `search_corpus` is a separate interface and its original K04 gate is unchanged.
T23's twenty-to-five reranker and T26's five-per-search package caps remain authoritative.
A shared need-aware selection stage or semantic assessment stage would need an agreed spec
and ticket change before application code. No new library or provider is needed to replay the
candidate-selection question.

## Offline selection replay

The [script](22-evidence-selection-replay.py) uses only the Python standard library and the
saved initial candidate lists from the previous experiment. It makes no search, embedding,
reranker or investigator-model calls. [Raw results](22-evidence-selection-replay.json).

The alternative gives each focused route and the broad route one new unique passage per
round until the cap is reached. Duplicate passages do not occupy multiple slots. Routes follow
the manifest's focused-need order, then the broad route. Every route-order permutation is also
reported; none was selected afterwards as a preferred winner. Gold is used only after
selection for offline scoring. N03's omitted need remains absent from the checklist.

This is a development replay designed after observing the first experiment. It is not a
new held-out evaluation or evidence that automatic support assessment works. Fair allocation
among query routes is not semantic coverage of evidence needs.

| Observation | Result |
| --- | --- |
| Previous focused+broad RRF at twenty passages | All gold in 9/10 positive-target cases |
| Fair turns, declared route order, twenty passages | All gold in 10/10 positive-target cases |
| K04 with fair turns at twenty | MFA register rank 19; runbook rank 2; no recovery query |
| K04 route-order sensitivity | Passes in four of six orders; fails in two |
| N03 omitted-device case, fair turns at twenty | Travel rank 2; handover rank 10; both route orders pass |
| Fair turns at five, declared route order | All gold in 8/10 positive-target cases; K04 and N03 miss one need |
| Two absent-topic cases | Unscored for positive coverage; no support assessment or refusal claim |

The five-passage run is a stress check on this simple selector, not a test or prediction of
Cohere's T23 reranker. Different packet lengths also have different context-token totals.

Mechanism checks passed for overlaps, empty routes, exhaustion, zero budget, deduplication and
hard caps. Input manifest hash matches the original run. The artifact records input/script
hashes and all selected IDs. No query, original gold, previous result, app code or model setting
changed. The scripts make no external calls; additional provider cost is zero.

## What we can decide from this

The saved pool already contains enough evidence for K04. We can therefore separate selection
repair from retrieval recovery and avoid requiring an additional search just to compensate
for a dropped passage. This is demonstrated for candidate selection only.

Do not adopt simple equal turns as the final design. K04 sits near the cutoff, depends on
route order, and fails under the tighter stress budget. The useful design direction is the
checklist and explicit coverage review, not this particular allocation formula.

Next design step: agree who reviews candidate support and how that review is represented.
A small human-labelled set can test retaining supporting and conflicting passages under the
actual output cap. It must include incorrect and incomplete assessments to avoid treating a
reviewer's labels as an oracle. Later compare model reviewers on the same evidence, separately
from their search planning. Those steps remain proposals; no semantic checker is built here.
