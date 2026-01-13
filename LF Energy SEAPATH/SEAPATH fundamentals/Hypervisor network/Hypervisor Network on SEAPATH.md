
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Hypervisor Network on SEAPATH

A SEAPATH machine is connected to different networks:

- An **administration** network to access all the physical and virtual machines
- A **PTP** network, where the PTP frames are sent to time synchronize the machines
- One or multiple **OT** networks depending on the chosen substation architecture
- Optionally, a **cluster** network if machines form a cluster

## Administration network

This network is used to access the hypervisor with SSH.

If you manage multiple physical machines (ex: cluster), we recommend using a switch to connect all of them to the same administration network.

To avoid using too many interfaces, the administration of all VMs running on the hypervisor can use the same physical NIC as the hypervisor administration.  
This is possible by using a Linux or OVS bridge and connecting all VMs and the hypervisor to it.

> [!IMPORTANT]
> This behavior is achieved by the br0 bridge, which is default on SEAPATH. See the next page for more information.

## PTP network

The management of the PTP network is not covered by SEAPATH. However, all SEAPATH hypervisor need to be time synchronized with PTP.

The PTP synchronization has to be received on a dedicated physical network interface on each hypervisor.

See [Time Synchronization](../Time%20Synchronization.md) for more information

## **OT network (How to connect VIEDs)**

There are two main ways to transmit data from a physical network interface to a virtual machine:

- **virtual interfaces**: A virtual NIC (Network Interface Card) is created inside the virtual machine. The data must be passed from the physical NIC of the hypervisor to the virtual NIC of the VM. This is the preferred way for non-time-critical data (ex: MMS)
- **Physical access**: The VM uses directly a physical network card of a hypervisor. This is the preferred way for time-critical data (ex: Sampled Values, GOOSE)

Using virtual interfaces necessitates creating a bridge. SEAPATH offers two kinds of bridges: Linux bridges or Open vSwitch bridges. The bridge must first be created on the hypervisor, then the VM must be connected to it.

Bridge creation is explained on [Network configuration and deployment](Network%20configuration%20and%20deployment.md)

VM connection to bridges or physical access to network cards is explained on [Connect a virtual machine to the network](../../Deploy%20your%20application%20on%20SEAPATH/Deploying%20virtual%20machines/Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)

## Cluster network

This network allows the physical machines of a cluster (hypervisor/observer) to communicate together to handle the high availability feature.

This network is entirely separated from the administration network so that the cluster is still functional if the administration is down.

Two physical network interfaces per hypervisor are necessary for the cluster.

More information on [High availability cluster](../High%20availability%20cluster.md)
