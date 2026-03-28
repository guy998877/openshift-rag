# Enabling NonAdminBackupStorageLocation administrator approval workflow

Enable the administrator approval workflow for `NonAdminBackupStorageLocation` custom resource to review backup storage location requests from namespace administrators before they are applied. This helps you maintain control over backup storage configurations.

.Prerequisites

- You are logged in to the cluster with the `cluster-admin` role.
- You have installed the OADP Operator.
- You have enabled OADP Self-Service in the `DataProtectionApplication` CR.

.Procedure

- To enable the NABSL administrator approval workflow, edit the DPA CR by using the following example configuration:
.Example `DataProtectionApplication` CR
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: oadp-backup
  namespace: openshift-adp
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: kopia
    velero:
      defaultPlugins:
        - aws
        - openshift
        - csi
      noDefaultBackupLocation: true
  nonAdmin:
    enable: true
    requireApprovalForBSL: true 
```
where:
`noDefaultBackupLocation`:: Specifies that there is no default backup storage location configured in the DPA CR. Set to `true` to enable the namespace admin user to create a NABSL CR and send the CR request for approval.
`requireApprovalForBSL`:: Specifies whether the NABSL administrator approval workflow is enabled. Set to `true` to enable the approval workflow.