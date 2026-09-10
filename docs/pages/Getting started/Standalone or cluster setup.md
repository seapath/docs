
[Getting started](../Getting%20started.md)

# Standalone or cluster setup

SEAPATH aims to run critical real-time virtual machines. The real-time constraint and the virtualization are achieved on a hypervisor, however, the “critical” requirement often implies high-availability.

On SEAPATH, a virtual machine is configured to restart automatically upon a failure. Yet this only protects against virtual machine failures and not from failures originating from the hypervisor itself (critical software error, hardware problem).

To achieve high-availability, multiple hypervisors must be connected together in a cluster.

Below is a quick overview of the benefits and drawbacks of using either a cluster or a standalone SEAPATH. In the end, the choice depends on your needs.

## Cluster

A SEAPATH cluster is composed of three machines: either three hypervisors, or two hypervisors and one observer.

### Benefits

- High availability (VMs can restart on another machine upon hypervisor failure)
- Easier maintenance (one hypervisor can be shut down for maintenance; the VMs will run on another machine)

### Drawbacks

- Necessitates three machines and at least two hypervisors
- More complex cable management and configuration

More information on cluster capabilities at

- [Cluster redundancy](../SEAPATH%20fundamentals/High%20availability%20cluster/Cluster%20redundancy.md)
- [Cluster fail-over](../SEAPATH%20fundamentals/High%20availability%20cluster/Cluster%20fail-over.md)
- [Cluster maintenance](../SEAPATH%20fundamentals/High%20availability%20cluster/Cluster%20maintenance.md)

## Standalone

Standalone SEAPATH uses only one hypervisor.

### Benefits

- Cheaper (only one hypervisor required)
- Easier to set up

### Drawbacks

- No redundancy or high-availability
