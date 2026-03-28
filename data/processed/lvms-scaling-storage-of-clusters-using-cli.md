# Scaling up the storage of clusters by using the CLI

You can scale up the storage capacity of the worker nodes on a cluster by using the OpenShift CLI (`oc`).

.Prerequisites

- You have additional unused devices on each cluster to be used by Logical Volume Manager (LVM) Storage.
- You have installed the OpenShift CLI (`oc`).
- You have created an `LVMCluster` custom resource (CR).

.Procedure

1. Edit the `LVMCluster` CR by running the following command:
```bash
$ oc edit <lvmcluster_file_name> -n <namespace>
```

1. Add the path to the new device in the `deviceSelector` field.

1. Save the `LVMCluster` CR.