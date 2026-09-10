
[Deploy your application on SEAPATH](../Deploy%20your%20application%20on%20SEAPATH.md)

# [Under development] Deploying containers

> [!WARNING]
> The full container support on SEAPATH is still in development and not yet functional in any of the official SEAPATH releases.
>
> This section is a forecast of what will be developed in the future, and is still under discussions.
>
> If you wish to deploy a container on an official SEAPATH version, you can simply use docker, but without any high availability cluster support

This is a complete, practical documentation for running high-availability containers on SEAPATH using the existing stack (Pacemaker/Corosync + Ceph + Cephadm + Open vSwitch / OVS, etc.).  
The goal: no Kubernetes — just a simple way to run a container (or a small pod of containers) on one host and have it automatically moved to another host if the original host fails.

We use **Ceph** for storage, **Podman** for containers (since it is cephadm default), **systemd Quadlets** for container management, and **Pacemaker** for failover orchestration.

For the time being, this feature is only available on the [Debian13](https://github.com/seapath/ansible/tree/trixie2) branch of Seapath (using cephadm)

The doc is split in three parts :

- [Containers on SEAPATH](_Under%20development_%20Deploying%20containers/Containers%20on%20SEAPATH.md)
- [Containers deployment](_Under%20development_%20Deploying%20containers/Containers%20deployment.md)
- [Containers management](_Under%20development_%20Deploying%20containers/Containers%20management.md)
