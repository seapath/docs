
[Project management](../Project%20management.md)

# Maintainers

# GitHub configuration

All new repositories must be configured to use the following branch ruleset: <https://raw.githubusercontent.com/seapath/.github/main/branch-default-ruleset.json>.

To enable it:

- Go to the project settings
- In the left menu, select "Rulesets" in "Rules"
- Click on the "New ruleset" button, then "Import a ruleset"
- Select the "branch-default-ruleset.json"
- On the new screen go to the end, click on the button "Create"

# Release procedure

For a new vX.Y.Z release:

- Bump SEAPATH Yocto distribution version

  - If not already done, bump python3-setup-ovs, python3-vm-manager python3-svtrace and cockpit plugins in `recipes-seapath`:

    - SRCREV
    - Version in recipe file name for python3-setup-ovs and python3-vm-manager
- Change the version in SEAPATH distro files for SEAPATH Yocto
- Change the version in `package.json` in the repositories:

  - <https://github.com/seapath/cockpit-cluster-dashboard>
  - <https://github.com/seapath/cockpit-cluster-vm-management>
  - <https://github.com/seapath/cockpit-update>
- Add `vX.Y.Z.xml` file in repo-manifest (pointing to vX.Y.Z repositories using commit ID)
- Use this `vX.Y.Z.xml` file as default manifest
- tag these repositories with vX.Y.Z:

  - ansible
  - build\_debian\_iso
  - yocto\_bsp
  - meta-seapath
  - ansible-role-systemd-networkd
  - vm\_manager
  - cockpit-cluster-vm-management
  - cockpit-cluster-dashboard
  - cockpit-update
  - python3-setup-ovs
  - repo-manifest
  - snmp\_passpersist
  - ~~cukinia-tests~~
- Revert the repo-manifest
- Publish ansible code on ansible-galaxy with version vX.Y.Z
- Write a wiki page with all the release note
- Write one dedicated release note for the following repositories :

  - ansible
  - build\_debian\_iso
  - yocto\_bsp
  - [cockpit-cluster-dashboard](https://github.com/seapath/cockpit-cluster-dashboard)
  - [cockpit-cluster-vm-management](https://github.com/seapath/cockpit-cluster-vm-management)
  - [cockpit-update](https://github.com/seapath/cockpit-update)
- Add artifacts in releases
- Update the CIs

## Release validation tests

The following tasks should be validated before any new release.

### Yocto

- Validate the build and generate the image for the release `cqfd -b release`

- Create a SEAPATH flasher USB key.
- Clone the revision that will be release of SEAPATH Ansible
- Set up the Ansible inventory for

  - Standalone machine
  - Cluster

    - 2 hypervisors
    - 1 observer
    - 1 VM
- **Flash and validate a standalone hypervisor**

  - Flash a machine with the built standalone release image using the flasher
  - Boot the newly flashed machine, check that it is reachable from SSH
  - Configure the standalone hypervisor: `cqfd run ansible-playbook --limit standalone_machine -i <inventory-to-use> playbooks/seapath_setup_main.yaml`
  - Check that cukinia tests succeed : `sudo cukinia`
- **Deploy and validate SEAPATH guest VM on a standalone machine**

  - Using the SEAPATH guest VM previously built, deploy it in the cluster

    - `cqfd run ansible-playbook playbooks/deploy_vms_standalone.yaml -i <path-to-inventory>`
  - Open a console in the VM (`vm-mgr console` or via SSH)
  - Check that cukinia tests succeed: `sudo cukinia`
- **Flash and validate cluster hypvervisors and observer**

  - Flash a SEAPATH cluster: 2 hypervisors and 1 observer
  - Boot the newly flashed machine, check that it is reachable from SSH
  - Run Ansible setup on the SEAPATH cluster

    - Set up the Ansible inventory for the cluster
    - Configure the cluster `cqfd run ansible-playbook --limit cluster_machines playbooks/seapath_setup_main.yaml`
  - Check that cukinia tests succeed on hypervisors and observer : `sudo cukinia && sudo cukinia /etc/cukinia/cukinia-cluster.conf`
- **Deploy and validate SEAPATH guest VM in a cluster**

  - Using the SEAPATH guest VM previously built, deploy it in the cluster

    - `cqfd run ansible-playbook playbooks/deploy_vms_cluster.yaml -i <path-to-inventory>`
  - Open a console in the VM (`vm-mgr console` or via SSH)
  - Check that cukinia tests succeed: `sudo cukinia`
  - Test VM migration

    - `sudo crm ressource move <vm-name> <destination-node>`

### Debian

**TODO**
