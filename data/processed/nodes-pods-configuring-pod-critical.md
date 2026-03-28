# Preventing pod removal using critical pods

There are a number of core components that are critical to a fully functional cluster,
but, run on a regular cluster node rather than the master. A cluster might stop working properly if a critical add-on is evicted.

Pods marked as critical are not allowed to be evicted.

.Procedure

To make a pod critical:

1. Create a `Pod` spec or edit existing pods to include the `system-cluster-critical` priority class:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pdb
spec:
  template:
    metadata:
      name: critical-pod
    priorityClassName: system-cluster-critical <1>
# ...
```
<1> Default priority class for pods that should never be evicted from a node.
Alternatively, you can specify `system-node-critical` for pods that are important to the cluster
but can be removed if necessary.

1. Create the pod:
```bash
$ oc create -f <file-name>.yaml
```