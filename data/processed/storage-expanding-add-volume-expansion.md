# Enabling volume expansion support

Before you can expand persistent volumes, the `StorageClass` object must
have the `allowVolumeExpansion` field set to `true`.

.Procedure

- Edit the `StorageClass` object and add the `allowVolumeExpansion` attribute by running the following command:
```bash
$ oc edit storageclass <storage_class_name> <1>
```
<1> Specifies the name of the storage class.
The following example demonstrates adding this line at the bottom
of the storage class configuration.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
...
parameters:
  type: gp2
reclaimPolicy: Delete
allowVolumeExpansion: true <1>
```
<1> Setting this attribute to `true` allows PVCs to be
expanded after creation.