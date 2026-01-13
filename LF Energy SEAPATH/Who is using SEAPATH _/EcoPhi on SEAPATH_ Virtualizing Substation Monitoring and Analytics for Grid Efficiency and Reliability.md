
[Who is using SEAPATH ?](../Who%20is%20using%20SEAPATH%20_.md)

# EcoPhi on SEAPATH: Virtualizing Substation Monitoring and Analytics for Grid Efficiency and Reliability

## **Overview**

EcoPhi used the SEAPATH project from Linux Foundation Energy (LF Energy) to virtualize key substation monitoring and analytics functions including phasor measurement (PMU), power quality (PQM), disturbance recording (DFR), and partial discharge (PD) on a unified, real-time platform. By consolidating these traditionally hardware-based roles into a software-defined environment, EcoPhi demonstrated how digital substations can achieve deterministic performance, higher resilience, and lower total cost of ownership.

## **Context and Motivation**

Across global power systems, substations remain complex, hardware-heavy environments with limited visibility and delayed fault insight. Outages cost utilities more than 150 billion USD annually in the United States and over 300 billion globally, largely due to aging infrastructure, manual monitoring, and disconnected systems. Hardware-based modernization approaches that require new relays, recorders, and sensors per feeder would demand investments measured in trillions.

EcoPhi, a spinout from Chalmers University of Technology in Sweden, recognized with national innovation awards in Sweden, set out to address this through software-defined automation. The company has deployed its digital substation platform in more than 200 deployments worldwide, including projects in Sweden, the United States, and the Middle East.

## **Challenge**

Utilities face the dual challenge of maintaining deterministic real-time performance while reducing physical infrastructure. Conventional architectures rely on multiple point devices, each with its own wiring, commissioning, and maintenance cycle. This leads to extensive copper cabling and long build times, redundant hardware across PMU, PQM, DFR, and PD systems, and difficulty ensuring deterministic behavior for IEC 61869-9 Sampled Values and IEC 61850 GOOSE and MMS traffic. Integration is further complicated under PRP and PTP redundancy and time synchronization requirements.

EcoPhi’s goal was to consolidate these workloads into a single virtualized edge environment without sacrificing real-time responsiveness, interoperability, or reliability.

## **Solution**

EcoPhi implemented a SEAPATH-based architecture combining high-resolution merging units with edge virtualization to unify substation monitoring and analytics.

**QMU 800 Merging Unit**  
Samples up to 2 million samples per second with 24-bit resolution, supporting both conventional CT and VT and low-power sensors. Publishes Sampled Values compliant with IEC 61850 and 61869, with integrated GPS timing and PRP redundancy.

**CMPC 800 Edge Server**  
Hosts virtualized PQM, PMU, PD, DFR, and metering applications using SEAPATH as the deterministic real-time platform. SEAPATH provides orchestration, time synchronization, and fault tolerance across both virtual machines and containers.

Using CPU and IRQ pinning, NIC passthrough, and self-healing orchestration, EcoPhi maintained deterministic latency for critical functions. Continuous real-time PD monitoring and explainable AI analytics enabled predictive fault detection with meter-level accuracy. The system integrates with third-party vendor applications, enabling a multi-vendor, open ecosystem for digital substations.

## **Impact**

In a 20-feeder substation deployment, EcoPhi’s SEAPATH-based virtualization produced measurable results.

Hardware CAPEX was reduced by 60–70 percent through consolidation of monitoring devices. Copper and field wiring were cut by approximately 90 percent. Rack cabinets and floor space were reduced by 50–70 percent. Commissioning time shortened by 40–60 percent through standardized images and remote deployment. Maintenance OPEX fell by 30–40 percent with on-site interventions down 50–80 percent. Rack power and cooling decreased by 30–40 percent.

Predictive analytics identified 90 percent of predictable faults, avoided 67 percent of total faults, and localized issues with meter-level accuracy, with no false positives reported. These efficiencies translated to an estimated €1.5 million (currency as reported by EcoPhi) in substation build-cost reduction per site, a 40–50 percent first-year reduction in combined CAPEX and OPEX, and a projected 35–45 percent lower total cost of ownership over five years.

## **Technical and Operational Advancements**

By deploying SEAPATH, EcoPhi unified high-resolution sampled data, analytics, and AI-driven prediction within a single deterministic environment.

Key advancements include continuous zero-downtime PD monitoring with trend analysis and classification, virtualized PQ and phasor measurements that meet Class A and Class P/M requirements with tighter trigger thresholds than the standard minimum, explainable AI models that provide transparent reasoning for fault prediction, integration of GIS and SCADA data for transformer capacity and dynamic line rating calculations, and software-based upgrades in place of hardware replacements as standards evolve.

Together, these capabilities establish a scalable, field-proven foundation for digital substations, reducing both operational risk and lifecycle cost.

## **Future Roadmap**

EcoPhi’s roadmap builds on SEAPATH to extend from monitoring to protection and fleet-level operations. Upcoming developments include deployment of containerized protection functions such as distance, line differential, transformer, and busbar protection, automation from SLD to SCL to orchestration enabling one-click bay deployment, enhanced determinism through TSN, DPDK, and PRP-aware self-healing orchestration, extended cybersecurity aligned to IEC 62351 including MACsec and IPsec, signed images, and zero-trust access, deeper observability tools for latency and jitter SLAs and trace-based root cause analysis, expansion of predictive analytics and digital-twin replay for protection setting validation, multi-site fleet management, brownfield retrofit playbooks, and formal certification under IEC 60255, EMC, KEMA, and UL.

Field pilots are already testing line differential protection over 5G, marking the next stage of converged protection and control.

## **About EcoPhi**

EcoPhi AB is a technology company headquartered in Sweden, specializing in software-defined substation automation, grid monitoring, and AI-driven predictive analytics. Founded in 2014 as a spinout from Chalmers University of Technology, EcoPhi develops solutions that unify data, computation, and control across the electrical grid.

Its flagship products, the QMU 800 merging units and CMPC 800 edge servers, enable real-time virtualization of power quality, phasor measurement, disturbance recording, and partial discharge functions. Deployed in more than 200 deployments worldwide, EcoPhi’s platforms help utilities modernize operations, reduce lifecycle cost, and improve reliability through open, interoperable, and future-ready architectures.

Learn more at [ecophi.ai](https://ecophi.ai/)
