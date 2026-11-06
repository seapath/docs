
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying containers](../Deploying%20containers.md)

# Containers management

Container support is fully functional on SEAPATH 2.0 release.

However, the setup requires many manual configuration and is not correctly streamlined in Ansible for now

### Logical Components

- **Compute nodes** (N nodes running Pacemaker/Corosync). Each node provides:

  - Podman installed and configured
  - Ceph rbd client (kernel mount or systemd mount unit)
  - OVS / host networking and a physical uplink (macvlan parent interface)
- **Ceph cluster** (MON, MGR, OSDs) managed by cephadm.

  - Ceph rbd is accessible to all cluster nodes.
- **Pacemaker/Corosync cluster** providing HA resource primitives, constraints, and failover orchestration.
- **Pacemaker primitive**:

  - A simple systemd-based resource (using `systemd` resource agent) that starts, stops, and migrates the Quadlet-defined container stack between hosts.

---

### Data Placement & Container Images

- **Quadlet unit definitions :**  
  → Stored on each node, in`/etc/containers/systemd`
- **Quadlets persistent volumes and environment files**  
  → stored on Ceph rbd and mounted read/write on all compute nodes.
- **Container images and Podman storage**  
  → stored locally on each node (e.g. `/var/lib/containers/storage`).  
  → during start, images can already be present, or an automated task can ensures they are pulled in advance (e.g. via Ansible).

---

### Networking Model

- **Macvlan network(s)** (one per logical network) are defined on each host.
- Quadlet `.network` definitions specify the macvlan configuration and are deployed on all candidate nodes.
- Containers receive a fixed IPv4 address (and optional MAC address) via their Quadlet configuration.
- When Pacemaker starts the Quadlet unit on a new node:

  - the macvlan interface is created if needed,
  - the configured MAC/IP are brought up,
  - gratuitous ARPs are sent to refresh L2/L3 tables in upstream switches.

This ensures transparent service continuity after failover.

---

### Pacemaker Resource & Constraints Overview

A typical Pacemaker configuration stacks a few resources:

1. **Systemd service resource (Quadlet)**

   - Uses the standard `systemd` agent.
   - Points to the Quadlet-defined unit (e.g. `my-stack.container`).
   - Parameters (IP, MAC, etc.) are encoded in the Quadlet definition itself, not in Pacemaker.
2. **Ordering and colocation constraints**

   - Filesystem mount must be active before the container unit starts.
   - If a separate IP resource is used (optional), colocate and order it with the Quadlet unit.
3. **Meta options**

   - Resource stickiness, migration threshold, failure timeout, and target role follow SEAPATH policy.

---

### Quadlet Lifecycle in Pacemaker Context

Pacemaker doesn’t implement container logic itself — it simply starts and stops the systemd service generated from the Quadlet definition.

- **Start**

  - Pacemaker calls `systemctl start my-stack.service`.
  - systemd/Podman ensures:

    - the CephRBD-mounted directory with Quadlet files is accessible,
    - the macvlan network is configured (via `.network` unit),
    - the container is started from the pre-pulled image,
    - IP and MAC are assigned, and gratuitous ARPs are sent.
- **Monitor**

  - Pacemaker checks the systemd service state (active, failed, etc.).
  - Healthchecks can be defined in the Quadlet `.container` file (via `--health-*` options), allowing systemd to reflect container health.
- **Stop**

  - Pacemaker calls `systemctl stop my-stack.service`.
  - The container is gracefully shut down, macvlan interfaces are removed (if defined in the unit), and ephemeral state is cleaned up by systemd.
- **Failover**

  - On node failure or policy-triggered migration:

    - Pacemaker detects failure,
    - selects a new node,
    - starts the same systemd unit there,
    - recreates the macvlan IP/MAC,
    - CephRBD-mounted volumes provide access to persistent data,
    - network reconvergence is handled via gratuitous ARPs.

---

### Failover Flow (Sequence)

1. Pacemaker detects a node failure (heartbeat loss or service failure).
2. Pacemaker selects another node and starts the container’s systemd unit.
3. The target node:

   - mounts Ceph RBD if not already mounted,
   - ensures macvlan network is configured,
   - starts the container from its local image,
   - brings up the configured IP/MAC and sends gratuitous ARPs.
4. Clients continue to reach the same IP/MAC.  
   Persistent data remains available through Ceph RBD.

---

### Operational Caveats & Gotchas

- **Local Podman storage**:  
  Container images must be local. Pre-pull images to minimize failover time.
- **Macvlan specifics**:

  - Containers are isolated from the host network namespace.
  - MAC migration may require coordination with network/security teams.
  - Some environments may prefer ipvlan or IP resource + NAT.
- **Fencing**:  
  Proper fencing is required to avoid concurrent access to shared storage during failover.
- **SELinux & mounts**:  
  Ensure Ceph RBD mounts are labeled correctly for container access (`:z` / `:Z` mount options or proper fs labels).
- **Root privileges**:  
  Creating macvlan interfaces requires root. Pacemaker runs the systemd service as root.
- **Startup time**:  
  Pre-pulling images with Ansible significantly improves recovery time.

---

This architecture uses Pacemaker only to orchestrate **systemd-managed Quadlet units**, relying on existing, well-integrated tooling. This simplifies lifecycle management, reduces maintenance overhead, and keeps the HA logic clear and transparent.
