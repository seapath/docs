
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../Deploying%20virtual%20machines.md)

# Virtual machines on SEAPATH

SEAPATH Virtualization stack is powered by well-established open source projects

- [QEMU](https://www.qemu.org/) emulates the hardware and runs virtual machines as processes on the hypervisor
- [KVM](https://linux-kvm.org/page/Main_Page) offers hardware acceleration
- [Libvirt](https://libvirt.org/) brings an API to control virtual machines both for applications and for the command line interface

With the correct configuration, these tools can effectively schedule virtual machines with real-time constraints.

Additionally, when deployed on a SEAPATH cluster, virtual machines benefit from the high-availability feature

- VM disk is stored on the Ceph replicated storage, making it accessible from all machines in the cluster
- VMs are managed by Pacemaker to schedule them on the different machines of the cluster and enable (live) migration

## The vm\_manager tool

The complexity of managing all these software components at once led SEAPATH to develop its own tool, [vm\_manager](https://github.com/seapath/vm_manager), which acts as a wrapper around Ceph, Pacemaker, and Libvirt.

This tool is the primary interface to interact with VMs on SEAPATH, whether in standalone mode or in a cluster. Learn more at [Virtual machines management](Virtual%20machines%20management.md)

Additionally, an Ansible module, `cluster_vm,` has been created to deploy virtual machines on a SEAPATH cluster. This module uses vm\_manager’s deployment capabilities and integrates them into the infrastructure-as-code philosophy of Ansible. Learn more at [Virtual machines deployment](Virtual%20machines%20deployment.md)
