# Replacing a control plane machine

To replace a control plane machine in a cluster that has a control plane machine set, you delete the machine manually. The control plane machine set replaces the deleted machine with one using the specification in the control plane machine set custom resource (CR).

.Prerequisites

- If your cluster runs on Red Hat OpenStack Platform (RHOSP) and you need to evacuate a compute server, such as for an upgrade, you must disable the RHOSP compute node that the machine runs on by running the following command:
```bash
$ openstack compute service set <target_node_host_name> nova-compute --disable
```
For more information, see [Preparing to migrate](https://docs.redhat.com/en/documentation/red_hat_openstack_platform/17.1/html/configuring_the_compute_service_for_instance_creation/assembly_migrating-virtual-machine-instances-between-compute-nodes_migrating-instances#proc_preparing-to-migrate_migrating-instances) in the RHOSP documentation.

.Procedure

1. List the control plane machines in your cluster by running the following command:
```bash
$ oc get machines \
  -l machine.openshift.io/cluster-api-machine-role==master \
  -n openshift-machine-api
```

1. Delete a control plane machine by running the following command:
```bash
$ oc delete machine \
  -n openshift-machine-api \
  <control_plane_machine_name> <1>
```
<1> Specify the name of the control plane machine to delete.
> **NOTE:** If you delete multiple control plane machines, the control plane machine set replaces them according to the configured update strategy: * For clusters that use the default `RollingUpdate` update strategy, the Operator replaces one machine at a time until each machine is replaced. * For clusters that are configured to use the `OnDelete` update strategy, the Operator creates all of the required replacement machines simultaneously. Both strategies maintain etcd health during control plane machine replacement.