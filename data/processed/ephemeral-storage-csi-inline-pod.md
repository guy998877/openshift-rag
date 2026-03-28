# Embedding a CSI inline ephemeral volume in the pod specification

You can embed a CSI inline ephemeral volume in the `Pod` specification in OpenShift Container Platform. At runtime, nested inline volumes follow the ephemeral lifecycle of their associated pods so that the CSI driver handles all phases of volume operations as pods are created and destroyed.

.Procedure

1. Create the `Pod` object definition and save it to a file.

1. Embed the CSI inline ephemeral volume in the file as in the following pod YAML file:
.Example pod YAML file with embedded ephemeral volume
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: my-csi-app
spec:
  containers:
    - name: my-frontend
      image: busybox
      volumeMounts:
      - mountPath: "/data"
        name: my-csi-inline-vol
      command: [ "sleep", "1000000" ]
  volumes:
    - name: my-csi-inline-vol
      csi:
        driver: inline.storage.kubernetes.io
        volumeAttributes:
          foo: bar
```
- `spec.volumes.name`: The name of the volume that is used by pods.

1. Create the object definition file that you saved in the previous step by running the following command.
```bash
$ oc create -f my-csi-app.yaml
```