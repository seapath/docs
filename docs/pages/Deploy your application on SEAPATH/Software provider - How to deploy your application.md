
[Deploy your application on SEAPATH](../Deploy%20your%20application%20on%20SEAPATH.md)

# Software provider - How to deploy your application

There are multiple ways to deploy an application on SEAPATH, depending on the features needed

- **Virtual machines** are the primary target for SEAPATH. They allow a high isolation, enhancing multi-provider applications. VMs benefit from high-availability when in a cluster.
- **Containers** can also be deployed on SEAPATH. They are faster and lighter than virtual machines but offer less isolation. High availability is not yet implemented for containers on SEAPATH.

## Use virtual machines

SEAPATH uses QEMU and Libvirt to deploy virtual machines. With this technology, two elements are needed:

- **A Libvirt XML configuration** **file**: This file describes all the devices needed by the VM. It can be memory, CPU information, interfaces ...
- **A VM disk image**: This file represents the disk of the virtual machine; it will contain the kernel as well as the filesystem.  
  VM disks come in different [formats](https://www.qemu.org/docs/master/system/images.html). On SEAPATH, qcow2 is used.

The handling of the Libvirt XML file and the actual VM deployment is explained in the next section [Deploying virtual machines](Deploying%20virtual%20machines.md). This page only tackles the disk question

There are three cases to consider if you want to deploy your application in a VM

- You already have your own VM
- You only have your application and want to run it inside a VM
- You want to use a third-party VM

### Use your own VM

If you already have a VM disk, or if you want to use a specific operating system (Ubuntu, Windows …), you must convert the disk to qcow2 format.

It is possible to convert alternative disk image formats to qcow2 thanks to qemu-img. Refer to [qemu documentation](https://www.qemu.org/docs/master/tools/qemu-img.html).

### Use a generic SEAPATH VM

If you only have your application and need a virtual machine to run it, you can use a generic SEAPATH VM which contains:

- All applicable cybersecurity policies and tests applied on SEAPATH hypervisor
- Minimal applications installed

Information on how to build a disk image in detail is available [here](https://github.com/seapath/yocto-bsp) for a Yocto-based VM, or [here](https://github.com/seapath/build_debian_iso?tab=readme-ov-file#build-a-virtual-machine-image) for a Debian-based VM.

### Use a supported provider VM

Some provider VMs are supported in SEAPATH, you can deploy them following their documentation: [Third party virtual machines](Deploying%20virtual%20machines/Third%20party%20virtual%20machines.md)

## Use containers on SEAPATH

SEAPATH supports the launch of containers using Docker. For now, containers are only launched on a single machine and cannot benefit from the high-availability cluster

> [!IMPORTANT]
> Discussions are on going to replace Docker with Podman in the upcoming 2.0 release. Docker compatibility will be kept thanks to the [podman-docker](https://packages.debian.org/sid/podman-docker) package.

> [!NOTE]
> High-availability cluster support for containers is in development. You can read more at [Deploying containers](Deploying%20containers.md)
