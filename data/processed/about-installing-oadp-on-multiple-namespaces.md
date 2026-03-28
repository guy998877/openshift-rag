# Installation of OADP on multiple namespaces

You can install OpenShift API for Data Protection into multiple namespaces on the same cluster so that multiple project owners can manage their own OADP instance. This use case has been validated with File System Backup (FSB) and Container Storage Interface (CSI).

You install each instance of OADP as specified by the per-platform procedures contained in this document with the following additional requirements:

- All deployments of OADP on the same cluster must be the same version, for example, 1.4.0. Installing different versions of OADP on the same cluster is *not* supported.

- Each individual deployment of OADP must have a unique set of credentials and at least one `BackupStorageLocation` configuration. You can also use multiple `BackupStorageLocation` configurations within the same namespace.

- By default, each OADP deployment has cluster-level access across namespaces. {OCP} administrators need to carefully review potential impacts, such as not backing up and restoring to and from the same namespace concurrently.