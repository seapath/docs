
[Getting started](../../Getting%20started.md) > [Prerequisites](../Prerequisites.md)

# Hardware requirements for SEAPATH machines

# Hypervisor

An hypervisor is a physical machine capable of running virtual machines. On SEAPATH, these machines must have :

- x86\_64 CPU architecture
- virtualization capability (Intel VT-x, AMD-V)
- UEFI (legacy BIOS is not supported)
- IOMMU (Intel VT-d or AMD SMD)

> [!NOTE]
> All these requirements should be fulfilled on any modern PC.

For a realistic production environment, it is recommended to have an IEC 61850 certified server

> [!IMPORTANT]
> For testing purposes, SEAPATH can run on standard servers or even on desktops

# High availability cluster

SEAPATH can enable high availability feature by using three physical machines in a cluster mode.

Read a comparative between cluster and standalone setup at [Standalone or cluster setup](../Standalone%20or%20cluster%20setup.md)

### Physical machines

A cluster can be built using three hypervisors. In that case, we recommend getting three of the same machine.

> [!IMPORTANT]
> Hybrid cluster using different machines is possible on SEAPATH, but some functionalities may not be supported.

A cluster can also be built using two hypervisors and one observer. This observer machine will not run any virtual machines and can then be less powerful to reduce the costs.

In any case, three Ethernet cables will be necessary to wire the machines together.

### Observer machine requirements

- x86-64
- UEFI

### Disks

SEAPATH can run on hardware or software RAID. However, the recommended setup is to use two physical disks per hypervisor in the cluster mode. One will host SEAPATH, and the other will be used by ceph.

The observer machine only needs one disk

# Recommended setup

For the best SEAPATH setup, we recommend purchasing three of the same IEC 61850 certified servers, and having two disks per machines.  
These machines will be put in cluster mode.
