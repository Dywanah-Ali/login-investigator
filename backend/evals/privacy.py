"""Secret filtering shared by local evaluation records and outbound payloads."""
from __future__ import annotations

import json
import os
import re
from typing import Any

REDACTED = "[REDACTED]"
SECRET_ENV = ("OPENROUTER_API_KEY", "ABUSEIPDB_API_KEY", "LANGFUSE_SECRET_KEY",
              "LANGFUSE_PUBLIC_KEY", "LI_PG_PASSWORD", "LI_PG_READER_PASSWORD",
              "LI_GRAPH_ADMIN_PASSWORD", "LI_GRAPH_READER_PASSWORD")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)(bearer\s+)[^\s\"']+"),
    re.compile(r"(?i)(authorization[\"']?\s*[:=]\s*[\"']?)[^\s\"',}]+"),
)


def redact(value: Any, secrets: list[str] | None = None) -> Any:
    """Remove known secret values and key-shaped strings from any JSON-ready value."""
    secrets = sorted({s for s in (secrets if secrets is not None else _env_secrets()) if s},
                     key=len, reverse=True)
    if isinstance(value, str):
        # SDK attributes and saved request artifacts may already contain JSON. Decode
        # before filtering so escaped quotes/backslashes cannot hide a configured secret.
        try:
            decoded = json.loads(value)
        except (ValueError, RecursionError):
            decoded = None
        if isinstance(decoded, (dict, list, str)):
            clean = redact(decoded, secrets)
            if clean != decoded:
                return json.dumps(clean, ensure_ascii=False)
        for secret in secrets:
            value = value.replace(secret, REDACTED)
        for pattern in SECRET_PATTERNS:
            value = pattern.sub(lambda m: (m.group(1) if m.groups() else "") + REDACTED, value)
        return value
    if isinstance(value, dict):
        return {redact(k, secrets): redact(v, secrets) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [redact(v, secrets) for v in value]
    return value


def _env_secrets() -> list[str]:
    return [os.environ[name] for name in SECRET_ENV if os.environ.get(name)]
