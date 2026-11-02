# 28: The playbook enforced

Type: build
Status: ready-for-agent
Blocked by: 26, 27
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## What to build

The playbook becomes one list in the core that the agent's policy, the report gate and the eval all
read. When the analyst asks for a full investigation, every required step runs; a narrow question
stays narrow. The incident report is written only after every required step has run, or it names
the step that could not run and why.

## Decisions implemented

- T05 d14 (the playbook as one data structure: steps with the tool and section that serve them and a
  required-for-report flag), T05 d9 (before-model hook adds a missing required step as a tool call;
  model-call limit), T05 d10 (the shortcut rule is the tool choice; the policy reads tool calls and
  results, never prose), T05 d11 (`playbook_status` and the report gate), T05 R3 (nothing runs
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
- [ ] The playbook is one list in the core, read by the policy hook, the report gate and the eval.
- [ ] After a call to `investigate_alert`, the before-model hook adds any missing required step as a
      tool call. A narrow tool call does not trigger the full plan.
- [ ] A model-call limit stops loops; a test proves it.
- [ ] `playbook_status` runs before the report chain and completes any missing code-derived step by
      calling the core directly, with no model call.
- [ ] A step that cannot run is named in the report in one plain line with its reason, and recorded
      in full (step, error class, time, store) in the artifact and the app log.
- [ ] The Port's policy tests pass unchanged; the report keeps its shape, PDF and severity scale.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments
