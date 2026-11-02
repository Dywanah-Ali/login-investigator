# T52: Independent spending-enforcement check

Author ruling, 2 November 2026: the reservation proposal below is rejected and retained
as research history. Actual-cost tracking and spending reviews replace a hard-budget
enforcement design for this screen. Do not treat this note's proposed checks as a build gate.

Checked: 2 November 2026. Status: researched proposal, not implementation or paid-run approval.
Scope: US$25 shared allowance, sequential cases, 180-second requests and 600-second cases,
without evaluation-imposed token, call or retry count caps. No credentials, account access,
inference or settings changes were used.

## Conclusion

A configured US$25 key limit is a useful second safeguard, but the inspected documentation
does not establish a strict US$25 final-charge guarantee for a request admitted near that
limit. Retain the local reservation ledger proposed below. This conclusion is an inference
from the documented request-admission and settlement behaviour, not a measured overspend
or a claim that OpenRouter's key limit is broken.

## What the primary sources establish

| Evidence | Consequence for this screen |
|---|---|
| OpenRouter documents per-key limits and a separate in-flight estimate. Charges settle when requests finish. Its in-flight estimate uses a fixed completion estimate when no output cap is supplied, excludes non-token charges and applies only to some accounts. | Do not substitute that estimate for a proven worst-case cost bound for this run. Check actual account eligibility later. |
| Workspace budgets check current spend when a request arrives and block when the limit is met or exceeded. | A new request can be the one that crosses a threshold. No inspected text promises exact mid-request termination at US$25. |
| Streaming cancellation is documented for OpenAI, Anthropic and DeepInfra. Non-streaming cancellation does not stop full-response billing. | Use streaming for the timed runner and verify the actual transport closes at the deadline. Do not treat a timeout exception alone as cancellation evidence. |
| Final usage contains the account charge, native token counts and available reasoning/cache breakdowns. Generation metadata can be fetched later by ID. | Reconcile reservations against reported account charges, and retain unresolved reservations when terminal usage is lost. |

Sources: [credit and rate limits](https://openrouter.ai/docs/api_reference/limits),
[workspace budgets](https://openrouter.ai/docs/guides/features/workspaces/workspace-budgets),
[streaming and cancellation](https://openrouter.ai/docs/api_reference/streaming),
[usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting).

The [shared-agent-key guide](https://openrouter.ai/docs/guides/best-practices/capping-shared-agent-keys)
calls the key credit limit a hard cap. Treat that as the documented administrative control,
not additional evidence about maximum settlement overshoot. A non-resetting evaluation-only
key would isolate this screen's accounting if approved later. No new key is required or
created by this research. The [spend-controls source](https://raw.githubusercontent.com/OpenRouterTeam/docs/main/guides/best-practices/spend-controls.mdx)
also distinguishes pooled workspace budgets from per-key/member controls; it does not provide
the missing per-request final-charge guarantee. Its layer-order description differs from
the current Limits page; the proposed design does not depend on which error is checked first.

## Proposed local accounting rule

Before each underlying inference request, including retries, admit it only when:

`settled charges + unresolved reservations + new request reservation <= US$25`.

The new reservation must conservatively cover that route's complete possible bill. Use
verified native provider limits, the full serialized input including history/tool schemas,
the applicable price tier and all charge components. A provider's own maximum is a bound
for accounting, not a smaller evaluation-imposed output cap. If native input tokenization
cannot be bounded reliably, reserve against the native input/context maximum instead.
Do not assume cache hits, promotional discounts or throughput estimates will reduce cost.
Do not count reasoning twice when already included in output usage.

Keep the reservation after a timeout, process crash or missing usage. Replace it with the
actual charge only after a credible settlement record is obtained. If the maximum cannot
be bounded, pause admission and resolve that gap. Sequential cases reduce overlap but do
not remove unresolved charges from earlier requests. A retry can therefore be blocked by
budget even though there is no retry-count cap. Label that outcome budget-limited.

This is an engineering proposal. It does not assert that the reservation assumptions are
already verified, or that 72 uncapped attempts fit US$25. A conservative bound may pause
the run before the balance is fully spent. The US$15 review remains separate from admission.

## Checks still needed before execution

- Verify exact route prices, native ceilings, long-context tiers, mandatory output parameters
  and reasoning billing. Parent research owns the price snapshot.
- Establish whether any enabled tool/plugin or cache-write path adds charges. Include them
  in reservations or explicitly leave them outside the approved runner configuration.
- Verify observable request attempts, streaming cancellation and generation-ID retention
  through the selected adapters. HTTP success alone does not establish successful generation.
- Test ledger persistence/recovery and duplicate-charge reconciliation locally before paid work.
- Decide how to isolate this run from unrelated account usage and account for charge records
  missing generation IDs. Do not infer this run's cost from a shared account balance alone.
- Reconcile charged dollars rather than upstream provider-cost fields. Usage fields and
  final settlement can be absent after transport failure; missing is not zero.

Method: inspected official web documentation. Spend-controls HTML failed in this independent
lookup; the official OpenRouterTeam raw documentation supplied its contents. No runtime
claim follows from documentation review.
