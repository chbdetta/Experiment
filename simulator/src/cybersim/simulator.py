"""Core simulation primitives."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Iterable, Iterator, List, Optional

from .flow import FlowRecord
from .topology import Link, NetworkTopology


@dataclass(frozen=True)
class TrafficEvent:
    """Represents a single simulated traffic observation."""

    timestamp: datetime
    src: str
    dst: str
    protocol: str
    byte_count: int
    replayed: bool


class NetworkSimulator:
    """Generate network traffic events from a topology and seed flows."""

    def __init__(
        self,
        topology: NetworkTopology,
        seed_flows: Iterable[FlowRecord],
        random_state: Optional[random.Random] = None,
    ) -> None:
        self.topology = topology
        self.seed_flows: List[FlowRecord] = list(seed_flows)
        self.random = random_state or random.Random()
        self._flows_by_edge: Dict[tuple[str, str], List[FlowRecord]] = {}
        for flow in self.seed_flows:
            self._flows_by_edge.setdefault((flow.src, flow.dst), []).append(flow)

    def replay(self) -> Iterator[TrafficEvent]:
        """Yield the seed flows in chronological order."""

        for flow in sorted(self.seed_flows, key=lambda f: f.timestamp):
            yield TrafficEvent(
                timestamp=flow.timestamp,
                src=flow.src,
                dst=flow.dst,
                protocol=flow.protocol,
                byte_count=flow.byte_count,
                replayed=True,
            )

    def generate(
        self,
        duration: timedelta,
        start_time: Optional[datetime] = None,
        average_interval: timedelta = timedelta(seconds=5),
    ) -> Iterator[TrafficEvent]:
        """Stochastically generate synthetic events.

        The generator performs a simple biased random walk over the topology where
        edge weights provide transition probabilities. When an edge is selected, a
        seed flow on that edge is sampled (if available) to determine protocol and
        byte counts.
        """

        current_time = start_time or datetime.utcnow()
        end_time = current_time + duration
        nodes = list({flow.src for flow in self.seed_flows} | {flow.dst for flow in self.seed_flows})
        if not nodes:
            return

        active_node = self.random.choice(nodes)
        while current_time <= end_time:
            neighbors = self.topology.neighbors(active_node)
            if not neighbors:
                active_node = self.random.choice(nodes)
                continue

            link = self._choose_link(neighbors)
            flow = self._sample_flow(link)

            jitter = average_interval.total_seconds() * self.random.uniform(0.5, 1.5)
            current_time += timedelta(seconds=jitter)
            if current_time > end_time:
                break

            yield TrafficEvent(
                timestamp=current_time,
                src=link.src,
                dst=link.dst,
                protocol=flow.protocol if flow else "TCP",
                byte_count=flow.byte_count if flow else int(self.random.expovariate(1 / 5000) + 100),
                replayed=False,
            )

            active_node = link.dst

    def _choose_link(self, links: List[Link]) -> Link:
        weights = [link.weight for link in links]
        total = sum(weights)
        if total <= 0:
            return self.random.choice(links)
        threshold = self.random.random() * total
        cumulative = 0.0
        for link in links:
            cumulative += link.weight
            if cumulative >= threshold:
                return link
        return links[-1]

    def _sample_flow(self, link: Link) -> Optional[FlowRecord]:
        candidates = self._flows_by_edge.get((link.src, link.dst))
        if not candidates:
            return None
        return self.random.choice(candidates)
