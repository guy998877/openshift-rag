# Cleaning CRI-O storage

You can manually clear the CRI-O ephemeral storage if you experience the following issues:

- A node cannot run any pods and this error appears:
```bash
+
```
Failed to create pod sandbox: rpc error: code = Unknown desc = failed to mount container XXX: error recreating the missing symlinks: error reading name of symlink for XXX: open /var/lib/containers/storage/overlay/XXX/link: no such file or directory
- You cannot create a new container on a working node and the  “can’t stat lower layer” error appears:
```bash
+
```
can't stat lower layer ...  because it does not exist.  Going through storage to recreate the missing symlinks.
- Your node is in the `NotReady` state after a cluster upgrade or if you attempt to reboot it.

- The container runtime implementation (`crio`) is not working properly.

- You are unable to start a debug shell on the node using `oc debug node/<node_name>` because the container runtime instance (`crio`) is not working.

Follow this process to completely wipe the CRI-O storage and resolve the errors.

.Prerequisites

  * You have access to the cluster as a user with the `cluster-admin` role.
  * You have installed the OpenShift CLI (`oc`).

.Procedure

1. Use `cordon` on the node. This is to avoid any workload getting scheduled if the node gets into the `Ready` status. You will know that scheduling is disabled when `SchedulingDisabled` is in your Status section:
```bash
+
```
$ oc adm cordon <node_name>
1. Drain the node as the cluster-admin user:
```bash
+
```
$ oc adm drain <node_name> --ignore-daemonsets --delete-emptydir-data
> **NOTE:** The `terminationGracePeriodSeconds` attribute of a pod or pod template controls the graceful termination period. This attribute defaults at 30 seconds, but can be customized for each application as necessary. If set to more than 90 seconds, the pod might be marked as `SIGKILLed` and fail to terminate successfully.

1. When the node returns, connect back to the node via SSH or Console. Then connect to the root user:
```bash
+
```
$ ssh core@node1.example.com
$ sudo -i
1. Manually stop the kubelet:
```bash
+
```
# systemctl stop kubelet
1. Stop the containers and pods:

.. Use the following command to stop the pods that are not in the `HostNetwork`. They must be removed first because their removal relies on the networking plugin pods, which are in the `HostNetwork`.
```bash
+
```
.. for pod in $(crictl pods -q); do if [[ "$(crictl inspectp $pod | jq -r .status.linux.namespaces.options.network)" != "NODE" ]]; then crictl rmp -f $pod; fi; done

.. Stop all other pods:
```bash
+
```
# crictl rmp -fa
1. Manually stop the crio services:
```bash
+
```
# systemctl stop crio
1. After you run those commands, you can completely wipe the ephemeral storage:
```bash
+
```
# crio wipe -f
1. Start the crio and kubelet service:
```bash
+
```
# systemctl start crio
# systemctl start kubelet
1. You will know if the clean up worked if the crio and kubelet services are started, and the node is in the `Ready` status:
```bash
+
```
$ oc get nodes
.Example output
```bash
+
```
NAME				    STATUS	                ROLES    AGE    VERSION
ci-ln-tkbxyft-f76d1-nvwhr-master-1  Ready, SchedulingDisabled   master	 133m   v1.34.2
1. Mark the node schedulable. You will know that the scheduling is enabled when `SchedulingDisabled` is no longer in status:
```bash
+
```
$ oc adm uncordon <node_name>
.Example output
```bash
+
```
NAME				     STATUS	      ROLES    AGE    VERSION
ci-ln-tkbxyft-f76d1-nvwhr-master-1   Ready            master   133m   v1.34.2