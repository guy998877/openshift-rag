# Deleting an LVMCluster CR by using the CLI

You can delete the `LVMCluster` custom resource (CR) using the OpenShift CLI (`oc`).

.Prerequisites

- You have access to OpenShift Container Platform as a user with `cluster-admin` permissions.
- You have deleted the persistent volume claims (PVCs), volume snapshots, and volume clones provisioned by LVM Storage. You have also deleted the applications that are using these resources.

.Procedure

1. Log in to the OpenShift CLI (`oc`).
1. Delete the `LVMCluster` CR by running the following command:
```bash
$ oc delete lvmcluster <lvm_cluster_name> -n <namespace>
```

.Verification

- To verify that the `LVMCluster` CR has been deleted, run the following command:
```bash
$ oc get lvmcluster -n <namespace>
```
.Example output
```bash
No resources found in openshift-lvm-storage namespace.
```