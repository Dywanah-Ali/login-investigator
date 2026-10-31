"""Run synchronous work without abandoning its resource owner on cancellation."""

import asyncio
from collections.abc import Callable
from typing import TypeVar

T = TypeVar('T')


async def owned_operation(operation: Callable[[], T]) -> T:  # noqa: UP047 - Keep the existing explicit TypeVar contract.
    """Cancellation waits for the resource owner before cleanup may start."""
    task = asyncio.create_task(asyncio.to_thread(operation))
    try:
        return await asyncio.shield(task)
    except asyncio.CancelledError:
        while not task.done():
            try:
                await asyncio.shield(task)
            except asyncio.CancelledError:
                continue
            except Exception:  # noqa: BLE001 - Finish joining the failed worker, then preserve cancellation.
                break
        if not task.cancelled():
            task.exception()  # Retrieve a worker failure while preserving the cancellation.
        raise
