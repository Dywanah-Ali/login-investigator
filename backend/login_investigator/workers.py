"""Run synchronous work without abandoning its resource owner on cancellation."""

import asyncio
from collections.abc import Callable
from typing import TypeVar


T = TypeVar('T')


async def owned_operation(operation: Callable[[], T]) -> T:
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
            except Exception:
                break
        if not task.cancelled():
            task.exception()  # Retrieve a worker failure while preserving the cancellation.
        raise
