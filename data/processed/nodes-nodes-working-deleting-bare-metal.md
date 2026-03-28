# Deleting nodes from a bare metal cluster

You can delete a node from a OpenShift Container Platform cluster that does not use machine sets by using the `oc delete node` command and decommissioning the node.

When you delete a node using the CLI, the node object is deleted in Kubernetes,
but the pods that exist on the node are not deleted. Any bare pods not backed by
a replication controller become inaccessible to OpenShift Container Platform. Pods backed by
replication controllers are rescheduled to other available nodes. You must
delete local manifest pods.

The following procedure deletes a node from an OpenShift Container Platform cluster running on bare metal.

.Procedure

1. Mark the node as unschedulable:
```bash
$ oc adm cordon <node_name>
```

1. Drain all pods on the node:
```bash
$ oc adm drain <node_name> --force=true
```
This step might fail if the node is offline or unresponsive. Even if the node does not respond, the node might still be running a workload that writes to shared storage. To avoid data corruption, power down the physical hardware before you proceed.

1. Delete the node from the cluster:
```bash
$ oc delete node <node_name>
```
Although the node object is now deleted from the cluster, it can still rejoin
the cluster after reboot or if the kubelet service is restarted. To permanently
delete the node and all its data, you must
[decommission the node](https://access.redhat.com/solutions/84663).

1. If you powered down the physical hardware, turn it back on so that the node can rejoin the cluster.