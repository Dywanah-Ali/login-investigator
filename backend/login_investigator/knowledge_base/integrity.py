"""Domain result and refusal used by independent native graph reconciliation."""

from dataclasses import dataclass


class GraphIntegrityError(ValueError):
    """The graph cannot be trusted to represent its sources."""


@dataclass(frozen=True)
class GraphCounts:
    """Source counts per node type and per relationship."""
    nodes: dict[str, int]
    edges: dict[str, int]
