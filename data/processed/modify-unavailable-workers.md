# Modifying the number of unavailable worker nodes

By default, only one machine is allowed to be unavailable when applying the kubelet-related configuration to the available worker nodes. For a large cluster, it can take a long time for the configuration change to be reflected. At any time, you can adjust the number of machines that are updating to speed up the process.

.Procedure

1. Edit the `worker` machine config pool:
```bash
$ oc edit machineconfigpool worker
```

1. Add the `maxUnavailable` field and set the value:
```yaml
spec:
  maxUnavailable: <node_count>
```
> **IMPORTANT:** When setting the value, consider the number of worker nodes that can be unavailable without affecting the applications running on the cluster.