
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [High availability cluster](../High%20availability%20cluster.md)

# Cluster management

# Cluster network

The cluster network is a separate network. It does not interact with the administration network, nor with [Cluster maintenance](Cluster%20maintenance.md) that the user can deploy on SEAPATH.

This machine is named “team0” on SEAPATH and is handled by Open vSwitch. Each of the three physical machines of the cluster has an IP address on this cluster network.

You can see all Open vSwitch bridges with the command

```java
ovs-vsctl show
```

# Shared storage (Ceph)

The mechanism of shared storage and replication is handled by Ceph. Internally, Ceph is handled by daemons. There are three main types of daemons:

- OSDs are actually storing the data.
- Monitors (MON) are monitoring the cluster and managing the redundancy
- Manager, a single daemon for all the cluster to take decisions

> [!IMPORTANT]
> More information about Ceph clusters is on the [Ceph documentation](https://docs.ceph.com/en/pacific/rados/). Note that SEAPATH is currently using the Ceph 16 (Pacific) version.

On SEAPATH,

- All machines run one monitor
- All hypervisors run one OSD (the observer doesn’t host any replicated data)
- The manager is auto elected by the cluster

## Interacting with Ceph

The overall status of Ceph on the cluster can be seen with the status command. This will show you the OSDs, monitors, and the manager of the cluster. It will also give you the health and the data storage of the cluster.

```java
ceph status
```

The logs for Ceph are accessible in `/var/log/ceph` and are stored by daemons.

> [!IMPORTANT]
> Internally, Ceph uses systemd services to run its daemons. You can look at their status with systemctl command. For example: `systemctl status ceph-mon@<machine_name>`

## SEAPATH usage

SEAPATH uses Ceph to replicate the disks of the virtual machines. The disks of the virtual machines deployed on the cluster can be seen with:

```java
rbd ls
```

Additional metadata are also replicated, like the Libvirt XML file. More information on the page [The vm_manager tool](../../Deploy%20your%20application%20on%20SEAPATH/Deploying%20virtual%20machines/The%20vm_manager%20tool.md)

# Pacemaker and corosync

From a machine point of view, the cluster is formed and handled by Pacemaker and Corosync.

- Corosync handles the cluster at the physical machine level. Cluster machines are then able to know that each other exists, and know the capability of each (ex: running virtual machines).
- Pacemaker handles the software resources and their location over the cluster (i.e., on which physical machine the resource is actually running).

On SEAPATH, each of the three machines of the cluster is a Corosync node. Pacemaker then uses the capability of each node (virtualization, computational power, number of resources already running on the machines) to schedule the resources.

## Interact with corosync/pacemaker

The status of the cluster can be seen with the following command. This will list the physical machine's status and all resources currently running on the cluster.

```java
crm status
```

Pacemaker logs can be found at `/var/log/pacemaker`

> [!WARNING]
> Pacemaker only handles the high level scheduling of resources. If you need more precise logs, you should check the underlying tool called by Pacemaker. For example, `/var/log/libvirt/qemu` for virtual machines.

## SEAPATH usage

When interacting with resources, Pacemaker relies on an OCF script file. This file defines the possible commands (start, stop, manage …) and their behavior.  
On SEAPATH, a custom OCF file script is used for virtual machines. This one can be found at `/usr/lib/ocf/resource.d/seapath/VirtualDomain`.

When defining location and colocation rules on virtual machines, these rules are managed by Pacemaker as constraints. You can list the constraints of a resource with the following command. More information about constraints on the [Pacemaker documentation](https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Explained/html/constraints.html).

```java
crm resource constraints <resource_name>
```

# Troubleshooting

## Ceph warning: Clock skew detected

This indicates that the physical machines are not synchronized correctly. It is not a fatal error, but will degrade the cluster’s performances over time.

Check the time synchronization of all your physical machines . Refer to [Time synchonization management](../Time%20Synchronization/Time%20synchonization%20management.md) for details.

## Cluster machines not displayed on the status

All three physical machines should be shown on both the `ceph status` and `crm status` command.

If it is not the case, verify that all machines are correctly powered on and that no Ethernet cables are missing or disconnected on the cluster network.

If the problem persists, verify the cluster network variables in the Ansible inventory and redeploy it using the `seapath-setup-network.yaml` playbook.
