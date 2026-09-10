
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Real-time](../Real-time.md)

# Real-time on SEAPATH

One goal of SEAPATH is to leverage real time for applications running inside virtual machines. To that purpose multiple configurations are used.

> [!IMPORTANT]
> Keep in mind that SEAPATH can run a mix of critical and non-critical applications.
>
> If your virtual machine doesn’t need any real-time capabilities, you can still run it on SEAPATH, but you don’t have to bother with the VM real time configuration.

## Real time on a SEAPATH hypervisor

A SEAPATH hypervisor uses several configurations for real time:

- Real-time Linux kernel is used (PREEMPT\_RT)
- All kernel and system processes run on some specific CPUs, leaving the rest for the virtual machines to use
- Kernel command line is tailored for real time virtualization
- System is configured with tuned

### CPU Isolation

At hypervisor configuration time, a list of isolated CPUs is selected. On these CPUs, the kernel will avoid running:

- System process
- User process
- IRQs

These CPUs will then be entirely dedicated to running real-time processes like virtual machines.

### Cgroups configuration (optional)

SEAPATH allows the configuration of cgroups to run all non-RT VMs on a specific set of CPUs and all RT VMs on another set.

Using these cgroups is useful to get a preset of CPU isolation for virtual machines. It seems particularly useful when deploying many VMs at once. Particularly, it allows:

- Having one more step in VM isolation
- Avoiding CPU hardware attacks like [Spectre or Meltdown](https://meltdownattack.com/)

> [!IMPORTANT]
> This new isolation layer protects from really advanced attacks. Because it has drawbacks (see below), the question remains open if you should or should not activate this feature.

Activating this cgroup configuration has two main drawbacks:

- One more CPU is needed on the RT VMs cgroup to schedule the QEMU management thread
- QEMU management thread must be carefully pinned, as this can prevent the VMs from booting

More information on [Real-time configuration](Real-time%20configuration.md).

### **Tuned**

The Debian version of SEAPATH uses tuned (<https://github.com/redhat-performance/tuned>).

This software configures different variables on the system in order to tune it for real-time virtualization performances. Among others:

- Add command-line arguments to isolate CPUs (as described above)
- Configure RT priority for kernel threads (ktimer,ksoft ...)
- Configure IRQs on isolated cores (with irqbalance)
- Configure sysfs workqueue on isolated cores

You can find a list of all tuned scheduling modifications at [Real-time configuration](Real-time%20configuration.md).

On SEAPATH Yocto, tuned is not used. Instead, all these configurations are done at compile time.

## Real time on a virtual machine

For a virtual machine to run real-time critical applications on SEAPATH, it must comply with the following requirements:

- Running a real time kernel (both the hypervisor and virtual machines must have a real time kernel)
- Run on isolated CPUs
- Use real-time priorities

All the information about configuring a virtual machine for real-time are available on [[Duplicated] Real-time virtual machine configuration](../../_Duplicated_%20Real-time%20virtual%20machine%20configuration.md).
