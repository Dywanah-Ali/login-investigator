# 60: Connect chat, research and saved investigations

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 26, 59, 27
Phase: 0

## What to build

An analyst uses the existing Investigator screen to clarify a question, request a narrow lookup
or start a full investigation. The parent workflow coordinates validated research and required
evidence collection, then delivers a grounded answer with preserved evidence and honest gaps.
Existing investigations, reports and downloads remain usable across restart.

Author approved this ownership on 8 November 2026 through to-tickets. T45 is the parent design;
IC-01–11 and P-01–03 are inherited. Planning approval is not build release.
Select the build model under the map's model guidance before implementation.

## Acceptance criteria

- [ ] Implement the thin explicit LangGraph parent workflow and central model construction.
      Chat constructs semantic assignments; trusted code allocates IDs, resolves scope/identity,
      validates, dispatches and assembles evidence. Use T57 contracts, T59 workers, T26 package/
      procedure and T27 citation resolution. No duplicate investigator inside the package.
- [ ] Establish full/narrow mode and its basis before dispatch. Full mode instantiates T26's
      required obligations independently of the model's task list. Narrow queries stay narrow;
      later narrow turns neither erase outstanding full work nor automatically rerun it.
      Test omitted mandatory work after full mode is established and a narrow control separately.
- [ ] Clarify material identity/scope ambiguity using ordinary chat. Resolve relative time using
      trusted reference context, preserve explicit user authority and require analyst approval
      for proposed history expansion. A malformed model response is not automatically a user
      question. Preserve finding-discovery and reputation capabilities through T57's boundary.
- [ ] Batch independent requests with separate results; dependent follow-ups wait for chat
      interpretation and remain bounded. Rejected requests stay visible while unrelated valid
      requests can proceed. Chat has no direct investigative retrieval tool exposure.
- [ ] Preserve actual original evidence and conditions at chat's interpretation boundary, with
      per-answer/task attribution, omissions and outstanding work. Keep baseline versus research
      candidate/delivery records separate for T29. Apply T27's single correction/unverified path;
      valid references alone do not certify semantic support.
- [ ] Implement selected chat examples for compound requests, material ambiguity and narrow
      follow-ups. Assess classification, assignment quality and interpretation through existing
      evaluations, separately from deterministic enforcement. No exam answers in examples.
- [ ] Route only public answer text to the public stream; worker reasoning/tool internals cannot
      leak through shared node names. Retain existing progress usability and update necessary
      event/name compatibility through API/frontend tests. T36 retains the later step-stack
      design; this ticket introduces no new screen. Write changed API shapes before code.
- [ ] Preserve one-writer ownership until cancelled child work stops. Test disconnect/cancellation,
      resume/replay and late results against request identity. Retain partial evidence without
      claiming exactly-once work merely because checkpoints exist.
- [ ] Preserve parent conversation state, existing history and report generation/update/PDF
      behaviour, including saved-case reads without a model. Prove reopen retains original
      evidence after source replacement rather than silently querying current data. No storage
      migration/retention policy; T33/T35 retain evidence-panel/download features. T28 adds the
      final completion-before-report gate after this integration.
- [ ] Exercise the application through agent/API and affected frontend boundaries, with focused
      cancellation, public-stream and saved-evidence checks. Run applicable existing agent evals;
      T29 still owns phase-0 knowledge-base acceptance after T28/T44. Keep failed/incomplete runs.
      Apply proportional testing, with full suites only where the actual cross-cutting change
      warrants them, and one scoped review. No extra paid comparison or model migration.
- [ ] Record relevant installed-version/documentation checks before library integration; retain
      LangGraph/LangChain and Pydantic behind their approved responsibilities. Update/test admin
      tasks if changed. Later Langfuse integration remains T31 over T56's foundation.

## Comments

- 2026-11-08 — Approved handoff. AUD-086 lifecycle/public-stream risks belong here, task-local
  lifecycle in T59, shared obligations in T26 and final report enforcement in T28. No new
  architecture review is requested. T45 remains unchanged by this ticket publication.
