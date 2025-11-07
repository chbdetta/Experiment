"""Network topology data structures and utilities."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Tuple

from .flow import FlowRecord


@dataclass(frozen=True)
class Node:
    """Represents a single endpoint in the simulated network."""

    identifier: str


@dataclass(frozen=True)
class Link:
    """Represents a directional connection between two nodes."""

    src: str
    dst: str
    weight: float


class NetworkTopology:
    """Graph-like structure describing network connectivity."""

    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[Tuple[str, str], Link] = {}

    def add_node(self, identifier: str) -> Node:
        node = self._nodes.get(identifier)
        if node is None:
            node = Node(identifier=identifier)
            self._nodes[identifier] = node
        return node

    def add_link(self, src: str, dst: str, weight: float = 1.0) -> Link:
        key = (src, dst)
        if key in self._edges:
            existing = self._edges[key]
            weight += existing.weight
        link = Link(src=src, dst=dst, weight=weight)
        self._edges[key] = link
        self.add_node(src)
        self.add_node(dst)
        return link

    def nodes(self) -> Iterator[Node]:
        return iter(self._nodes.values())

    def links(self) -> Iterator[Link]:
        return iter(self._edges.values())

    def neighbors(self, identifier: str) -> List[Link]:
        return [link for link in self._edges.values() if link.src == identifier]

    @classmethod
    def from_flow_records(
        cls, records: Iterable[FlowRecord], normalize: bool = True
    ) -> "NetworkTopology":
        """Build a topology by aggregating flow records.

        Parameters
        ----------
        records:
            Iterable of :class:`FlowRecord` objects.
        normalize:
            Whether to normalize edge weights to sum to 1 per source node.
        """

        volume_by_edge: Dict[Tuple[str, str], int] = defaultdict(int)
        for record in records:
            volume_by_edge[(record.src, record.dst)] += record.byte_count

        topology = cls()
        if not normalize:
            for (src, dst), volume in volume_by_edge.items():
                topology.add_link(src, dst, weight=float(volume))
            return topology

        volume_by_src: Dict[str, int] = defaultdict(int)
        for (src, _), volume in volume_by_edge.items():
            volume_by_src[src] += volume

        for (src, dst), volume in volume_by_edge.items():
            total = volume_by_src[src]
            weight = volume / total if total else 0.0
            topology.add_link(src, dst, weight=weight)

        return topology

    def to_adjacency(self) -> Dict[str, Dict[str, float]]:
        adjacency: Dict[str, Dict[str, float]] = defaultdict(dict)
        for link in self.links():
            adjacency[link.src][link.dst] = link.weight
        return dict(adjacency)

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"NetworkTopology(nodes={len(self._nodes)}, links={len(self._edges)})"
