# Querying cluster node journal logs

You can gather `journald` unit logs and other logs within `/var/log` on individual cluster nodes.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).
- Your API service is still functional.
- You have SSH access to your hosts.

.Procedure

1. Query `kubelet` `journald` unit logs from OpenShift Container Platform cluster nodes. The following example queries control plane nodes only:
```bash
$ oc adm node-logs --role=master -u kubelet  <1>
```
`kubelet`:: Replace as appropriate to query other unit logs.

1. Collect logs from specific subdirectories under `/var/log/` on cluster nodes.
.. Retrieve a list of logs contained within a `/var/log/` subdirectory. The following example lists files in `/var/log/openshift-apiserver/` on all control plane nodes:
```bash
$ oc adm node-logs --role=master --path=openshift-apiserver
```
.. Inspect a specific log within a `/var/log/` subdirectory. The following example outputs `/var/log/openshift-apiserver/audit.log` contents from all control plane nodes:
```bash
$ oc adm node-logs --role=master --path=openshift-apiserver/audit.log
```
.. If the API is not functional, review the logs on each node using SSH instead. The following example tails `/var/log/openshift-apiserver/audit.log`:
```bash
$ ssh core@<master-node>.<cluster_name>.<base_domain> sudo tail -f /var/log/openshift-apiserver/audit.log
```
> **NOTE:** OpenShift Container Platform 4.21 cluster nodes running Red Hat Enterprise Linux CoreOS (RHCOS) are immutable and rely on Operators to apply cluster changes. Accessing cluster nodes by using SSH is not recommended. Before attempting to collect diagnostic data over SSH, review whether the data collected by running `oc adm must gather` and other `oc` commands is sufficient instead. However, if the OpenShift Container Platform API is not available, or the kubelet is not properly functioning on the target node, `oc` operations will be impacted. In such situations, it is possible to access nodes using `ssh core@<node>.<cluster_name>.<base_domain>`.