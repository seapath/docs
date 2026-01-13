
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Use Open vSwitch bridges on SEAPATH

SEAPATH provides wrappers to define the network of a machine inside an Ansible inventory.

- For systemd-networkd, this wrapper mostly uses the `custom_network` and `custom_netdev` variables (see [network\_systemdnetworkd](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_systemdnetworkd/) role documentation).
- For Open vSwitch (OVS) bridges, the `ovs_bridges` variable is used, along with the role [network\_configovs](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_configovs/).

## Create an additional OVS bridge

An OVS bridge can be useful to connect virtual VM interfaces to physical interfaces of the hypervisor.

All bridges must be described under the `ovs_bridges` variable. Additional ports can be added to the bridge at its creation.

```java
ovs_bridges:
  - name: ovsbr
    ports:
      - name: VM1.0 # Tap interface to connect a future VM to the bridge
        type: tap
      - name: ovsbr_ext # External physical interface to connect to the bridge
        interface: eno1
```

The bridge is then created by the `network_configovs` role, which is included by default on the `seapath_setup_main` playbook.

See the full documentation of the `ovs_bridges` variable on the [network\_configovs](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_configovs/) role documentation.

> [!NOTE]
> It is not mandatory to create a tap interface for a VM to connect on, as Libvirt is capable of creating them itself with the VM. Read [Connect a virtual machine to the network](../../Deploy%20your%20application%20on%20SEAPATH/Deploying%20virtual%20machines/Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)  
> Creating the tap interface manually is useful for interface customization.

## Create an extended bridge over the cluster

Virtual machines can migrate on different hypervisors on the cluster. In order for them to communicate with each other, no matter their position on the cluster, one OVS extended bridge has to be created.

Full documentation of this feature on the dedicated page : [Create an extended bridge over the cluster](../High%20availability%20cluster/Create%20an%20extended%20bridge%20over%20the%20cluster.md)

## **Connect a virtual machine to an OVS bridge**

The connection of a VM to the OVS bridge is configured inside the Libvirt XML file.

Full documentation on the dedicated section [Connect a virtual machine to the network](../../Deploy%20your%20application%20on%20SEAPATH/Deploying%20virtual%20machines/Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)

## Infrastructure management

Internally, the `ovs_bridges` variable is transformed into a JSON configuration file by the `network_configovs` role.

This configuration file is then located at `/etc/ovs_configuration.json`. The bridge itself is created by the `seapath-config_ovs` systemd service.

All the **logs** are available in the service output.
