
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Supervision](../Supervision.md)

# SNMP

SEAPATH can be monitored using SNMP. This page documents the custom SNMP MIB implementation for the SEAPATH project. It allows monitoring of hardware health, virtualization metrics, and cluster status through a specific OID branch.

SEAPATH SNMP’s data are only accessible in read-only.

> [!NOTE]
> SEAPATH does not include the IEC-61850 MIB.

## MIB Architecture

SEAPATH uses a pass\_persist mechanism to extend the standard **Net-SNMP** agent.

The MIB is provided as an example and should be updated to your hardware and needs.

### Base OID

The root OID for all SEAPATH custom metrics is: .2.25.1936023920.1635018752.0.

### OID Tree Structure

The MIB is organized into 5 main branches.

### Branch .1: Virtualization & Cluster Status

*Base Path:* `[ROOT].1.x`

|  **OID Suffix**    |  **Description**                |  **Output detail**                                                                                                                                               |
|:-------------------|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `.1.1`             | Pacemaker cluster status (text) | `crm status`                                                                                                                                                     |
| `.1.2`             | VM Domain Statistics            | `virsh domstats`                                                                                                                                                 |
| `.1.3`             | VM Memory Statistics            | `virsh dommemstat`                                                                                                                                               |
| `.1.4`             | Ceph Status                     | `ceph status`                                                                                                                                                    |
| `.1.5`             | Guest Disk Usage (Internal)     | `virt-df.sh` (mounts guest FS read-only)                                                                                                                         |
| `.1.6`             | List of all VMs                 | `virsh list --all`                                                                                                                                               |
| `.1.7`             | Ceph Placement Groups Map       | `ceph status` ([Example of SNMP output](SNMP/Example%20of%20SNMP%20output.md))                                                                                   |
| `.1.8`             | Disk Temperatures               | The temperature in Celsius                                                                                                                                       |
| `.1.9`             | Detailed S.M.A.R.T. Attributes  | `smartctl --attributes` [Example of SNMP output](SNMP/Example%20of%20SNMP%20output.md)                                                                           |
| `.1.10`            | LVM Detailed Status             | `lvs -a -o +devices,lv_health_status`                                                                                                                            |
| `.1.11`            | CRM Status (JSON)               | `crm status --as-xml` [(re-format as JSON string)](SNMP/Example%20of%20SNMP%20output.md#example-of-crm-status-111).       |
| `.1.11.0.1`        | CRM Summary (JSON)              | `crm status --as-xml` [(re-format as JSON string)](SNMP/Example%20of%20SNMP%20output.md#example-of-crm-summary-11101). |
| `.1.11.0.2`        | CRM Nodes Status (JSON)         | `crm status --as-xml` [Example of SNMP output](SNMP/Example%20of%20SNMP%20output.md).                                                                            |

### Branch .2: Disk Health & Monoline Metrics

*Base Path:* `[ROOT].2.x`

|  **OID Suffix**    |  **Description**          |  **Output detail**                                                                                                                                           |
|:-------------------|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `.2.1`             | Health Status: `/dev/sda` | `smartctl -H /dev/sda` result (PASSED or FAILED!)                                                                                                            |
| `.2.2`             | Health Status: `/dev/sdb` | `smartctl -H /dev/sdb` result (PASSED or FAILED!)                                                                                                            |
| `.2.3`             | Health Status: `/dev/sdc` | `smartctl -H /dev/sdc` result (PASSED or FAILED!)                                                                                                            |
| `.2.4`             | Health Status: `/dev/sdd` | `smartctl -H /dev/sdd` result (PASSED or FAILED!)                                                                                                            |
| `.2.5.x`           | LVM Full Report (JSON)    | [Arrays of LVM data in JSON format (one per LV)](SNMP/Example%20of%20SNMP%20output.md#example-of-lvm-full-report-25x) |
| `.2.6`             | Number of unhealthy disks | The number of unhealthy disks or void if all disks are healthy                                                                                               |
| `.2.7`             | lvs full status           | [Example of SNMP output](SNMP/Example%20of%20SNMP%20output.md)                                                                                               |
| `.2.8`             | lvs basic status          | [Example of SNMP output](SNMP/Example%20of%20SNMP%20output.md)                                                                                               |
| `.2.9`             | LVM Health Summary        | Returns "NO LVS PROBLEM" or specific error                                                                                                                   |
| `.2.10`            | Ceph Health Status        | Returns "HEALTH\_OK" or specific error                                                                                                                       |

### Branch .3: Hardware RAID (Arcconf)

*Only populated if* `arcconf` *is available.* *Base Path:* `[ROOT].3.x`

|  **OID Suffix**    |  **Description**                           |
|:-------------------|:-------------------------------------------|
| `.3.1.x`           | Physical Disk Temperatures                 |
| `.3.2.x`           | S.M.A.R.T. Warnings count per disk         |
| `.3.3`             | Sum of all S.M.A.R.T. Warnings (0 = OK)    |
| `.3.4.x`           | RAID Array Device Status (e.g., "Present") |

### Branch .4: IPMI Sensors

*Base Path:* `[ROOT].4.x`

|  **OID Suffix**    |  **Description**       |  **Output detail**     |
|:-------------------|:-----------------------|:-----------------------|
| `.4.1`             | IPMI Sensors (Concise) | `ipmitool sensor`      |
| `.4.2`             | IPMI Sensors (Verbose) | `ipmitool sensor -v`   |
| `.4.3`             | IPMI SDR List          | `ipmitool sdr list`    |
| `.4.4`             | IPMI SDR Verbose       | `ipmitool sdr list -v` |

### Branch .5: Global Replacement Alerts

*Base Path:* `[ROOT].5.x` This branch aggregates logic from RAID, S.M.A.R.T, and LVM to provide a simple "Replace Disk" indicator.

|  **OID Suffix**    |  **Description**          |  **Output detail**           |
|:-------------------|:--------------------------|:-----------------------------|
| `.5.1`             | Replace Disk 1 Status     | "OK" or Error Message        |
| `.5.2`             | Replace Disk 2 Status     | "OK" or Error Message        |
| `.5.3`             | Replace Disk 3 Status     | "OK" or Error Message        |
| `.5.4`             | Replace Disk 4 Status     | "OK" or Error Message        |
| `.5.5`             | Global Replacement Status | "OK" or Global Error Summary |

## Ansible Role Configuration

The SNMP configuration is managed by the `snmp` role. It handles package installation, user creation, `snmpd.conf` generation, and the deployment of the custom scripts.

### Prerequisites

- **Operating System:** Yocto is not supported for this role.
- **Variable:** `snmp_admin_ip_addr` must be defined, otherwise the role disables the SNMP service.

### Variables

See full description of the variables on the [snmp](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/snmp/) role documentation

### Configuration Modes

#### 1. SNMP v2c (Default)

If `snmp_accounts` is **not** defined, the role configures a standard SNMP v2c setup:

- **RO Community:** `public`
- **Views:** Grants access to `.1` (System) and `.2` (SEAPATH Custom) OID trees.

**Example Playbook (v2c):**

```java
- hosts: cluster_machines
  vars:
    snmp_admin_ip_addr: "192.168.1.10"
  roles:
    - { role: seapath_ansible.snmp }
```

#### SNMP v3 (Secure)

If `snmp_accounts` is defined, the role switches to v3. It creates the users with SHA auth and AES encryption.

**Example Playbook (v3):**

```java
- hosts: cluster_machines
  vars:
    snmp_admin_ip_addr: "192.168.1.10"
    snmp_accounts:
      - name: "myuser"
        password: "MySecurePassword"
  roles:
    - { role: seapath_ansible.snmp }
```
