# Dynamically provisioning VMware vSphere volumes using the CLI

OpenShift Container Platform installs a default StorageClass, named `thin`, that uses the `thin` disk format for provisioning volumes.

.Prerequisites

- Storage must exist in the underlying infrastructure before it can be mounted as a volume in OpenShift Container Platform.

.Procedure (CLI)

1. You can define a VMware vSphere PersistentVolumeClaim by creating a file, `pvc.yaml`, with the following contents:
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pvc <1>
spec:
  accessModes:
  - ReadWriteOnce <2>
  resources:
    requests:
      storage: 1Gi <3>
```
<1> A unique name that represents the persistent volume claim.
<2> The access mode of the persistent volume claim. With `ReadWriteOnce`, the volume can be mounted with read and write permissions by a single node.
<3> The size of the persistent volume claim.

1. Enter the following command to create the `PersistentVolumeClaim` object from the file:
```bash
$ oc create -f pvc.yaml
```