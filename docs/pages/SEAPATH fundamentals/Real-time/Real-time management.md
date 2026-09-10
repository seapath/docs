
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Real-time](../Real-time.md)

# Real-time management

## CPU isolation and tuned profile

The tuned profile used by SEAPATH is available in `/etc/tuned/seapath-rt-host/tuned.conf`.

To verify the isolated CPUs, take a look at the kernel command line:

```java
cat /proc/cmdline
```

## Cgroup usage

If real-time and non-real-time cgroups are configured, you can verify the processes running inside of them (the VMs) by looking at the associated slide. The CPU range is also described with the slide:

- `machine.slice` is the default cgroup for all VMs
- `machine-rt.slice` is used for real-time virtual machine
- `machine-nort` is used for non-real-time virtual machines

All these cgroups can be investigated with `systemctl status <cgroup>` command.

## VM CPU usage

The number of CPUs used by a virtual machine can be investigated with the `vcpu*` Libvirt commands. Refer to [Libvirt documentation](https://libvirt.org/manpages/virsh.html#vcpucount).
