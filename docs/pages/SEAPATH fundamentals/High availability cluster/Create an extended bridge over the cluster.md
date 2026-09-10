
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [High availability cluster](../High%20availability%20cluster.md)

# Create an extended bridge over the cluster

On SEAPATH, the virtual machines can migrate on the different hypervisors. If there is a need for two VMs to communicate with each other, a standard Linux bridge cannot be used because the location of both VMs on the cluster can change.

The solution is then to use an extended bridge over the cluster using OpenvSwitch and VXLAN. This bridge will use the physical cluster network and will be accessible no matter the position of the VMs on the cluster.

# Extended bridge deployment

The deployment of the bridge is as follow:

1. The bridge to deploy is first described as an Ansible inventory.
2. This inventory is transformed into a configuration file through the role [network\_configovs](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_configovs).
3. This configuration file is copied on the SEAPATH machines in `/etc/ovs_configuration.json`
4. This configuration file is read by the `seapath-config_ovs` systemd service at each boot.
5. This service calls [python3-setup-ovs](https://github.com/seapath/python3-setup-ovs), which launches the Open vSwitch commands.

> [!IMPORTANT]
> The extended bridge is only deployed on the hypervisors, as the observer doesn’t run any virtual machines.

## Deploy the bridge using Ansible

Below is an example inventory to deploy an extended bridge over the cluster. This inventory

- Creates a brBRIDGE1 bridge
- Configure VXLAN interfaces on this bridge to communicate with the other hypervisors on the cluster
- Configure RSTP on this bridge to avoid a network loop
- Configure two tap interfaces for VMs on this bridge

> [!NOTE]
> This example showcases only two standard tap interfaces for virtual machines. It is possible to add more interfaces, use VLAN features, use DPDK, or link this bridge to physical interfaces, so that it is accessible from outside the cluster. See the [network\_configovs](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_configovs) role for details.

```java
cluster_machines:
  children:
    hypervisors:
      vars:
        ovs_bridges:
          - name: brBRIDGE1
            rstp_enable: true
            other_config: "rstp-priority={{ br_rstp_priority | default(16384) }}"
            ports:
              - name: "brBRIDGE1_next"
                type: vxlan
                key: "1001"
                remote_ip: "{{ cluster_next_ip_addr }}"
              - name: "brBRIDGE1_previous"
                type: vxlan
                key: "1001"
                remote_ip: "{{ cluster_previous_ip_addr }}"
              - name: VM1.0
                type: tap
              - name: VM2.0
                type: tap
```

> [!IMPORTANT]
> This inventory can be merged with the cluster inventory or handled as a separate inventory.  
> In any case, it should always be used along with the cluster one, as it uses some Ansible variables defined in there (RSTP priority and cluster IP)

This bridge can be deployed using the `seapath_setup_network.yaml` playbook.

## Connect the virtual machine on this bridge

The VM can then be connected on the bridge using the templated `guest.xml.j2` libvirt XML file.

```java
vm:
  vm_template: "../templates/vm/guest.xml.j2"
  vm_disk: <your_vm_disk_path>
  ovs:
    - mac_address: "52:54:00:e4:ff:02"
      ovs_port: VM1.0
```

For more information on VM deployment and inventories, see [Connect a virtual machine to the network](../../Deploy%20your%20application%20on%20SEAPATH/Deploying%20virtual%20machines/Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)
