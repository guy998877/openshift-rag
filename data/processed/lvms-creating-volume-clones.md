# Creating volume clones

To create a clone of a persistent volume claim (PVC), you must create a `PersistentVolumeClaim` object in the namespace where you created the source PVC.

> **IMPORTANT:** The cloned PVC has write access.

.Prerequisites

- You ensured that the source PVC is in `Bound` state. This is required for a consistent clone.

.Procedure

1. Log in to the OpenShift CLI (`oc`).

1. Create a `PersistentVolumeClaim` object:
.Example `PersistentVolumeClaim` object to create a volume clone
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: lvm-pvc-clone
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: lvms-vg1 <1>
  volumeMode: Filesystem <2>
  dataSource:
    kind: PersistentVolumeClaim
    name: lvm-pvc <3>
  resources:
    requests:
      storage: 1Gi <4>
```
<1> Set this field to the value of the `storageClassName` field in the source PVC.
<2> Set this field to the `volumeMode` field in the source PVC.
<3> Specify the name of the source PVC.
<4> Specify the storage size for the cloned PVC. The storage size of the cloned PVC must be greater than or equal to the storage size of the source PVC.

1. Create the PVC in the namespace where you created the source PVC by running the following command:
```bash
$ oc create -f <file_name> -n <namespace>
```

.Verification

- To verify that the volume clone is created, run the following command:
```bash
$ oc get pvc -n <namespace>
```
.Example output
```bash
NAME                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
lvm-block-1-clone   Bound    pvc-e90169a8-fd71-4eea-93b8-817155f60e47   1Gi        RWO            lvms-vg1       5s
```