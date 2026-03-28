# About OADP Self-Service

From OADP 1.5.0 onward, you do not need the `cluster-admin` role to perform the backup and restore operations. You can use OADP with the namespace `admin` role. The namespace `admin` role has administrator access only to the namespace the user is assigned to.

You can use the Self-Service feature only after the cluster administrator installs the OADP Operator and provides the necessary permissions.

The OADP Self-Service feature provides secure self-service data protection capabilities for users without `cluster-admin` privileges while maintaining proper access controls.

The OADP cluster administrator creates a user with the namespace `admin` role and provides the necessary Role Based Access Controls (RBAC) to the user to perform OADP Self-Service actions. As this user has limited access compared to the `cluster-admin` role, this user is referred to as a namespace admin user. 

As a namespace admin user, you can back up and restore applications deployed in your authorized namespace on the cluster.

OADP Self-Service offers the following benefits:

- As a cluster administrator:
- You allow namespace-scoped backup and restore operations to a namespace admin user. This means, a namespace admin user cannot access a namespace that they are not authorized to.
- You keep administrator control over non-administrator operations through `DataProtectionApplication` configuration and policies.

- As a namespace admin user:
- You can create backup and restore custom resources for your authorized namespace.
- You can create dedicated backup storage locations in your authorized namespace.
- You have secure access to backup logs and status information.