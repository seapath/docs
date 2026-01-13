
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Network configuration and deployment

This page explains the configuration and extensions points provided by the SEAPATH Ansible repository regarding networking. The technical description of all the variables is explained on the associated Ansible Galaxy web page for each role.

## Administration

The administration network primarily consists of one IP address on one physical network interface on the hypervisor. These are configured with the mandatory variables `ansible_host` and `network_interface`.

Although the IP address is not directly assigned to the network interface, it is assigned through through a Linux bridge named br0. By default:

- The br0 bridge is created
- The interface `network_interface` is added on that bridge
- The IP address `ansible_host` of the machine is statically assigned to the bridge

All the configuration and customization of the administration network on a SEAPATH hypervisor is done in the [network\_systemdnetworkd](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_systemdnetworkd/) role.

> [!IMPORTANT]
> To avoid SEAPATH creating the br0 bridge, use the variable `network_simple`. However, be aware that no IP will be assigned to the machine on the administration network then.
>
> To assign an IP address manually, use the `custom_network` variable.

## Additional OT networks

### Create an additional Linux bridge

A second bridge can be useful to connect a physical interface to the virtual interface of a VM. This can be achieved in any configuration by using the `custom_network` and `custom_netdev` variables.

Here is an example to create a br1 bridge with IP address 10.10.1.100/24. The bridge is then created by the `network_systemdnetworkd` role, included in the `seapath_setup_main` playbook.

```java
custom_netdev:
  70-br1: # Create the br1 bridge
    - NetDev:
      - Name: br1
      - Kind: bridge
custom_network:  
  70-br1: # Assign IP address to the bridge (optional)
    - Match:
      - Name: b1
    - Network:
      - Address: "10.10.1.100/24"
```

See complete documentation of these variables on the [network\_systemdnetworkd](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_systemdnetworkd/) role.

> [!IMPORTANT]
> To connect a virtual machine to this bridge, see TODO

### Create an Open vSwitch bridge

Similarly to a Linux bridge, an additional Open vSwitch bridge can be created. This is described on [Use Open vSwitch bridges on SEAPATH](Use%20Open%20vSwitch%20bridges%20on%20SEAPATH.md)

## Cluster

The cluster network is handled by Open vSwitch. One bridge named `team0` is created on each cluster machine with the associated IP address of the machine on the cluster.

Three variables are necessary to build the cluster:

- `cluster_ip_addr` is the IP address of the physical machine on the cluster
- `team0_0` and `team0_1`are the network interfaces connected to the two other cluster machines

The creation and the customization of the cluster network is handled by the [network\_clusternetwork](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_clusternetwork/) role.

> [!NOTE]
> The ring topology of the cluster enforces the usage of the RSTP protocol to prevent network loops. The priority of each machine is handled by the `br_rstp_priority` variable.

> [!IMPORTANT]
> Even though the cluster network is created by the `network_clusternetwork` role, each IP address on the cluster network is handled by `network_systemdnetworkd`.

For more information about cluster setup, read [Cluster configuration](../High%20availability%20cluster/Cluster%20configuration.md)

## Iptables

SEAPATH provides a way to deploy a custom set of iptables rules. Read the [iptables role documentation](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/iptables/) for more information.

This role is included in the `seapath_setup_network.yaml` playbook.

## Troubleshooting

### Lose access to the machine when executing Ansible network role

If access to the machine is lost when rebooting or restarting systemd\_networkd after modifying the network, this likely points to a misconfiguration on the administration network. There is no automatic rollback mechanism on SEAPATH in that case. You should connect to your hypervisor manually or with remote access to modify the IP address on the administration network.
