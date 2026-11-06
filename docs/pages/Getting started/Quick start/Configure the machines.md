
[Getting started](../../Getting%20started.md) > [Quick start](../Quick%20start.md)

# Configure the machines

Your SEAPATH machines are now correctly flashed and wired. The last step is the configuration with Ansible. All this section will be done on the administration machine.

This section assumes you have an administration machine setup. See [External support machines](../Prerequisites/External%20support%20machines.md) for more information.

> [!NOTE]
> This step is the same for Yocto and Debian.

## Prepare the sources

Clone the SEAPATH Ansible repository.

```java
git clone -b v2.0.1 https://github.com/seapath/ansible.git
cd ansible
```

Copy the example inventory

For standalone :

```java
cp inventories/examples/seapath-standalone.yaml inventories/my-inventory.yaml
```

For cluster:

```java
cp inventories/examples/seapath-cluster.yaml inventories/my-inventory.yaml
```

## Fill the inventory

Open `my-inventory.yaml` with your favorite text editor.

You should now fill in all the required information (marked “TODO”). For this purpose, you should SSH to your SEAPATH machines and recover the information from there.

For a first SEAPATH installation, some variables can be left with the default value. Here is an overview of the variable you must modify.

- `ansible_host`: The IP address of the hypervisor. Must be set for all SEAPATH machines
- `network_interface`: The name of the hypervisor interface to use as administration. This is the one currently having the IP. Must be set for all SEAPATH machines
- `ptp_interface`: The name of the hypervisor interface where PTP frames are received. Must be set for all SEAPATH machines
- `gateway_addr`: The name of the gateway. Put an empty value if you don’t know it `””`
- `dns_servers`: Address of the DNS, if any. Remove it if you don’t have access to a DNS.
- `ntp_servers`: Address of the NTP servers, if any. Remove it if you don’t have NTP servers.

Additional variables only used in cluster mode

- `team0_0`: The name of one hypervisor interface used in the triangle cluster. Must be set for all SEAPATH machines
- `team0_1`: The name of the other hypervisor interface used in the triangle cluster. Must be set for all SEAPATH machines
- `ceph_osd_disk`: The name of the disk for CEPH to use. This is the second disk, where SEAPATH is not installed. Must be set for all SEAPATH machines

> [!IMPORTANT]
> To avoid errors, the ceph\_osd\_disk path should be set using the disk by-path link. You can find all your disk links with the command `ls -la /dev/disk/by-path`

> [!NOTE]
> All cluster IPs and networks can be let as default. A default IP subnet 192.168.55.0/24 will be created, but it is only used between the cluster machines. It will not impact your external network.

## Launch the configuration

Gather dependencies

```java
cqfd init && cqfd -b prepare
```

Launch the configuration of your SEAPATH infrastructure using

```java
cqfd run ansible-playbook -i inventories/my-inventory.yaml playbooks/seapath_setup_main.yaml
```

If you are on a Debian SEAPATH, the hardening must be applied separately with the command :

```java
cqfd run ansible-playbook -i inventories/training-hypervisor.yaml playbooks/seapath_setup_hardened_debian.yaml
```

> [!WARNING]
> This will remove the password access on the machines. Applying the hardening is not necessary on a lab setup. You may want not to activate it to keep easy access to the server.  
> Hardening must be applied in a production environment.
