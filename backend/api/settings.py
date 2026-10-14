"""Configuration from environment variables, so the eval runner can isolate a run. The defaults are
the core's own paths, so v2 runs on v1's data with nothing set. The two API keys are not read here:
the core reads them where it uses them, as in v1.

Not yet wired: the agent's tools read the core's default log and reputation folder, not
`log_path` and `reputation_dir`. Changing that touches the core's tools, so it has its own ticket
(22), done before the eval runner's API mode (18).
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from login_investigator.generator import LOG_PATH
from login_investigator.investigations import MEMORY_PATH
from login_investigator.reputation import SAVED_DIR


@dataclass(frozen=True)
class Settings:
    log_path: Path
    memory_path: Path
    reputation_dir: Path

    @classmethod
    def from_env(cls, environ: Mapping[str, str] = os.environ) -> Settings:
        def path(name: str, default: Path) -> Path:
            value = environ.get(name, "").strip()
            return Path(value) if value else default

        return cls(
            log_path=path("LI_LOG_PATH", LOG_PATH),
            memory_path=path("LI_MEMORY_PATH", MEMORY_PATH),
            reputation_dir=path("LI_REPUTATION_DIR", SAVED_DIR),
        )
