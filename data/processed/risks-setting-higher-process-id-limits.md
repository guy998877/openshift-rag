# Risks of setting higher process ID limits for OpenShift Container Platform pods

You can review the following information to learn about some considerations about allowing a high maximum number of processes to run on your nodes. Configuring an appropriate number of processes can help keep the nodes in your cluster running efficiently. 

You can increase the value for `podPidsLimit` from the default of 4,096 to a maximum of 16,384. Changing this value might incur downtime for applications, because changing the `podPidsLimit` requires rebooting the affected node.

If you are running a large number of pods per node, and you have a high `podPidsLimit` value on your nodes, you risk exceeding the PID maximum for the node.

To find the maximum number of pods that you can run simultaneously on a single node without exceeding the PID maximum for the node, divide 3,650,000 by your `podPidsLimit` value. For example, if your `podPidsLimit` value is 16,384, and you expect the pods to use close to that number of process IDs, you can safely run 222 pods on a single node.