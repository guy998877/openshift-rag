# Verifying access to OpenShift Container Platform web console for OpenShift Container Platform cluster in ready state

OpenShift Container Platform clusters return a `ready` status when the control plane hosted in the OpenShift Container Platform service account becomes ready. Cluster console workloads are deployed on the cluster's worker nodes. The OpenShift Container Platform web console will not be available and accessible until the worker nodes have joined the cluster and console workloads are running.

.Procedure

- If your OpenShift Container Platform cluster is ready but you are unable to access the OpenShift Container Platform web console for the cluster, wait for the worker nodes to join the cluster and retry accessing the console.
You can either log in to the OpenShift Container Platform cluster or use the `rosa describe machinepool` command in the `rosa` CLI watch the nodes.