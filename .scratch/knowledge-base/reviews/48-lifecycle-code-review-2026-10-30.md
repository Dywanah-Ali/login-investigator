# T48 lifecycle checkpoints: two-axis review

Scope: checkpoints 1–2, before the agreed fresh-session continuation for native inspection.
Baseline: `ccf5348924afc2911c1fe0c405ad1abf407e1ac6`.
Review input: staged working changes, `git diff --cached ccf5348924afc2911c1fe0c405ad1abf407e1ac6`.
Two independent reviewers used the originating ticket/spec and repository standards respectively.
Checkpoint 3 remains open; this is not whole-ticket acceptance.

## Standards

Initial: one medium finding. A graph-driver close error or cancellation could prevent PostgreSQL
pool disposal. Fixed with an independent nested `finally`; failure and cancellation tests added.
See B-117.

Final independent recheck: **0 remaining actionable findings**. The reviewer confirmed separate
cleanup ownership and the evaluation lifecycle's core placement and retained recovery state.
No actionable baseline code smells were reported.

## Spec

Initial: two P2 findings. The same independent-cleanup gap, and evaluation entry points using
the application's selected stores instead of owning disposable complete versions. Both fixed.
Evaluations now own a new source snapshot, PostgreSQL database, Neo4j service and private pointer.
Exact checked passage vectors avoid repurchasing identical embeddings. Query/model calls retain
their existing behaviour; offline pairs cannot provide live evaluation evidence. See B-118.

Follow-up: one P2 finding in the no-build branch. It still exposed the working pointer, permitting
a first build published during evaluation to enter that evaluation. Fixed with a private absent
pointer. The regression test failed by attempting forbidden database settings before the fix,
then passed after it, including cleanup of the private state.

Final independent recheck: **0 remaining actionable findings** for checkpoints 1–2. The reviewer
confirmed the publication-race fix and that both earlier fixes remain resolved.

## Verification and boundaries

Test results and actual restart measurements are recorded in the ticket. Review inspection does
not replace those checks. No live paid agent evaluation is claimed. Native Browser queries,
styling/limits, the author's walkthrough and Gephi retirement remain checkpoint 3. T49 owns
maintenance-window acceptance and switching the working application.

Totals: Standards 0 remaining; Spec 0 remaining. Initial findings and fixes are preserved above.
