
[Tests and CI](../../Tests%20and%20CI.md) > [SEAPATH toolbox](../SEAPATH%20toolbox.md)

# SEAPATH benchmark

[seapath-benchmark](https://github.com/seapath/seapath-benchmark) is a tool used to evaluate the performance of a SEAPATH architecture (cluster/standalone) and its components (distributed software, virtualization, real time performance…). The main purpose of seapath-benchmark is to provide a test architecture to measure and monitor the performance of SEAPATH independently of the hardware used. Seapath-benchmark is build upon two core elements:

- The phoronix-test-suite to provide a test backend: test skeleton, test management, results handling, report generation
- Ansible as an orchestrator, used to the run the configuration and execution of tests across various physical and virtual machines.

The main purposes of Seapath-benchmark are:

- Provide tests and monitoring benchmarks for testing the performance of various SEAPATH components.
- Reproducible test scenario agnostic to the hardware used.
- Test results generation in PDF format.

## Available tests

Following phoronix-test-suite typology, seapath-benchmark tests are called test profiles. Test profiles can be one of two types:

- Monitoring test profiles: these tests are used to only monitor various system and SEAPATH sensors (ex: CPU/memory/disk usage, bandwidth consumption, etc.).
- Benchmark test profiles: these tests are used to measure the performance of a particular system or SEAPATH components (ex: CPU, memory, disk, VM migration...).

|                     |                       |                              |                                                        |                                                                                                                                                                                                                  |                                                         |                                                         |
|:--------------------|:----------------------|:-----------------------------|:-------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------|:--------------------------------------------------------|
| **Name**            | **Test profile type** | **Tested components**        | **Compatible machines and infrastructure**             | **Test arguments**                                                                                                                                                                                               | **Generated results**                                   | **Needed dependencies**                                 |
| cpu                 | Benchmark             | CPU, virtualization stack    | Hypervisor and VMs, all SEAPATH configuration          | <ul><li><p><code>time_to_run</code>: duration of the test (default 60s)</p></li></ul>                                                                                                                            | PDF report with sysbench score                          | sysbench                                                |
| disk                | Benchmark             | Disk, distributed storage    | Hypervisor and VMs, all SEAPATH configuration          | <ul><li><p><code>time_to_run</code>: duration of the test (default 60s) </p></li><li><p><code>size</code>: size of data to be wrote (default 1M) </p></li></ul> By default, the test uses the time based option. | PDF report with fio score                               | fio                                                     |
| vm\_migration       | Benchmark             | CPU, disk                    | Hypervisor and VMs, only SEAPATH cluster configuration | <ul><li><p><code>resource</code>: name of the VM to migrate (default <code>guest0</code>) </p></li><li><p><code>iterations</code>: number of VM migration (default 5)</p></li></ul>                              | PDF report with average VM migration time               | A working SEAPATH cluster using crm as resource manager |
| rt\_tests           | Benchmark             | CPU, real time configuration | Hypervisor and VMs, all SEAPATH configuration          | <ul><li><p><code>time_to_run</code>: duration of the test (default 60s)</p></li><li><p><code>reference_test</code>: SEAPATH latency reference test<sup>1</sup></p></li></ul>                                     | PDF report with plot by cores of latencies              | Cyclictest <br/> gnuplot                                |
| process\_monitoring | Monitoring            | /                            | Hypervisor and VMs, all SEAPATH configuration          | `processes_to_monitor`: list of processes to monitor separated by a coma `,`. If not provided, only shows the three most CPU consumer processes                                                                  | PDF report with process CPU consumption per CPU core    |                                                         |
| network\_monitoring | Monitoring            | /                            | Hypervisor and VMs, all SEAPATH configuration          | `interface`: network interface to be monitored (default `team0`)                                                                                                                                                 | PDF report with average and max bandwidth for RX and TX | vnstat                                                  |

[^1]:: The test takes about 5 hours to complete.

Test-profiles are run in test scenarios. Each test scenario describes what tests have to be run, with which parameters, and which concurrency (parallel or sequential).

Test scenarios are formatted in YAML file format and are located in vars/test\_scenarios directory.

|                   |                                                                           |                                                                                                                         |
|:------------------|:--------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------|
| **Name**          | **Test scenario description**                                             | **Test profiles arguments**                                                                                             |
| disk\_cpu\_rttest | Disk, CPU and RT tests run simultaneously, process\_monitoring monitoring | Disk and CPU test profiles: 120s test                                                                                   |
| vmmigration       | 5 iterations of VM migration                                              | VM migration test profile: `5` iterations of `guest0` VM  `processes_to_monitor`: `crm` and `qemu-system-x86` processes |
| disk              | Disk test, with process\_monitoring and network\_monitoring monitoring    | `size`: `1G`                                                                                                            |
| idle              | Idle test with process\_monitoring monitoring                             | `time_to_run`: `1800`                                                                                                   |

## Installation

### Requirements

#### Localhost machine

Make sure Docker is installed on the localhost machine. See <https://docs.docker.com/engine/> to install it following the distribution you are using.

Normally, seapath-benchmark is designed to be run on localhost inside a Docker container. If you wish to run seapath-benchmark directly on the localhost machine, make sure it complies with the following dependencies:

```java
sudo apt install \
ansible \
bash
```

### Tested machines

Make sure the phoronix-test-suite package is installed on each tested machines:

1. Get the phoronix-test-suite at [phoronix-test-suite](https://github.com/phoronix-test-suite/phoronix-test-suite/archive/refs/heads/master.zip)
2. Unzip the archive
3. Run the file `install.sh`

For Debian based distribution:

```java
wget https://github.com/phoronix-test-suite/phoronix-test-suite/releases/download/v10.8.4/phoronix-test-suite_10.8.4_all.deb .
apt install ./phoronix-test-suite_10.8.4_all.deb
```

Then make sure following dependencies are satisfied on each tested machine:

```java
librsvg2-bin \
patch \
php-cli \
php-xml \
gnuplot
```

The user used by Ansible, targeted by inventory variable `ansible_user` variable must be configured on each machine to have sudo access.

## Usage

### Configuration

Each machine has to be configured for the Ansible access, as well as `monitored_machines` and `benchmarked_machines` groups. See `inventories/README` for more information. Configuration can then be started using:

```java
cqfd -b configure_test_profiles
```

or

```java
cqfd run ansible-playbook -i inventories/<YOUR INVENTORY> playbooks/configure_test_profiles.yaml
```

### Run tests

Using cqfd, seapath-benchmark can be launched using:

```java
cqfd -b run_test_profiles
```

or

```java
cqfd run ansible-playbook -i inventories/<YOUR INVENTORY> playbooks/run_test_profiles.yaml -e test_scenario_name=vmmigration
```

> [!NOTE]
> By default, `disk_cpu_rttest`is the default test scenario.

To choose the test scenario to be run use the Ansible argument `-e test_scenario_name=<TEST_SCENARIO_NAME>`

Each test-profiles arguments have default values, which can be overwritten in the test scenario.
