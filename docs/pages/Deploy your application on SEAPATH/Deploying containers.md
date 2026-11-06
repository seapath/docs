
[Deploy your application on SEAPATH](../Deploy%20your%20application%20on%20SEAPATH.md)

# Deploying containers

Container support is fully functional on SEAPATH 2.0 release.

However, the setup requires many manual configuration and is not correctly streamlined in Ansible for now

This is a complete, practical documentation for running high-availability containers on SEAPATH using the existing stack (Pacemaker/Corosync + Ceph + Cephadm + Open vSwitch / OVS, etc.).  
The goal: no Kubernetes — just a simple way to run a container (or a small pod of containers) on one host and have it automatically moved to another host if the original host fails.

We use **Ceph** for storage, **Podman** for containers (since it is cephadm default), **systemd Quadlets** for container management, and **Pacemaker** for failover orchestration.

The doc is split in three parts :

- [Containers on SEAPATH](Deploying%20containers/Containers%20on%20SEAPATH.md)
- [Containers deployment](Deploying%20containers/Containers%20deployment.md)
- [Containers management](Deploying%20containers/Containers%20management.md)
