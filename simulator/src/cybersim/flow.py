"""Definitions related to network-flow records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Iterator, Mapping, Optional


@dataclass(frozen=True)
class FlowRecord:
    """A structured representation of a single network flow.

    Attributes
    ----------
    timestamp:
        Timestamp marking the beginning of the flow.
    src:
        Source node identifier (IP address, hostname, etc.).
    dst:
        Destination node identifier.
    protocol:
        Transport protocol used (e.g., TCP, UDP).
    byte_count:
        Number of bytes transferred during the flow.
    metadata:
        Optional dictionary containing additional attributes from the raw dataset.
    """

    timestamp: datetime
    src: str
    dst: str
    protocol: str
    byte_count: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        row: Mapping[str, Any],
        timestamp_key: str = "timestamp",
        src_key: str = "src",
        dst_key: str = "dst",
        protocol_key: str = "protocol",
        byte_count_key: str = "bytes",
        timestamp_format: Optional[str] = None,
    ) -> "FlowRecord":
        """Create a :class:`FlowRecord` from a dictionary.

        Parameters
        ----------
        row:
            Raw mapping obtained from CSV, JSON, or another source.
        timestamp_key, src_key, dst_key, protocol_key, byte_count_key:
            Keys expected in *row* for the corresponding attributes.
        timestamp_format:
            Optional ``strptime`` format string when the timestamp is stored as text.

        Returns
        -------
        FlowRecord
            Parsed flow instance.
        """

        timestamp_raw = row[timestamp_key]
        if isinstance(timestamp_raw, datetime):
            timestamp = timestamp_raw
        else:
            if timestamp_format:
                timestamp = datetime.strptime(str(timestamp_raw), timestamp_format)
            else:
                timestamp = datetime.fromisoformat(str(timestamp_raw))

        metadata = {
            key: value
            for key, value in row.items()
            if key
            not in {timestamp_key, src_key, dst_key, protocol_key, byte_count_key}
        }

        return cls(
            timestamp=timestamp,
            src=str(row[src_key]),
            dst=str(row[dst_key]),
            protocol=str(row[protocol_key]).upper(),
            byte_count=int(row[byte_count_key]),
            metadata=metadata,
        )


def iter_flow_records(
    rows: Iterable[Mapping[str, Any]],
    **kwargs: Any,
) -> Iterator[FlowRecord]:
    """Convert an iterable of raw mappings into :class:`FlowRecord` objects."""

    for row in rows:
        yield FlowRecord.from_dict(row, **kwargs)
