# Backing up applications with File System Backup

.Prerequisites

- You must install the OpenShift API for Data Protection (OADP) Operator.
- You must not disable the default `nodeAgent` installation by setting `spec.configuration.nodeAgent.enable` to `false` in the `DataProtectionApplication` CR.
- You must select Kopia or Restic as the uploader by setting `spec.configuration.nodeAgent.uploaderType` to `kopia` or `restic` in the `DataProtectionApplication` CR.
- The `DataProtectionApplication` CR must be in a `Ready` state.

.Procedure

- Create the `Backup` CR, as in the following example:
```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: <backup>
  labels:
    velero.io/storage-location: default
  namespace: openshift-adp
spec:
  defaultVolumesToFsBackup: true <1>
...
```
<1> In OADP version 1.2 and later, add the `defaultVolumesToFsBackup: true` setting within the `spec` block. In OADP  version 1.1, add `defaultVolumesToRestic: true`.