
[Deploy your application on SEAPATH](../../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../../Deploying%20virtual%20machines.md) > [Third party virtual machines](../Third%20party%20virtual%20machines.md)

# ABB - SSC600 SW

### Requirements

To run the SSC600 SW VM in SEAPATH, the **SSC600 SW package** has to be downloaded from the ABB website. A **license** is also needed to run the software. Find more information in the [dedicated webpage](https://new.abb.com/medium-voltage/digital-substations/protection-relays/multiapplication/smart-substation-control-and-protection-ssc600-sw).

### Deploy the VMs

A template xml *ssc600.xml.j2* is provided in the ansible repository. There is also example inventories in the [*inventory/provider/abb* directory](https://github.com/seapath/ansible/tree/main/inventories/providers/abb).

The following variables configure the template:

|  Variable                |  Required    |  Type         |  Comments                                                                                                                           |
|:-------------------------|:-------------|:--------------|:------------------------------------------------------------------------------------------------------------------------------------|
| description              | No           | String        |                                                                                                                                     |
| uuid                     | No           | Int           |                                                                                                                                     |
| cpuset                   | Yes          | Array of int  | A minimum of 4 CPUs is required                                                                                                     |
| memory                   | No           | Int           | (GiB). The default and minimum required is 6                                                                                        |
| emulatorpin              | Yes          | Int           |                                                                                                                                     |
| vm\_disk                 | Yes          | String        | The disk image can be in *raw* or in *qcow2*. More information in the [disk](#disk) section.                                        |
| bridges                  | No           | Dict          | `name` (String) and `mac_address` (String) must be defined. In competition with `ovs` bridge. Use for the rear interface in the VM. |
| process\_bus\_interfaces | No           | Array of dict | `name` (String), `mac_address` (String) and `mode` (String) must be defined.                                                        |
| protection\_ports        | No           | Dict          | The interface PCI address used for SVs. <br/> `domain` `bus` `slot` `function`                                                      |

### Disk

The VM can be deployed in two format:

- gzipped raw disk (default from ABB)

  - `vm_disk`: link to the img.gz from the SSC600 SW package. Must be extracted and converted to qcow2 format using `qemu-img`. Refer to [qemu documentation](https://www.qemu.org/docs/master/tools/qemu-img.html).)

### Hypervisor configuration

Following the ABB documentation about the SSC600 SW, some configurations are required to improve the global performance.

- A minimum of 4 isolated CPUs in a RT kernel is needed. More information in [Real time virtual machine configuration](../Virtual%20machines%20deployment/Real%20time%20virtual%20machine%20configuration.md)
- Hugepages should be enabled. For a 6GiB dedicated memory, 6 pages of 1GiB must be reserved.

  - This can be done with the following variable in the inventory `grub_append: "default_hugepagesz=1G hugepagesz=1G hugepages=6"`
- The PTP is passed using `ptp_kvm` and the ptp status is reported to the VM using a vsock. The `ptp_interface` must be declared in the inventory. More information in [Time synchronization configuration](../../../SEAPATH%20fundamentals/Time%20Synchronization/Time%20synchronization%20configuration.md) .
- The NIC affinity can be configured in the `nic_affinity` variable.
- A qemu hook is provided in the ABB package, this sould be added in each hypervisor using the `upload_files` variable.

### Tested configuration

The VM has been tested in the following SEAPATH configuration:

- Yocto SEAPATH standalone
- Debian SEAPATH standalone
- Debian SEAPATH cluster (3 hypervisors)
- Yocto SEAPATH cluster (3 hypervisors)

### Not yet supported

- The live migration cannot be done due to macvtap / PCI pass-through configuration. It isn't supported by qemu for now.
- The L3 cache partionning asked in the ABB documentation is not yet implemented and will require test to check the impact in SEAPATH.
