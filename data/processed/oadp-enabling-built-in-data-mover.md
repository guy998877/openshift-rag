# Enabling the built-in Data Mover

Enable the built-in Data Mover by configuring the CSI plugin and node agent in the `DataProtectionApplication` custom resource (CR). This provides volume-level backup and restore operations by using the Kopia uploader.

.Procedure

- Include the CSI plugin and enable the node agent in the `DataProtectionApplication` custom resource (CR) as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: dpa-sample
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: kopia
    velero:
      defaultPlugins:
      - openshift
      - aws
      - csi
      defaultSnapshotMoveData: true
      defaultVolumesToFSBackup:
      featureFlags:
      - EnableCSI
# ...
```
where:

`enable`:: Specifies the flag to enable the node agent.
`uploaderType`:: Specifies the type of uploader. The possible values are `restic` or `kopia`. The built-in Data Mover uses Kopia as the default uploader mechanism regardless of the value of the `uploaderType` field.
`csi`:: Specifies the CSI plugin included in the list of default plugins.
`defaultVolumesToFSBackup`:: Specifies the default behavior for volumes. In OADP 1.3.1 and later, set to `true` if you use Data Mover only for volumes that opt out of `fs-backup`. Set to `false` if you use Data Mover by default for volumes.