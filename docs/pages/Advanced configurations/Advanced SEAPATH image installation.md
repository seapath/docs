
[Advanced configurations](../Advanced%20configurations.md)

# Advanced SEAPATH image installation

This page explains how to customize the SEAPATH image installation.

It describes how to customize the installer to embed custom images and SSH keys. Custom images can be built by following [Build and configure a custom image](Advanced%20SEAPATH%20image%20installation/Build%20and%20configure%20a%20custom%20image.md)

> [!NOTE]
> A section is also dedicated to the manual installation of images [Flash the machines manually](Advanced%20SEAPATH%20image%20installation/Flash%20the%20machines%20manually.md). This method allows, among other things, a non-interactive installation.  
> It is however harder to use than the installer. Unless there is a blocking issue, the seapath-installer should be preferred.

# Customize the installer

This section describe how to customize or even rebuild the seapath-installer. It assumes you have flashed the installer on a USB key. See [Install SEAPATH](../Getting%20started/Quick%20start/Install%20SEAPATH.md) for more information

The installer can be customize to modify the installed artifacts installed on the target machine. To do so, plug the flashed installer USB key, on a computer and mount it. The directory `DATA` contains the installer artifacts.

## SEAPATH images

The installer already include the latest public release of SEAPATH:

- SEAPATH Yocto cluster/standalone/observer
- SEAPATH Debian all machines

If you wish to add your own SEAPATH image, you can build them following [Build and configure a custom image](Advanced%20SEAPATH%20image%20installation/Build%20and%20configure%20a%20custom%20image.md)

> [!NOTE]
> The installer currently only support the following images format:
>
> - `.raw.gz` for SEAPATH Debian. No `.bmap` file is needed.
> - `.wic.gz` for SEAPATH Yocto. A `.bmap` file, generated during build, is needed.

## SSH keys

The installer already include the SEAPATH public SSH key. If you wish to add your own public SSH keys, copy them in the directory `DATA/ssh`.

NOTE: The SSH keys must be in `.pub` format.

> [!WARNING]
> The generic SSH key embedded by default in the SEAPATH installer is meant to be used for testing and POC.
>
> **For production, you must use your own SSH key**

## Others

You can add other types of artifacts in the `DATA/others` directory. This directory is only for passing data to the installer, and there will be not installed on the target machine.

## Continue with the flashing process

Once you have loaded your image and SSH keys inside the installer, you can continue with the flashing process [Install SEAPATH](../Getting%20started/Quick%20start/Install%20SEAPATH.md)

# Rebuild the installer

The SEAPATH installer is composed of two projects:

- [seapath-installer](https://github.com/seapath/seapath-installer), the installer tool used to configure and install the SEAPATH image
- [seapath-live-installer](https://github.com/seapath/seapath-live-installer), the live OS environment used to run seapath-installer

## seapath-installer

seapath-installer is based on the [Calamares](https://codeberg.org/Calamares/calamares/) project, aim to provide a distribution independent installer framework. Additionally to what Calamares already provide, we:

- Added a custom SEAPATH branding
- Created custom modules to fit the SEAPATH installation process
- Modified existing Calamares modules to fit the SEAPATH installation process

### Build seapath-installer

First, get the sources:

```java
git clone https://github.com/seapath/seapath-installer.git 
```

Then you can follow the steps described in the [README](https://github.com/seapath/seapath-installer/blob/main/README.md) file.

### Tweaking seapath-installer custom modules

To fit the SEAPATH installation process we developed the following modules:

- `rawimage`: A module used to copy a raw SEAPATH image on a target disk
- `imageselection`: A module used to show the available SEAPATH images to install
- `sshkeyselection`: A module used to show the available SSH public keys to install
- `uefiboot`: A module used to configure the UEFI boot entries once the SEAPATH image is installed

## seapath-live-installer

seapath-live-installer is based on the [debian-live-config](https://gitlab.com/nodiscc/debian-live-config) project, aim to provide a configurable Debian live OS generator. Additionally to what the project already provide, we:

- Added a custom SEAPATH branding (splash screen, desktop wallpaper)
- Removed most of the default packages
- Customize the pre and post build steps to fetch and install the latest SEAPATH images and seapath-installer release in the generated ISO image file

### Build seapath-live-installer

First, get the sources:

```java
git clone https://github.com/seapath/seapath-live-installer.git 
```

Then, follow the steps described in the [README](https://github.com/seapath/seapath-live-installer/blob/main/README.md) file.

### Use your custom version of seapath-installer

If you wish to use your own version of seapath-installer, simply drop the seapath-installer .deb package in the root directory of the project `config/packages/`.
