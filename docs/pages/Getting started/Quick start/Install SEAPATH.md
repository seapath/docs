
[Getting started](../../Getting%20started.md) > [Quick start](../Quick%20start.md)

# Install SEAPATH

The SEAPATH installation uses the [seapath-installer](https://github.com/seapath/seapath-installer) tool. It can:

- Install SEAPATH (Yocto/Debian or others) on the physical machine disk
- Configure basic access to the SEAPATH machine (SSH keys, IP address, keyboard layout, etc), without needing to regenerate an image

The installation process is done though a live environment, booted from a USB key.

# Get the installer

Get the release of the installer, with SEAPATH images embedded inside.

|                                                                                                                         |                                                                                                                                                                              |
|:------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Installer with SEAPATH images v2.0.0 <br/> SHA256: `ad4405d99732bd9ce5edd466d96b74b3efaa877c3c63aa75d010d4ccfc2f59c3`   | [seapath-live-installer-v2.0.0-seapath-images-v2.0.0.iso.zip](https://releases.seapath.org/builds/v2.0.0/seapath-live-installer-v2.0.0-seapath-images-v2.0.0.iso.zip)       |
| Installer with SEAPATH images v1.2.1 <br/> SHA256: `b7253125108520f305e07ed44a8a05b9c211a0ed187bebb05911e9378c4778a5`   | [seapath-live-installer-1.2.2-seapath-images-1.2.1.iso.zip](https://releases.seapath.org/seapath-installer-bundled/seapath-live-installer-1.2.2-seapath-images-1.2.1.iso.zip) |
| Installer with SEAPATH images v1.2.0 <br/> SHA256: `f37744dfd4d0f3ff6a717b4c10aeab7420e2ecda8285be257dcb7520d66617d4`   | [seapath-live-installer-1.2.1-seapath-images-1.2.0.iso.zip](https://releases.seapath.org/seapath-installer-bundled/seapath-live-installer-1.2.1-seapath-images-1.2.0.iso.zip) |

## Flash the installer

Unzip the file and flash the .iso on a USB key

This can be done with

- Graphical tool like [balenaEtcher](https://etcher.balena.io/) (recommended for non IT people)
- A standard `dd` command (recommended for IT people)

The USB key must have 8GB of memory at minimum.

# Use the installer

> [!IMPORTANT]
> By default, the installer is filled with default images and default SSH keys. For a first SEAPATH test, we recommend sticking to that.  
> For more advanced usage, you can read about modifying the SSH key and images at [Advanced SEAPATH image installation](../../Advanced%20configurations/Advanced%20SEAPATH%20image%20installation.md)

## Boot on the installer

Plug the installer USB key on the target machine and configure your BIOS boot entries to boot on it.

Once booted, the installer automatically shows up on the screen.

![image-20251210-152137.png](../../../assets/16812f15-ddbf-49ea-a786-bc431617e08c.png)

From now, follow the instruction on the screen to install SEAPATH on your  
target machine.

Once the installation process is done you can reboot the target machine.

> [!NOTE]
> The machine will reboot directly on the installed SEAPATH. Once its done, you can remove the installer USB key

## Report an issue

If you encounter an issue on the use installer, you can raise an issue of the following repositories:

- <https://github.com/seapath/seapath-installer> for the installer tool itself.
- <https://github.com/seapath/seapath-live-installer> for the live OS environment.

# Go on with your machine configuration

> [!NOTE]
> All of your SEAPATH machines must be flashed with the installer.  
> If you are setting up a cluster, repeat [Use the installer](#use-the-installer) on each hypervisor.

Once your machine(s) is flashed, you shall continue the configuration by following the next pages of the Quick start

- [Wire and connect to the machines](Wire%20and%20connect%20to%20the%20machines.md)
- [Configure the machines](Configure%20the%20machines.md)
- [Deploy your first virtual machine](Deploy%20your%20first%20virtual%20machine.md)
