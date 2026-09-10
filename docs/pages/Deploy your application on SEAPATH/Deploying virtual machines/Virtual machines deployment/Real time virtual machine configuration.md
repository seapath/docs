
[Deploy your application on SEAPATH](../../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../../Deploying%20virtual%20machines.md) > [Virtual machines deployment](../Virtual%20machines%20deployment.md)

# Real time virtual machine configuration

## **Scheduling virtual machines**

SEAPATH virtual machines are managed by Qemu.

On a hypervisor, when launching a VM, Qemu creates different threads. They can be dispatched in two categories:

- Virtual CPU threads: These threads emulate the CPUs of the virtual machines. Each CPU inside the virtual machine is handled by one vCPU thread on the hypervisor.
- Management threads: They are responsible for creating the VM, checking if it crashes, managing the IO etc.

By default, all these threads are managed by the Linux scheduler and thus run on the non-isolated cores. But they can also be pinned to specific CPUs, which forces them to run on those CPUs.

### **Standard virtual machines**

For a VM without any performance or real-time needs, it is unnecessary to handle any of the Qemu threads in a particular way:

- All threads inherit a default priority and scheduling type (TS 19)
- All threads are handled by the Linux scheduler on the non-isolated cores

The only thing to configure is the number of CPUs desired.

- Using `vcpu` if you write your own Libvirt XML file (more information at <https://libvirt.org/formatdomain.html#cpu-allocation>)
- Using `nb_cpu` if you use `guest.xml.j2`

### **Real-time virtual machines**

For a VM where performance and determinism are needed, the recommendations are to isolate the vCPU threads and optionally, the management threads.

The vCPU threads are where the work of the VM run. They must therefore have as much CPU time as possible. To achieve that, they should be scheduled with a real-time scheduler (FIFO), a real-time priority (1 or more), and placed alone on an isolated core.

General information about configuring real time virtual machines at <https://libvirt.org/kbase/kvm-realtime.html>

#### On the `guest.xml.j2` templated Libvirt XML file

- Select the “rt” and “isolated” vm\_features
- Select the hypervisor isolated CPUs to use with the `cpuset` variable.
- Optionally, use `emulatorpin` to schedule the management processes of the VM.

More information in the [deploy\_vms\_standalone](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/deploy_vms_standalone/) and [deploy\_vms\_cluster](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/deploy_vms_cluster/) role documentation.

> [!WARNING]
> Each vCPU must be placed **alone** on an isolated CPU. It is counterproductive to put two vCPU threads on the same core. This means you must have at least as many isolated cores as RT VM vCPUs.

> [!IMPORTANT]
> Isolating the management process of QEMU is useful if you use software solutions (bridges or macvtap) to send time-critical data to the VM. See [Connect a virtual machine to the network](Connect%20a%20virtual%20machine%20to%20the%20network.md)

#### On a hand-written Libvirt XML file

- Use `vcpupin` to schedule each vCPU of the VM on an isolated core
- Use `vcpusched` to select the scheduler and priority
- Optionally, use `emulatorpin` to schedule the management processes of the VM.

More information about CPU tuning at <https://libvirt.org/formatdomain.html#cpu-allocation>

> [!NOTE]
> Other configurations are needed to properly configure a real-time VM from scratch. They are listed at <https://libvirt.org/kbase/kvm-realtime.html>

## Cgroup usage (optional)

If you have configured real-time and non-real time virtual machine cgroups (see [Real-time on SEAPATH](../../../SEAPATH%20fundamentals/Real-time/Real-time%20on%20SEAPATH.md) ), you must integrate the VM into the appropriate cgroup.

This is done using Libvirt resources. Possible values:

- /machine/nort
- /machine/rt

Example for a virtual machine with real-time:

```java
<resource>
    <partition>/machine/rt</partition>
</resource>
```

> [!NOTE]
> This behavior is automatically done in`guest.xml.j2`, when selecting the `rt` vm feature.

> [!WARNING]
> If the vCPUs of the VMs are isolated (with `vcpupin` or `cpuset`), all vCPUs must be scheduled inside the cgroup cpuset.
>
> If the QEMU thread is isolated (with `emulatorpin`), it must be scheduled inside the cgroup cpuset.
