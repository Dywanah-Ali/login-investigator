# 43: Restore the Port eval's margin: Q02 and Q04 in the grown world

Type: grilling, then build
Status: ready-for-agent
Blocked by: none
Phase: 0

## Why this ticket exists

From T13 on, the Port eval meets its 90% gate at exactly 57/63 with no spare run: Q02 and Q04
fail all three runs on an unchanged agent (fingerprint `7ff8e5ae`). One more failure on any later
ticket would fail the gate on behaviour no ticket changed. Both failures began when T11 and T12
grew the synthetic world (S6, the benign twins, 1,948 rows, ten findings). The author ruled on
26 October 2026 to scope a fix before T14, and to track it as a ticket in this initiative.

Register: AUD-046 (Q04), AUD-047 (Q02). Bug log: B-074, B-076 and their recurrences.

## What the T13 eval artifact shows

Source: `backend/evals/results/2026-10-26-131223-7ff8e5ae.json`, Q02 runs 1 to 3 and Q04 runs 1
to 3.

### Q04 "Was any account compromised this week?"

- All three runs call `find_suspicious_activity`, then `search_logins` for the six addresses in
  the findings, and no `lookup_ip_reputation` at all. The three required-lookup checks fail.
- The prompt already asks for the lookups (`agent.py`, "How to investigate", step 2). Only the
  searches are enforced in code: `complete_detection_searches` in
  `backend/login_investigator/investigation_policy.py` adds a missing `search_logins` per finding
  address, and nothing adds a missing lookup.
- Inferred, not recorded: the six searches were probably added by that hook rather than chosen by
  the model, because their order matches the findings order the hook uses. The artifact does not
  record which calls the hook made.
- Likely cause: the Port world had four findings and three addresses; the grown world has nine
  findings in the broad window and six addresses, two of them reserved. With more to cover, the
  model stops after the detection step and the hook fills in only the searches.
- Not measured by Q04's checks: **no run states that amelia.ward was compromised.** Run 1 lists
  her only as a `new_country` finding; runs 2 and 3 omit her. Q04's checks were written for the
  Port world and never ask about S6 or its address `45.148.10.80`.

### Q02 "Was there any password spraying this week?"

- All three runs call the rules, both lookups and both address searches. Every run passes the
  address, the 35 accounts and the rules check, and fails "says no attempt succeeded".
- Every run gives S6 as "20 failed attempts on 20 accounts" and never mentions its three
  successful sign-ins on amelia.ward, and none states that S2 had no success.
- The `password_spraying` finding counts failed attempts only. The search for `45.148.10.80`
  returned the successes (`search.py`, `summarize`: `successes`), so the right number was in front
  of the model; it trusted the finding's count instead.
- The code hook does not run for Q02: `_specific_question` treats a question that names an attack
  type ("spray") as specific and returns before any coverage check.
- The check itself is stale: "says no attempt succeeded" (`evals/questions.json`, Q02) was
  correct when S2 was the only spray. In the grown world one spray succeeded, so the check could
  pass a false "nothing succeeded" answer.

### Noticed, outside scope

- Q02 run 2 gives S6's last-seen time as 02:06:20; runs 1 and 3 say 02:20:00. Corrected at the
  build: `truth.json` gives S6's last failure as 02:06:20, the spraying finding's own last-seen
  time, so run 2 was right; runs 1 and 3 gave the address's last success as the finding's time.
- The benign twins (maya.patel, oliver.hayes) appear as suspicious in Q04. Expected until the
  clearing documents and the corpus exist (T15, T16 and phase 1).

## Proposed shape, for the author's rulings

Nothing below is approved. Each line becomes a decision under the Answer once the author rules.

| Part | Proposal | Reason |
|---|---|---|
| Q04 lookups | Extend `complete_detection_searches` so it also adds `lookup_ip_reputation` for every public address in a broad question's findings | Deterministic; the spec keeps the Port's policy "kept and extended, not replaced" (T05 d9) |
| Q02 outcomes | One prompt line: a brute-force or spraying finding counts failures only, so take each source's successes from `search_logins` and say for every source whether any sign-in succeeded | The spec keeps the Port's three tools unchanged (T05 d1), so changing the finding's output would need a spec change |
| Eval checks | Make Q02 and Q04 stricter for the grown world: Q02 states S2's no-success and S6's three successes; Q04 names amelia.ward and looks up `45.148.10.80` | The current checks can pass a wrong answer; a content change, so the author's ruling |

## Open questions for the author

1. Scope: does this count as a Port change "the use case requires" (map, Out of scope), since this
   initiative's data caused it? **Ruled yes by the author, 26 October 2026.**
2. Q04: the code hook extension as proposed, or another approach? **Ruled: the code hook
   extension, by the author, 26 October 2026.**
3. Q02: the prompt line as proposed, a spec change to the tool's output, or another approach?
   **Ruled: put the truth on the card, by the author, 26 October 2026. Form ruled in ruling 4: an
   agent-only field.**
4. The eval checks: make Q02 and Q04 stricter as proposed, and with which exact wording?
   **Ruled: add the checks to Q02 and Q04 in place, by the author, 26 October 2026 (ruling 5).**
5. Acceptance: which eval result closes the ticket, given that stricter checks may lower the score
   before the fixes raise it? **Ruled: gates met plus Q02 and Q04 at 2/3 or better each, by the
   author, 26 October 2026 (ruling 6).**

## What to build

Three changes, from rulings 2, 4 and 5:

1. `complete_detection_searches` also adds `lookup_ip_reputation` for every globally routable
   address in a broad question's findings that has not been looked up this turn. Reserved and
   private addresses are skipped. Specific questions stay untouched, as today.
2. `find_suspicious_activity` adds one agent-only field to each finding with what the finding's
   address did over the tool call's window (the whole log when no window is given): successes,
   failures, and the accounts it signed in to. Proposed name `address_activity`, a list with one
   entry per address. `Finding`, `Finding.to_dict()` and the Alerts reply stay unchanged.
3. Q02 and Q04 in `backend/evals/questions.json` gain the ruling-5 checks, with nothing removed.

## Acceptance criteria

- [ ] A broad question whose findings name public addresses ends its turn with a reputation lookup
      for each of them, proven by the investigation-policy tests with a fake model; a reserved
      address gets no lookup; a specific question gets none added; an address the model already
      looked up is not looked up twice.
- [ ] Each finding in `find_suspicious_activity`'s output carries `address_activity`; for S6 it
      shows 3 successes, 20 failures and amelia.ward; for S2 it shows 0 successes. Proven by tool
      tests against the `default` dataset.
- [ ] The Alerts reply and `Finding.to_dict()` are byte-for-byte unchanged, proven by the existing
      API and rules tests passing untouched.
- [ ] Q02 and Q04 carry the ruling-5 checks; their expected values agree with `truth.json`,
      proven by the eval-question tests.
- [ ] One paid eval run with a `--label`: 90% overall and 100% security met, and Q02 and Q04 each
      pass at least 2 of 3 runs. A failed run is not rerun for a cleaner score: it is logged in the
      bug log and the fix is reworked.
- [ ] AUD-046 and AUD-047 closed with that run as evidence; B-074 and B-076 updated with the fix.
- [ ] Standing criteria (spec, Testing Decisions): the safety net passes, new Python files are clean
      under the type checker, and the two-axis code review (`mp-code-review`) has run with its
      findings triaged.

Open at build, for the author's review before the eval run: the field's final name, and the exact
check patterns for Q02 and Q04.

## Comments

- 26 October 2026, scoping (Claude): opened from the T13 handoff's open question. The author chose
  to scope Q02 and Q04 before T14 and ruled that the work is tracked as a ticket in this
  initiative. Evidence read: the T13 artifact, `agent.py` system prompt, `investigation_policy.py`,
  `search.py`, `evals/questions.json`, AUD-046, AUD-047, B-074 and B-076. No code changed.
- 26 October 2026, ruling 1 (author): this is a Port change the use case requires, because the
  initiative's grown world caused both failures. It is in scope for this initiative.
- 26 October 2026, ruling 2 (author): Q04's lookups are enforced in code.
  `complete_detection_searches` also adds `lookup_ip_reputation` for every public address in a
  broad question's findings; reserved addresses are skipped, since they have no reputation. A
  stronger prompt alone was rejected because the prompt already asks for the lookups. Dropping the
  lookup checks was rejected because it lowers the bar.
- 26 October 2026, how a finding's counts are filled (Claude, from `rules.py`): each rule builds
  its finding from only the rows it selects, across the whole log; the question's window only
  filters which findings are shown (`in_window`). The spraying rule selects failed sign-ins only
  (`_failures`), so a spraying finding's `success_count` is always 0. The agent therefore sees
  S6 as `failure_count: 20, success_count: 0`, which is true for the rule's rows and false for
  the address, which also made three successful sign-ins on amelia.ward. The model was not only
  ignoring the search; the finding told it something misleading.
- 26 October 2026, ruling 3 (author): Q02 is fixed by putting each address's success count where
  the model already looks, the finding. A prompt line alone was rejected as unreliable; a code
  check on the answer's wording was rejected because the policy never reads prose (T05 d10).
  This changes T05 d1 ("the Port's three tools unchanged"), so it needs a spec edit and a
  decisions-log row once the form is ruled.
- 26 October 2026, the Alerts screen (Claude, from `frontend/src`): the table shows only
  `event_count` (`alerts-table.tsx`); it never shows `success_count` or `failure_count`. The
  misleading zero reaches the agent, not the analyst's eye.
- 26 October 2026, ruling 4 (author): the truth goes on the card as an agent-only field. The
  detection tool adds one clearly named field to each finding with what the finding's address did
  overall: successes, failures, and the accounts it signed in to. The core `Finding`,
  `Finding.to_dict()` and the Alerts reply stay unchanged. Replacing the rule's own counts in the
  agent's view was rejected as a wider change to what the agent sees; changing the core finding
  was rejected because ticket 32 allows the Alerts reply to gain `finding_id` and nothing else.
  Open for the acceptance criteria: whether "overall" means the question's window (Claude's
  lean) or the whole log, and the field's exact name.
- 26 October 2026, ruling 5 (author): Q02 and Q04 in the Port's `questions.json` gain checks for
  the grown world, in place. Nothing is removed. Q02 adds: names `45.148.10.80`, names
  amelia.ward, states three successful sign-ins; its no-success check stays and covers S2. Q04
  adds: names amelia.ward, looks up `45.148.10.80`. This stretches T04 d17's exception (an expected
  value updated when a new story changes it) from counts to expected facts; recorded in the spec's
  decisions log. Adding two duplicate S6 questions instead was rejected because the old Q02 check
  would stay stale and each run would ask the same question twice. No eval change was rejected
  because the eval could not see a missed compromise. Exact check patterns are written at build
  and shown to the author with the acceptance criteria.
- 26 October 2026, ruling 6 (author): the ticket closes on tests for the hook and the field, and
  one paid eval run that meets 90% overall and 100% security with Q02 and Q04 each at 2/3 or
  better, which restores about four spare runs. Requiring 3/3 was rejected because one unlucky
  run would fail the ticket with no clean way out under the no-rerun rule. Gates alone were
  rejected because they could pass with Q02 and Q04 still failing. Claude chose the window for
  `address_activity`: the tool call's own window, so the field never reports activity outside
  what the analyst asked about. All six rulings are in; status set to ready-for-agent.
- 26 October 2026, build start (author agreed the seams): 1, the real agent loop with a fake
  model (`test_investigation_policy.py`); 2, the detection tool on the `default` dataset
  (`test_tools.py`), expected values from `truth.json`; 3, the eval grader
  (`test_eval_scoring.py`), right answers pass and T13's real wrong answers fail; 4, the existing
  Alerts API and rules tests, untouched; 5, one paid eval run.
- 26 October 2026, build (Claude): implementation commit `d2475f8`, test first at seams 1 to 3.
  Red before green for the hook lookups, `address_activity` and the new checks; the guard line
  on specific questions passed at once, as it pins behaviour that already worked. One existing
  policy test changed: each turn now also gets a lookup, so its per-turn tool count is 3.
- 26 October 2026, `mp-code-review` on `aac502a...d2475f8`, triage:
  - Spec, fixed: the first Q02 three-successes pattern (copied from Q21) and the Q04 compromise
    pattern passed wrong answers and failed right ones (negations, "succeeded", "signed in to X
    three times", markdown lists). Both became shared patterns `THREE_SUCCESSES` and
    `AMELIA_COMPROMISED`, pinned by both-direction tables holding every reviewer probe. Spec
    T05 d1 now says "in the tool call's window", not "overall".
  - Spec, for the author: Q04's check says amelia.ward was compromised, stricter than ruling 5's
    "names amelia.ward", because T13 run 1 named her only as a new-country sign-in.
  - Standards, fixed: the detection tool's description, which the model reads, now explains
    `address_activity`; the hook is renamed `complete_detection_evidence`; the gold test checks
    through `passes` instead of the pattern text; `address_activity` reuses `summarize`; one
    `s6` fixture in `conftest.py`; `_finding` rename; declaration order; a glossary entry.
  - Standards, kept: the register and bug log update at closure, after the paid run.
  - Noticed, outside scope: Q21's three-successes pattern has the same weaknesses as the first
    Q02 pattern. Q21 passed 3/3 in T13; not changed here.
- 26 October 2026, evidence before the paid run: 485 backend and 149 frontend tests, pyright
  clean. Free re-grades of T13's saved answers (`2026-10-26-171504` before review,
  `2026-10-26-172237` after): 57/63 and 15/15, Q02 and Q04 0/3 on exactly the new and old
  checks, no other question affected.
- 26 October 2026, ruling 7 (author): an agent should not pronounce an account compromised on its
  own; it raises the concern with its evidence and the verdict stays the analyst's, as in the S4
  ruling. The Q04 check already passed hedged wording ("potentially compromised", "may have been
  compromised", "likely compromised; confirm with her") and failed only when no concern was
  raised; its name said otherwise. Renamed "flags amelia.ward as possibly compromised (S6)", with
  four hedged phrasings added to its tests (69 grader tests pass). Failing a definite "was
  compromised" was not taken: it needs a prompt change that touches every question, so it would
  be its own ticket. This ruling amends ruling 5's "names amelia.ward" for Q04.
- 26 October 2026, the paid eval run (author's go): `2026-10-26-173622-f853f368.json`, label
  "T43 lookups, address activity, S6 checks", fingerprint `f853f368`, fresh API server from
  `b691014`. Overall 57/63 (90%) and security 15/15: the Port gates are met with no spare run.
  **Ticket 43's bar is not met**: Q02 0/3 and Q04 1/3, where ruling 6 asks 2/3 each. Not rerun.
  - Q04: the hook fix works. Every required lookup ran in all three runs (the four lookup checks
    pass 12/12). Flagging amelia.ward passes run 2 only; run 3 omits her; run 1 recommends
    securing her for "sign-ins from new countries" without linking her to the spray.
  - Q02: no progress. All runs give S6 as 20 attempts; runs 2 and 3 say "all failures", a false
    claim. The model ran no sign-in search this time, and repeated the finding's own counts
    rather than `address_activity`. Run 1 also lost S2's no-success statement.
  - Q02's "names the account S6 signed in to" passed only because amelia.ward is in the targeted
    list; the check needs to tie her to the successes.
  - Q19 run 3 failed on a grader miss (B-077): "Please follow your organization's procedures" is a
    recommendation the `RECOMMENDS` pattern does not know.
  Logged as the B-074 partial fix, the B-076 recurrence and B-077. Status set to needs-info: the
  rework needs the author's ruling, since the evidence points against ruling 4's choice to keep
  the finding's own counts in the agent's view.
- 26 October 2026, ruling 8 (author), amending ruling 4: the rework does three things. (1) The
  agent's view of each finding drops the rule's own `success_count` and `failure_count`, so the
  only success number it sees is `address_activity`'s; `event_count` stays, since the tool panel
  shows it and it is not a success figure. `Finding.to_dict()` and the Alerts reply stay
  unchanged. (2) One prompt line: when an address from a spraying or brute-force finding signed
  in to an account, say so with the count and flag that account as possibly compromised (ruling
  7: the agent flags, the analyst decides). (3) Q02's "names the account S6 signed in to" must tie
  amelia.ward to a success, not pass on the list of targeted accounts. Dropping the counts alone
  was not taken: a failed run costs another paid run. Pausing the rework was not taken: the margin
  would stay at zero. Status back to ready-for-agent; the acceptance criteria are unchanged.
- 26 October 2026, rework build (Claude), test first: the agent's view drops `success_count` and
  `failure_count` (tool test red, then green); the tool description now speaks of "an event
  count"; one prompt line under "How to investigate" (prompt test red, then green); Q02's account
  check is now "ties amelia.ward to S6's successes" with the shared pattern `AMELIA_SIGNED_IN`
  and a both-direction table holding T43 run 1's target list. Evidence: 499 backend and 149
  frontend tests, pyright clean. Free re-grade of the T43 run (`2026-10-26-174557`): 57/63, and
  the tightened check now fails all three Q02 runs that named her only as a target.
- 26 October 2026, `mp-code-review` on `79efb01...39cf2a8`, triage:
  - Spec, fixed: `AMELIA_SIGNED_IN` passed answers with a negation before her name ("no
    successful sign-ins… including amelia.ward", "0 successful", "success count: 0") and failed
    the model's list style ("Signed-in accounts: amelia.ward", a "Signed in to:" list, "got
    into", "signed in from 45.148.10.80 three times"). It now guards the whole line against
    negation and accepts those forms; it no longer passes on "compromised" alone, which is Q04's
    check. Every probe is in the both-direction table (89 grader tests).
  - Spec, kept, a risk for the paid run: S6's rule summary still reads "failed on 20 accounts in
    20 attempts". It is true and comes from the core, which the Alerts screen shares; ruling 8 did
    not ask to change it.
  - Spec, kept: the prompt addition is one bullet of four sentences carrying ruling 8's intent.
    Q04 will likely flag benign twin oliver.hayes too, which is expected until the clearing
    documents exist.
  - Standards, fixed: pattern-key whitespace, one docstring line over 100 characters, the glossary
    entry, and a named `HIDDEN_FROM_AGENT` constant in `tools.py`.
  - Standards, kept: the two Amelia patterns repeat a negation guard; JSON patterns cannot share
    a fragment.
  - Noticed, outside scope: three lines in `agent.py` over 100 characters predate this ticket.
- 26 October 2026, evidence before the second paid run: 510 backend and 149 frontend tests,
  pyright clean; free re-grade of the T43 run (`2026-10-26-175342`) 57/63 with the same failures.
