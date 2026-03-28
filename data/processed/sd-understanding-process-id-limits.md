# Understanding process ID limits

You can review the following information to learn how to limit the number of processes running on your nodes. Configuring an appropriate number of processes can help keep the nodes in your cluster running efficiently. 

In OpenShift Container Platform, consider these two supported limits for process ID (PID) usage before you schedule work on your cluster:

- Maximum number of PIDs per pod.
The default value is 4,096 in OpenShift Container Platform 4.11 and later. This value is controlled by the `podPidsLimit` parameter set on the node.

When a pod exceeds the allowed maximum number of PIDs per pod, the pod might stop functioning correctly and might be evicted from the node. See [the Kubernetes documentation for eviction signals and thresholds](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/#eviction-signals-and-thresholds) for more information.

When a node exceeds the allowed maximum number of PIDs per node, the node can become unstable because new processes cannot have PIDs assigned. If existing processes cannot complete without creating additional processes, the entire node can become unusable and require reboot. This situation can result in data loss, depending on the processes and applications being run. Customer administrators and Red Hat Site Reliability Engineering are notified when this threshold is reached, and a `Worker node is experiencing PIDPressure` warning will appear in the cluster logs.