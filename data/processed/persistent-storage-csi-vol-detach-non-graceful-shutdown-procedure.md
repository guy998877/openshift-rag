# Adding an out-of-service taint manually for automatic volume detachment

.Prerequisites

- Access to the cluster with cluster-admin privileges.

.Procedure

To allow volumes to detach automatically from a node after a non-graceful node shutdown:

1. After a node is detected as unhealthy, shut down the worker node.

1. Ensure that the node is shutdown by running the following command and checking the status:
```bash
$ oc get node <node_name> <1>
```
<1> <node_name> = name of the node that shut down non-gracefully
> **IMPORTANT:** If the node is not completely shut down, do not proceed with tainting the node. If the node is still up and the taint is applied, filesystem corruption can occur.
1. Taint the corresponding node object by running the following command:
> **IMPORTANT:** Tainting a node this way deletes all pods on that node. This also causes any pods that are backed by statefulsets to be evicted, and replacement pods to be created on a different node.
```bash
$ oc adm taint node <node_name> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute <1>
```
<1> <node_name> = name of the node that shut down non-gracefully
After the taint is applied, the volumes detach from the shutdown node allowing their disks to be attached to a different node.
.Example
The resulting YAML file resembles the following:
```yaml
spec:
  taints:
  - effect: NoExecute
    key: node.kubernetes.io/out-of-service
    value: nodeshutdown
```

1. Restart the node.

1. Remove the taint from the corresponding node object by running the following command:
```bash
$ oc adm taint node <node_name> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute- <1>
```
<1> <node_name> = name of the node that shut down non-gracefully