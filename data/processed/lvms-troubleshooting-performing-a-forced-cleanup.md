# Performing a forced clean-up

If the disk or node-related problems persist even after you have completed the troubleshooting procedures, you must perform a forced clean-up. A forced clean-up is used to address persistent issues and ensure the proper functioning of Logical Volume Manager (LVM) Storage.

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

- You have logged in to the pass:quotes[OpenShift CLI (`oc`)] as a user with `cluster-admin` permissions.

- You have deleted all the persistent volume claims (PVCs) that were created by using LVM Storage.

- You have stopped the pods that are using the PVCs that were created by using LVM Storage.

.Procedure

1. Switch to the namespace where you have installed the LVM Storage Operator by running the following command:
```bash
$ oc project <namespace>
```

1. Check if the `LogicalVolume` custom resources (CRs) are present by running the following command:
```bash
$ oc get logicalvolume
```

.. If the `LogicalVolume` CRs are present, delete them by running the following command:
```bash
$ oc delete logicalvolume <name> <1>
```
<1> Replace `<name>` with the name of the `LogicalVolume` CR.

.. After deleting the `LogicalVolume` CRs, remove their finalizers by running the following command:
```bash
$ oc patch logicalvolume <name> -p '{"metadata":{"finalizers":[]}}' --type=merge <1>
```
<1> Replace `<name>` with the name of the `LogicalVolume` CR.

1. Check if the `LVMVolumeGroup` CRs are present by running the following command:
```bash
$ oc get lvmvolumegroup
```

.. If the `LVMVolumeGroup` CRs are present, delete them by running the following command:
```bash
$ oc delete lvmvolumegroup <name> <1>
```
<1> Replace `<name>` with the name of the `LVMVolumeGroup` CR.

.. After deleting the `LVMVolumeGroup` CRs, remove their finalizers by running the following command:
```bash
$ oc patch lvmvolumegroup <name> -p '{"metadata":{"finalizers":[]}}' --type=merge <1>
```
<1> Replace `<name>` with the name of the `LVMVolumeGroup` CR. 

1. Delete any `LVMVolumeGroupNodeStatus` CRs by running the following command:
```bash
$ oc delete lvmvolumegroupnodestatus --all
```

1. Delete the `LVMCluster` CR by running the following command:
```bash
$ oc delete lvmcluster --all
```

.. After deleting the `LVMCluster` CR, remove its finalizer by running the following command:
```bash
$ oc patch lvmcluster <name> -p '{"metadata":{"finalizers":[]}}' --type=merge <1>
```
<1> Replace `<name>` with the name of the `LVMCluster` CR.