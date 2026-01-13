
[Tests and CI](../Tests%20and%20CI.md)

# SEAPATH Yocto Test Bench

This section presents the SEAPATH Yocto reference results produced on a reference hardware. These results are updated every week.

# Test protocol

Reference results are produced using [SEAPATH benchmark](SEAPATH%20toolbox/SEAPATH%20benchmark.md) tool. The test consists of a sequential run of different test scenarios, testing different SEAPATH components, in various test condition. It is run with weekly CI GitHub action, every Saturday at 10:30PM.

## Reference hardware

|  CPU    |  Intel® Xeon W-11865MLE 8 Cores                      |
|:--------|:-----------------------------------------------------|
| Memory  | 64Gb 3200MHz DDR4                                    |
| Disk    | 2xSATA SSD 500Gb                                     |
| Network | Intel® Ethernet Controller I226-IT 1000Mbit Ethernet |

## Reference software

The hypervisor machine is running a SEAPATH Yocto host distribution. The VM used in running a SEAPATH Yocto guest distribution. SEAPATH Ansible main branch is used to configure each machine.

> [!NOTE]
> Each repository used are checkout on the latest commit merged.

### Test scenarios

#### Real time reference benchmark

This test scenario purpose is to measure the real time performance in a SEAPATH VM, hosted by a SEAPATH hypervisor. It use [cyclictest](https://wiki.linuxfoundation.org/realtime/documentation/howto/tools/cyclictest/start) package to perform this test using following arguments:

```java
cyclictest -l100000000 -m -Sp90 -i200 -h400 -q
```

### Test report results

|  **Test scenario**            |  **Machine**                                             |  **Reports**                                                                                                                                                                                                  |  **Notes**                                                                                                          |
|:------------------------------|:---------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|
| Real time reference benchmark | SEAPATH Yocto VM running on WELOTEC RSAPC Mk2 hypervisor | [VM1 report](https://drive.google.com/file/d/1gWov-l8BcVLjmamW4gS1YNvJFBQCDKNS/view?usp=drive_link) <br/> [VM2 report](https://drive.google.com/file/d/1YuD0S7UZoswGXEqETloaaVd8qJB0kdkS/view?usp=drive_link) | <ul><li><p>VM1 is configured with RT isolation</p></li><li><p>VM2 is not configured with RT isolation</p></li></ul> |
