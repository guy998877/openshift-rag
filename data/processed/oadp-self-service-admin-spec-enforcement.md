# OADP Self-Service administrator DPA spec enforcement

Enforce policy templates in the `DataProtectionApplication` (DPA) custom resource (CR) to control `NonAdminBackup`, `NonAdminRestore`, and `NonAdminBackupStorageLocation` custom resources created by namespace administrators. This helps you maintain compliance standards. 

The cluster administrator can enforce a company, or a compliance policy by using the following fields in the `DataProtectionApplication` (DPA) CR:

`enforceBSLSpec`:: To enforce a policy on the `NonAdminBackupStorageLocation` CR.
`enforceBackupSpec`:: To enforce a policy on the `NonAdminBackup` CR.
`enforceRestoreSpec`:: To enforce a policy on the `NonAdminRestore` CR.

By using the enforceable fields, administrators can ensure that the NABSL, NAB, and NAR CRs created by a namespace admin user, comply with the administrator defined policy.