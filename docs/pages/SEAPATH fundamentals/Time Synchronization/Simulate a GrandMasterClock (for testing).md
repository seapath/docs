
[SEAPATH fundamentals](../../SEAPATH%20fundamentals.md) > [Time Synchronization](../Time%20Synchronization.md)

# Simulate a GrandMasterClock (for testing)

**Warning: This section is for test only. It is not intended to be used in a real environment.**

To avoid the use of a physical grand master clock, a standard machine like a laptop can be used to simulate the PTP reference time. This is called « software PTP ».

To achieve that :

- Install `linuxptp`package on the laptop.
- Configure the PTP settings, in the file /etc/linuxptp/ptp4l.conf
- Starts the `ptp4l`service.

The configuration of PTP is fixed by IEC-61850 (see here on [Wikipedia](https://en.wikipedia.org/wiki/IEC/IEEE_61850-9-3)). Here is a proposed configuration of the file /etc/linuxptp/ptp4l.conf that fits the standard requirements.

```java
[Global]
slaveOnly                0
gmCapable 1

domainNumber             0

# Announce interval: 1s
logAnnounceInterval      0

# Sync interval: 1 s
logSyncInterval          0

# Pdelay interval: 1 s
logMinPdelayReqInterval  0

# Announce receipt time-out: 3 s (fixed)
announceReceiptTimeout   3

priority1                128
priority2                128
# Default clock class : any specialised clock will be better (ie a GPS Grand Master Clock)
#clockClass              192
network_transport        L2
delay_mechanism          P2P
clockClass 248
clockAccuracy 0xFE
offsetScaledLogVariance 0xFFFF
```

> [!IMPORTANT]
> The PTP clock created by ptp4l will not be synchronized with the current time. So even if your cluster machines are synchronized with each other, the date will be random.  
> To synchronize the PTP clock with the current time, type this command on the machine that simulate the grand master clock
>
> phc\_ctl <ptp\_interface> set
