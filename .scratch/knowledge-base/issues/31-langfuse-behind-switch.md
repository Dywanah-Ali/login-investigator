# 31: Langfuse behind its switch

Type: build
Status: ready-for-agent
Blocked by: 29, 54
Phase: 0
Model: standard (Opus 5.5 or Sol 6.1)

## What to build

Delivery split: [T54](54-early-langfuse-evaluation-integration.md) completed the temporary
comparison and Langfuse familiarisation. [T56](56-minimal-evaluation-foundation.md) owns its
retirement and a small official SDK foundation. This ticket retains application and full-exam
integration, building on that foundation rather than inheriting the temporary comparison schema.
The criteria below apply to this remaining scope.

Langfuse mirrors dev investigations and eval runs behind one switch that is off by default. The repo
stays the source of truth: the JSON result file is written first, an upload failure is shown loudly,
and the author's labels come back only through an export script into a repo file.

## Decisions implemented

- T06 d10 (Langfuse adopted to the full as a mirror), AUD-036.
- [review ruling 4] proven with the switch on against a fake destination, plus one real eval run
  seen in Langfuse.
- API contract change 5 (the Langfuse switch setting).
- User stories 83 to 85. Spec doors 3 and 6.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] One callback handler is added in the agent-building function.
- [ ] Off by default; one environment variable turns it on; the key is loaded only when on and never
      written to a result.
- [ ] The two question files are uploaded as datasets; each eval run is an experiment run stamped with
      the same fingerprint and commit as the JSON file; every check verdict is a boolean score; the
      judge's verdict and reason are a score with a comment.
- [ ] A masking hook is applied to everything sent.
- [ ] Tests with the switch off, and with it on against a fake destination: the JSON is written
      before any upload; an upload failure is reported loudly in the summary and the JSON survives;
      the masking hook is applied; labels return only through the export script.
- [ ] Nothing at runtime reads from Langfuse.
- [ ] One real eval run is visible in Langfuse; a dated line records the author's look, and AUD-036 is
      closed with that evidence.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- Author approved on 2 November 2026: finish T52, then T54 early Langfuse evaluation
integration, then instrumented 12-answer A/B/C calibration. T31 retains application tracing
and full T29 exam integration, reusing T54. T52 must assign the calibration runner implementation
owner and settle its record contract before T54 starts. Local files remain authoritative;
results are saved before upload, masking applies throughout, and human labels return only
through explicit export. Blinded scoring must hide revealing architecture labels and traces.
Model choice, budgets and paid execution remain separate unresolved decisions.

- 2026-11-02 — Later author ruling assigns the comparison runner and its nine-group record
  contract to T54. Its live integration can be proved with a scored screening result before
  architecture calibration. This ticket keeps application/full-T29 integration and reuses
  that recording module; its original full-exam acceptance evidence remains required.

- 2026-11-04 — Author clarified that T54's ad hoc model-comparison upload is only for
  learning Langfuse, not a routine operational workflow or operational-integration proof.
  Real evaluation/tracing work comes with fully implemented running v2 under T29/T30/T31.
  No operational requirements or implementation are silently established by the temporary
  comparison workflow. Automated comparison remote reconciliation was explicitly dropped.

- 2026-11-04 — T54 resolved after author accepted the visual familiarisation walkthrough.
  Its current custom connector is temporary. Separate T56 carries the approved retirement
  and minimal SDK-based foundation, exact scope before build. T31's later operational
  evaluation/tracing must follow the settled agent evaluation scope rather than inheriting
  the ad hoc comparison design. No operational acceptance or T31 implementation claimed.
