# Querying the kubelet's status on a node

You can review cluster node health status, resource consumption statistics, and node logs. Additionally, you can query `kubelet` status on individual nodes.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- Your API service is still functional.
- You have installed the OpenShift CLI (`oc`).

.Procedure

1. The kubelet is managed using a systemd service on each node. Review the kubelet's status by querying the `kubelet` systemd service within a debug pod.
.. Start a debug pod for a node:
```bash
$ oc debug node/my-node
```
> **NOTE:** If you are running `oc debug` on a control plane node, you can find administrative `kubeconfig` files in the `/etc/kubernetes/static-pod-resources/kube-apiserver-certs/secrets/node-kubeconfigs` directory.
.. Set `/host` as the root directory within the debug shell. The debug pod mounts the host's root file system in `/host` within the pod. By changing the root directory to `/host`, you can run binaries contained in the host's executable paths:
```bash
# chroot /host
```
> **NOTE:** OpenShift Container Platform 4.21 cluster nodes running Red Hat Enterprise Linux CoreOS (RHCOS) are immutable and rely on Operators to apply cluster changes. Accessing cluster nodes by using SSH is not recommended. However, if the OpenShift Container Platform API is not available, or `kubelet` is not properly functioning on the target node, `oc` operations will be impacted. In such situations, it is possible to access nodes using `ssh core@<node>.<cluster_name>.<base_domain>` instead.
.. Check whether the `kubelet` systemd service is active on the node:
```bash
# systemctl is-active kubelet
```
.. Output a more detailed `kubelet.service` status summary:
```bash
# systemctl status kubelet
```