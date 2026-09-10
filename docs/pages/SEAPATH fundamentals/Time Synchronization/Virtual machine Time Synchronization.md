
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Time Synchronization](../Time%20Synchronization.md)

# Virtual machine Time Synchronization

## IEC 61850 Requirement

The IEC 61850 standard specifies that each IED (Intelligent Electronic Device) must be synchronized using PTP. In a physical deployment, this is straightforward: every device connects to the PTP network and aligns its hardware clock with the Grand Master.

## Challenges in Virtual Environments

When IEDs are virtualized, enforcing IEC 61850 compliance becomes complicated:

- The PTP network must be propagated into the VM, requiring careful configuration of virtual NICs.
- The VM must receive hardware timestamps to achieve precise synchronization. This usually requires **PCI passthrough** of the network interface.
- **SR-IOV cannot be used**, because virtual functions do not support hardware timestamping, which is critical for PTP accuracy.
- Each VM would need its own PTP setup (ptp4l, phc2sys), VLANs, and careful network isolation, making the configuration complex and fragile.

> [!IMPORTANT]
> It is a totally viable solution to let the VM receive PTP frames on a pci\_passthrough interface and synchronize itself directly on this source.  
> However, this solution is usually less precise and less practical than the host synchronization described below

## PTP synchronisation through the host (ptp\_kvm)

SEAPATH takes a simpler and more reliable approach:

- Only the **physical host** is synchronized to the PTP Grand Master.
- The **host’s PTP clock is exposed to the VM** using the **ptp\_kvm** kernel module.
- This allows the VM to inherit the host’s synchronized time without requiring direct access to the PTP network.

Steps to use ptp\_kvm in the VM:

1. Load the `ptp_kvm` kernel module (at boot or manually).
2. Identify the created PTP device under `/dev/ptp*` by checking `/sys/class/ptp/ptp*/clock_name`, which should show `"KVM virtual PTP"`. Example: `/dev/ptp0`.
3. Synchronize the VM system clock to the PTP clock using **chrony** (for example by creating the `/etc/chrony/conf.d/ptp.conf` file):

   ```java
   refclock PHC /dev/ptp0 poll 2
   ```

## PTP Status Propagation to Virtual IEDs

### IEC 61850 Requirement

IEC 61850 specifies that each Sampled Value (SV) message should include a `SmpSynch` field, indicating the PTP synchronization status of the source device. For a physical IED, this is straightforward: the device knows whether it is synchronized.

In a virtual environment, the VM itself does not have a direct PTP connection, so it cannot know its own PTP sync status.

### SEAPATH Solution: `ptp_status_vsock` Role

SEAPATH provides the `ptp_status_vsock` [Ansible role](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/ptp_status_vsock/) to bridge this gap.

- The role runs on the **host** and retrieves the host’s PTP synchronization status every second.
- It exposes this status to the guest VM via a **vsock interface**.

More information on this role on [Ansible Galaxy](https://galaxy.ansible.com/ui/repo/published/seapath/ansible/content/role/ptp_status_vsock/).

#### What is a vsock?

A **vsock (virtual socket)** is a communication channel between the hypervisor and its guests. It allows data to flow between host and VM without going through a network stack, making it fast and reliable.

- In libvirt, you define a vsock device in the VM XML, for example:

  ```java
  <devices>
    <vsock model='virtio' cid='3'/>
  </devices>
  ```

#### How to use it in the guest

- The VM can open the vsock device using standard libraries (e.g., `libvirt` or `python-vsock`) to read the host’s PTP status.

Example python code:

```java
#!/usr/bin/env python3
import socket,sys

PORT = int(sys.argv[1])
message = sys.argv[2]
CID = socket.VMADDR_CID_HOST

s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
s.connect((CID, PORT))
s.send(str.encode(message))
buf = s.recv(10000)
if buf:
  print(buf.decode(),end='')
```

And call the script this way : python3 test.py 9999 STATUS and python3 test.py 9999 DETAILS

- This value can then be propagated into the `SmpSynch` field of the Virtual IED’s SV messages.

With this mechanism, **virtual IEDs effectively inherit the PTP status of the host**, maintaining IEC 61850 compliance without needing the guest to manage its own PTP stack.
