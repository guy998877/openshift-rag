# Updating the virtual hardware for compute nodes on vSphere

To reduce the risk of downtime, it is recommended that compute nodes be updated serially.

> **NOTE:** Multiple compute nodes can be updated in parallel given workloads are tolerant of having multiple nodes in a `NotReady` state. It is the responsibility of the administrator to ensure that the required compute nodes are available.

.Prerequisites

- You have cluster administrator permissions to execute the required permissions in the vCenter instance hosting your OpenShift Container Platform cluster.
- Your vSphere ESXi hosts are version 8.0 Update 1 or later, or VWware vSphere Foundation 9, or VMware Cloud Foundation 9.

.Procedure

1. List the compute nodes in your cluster.
```bash
$ oc get nodes -l node-role.kubernetes.io/worker
```
.Example output
```bash
NAME              STATUS   ROLES    AGE   VERSION
compute-node-0    Ready    worker   30m   v1.34.2
compute-node-1    Ready    worker   30m   v1.34.2
compute-node-2    Ready    worker   30m   v1.34.2
```
Note the names of your compute nodes.

1. Mark the compute node as unschedulable:
```bash
$ oc adm cordon <compute_node>
```

1. Evacuate the pods from the compute node. There are several ways to do this. For example, you can evacuate all or selected pods on a node:
```bash
$ oc adm drain <compute_node> [--pod-selector=<pod_selector>]
```
See the "Evacuating pods on nodes" section for other options to evacuate pods from a node.

1. Shut down the virtual machine (VM) associated with the compute node. Do this in the vSphere client by right-clicking the VM and selecting *Power* -> *Shut Down Guest OS*. Do not shut down the VM using *Power Off* because it might not shut down safely.

1. Update the VM in the vSphere client. Follow link:https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-60768C2F-72E1-42E0-8A17-CA76849F2950.html[Upgrade the Compatibility of a Virtual Machine Manually] in the VMware documentation for more information.

1. Power on the VM associated with the compute node. Do this in the vSphere client by right-clicking the VM and selecting *Power On*.

1. Wait for the node to report as `Ready`:
```bash
$ oc wait --for=condition=Ready node/<compute_node>
```

1. Mark the compute node as schedulable again:
```bash
$ oc adm uncordon <compute_node>
```

1. Repeat this procedure for each compute node in your cluster.