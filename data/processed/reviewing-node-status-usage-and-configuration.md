# Reviewing node status, resource usage, and configuration

Review cluster node health status, resource consumption statistics, and node logs. Additionally, query `kubelet` status on individual nodes.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).

.Procedure

- List the name, status, and role for all nodes in the cluster:
```bash
$ oc get nodes
```

- Summarize CPU and memory usage for each node within the cluster:
```bash
$ oc adm top nodes
```

- Summarize CPU and memory usage for a specific node:
```bash
$ oc adm top node my-node
```