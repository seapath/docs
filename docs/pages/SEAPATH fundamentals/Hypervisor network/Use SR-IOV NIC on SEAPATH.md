
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Hypervisor network](../Hypervisor%20network.md)

# Use SR-IOV NIC on SEAPATH

**SR-IOV (Single Root I/O Virtualization)** is a PCI Express feature that enables a single physical device, called a **Physical Function (PF)**, to expose multiple lightweight, hardware-virtualized interfaces known as **Virtual Functions (VFs)**.  
Each VF appears as an independent PCI device with its own address, allowing direct assignment to virtual machines (VMs) through PCI passthrough.

On SEAPATH, SR-IOV can be used with supported **Network Interface Cards (NICs)** to create **virtual NICs (vNICs)** that provide:

- Very low latency (close to bare-metal performance),
- Hardware-level isolation between VMs,
- Efficient sharing of a single physical NIC among multiple VMs.

> [!WARNING]
> The NIC must explicitly support SR-IOV for these features to be available. Check the vendor documentation to confirm.

Configuring SR-IOV on SEAPATH involves two main steps:

1. **Creating vNICs (Virtual Functions) on the hypervisor**
2. **Attaching those vNICs to VMs**

> [!IMPORTANT]
> VFs creation is handled during the hypervisor's network configuration via Ansible.

## Hypervisor Configuration

### Basic VF Creation

The `sriov` variable, defined in your Ansible inventory, specifies which physical NICs (PFs) to use and how many VFs (vNICs) to create for each. This variable is a dictionary mapping the PF's interface name to the number of VFs desired.

**Example:**

```java
# Creates 2 VFs from eno1 and 7 VFs from eno3
sriov:
  eno1: 2
  eno3: 7
```

On Debian and CentOS, you must also specify the kernel module (driver) for the SR-IOV-capable NIC. This is done using the `sriov_driver` variable.

**Example:**

```java
sriov_driver: igb
```

Additionally, the Ansible automation will create a libvirt SR-IOV pool for each configured PF. These pools manage the available VFs. The pool name follows the format `sr-iov-net-<interface-name>`, for example, `sr-iov-net-eno1` or `sr-iov-net-eno3`.

### Verifying VF Creation

After the Ansible configuration is complete, you can verify that the VFs were created successfully on the hypervisor.

1. **Check** `sriov_numvfs`**:** You can check the number of configured VFs by reading the `sriov_numvfs` file for the physical interface (PF).

   ```bash
   cat /sys/class/net/eno1/device/sriov_numvfs
   ```

   This command should return the number you configured (e.g., `2` if you requested 2 VFs on `eno1`).
2. **List VFs with** `ip link`**:** You can also see the VFs listed as network interfaces, associated with their PF.

   ```bash
   ip link show eno1
   ```

   The output will list the VFs associated with `eno1` (e.g., `eno1v0`, `eno1v1`).

### Advanced VF Configuration (optional)

SR-IOV supports advanced features, such as assigning a VF to a specific VLAN, setting a MAC address, or enabling spoof checking.

On SEAPATH, these properties are configured by applying `systemd-networkd` settings directly to the VFs. This is managed through the top-level `custom_network` Ansible variable, which allows you to define custom `.network` files.

See the [role documentation](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_systemdnetworkd) on ansible galaxy for custom\_network syntax.

The following options are available:

|  **Variable**               |  **Description**                                                                                                                                                                                                                                                                                                                             |  **Type**                                   |
|:----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------|
| **VirtualFunction**         | Specifies a Virtual Function (VF), lightweight PCIe function designed solely to move data in and out. This option is compulsory.                                                                                                                                                                                                             | Takes an integer in the range 0…2147483646. |
| **VLANId**                  | Specifies VLAN ID of vNIC.                                                                                                                                                                                                                                                                                                                   | Takes an integer in the range 1…4095.       |
| **QualityOfService**        | Specifies quality of service of the vNIC.                                                                                                                                                                                                                                                                                                    | Takes an integer in the range 1…4294967294. |
| **VLANProtocol**            | Specifies VLAN protocol of the virtual function.                                                                                                                                                                                                                                                                                             | Takes `"802.1Q"` or `"802.1ad"`.            |
| **MACSpoofCheck**           | Controls the MAC spoof checking. When unset, the kernel’s default will be used.                                                                                                                                                                                                                                                              | `"yes"` or `"no"`                           |
| **QueryReceiveSideScaling** | Toggle the ability of querying the receive side scaling (RSS) configuration of the virtual function (VF). The VF RSS information like RSS hash key may be considered sensitive on some devices where this information is shared between VF and the physical function (PF). When unset, the kernel’s default will be used.                    | `"yes"` or `"no"`                           |
| **Trust**                   | Allows one to set trust mode of the virtual function (VF). When set, VF users can set a specific feature which may impact security and/or performance. When unset, the kernel’s default will be used.                                                                                                                                        | `"yes"` or `"no"`                           |
| **LinkState**               | Allows one to set the link state of the vNIC. Setting to “auto” means a reflection of the physical function (PF) link state, `"yes"` lets the VF to communicate with other VFs on this host even if the PF link state is down, `"no"` causes the hardware to drop any packets sent by the VF. When unset, the kernel’s default will be used. | `"yes"`/`"on"` , `"no"`/`"off"` or `"auto"` |
| **MACAddress**              | Specifies the MAC address for the virtual function.                                                                                                                                                                                                                                                                                          | Mac address (string)                        |

> [!IMPORTANT]
> It is often recommended to set LinkState to "on" (or "yes"). On some SR-IOV implementations, the physical link for a VF does not come up automatically when attached to a VM, and this setting ensures it is enabled.

### Full Hypervisor Configuration Example

This example combines the `hypervisor` variables with `custom_network` to configure VFs with advanced properties.

```java
hypervisor:
  sriov_driver: 'igb'
  sriov:
    eno2: 2 # Create 2 VFs on eno2
    eno3: 1 # Create 1 VF on eno3

custom_network:
   # Configuration file for eno2's VFs
  - 01-eno2_sriov:
    - Match:
      - Name: "eno2*"
		- SR-IOV:
			- VirtualFunction: 0 # Settings for VF 0 on eno2
			- Trust: 1
			- LinkState: "on"
			- VLANId: 20
			- VLANProtocol: "802.1Q"
			- MACSpoofCheck: "yes"
			- QueryReceiveSideScaling: "yes"
			- QualityOfService: "1536"
			- MACAddress: "0b:90:39:6c:88:27"
		- SR-IOV:
			- VirtualFunction: 1 # Settings for VF 1 on eno2
			- Trust: 1
			- LinkState: "on"
  # Configuration file for eno3's VF
  - 01-eno3_sriov:
    - Match:
      - Name: "eno3*"
		- SR-IOV:
			- VirtualFunction: 0 # Settings for VF 1 on eno2
			- Trust: 1
			- LinkState: "on"
```

## Attach vNICs to VMs

Once the VFs are created on the hypervisor, they can be attached to VMs.

> [!WARNING]
> **Important:** Because SR-IOV uses PCI passthrough, the guest VM sees a real PCI device. The VM's operating system **must have the appropriate driver** for this virtual NIC (e.g., `igbvf` for `igb` PFs, `ixgbevf` for `ixgbe` PFs) for the interface to function.

You have two methods for attachment:

### Option A: Direct PCI Passthrough

You can attach a specific VF to a VM manually using pci passthrough, as you would do with a physical NIC.

For a hand written Libvirt XML, refer to <https://libvirt.org/formatnetwork.html#connectivity>

If you use the templated `guest.xml.j2` Libvirt XML file, you can use the `pci_passthrough` variable in the VM configuration.

```java
VM:
# ... other VM settings
  pci_passthrough:
    - domain: 0
      bus: 1
      slot: 0
      function: 1
```

### Option B: Automatic SR-IOV Pool Assignment

If you prefer not to manually assign PCI addresses, you can instruct Libvirt to automatically pick an available VF from a given SR-IOV pool.

For a hand written Libvirt XML, refer to <https://libvirt.org/formatnetwork.html#connectivity>

If you use the templated `guest.xml.j2` Libvirt XML file, you can use the `sriov` variable in your VM configuration:

```java
VM:
# ... other VM settings
  sriov:
    - sr-iov-net-eno1
    - sr-iov-net-eno3
```
