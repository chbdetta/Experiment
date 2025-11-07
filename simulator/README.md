# CyberSim: Network Security Experimentation Workspace

CyberSim is a lightweight, extensible workspace for building agent-based cybersecurity experiments. The initial milestone focuses on simulating network traffic traces that resemble the artifacts produced by cyber attacks. Future iterations will allow autonomous agents to execute offensive and defensive tactics inside the simulated environment.

## Key capabilities

* **Topology bootstrapping** – Generate a network graph from historical network-flow records.
* **Traffic replay & synthesis** – Reproduce past flows and stochastically generate new traffic based on learned communication patterns.
* **Extensibility** – Compose detectors, attack playbooks, and scoring routines on top of the simulator core.

## Getting started

1. Create a virtual environment with Python 3.10+.
2. Install the project in editable mode if desired:

   ```bash
   pip install -e .[dev]
   ```

3. Explore the example script:

   ```bash
   python scripts/run_sample.py
   ```

   The script loads a small CSV of network-flow records, builds a topology, and produces a short sequence of simulated traffic events.

## Project layout

```
├── docs/               # Research notes and background reading
├── examples/           # Example datasets used for bootstrapping
├── scripts/            # Entry points that stitch the modules together
└── src/cybersim/       # Library code for the simulator
```

## Next steps

* Enrich the simulator with higher-fidelity protocol models and attack behaviors.
* Add evaluation harnesses so security agents can be scored automatically.
* Integrate additional open datasets to diversify topology bootstrapping.
