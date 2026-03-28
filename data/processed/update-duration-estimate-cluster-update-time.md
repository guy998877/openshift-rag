# How to estimate cluster update time

Historical update duration of similar clusters provides you the best estimate for the future cluster updates. If you do not have historical data, you can calculate an estimate of the update duration.

You can use the following convention to estimate your cluster update time:

```text
Cluster update time = CVO target update payload deployment time + (# node update iterations x MCO node update time)
```

A node update iteration consists of one or more nodes updated in parallel. The control plane nodes are always updated in parallel with the compute nodes. In addition, one or more compute nodes can be updated in parallel based on the `maxUnavailable` value.

> **WARNING:** The default setting for `maxUnavailable` is `1` for all the machine config pools in OpenShift Container Platform. It is recommended to not change this value and update one control plane node at a time. Do not change this value to `3` for the control plane pool.

For example, to estimate the update time, consider an OpenShift Container Platform cluster with three control plane nodes and six compute nodes, where each host takes about 5 minutes to reboot.

> **NOTE:** The time it takes to reboot a particular node varies significantly. In cloud instances, the reboot might take about 1 to 2 minutes, whereas in physical bare metal hosts the reboot might take more than 15 minutes.

In a scenario where you set `maxUnavailable` to `1` for both the control plane and compute nodes Machine Config Pool (MCP), then all the six compute nodes will update one after another in each iteration:

```text
Cluster update time = 60 + (6 x 5) = 90 minutes
```

In a scenario where you set `maxUnavailable` to `2` for the compute node MCP, then two compute nodes will update in parallel in each iteration. Therefore it takes total three iterations to update all the nodes.

```text
Cluster update time = 60 + (3 x 5) = 75 minutes
```

> **IMPORTANT:** The default setting for `maxUnavailable` is `1` for all the MCPs in OpenShift Container Platform. It is recommended that you do not change the `maxUnavailable` in the control plane MCP.