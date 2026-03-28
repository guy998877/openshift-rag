# Changes from OADP 1.4 to 1.5

The Velero server has been updated from version 1.14 to 1.16.

This changes the following:

Version Support changes::
OpenShift API for Data Protection implements a streamlined version support policy. Red Hat supports only one version of OpenShift API for Data Protection (OADP) on one {OCP-short} version to ensure better stability and maintainability. OADP 1.5.0 is only supported on {OCP-short} 4.19 version.

OADP Self-Service::
OADP 1.5.0 introduces a new feature named OADP Self-Service, enabling namespace admin users to back up and restore applications on the OpenShift Container Platform.
In the earlier versions of OADP, you needed the cluster-admin role to perform OADP operations such as backing up and restoring an application, creating a backup storage location, and so on.
From OADP 1.5.0 onward, you do not need the cluster-admin role to perform the backup and restore operations. You can use OADP with the namespace admin role. The namespace admin role has administrator access only to the namespace the user is assigned to.
You can use the Self-Service feature only after the cluster administrator installs the OADP Operator and provides the necessary permissions.

`backupPVC` and `restorePVC` configurations::
A `backupPVC` resource is an intermediate persistent volume claim (PVC) to access data during the data movement backup operation. You create a `readonly` backup PVC by using the `nodeAgent.backupPVC` section of the `DataProtectionApplication` (DPA) custom resource.
A `restorePVC` resource is an intermediate PVC that is used to write data during the Data Mover restore operation.
You can configure `restorePVC` in the DPA by using the `ignoreDelayBinding` field.