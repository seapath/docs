
[Advanced configurations](../../Advanced%20configurations.md) > [Advanced SEAPATH image installation](../Advanced%20SEAPATH%20image%20installation.md)

# Build and configure a custom image

This section first describe how to get a default pre-built image from the SEAPATH release.  
If this image doesn’t suit your needs, you can generate your own with multiple configurations in the section below.

Once your image is ready, you can flash it on your machine using the seapath-installer. See TODO

> [!IMPORTANT]
> This section assumes you have a build machine ready. See [External support machines](../../Getting%20started/Prerequisites/External%20support%20machines.md) for more information

# Use a pre-built image

Pre-built SEAPATH images are published at each release. You can use them to skip the building part of the images. Be aware that this image is configured for a default standard use case. If you want a more advanced usage in the future, you will have to customize and build the image yourself.

> [!NOTE]
> SEAPATH images embed their own SSH keys. For the release, default SSH keys have been used.  
> These keys are published along with the release, in order to access the machine when deployed.  
> Therefore, these keys are not safe.  
>   
> **Pre-built images must only be used for testing and not in production**

## Download the necessary files

The image will be downloaded on the release pages of the [yocto-bsp](https://github.com/seapath/yocto-bsp/releases) and the [build-debian-iso](https://github.com/seapath/build_debian_iso/releases) repositories.

First, you must download the [SSH private key file](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-artifacts-key) from the release and put it in your ~/.ssh/ folder. This will be used to access the SEAPATH machine once deployed.

Then, you should download the necessary images

### For Yocto

- Download the [flasher image](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-flasher-image.rootfs.wic.gz) and its [bmap file](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-flasher-image.rootfs.wic.bmap).
- For a standalone setup, download the [standalone image](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-host-standalone-efi-image.rootfs.wic.gz) and its [bmap file](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-host-standalone-efi-image.rootfs.wic.bmap).
- For a cluster setup, download the [cluster image](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-host-cluster-efi-image.rootfs.wic.gz) and its [bmap file](https://github.com/seapath/yocto-bsp/releases/download/v1.1.0/seapath-v1.1.0-host-cluster-efi-image.rootfs.wic.bmap).

### For Debian

- For a standalone setup, download the [standalone image](https://github.com/seapath/build_debian_iso/releases/download/v1.1.0/seapath-v1.1.0-host-standalone.iso).
- For a cluster setup, download the [cluster image](https://github.com/seapath/build_debian_iso/releases/download/v1.1.0/seapath-v1.1.0-host-cluster.iso).

# Build Yocto-based image

This section assumes you have a build machine ready. See [External support machines](../../Getting%20started/Prerequisites/External%20support%20machines.md) for more information

### Software prerequisites

Follow the [yocto-bsp prerequisites](https://github.com/seapath/yocto-bsp?tab=readme-ov-file#prerequisites) section to download Docker, cqfd and repo.

### Get the source code

Create a directory on your machine to download the sources, and cd into it. For example:

```java
mkdir ~/seapath-yocto
cd ~/seapath-yocto
```

Clone the sources

```java
repo init -u "https://github.com/seapath/repo-manifest.git"
repo sync
```

> [!NOTE]
> You can download a specific version with the `-m` argument.  
> For example, to download the v1.2.0, use  
> `repo init -u "https://github.com/seapath/repo-manifest.git" -m v1.2.0.xml`

### Prepare the sources

Copy the configuration file of SEAPATH.

```java
cp seapath.conf.sample seapath.conf
```

> [!IMPORTANT]
> This `seapath.conf` file can be customized for your needs. For a first SEAPATH build, going with the default is sufficient.

Copy your SSH key

```java
cp <your_ssh_key_public_file.pub> keys/ansible_public_ssh_key.pub
```

If you don’t have an SSH key, you can follow this [documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) by GitHub.

Prepare the cqfd container

```java
cqfd init
```

### Launch the build

Launch either the standalone or the cluster image build, depending on your needs :

Standalone:

```java
cqfd -b host_standalone_efi
```

Cluster:

```java
cqfd -b host_efi
```

> [!NOTE]
> The build of SEAPATH will take approximately 4 to 5 hours on a current developer machine and will produce approximately 50GB of data.

**Get the built images**

In the directory `build/tmp/deploy/images/seapath-hypervisor`, you should get

- seapath-host-efi-image-seapath-hypervisor.rootfs.wic.gz
- seapath-host-efi-image-seapath-hypervisor.rootfs.wic.bmap

## Tips for building

- About 250GB is needed for building SEAPATH.
- A USB attached storage may be too slow to be practical for a successful build.
- Ensure you use an ext 2/ ext3 / ext4 filesystem for the build directory. NTFS will not work.
- Watch out with only manually deleting the /tmp/work directory. Instead delete the whole tmp directory.
- When deleting the tmp, it may take a very long time, and might cause `rm -rf` to fail with an error. `find . -delete` will work better, as it will not try to index all files before deleting them.

# Build Debian-based image

This section assumes you have a build machine setup. See [External support machines](../../Getting%20started/Prerequisites/External%20support%20machines.md) for more information

### Software prerequisites

Download Docker and docker-compose on your machine.

### Get the source code

Clone the sources and cd into the directory.

```plain
git clone https://github.com/seapath/build_debian_iso.git
cd build_debian_iso
```

> [!NOTE]
> You can download a specific version with the `-b` argument.  
> For example, to download the v1.2.0, use  
> `git clone -b v1.2.0 https://github.com/seapath/build_debian_iso.git`

### Prepare the sources

Copy the configuration file of SEAPATH.

```java
cp srv_fai_config/class/SEAPATH_COMMON.var usercustomization/class/SEAPATH_COMMON.var
```

Open this file with your favorite text editor and put your SSH **public** key in the file

```java
myrootkey='ssh-rsa XXX'
myuserkey='ssh-rsa YYY'
ansiblekey='ssh-rsa ZZZ'
```

Your public SSH key should be accessible in `~/.ssh/<key-name>.pub`. If you don’t have an SSH key, you can follow this [documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) by GitHub.

> [!IMPORTANT]
> If your lab setup has a DHCP server and you wish to set up the IP address of the SEAPATH machine with DHCP, you can enable the DHCP method on the last line of this file with `REMOTEDHCP=all`.  
> This also requires commenting the variables `REMOTENIC`, `REMOTEADDR` and `REMOTEGW`  
> This feature is meant for IT users who already manage networks. For all other users, the IP of each machine will be set manually after the flashing process.

### Customization

In the usercustomization class file, you can define these variables:

- `FAI_ALLOW_UNSIGNED`: Boolean to allow installation of packages from unsigned repositories (0 => true)
- `UTC`: Boolean to set the system clock to UTC (possible values: yes or no)
- `TIMEZONE`: Time to choose
- `KEYMAP`: Keyboard translation to choose
- `ROOTPW`: Crypted password for root
- `STOP_ON_ERROR`: FAI error threshold. In FAI each error has a score. If the error is greater than `STOP_ON_ERROR` then the installation will fail. The default is 700.
- `MAXPACKAGES`: Max packages installed at a time. If you have a small /var partition and you encounter error, try a reduce this variable number.
- `username`: ID of the user account to be created
- `USERPW`: Crypted password for the user account to be created
- `usernameansible`: ID of the ansible account to be created
- `myrootkey`: SSH root user public key. If not set SSH root user connexion will be disabled.
- `myuserkey`: SSH admin user public key.
- `ansiblekey`: SSH ansible user public key.
- `apt_cdn`: Debian registry to use. Change this if you have a local Debian registry mirror.
- `REMOTENIC`: Network interface to be set
- `REMOTEADDR`: IP address to be set on `REMOTENIC` with the mask
- `REMOTEGW`: IP address for the gateway to be set on `REMOTENIC`

However, all host will be with the same IP address.

### Disks customization

The disk is composed:

1. (If the installation is in UEFI) EFI partition in `/boot/efi` with VFAT filesystem (512 MB).
2. Boot partition in `/boot` with ext4 filesystem (500 B).
3. Main partition with LVM configuration (30 GB). This partition is divided into 3 parts:

   1. Root partition in `/` with ext4 filesystem (7 GB).
   2. Log partition in `/var/log` with ext4 filesystem (1 GB).
   3. Swap partition (500 B).

This can be overriden in the `build_debian_iso/usercustomization/disk_config/USERCUSTOMIZATION` file.

### Launch the build

Launch the image build

> [!WARNING]
> If you are using v1.2 or older version of SEAPATH, you should use `./build_iso.sh` and `./build_iso.sh --custom`. See build\_debian\_iso README for more information.
>
> Also, you must use the legacy flashing method for custom Debian ISOs See [Flash the machines manually](Flash%20the%20machines%20manually.md)
>
> If you are using the main version of SEAPATH, you can proceed as described below and use seapath-installer

Launch the build of a raw SEAPATH Debian image with the command

```java
./generate_seapath_image.sh <flavor>
```

The flavor can be “standalone”, “cluster” or “observer”

**Get the built image**

The built image is available at the root of the directory under the name `seapath.raw`.

### Video tutorial

You can also watch a video tutorial:
