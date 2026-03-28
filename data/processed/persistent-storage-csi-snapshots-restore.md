# Restoring a volume snapshot

The `VolumeSnapshot` CRD content can be used to restore the existing volume to a previous state.

After your `VolumeSnapshot` CRD is bound and the `readyToUse` value is set to `true`, you can use that resource to provision a new volume that is pre-populated with data from the snapshot.

.Prerequisites
- Logged in to a running OpenShift Container Platform cluster.
- A persistent volume claim (PVC) created using a Container Storage Interface (CSI) driver that supports volume snapshots.
- A storage class to provision the storage back end.
- A volume snapshot has been created and is ready to use.

.Procedure

1. Specify a `VolumeSnapshot` data source on a PVC as shown in the following:
.pvc-restore.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim-restore
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: mysnap <1>
    kind: VolumeSnapshot <2>
    apiGroup: snapshot.storage.k8s.io <3>
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```
<1> Name of the `VolumeSnapshot` object representing the snapshot to use as source.
<2> Must be set to the `VolumeSnapshot` value.
<3> Must be set to the `snapshot.storage.k8s.io` value.

1. Create a PVC by entering the following command:

```bash
$ oc create -f pvc-restore.yaml
```

1. Verify that the restored PVC has been created by entering the following command:

```bash
$ oc get pvc
```
A new PVC such as `myclaim-restore` is displayed.