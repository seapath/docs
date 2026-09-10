
[Getting started](../../Getting%20started.md) > [Prerequisites](../Prerequisites.md)

# External support machines

In order to deploy and manage SEAPATH, you will need external machines to

- Build the SEAPATH ISO
- Configure and manage the SEAPATH machines (Administration using Ansible)

Below are the requirements for each machines

> [!IMPORTANT]
> It is absolutely possible to use the same machine for the two steps. In that case, the machine has to be compliant with all the requirements

# Build machine

> [!IMPORTANT]
> Default pre-built ISOs are provided at each SEAPATH release.  
> If you are new to the project, you can use them. Thus you avoid having to set up a build machine.

## Debian base ISO

Building a SEAPATH Debian based ISO doesn’t require a strong machine

- Linux-based (WSL can be used)
- Docker support
- Internet access
- Software requirements are described on <https://github.com/seapath/build_debian_iso>

## Yocto base ISO

Building a SEAPATH Yocto-based ISO means recompiling all the software in SEAPATH, this requires

- Linux based (native; WSL is not sufficient)
- Internet access
- Strong build machine
- Docker support (optional, but simplifies the process)
- Software requirements are described on <https://github.com/seapath/yocto-bsp> .

> [!NOTE]
> We recommend having at least 16 GB of RAM and 8 CPUs to build SEAPATH. Yocto builds are usually long (several hours), so the bigger, the better.

> [!NOTE]
> We recommend not to use Virtual Machine. The Yocto project will ensure to multi-thread your build, so try to use a build machine with many CPU cores.  
> More information on the Yocto Project mailing list: <https://lists.yoctoproject.org/g/yocto/topic/72047879#48815>

# Administration machine

The configuration and the management of the SEAPATH infrastructure will be done with [Ansible](https://docs.ansible.com/). A machine is then required to run it. This machine requires :

- Linux based (WSL can be used)
- SSH access to all the SEAPATH machines.
- Internet access
- Docker support (optional, but simplifies the process)
- Software requirements are described directly on <https://github.com/seapath/ansible>

> [!IMPORTANT]
> The internet access on this machine is only required to fetch and prepare the sources. Internet connection is not required during the SEAPATH infrastructure configuration and management

> [!NOTE]
> The SSH access is usually done by connecting the Ansible machine with an Ethernet cable directly to the SEAPATH administration switch. However, any connection type is valid, as long as it allows SSH.

# Recommended setup

Your everyday work laptop (Linux or WSL) should be sufficient to build the SEAPATH Debian-based ISO and to run Ansible.

For a Yocto-based ISO build, we recommend having a dedicated build desktop or server.
