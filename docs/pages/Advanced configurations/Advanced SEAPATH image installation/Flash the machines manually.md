
[Advanced configurations](../../Advanced%20configurations.md) > [Advanced SEAPATH image installation](../Advanced%20SEAPATH%20image%20installation.md)

# Flash the machines manually

> [!WARNING]
> This page describe the manual method for installing SEAPATH. We recommend you to install SEAPATH using the official installer. See [Install SEAPATH](../../Getting%20started/Quick%20start/Install%20SEAPATH.md)

This page assumes that you already have a SEAPATH image ready. If not, Read [Build and configure a custom image](Build%20and%20configure%20a%20custom%20image.md)

> [!NOTE]
> The flashing process is different between Yocto and Debian.
>
> However, within one distribution, flashing a standalone machine or a cluster machine is the same. When this section mentions “the SEAPATH image”, this can either be the standalone or the cluster one, depending on what you choose.

# Yocto

## Prepare the USB key

The USB key is prepared in two steps

- Flash the USB key with the flasher image
- Copy the SEAPATH image on the USB key

### Flash the USB key

Flash the USB key with the **flasher image** . This can be done with

> [!IMPORTANT]
> The flasher image is generic, if you can build it from source, but it is simpler to get it on the last release page of SEAPATH. Download the [flasher image](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-flasher-image.rootfs.wic.gz) and its [bmap file](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-flasher-image.rootfs.wic.bmap).

- Graphical tool like [balenaEtcher](https://etcher.balena.io/) (recommended for non IT people)
- Command line [bmap-tool](https://github.com/seapath/yocto-bsp?tab=readme-ov-file#flashing-the-flasher-image-to-an-usb-drive) (recommended for IT people)
- A standard `dd` command

### Copy the SEAPATH image on the USB key

Once the flashing is done

- Mount the USB key on your computer (you can also unplug the key from your computer, and plug it again. It will be auto-mounted)
- Copy your image into the *flasher\_data* partition.

> [!IMPORTANT]
> You should copy two files in the partition: the wic.gz file and the wic.bmap file.

## Flash the hypervisor

Unmount the USB key from your computer and plug it into the SEAPATH machine.

Boot on the USB key and log into the machine using the “root” user (no password required)

Flash the server using the `flash` command

```java
 flash --image /media/<your_image>.wic.gz --disk /dev/<selected_disk>
```

Reboot the machine and remove the USB key

> [!NOTE]
> If you are setting up a cluster, repeat the flashing part on the three hypervisors

## Debian

## Prepare the USB key

There is only one step to prepare the USB key on Debian

Flash the USB key with the SEAPATH image. This can be done with

- Graphical tool like [balenaEtcher](https://etcher.balena.io/) (recommended for non IT people)
- A standard `dd` command (recommended for IT people)

## Flash the hypervisor

Plug the USB key into your server and boot onto it.

The flashing process will start automatically, displaying the logs on the screen

> [!IMPORTANT]
> SEAPATH will be flashed on the first disk in alphabetical order

> [!NOTE]
> If you are setting up a cluster, repeat the flashing part on the three hypervisors
