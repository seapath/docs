
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Time Synchronization](../Time%20Synchronization.md)

# Time synchronization on SEAPATH

### **Why It’s Needed**

In an IEC 61850 environment, all devices — physical or virtual — must share a highly accurate time reference to correctly timestamp and correlate events exchanged over SV, GOOSE or MMS. Any drift between nodes can lead to inconsistent logs or even malfunctions.

### **What SEAPATH Provides**

SEAPATH lets you configure **both Precision Time Protocol (PTP)** and **Network Time Protocol (NTP)** for your infrastructure:

- **PTP** gives sub-millisecond precision and is the primary mechanism required by IEC 61850.
- **NTP** is usually used as a fallback if PTP is unavailable.
- When no PTP grand master is present, SEAPATH can still synchronize with one or more NTP servers, either on your local network or on the Internet.

This dual approach ensures that your nodes stay in sync even if one time source becomes unavailable.

### **A Special Feature for Guests**

Beyond synchronizing the **hosts**, SEAPATH also proposes a built-in mechanism to synchronize **guest virtual machines** without requiring PCI passthrough: the `ptp_kvm` integration.  
This allows the hypervisor’s already synchronized PTP clock to be exposed inside each VM, so the guests stay aligned with the cluster time source.

> [!NOTE]
> The guest-synchronization mechanism (`ptp_kvm`) is an important part of SEAPATH but is documented in detail on its [Virtual machine Time Synchronization](Virtual%20machine%20Time%20Synchronization.md).
