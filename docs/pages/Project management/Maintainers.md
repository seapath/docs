
[Project management](../Project%20management.md)

# Maintainers

# GitHub configuration

All repositories are configured with two rulesets:

- `default`: Protect the default branch
- `default-yocto`: Does the same as `default` but also protect LTS branches: `wrynose`,`scarthgap` and `kirkstone`
- `disable branches and merge for members`: Avoid members pushing branches and merging PRs

Ansible have an additional ruleset because of the legacy branches (`debian-main`, `debiancentos`, `yocto_legacy`)

Ansible, `build_debian_iso`, `yocto_bsp` and `meta-seapath` have an additional CI ruleset for the CI

# Release procedure

For a new `vX.Y.Z` release:

## Pre-release stage (before validation test)

### Cockpit images bump

- Change the version in `package.json`
- Tag the repositories with `vX.Y.Z` and create a release. This will automatically upload the npm files to the release.

  - [cockpit-cluster-dashboard](https://github.com/seapath/cockpit-cluster-dashboard)
  - [cockpit-cluster-vm-management](https://github.com/seapath/cockpit-cluster-vm-management)
  - [cockpit-update](https://github.com/seapath/cockpit-update)

### Yocto images bump

- Bump SEAPATH Yocto distribution version

  - If not already done, bump `python3-setup-ovs`, `python3-vm-manager` `python3-svtrace` and cockpit plugins in `recipes-seapath`:

    - `SRCREV`
    - Version in recipe file name for `python3-setup-ovs` and `python3-vm-manager`
- Change the version in SEAPATH distro files for SEAPATH Yocto

### Installer

- Bump versions on the [seapath-installer](https://github.com/seapath/seapath-installer) and [seapath-live-installer](https://github.com/seapath/seapath-live-installer) brandings

Currently, the seapath-live-installer will not build until the seapath-installer release is made on GitHub.  
We should re-think the live-installer CI in the future. For now, you can force merge.

## Validation tests

Generate all SEAPATH images (Debian, Yocto) and installer using a manual trigger on <https://github.com/seapath/.github/actions/workflows/build-release.yml>.

This will make all images accessible on <http://releases.seapath.org/builds/> after around 2h of build.

### Yocto cluster

Setting up a virtual cluster requires at least 32GB of RAM on the physical host machine.

- Clone the SEAPATH virtual cluster repository: <https://github.com/seapath/virtual-cluster>
- Ensure all the prerequisites are met (see the [README](https://github.com/seapath/virtual-cluster/blob/dev/README.md) file)

> [!WARNING]
> Virtual cluster cannot be used in a containerized environment. Make sure all the needed dependencies are installed.

- Inside the `virtual-cluster` repository, clone the SEAPATH Ansible repository with the Git reference that will be the release
- Fetch the SEAPATH Yocto hypervisor VM qcow2 release file from the [releases.seapath.org](http://releases.seapath.org) repository in the `images/`folder
- Fetch the SEAPATH Yocto guest VM qcow2 release file from the [releases.seapath.org](http://releases.seapath.org) repository in the `images/`folder
- Ensure that your SSH public keys are configured with the published SEAPATH SSH public key
- Configure the Terraform variable file with the path to your SEAPATH virtual hypervisor image:

```bash
cp terraform.tfvars.example terraform/terraform.tfvars
sed -i 's|^base_image_path = ".*"|base_image_path = "/path-to-your-image"|' terraform/terraform.tfvars
```

- Configure virtual hypervisors and start them using the following commands:

```bash
make init
make apply
make start
make ansible-ping
make ansible-grow-rootfs
```

- Test that each virtual hypervisor are running:

```bash
make ansible-ping
```

- Run the full SEAPATH setup:

```bash
make ansible-setup ANSIBLE_REPO=/path/to/ansible
```

- Deploy a guest VM in the cluster:

```bash
make ansible-deploy-vm ANSIBLE_REPO=/path/to/ansible
```

- Finally run all the Cukinia hypervisor tests:

```bash
make ansible-cukinia-tests ANSIBLE_REPO=/path/to/ansible
```

TODO: change this section after virtual cluster

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

### Yocto standalone

- Recover the Yocto standalone **test** image from the last <http://releases.seapath.org/builds/>
- Update the Yocto standalone CI
- Launch a weekly CI: <https://github.com/seapath/ansible/actions/workflows/ci-yocto-weekly.yml>

### Debian (cluster and standalone)

- Ask Florent to update the Ci images (if necessary)
- Trigger a weekly CI on ansible Debian: <https://github.com/seapath/ansible/actions/workflows/ci-debian-weekly.yml>

Note that the cluster part may be subject to changes once virtual cluster is ready

### Installer empty

- Recover the empty installer from the last <http://releases.seapath.org/builds/>
- Recover one Debian and one Yocto SEAPATH image from the last <http://releases.seapath.org/builds/>
- Add these images and an SSH key to the empty version of the installer
- Test both images

  - Flash
  - Boot
  - Verify SSH key is ok

### Installer bundled

- Recover the bundled installer from the last <http://releases.seapath.org/builds/>
- Test **all images** present in the bundled version of the installer

  - Flash
  - Boot
  - Verify SSH key
  - Verify DHCP and static IP for at least one image

## Release stage (once validation passed)

### repo-manifest

- Recover the repo manifest from the last <http://releases.seapath.org/builds/>
- Use this `vX.Y.Z.xml` file as default manifest
- tag the repo-manifest repository
- Revert the default repo-manifest

### Installer

- Tag with `vX.Y.Z` and release seapath-installer

  - It will automatically add the .deb to the release
- Tag with `vX.Y.Z` and release seapath-live-installer

  - It will automatically add the empty installer to the release
- Add bundled installer to cloudfare

  - Get bundled installer from the last <http://releases.seapath.org/builds/>
  - Upload bundled version to `s3://seapath-releases/seapath-installer-bundled/` (you can use [s3cmd](https://github.com/s3tools/s3cmd) to do it)
  - Add the link and SHA on [Install SEAPATH](../Getting%20started/Quick%20start/Install%20SEAPATH.md)
  - Provide the link and SHA to the bundled version of the installer to <https://github.com/seapath/seapath-live-installer/releases>

### Tag repositories

- tag these repositories with `vX.Y.Z`:

  - ansible
  - build\_debian\_iso
  - yocto\_bsp
  - meta-seapath
  - vm\_manager
  - python3-setup-ovs

### Create releases

- Create release and write release notes for

  - ansible (it automatically uploads ansible galaxy release)
  - build\_debian\_iso
  - yocto\_bsp
- Add artifacts in releases

  - ansible (TODO tar.gz)
- In this of none bug fixes version create the issue label tag in wanted repos.

  - Name: `vX.Y.Z`
  - Description: `Version vX.Y.x issues.`
  - Color: use the same color from all repos
  - Example of gh command: `gh label create v2.0 --description "Version v2.0.x issues." --color ccda67`
  - Repos:

    - yocto\_bsp
    - meta-seapath
    - vm\_manager
    - python3-setup-ovs
    - ansible
    - build\_debian\_iso
    - cockpit-cluster-dashboard
    - cockpit-cluster-vm-management
    - cockpit-update
    - virtual-cluster
- Write a wiki page with all the release note
