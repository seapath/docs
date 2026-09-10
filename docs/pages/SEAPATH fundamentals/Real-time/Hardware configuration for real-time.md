
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Real-time](../Real-time.md)

# Hardware configuration for real-time

This page lists specific hardware configurations to keep in mind in order to achieve real time performances. This concerns the hypervisor running SEAPATH.

### **Hyper-threading**

Most of the modern CPUs support hyper-threading. This option can be enabled in the BIOS and double the number of CPUs available on the system. However, the newly created CPUs are not as fast and independent as classic ones.

Hyper-threading uses the concept of logical cores. A logical core is only the pipeline part of a CPU. It shares an Arithmetic Logic Unit (ALU) and memory with another logical core to form a physical core.  
When hyper-threading is disabled, every physical core runs only one logical core. It then has full access to the memory and the ALU. When hyper-threading is enabled, the two logical cores are enabled. The obvious drawback is that each logical core will influence its sibling.

When running real-time virtual machines, it is **highly recommended to disable hyper-threading.** However, on test systems or systems with fewer cores, it can be an interesting feature. In that case, the RT VM vCPU must be pinned to a logical core where its sibling doesn’t run any process. Otherwise, it will influence the vCPU thread, which will lose determinism.

To know the exact architecture of your CPUs, use the command `virsh capabilities` and watch the `topology` section. The siblings field describes which logical CPUs are grouped together.

> [!IMPORTANT]
> On most systems, logical CPUs are grouped in numerical order (0 with 1, 2 with 3 …) but this is not always the case. Always refer to `virsh capabilities` to check the exact architecture.

### **NUMA**

NUMA (Non-Uniform Memory Access) refers to machines that have the ability to contain several CPU sockets. Each of these sockets has its own cache memory, which means that accessing memory from one socket to another is much slower than accessing memory on its own socket.

To know if a SEAPATH hypervisor has a NUMA architecture, use the command `virsh nodeinfo` . It gives, among others, the number of NUMA cells in the system.  
To know the architecture of CPUs in the system, launch the command `virsh capabilities`. It provides a section called `topology` with a description of the sockets (here called cells) and the CPUs each one contains. More information about these commands [here](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/virtualization/ch33s08).

If your system contains more than one NUMA cell, you must be careful to pin all the vCPU threads of one VM **on the same NUMA cell**. Otherwise, the data transfer between two cells will significantly slow down the VM.
