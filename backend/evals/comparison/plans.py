"""The approved screening configurations (T52, configuration approved 2 November 2026).

These are requested settings. Routes, model revisions and the effective application of reasoning
and sampling are unverified until each configuration's compatibility session; changes need an
explicit, recorded disposition, never silent substitution.
"""

from __future__ import annotations

from evals.comparison.adapters import ModelConfig

UNVERIFIED = "requested; route and effective settings unverified until the compatibility session"

SCREENING_CONFIGS = [
    ModelConfig(config_id="qwen3.8-27b", label="Qwen3.8-27B", model="qwen/qwen3.8-27b",
                provider="deepinfra", reasoning={"enabled": True, "effort": "medium"},
                sampling={"temperature": 1.0, "top_p": 0.95, "top_k": 20}, notes=UNVERIFIED),
    ModelConfig(config_id="gpt-oss-120b", label="gpt-oss-120b", model="openai/gpt-oss-120b",
                provider="deepinfra", reasoning={"effort": "medium"}, notes=UNVERIFIED),
    ModelConfig(config_id="deepseek-v4.1-flash-1017", label="DeepSeek V4.1 Flash 1017",
                model="deepseek/deepseek-v4.1-flash-1017", provider="deepinfra/fp8",
                reasoning={"enabled": True, "effort": "high"}, notes=UNVERIFIED),
    ModelConfig(config_id="gpt-6-luna", label="GPT-6 Luna", model="openai/gpt-6-luna",
                provider="openai", reasoning={"effort": "medium"}, notes=UNVERIFIED),
    ModelConfig(config_id="claude-haiku-5.5", label="Claude Haiku 5.5",
                model="anthropic/claude-haiku-5.5", provider="anthropic",
                reasoning={"enabled": True, "mode": "adaptive", "effort": "medium"},
                notes=UNVERIFIED),
    ModelConfig(config_id="gpt-6.1-sol", label="GPT-6.1 Sol", model="openai/gpt-6.1-sol",
                provider="openai", reasoning={"effort": "medium"}, notes=UNVERIFIED),
]

SCREENING_CASES = ["O1-02", "O1-06", "O1-09", "O1-12-D"]
SCREENING_PASSES = 3
