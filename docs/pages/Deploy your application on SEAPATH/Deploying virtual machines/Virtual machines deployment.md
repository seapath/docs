
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../Deploying%20virtual%20machines.md)

# Virtual machines deployment

Two files are needed to deploy a virtual machine on SEAPATH:

- The disk in [qcow2](https://www.qemu.org/docs/master/interop/qcow2.html) format, where the data of the VM is stored
- The Libvirt XML file that defines the hardware to emulate for the VM

> [!IMPORTANT]
> This section doesn’t explain how to create the qcow2 disk. More information at [Software provider - How to deploy your application](../Software%20provider%20-%20How%20to%20deploy%20your%20application.md)

## Ansible VM deployment

All VMs to deploy must be configured inside the `VMs` Ansible group

> [!NOTE]
> We advise creating a separate inventory for the VMs to avoid side effects when launching playbooks

Each VM host must contain, at minimum, two variables:

- `vm_disk`: The location of the qcow2 file on the administration machine
- `vm_template`: The location of the Libvirt XML file on the administration machine

The `vm_template` variable can point either directly to a Libvirt XML file, or to a jinja2 templated Libvirt XML file. The templated file is useful to customize the VM inside the Ansible inventory instead of modifying the XML directly.

SEAPATH provides two Libvirt XML templates:

- `guest.xml.j2` for a basic configurable VM
- one for the [ABB - SSC600 SW](Third%20party%20virtual%20machines/ABB%20-%20SSC600%20SW.md) virtual machine.

> [!IMPORTANT]
> The `guest.xml.j2` Libvirt XML file was specifically configured to work on SEAPATH with or without real time performances. It should be able to deploy almost all Linux UEFI VMs; it is thus the recommended XML to use.
>
> For all other usages, you will have to write your own non-templated Libvirt XML file

### Use a templated Libvirt XML (guest.xml.j2)

SEAPATH provides a templated Libvirt XML file located in the Ansible repository at `templates/vm/guest.xml.j2`

Multiple variables are available directly in the VM inventory to customize this template and specify VM characteristics such as names, IP addresses, CPU settings, and more. The full documentation is located in the [deploy\_vms\_standalone](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/deploy_vms_standalone/) and [deploy\_vms\_cluster](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/deploy_vms_cluster/) role documentation.

> [!IMPORTANT]
> For a virtual machine with determinism and performance needs, we recommend using both the "isolated" and "rt" feature. For more information, refer to [Real time virtual machine configuration](Virtual%20machines%20deployment/Real%20time%20virtual%20machine%20configuration.md)

> [!NOTE]
> Note that the `guest.xml.j2` template relies only on a UEFI boot-loader for the VMs. If your VM uses legacy BIOS, you must create your own Libvirt XML file.

An example inventory is provided on the [Ansible GitHub repository](https://github.com/seapath/ansible/blob/main/inventories/examples/seapath-vm-deployement.yaml).

If your VM has real-time needs, refer to [Real time virtual machine configuration](Virtual%20machines%20deployment/Real%20time%20virtual%20machine%20configuration.md)

To connect your VM to the different SEAPATH networks, refer to [Connect a virtual machine to the network](Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)

### Use a non-templated Libvirt XML file

Standard Libvirt XML files can be used directly with the `vm_template` variables, without any additional information in the VM inventory.

To create your Libvirt XML file, refer to <https://libvirt.org/formatdomain.html>

> [!WARNING]
> When deploying a VM on the SEAPATH cluster, do not include disk management in your Libvirt XML.
>
> The disk of the VM is automatically replicated on the Ceph storage and the XML modified to include Ceph RBD communication. More information at [The vm_manager tool](The%20vm_manager%20tool.md)

If your VM has real-time needs, refer to [Real time virtual machine configuration](Virtual%20machines%20deployment/Real%20time%20virtual%20machine%20configuration.md)

To connect your VM to the different SEAPATH networks, refer to [Connect a virtual machine to the network](Virtual%20machines%20deployment/Connect%20a%20virtual%20machine%20to%20the%20network.md)

### Define location and co-location constraint for the VMs (cluster only)

When deploying VMs on the cluster, it is possible to select a mandatory or preferred hypervisor to run on (location rules). It is also possible to select VMs that must run on the same machine (co-location rules).

All these rules can be defined in the VM inventory using the `cluster_vm` module.

Pacemaker meta, params and utilization can also be defined there.

See the `cluster_vm` module [role documentation](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/module/cluster_vm/) for more information.

## Deployment

To deploy your VMs on SEAPATH machines, you can call

- `playbooks/deploy_vms_cluster.yaml`, for a deployment on a SEAPATH cluster

```bash
ansible-playbook -i inventories/cluster_inventory.yaml -i inventories/vm_inventory.yaml playbooks/deploy_vms_cluster.yaml
```

- `playbooks/deploy_vms_standalone.yaml`, for deployment on a SEAPATH standalone machine

```bash
ansible-playbook -i inventories/standalone_inventory.yaml -i inventories/vm_inventory.yaml playbooks/deploy_vms_standalone.yaml
```

### Advanced playbook with the cluster\_vm Ansible module

The *cluster\_vm* Ansible module is a wrapper above the vm\_manager command line interface. It serves as an Ansible connection to deploy VMs on SEAPATH.  
It is primarily used inside the `deploy_vms_standalone` and `deploy_vms_cluster` roles.

It can also be called directly from custom playbooks to perform actions on VMs. For instance, an example playbook that removes a VM on the cluster:

```java
- name: Remove vm1
  cluster_vm:
    name: vm1
    command: remove
```

Playbooks can be executed on any hypervisor.

The complete documentation of `cluster_vm` is at <https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/module/cluster_vm/>

> [!IMPORTANT]
> `cluster_vm` is a wrapper around the vm\_manager command line interface. All actions of vm\_manager can be done with this module.
>
> More information at [The vm_manager tool](The%20vm_manager%20tool.md)
