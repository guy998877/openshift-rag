# OADP Self-Service limitations

Review the limitations and unsupported features of OADP Self-Service to understand which operations are restricted for namespace administrators. This helps you plan appropriate backup and restore strategies within the supported functionality.

The following features are not supported by OADP Self-Service:

- Cross cluster backup and restore, or migrations are not supported. These OADP operations are supported for the cluster administrator.

- A namespace `admin` user cannot create a `VolumeSnapshotLocation` (VSL) CR. The cluster administrator creates and configures the VSL in the `DataProtectionApplication` (DPA) CR for a namespace `admin` user.

- The `ResourceModifiers` CR and volume policies are not supported for a namespace `admin` user.

- A namespace `admin` user can request backup or restore logs by using the `NonAdminDownloadRequest` CR, only if the backup or restore is created by a user by using the `NonAdminBackupStorageLocation` CR. 
If the backup or restore CRs are created by using the cluster-wide default backup storage location, a namespace `admin` user cannot request the backup or restore logs.

- To ensure secure backup and restore, OADP Self-Service automatically excludes the following CRs from being backed up or restored:

- `NonAdminBackup`
- `NonAdminRestore`
- `NonAdminBackupStorageLocation`
- `SecurityContextConstraints`
- `ClusterRole`
- `ClusterRoleBinding`
- `CustomResourceDefinition`
- `PriorityClasses`
- `VirtualMachineClusterInstanceTypes`
- `VirtualMachineClusterPreferences`