# 28: Enforce investigation completion before reporting

Type: build
Proof type: AI judgement
Rigour: Tier 3
Status: ready-for-agent
Blocked by: 60
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

T26 supplies the single shared core procedure and T60 supplies full/narrow activation and
application integration. This ticket enforces completion before reporting using that same
procedure and the retained investigation state. A narrow question stays narrow. The incident
report is written only after every required step has run, or it names the step that could not
run and why.

## Decisions implemented

- T05 d14 (one shared procedure, now built by T26 and consumed here), T05 d9 (required-work
  enforcement and model-call limit, integrated in T60 rather than a duplicate hook), T45's
  8 November 2026 full/narrow parent-mode ruling (supersedes T05 d10's tool-choice activation), T05 d11 (`playbook_status` and the report gate), T05 R3 (nothing runs
  unasked), T05 conditions (the Port's existing policy is kept and extended).
- User stories 7, 8, 13, 49 to 51. Spec door 3.

## Acceptance criteria

- [ ] Required checks implement the bounded T26 investigation scope. Track empty, unavailable,
      failed and omitted states distinctly. A failed check must not be marked complete merely
      because prose exists; the report identifies the resulting limit.
- [ ] Default alert/event windows and analyst-controlled expansion survive report completion
      and follow-up. Neither the policy nor report gate silently widens collection.
- [ ] External next-investigation recommendations remain recommendations, not tool results
      or completed playbook checks. Test this distinction and narrow-question behaviour.

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] Consume T26's one core procedure and T60's retained obligation state. Report completion
      and evaluation use the same definitions; do not create another playbook or policy loop.
- [ ] Verify T60's pre-dispatch full-investigation mode instantiates required work from
      the shared core procedure. Omitting a task or choosing a narrow tool cannot waive it.
      Narrow-lookup mode stays narrow; a later narrow turn does not erase outstanding full work.
      Coordinate enforcement placement with the approved parent workflow rather than duplicate
      the procedure in a hook. Natural-language classification and deterministic enforcement
      are checked separately under the existing workflow evaluation.
- [ ] Verify T60/T59 loop limits also bound the report path; no second independent retry budget.
- [ ] `playbook_status` runs before the report chain and completes any missing code-derived step by
      calling the core directly, with no model call.
- [ ] A step that cannot run is named in the report in one plain line with its reason, and recorded
      in full (step, error class, time, store) in the artifact and the app log.
- [ ] The Port's policy tests pass unchanged; the report keeps its shape, PDF and severity scale.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Apply the current proportional-testing and proof rules: focused affected-behaviour tests,
      relevant types/lint, one scoped review and applicable existing agent evaluations. Fake-model
      tests prove plumbing; evaluation proves model behaviour. Older standing safety-net wording
      does not require full suites after every edit or an extra review campaign. Record third-party
      documentation/version checks and test any changed admin commands.

## Comments

- 2026-11-08 — Author approved this final report-enforcement slice after T60. T26 owns the
  procedure, T60 activation and public application integration, T27 the citation resolver.
  T60 transitively supplies T26/T27, so the blocking edge is T60. IC-07–11 are inherited.
  Planning approval is not build release; older ownership wording below is historical.

- 8 November 2026 — Author approved T45's explicit full/narrow parent workflow mode. This
  replaces the legacy trigger based solely on investigate_alert tool choice. Mandatory core
  procedure, report gate, scope approval and honest incomplete outcomes remain. Exact ownership
  is reconciled with the forthcoming orchestration ticket; no implementation starts here.
