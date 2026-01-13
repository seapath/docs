
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Time Synchronization](../Time%20Synchronization.md)

# Time synchronization configuration

### Ansible Role `timemaster`

SEAPATH provides an [Ansible role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/timemaster/) for`timemaster` to automate the setup of time synchronization on your hosts.

This role:

- Generates and manages the `/etc/linuxptp/timemaster.conf` file.
- Enables and supervises the `timemaster` service.
- Populates the `ptp4l`, `chrony`, and `phc2sys` sections according to your variables.

**Main Variables:**

|  Variable       |  Purpose                                                         |
|:----------------|:-----------------------------------------------------------------|
| `ptp_interface` | Name of the network interface that receives PTP frames.          |
| `ptp_vlanid`    | (Optional) VLAN ID to use for the PTP interface.                 |
| `ntp_servers`   | List of NTP servers to configure in the `[chrony.conf]` section. |

By setting these variables in your inventory or playbook, you describe exactly how `timemaster` should behave on each host.

### ⚠️ Networking Is Separate

The `timemaster` role **does not create or configure network interfaces** itself.  
If you need to create a dedicated interface or VLAN for PTP traffic, do it first using the `network_basics` [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_basics/) on Ansible Galaxy

- `network_basics` consumes `custom_network` / `custom_netdev` variables where you can write your desired `systemd-networkd` configuration (interfaces, VLANs, bonds, etc.).
- Once the interface exists, you can point `timemaster` at it via `ptp_interface` and, if applicable, `ptp_vlanid`.

This separation ensures that network changes and time synchronization configuration remain decoupled and manageable.

### Documentation

For all variable names, defaults, and examples, consult the official documentation of each role:

- `timemaster` [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/timemaster/) on Ansible Galaxy
- `network_basics` [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/network_basics/) on Ansible Galaxy
