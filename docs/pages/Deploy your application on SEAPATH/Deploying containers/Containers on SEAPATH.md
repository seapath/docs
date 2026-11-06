
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying containers](../Deploying%20containers.md)

# Containers on SEAPATH

Container support is fully functional on SEAPATH 2.0 release.

However, the setup requires many manual configuration and is not correctly streamlined in Ansible for now

### Goals

- Run a container stack (one Quadlet-defined unit or a small pod of containers) on a host.
- If that host fails, automatically start the same stack on another host with the same IP and MAC, so services remain reachable without reconfiguration.
- Keep deployment and operations simple — no Kubernetes or heavy orchestration layers.
- Reuse the existing SEAPATH building blocks (Pacemaker/Corosync, Ceph via cephadm).
- Make deployment fully automatable with Ansible.

### Constraints & Existing Stack

- SEAPATH already runs VM workloads with KVM and relies on:

  - Pacemaker / Corosync for HA
  - Ceph (managed with cephadm)
  - Open vSwitch / standard Linux networking
- Ceph can provide distributed and resilient storage for volumes across cluster nodes (via the use of RBD, exactly like for virtual machines).
- Cephadm uses Podman by default, making Podman the natural container runtime.

### Key Design Choices and Rationale

### Podman and systemd Quadlets

- **Quadlets provide a native way to define and manage containers through systemd units**, turning containers into first-class system services.
- They allow clean, lightweight integration with existing service management and Pacemaker primitives — **no extra resource agent or custom tooling** is needed.
- **Podman remains the container runtime**, with systemd handling lifecycle events (start, stop, restart, monitor) in a predictable and stable way.

**Additional advantages for SEAPATH use cases:**

- **Fine-grained control over CPU affinity and real-time priorities:**  
  Quadlets inherit the full range of systemd service configuration options. This makes it straightforward to set CPU pinning, scheduling policies, and priorities — which is critical for SEAPATH’s real-time workloads.
- **Rich service orchestration features out of the box:**  
  With systemd, containers can define:

  - `ExecStartPre` / `ExecStartPost` hooks for pre-start and post-start actions (e.g. preparing volumes, sending gratuitous ARPs),
  - dependency chains (`Requires=`, `Wants=`, `After=`) for coordinating with other services or network initialization,
  - restart policies, resource limits, and cgroup configuration.
- **Native monitoring and integration:**  
  Systemd provides built-in service supervision and health reporting, which Pacemaker can use directly, simplifying the HA logic compared to maintaining a custom Pacemaker resource agent.

In short, Quadlets bring **a more robust, feature-rich, and maintainable integration layer** between Podman containers and Pacemaker, while satisfying SEAPATH’s real-time and deterministic execution requirements.

#### Quadlet units as the HA resource

- Each HA resource corresponds to a fully defined Quadlet stack (a directory containing the container or pod description, environment files, and volume definitions).
- This keeps operational semantics simple: start/stop a single unit representing the entire stack, rather than managing individual containers.

#### Pacemaker for availability and migration

- Pacemaker already provides host-level HA and failover.
- It starts and stops the Quadlet-defined container stack on the active host and ensures the required network failover steps are executed.

#### Ceph RBD for configuration and persistent data

- Ceph stores persistent volume data in rbd images (mapped and mounted into containers at runtime).
- Container image layers remain local to the nodes
- Images can be pre-pulled or updated on each node to ensure fast failover.

#### Macvlan network with migratable IP & MAC

- A macvlan network gives containers a stable MAC and IP on the L2 network.
- When a stack moves, Pacemaker recreates the same IP and MAC on the new host and sends gratuitous ARPs so network switches update their tables.
- Clients continue to reach the service seamlessly.

#### Automated Deployment with Ansible

- The entire process — creating Quadlet definitions, mapping and mounting Ceph rbd images, configuring network failover, and registering Pacemaker primitives — is automated through Ansible for repeatable, cluster-wide deployment (see [this page](Containers%20deployment.md))

### Why not Kubernetes?

Kubernetes provides large-scale orchestration but adds significant operational overhead and infrastructure complexity.  
For SEAPATH, the goal is to deliver a **simple, robust HA container primitive** using the existing stack — similar to VM failover behavior — without introducing a new orchestration layer.
