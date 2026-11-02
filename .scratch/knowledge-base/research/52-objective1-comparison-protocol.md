# T52: Proposed trial and architecture decision protocol

Date: 2 November 2026. Status: staged comparison plan.
The A/B/C comparison structure, common rubric and 12-answer calibration stage are agreed.
The author approved calibration first on 2 November. The 189-answer exploratory stage,
eligibility rules, budgets and implementation details remain proposals.

## Stage 1: calibrate the scoring and runner (author agreed)

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

## Decisions still needed

Model research now precedes setup design at the author's request. See
`52-model-calibration-proposal.md` and `52-model-selection-industry-evidence.md`.
Neither model name nor reasoning setting is selected yet; the fixed-model A/B/C control
remains the proposed first-calibration baseline pending the model ruling.

The 12-answer calibration stage is agreed. Review the proposed 189-answer exploratory stage
only after calibration; approve remaining new case anchors; agree scorer arrangements and
review workload; set call/time/cost limits before
any paid run; authorise bounded fixture/runner work separately; define held-out confirmation
and final acceptance rules. T52 remains a decision ticket. This protocol launches nothing.
