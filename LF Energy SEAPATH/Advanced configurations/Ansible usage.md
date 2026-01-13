
[Advanced configurations](../Advanced%20configurations.md)

# Ansible usage

SEAPATH uses Ansible to configure and manage the infrastructure. This page assumes you know Ansible basics.

> [!IMPORTANT]
> If you are not familiar with Ansible at all, you can read <https://docs.ansible.com/ansible/latest/getting_started/index.html> and <https://docs.ansible.com/ansible/latest/getting_started/basic_concepts.html>

A SEAPATH Ansible collection is available on <https://github.com/seapath/ansible>

It’s documentation is displayed on <https://galaxy.ansible.com/ui/repo/published/seapath/ansible/>

# Ansible use on SEAPATH

SEAPATH image building differs between Debian- and Yocto- based SEAPATH:

- The Debian image contains a minimal set of configurations to allow an installation without internet access. It then necessitates a specific configuration step with Ansible.

- The Yocto image is compiled with all the configuration and hardening. It does not necessitate this additional step

Ansible has then three different uses on SEAPATH:

- Configure the operating system for SEAPATH requirements (only for Debian). This includes all the “debian” named roles and playbooks
- Configure the SEAPATH infrastructure (e.g., network, time synchronization, cluster …). All these actions cannot be done at compile time, because they directly depend on the environment where the machine will be deployed (IP addresses, physical network connection, number and types of machines …)
- Managing the infrastructure after initial deployment (deploy VMs, modify a configuration, update or change a machine …)

> [!IMPORTANT]
> The infrastructure configuration and management steps are the same for the two distributions

# Inventory structure

The structure of the inventories is described on <https://galaxy.ansible.com/ui/repo/published/seapath/ansible/>.

# Roles and playbook usage

SEAPATH divides its tasks into roles. You can find the list of roles and their use on <https://galaxy.ansible.com/ui/repo/published/seapath/ansible/>.

All the customization and extension offered by SEAPATH comes in Ansible variables to provide or modify in the inventory. These variables are described in each role page README on Ansible galaxy.

A list of playbooks is also available in the repository. You can use the main playbook to deploy a full SEAPATH infrastructure without having to worry about the details.  
However, for production usage, we strongly recommend writing your own playbook by calling only the necessary roles.

The rest of the playbooks can be used to redeploy specific parts of the SEAPATH configuration when you want to change some things.
