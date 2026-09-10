
[Advanced configurations](../Advanced%20configurations.md)

# Update a physical machine

# Yocto

The update of the Yocto version of SEAPATH uses [SwUpdate](https://sbabic.github.io/swupdate/), by having 2 separate disk partitions. SEAPATH has an evolved process to manage an automatic rollback in case of failure, that change the "active" partition back to the original (known to be working) one.

## A/B partitioning

A/B partitioning is used to allow for an atomic and recoverable update procedure. The update will be written to the passive partition.  
Once the update is successfully transferred to the device, the device will reboot into the passive partition which thereby becomes the new active partition.

If the update causes any failures, a roll back to the original active partition can be done to preserve uptime.

The following partitioning is used on hypervisors:

|  Slot A                                         |  Slot B                                         |
|:------------------------------------------------|:------------------------------------------------|
| Boot A partition (Grub + Kernel) [/dev/<disk>1] | Boot B partition (Grub + Kernel) [/dev/<disk>2] |
| Rootfs A partition [/dev/<disk>3]               | Rootfs B partition [/dev/<disk>4]               |
| Logs partition [/dev/<disk>5]                   |                                                 |
| Persistent data partition [/dev/<disk>6]        |                                                 |

## Building an update file

Building un update file for an hypervisor is done through the *host\_efi\_swu* flavor of cqfd. Refer to the [yocto-bsp GitHub readme](https://github.com/seapath/yocto-bsp) for information on how to setup the source and build.

## Run an update with command line

Copy the image on the target and run

```java
$ sudo swupdate -i <my update>.swu
$ sudo reboot
```

## Run an update from a deployment server (Hawkbit)

SwUpdate can interact with a Hawbit server to push updates on the device.

### Installation of Hawkbit server

We use docker-compose as explained in [Hawkbit documentation](https://www.eclipse.org/hawkbit/gettingstarted/#b-run-hawkbit-update-server-with-services-as-docker-compose).

```java
$ git clone <https://github.com/eclipse/hawkbit.git>
$ cd hawkbit/hawkbit-runtime/docker
```

We decided to enable anonymous connection. To do that, add this line in *hawkbit-runtime/docker/docker-compose.yml*

```java
- 'HAWKBIT_SERVER_DDI_SECURITY_AUTHENTICATION_ANONYMOUS_ENABLED=true'
```

And start the server:

```java
$ docker-compose up -d
```

Then you can access the http server on port 8080. In *System Config* menu,  
enable "Allow targets to download artifact without security credentials", so that anonymous updates can be used.  
More documentation on Hawkbit is available on [Hawkbit website](https://www.eclipse.org/hawkbit/).

### Configuration of Hawkbit

Hawkbit Server URL and PORT must be configured in */etc/sysconfig/swupdate\_hawkbit.conf* or directly in meta-seapath (/recipes-seapath/system-config/system-config/efi/swupdate\_hawkbit.conf)

A systemd daemon (*swupdate\_hawkbit.service*) is started automatically at boot.  
If you want to modify *swupdate\_hawkbit.conf* at runtime, you must restart the systemd service.

Once the systemd service is started, you should see the device in Hawkbit interface. Once an update on the device is performed, a reboot will be done.

## Run an update from ansible

You need to pass two variables in the command line :

- `machine_to_update` is the name of the machine that ansible will update
- `swu_image` is the name of the swu file that was created in yocto-bsp.

Note: The swu image must be placed in the `swu_images` directory.

For the update of a machine in the cluster, call the playbook `playbooks/update_machine_cluster.yaml`

```java
ansible-playbook -i inventories/cluster_inventory.yaml -e "machine_to_update=node1" -e "swu_image=update.swu" playbooks/seapath_update_yocto_cluster.yaml
```

Otherwise, for the standalone, call the playbook `playbooks/update_machine_standalone.yaml`

```java
ansible-playbook -i inventories/standalone_inventory.yaml -e "machine_to_update=node1" -e "swu_image=update.swu" playbooks/seapath_update_yocto_standalone.yaml
```

## Run an update from a graphical environment

A cockpit plugin is available to update a Yocto hypervisor. Read [Using a graphical interface on Seapath](../SEAPATH%20fundamentals/Supervision/Using%20a%20graphical%20interface%20on%20Seapath.md) for more information.

# Debian

The upgrade process is the very standard "apt" way (apt update, apt upgrade, ...).  
The rollback posibilities leverage [LVM snapshots](https://documentation.suse.com/sles/12-SP4/html/SLES-all/cha-lvm-snapshots.html).

## Update

The apt package tool is used to upgrade the system. You can use the rollback to avoid loss of the system (more details in the below section).

Update the database of available packages, with their version:

```bash
apt update
```

Upgrade the system with the new version of packages:

```bash
apt upgrade --yes
```

Upgrade the system with new version of Debian and remove useless packages:

```bash
apt dist-upgrade --yes
apt autoremove --yes --purge
```

## Rollback

As mentioned [[Duplicated] Image configuration](../_Duplicated_%20Image%20configuration.md), the root partition is on LVM disk. With this configuration, it can be saved by a LVM snapshot.

```bash
lvcreate -L SIZE -s -n SNAPSHOT_NAME /dev/VOLUME_GROUP/DISK_NAME
```

With snapshots, the partition can be rollback in the stable state with this command:

```bash
lvconvert --merge /dev/VOLUME_GROUP/SNAPSHOT_NAME
```

Otherwise, the snapshot can be removed with these commands:

```bash
lvremove /dev/VOLUME_GROUP/SNAPSHOT_NAME
```

## Troubleshooting

### Can't create a snapshot with old name

If you don't reboot the machine, the `lvcreate` command believes the name is always used. To remove it, you need to launch this command:

```bash
vgchange --refresh
```
