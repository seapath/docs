
[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [[Under development] Deploying containers](../_Under%20development_%20Deploying%20containers.md)

# Containers deployment

> [!WARNING]
> The full container support on SEAPATH is still in development and not yet functional in any of the official SEAPATH releases.
>
> This section is a forecast of what will be developed in the future, and is still under discussions.
>
> If you wish to deploy a container on an official SEAPATH version, you can simply use docker, but without any high availability cluster support

### Overview

Container high availability on SEAPATH is deployed entirely through **Ansible roles and inventory variables**, reusing the existing SEAPATH stack.  
The workflow consists of:

1. Deploying and mounting **CephFS**
2. Uploading **Quadlet** unit files (for containers and networks) to all candidate nodes
3. Registering the **Pacemaker primitives** for HA orchestration

This approach avoids any custom container orchestration layer — everything is built on standard SEAPATH components: Ceph, Pacemaker, Podman, systemd, and Ansible.

---

### Step 1 — Deploy CephFS

The `deploy_cephfs` role:

- Deploys the CephFS service on the cluster
- Creates the required directories for container volumes and configuration
- Mounts CephFS on each node (e.g. at `/mnt/cephfs`)

You can then prepares the mount for use by Quadlet containers (e.g. correct permissions and SELinux labels)

Typical directories:

```java
/mnt/cephfs/
 ├── podman-volumes/
     ├── nginx2-html/
     └── nginx2-logs/
```

This ensures that container persistent volumes are **shared across all nodes**, enabling seamless failover.

You don’t even have to prepare those folders, as we will see in the example below, you can rely on a systemd `ExecStartPre`task to do it:

```java
ExecStartPre=mkdir -p /mnt/cephfs/podman-volumes/nginx2-html /mnt/cephfs/podman-volumes/nginx2-logs
```

---

### Step 2 — Upload Quadlet Files

Quadlets define the container and its networking declaratively through `.container`, `.network`, `.volume` (if needed) unit files placed in `/etc/containers/systemd/`.  
These units are automatically picked up by systemd and exposed as standard services.

For this example, we use two Quadlet files:

#### `quadlet-macvlan.network`

```plain
# /etc/containers/systemd/quadlet-macvlan.network
[Unit]
Description=External Ceph macvlan network for containers
After=network-online.target
Wants=network-online.target

[Network]
Driver=macvlan
NetworkName=quadlet-macvlan
Options=parent=br0
Subnet=10.132.170.0/24
Gateway=10.132.170.1

[Install]
WantedBy=multi-user.target
```

This defines the macvlan network that the container will attach to, ensuring it receives a stable IP and MAC address that can migrate between hosts.

#### `nginxquadlet.container`

```java
# /etc/containers/systemd/nginxquadlet.container
[Unit]
Description=Nginx container with Ceph volumes
After=network-online.target quadlet-macvlan-network.service
Wants=quadlet-macvlan-network.service
Requires=quadlet-macvlan-network.service

[Container]
Image=docker.io/library/nginx:alpine
# Volumes with :Z SELinux relabel
Volume=/mnt/cephfs/podman-volumes/nginx2-html:/usr/share/nginx/html:Z
Volume=/mnt/cephfs/podman-volumes/nginx2-logs:/var/log/nginx:Z
# Attach to macvlan network
Network=quadlet-macvlan
IP=10.132.170.202
# Static IP and MAC
PodmanArgs=--mac-address 02:42:ac:1f:0f:03
# Simple demo workload: tail log file into index.html and run nginx
Exec=sh -c "while true; do tail -n 10 /var/log/nginx/access.log > /usr/share/nginx/html/index.html; sleep 2; done & exec nginx -g 'daemon off;'"

[Service]
CPUSchedulingPolicy=fifo
CPUSchedulingPriority=4
Restart=always
ExecStartPre=mkdir -p /mnt/cephfs/podman-volumes/nginx2-html /mnt/cephfs/podman-volumes/nginx2-logs
ExecStartPost=/bin/sh -c 'sleep 2; nsenter -t $(podman inspect -f "{{.State.Pid}}" systemd-nginxquadlet) -n arping -c 3 -A -I eth0 10.132.170.202; exit 0'
```

This unit definition demonstrates how **a single Quadlet file** can combine networking, storage, resource control, and failover behavior into a clean and predictable deployment model. It’s a minimal yet powerful example of what SEAPATH aims to provide.

#### 1. **Floating IP with Transparent Failover**

- The container is configured with a **static IP and MAC address** on a macvlan network (`10.132.170.202` with MAC `02:42:ac:1f:0f:03`).
- Because the IP and MAC are tied to the container definition, they move automatically when Pacemaker migrates the service to another node.
- Clients continue to reach the service on the same IP, without reconfiguration or DNS changes.

This gives us the same **“floating IP” behavior** used in traditional HA setups, but fully handled through standard Podman + systemd + Pacemaker — no external IP resource agent required.

---

#### 2. **ARP Refresh to Eliminate Downtime**

- The `ExecStartPost` hook runs a short `arping` command inside the container’s network namespace right after it starts:

  ```java
  nsenter -t $(podman inspect -f "{{.State.Pid}}" systemd-nginxquadlet) \
    -n arping -c 3 -A -I eth0 10.132.170.202
  ```
- This sends **gratuitous ARPs**, prompting network switches and routers to immediately update their forwarding tables for the floating IP/MAC.

✅ **Result:**  
Failover is almost seamless — typically sub-second or just a few seconds of service interruption, depending on Pacemaker failover timing. This is crucial for real-time or mission-critical systems.

---

#### 3. **Network Dependencies with Quadlets**

- The `[Unit]` section declares:

  ```java
  After=network-online.target quadlet-macvlan-network.service
  Wants=quadlet-macvlan-network.service
  Requires=quadlet-macvlan-network.service
  ```
- This ensures that the container only starts once the macvlan network Quadlet is active and ready.
- This built-in dependency management eliminates the need for custom pre-checks in a resource agent.  
  If the network isn’t available, the unit won’t even try to start, which simplifies failure handling and ensures **deterministic startup order**.

---

#### 4. **Persistent Storage with CephFS**

- The container mounts its content and logs directly from CephFS:

  ```java
  Volume=/mnt/cephfs/podman-volumes/nginx2-html:/usr/share/nginx/html:Z
  Volume=/mnt/cephfs/podman-volumes/nginx2-logs:/var/log/nginx:Z
  ```
- ince CephFS is **mounted on all cluster nodes**, persistent data and configuration follow the container seamlessly.
- On failover, the new node accesses the same shared volume with no extra sync steps.
- SELinux relabeling (`:Z`) ensures secure and correct container access.

✅ **Result:**  
Data persistence and HA behavior are naturally aligned, without requiring external volume replication or complex synchronization.

---

#### 5. **Real-Time Behavior and CPU Control**

- The `[Service]` section sets:

  ```java
  CPUSchedulingPolicy=fifo
  CPUSchedulingPriority=4
  CPUAffinity=12
  ```
- These directives give the container process **real-time scheduling** with a fixed priority.
- Quadlets also allow setting `CPUAffinity` for **core pinning**, guaranteeing deterministic CPU access and predictable latencies — a critical feature for SEAPATH’s real-time use cases.

✅ **Result:**  
Real-time containers can be deployed and migrated with the same HA guarantees as non-RT workloads — something that is **much harder to achieve with traditional container orchestration frameworks**.

---

#### 6. **Pre- and Post-Start Hooks**

- The use of `ExecStartPre` and `ExecStartPost` in the service unit allows:

  - preparing volume directories before container launch,
  - executing ARP announcements after startup,
  - or running any other node-local action needed during failover.

This gives administrators **fine-grained control** over service startup sequencing, directly integrated into systemd, with no custom resource agent logic to maintain.

---

#### 7. **Simplicity and Maintainability**

- All the HA logic — IP migration, persistent storage, startup sequencing, real-time configuration — is expressed in a **single Quadlet file**.
- Pacemaker only needs to manage a standard systemd service (see part 3) :

  ```java
  primitive nginxquadlet systemd:nginxquadlet.service ...
  ```
- No custom scripts, no special resource agents, no container orchestration platform.

✅ **Result:**

- Easy to deploy with Ansible (upload file + create primitive).
- Easy to understand and debug (standard systemd + Podman logs).
- Easy to extend (more containers, networks, hooks).

#### Ansible inventory example to upload these files

```java
upload_files:
  - { src: '../inventories_private/quadlet-macvlan.network', dest: '/etc/containers/systemd/quadlet-macvlan.network', mode: "0644" }
  - { src: '../inventories_private/nginxquadlet.container', dest: '/etc/containers/systemd/nginxquadlet.container', mode: "0644" }
```

These files are deployed automatically by the `debian_prerequisites` playbook.  
Once uploaded, systemd automatically exposes them as `quadlet-macvlan-network.service` and `nginxquadlet.service`.

---

### Step 3 — Create Pacemaker Primitive

With the Quadlet units present on all nodes, we can register the container as a **Pacemaker primitive** using the standard `systemd` resource agent.

#### Example:

```java
extra_crm_cmd_to_run: |
  primitive nginxquadlet systemd:nginxquadlet.service \
    op monitor interval=30s \
    op start timeout=60s interval=0s \
    op stop timeout=60s interval=0s
```

This tells Pacemaker to manage `nginxquadlet.service` as an HA resource:

- Start the service on the designated node
- Monitor its health periodically (30 s)
- Stop and restart it on another node in case of failure

This is done with the `configure_ha`role.

---

### Step 4 — Failover Behavior

Once deployed:

1. Pacemaker keeps `nginxquadlet.service` active on one node.
2. If the node fails, Pacemaker:

   - Detects the failure,
   - Starts the same Quadlet unit on another node,
   - Brings up the macvlan interface with the same IP and MAC,
   - Gratuitous ARPs update the network’s forwarding tables.
3. The container continues serving traffic transparently.  
   CephFS provides consistent access to volumes and configuration files.

---

### Step 5 — Automating Everything

The entire workflow can be integrated into a **single Ansible playbook** that:

- Runs `deploy_cephfs` to provision storage,
- Uploads Quadlet unit files with `upload_files`,
- Pre-pulls container images on all candidate nodes,
- Configures Pacemaker primitives using `extra_crm_cmd_to_run`,
- Optionally defines constraints (e.g. filesystem before container).

This makes container HA deployment on SEAPATH fully **repeatable**, **idempotent**, and **lightweight**, without introducing new orchestration layers.

---

✅ **Result:**  
A simple, fully automated HA container deployment on SEAPATH — using standard tools:  
**CephFS + Podman Quadlets + Pacemaker + Ansible.**
