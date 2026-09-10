
[SEAPATH fundamentals](../../../SEAPATH%20fundamentals.md) > [Supervision](../../Supervision.md) > [SNMP](../SNMP.md)

# Example of SNMP output

Some SNMP outputs are complex. This page provides examples of outputs:

## Example of Ceph pgmap (.1.7)

```java
{
  "pgs_by_state":[
    {
      "state_name":"active+clean",
      "count":123
    },
    {
      "state_name":"active+recovery_unfound+degraded",
      "count":6
    }
  ],
  "num_pgs":129,
  "num_pools":2,
  "num_objects":1899,
  "data_bytes":7247356075,
  "bytes_used":15049560064,
  "bytes_avail":239687299072,
  "bytes_total":254736859136,
  "degraded_objects":14,
  "degraded_total":3798,
  "degraded_ratio":0.003686150605581885,
  "unfound_objects":7,
  "unfound_total":1899,
  "unfound_ratio":0.003686150605581885,
  "write_bytes_sec":171956,
  "read_op_per_sec":0,
  "write_op_per_sec":27
}
```

## Example of smartctl --attributes (.1.9)

```text
SMART Status not supported: ATA return descriptor not supported by controller firmware
SMART overall-health self-assessment test result: PASSED
Warning: This result is based on an Attribute check.

General SMART Values:
Offline data collection status:  (0x00) Offline data collection activity
                                        was never started.
                                        Auto Offline Data Collection: Disabled.
Self-test execution status:      (   0) The previous self-test routine completed
                                        without error or no self-test has ever 
                                        been run.
Total time to complete Offline 
data collection:                (    1) seconds.
Offline data collection
capabilities:                    (0x59) SMART execute Offline immediate.
                                        No Auto Offline data collection support.
                                        Suspend Offline collection upon new
                                        command.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        No Conveyance Self-test supported.
                                        Selective Self-test supported.
SMART capabilities:            (0x0002) Does not save SMART data before
                                        entering power-saving mode.
                                        Supports SMART auto save timer.
Error logging capability:        (0x01) Error logging supported.
                                        General Purpose Logging supported.
Short self-test routine 
recommended polling time:        (   1) minutes.
Extended self-test routine
recommended polling time:        (   2) minutes.

SMART Attributes Data Structure revision number: 10
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x002f   100   100   050    Pre-fail  Always       -       0
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  9 Power_On_Hours          0x0032   100   100   000    Old_age   Always       -       3176
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       154
161 Unknown_Attribute       0x0032   100   100   050    Old_age   Always       -       0
162 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       48939
163 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       3000
164 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       94
166 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       9
167 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
168 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
169 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       97
171 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
172 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       0
174 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       51
175 Program_Fail_Count_Chip 0x0032   100   100   000    Old_age   Always       -       0
181 Program_Fail_Cnt_Total  0x0022   100   100   000    Old_age   Always       -       231401
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
194 Temperature_Celsius     0x0022   100   100   000    Old_age   Always       -       40
195 Hardware_ECC_Recovered  0x003a   100   100   000    Old_age   Always       -       0
196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
199 UDMA_CRC_Error_Count    0x0032   100   100   000    Old_age   Always       -       0
206 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       41
207 Unknown_SSD_Attribute   0x0032   100   100   000    Old_age   Always       -       247
232 Available_Reservd_Space 0x0032   100   100   000    Old_age   Always       -       100
241 Total_LBAs_Written      0x0032   100   100   000    Old_age   Always       -       3776
242 Total_LBAs_Read         0x0032   100   100   000    Old_age   Always       -       547
249 Unknown_Attribute       0x0032   100   100   000    Old_age   Always       -       8779
250 Read_Error_Retry_Rate   0x0032   100   100   000    Old_age   Always       -       3816

SMART Error Log Version: 1
No Errors Logged

SMART Self-test log structure revision number 1
No self-tests have been logged.  [To run self-tests, use: smartctl -t]

SMART Selective self-test log data structure revision number 0
Note: revision number not 1 implies that no selective self-test has ever been run
 SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS
    1        0        0  Not_testing
    2        0        0  Not_testing
    3        0        0  Not_testing
    4        0        0  Not_testing
    5        0        0  Not_testing
Selective self-test flags (0x0):
  After scanning selected spans, do NOT read-scan remainder of disk.
If Selective self-test is pending on power-up, resume after 0 minute delay.
```

## Example of crm status .1.11

```java
{
  "crm_mon": {
    "version": "2.1.5",
    "pacemakerd": {
      "sys_from": "pacemakerd",
      "state": "running",
      "last_updated": "2025-12-01 11:48:03 +01:00"
    },
    "summary": {
      "stack": {
        "type": "corosync"
      },
      "current_dc": {
        "present": "true",
        "version": "2.1.5-a3f44794f94",
        "name": "node1",
        "id": "1",
        "with_quorum": "true",
        "mixed_version": "false"
      },
      "last_update": {
        "time": "Mon Dec  1 11:48:04 2025"
      },
      "last_change": {
        "time": "Mon Dec  1 10:43:04 2025",
        "user": "root",
        "client": "crm_resource",
        "origin": "node3"
      },
      "nodes_configured": {
        "number": "3"
      },
      "resources_configured": {
        "number": "10",
        "disabled": "0",
        "blocked": "0"
      },
      "cluster_options": {
        "stonith-enabled": "false",
        "symmetric-cluster": "true",
        "no-quorum-policy": "stop",
        "maintenance-mode": "false",
        "stop-all-resources": "false",
        "stonith-timeout-ms": "60000",
        "priority-fencing-delay-ms": "0"
      }
    },
    "nodes": {
      "node": [
        {
          "name": "node1",
          "id": "1",
          "online": "true",
          "standby": "false",
          "standby_onfail": "false",
          "maintenance": "false",
          "pending": "false",
          "unclean": "false",
          "health": "green",
          "feature_set": "3.16.1",
          "shutdown": "false",
          "expected_up": "true",
          "is_dc": "true",
          "resources_running": "4",
          "type": "member"
        },
        {
          "name": "node2",
          "id": "2",
          "online": "true",
          "standby": "false",
          "standby_onfail": "false",
          "maintenance": "false",
          "pending": "false",
          "unclean": "false",
          "health": "green",
          "feature_set": "3.16.1",
          "shutdown": "false",
          "expected_up": "true",
          "is_dc": "false",
          "resources_running": "3",
          "type": "member"
        },
        {
          "name": "node3",
          "id": "3",
          "online": "true",
          "standby": "false",
          "standby_onfail": "false",
          "maintenance": "false",
          "pending": "false",
          "unclean": "false",
          "health": "green",
          "feature_set": "3.16.1",
          "shutdown": "false",
          "expected_up": "true",
          "is_dc": "false",
          "resources_running": "3",
          "type": "member"
        }
      ]
    },
    "resources": {
      "clone": [
        {
          "id": "cl_ntpstatus_test",
          "multi_state": "false",
          "unique": "false",
          "managed": "true",
          "disabled": "false",
          "failed": "false",
          "failure_ignored": "false",
          "target_role": "Started",
          "resource": [
            {
              "id": "ntpstatus_test",
              "resource_agent": "ocf:seapath:ntpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node2",
                "id": "2",
                "cached": "true"
              }
            },
            {
              "id": "ntpstatus_test",
              "resource_agent": "ocf:seapath:ntpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node1",
                "id": "1",
                "cached": "true"
              }
            },
            {
              "id": "ntpstatus_test",
              "resource_agent": "ocf:seapath:ntpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node3",
                "id": "3",
                "cached": "true"
              }
            }
          ]
        },
        {
          "id": "cl_ptpstatus_test",
          "multi_state": "false",
          "unique": "false",
          "managed": "true",
          "disabled": "false",
          "failed": "false",
          "failure_ignored": "false",
          "target_role": "Started",
          "resource": [
            {
              "id": "ptpstatus_test",
              "resource_agent": "ocf:seapath:ptpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node2",
                "id": "2",
                "cached": "true"
              }
            },
            {
              "id": "ptpstatus_test",
              "resource_agent": "ocf:seapath:ptpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node1",
                "id": "1",
                "cached": "true"
              }
            },
            {
              "id": "ptpstatus_test",
              "resource_agent": "ocf:seapath:ptpstatus",
              "role": "Started",
              "target_role": "Started",
              "active": "true",
              "orphaned": "false",
              "blocked": "false",
              "managed": "true",
              "failed": "false",
              "failure_ignored": "false",
              "nodes_running_on": "1",
              "node": {
                "name": "node3",
                "id": "3",
                "cached": "true"
              }
            }
          ]
        }
      ],
      "resource": [
        {
          "id": "ClusterIP",
          "resource_agent": "ocf:heartbeat:IPaddr2",
          "role": "Started",
          "target_role": "Started",
          "active": "true",
          "orphaned": "false",
          "blocked": "false",
          "managed": "true",
          "failed": "false",
          "failure_ignored": "false",
          "nodes_running_on": "1",
          "node": {
            "name": "node1",
            "id": "1",
            "cached": "true"
          }
        },
        {
          "id": "vmmgrapi",
          "resource_agent": "systemd:nginx.service",
          "role": "Started",
          "active": "true",
          "orphaned": "false",
          "blocked": "false",
          "managed": "true",
          "failed": "false",
          "failure_ignored": "false",
          "nodes_running_on": "1",
          "node": {
            "name": "node1",
            "id": "1",
            "cached": "true"
          }
        },
        {
          "id": "vmtest12",
          "resource_agent": "ocf:seapath:VirtualDomain",
          "role": "Started",
          "target_role": "Started",
          "active": "true",
          "orphaned": "false",
          "blocked": "false",
          "managed": "true",
          "failed": "false",
          "failure_ignored": "false",
          "nodes_running_on": "1",
          "node": {
            "name": "node2",
            "id": "2",
            "cached": "true"
          }
        },
        {
          "id": "vmtest12rt",
          "resource_agent": "ocf:seapath:VirtualDomain",
          "role": "Started",
          "target_role": "Started",
          "active": "true",
          "orphaned": "false",
          "blocked": "false",
          "managed": "true",
          "failed": "false",
          "failure_ignored": "false",
          "nodes_running_on": "1",
          "node": {
            "name": "node3",
            "id": "3",
            "cached": "true"
          }
        }
      ]
    },
    "node_attributes": {
      "node": [
        {
          "name": "node1",
          "attribute": [
            {
              "name": "ntpstatus",
              "value": "0"
            },
            {
              "name": "ptpstatus",
              "value": "0"
            }
          ]
        },
        {
          "name": "node2",
          "attribute": [
            {
              "name": "ntpstatus",
              "value": "0"
            },
            {
              "name": "ptpstatus",
              "value": "0"
            }
          ]
        },
        {
          "name": "node3",
          "attribute": [
            {
              "name": "ntpstatus",
              "value": "0"
            },
            {
              "name": "ptpstatus",
              "value": "0"
            }
          ]
        }
      ]
    },
    "node_history": {
      "node": [
        {
          "name": "node2",
          "resource_history": [
            {
              "id": "ptpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "20",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "208ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "22",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:51 2025",
                  "exec-time": "28ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "ntpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "21",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "182ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "23",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:51 2025",
                  "exec-time": "59ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "vmtest12",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "41",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:38:58 2025",
                  "exec-time": "4024ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "42",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:39:02 2025",
                  "exec-time": "228ms",
                  "queue-time": "0ms"
                }
              ]
            }
          ]
        },
        {
          "name": "node1",
          "resource_history": [
            {
              "id": "vmmgrapi",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "26",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:53 2025",
                  "exec-time": "2352ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "27",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "30000ms",
                  "last-rc-change": "Mon Dec  1 10:31:53 2025",
                  "exec-time": "0ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "ptpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "20",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "68ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "23",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "39ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "ntpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "21",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "62ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "22",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "50ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "ClusterIP",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "24",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "87ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "25",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "30000ms",
                  "last-rc-change": "Mon Dec  1 10:31:51 2025",
                  "exec-time": "166ms",
                  "queue-time": "0ms"
                }
              ]
            }
          ]
        },
        {
          "name": "node3",
          "resource_history": [
            {
              "id": "ptpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "20",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "49ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "22",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "28ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "ntpstatus_test",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "21",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "64ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "23",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:31:50 2025",
                  "exec-time": "55ms",
                  "queue-time": "0ms"
                }
              ]
            },
            {
              "id": "vmtest12rt",
              "orphan": "false",
              "migration-threshold": "1000000",
              "operation_history": [
                {
                  "call": "37",
                  "task": "start",
                  "rc": "0",
                  "rc_text": "ok",
                  "last-rc-change": "Mon Dec  1 10:42:58 2025",
                  "exec-time": "6187ms",
                  "queue-time": "0ms"
                },
                {
                  "call": "38",
                  "task": "monitor",
                  "rc": "0",
                  "rc_text": "ok",
                  "interval": "10000ms",
                  "last-rc-change": "Mon Dec  1 10:43:04 2025",
                  "exec-time": "192ms",
                  "queue-time": "0ms"
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

## Example of CRM Summary (.1.11.0.1)

```java
{
  "stack": {
    "type": "corosync"
  },
  "current_dc": {
    "present": "true",
    "version": "2.1.5-a3f44794f94",
    "name": "node1",
    "id": "1",
    "with_quorum": "true",
    "mixed_version": "false"
  },
  "last_update": {
    "time": "Mon Dec  1 11:06:15 2025"
  },
  "last_change": {
    "time": "Mon Dec  1 10:43:04 2025",
    "user": "root",
    "client": "crm_resource",
    "origin": "node3"
  },
  "nodes_configured": {
    "number": "3"
  },
  "resources_configured": {
    "number": "10",
    "disabled": "0",
    "blocked": "0"
  },
  "cluster_options": {
    "stonith-enabled": "false",
    "symmetric-cluster": "true",
    "no-quorum-policy": "stop",
    "maintenance-mode": "false",
    "stop-all-resources": "false",
    "stonith-timeout-ms": "60000",
    "priority-fencing-delay-ms": "0"
  }
}
```

## Example of Nodes Status (.1.11.0.2)

```java
{
  "node": [
    {
      "name": "node1",
      "id": "1",
      "online": "true",
      "standby": "false",
      "standby_onfail": "false",
      "maintenance": "false",
      "pending": "false",
      "unclean": "false",
      "health": "green",
      "feature_set": "3.16.1",
      "shutdown": "false",
      "expected_up": "true",
      "is_dc": "true",
      "resources_running": "4",
      "type": "member"
    },
    {
      "name": "node2",
      "id": "2",
      "online": "true",
      "standby": "false",
      "standby_onfail": "false",
      "maintenance": "false",
      "pending": "false",
      "unclean": "false",
      "health": "green",
      "feature_set": "3.16.1",
      "shutdown": "false",
      "expected_up": "true",
      "is_dc": "false",
      "resources_running": "3",
      "type": "member"
    },
    {
      "name": "node3",
      "id": "3",
      "online": "true",
      "standby": "false",
      "standby_onfail": "false",
      "maintenance": "false",
      "pending": "false",
      "unclean": "false",
      "health": "green",
      "feature_set": "3.16.1",
      "shutdown": "false",
      "expected_up": "true",
      "is_dc": "false",
      "resources_running": "3",
      "type": "member"
    }
  ]
}
```

## Example of LVM Full Report (.2.5.x)

```java
 {
    "lv_name": "root",
    "vg_name": "vg1",
    "lv_attr": "-wi-ao----",
    "lv_size": "8.00g",
    "pool_lv": "",
    "origin": "",
    "data_percent": "",
    "metadata_percent": "",
    "move_pv": "",
    "mirror_log": "",
    "copy_percent": "",
    "convert_lv": "",
    "devices": "/dev/vda2(0)",
    "lv_health_status": ""
  }
```

## Example of lvs full status (.2.6)

```java
{
  "report":[
    {
      "lv":[
        {
          "lv_name":"osd-block-70b51fa6-a6b6-4e23-a726-952a7f3320dd",
          "vg_name":"ceph-27a4d1bc-8ae5-45fd-b416-6ae9600268d4",
          "lv_attr":"-wi-a-----",
          "lv_size":"118.62g",
          "pool_lv":"",
          "origin":"",
          "data_percent":"",
          "metadata_percent":"",
          "move_pv":"",
          "mirror_log":"",
          "copy_percent":"",
          "convert_lv":"",
          "devices":"/dev/sdb(0)",
          "lv_health_status":""
        },
        {
          "lv_name":"root",
          "vg_name":"vg1",
          "lv_attr":"owi-aos---",
          "lv_size":"15.00g",
          "pool_lv":"",
          "origin":"",
          "data_percent":"",
          "metadata_percent":"",
          "move_pv":"",
          "mirror_log":"",
          "copy_percent":"",
          "convert_lv":"",
          "devices":"/dev/sda2(0)",
          "lv_health_status":""
        },
        {
          "lv_name":"root_snap",
          "vg_name":"vg1",
          "lv_attr":"swi-a-s---",
          "lv_size":"15.00g",
          "pool_lv":"",
          "origin":"root",
          "data_percent":"74.24",
          "metadata_percent":"",
          "move_pv":"",
          "mirror_log":"",
          "copy_percent":"",
          "convert_lv":"",
          "devices":"/dev/sda2(5245)",
          "lv_health_status":""
        },
        {
          "lv_name":"swap",
          "vg_name":"vg1",
          "lv_attr":"-wi-ao----",
          "lv_size":"500.00m",
          "pool_lv":"",
          "origin":"",
          "data_percent":"",
          "metadata_percent":"",
          "move_pv":"",
          "mirror_log":"",
          "copy_percent":"",
          "convert_lv":"",
          "devices":"/dev/sda2(5120)",
          "lv_health_status":""
        },
        {
          "lv_name":"varlog",
          "vg_name":"vg1",
          "lv_attr":"-wi-ao----",
          "lv_size":"5.00g",
          "pool_lv":"",
          "origin":"",
          "data_percent":"",
          "metadata_percent":"",
          "move_pv":"",
          "mirror_log":"",
          "copy_percent":"",
          "convert_lv":"",
          "devices":"/dev/sda2(3840)",
          "lv_health_status":""
        }
      ]
    }
  ]
}
```

## Example of lvs basic status (.2.7)

```java
{
  "report":[
    {
      "lv":[
        {
          "lv_name":"osd-block-70b51fa6-a6b6-4e23-a726-952a7f3320dd",
          "lv_health_status":""
        },
        {
          "lv_name":"root",
          "lv_health_status":""
        },
        {
          "lv_name":"root_snap",
          "lv_health_status":""
        },
        {
          "lv_name":"swap",
          "lv_health_status":""
        },
        {
          "lv_name":"varlog",
          "lv_health_status":""
        }
      ]
    }
  ]
}
```
