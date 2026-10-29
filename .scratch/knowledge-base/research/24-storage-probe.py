"""T24 evidence probe: fake model, read-only current graph, disposable SQLite memory.

Run from the repository root:
    uv run --directory backend python ../.scratch/knowledge-base/research/24-storage-probe.py
No provider calls; does not write to the real investigation memory or knowledge base.
"""

import asyncio
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "backend"))

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig

from api.settings import Settings
from login_investigator import agent, investigations, knowledge_base
from tests.test_agent import FakeModel, tool_call


def storage(memory, path):
    # Include intermediate writes and the checkpoint payload separately; the SQLite file's
    # allocated pages alone do not show whether the same evidence is repeated in saved state.
    rows = {}
    for table, column in (("checkpoints", "checkpoint"), ("writes", "value")):
        count, size = memory.conn.execute(
            f"SELECT count(*), coalesce(sum(length({column})), 0) FROM {table}"
        ).fetchone()
        rows[table] = {"rows": count, "payload_bytes": size}
    memory.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    rows["file_bytes"] = path.stat().st_size
    return rows


async def main():
    settings = Settings.from_env()
    started = time.perf_counter()
    async with knowledge_base.open_current_knowledge_base(
        settings.dataset_dir, settings.knowledge_base_state,
    ) as kb:
        if kb is None:
            raise RuntimeError("Build the knowledge base before running this probe")
        preparation = time.perf_counter() - started
        responses: list[BaseMessage] = [item for i in range(50) for item in (
            tool_call("lookup_account", {"account_id": "amelia.ward"}, f"lookup-{i}"),
            AIMessage("Amelia Ward belongs to IT and IT Admins."),
        )]
        model = FakeModel(responses=responses)
        with tempfile.TemporaryDirectory(prefix="li-t24-storage-") as folder:
            path = Path(folder) / "memory.sqlite"
            memory = investigations.open_memory(path)
            config: RunnableConfig = {"configurable": {"thread_id": "storage-probe"}}
            try:
                memory.setup()
                configured = agent.build_agent(model, memory, kb)
                samples = {"0": storage(memory, path)}
                for number in range(1, 51):
                    configured.invoke({"messages": [{"role": "user", "content": "Who owns amelia.ward?"}]}, config)
                    if number in (1, 10, 50):
                        samples[str(number)] = storage(memory, path)
                checkpoint = memory.get_tuple(config)
                assert checkpoint is not None
                artifacts = [m.artifact for m in checkpoint.checkpoint["channel_values"]["messages"]
                             if isinstance(m, ToolMessage)]
                artifact_bytes = len(json.dumps(artifacts[0], sort_keys=True).encode())
            finally:
                memory.conn.close()
            reopen_start = time.perf_counter()
            memory = investigations.open_memory(path)
            try:
                restored = memory.get_tuple(config)
                assert restored is not None
                restored_artifacts = [m.artifact for m in restored.checkpoint["channel_values"]["messages"]
                                      if isinstance(m, ToolMessage)]
                assert restored_artifacts == artifacts
                reopen_seconds = time.perf_counter() - reopen_start
            finally:
                memory.conn.close()
        print(json.dumps({"graph_preparation_seconds": round(preparation, 4),
                          "artifact_json_bytes": artifact_bytes,
                          "saved_artifacts_after_50": len(artifacts), "samples": samples,
                          "reopen_seconds": round(reopen_seconds, 4)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
