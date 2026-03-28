# Gathering CRI-O journald unit logs

If you experience CRI-O issues, you can obtain CRI-O journald unit logs from a node.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- Your API service is still functional.
- You have installed the OpenShift CLI (`oc`).
- You have the fully qualified domain names of the control plane or control plane machines.

.Procedure

1. Gather CRI-O journald unit logs. The following example collects logs from all control plane nodes (within the cluster:
```bash
$ oc adm node-logs --role=master -u crio
```

1. Gather CRI-O journald unit logs from a specific node:
```bash
$ oc adm node-logs <node_name> -u crio
```

1. If the API is not functional, review the logs using SSH instead. Replace `<node>.<cluster_name>.<base_domain>` with appropriate values:
```bash
$ ssh core@<node>.<cluster_name>.<base_domain> journalctl -b -f -u crio.service
```
> **NOTE:** OpenShift Container Platform 4.21 cluster nodes running Red Hat Enterprise Linux CoreOS (RHCOS) are immutable and rely on Operators to apply cluster changes. Accessing cluster nodes by using SSH is not recommended. Before attempting to collect diagnostic data over SSH, review whether the data collected by running `oc adm must gather` and other `oc` commands is sufficient instead. However, if the OpenShift Container Platform API is not available, or the kubelet is not properly functioning on the target node, `oc` operations will be impacted. In such situations, it is possible to access nodes using `ssh core@<node>.<cluster_name>.<base_domain>`.