# 18: Eval set in API mode

**What to build:** the v1 eval set proves the agent through the real transport. The runner starts
its own server, drives the Investigation endpoints for every question and the report, scores with
the unchanged grader, and records the run in a results table that begins with v1's history.

**Blocked by:** 16 (Investigations API).

**Status:** ready-for-agent

Spec: [spec.md](../spec.md), "Testing Decisions". Contract: "What the eval runner's API mode drives".

- [ ] A new API mode in the runner: starts FastAPI on a free port with a temporary memory file and the AbuseIPDB key unset; starts an Investigation; asks each question through the ask endpoint and reads the stream to the end; a `REPORT` turn goes to the report endpoint; reopens and scores the last Turn with the unchanged grader
- [ ] The direct mode still works for cheap iteration; the API mode is the one that counts
- [ ] Questions, gold answers and grader unchanged from v1; the scoring tests pass
- [ ] v1's results summary rows copied in as the first rows of v2's table; v2 runs append
- [ ] One full run recorded: 19 questions times 3 runs, with the result against the bar (90% overall, 100% injection and refusal) and the run files saved
- [ ] No key printed or saved in any run file
