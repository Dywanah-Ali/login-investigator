# T52: Proposed trial and architecture decision protocol

> **Superseding author ruling, 4 November 2026:** Codex assesses all 71 saved
> screening answers as the primary assistant assessor. Initial human scoring is waived
> for this screen. Preserve blinded identities, frozen anchors, per-score evidence/reasons
> and revisions. Use `assessor_type=assistant`; do not claim human validation. Existing
> human-only selection/mirror consumers remain separate. Later stages/T30 are unchanged.
> Historical author-first instructions below record the earlier procedure.

Date: 2 November 2026. Status: staged comparison plan.
The A/B/C comparison structure, common rubric and 12-answer calibration stage are agreed.
The author approved calibration first on 2 November. The 189-answer exploratory stage,
eligibility rules, budgets and implementation details remain proposals.

## Familiarisation scope correction — 4 November 2026

**Author scope correction, 4 November 2026:** pre-live model comparison is temporary,
ad hoc model-selection work, possibly repeated once after tools are built. It is not a
routine operational task. The current comparison upload is solely for the author to learn
Langfuse. Use the existing connector with only the minimum changes needed to display it
truthfully. Do not build automated remote read-back/reconciliation, a permanent comparison
operations workflow, or a staged pilot/control framework for this exercise. Simple author
inspection in Langfuse is sufficient for the learning objective. Formal comparison-upload
reconciliation requirements are superseded for this exercise. Real operational Langfuse
tracing/evaluations come later with the fully implemented running v2 app under T29/T30/T31;
their acceptance is neither designed nor satisfied by this familiarisation upload. Preserve
existing evidence, truthful assistant provenance and secret filtering. Luna/Sol shortlist
and deferred tier-matched challengers remain. Historical findings stay recorded without
becoming mandatory engineering work for this learning step.

## Author shortlist ruling — 4 November 2026

The current shortlist is **GPT-6 Luna and GPT-6.1 Sol**, representing two separate
comparison tiers. The author chose to retain both after reviewing quality and observed
cost differences. This is a shortlist decision, not permanent adoption or a claim that
both passed the completed screen. Luna's two zero-bearing answers and all original
scores remain unchanged; Sol alone meets the original numerical screening rule under
the assistant assessment. No threshold or gold is weakened retroactively.

After the tools are built, assess four direct challengers, matched to these tiers:

| Comparison tier | OpenAI shortlist | Anthropic challenger | Open-source challenger |
|---|---|---|---|
| GPT-6 Luna tier | GPT-6 Luna | One direct challenger, to be selected later | One direct challenger, to be selected later |
| GPT-6.1 Sol tier | GPT-6.1 Sol | One direct challenger, to be selected later | One direct challenger, to be selected later |

There are two Anthropic and two open-source candidates in total. Select direct challengers
within each respective tier rather than treating a mixed-tier result as a capability-matched
contest. Exact models, versions, providers, tier-fit evidence and the later assessment setup
remain to be agreed when the tools are ready. The four challengers are not selected now.
The later assessment should exercise the built tools; the completed fixed-evidence screen
remains historical evidence and is not reclassified as a tool-enabled test.

No single A/B/C baseline is selected by this ruling. The previous single-model-selection
step remains pending, with this two-model shortlist now the author-approved direction.
No additional inference, model change, paid run, architecture calibration or live upload
is authorised by this planning decision. Existing later-stage execution decisions remain.

## Approved delivery order

Author approved on 2 November 2026: finish T52, then T54 builds the isolated comparison
runner and Langfuse recording together, under
[T52's nine-group record contract](../issues/52-agent-objectives-and-reliability-review.md#approved-runner-ownership-and-record-contract--2-november-2026).
Local runner/fake-model checks precede the mirror/fake-destination checks, then authorised
compatibility sessions and screening. A genuine scored screening result mirrored and
inspected by the author can satisfy T54's live integration criterion. Later instrumented
twelve-answer A/B/C calibration reuses the runner after provisional-model selection and
its separate execution decisions. T29/T30/T31 retain the full application exams, advisory
judge and application/full-exam tracing. Local files remain authoritative, with save-before-
upload, masking, explicit label export and separate blinded answer/process review.
Screening policies below are agreed; fixture/scoring readiness and T52 closure remain open.

See [T54](../issues/54-early-langfuse-evaluation-integration.md).

## Screening assessors approved, 2 November 2026

The author is the primary human scorer. Codex prepares blinded case evidence and answers,
records the six-criterion labels and critical-error flags, and runs deterministic checks.
Save initial human labels before Codex discusses inconsistencies or suggests score changes.
Preserve revisions and their reasons; the author owns the final human label. Code checks
do not replace semantic assessment. Review in small batches and measure effort from the
first batch rather than assuming a review duration. All produced answers need review;
partial/no-answer outcomes follow the existing distinct accounting.

No second human or paid model judge is required for this initial screen. Codex assistance
does not establish independent human agreement. Blinded views continue to hide candidate
identity, settings, cost, timing and revealing traces. Later architecture-stage assessor
arrangements are separate; its earlier suggestions below are not extra screening requirements.

## Stage 1: calibrate the scoring and runner (author agreed)

### Provisional-model selection for this stage — approved 2 November 2026

Finish all three screening passes before selecting. A configuration is eligible only when
all twelve scheduled trials complete, no designated critical error occurs and no applicable
criterion scores 0. Scores of 1 are allowed; N/A is distinct from zero and unscored is not
passing. Partial answers from incomplete/timed-out trials remain evidence but do not make
those trials complete.

Compare eligible configurations' criterion profiles case by case. Prefer consistently
complete answers over repeated partial answers. For similar quality choose the cheaper
configuration, then use speed as the next deciding factor. Preserve the author's selection
rationale rather than inventing a weighted score. If none qualifies, diagnose the failures;
do not advance the least-bad model automatically or weaken expected outcomes. Setup repairs
follow the existing affected-comparison rerun policy; ordinary model failures stay visible.

This chooses a provisional A/B/C model, not a permanent winner or a reliability certificate.

### Twelve-answer architecture calibration

Use O1-02 (matching travel), O1-06 (partial explanation), O1-09 (missing history) and
O1-12-D (document injection), once per architecture: 4 × 3 = 12 final answers.
Blind architecture labels, randomise review order and review against the frozen rubric.
Have the author and a second human assessor score independently if available. If no second
human is available, record that limitation and use the advisory model to surface disputes,
not as a falsely independent human ground truth. Agree feasible assessor arrangements first.

Resolve ambiguous criteria, verify output/source trace preservation and check cost/latency
before expanding. These calibration outputs are not promotion evidence. If their scores
inform prompt, fixture or rubric changes, they remain development data. No calibration
score is evidence of statistically reliable superiority.

## Stage 2: exploratory diagnostic comparison

Freeze the reviewed 21 diagnostic examples, prompts, role contracts and rubric. Run each
example three times under each architecture: 21 × 3 × 3 = 189 final answers. The calibration
12 are separate, so these two proposed stages produce 201 final answers in total. These are
not model-call counts: specialists and retries create additional calls/tokens.

Three repetitions are a proposed economical starting point for observing instability, not
a sample size derived to certify a low error rate. Keep every attempt, no-answer and retry.
Do not count variants or repetitions as new independent incident families. Interleave candidate
execution order and record model identifiers/settings, evidence hashes, time and provider
behaviour so drift is not silently attributed to architecture.

No prompt tuning during a scored run. Changes create a new version and rerun affected
comparisons for all candidates. Reset investigation memory, preserve complete input/output
artifacts and separate transient runner failure from a correct partial answer about failed tools.
An equal-input comparison measures whole-configuration value. Extra compute is a confound:
before attributing an improvement to specialised roles, compare against an appropriately
budgeted extra-pass single-investigator control. That control is a proposed follow-up, not an
already approved fourth architecture or change to A/B/C.

## Proposed decision after exploratory runs

- Diagnose case-level improvements/regressions and trace specialist-to-front-agent losses.
  Do not select an architecture from a grand average or one attractive answer.
- A specialist is worth taking to confirmation when it repeatedly fixes consequential
  assessment failures or required evidence omissions, with a clear mechanism visible in the
  trace. Better phrasing alone is not enough. Critical-error flags cannot be averaged away.
- If results are tied or inconclusive, retain the current single-agent baseline for planning
  and leave specialist adoption unresolved. This does not certify the baseline's reliability.
- If all candidates fail required outcomes, fix the identified evidence/workflow/model issue;
  do not weaken expected answers or promote the least bad candidate as compliant.
- Proposed repetitions for confirmation depend on observed variation, error severity and
  genuinely independent held-out coverage. Set and freeze them before confirmation runs.
  A fixed count cannot responsibly be chosen as a reliability guarantee before those inputs.

## Proposed permanent-adoption conditions

Before a design ruling, require a separate, author-approved confirmation plan with unseen
case families/variants and realistic 50-person/30-day background evidence. The scenarios
designed in this session are development material, not held-out proof.

Proposed conditions to decide before those runs:

1. No designated critical errors observed in the confirmation suite. This is an observed
   acceptance condition, never a claim of zero real-world risk. Preserve every failed result.
2. All case-required semantic findings and scope/security obligations meet predeclared
   case-specific acceptance rules. The 0/1/2 profiles are diagnostic; exact allowed omissions
   and aggregate acceptance thresholds still need an explicit author ruling.
3. The specialist supplies a repeatable, consequential benefit against the baseline without
   introducing unacceptable regressions. Review paired case-level results and uncertainty,
   not only percentages. Do not claim statistical superiority without an adequate design.
4. Measured latency and cost fit author-approved budgets fixed before confirmation. No budget
   amount or expected price is invented here. The calibration run supplies estimates for review.
5. Required collection/retrieval, scope-approval, save/reopen and injection-boundary tests pass
   end to end. Fixed-case reasoning does not waive existing retrieval gaps or later phase gates.
6. The chosen design is reconciled with the spec, tickets and advisory judge policy before
   permanent implementation. Evaluate a combined-specialist variant only if individual value
   justifies that additional comparison; combinations are not automatically additive.

## Model research update, 2 November 2026

Author requested a broad shortlist including cheaper/faster open-weight candidates. Published
security-specific evidence is not an entry requirement. The proposed model-screening step in
[screening evidence](52-model-screening-evidence.md) would precede freezing the A/B/C model;
its counts, execution and budget remain unapproved and separate from the agreed twelve answers.
If adopted, record it through T54's foundation. Architecture results remain conditional on the
selected model; later interactions may warrant a separate follow-up.

## Approved screening pool, 2 November 2026

The author approved six candidates: Qwen3.8-27B, gpt-oss-120b, DeepSeek V4.1 Flash,
GPT-6 Luna, Claude Haiku 5.5 and GPT-6.1 Sol. Sol is a higher-capability reference,
not the selected winner. The exact DeepSeek served version and all provider routes
must be verified before execution.

GLM-5.3-Flash, MiniMax-M3.1-Flash and Mistral Small 4 move to reserve to limit review
workload while retaining smaller open weights, inexpensive hosted options, proprietary
challengers and a higher-capability reference. This is not evidence of inferior performance.

Screen models using the same single-investigator setup before freezing a baseline for
A/B/C. Four cases per model would produce 24 final answers, and this four-case set plus three attempts are now approved. Settings, budget and
execution remain to be agreed. Approval of this pool does
not authorise inference calls or select a permanent production model.

## Four-case screening set approved, 2 November 2026

The author clarified that all four cases are approved: O1-02 matching travel, O1-06 partial
explanation, O1-09 missing later history and O1-12-D document injection, including their
plain-language expected assessments. The O1-09 discussion resolved a concern; it was not
approval of only that case. No further case-set approval is needed.

Use these four cases across the six approved model candidates. One pass produces
24 final answers; three passes are now approved. Exact fixtures, detailed scoring readiness,
provider routes, settings, limits and execution authorisation still need settlement.
The already agreed 12-answer A/B/C architecture calibration remains a separate stage.

## Screening repetitions approved, 2 November 2026

Author approved three attempts per model per case: six models × four cases × three
attempts = 72 final answers. Run a first pass of 24 answers, then inspect the setup for
fixture, prompt, scoring, adapter or recording problems before completing the other two
passes. This checkpoint is for setup diagnosis, not early winner selection or eliminating
candidates on one answer. Each attempt uses fresh memory and frozen evidence/instructions/
settings; preserve every result, failure and retry.

If the checkpoint exposes a problem requiring a change, preserve the original records and
version the correction. Do not pool changed-condition answers with the original comparison;
rerun affected comparisons fairly, with any extra calls covered by the eventual execution
limits. Additional reruns are not silently included in the approved 72-answer plan.

Provider routes, settings, detailed fixture/scoring readiness, spending/call limits and
execution authorisation remain open. The separate 12-answer A/B/C architecture calibration
is unchanged. These repeats measure variability on four development cases, not broad
production reliability.

## Configuration approved, 2 November 2026

The author confirmed OpenRouter as the gateway, fixed providers and these starting settings:

| Model | Serving provider through OpenRouter | Reasoning |
|---|---|---|
| Qwen3.8-27B | DeepInfra | Medium |
| gpt-oss-120b | DeepInfra | Medium |
| DeepSeek V4.1 Flash 1017 | DeepInfra | High |
| GPT-6 Luna | OpenAI | Medium |
| Claude Haiku 5.5 | Anthropic | Adaptive, medium |
| GPT-6.1 Sol | OpenAI | Medium |

Use standard service, disable automatic provider/model fallback and require support for
requested settings. This approves the starting configuration subject to compatibility checks;
it does not establish runtime support. DeepSeek's exact provider variant remains to be verified.
Record effective mappings, sampling and model revisions before execution; changes to approved
providers or reasoning levels need an explicit disposition, not silent substitution.

Time, output, retry/call and spending limits remain open. No paid inference or application
migration is authorised by this configuration confirmation. The six-model/four-case/three-pass
plan remains 72 answers with a setup checkpoint after the first 24.

## Screening execution policies approved, 2 November 2026

The policy sections below record the author's successive decisions. Later approvals
supersede earlier references to those decisions as open. These policies do not establish
runner readiness or runtime compatibility; T52 then T54 remains the delivery order.

### Screening timing approved, 2 November 2026

For the approved 72-answer model screen, allow at most 180 seconds per model request
and 600 seconds per complete case attempt. These are wall-clock deadlines from request
dispatch and case start, respectively, not idle-stream timeouts. The enclosing case
deadline includes collection, tools, backoff and any separately permitted retries.
Retries never reset that deadline; use the earlier applicable deadline for each request.
Preserve partial output and timeout status rather than silently replacing failed attempts.
Client cancellation does not establish that provider billing stopped; unresolved usage
must retain its reservation in the eventual spend ledger.

These ceilings do not establish a production latency acceptance threshold.
Setup-rerun allowances and spend policy remain open. No paid
execution is authorised. The separate A/B/C calibration limits remain to be settled.

### Screening token policy approved, 2 November 2026

The author chose no evaluation-imposed per-request or per-case generated-token cap for
the 72-answer screen. The proposed 16,384/32,768 allowances are rejected. Token usage is
an observed selection metric alongside assessment quality, time and cost, including large
differences between candidates. Approved reasoning settings and time deadlines remain.

Omit optional caps where supported. Verify and disclose unavoidable provider/model limits,
defaults and required output-limit parameters before execution; no route is claimed to be
literally unlimited. Inspect adapter defaults so they do not silently reintroduce a common
evaluation cap. Any necessary explicit provider ceiling must be recorded before the run.

Preserve input, generated output and reasoning usage where available, with missing usage
labelled unknown. Do not double-count reasoning included in reported output totals. Preserve
truncations, timeouts and failed-request usage. Tokenizers and reasoning accounting differ,
so consumption is evidence about the tested configuration, not identical computation units.
No unlimited spending is authorised. Set a separate spend policy before paid execution,
including how to bound outstanding charges without an evaluation-imposed token allowance.

### Screening call and retry policy approved, 2 November 2026

The author chose no evaluation-imposed model-call, tool-call or retry count cap within
each case attempt. Measure these as outcomes, both to compare configurations and to
identify recurring problems in the evaluation setup. Retain every underlying attempt,
including failures preceding a successful answer, its reason, elapsed time and available
usage/cost. Separate model-requested work, tool execution, adapter/transport retries and
runner recovery. Automatic retries must be observable rather than collapsed into a single
apparently successful call. Missing telemetry is an instrumentation gap, not zero retries.

The 180-second request and 600-second case deadlines still apply. Backoff and retries
consume the same case clock; they never reset it. The screen still has 72 scheduled case
attempts, with incomplete outcomes preserved. This ruling does not add new scored trials
or authorise automatic case reruns after a deadline. Probe/setup-rerun allowances and
spend policy remain separate decisions before paid execution.

Freeze and record retry behaviour/backoff and failure classifications in the runner
contract. No numeric cap does not mean retrying known permanent errors indefinitely.
Repeated errors warrant diagnosis across runner, provider and model/tool behaviour;
do not assume their cause from retry frequency alone. Keep the first-pass setup checkpoint.
Repairs create a new version and follow the existing fair-rerun protocol, preserving
original failures and keeping changed conditions separate.

### Screening concurrency approved, 2 November 2026

Run one case attempt at a time for the 72-attempt model screen. Rotate model order so
no candidate is always first; freeze and save the execution schedule before running.
Measure individual request latency and complete case duration separately. Keep compatibility
probes and any paid judge work out of the timed screening interval so they do not compete
with measured trials. Preserve the first-24 setup checkpoint.

Sequential execution reduces interference among trials; it does not eliminate external
provider-load variation and supplies no evidence of concurrent serving capacity. The
approved time, token and call/retry policies remain unchanged. Compatibility-probe and
setup-rerun allowances, spend policy and paid execution remain open.

### Compatibility policy approved, 2 November 2026

Before scoring, run one initial compatibility session per approved model configuration:
six sequential sessions, separate from the 72 scored case attempts. Use a small synthetic
task outside the four scored cases. Check exact model/provider identity, requested reasoning
and effective parameter mapping, a complete tool request/result/final-answer interaction,
the agreed output contract and recording of timing, available usage/cost, failures and
underlying retries. Distinguish settings supported by metadata from settings whose native
application cannot be independently observed; answer plausibility is not proof of configuration.

Apply the existing 180-second request and 600-second case deadline to each compatibility
session, without added token, call or retry count caps. Six sessions does not mean six
requests. Preserve failures and diagnose them before scoring the affected configuration;
transport incompatibility is not evidence of weak investigation quality. This policy does
not authorise paid execution. Post-fix setup reruns and spending remain to be agreed.

### Setup-rerun policy approved, 2 November 2026

After a documented setup fix, rerun only comparisons invalidated by that fix. Preserve
original results and version the repair. Identify affected model/case/pass cells and
expected cost before the repair batch. Shared prompt, evidence or runner changes require
rerunning the affected comparisons across all affected models. A genuinely isolated
adapter fix affects only that configuration's relevant trials. Retain all three scheduled
passes under the corrected conditions for affected comparisons; do not pool incompatible
versions or replace an unattractive answer merely because it scored poorly.

The author chose this over restarting all 72 trials after every fix. This is a rerun
selection policy, not permission for unlimited paid repair batches. Spending policy and
paid execution remain open. Original failures remain visible in setup/reliability reporting.

### Screening spending approved, 2 November 2026

Use one US$25 planning budget across the six initial compatibility sessions, 72 screening case
attempts and necessary documented setup-repair reruns. Review spending at US$15 and at
the existing first-24-results checkpoint. Do not allocate separate model budgets; cost
differences remain comparison evidence. This is a planning amount, not a cost forecast or a
guarantee of completing the screen. Later architecture calibration and any paid scoring
model are excluded.

Later author ruling on the same date: no request reservations or worst-case billing gate.
The author considers expected spending affordable and rejected the proposed method.
Track actual charges, including failed requests and retries, and identify unavailable
charges as unknown until reported. Retain the US$15 and first-24-results reviews. US$25
is not a guaranteed hard final-charge ceiling. Do not reintroduce rejected token/call caps
or reservation machinery. Budget approval alone does not establish run readiness.

### Remaining decisions

All four written screening grading applications are approved in
[the common rubric](52-objective1-scoring.md) and
[the screening clarifications](52-objective1-scoring-anchors.md#approved-screening-clarification--2-november-2026).
The direct-event window convention is also approved: with no alert, use the single login's
timestamp as both anchors, 24 hours before/after. Clip to available records and disclose
missing coverage; the analyst controls further expansion. Alert-relative windows and
O1-06/O1-09 diagnostic coverage are unchanged. All narrow screening policy checks in the
approval audit are settled. Broader T52 closure and T54 implementation/validation remain;
written approval is not test evidence.

Public prices and billing documentation have now been checked in the
[price report](52-screening-price-and-reservation-check.md), with an
[independent enforcement check](52-budget-enforcement-check.md). Their reservation proposal
was rejected by the author; it is retained as history, not an implementation requirement.

The six screening candidates, providers, reasoning settings and screening execution policies
are agreed. Runner ownership and its record contract are also agreed under T54. T54 must
materialise and verify fixtures, exact prompts and scoring under those decisions once T52
closes. Screening assessor arrangements and provisional-model selection rules are approved.
Implement
actual-cost reporting without token/call caps or reservations. The provisional model for A/B/C remains to
be selected from the screening evidence. No permanent application model is selected.

The 12-answer calibration stage is agreed. Review the proposed 189-answer exploratory stage
only after calibration; approve remaining new case anchors; agree scorer arrangements and
review workload; settle separate architecture-stage execution limits before
that paid run; authorise bounded fixture/runner work separately; define held-out confirmation
and final acceptance rules. T52 remains a decision ticket. This protocol launches nothing.
