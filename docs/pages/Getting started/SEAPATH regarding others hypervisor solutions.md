[Getting started](../Getting%20started.md)

# SEAPATH regarding others hypervisor solutions

When it comes to choose an hypervisor platform, you might wondering why makes SEAPATH different from others popular hypervisor platforms like Proxmox or XCP-ng.

The goal of this page is not to demonstrate if SEAPATH is better than other hypervisor platform, but rather synthesize the key differences between them.

# Architecture Overview

|  | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **Hypervisor** | KVM (via Libvirt) | KVM (no Libvirt) | Xen (type 1) |
| **Host OS** | Linux distribution agnostic (currently Yocto and Debian) | Custom Proxmox distribution based on Debian | Custom distribution based on CentOS (dom0) |
| **Kernel type** | Fully preemptible kernel (PREEMPT\_RT) | Standard Debian non-RT kernel | Xen kernel |
| **Kernel version** <br/> **(Latest stable release)** | 6.13 (SEAPATH 2.0.0) | 6.17 (Proxmox VE 9) | 4.19 (XCP-ng 8.3) |
| **Containers type** | Podman, cluster support in WIP | LXC, cluster supported | None natively |

## Key architectural difference (Xen vs KVM)

On one side, XCP-ng uses the Xen hypervisor, a Type-1 bare-metal hypervisor where dom0 (the management domain) runs a restricted Linux.

On the other side, SEAPATH and Proxmox uses KVM, which is run as a kernel module within the Linux host.

On SEAPATH this distinction matters for Real-Time (RT): the entire host kernel becomes RT capable, benefiting for Virtual Machines (VMs) scheduling.

With Xen, the host kernel (dom0) is not use to schedule VMs, but uses its own scheduler, and has not RT patch equivalent such as PREEMPT\_RT on SEAPATH.

# VM Real-Time support

| **Feature** | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **RT Kernel on host support** | Yes, natively | No, but possible using a custom kernel; replacing it is non-trivial | No, but possible by tweaking Xen to use the RTDS scheduler |
| **CPU cores partitioning** | Yes, natively | No, but could be backported from SEAPATH Debian | Not natively possible on XCP-ng. |
| **vCPU pinning + thread priority tuning** | Yes, natively | No, but is possible via custom QEMU hooks | Partial, vCPU mask exists but causes degraded performance (See note below) |
| **Virtualization/network thread priority tuning** | Yes, natively | No | No |
| **QEMU/KVM low-latency tuning (libvirt kbase)** | Yes, natively | No, some tweaks conflicts with the Proxmox monitoring web UI | Not applicable (not VM based) |
| **PCI-Passtrough** | Yes, natively | Yes, natively | Yes, natively via Xen |
| **SR-IOV** | Yes, natively | Yes, but not from the UI | Yes, (inherited from XenServer/XAPI) |
| **SR-IOV + live migration (SR-IOV pool)** | Yes, but require compatible NICs | Yes, but not from the UI and complex to implement | No, SR-IOV do not support live migration |

> [!NOTE]
> A user reported on GitHub ([xcp-ng/xcp#586](https://github.com/xcp-ng/xcp/issues/586)) that using `VCPUs-params:mask`for CPU pinning on XCP-ng actually increased worst-case cyclictest latency from ~4ms to 15-25ms. After extensive tuning (disabling VGA, SSH-only access) they could only get down to ~2ms.
>
> Compare this to raw Xen + xl where the same hardware achieved <300μs. The XAPI/toolstack overhead is significant for RT workloads.
>
> SEAPATH with PREEMPT\_RT + libvirt tuning targets sub-100μs worst-case latency.

## Why do we need Real-Time features?

Scheduling low latency Virtual Machines necessitate the following Real-times features:

1. **RT kernel:** Without PREEMPT\_RT, kernel code paths (interrupts, locks, memory allocation) can introduce unbounded latency spikes. Neither Proxmox nor XCP-ng ship an RT kernel, and retrofitting one is non-trivial on both.
2. **Isolation by design:** SEAPATH partitions CPU cores at boot (isolcpus), ensuring that host services, management agents, and monitoring daemons never compete with RT VM threads. General-purpose platforms have monitoring UIs, agents, and background services sharing all cores.
3. **Minimal OS:** Proxmox's web UI monitoring and XCP-ng's XAPI/xapi tool-stack both add processing and interrupt load on the host. SEAPATH minimal OS eliminates unnecessary services.

# Time Synchronization

| **Feature** | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **NTP/SNTP** | Yes, natively | Yes, natively | Yes, natively |
| **PTP (IEEE 1588)** | Yes, natively | No, but can be added via a dedicated container (see note) | No |
| **KVP PTP** | Yes, natively | Yes, natively | Not applicable |

PTP is critical for IEC 61850 substation applications requiring μs-level time accuracy. NTP provides ms-level accuracy at best.

**Only SEAPATH** provides PTP natively and integrates it into the VM time synchronization chain via KVM PTP.

> [!NOTE]
> Proxmox does not ship PTP/ptp4l/timemaster support out of the box. You could install it manually or run it in a container, but it is not integrated or tested. **SEAPATH integrates PTP into its build and testing pipeline.**

# Cluster Features

| **Feature** | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **Shared storage** | Ceph | Ceph, iSCSI, NFS | XOSTOR (LINSTOR/DRBD), iSCSI, NFS, CephFS (community) |
| **High Availability mechanism** | Corosync + Pacemaker | Corosync + custom mechanism | XAPI HA (heartbeat on shared storage) |
| **Advanced HA for non VM resources** | Yes | No | No |
| **Fencing** | Yes | Yes | Yes |
| **Cluster network overlay** | OVS + VXLAN | OVS + VXLAN | OVS + VXLAN |
| **SDN** | OVS | OVS | OVS |

**SEAPATH advantage:** Pacemaker manages arbitrary cluster resources (OCF agents), not just VMs. This means network services, monitoring agents, or custom daemons can be HA-managed. Proxmox and XCP-ng only provide HA for VMs and containers.

# Interfaces & Automation

| **Feature** | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **Web UI** | Cockpit (limited) | Full Web UI | Xen Orchestra |
| **Infrastructure as code** | Ansible | Ansible or Terraform via community modules | Xen Orchestra API, Ansible automation possible |
| **RBAC** | No | Yes | Yes |

SEAPATH's UI is intentionally minimal. The target is automated, reproducible deployments via Ansible; not manual administration through a web console.

# License & Economic Model

|  | **SEAPATH** | **Proxmox** | **XCP-ng** |
|:--|:--|:--|:--|
| **License** | Apache 2.0 | AGPL 3.0 | GPLv2/mixed |
| **Governance** | Linux Foundation Energy project, fully community driven | Proxmox Server Solutions GmbH | Vates SAS |
| **Access to stable repositories** | Free | Requires paid subscription | Free, support subscription optional |
| **Copyleft implications** | None, can embed proprietary products | AGPL: modifications to server-side code must be shared | GPLv2: standard kernel copyleft |

Apache 2.0 allows integrators to embed SEAPATH in proprietary products without disclosing modifications. AGPL (Proxmox) requires sharing any modifications if the software is offered as a service.

**This is a significant differentiator for industrial OEMs.**

# Summary

## What SEAPATH offers compared to other virtualization platforms

1. **Purpose-built for RT:** PREEMPT\_RT kernel, CPU isolation, thread priority tuning, QEMU/KVM low-latency configuration all integrated and tested together. Not achievable on Proxmox without significant custom work; not achievable on XCP-ng at all due to Xen architecture.
2. **PTP time synchronization:** Native ptp4l + KVM PTP for μs-accurate VM clocking. Neither Proxmox nor XCP-ng provides this.
3. **Minimal, hardened OS:** Yocto-based image or Debian minimal image with only required packages. Smaller attack surface, fewer background processes interfering with RT. Proxmox and XCP-ng ship full Linux distributions with management daemons, web servers, etc.
4. **Permissive license:** Apache 2.0 allows OEM embedding without copyleft obligations.
5. **Advanced HA:** Pacemaker OCF resources allow HA for any service, not just VMs.
6. **SR-IOV + live migration:** Supported on SEAPATH. Not supported on XCP-ng (SR-IOV VFs cannot be migrated). Complex and unsupported on Proxmox
7. **LF Energy ecosystem:** Governed by the Linux Foundation, with a community focused on power

## What SEAPATH lacks compared to other virtualization platforms

1. **Web UI:** Cockpit is limited compared to Proxmox or Xen Orchestra. Not a blocker for automated deployments, but a concern for customers used to VMware/Proxmox-style management.
2. **RBAC:** Not implemented. Fully implemented in Proxmox and XCP-ng.
3. **Container clustering:** Currently as WIP. Proxmox has a mature LXC cluster support.
4. **Community size:** Proxmox and XCP-ng have much larger user communities and more third-party documentation/tooling
