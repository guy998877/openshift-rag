# Installing and configuring OADP with OpenShift Virtualization

As a cluster administrator, you install OADP by installing the OADP Operator.

The latest version of the OADP Operator installs [Velero 1.16](https://velero.io/docs/v1.16).

.Prerequisites

- Access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. Install the OADP Operator according to the instructions for your storage provider.

1. Install the Data Protection Application (DPA) with the `kubevirt` and `openshift` OADP plugins.

1. Back up virtual machines by creating a `Backup` custom resource (CR).

> **WARNING:** Red Hat support is limited to only the following options: * CSI backups * CSI backups with DataMover.
You restore the `Backup` CR by creating a `Restore` CR.