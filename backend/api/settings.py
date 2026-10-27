"""Configuration from environment variables, so the eval runner can isolate a run. The defaults are
the core's own paths, so v2 runs on v1's data with nothing set. The two API keys are not read here:
the core reads them where it uses them, as in v1. The dashboards and the agent's tools read the
same `dataset_dir` and `reputation_dir`: startup hands the loaded log to the tools (ticket 22).
`knowledge_base_state` is the build command's pointer file, which the staleness guard reads.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from login_investigator import knowledge_base
from login_investigator.generator import DATASET_DIR
from login_investigator.investigations import MEMORY_PATH
from login_investigator.reputation import SAVED_DIR


@dataclass(frozen=True)
class Settings:
    dataset_dir: Path
    memory_path: Path
    reputation_dir: Path
    knowledge_base_state: Path

    @classmethod
    def from_env(cls, environ: Mapping[str, str] = os.environ) -> Settings:
        def path(name: str, default: Path) -> Path:
            value = environ.get(name, "").strip()
            return Path(value) if value else default

        return cls(
            dataset_dir=path("LI_DATASET_DIR", DATASET_DIR),
            memory_path=path("LI_MEMORY_PATH", MEMORY_PATH),
            reputation_dir=path("LI_REPUTATION_DIR", SAVED_DIR),
            # Read from the module at call time, so the test run's guard can replace it.
            knowledge_base_state=path("LI_KNOWLEDGE_BASE_STATE", knowledge_base.STATE_FILE),
        )
