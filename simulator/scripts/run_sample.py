"""Run a short end-to-end demonstration of the simulator."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR / "src") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "src"))

from cybersim.data_loader import load_csv_flows
from cybersim.simulator import NetworkSimulator
from cybersim.topology import NetworkTopology


def main() -> None:
    flows = list(load_csv_flows(Path(__file__).resolve().parent.parent / "examples" / "sample_flows.csv"))
    topology = NetworkTopology.from_flow_records(flows)
    simulator = NetworkSimulator(topology=topology, seed_flows=flows)

    print("=== Replaying Seed Flows ===")
    for event in simulator.replay():
        print(event)

    print("\n=== Generating Synthetic Traffic ===")
    for event in simulator.generate(duration=timedelta(minutes=2)):
        print(event)


if __name__ == "__main__":
    main()
