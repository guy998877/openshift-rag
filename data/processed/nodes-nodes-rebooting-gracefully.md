# Rebooting a node gracefully

You can perform a graceful restart of a node, where all workloads are moved to other nodes, without data loss or service disruption. 

Before rebooting a node, it is recommended to backup etcd data to avoid any data loss on the node.

> **NOTE:** For single-node OpenShift clusters that require users to perform the `oc login` command rather than having the certificates in `kubeconfig` file to manage the cluster, the `oc adm` commands might not be available after cordoning and draining the node. This is because the `openshift-oauth-apiserver` pod is not running due to the cordon. You can use SSH to access the nodes as indicated in the following procedure. In a single-node OpenShift cluster, pods cannot be rescheduled when cordoning and draining. However, doing so gives the pods, especially your workload pods, time to properly stop and release associated resources.

The following procedure demonstrates how to perform a graceful restart of a node.

.Procedure

1. Mark the node as unschedulable:
```bash
$ oc adm cordon <node1>
```

1. Drain the node to remove all the running pods:
```bash
$ oc adm drain <node1> --ignore-daemonsets --delete-emptydir-data --force
```
You might receive errors that pods associated with custom pod disruption budgets (PDB) cannot be evicted.
.Example error
```bash
error when evicting pods/"rails-postgresql-example-1-72v2w" -n "rails" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.
```
In this case, run the drain command again, adding the `disable-eviction` flag, which bypasses the PDB checks:
```bash
$ oc adm drain <node1> --ignore-daemonsets --delete-emptydir-data --force --disable-eviction
```

1. After the reboot is complete, mark the node as schedulable by running the following command:
```bash
$ oc adm uncordon <node1>
```

1. Verify that the node is ready:
```bash
$ oc get node <node1>
```
.Example output
```bash
NAME    STATUS  ROLES    AGE     VERSION
<node1> Ready   worker   6d22h   v1.18.3+b0068a8
```