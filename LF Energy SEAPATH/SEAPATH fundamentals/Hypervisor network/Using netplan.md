
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Using netplan

## **Reconfiguring the network entirely with netplan**

It is possible to redefine the SEAPATH network entirely using [netplan.io](https://netplan.io/) yaml files. This behavior is achieved by the variable `netplan_configurations`  in the inventory. Examples are provided in the Ansible repository.

Below are some useful examples for using netplan:

- [SR-IOV configuration](https://netplan.readthedocs.io/en/stable/examples/#how-to-configure-sr-iov-virtual-functions)
- [Configuring a Linux bridge with vlans](https://computingforgeeks.com/configuring-linux-bridge-vlan-using-netplan-ubuntu/)
- [Official documentation](https://netplan.readthedocs.io/en/stable/)

> [!IMPORTANT]
> For now, using netplan disables all network configuration on SEAPATH. Everything, including the administration and cluster network, has to be handled by netplan yaml files.
>
> The goal would be to be able to define the network entirely, either with systemd-networkd directly or with netplan, but this is not done now.

## **Creating an OVS bridge with Netplan**

Seapath supports the creation of an OVS bridge directly from a Netplan configuration file. To do so, you can use the Netplan configuration example file located in Seapath Ansible inventories directory.

In the following example, we create an OVS bridge connected to the physical interface pointed by `ovs_ext_interface` inventory variable, defined in the hypervisor inventory. All the network stream coming from this interface will be redirected to this bridge. This configuration can be useful in the case you want to share the network stream coming on one interface to multiple virtual port, and so virtual machines.

```text
# Copyright (C) 2024 Savoir-faire Linux, Inc.
# SPDX-License-Identifier: Apache-2.0
network:
version: 2
renderer: networkd
openvswitch:
protocols: [OpenFlow13, OpenFlow14, OpenFlow15]
ethernets:
{{ ovs_ext_interface }}: {}
bridges:
ovs0:
interfaces: [{{ ovs_ext_interface }}]
openvswitch:
protocols: [OpenFlow10, OpenFlow11, OpenFlow12]
```

After applying the Netplan configuration using `netplan apply` command, you can identify the created OVS bridge (here ovs0) with command `ip a`:

```bash
root@minisforum:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
2: enp2s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
link/ether 58:47:ca:72:49:50 brd ff:ff:ff:ff:ff:ff
3: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master ovs-system state UP group default qlen 1000
link/ether 58:47:ca:72:49:51 brd ff:ff:ff:ff:ff:ff
4: enx782d7e14367c: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel master br0 state UP group default qlen 1000
link/ether 78:2d:7e:14:36:7c brd ff:ff:ff:ff:ff:ff
7: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
link/ether fa:f7:2f:2c:1b:b8 brd ff:ff:ff:ff:ff:ff
inet 192.168.216.74/24 brd 192.168.216.255 scope global br0
valid_lft forever preferred_lft forever
8: wlp4s0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
link/ether 38:d5:7a:25:d4:2d brd ff:ff:ff:ff:ff:ff
9: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
link/ether 02:42:a2:71:7b:7e brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
10: ovs-system: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
link/ether 1e:86:fb:0e:ff:7c brd ff:ff:ff:ff:ff:ff
11: ovs0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
link/ether 58:47:ca:72:49:51 brd ff:ff:ff:ff:ff:ff
```

You can also confirm the creation of the OVS bridge using `ovs-vsctl` show:

```bash
root@minisforum:~# ovs-vsctl show
db96c66c-2cfb-40d0-bbcb-10038eb1e6fb
Bridge ovs0
fail_mode: standalone
Port enp3s0
Interface enp3s0
Port ovs0
Interface ovs0
type: internal
ovs_version: "3.1.0"
```

> [!IMPORTANT]
> `enp3s0` is the interface pointed by `ovs_ext_interface`.
