# T52: Model choices in comparable investigation systems

Date: 2 November 2026. Researcher: Codex, Astra.
Status: primary-source research; no model, provider, architecture or budget is selected.
Scope: published security-system choices plus current Anthropic/Google candidate tiers.
OpenAI and OpenRouter compatibility are inspected separately by the parent review.

Production-selection follow-up, 2 November: the parent verified OpenAI's
[deprecation schedule](https://developers.openai.com/api/docs/deprecations): GPT-4.1 is due
for API shutdown on 14 January 2027. The historical study choices below must not be treated
as a recommendation to begin a new production baseline on that model.

## Finding

There is evidence for capable general-purpose models, reasoning models and role-specific
model allocation. The inspected sources do not establish one industry-standard model or
mandatory provider mix. Published security results are stronger evidence than a generic
model tier description, but their datasets and decisions differ from this app's objective.

For the initial 12-answer architecture calibration, use one explicit model and compatible
reasoning settings across A, B and C. A is one investigator; B adds applicability analysis;
C adds independent review. These are the current protocol labels, superseding the candidate
labels in the earlier architecture research note. Heterogeneous role assignment should be a
later, separately labelled optimisation experiment. This is a research recommendation.

## Published choices and evidence strength

| System/source | What was actually disclosed | What it establishes and does not establish |
|---|---|---|
| [Microsoft DTDA, May 2026 paper](https://arxiv.org/html/2605.20896v1), §6 | GPT-4.1 was active in the measured production window. Offline gap recovery compared GPT-4.1 with GPT-5.4 on frozen incident snapshots, with three repetitions. GPT-5.4 improved reported recovery. No role-specific model/settings matrix was disclosed in the inspected text. | First-party deployed-system report plus offline model comparison. Supports testing reasoning quality with fixed evidence. It does not identify the current live model or a universal SOC baseline. |
| [AIDA, October 2026 paper](https://arxiv.org/html/2610.10608v1), §IV and §VI | Reference model `gpt-4.1-2025-04-14`; systematic-study temperature 0.2 except sampled Self-Consistency at 0.7. Full AIDA uses the same GPT-4.1 reference and alert set. Five open-weight alternatives are tested separately. No heterogeneous per-role allocation is reported. | Controlled research comparison, not a deployed industry standard. Its 300-alert ablation does not isolate a statistically significant benefit from the challenger alone. Qwen3.5 9B matches the reference confusion matrix on that subset, showing model size is not sufficient selection evidence. Generalisation outside the dataset family remains unproved. |
| [Google SOC reference architecture](https://docs.cloud.google.com/architecture/agentic-ai-orchestrate-security-ops-workflows), model selection | Coordinator, Tier 1 analyst and threat-intelligence researcher use Gemini. Guidance suggests thinking models such as Pro for complex decomposition and Flash for small/direct tasks. It does not pin a model/version to every role. | Official architecture guidance, not comparative model-quality evidence. It supports role-based optimisation in principle, not a specific selection for our evidence reviewer. |
| [Anthropic Research engineering report, June 2025](https://www.anthropic.com/research/multi-agent-research-system) | Claude Opus 4 lead with Sonnet 4 subagents in the reported comparison against single-agent Opus 4. More compute and context are part of that system. | A concrete heterogeneous production pattern, but broad research rather than security investigation. Historical model names and quality gains are not current recommendations or proof of isolated role-specialisation benefit. |

AIDA's live adjudicator is different from our proposed review specialist and from T30's
advisory evaluation judge. Its automatic classification authority is not adopted here.

## Current non-OpenAI candidates checked

These are provider descriptions and documented capabilities, not measured performance on our
cases. API catalogue presence does not prove account access or OpenRouter route compatibility.

| Candidate | Verified official description | Implication for consideration |
|---|---|---|
| `claude-opus-5-5` | Anthropic's current general starting recommendation, adaptive thinking always on, default medium effort, tool use. Listed standard price is $4 input/$20 output per million tokens. | A capable all-role calibration candidate if route, output format and cost checks pass. |
| `claude-sonnet-5-5` | Speed/intelligence tier, adaptive thinking, default high effort, tool use; $2/$10 per million tokens. | A lower-price comparison candidate, not automatically suitable for a reviewer merely because its task is narrow. |
| `claude-fable-5-1` | Demanding reasoning/long-horizon tier, adaptive thinking always on, default high effort; $10/$50 per million tokens. | A stronger reference candidate if cheaper models miss required judgments. |

Source for Claude rows: [official model overview](https://platform.claude.com/docs/en/models/overview).
Prices above are listed provider rates at inspection, not routed estimates or total run costs.

Google's [current catalogue](https://ai.google.dev/gemini-api/docs/models) lists stable
`gemini-4-argon` and `gemini-3.8-flash`. The [Argon page](https://ai.google.dev/gemini-api/docs/models/gemini-4-argon)
describes a flagship reasoning model; the [Flash page](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash)
describes a faster model for agentic/enterprise work. Both explicitly support function calling,
structured outputs and thinking levels low/medium/high. Their pages were updated 30 October.
No Google price or account availability claim is made here. The SOC architecture's generic
Pro/Flash guidance must not be mistaken for these exact models having passed a SOC benchmark.

## Role requirements and fair comparison

The following is our inference from the objective and evidence above:

- **Investigator/front agent:** multi-source synthesis, uncertainty, instruction-following,
  citations and supported structured outputs. It needs reasoning capacity, not just routing.
- **Applicability specialist:** nuanced identity/time/context matching and partial explanations.
  A bounded context does not make this simple extraction. Exact comparisons remain code-owned.
- **Review specialist:** evidence-based challenge without reflexive disagreement or false
  reassurance. Use the same model initially; different context is the tested intervention.
- **Evaluation judge:** remains advisory and follows the separately agreed cross-family policy.
  Giving the live reviewer a different family would change another variable and requires its
  own experiment; it is not automatically required by the evaluation-judge policy.

Freeze the model ID/version, provider route, reasoning effort, allowed parameters, output limits
and prompts for calibration. Do not equate identical effort labels across vendors with equal
compute. Same-model architecture comparisons still have extra-call/token confounds; report them.
Avoid assuming temperature zero is supported or makes a model deterministic. Validate exact
parameter and structured-output behaviour on the chosen route before the scored runs.

After architecture evidence exists, test cheaper or cross-family specialists one role at a time
against unchanged cases. Preserve regression and injection checks. None of these sources
establishes that the current app's GPT-4o-mini is adequate for the expanded objective, nor
requires replacing the working app before isolated calibration.

## Method and limits

Read eight primary pages through official-site/paper browsing. No vendor tenant, API inference
or benchmark was executed. Perplexity was unavailable in this child context. Source models
are dated examples; current model descriptions are vendor guidance. No exact role model is
an industry consensus. This note supplies candidates and controls for the author's decision.
