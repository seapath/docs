
[Getting started](../../Getting%20started.md) > [Prerequisites](../Prerequisites.md)

# Network requirements

# Network cards

Industrial servers come with embedded network interfaces. However, for advanced features, it is recommended to get additional network cards and plug them into the server.

## **Network technologies**

Optional technologies can be available on each network cards

- PTP (Precision time protocol)
- SR-IOV (Single-Root Input-Output Virtualization)
- PRP (Parallel Redundancy Protocol)
- PCI-passthrough

The time synchronization with PTP is required on SEAPATH. Be sure to get a network card compatible with **hardware PTP**.

SR-IOV PRP and PCI-passthrough features are not mandatory on SEAPATH, it depend on the user’s needs. See dedicated section [Hypervisor network](../../SEAPATH%20fundamentals/Hypervisor%20network.md)

> [!WARNING]
> If you plan to use PCI-passthrough, you must check that each network interface has its own IOMMU group.

## Number of interfaces

### Hypervisors

SEAPATH hypervisors require :

- One administration interface for SSH connection and Ansible
- One PTP interface for time synchronization
- Multiple IEC61850 interface to send and receive GOOSE/SV/MMS
- Two cluster interfaces to connect cluster machines together (not necessary in standalone configuration)

The total number of IEC 61850 interfaces depends on your needs. However, we recommend having at least 2. This brings the total number of interfaces to 4 in standalone and 6 in cluster

> [!IMPORTANT]
> If your machine doesn't have enough interfaces, you can use a USB-Ethernet interface. For example, the TRENDnet TU3-ETG was tested and does work natively on SEAPATH. These added interfaces will not be compatible with any of the additional network technologies described above (PTP, SR-IOV, PRP).

For more information on the possible network topologies, see [Hypervisor network](../../SEAPATH%20fundamentals/Hypervisor%20network.md)

### Observer

The observer will not run virtual machines, thus the IEC61850 interfaces are not required. However, administration, PTP, and cluster interfaces are necessary. This brings the total number of interfaces to 4.

Hardware PTP is also required for the observer

# Ethernet switches

One ethernet switch must be used to connect all administration interfaces of the cluster machines. This switch must have at least 4 interfaces.

One other switch must be used to handle the PTP and the IEC 61850 streams. This part of the setup falls under the substation infrastructure setup and is not directly covered in this wiki.

> [!IMPORTANT]
> For testing purposes, only one switch can be used to handle administration, PTP, and 61850 streams. The different parts can be separated with different VLANs. This requires a manageable ethernet switch.

# Internet access

Internet connection is not required on any of the SEAPATH machines. However, it is supported by SEAPATH and it is interesting to have this access during the testing phase.

# Recommended setup

Assuming a 3-hypervisor cluster setup, each machine should have at least 6 ethernet interfaces and hardware PTP support. This is usually the case for IEC 61850 certified machines.

Each machine should also have an empty slot for an additional network card. You can use it later to add an SR-IOV or PRP capable card, depending on your needs.

Two network switches should be used :

- The administration switch with at least 4 network interfaces
- The substation switch
