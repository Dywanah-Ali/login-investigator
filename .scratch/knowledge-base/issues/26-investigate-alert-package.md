# 26: The investigation tool and its package

Type: build
Status: ready-for-agent
Blocked by: 13, 25, 45, 50, 52
Phase: 0
Model: strongest (Fable 5.1 or Astra)

## T52 scope handoff — 2 November 2026

Author confirmed reliable login investigation as the sole phase-0/1 objective, with bounded
account-impact and directly connected activity context. Standalone full inventory, exhaustive
permission-path presentation and reverse asset exposure are deferred. This supersedes broader
product-scope wording below. See [spec Current scope ruling](../spec.md#current-scope-ruling--t52-2-november-2026).
Detailed criteria below carry the approved T52 boundaries. Open design decisions remain
explicit; this reconciliation does not release T52 or authorise implementation.
Existing source code, questions, gold and thresholds are not changed or waived by this note.

## What to build

The analyst asks the agent to investigate a finding by its ID, and `investigate_alert` runs playbook
steps 2 to 6 in code and returns one package: account context, bounded potential impact,
involved-device peers, clearing documents and aggravating documents. Each section has its
evidence status and citations. Code supplies facts and check outcomes; the model assesses
the evidence and the analyst retains the verdict. It reports
progress per internal step, so the screen can later stack the steps while they run.

## Decisions implemented

- T05 d1 (`investigate_alert(finding_id)`), T05 d2 and d3 (one package with a named section per step,
  computed and ordered in code; spray and brute-force targets as a section, empty for other rules),
  T05 R5 (clearing and aggravating searches built in code from the finding's record, never from the
  chat; the radius from the one radius function of ticket 19), T05 d12 (package caps), T05 d13
  (parallel tool calls stay on).
- T05 d2 and T07 d4 (progress per internal step through the Port's custom stream).
- User stories 9, 15 to 19, 22, 23. Spec doors 2 and 3.

## Acceptance criteria

- [ ] Before any build work starts, the builder tells the author this ticket's `Model:` line and
      asks the author to set that model. The build starts only after the author confirms, and a
      dated line under Comments records the model used.
- [ ] `investigate_alert` finds the finding by its ID; an unknown ID returns plain content saying so.
- [ ] For an alert, omitted bounds use alert start minus 24 hours through alert end plus
      24 hours. Direct single-login investigation uses its timestamp ±24 hours. Clip to
      available records and disclose requested/effective bounds and coverage gaps. Explicit
      bounds reach the shared core; expanding history requires the analyst's decision. Test
      both defaults, explicit bounds and clipping. The generic core's all-record default
      must not silently become the package default. Permissions remain a snapshot.
- [ ] Device context selects devices involved in the suspicious activity, with dated peer
      records in the agreed window. Record the selection basis and omissions. Do not include
      every device used by the account merely because it appears in the window. No
      address-sharing context; same-source login activity remains distinct.
- [ ] The five named sections have code-built facts, evidence status and citations in a fixed
      order. A targets section is filled for spray and brute force and empty otherwise.
      Triggering/surrounding counts and outcomes come from code, not model arithmetic.
- [ ] Account context includes recorded owner/role and relevant privileged or sensitive
      access with supporting paths. Missing role evidence is explicit. Role is not a
      behavioural baseline; permissions never imply observed asset access.
- [ ] Before build, record the deterministic relevance/device-selection rules and package
      input/output shape under Answer, aligned with T45. Any new scope choice needs the
      author's ruling. Standalone inventory and exhaustive path presentation are deferred.
- [ ] The clearing and aggravating searches are built from the finding's record; a test proves the
      chat text does not reach them.
- [ ] Keep the package a thin coordinator over the same core account, graph and search
      functions used by narrow tools. Do not duplicate retrieval logic or introduce a model
      investigator inside the tool. No prior narrow-tool calls or model-supplied tool outputs
      are required to assemble the package.
- [ ] Save each internal step's inputs, outputs, evidence IDs and failure status in the artifact,
      under existing security/persistence rules. Independently verify component behaviour and
      package assembly/selection/caps. Use controlled missing-document and failed-step cases
      to distinguish retrieval misses from assembly omissions; do not add new gold or thresholds.
- [ ] Reuse the shared graph operations and retain their exact S6 regression against
      `truth.json`. Test the bounded package selection separately with supporting record/path
      IDs and stated omissions. Do not assert that a selected subset equals the full radius,
      or change existing gold to make that assertion pass.
- [ ] Caps hold: five chunks per search; selected impact and peer evidence is paged with
      `truncated` flags and its complete returned lists preserved in the artifact. Distinguish
      relevance selection from truncation. Full returned evidence is not a promise of full
      reachable inventory. T45 tests that required evidence survives selection and caps.
- [ ] Empty, unavailable, failed and omitted checks remain distinct in content and artifacts.
      Tests include controlled missing coverage and failed checks without inventing telemetry.
- [ ] Bounded next-investigation guidance names the uncertainty addressed, its case evidence
      and approved practice source, and distinguishes external checks from app actions.
      T45 selects sources for author approval; this ticket integrates only approved guidance.
      Recommendations must never be recorded as completed checks.
- [ ] Each internal step emits start, end or error through the Port's custom stream; a test proves
      the order. The API event itself ships in ticket 36.
- [ ] Parallel tool calls stay on.
- [ ] Agent tests use the fake model; the Port's eval passes.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

## Comments

- 2026-11-03 — Author approved the coordinator boundary after discussing overlap with
  narrow tools and troubleshooting. Reuse shared core functions; retain step-level evidence;
  test components and assembly separately. T29 owns separate application evidence for collection,
  assembly and model interpretation. See spec "Investigation coordinator boundary". Documentation
  only; no build release, specialist adoption or T54 change.

- 2026-11-01 — T25 gate ruling: address-sharing context is removed everywhere. T50 removes it
  from the radius and answer key first, so this ticket now also waits for T50.

- 2026-11-01 — Author: wait for [T52](52-agent-objectives-and-reliability-review.md), the
  phase 0 and 1 objectives and reliability review. Carry its approved requirements into this
  ticket before work starts; existing requirements remain in force until explicitly amended.

- 2026-11-02 — Author approved this ticket as the integration owner for E06 guidance,
  using sources selected in T45 and approved by the author before use. No build authorised
  by the ownership ruling; existing design and dependency requirements remain.
