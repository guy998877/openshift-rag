# Updating the virtual hardware for control plane nodes on vSphere

To reduce the risk of downtime, it is recommended that control plane nodes be updated serially. This ensures that the Kubernetes API remains available and etcd retains quorum.

.Prerequisites

- You have cluster administrator permissions to execute the required permissions in the vCenter instance hosting your OpenShift Container Platform cluster.
- Your vSphere ESXi hosts are version 8.0 Update 1 or later, or VWware vSphere Foundation 9, or VMware Cloud Foundation 9.

.Procedure

1. List the control plane nodes in your cluster.
```bash
$ oc get nodes -l node-role.kubernetes.io/master
```
.Example output
```bash
NAME                    STATUS   ROLES    AGE   VERSION
control-plane-node-0    Ready    master   75m   v1.34.2
control-plane-node-1    Ready    master   75m   v1.34.2
control-plane-node-2    Ready    master   75m   v1.34.2
```
Note the names of your control plane nodes.

1. Mark the control plane node as unschedulable.
```bash
$ oc adm cordon <control_plane_node>
```

1. Shut down the virtual machine (VM) associated with the control plane node. Do this in the vSphere client by right-clicking the VM and selecting *Power* -> *Shut Down Guest OS*. Do not shut down the VM using *Power Off* because it might not shut down safely.

1. Update the VM in the vSphere client. Follow link:https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-60768C2F-72E1-42E0-8A17-CA76849F2950.html[Upgrade the Compatibility of a Virtual Machine Manually] in the VMware documentation for more information.

1. Power on the VM associated with the control plane node. Do this in the vSphere client by right-clicking the VM and selecting *Power On*.

1. Wait for the node to report as `Ready`:
```bash
$ oc wait --for=condition=Ready node/<control_plane_node>
```

1. Mark the control plane node as schedulable again:
```bash
$ oc adm uncordon <control_plane_node>
```

1. Repeat this procedure for each control plane node in your cluster.