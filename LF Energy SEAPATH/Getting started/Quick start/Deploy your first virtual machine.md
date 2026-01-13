
[Getting started](../../Getting%20started.md) > [Quick start](../Quick%20start.md)

# Deploy your first virtual machine

This section explains how to deploy a standard virtual machine (VM). It is meant as an example. Deploying virtual machines will vary a lot depending on your needs.

SEAPATH handles QEMU virtual machines, deployed with Libvirt. In that case a VM is composed of two files

- The disk of the VM, which contains all the data (usually qcow2 format)
- The Libvirt XML file of the VM, which describes the hardware to emulate.

For this tutorial, we will first generate the qcow2 image of the VM.

Then we will use an Ansible inventory, which will automatically create the Libvirt XML file for us.

# Get a virtual machine disk

You can generate basic virtual machines using the same SEAPATH code base. These VMs are used in SEAPATH CI

> [!IMPORTANT]
> You can generate VMs based on Debian or Yocto. It is not necessary to follow the same base for the hypervisor and the VM.

### For a Yocto virtual machine

Come back into the `seapath-yocto` directory and launch

```java
cqfd -b guest_efi
```

Once the build is complete, you should get the virtual machine file in `build/tmp/deploy/images/seapath-vm/seapath-guest-efi-image-seapath-vm.rootfs.wic.qcow2`

### For a Debian virtual machine

Come back into the `build_debian_iso` directory and launch

```java
./build_qcow2.sh
```

The machine qcow2 file should be at the root of the directory under the name `seapath-vm.qcow2`

# Prepare the Ansible inventories

Move your VM qcow2 file under the Ansible directory, in the `files` folder.

Copy the VM example inventory

```java
cp inventories/examples/seapath-vm-deployement.yaml inventories/my-vm.yaml
```

Open the `my-vm.yaml`inventory with your favorite text editor

As for the SEAPATH cluster or standalone inventory example, the modifications are marked as “TODO”. Here are the basic mandatory modifications:

- Choose if you want to deploy an `rtvm` or a simple `vm`. Remove the other one.
- `vm_disk`: replace by the path to your VM disk, depending of your name
- Remove `ansible_host` and `wait_for_connection`. We will not connect by SSH to the VM in this tutorial

# Launch the VM

The VM is launched by Ansible

In standalone mode

```java
cqfd run ansible-playbook -i inventories/my-inventory.yaml -i inventories/my-vm.yaml playbooks/deploy_vms_standalone.yaml
```

In cluster mode

```java
cqfd run ansible-playbook -i inventories/my-inventory.yaml -i inventories/my-vm.yaml playbooks/deploy_vms_cluster.yaml
```

# Access the VM

Once deployed, you can access the VM by connecting to one of your SEAPATH machines (SSH).

List the VM deployed on your infrastructure

```java
vm-mgr list
```

Access one VM on console

```java
vm-mgr console <vm_name>
```
