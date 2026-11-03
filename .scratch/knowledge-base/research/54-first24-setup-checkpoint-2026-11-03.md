# T54: first screening round, 24-answer setup checkpoint

Date: 3 November 2026. Author approved the first 24 paid screening answers, inspecting
the first answer before continuing. All 24 final answers are saved. The runner stopped at
slot 24; rounds 2 and 3 have not started. There are 48 scheduled answers remaining.

## Captured evidence

| Item | Result |
|---|---|
| Cases | O1-02, O1-06, O1-09, O1-12-D; six answers each |
| Design | A, one investigator; frozen evidence; no tools |
| Completed trials | 24 of 72 scheduled; no manual reruns |
| Requests | 27: 24 completions, two HTTP 429 rejections, one elapsed timeout |
| Retries | Three, under the unchanged approved policy |
| Wall time | 1162.393 seconds, about 19 minutes 22 seconds |
| Screening known charge | US$0.107868, including the reconciled timeout charge |
| Combined known charge | US$0.111008, including both compatibility bundles |
| Raw missing charges | Two screening rejections; five including compatibility |
| Human labels and selection | All unscored; no selection |
| Live Langfuse upload | None |

The first answer's input/prompt/route/recording/reference check passed before slots 2–24.
All 24 trials use fresh memory IDs and the frozen case inputs, investigator prompt,
provider pins, reasoning/sampling settings, standard service and no fallback. Gold was not
sent to models. Requests have no tools, upstream diagnostics or evaluation-imposed output cap.
Package source and case hashes still match the manifest. Configured credentials are absent
from the bundle. The initial checkpoint verified 151 artifact references and all 27 request
terminal records. No application tests were repeated for this isolated operation.

Manifest: prompt `28b2667c34b4`, fixture `f903b7f47620`, adapter `openrouter/2`.
Authoritative bundle: `backend/evals/comparison/runs/screen-live/` (git-ignored).
[Machine-readable setup evidence](54-first24-setup-evidence.json) preserves counts and checks.

## Request failures and billing

One trial encountered two upstream capacity rejections and one request timeout, then completed
within its case allowance on retry. All attempts and available partial output are retained.
The timeout's original generation ID supported an authenticated, read-only metadata lookup.
OpenRouter reported `total_cost: 0.000426477`, `finish_reason: stop` and `cancelled: false`.
An append-only `cost_settled` event attaches that charge to the same request after the runner
stopped. No inference was repeated for reconciliation, and the charge is counted once.
Missing streamed usage remains unknown; native billing metadata is retained separately.

Both HTTP 429 responses identify `engine_overloaded` and have no generation ID or usage.
They have published-policy nonbilling dispositions, but their missing numeric charges have
not been replaced with invented zeroes. Combined charges remain a known subtotal, not a full
account-invoice reconciliation. The US$15 known-spending checkpoint was not reached.
B-152 records the operational observation; the location/cause of the timeout delay is unproven.

## New citation-checker gap, B-153 / AUD-080

All 24 answers have a saved version-1 reference check. No recognized reference is unresolved.
One answer has zero recognized references because it uses spaced/grouped/ranged citations
such as `[ D1 ]`, `[ A1 ; A2 ]` and `[ L1‑L20 ; L21 ; C1 ]`.
This is not evidence that it has no citations or that its content fails the rubric.

The checker currently recognizes only a single tightly bracketed reference such as `[D1]`.
An offline probe reproduces that `[D999]` flags a nonexistent reference while `[ D999 ]` and
`[D1; D999]` are silently skipped. Therefore zero unresolved references does not establish
complete citation coverage. See the [saved lexical probe](54-citation-parser-probe.json).

No parser, prompt, rubric, gold or answer was changed, and no answer was rerun to improve it.
Proposed next step: define the supported spaced/grouped/ranged citation grammar, repair this
deterministic parser under a new check version, then recheck saved answers locally. This
needs no paid inference and does not require altering the model answers or human scores.
Keep version-1 checks as history. Resolve this before treating citation checks as complete.

## Prepared review and next gate

Blinded batch 1 contains six shuffled answers and the agreed assessor anchors, with a blank
label sheet. Candidate/design identity, cost, timing and trace are hidden. The existing
self-identification check reports no blinding limitation in these six items. No initial
human score or assistant quality suggestion has been entered.

- Batch: `backend/evals/comparison/runs/screen-live/artifacts/review/batch-1.json`
- Blank labels: `backend/evals/comparison/runs/screen-live/artifacts/review/labels-batch-1.json`
- Keep the operator evidence, identity map and Langfuse views separate from initial blind scoring.

T54 remains claimed. Two rounds of 24 remain, with model selection only after all three
rounds and the agreed human scoring. The parser gap is open at the setup checkpoint; no
later-pass execution, model selection or live upload has been authorised by this first-round go.

## Author-approved local parser repair, 3 November 2026

The author approved the proposed repair in the next session. `reference-resolution/2`
accepts whitespace, comma/semicolon groups, and ascending same-prefix ranges with full
endpoints. Range separators: ASCII hyphen, Unicode hyphen, nonbreaking hyphen, en dash,
and minus. A range expands at most 1000 references, with endpoint numbers of at most nine
digits and no zero padding. Reversed, mixed-prefix, larger, padded or otherwise unsupported
reference-like groups retain their explicit references and an `unsupported_citations` warning.
Ordinary bracketed prose without a reference-shaped token is ignored. Unbracketed citations,
other bracket alphabets, nested or unmatched brackets are outside this grammar. This is a
bounded lexical check, not a universal citation detector or an entailment judgement.
`citation_count` now counts expanded reference occurrences, including repeats. It is not a
quality score and is not directly comparable to the old single-reference count.

Local recheck appended exactly 24 v2 checks. All 24 v1 checks and the original 135-event
prefix are unchanged. All 152 other bundle files, including answers, manifest and blinded
review/labels, hash-match their baseline. Repeating the recheck appends nothing. Thirteen
answers have newly recognized references, including the former zero-reference answer,
which now has 37 reference occurrences. No detected reference is unresolved.

Two answers have five reference-like brackets containing explanatory prose, for example
`[S4 unavailable]`. V2 retains/checks the explicit status references and flags these groups
rather than treating them as fully supported grammar. All their explicit references exist.
This observation assigns no human score and does not establish source support. Retain these
warnings at the checkpoint. Any future mirror's unresolved-reference metric alone still
cannot establish complete syntax coverage; consult local v2 checks alongside that metric.

Verification: initial assessment file run 53 passed in 48.09 seconds; after adding the exact
live-form regression and strengthening the history test, both affected tests passed in
3.01 seconds. New command-warning test passed in 0.60 seconds. These cover all 55 current
assessment tests. Focused Ruff and Pyright on assessment, command entry point and tests are
clean. One import-order lint failure during the command-test addition was corrected and
rerun clean. No application suite needed for this isolated evaluation repair.

[Version-2 evidence](54-citation-parser-v2-evidence.json) retains counts, lexical deltas,
original-prefix digest and original/current package hashes. The frozen manifest is not
rewritten: the package hash now differs because the parser and local-check command changed.
Disclose this check-only source change at any later setup review; no model-execution,
prompt, fixture, rubric, gold, settings or adapter change was made here.

The admin manual's live `checks` command ran successfully and again with zero new checks.
No paid inference, labels, selection or live upload occurred. T54 remains claimed. B-153's
bounded repair is verified; AUD-080 remains open for author checkpoint disposition, with
the two explicit syntax warnings and grammar limits retained. Later-round paid execution
still requires its separate go.

## Final three-round collection and housekeeping, 3 November 2026

After the bounded parser repair and checkpoint summary, the author explicitly authorised
original slots 25–72. They then requested stopping after round 3 and housekeeping, with
blinded human scoring in a fresh session. “Round 4” was clarified as that review stage;
there is no fourth paid screening round. No extra answers or paid repairs were authorised.

| Item | Final result |
|---|---|
| Original scheduled trials | All 72 closed; 71 completed with answers, one `no_answer` |
| Answers by round | 24, 24, 23 |
| Case coverage | 18 trials per case; one has an explicit absence |
| Later-round wall time | 2847.102 seconds, 47 minutes 27 seconds |
| Screening requests | 96; 72 completed transports, 21 errors, three request timeouts |
| Error classification | 20 HTTP 429 capacity rejections; one streamed `rate_limit_exceeded` |
| Retries | 24 total; 21 added in rounds 2–3, within unchanged policy |
| Screening known charge | US$0.278057 |
| Combined known charge | US$0.281197, including both compatibility bundles |
| Missing numeric charges | 22 screening requests; 25 including compatibility |
| Streamed usage unknown | 25 screening requests; not filled from billing metadata |
| Reference checks | All 71 answers checked with v2; zero unresolved references |
| Unsupported syntax | Eight answers retain warnings; these are not scores |
| Original evidence | 159-event pre-continuation prefix and all 152 original files preserved |
| Final artifact verification | 485 event artifact references hash-match |
| Setup | 72 fresh memories; frozen inputs, prompts, provider pins and wire settings match |
| Human scoring, selection, live upload | None; batch 1 and its blank labels unchanged |

Authoritative [final machine evidence](54-complete-screen-evidence.json) records counts,
request failures, resource limits and checks. The runner exited 0 at slot 72. No linked
rerun was scheduled. The paid command used both compatibility cost bundles and
`--after-setup-review`, with no spending-review override. Known spending never reached US$15.
The source change remains the reviewed parser/command-only change recorded with v2;
original manifest and model-execution source/settings are preserved.

**Empty response, B-155/AUD-081:** slot 64 returned a completed response with no answer
text, empty continuation output, no streamed usage/cost and a generation ID after ten
HTTP 429 rejections. Trial status is `no_answer`, elapsed 310.588 seconds. An authenticated
metadata lookup returned 404. This does not establish zero charge or the responsible layer.
No automatic replacement, model blame, model elimination or quality score is justified.
Retain the absence under the approved scoring/selection rules; any proposed technical repair
would need evidence, its own disposition and explicit execution authority.

**Billing:** four authenticated read-only generation lookups ran after the runner stopped.
Two timed-out generations returned charges US$0.002126992 and US$0.001812412, each with
`cancelled: true` and null finish fields. Exactly two new `cost_settled` events attach those
receipts once. The empty response and one streamed rate-limit failure returned 404; their
charges remain unknown. Remaining missing numeric charges are the 20 HTTP 429 requests.
Compatibility adds three further unknown numeric charges. Do not replace absent values
with invented zeroes or treat the subtotal as invoice reconciliation. The billing receipt is
`screen-live/artifacts/billing/later-rounds-generation-metadata.json`, linked by both new
settlements. Streamed usage stays unchanged. The streamed failure is recorded with synthetic
`HTTP 0` text and a raw `rate_limit_exceeded` body; this is not a real HTTP status 0.
B-152 retains these operational observations.

**Documentation and iterations:** B-154 records the corrected manual example that omitted
the compatibility repair's cost context; the corrected command was used successfully.
The initial sandboxed launch failed on uv cache access before dispatch and was retried with
authorised network/cache access. A temporary monitor initially lacked the project import
path; setting `PYTHONPATH=.` fixed the helper without changing application code. No application
suite, provider/prompt/fixture/gold change, commit or push occurred in this collection step.

**Stop point:** preserve batch 1's six blinded answers and blank labels. Start initial human
scoring in the fresh session. No assistant quality suggestions before those initial labels;
no model winner, architecture calibration or Langfuse upload has been authorised here.
T54 stays claimed. AUD-080 closes for the bounded parser repair/checkpoint disposition;
AUD-081 stays open for the unexplained empty response. Prior graph concerns remain separate.

Final stop checks: status confirms all 72 original trials closed; repeat offline checks
append zero. Configured credential values are absent from all 463 bundle files. Final
`git diff --check` passes. The fixed session handoff is saved; its dated backup is offered
separately and requires the author's choice. No process remains owned by this session.
