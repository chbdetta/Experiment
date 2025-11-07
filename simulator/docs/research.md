# Research Notes: Cybersecurity Network Simulation

## Open-source simulators and emulators

| Project | Highlights | Notes for CyberSim |
|---------|------------|--------------------|
| **[ns-3](https://www.nsnam.org/)** | Discrete-event network simulator with extensive protocol models and support for flow-level tracing. | Can serve as a high-fidelity reference implementation. CyberSim can export generated topologies or traffic patterns for replay inside ns-3 for validation. |
| **[Mininet](http://mininet.org/)** | Emulates networks using lightweight virtualization; integrates well with SDN controllers. | Useful for hardware-in-the-loop experiments. CyberSim can output controller scripts or flow tables derived from synthetic traffic. |
| **[GNS3](https://www.gns3.com/)** | Graphical network emulator supporting real router images and appliances. | Heavyweight but helpful for validating attack playbooks on vendor-specific firmware. |
| **[CORE](https://www.nrl.navy.mil/itd/ncs/products/core)** | Container-based real-time network emulator developed by the U.S. Naval Research Laboratory. | Provides Python API for programmatic topology control similar to CyberSim's goals. |
| **[Shadow](https://shadow.github.io/)** | Parallel discrete-event simulator optimized for Internet-scale experiments. | Offers plugin system for application models; relevant when simulating large botnets. |
| **[Scapy](https://scapy.net/)** | Packet crafting framework. | While not a simulator, Scapy can be paired with CyberSim to craft packets that match generated flow events. |

## Public network-flow datasets for bootstrapping

| Dataset | Description | Access |
|---------|-------------|--------|
| **[CIC-IDS 2017](https://www.unb.ca/cic/datasets/ids-2017.html)** | Comprehensive intrusion detection dataset with labeled benign and malicious flows captured over multiple days. | Provides CSVs of network-flow features suitable for seeding CyberSim's topology. |
| **[MAWI Working Group Traffic Archive](https://mawi.wide.ad.jp/mawi/)** | Long-running packet trace archive from a trans-Pacific link. | Requires conversion from pcap to flow format; offers realistic background traffic. |
| **[DARPA Transparent Computing Engagement 3](https://github.com/darpa-i2o/TransparentComputing)** | System activity traces with network-flow components capturing red-team operations. | Useful for modeling adversarial behavior sequences. |
| **[LANL Unified Host and Network Dataset](https://csr.lanl.gov/data/2017.html)** | Massive authentication and network-flow logs from a large enterprise environment. | Ideal for topology bootstrapping and attack-path analysis. |
| **[UNSW-NB15](https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/)** | Hybrid of real and synthetic traffic with labeled attacks. | Provides NetFlow-like features that can seed simulator events. |

## Recommended next investigations

1. Implement adapters that translate the above datasets into `FlowRecord` objects while preserving labels (benign vs. attack).
2. Incorporate protocol-aware payload generation using frameworks such as [Impacket](https://github.com/SecureAuthCorp/impacket) for realistic SMB/DCERPC traffic synthesis.
3. Evaluate integration with reinforcement-learning environments (e.g., OpenAI Gymnasium) so agents can interact with the simulator via standardized APIs.
