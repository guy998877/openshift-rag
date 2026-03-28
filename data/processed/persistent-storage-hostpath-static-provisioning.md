# Statically provisioning hostPath volumes

A pod that uses a hostPath volume must be referenced by manual (static) provisioning.

.Procedure

1. Define the persistent volume (PV) by creating a `pv.yaml` file with the `PersistentVolume` object definition:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume <1>
  labels:
    type: local
spec:
  storageClassName: manual <2>
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce <3>
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: "/mnt/data" <4>
```
<1> The name of the volume. This name is how the volume is identified by persistent volume (PV) claims or pods.
<2> Used to bind persistent volume claim (PVC) requests to the PV.
<3> The volume can be mounted as `read-write` by a single node.
<4> The configuration file specifies that the volume is at `/mnt/data` on the cluster's node. To avoid corrupting your host system, do not mount to the container root, `/`, or any path that is the same in the host and the container. You can safely mount the host by using `/host` 

1. Create the PV from the file:
```bash
$ oc create -f pv.yaml
```

1. Define the PVC by creating a `pvc.yaml` file with the `PersistentVolumeClaim` object definition:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pvc-volume
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: manual
```

1. Create the PVC from the file:
```bash
$ oc create -f pvc.yaml
```