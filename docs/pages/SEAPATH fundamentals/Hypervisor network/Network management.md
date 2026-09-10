
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Network management

All the SEAPATH network setup is handled by systemd-networkd. The network configuration files created by SEAPATH are located in `/etc/systemd/network`.

## Administration bridge

The br0 bridge created by default for the administration network is a standard Linux bridge. It can be investigated with the `brctl show` command

## Logs

All logs are accessible on the `systemd-networkd` systemd service.

## IP addresses

All the IP addresses on the hypervisor (Administration, cluster, or additional networks) should be visible with the `ip a` command.

## Cluster network

The team0 bridge of the cluster is handled by Open vSwitch. It can be inspected with the command `ovs-vsctl show`.
