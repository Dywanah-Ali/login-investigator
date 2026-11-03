# T54: six initial live compatibility sessions

Date: 3 November 2026. Author authorised these six sessions after the handoff.
Scope: initial compatibility only. No screening, linked rerun, live Langfuse upload,
application change or model selection. Existing configuration and budget approvals retained.

## Result

All six sessions completed their tool round trip. Five passed the literal answer contract.
gpt-oss returned the right fact with different citation delimiters, so its contract failed.
Do not describe six completed sessions as six fully compatible configurations.

| Configuration | Tool round trip | Output contract | Seconds | Known cost US dollars |
|---|---|---|---:|---:|
| Qwen3.8-27B | Pass | Pass | 8.203 | 0.000378900 |
| gpt-oss-120b | Pass | Fail | 12.417 | 0.000031536 |
| DeepSeek V4.1 Flash 1017 | Pass | Pass | 3.766 | 0.00006600496 |
| GPT-6 Luna | Pass | Pass | 4.806 | 0.000044800 |
| Claude Haiku 5.5 | Pass | Pass | 10.520 | 0.000166600 |
| GPT-6.1 Sol | Pass | Pass | 6.435 | 0.000896000 |

The runner reports aggregate known cost **US$0.001584**. Two HTTP 429 responses during
gpt-oss have no cost or usage, and no generation ID. They remain unknown, not zero.
The table's extra precision preserves per-configuration returned charges; the runner rounds
the aggregate. Fourteen HTTP requests were recorded: twelve successes and two rate-limit
responses. Both rate-limit responses recovered through the approved runner retry policy.
Neither a new provider nor a fallback was used. No US$15 spending checkpoint was reached
on known charges. This is not an exact account-billing reconciliation.

## Diagnosis and settings limits

- gpt-oss final answer: `The colour code stated in record CMP-1 is **7**【CMP-1】.`
  The prompt explicitly requested `[CMP-1]`. The raw saved output contains the different
  delimiters, so this is model output noncompliance, not a display transformation or a
  failed tool response. The existing literal check correctly rejects it. B-150/AUD-079
  retain the failure. No check was loosened, prompt changed or favourable retry taken.
- Both gpt-oss errors identify DeepInfra's shared upstream pool as temporarily rate-limited
  (`engine_overloaded`). Successful requests on both sides of the tool exchange used the
  approved provider. Availability under longer screening remains unproven.
- Returned identities match the requested model families and providers on all successes.
  Selected endpoint metadata reports Qwen `qwen/qwen3.8-27b-20260814`, gpt-oss
  `openai/gpt-oss-120b`, DeepSeek `deepseek/deepseek-v4.1-flash-20261017`, Luna
  `openai/gpt-6-luna-20260922`, Haiku `anthropic/claude-haiku-5.5-20261007` and Sol
  `openai/gpt-6.1-sol-20260929`. gpt-oss exposes no dated revision here. Provider metadata
  does not independently attest precision or weight identity.
- Responses report the requested efforts, `service_tier: default` and no explicit output
  cap (`max_output_tokens: null`). Luna/Sol also report standard reasoning mode and
  `all_turns`. Qwen reports temperature 1 and top_p 0.95; its requested top_k 20 is not
  returned. Others report temperature/top_p 1 although no sampling override was sent.
  Generic returned fields do not prove native effective sampling, especially for models
  whose native reasoning interface ignores or omits sampling controls.
- Haiku returns enabled/medium, but not a native adaptive-thinking attestation. Qwen and
  gpt-oss effort forwarding likewise is not independently established by echoed fields.
  These observations support gateway acceptance, not proof of every native mapping.
- Reasoning items were returned by Qwen, gpt-oss, DeepSeek and Haiku on at least one turn.
  Luna/Sol returned none. Absence of exposed reasoning is not evidence that reasoning was
  disabled. Full returned output items were preserved and replayed on all six tool returns.
- This tiny connection check exercises tools and a plain-text citation contract, not a
  JSON-schema structured-output request, investigation quality, comparative speed or reliability.

## Local evidence and verification

Authoritative bundle: `backend/evals/comparison/runs/compat-live/` (git-ignored).
Manifest fixtures `f903b7f47620`; prompt version `c7a48ccf57f1`.
Each slot was dispatched separately with `--execute-paid --until-slot N`, N from 1 to 6,
and inspected before the next slot. No Langfuse mirror command was run.

- Frozen-fixture check passed before creation.
- Documented creation and six bounded live run commands completed.
- All 64 event artifact references matched their SHA-256 digests.
- All fourteen started requests have terminal records. All six first-turn outputs were
  present unchanged in the next tool-result request, including returned reasoning items.
- Configured OpenRouter and Langfuse credential values were absent from bundle files.
- No application tests rerun: this step changed documentation and produced isolated evidence.
- A read-only summary command hit the sandbox's uv-cache restriction. It was rerun using
  the existing backend virtual environment. No dependency or permission change was needed.

## Next gate

Review B-150/AUD-079 and the native-settings disclosure limits before authorising screening.
Keep the original gpt-oss failure. Any setup repair needs an explained, versioned change and
the approved affected-comparison policy. Do not repeat an unchanged request merely to obtain
a passing answer. Native-settings claims must remain limited to available evidence.
