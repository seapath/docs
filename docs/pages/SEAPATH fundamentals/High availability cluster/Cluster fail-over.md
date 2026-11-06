
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [High availability cluster](../High%20availability%20cluster.md)

# Cluster fail-over

When a node fault is detected, and the resource is considered as unavailable, many actions scenarios can be done to recover it. The choice of the scenario depends of how the resource is deployed and constraint along the cluster (collocation, banned nodes…).

On SEAPATH the strategy of nodes and resources recover is done by the virtual domain resource agent.

# Migration to another cluster node

This scenario is the default SEAPATH cluster behavior when a node is unavailable. The deployed resource is migrated to another working node. These type of fail-over can occurred in various cases: hypervisor crash, network cut, etc.

## Cold migration

The resource is firstly stop (if possible), and restarted to another valid cluster node, through the cluster network. Persistent resource datas are kept as there are deployed across the cluster, but the live state of the resource is lost.

All active connections will be closed and resource will be available again until it is fully started on the new node.

> [!NOTE]
> The migration time is mainly bottle-necked by the the speed rate of the network cluster.

## Live migration (also called hot-migration)

The resource is migrated from a node to another without needing to stop it. The live state of the resource is kept and a minimal downtime occurs (a few seconds). All active connections are kept alive.

This type of migration needs a precise and reliable time synchronization between the host using at least NTP protocol. It is also recommended that the migrated resource (specially VMs) is time synchronized, to avoid time gap.

Live migration might not be compatible if the resource has hardware dependencies to the node. When using PCI-Passthrough, be sure that the PCI address of the shared device is the same between the all the nodes where resource can be deployed. SR-IOV can also be used to address hardware dependencies.

If the resource has pinned CPUs configured using host pass-through, the same CPU cores must be available on the host where the resource is migrated.

# Reboot the resource on the same node

In some configuration, specially when colocation or node bans constraints are defined the only way to get the resource available is to restart the resource on the same failed node.

# Fencing

The fencing is the process of isolating a failing node of the cluster to avoid any data corruption and miscellaneous, using the [STONITH](https://en.wikipedia.org/wiki/Fencing_(computing)#STONITH) method. The isolation is done by a power cut of the node itself to prevent it drastically to run anything on the cluster.

The fencing can be implemented using a Switched Power Distribution Unit (PDU), capable of dialoging with Pacemaker.

> [!WARNING]
> We do not recommend to use IMPI technology (iDRAC, etc) to implement fencing, as it can lead to non-deterministic state of the node.

On SEAPATH, fencing with STONITH can be configured using this [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/configure_ha/).
