
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../Deploying%20virtual%20machines.md)

# Virtual machines management

## Manipulate VMs

The main tool to interact with VMs on SEAPATH is vm\_manager. It works either in standalone mode or in a cluster.

Below is a list of basic vm\_manager commands for VM management. Full documentation at [The vm_manager tool](The%20vm_manager%20tool.md)

All these commands can be executed on any SEAPATH machine of the cluster (if using acluster), no matter where the VMs are running.

### List the VMs deployed on the cluster (or the standalone machine)

```java
sudo vm-mgr list
```

### Get the state of a VM

```java
sudo vm-mgr status -n <vm_name>
```

### Get the Libvirt XML file of the VM

```java
sudo vm-mgr get_metadata --metadata_name xml -n <vm_name>
```

### Access the console of the VM

```java
sudo vm-mgr console <vm_name>
```

### Manipulate VMs with a REST API

A rest API is available for vm\_manager, read more at [The vm_manager tool](The%20vm_manager%20tool.md)

## Pacemaker usage

Pacemaker handles the location and constraints of the VMs on the cluster.

### See the locations of the VMs on the cluster

```java
crm status
```

### Verify VM constraints configuration

```java
crm configure show vm
```

For more information, see the [crm usage documentation](https://documentation.suse.com/sle-ha/15-SP7/html/SLE-HA-all/cha-ha-manage-resources.html).

## Location of the VM disk

On a standalone machine, by default, the disk is located in `/var/lib/libvirt/images`

Note that this may be overridden if you change the `deploy_vms_standalone_disk_pool` in Ansible.

On a cluster machine, the disk is replicated on CEPH RBD.

## Migrate a virtual machine

```bash
crm resource move <vm_name> <hypervisor_name>
```

## Logs

The logs of a VM are only available **on the hypervisor that schedules the VM** in `/var/log/libvirt/qemu/<vm_name>.log`

Additional logs are available on journald `journalctl -u libvirtd`

Logs related to VM migration can also be found in `/var/log/pacemaker/pacemaker.log`

## Modify the XML of a VM

To modify the XML of the VM we recommend going through a VM update process. Read [Update a virtual machine](Update%20a%20virtual%20machine.md)

## Time synchronization on virtual machines

Refer to [Virtual machine Time Synchronization](../../SEAPATH%20fundamentals/Time%20Synchronization/Virtual%20machine%20Time%20Synchronization.md)
