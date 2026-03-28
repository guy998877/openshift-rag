# Creating generic ephemeral volumes

Configure temporary storage by creating generic ephemeral volumes that use drivers that support dynamic provisioning.

.Procedure

1. Create the `pod` object definition and save it to a file.

1. Include the generic ephemeral volume information in the file.
.my-example-pod-with-generic-vols.yaml
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: my-app
spec:
  containers:
    - name: my-frontend
      image: busybox:1.28
      volumeMounts:
      - mountPath: "/mnt/storage"
        name: data
      command: [ "sleep", "1000000" ]
  volumes:
    - name: data
      ephemeral:
        volumeClaimTemplate:
          metadata:
            labels:
              type: my-app-ephvol
          spec:
            accessModes: [ "ReadWriteOnce" ]
            storageClassName: "gp2-csi"
            resources:
              requests:
                storage: 1Gi

```
- `volumes.name`:: Specifies the name for the generic ephemeral volume.