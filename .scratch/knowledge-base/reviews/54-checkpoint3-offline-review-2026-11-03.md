# T54 checkpoint 3 offline adapter review

Date: 3 November 2026. Baseline: `ffcce01674f504710c99a771b423b1f7d7cc3f56` plus this
session's working-tree additions. Review method: mp-code-review, two independent read-only
agents, followed by re-reviews of the fixes. Nothing committed or pushed in this session.

## Standards

Initial findings: malformed nested API output escaped the adapter's error contract and lost
reported billing information; the admin manual still described only the dry-run adapter.
Both corrected. Judgment calls: configuration labels controlled protocol behaviour, and
error-type classifications were duplicated. Mapping now follows the model identifier, and
the HTTP worker leaves classification to the adapter.

Final reviewer result: zero remaining standards findings. The manual describes live commands
as fake-tested and pending remote verification. B-148 retains the review iterations.

## Spec

Initial findings: malformed output lost partial/charge evidence; preparation could consume
the case clock while leaving a stale dispatch allowance; paid review notices were only
retrospective; two DeepInfra configurations used broad provider names. Corrected with safe
validation, recalculated dispatch allowance, bounded paid commands and review pauses, related
cost context, and the `deepinfra/bf16` endpoints already identified in approved research.

Re-review found HTTP errors discarded available billing telemetry and linked repair slot 73
would first execute pending original slots 25–72. Corrected by retaining sanitized HTTP
failure responses and adding `--reruns-only`. Fake regressions cover both.

Final reviewer result: zero remaining blocking spec findings. Native settings and live
Langfuse behaviour remain unverified; remote evidence and full regression acceptance are
separate completion gates.

## Evidence and limits

- Final comparison suite: 143 passed in 122.09 seconds.
- Frozen fixtures: current. Backend lint: clean. Backend Pyright: zero errors.
- Frontend type check: clean. Full frontend: 149 passed, one known five-second Explorer
  Reset timeout. Focused Explorer: seven passed, same timeout. Chart size warnings retained.
- Final full one-worker frontend rerun: 150 passed in 277.21 s, no frontend changes.
- Full backend `pytest -q -x`: 137 passed, then one B-147 image-name setup error in 392.02 s.
  The earlier retag workaround returned Docker HTTP 500. Full backend acceptance remains
  incomplete. The image is still present by ID; no running containers remain.
- No real OpenRouter request or live Langfuse upload. No agent behaviour/application model
  change, no exam gold or threshold change, and no paid application eval run.

Standards: zero remaining findings. Spec: zero remaining blocking findings.
