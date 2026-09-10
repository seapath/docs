
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Time Synchronization](../Time%20Synchronization.md)

# Monitoring Time Synchronization Status and Driving VM Placement

### Overview

In SEAPATH, you can monitor the PTP and NTP synchronization status of every host and use that information to influence where your virtual machines run.  
For example, you might require that a critical VM runs only on a host where **PTP synchronization is prioritized**, falling back to NTP only if no host with proper PTP synchronization is available

This is achieved using two custom Pacemaker resource agents:

- `ocf:seapath:ptpstatus` – checks the host’s PTP sync status ([link](https://github.com/seapath/ansible/blob/main/roles/debian_physical_machine/files/pacemaker_ra/ptpstatus)).
- `ocf:seapath:ntpstatus` – checks the host’s NTP sync status ([link](https://github.com/seapath/ansible/blob/main/roles/debian_physical_machine/files/pacemaker_ra/ntpstatus)).

Both agents feed a simple status in the pacemaker database (the CIB), which you can use in Pacemaker **rules** to influence VM placement.

### Deploying the Status Agents

The `ptpstatus` and `ntpstatus` agents are deployed as **cloned resources** in Pacemaker, so that every cluster node runs its own local check.  
Example configuration:

```java
primitive ansible_ntpstatus_test ocf:seapath:ntpstatus \
    params host_ip=10.0.0.1 multiplier=500 \
    op monitor timeout=10 interval=10

primitive ansible_ptpstatus_test ocf:seapath:ptpstatus \
    op monitor timeout=10 interval=10 \
    op_params multiplier=1000

clone ansible_cl_ntpstatus_test ansible_ntpstatus_test \
    meta target-role=Started

clone ansible_cl_ptpstatus_test ansible_ptpstatus_test \
    meta target-role=Started
```

The `multiplier` parameter in the `ptpstatus` and `ntpstatus` Pacemaker resource agents controls the **weight** of the attribute they publish to the cluster.

Each agent periodically checks the time-sync status (PTP offset, NTP offset, etc.) and reports an attribute to Pacemaker. Pacemaker then evaluates your *location constraints* based on those attributes. By setting different `multiplier` values, you influence how “strong” that attribute is in placement decisions.

This means you can:

- Give **PTP sync** a much higher weight than **NTP sync**, so nodes with valid PTP become the top choice.
- Combine multiple criteria (PTP, NTP, hardware health, available RAM, etc.) and have Pacemaker pick the best host according to the sum of all weights.
- Build hierarchies of preference: for example, PTP with multiplier 1000 > NTP with multiplier 500 > “other” with multiplier 100.

### Using Status in Pacemaker Rules

Once the resources are running, you can create **location rules** to prefer or prevent running a VM on a host depending on its sync status.  
Example rules:

```java
location ptpstatus_location_ICT1 ICT1 \
    rule ptpstatus: defined ptpstatus

location ptpstatus_location_ICT2 ICT2 \
    rule ptpstatus: defined ptpstatus
```

Here, the VM will only be placed on ICT1 or ICT2 if their `ptpstatus` is defined (i.e. OK).

### Deploying with Ansible

The ptp\_status and ntp\_status pacemaker resource agents are deployed with the `*_physical_machine` [roles](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/debian_physical_machine/) (see [here](https://github.com/seapath/ansible/blob/3d2a6b4a513fb54a4c964a2de63c1b769e75a35d/roles/debian_physical_machine/tasks/main.yml#L53)).  
Then the pacemaker resources creation and associated rules can be deployed automatically with the `configure_ha` [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/configure_ha/) using the `extra_crm_cmd_to_run` variable:

```java
extra_crm_cmd_to_run: |
  primitive ntpstatus_test ocf:seapath:ntpstatus params host_ip=134.59.1.5 multiplier=500 op monitor timeout=10 interval=10
  primitive ptpstatus_test ocf:seapath:ptpstatus op monitor timeout=10 interval=10 op_params multiplier=1000
  clone cl_ntpstatus_test ntpstatus_test meta target-role=Started
  clone cl_ptpstatus_test ptpstatus_test meta target-role=Started
```

And you can also define **VM placement rules** when deploying VMs with the `deploy_vms_cluster` [role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/deploy_vms_cluster/), using the `crm_config_cmd` attribute. Example:

```java
VMs:
  hosts:
    test:
      live_migration: true
      migration_user: "{{ livemigration_user }}"
      migrate_to_timeout: 183
      migration_downtime: 5000
      enable: false
      priority: 4
      force: true
      crm_config_cmd:
        - "location cli-prefer-{{ inventory_hostname}} {{ inventory_hostname}} role=Started 100: virtu-elabo1"
        - "location ntpstatus_location_{{ inventory_hostname}} {{ inventory_hostname}} rule ntpstatus: defined ntpstatus"
        - "location ptpstatus_location_{{ inventory_hostname}} {{ inventory_hostname}} rule ptpstatus: defined ptpstatus"
```

This ensures that Pacemaker automatically places or migrates your VMs based on the time synchronization status of the hosts.
