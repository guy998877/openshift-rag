# Investigating control plane node kubelet and API server issues

To investigate control plane node kubelet and API server issues during installation, check DNS, DHCP, and load balancer functionality. Also, verify that certificates have not expired.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).
- You have SSH access to your hosts.
- You have the fully qualified domain names of the control plane nodes.

.Procedure

1. Verify that the API server's DNS record directs the kubelet on control plane nodes to [x-]`https://api-int.<cluster_name>.<base_domain>:6443`. Ensure that the record references the load balancer.

1. Ensure that the load balancer's port 6443 definition references each control plane node.

1. Check that unique control plane node hostnames have been provided by DHCP.

1. Inspect the `kubelet.service` journald unit logs on each control plane node.
.. Retrieve the logs using `oc`:
```bash
$ oc adm node-logs --role=master -u kubelet
```
.. If the API is not functional, review the logs using SSH instead. Replace `<master-node>.<cluster_name>.<base_domain>` with appropriate values:
```bash
$ ssh core@<master-node>.<cluster_name>.<base_domain> journalctl -b -f -u kubelet.service
```
> **NOTE:** OpenShift Container Platform 4.21 cluster nodes running Red Hat Enterprise Linux CoreOS (RHCOS) are immutable and rely on Operators to apply cluster changes. Accessing cluster nodes by using SSH is not recommended. Before attempting to collect diagnostic data over SSH, review whether the data collected by running `oc adm must gather` and other `oc` commands is sufficient instead. However, if the OpenShift Container Platform API is not available, or the kubelet is not properly functioning on the target node, `oc` operations will be impacted. In such situations, it is possible to access nodes using `ssh core@<node>.<cluster_name>.<base_domain>`.
1. Check for certificate expiration messages in the control plane node kubelet logs.
.. Retrieve the log using `oc`:
```bash
$ oc adm node-logs --role=master -u kubelet | grep -is 'x509: certificate has expired'
```
.. If the API is not functional, review the logs using SSH instead. Replace `<master-node>.<cluster_name>.<base_domain>` with appropriate values:
```bash
$ ssh core@<master-node>.<cluster_name>.<base_domain> journalctl -b -f -u kubelet.service  | grep -is 'x509: certificate has expired'
```