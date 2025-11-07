"""Utilities for loading network-flow datasets."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator, Optional

from .flow import FlowRecord


def load_csv_flows(
    path: Path | str,
    timestamp_key: str = "timestamp",
    src_key: str = "src",
    dst_key: str = "dst",
    protocol_key: str = "protocol",
    byte_count_key: str = "bytes",
    timestamp_format: Optional[str] = None,
) -> Iterator[FlowRecord]:
    """Load flow records from a CSV file."""

    with Path(path).open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield FlowRecord.from_dict(
                row,
                timestamp_key=timestamp_key,
                src_key=src_key,
                dst_key=dst_key,
                protocol_key=protocol_key,
                byte_count_key=byte_count_key,
                timestamp_format=timestamp_format,
            )
