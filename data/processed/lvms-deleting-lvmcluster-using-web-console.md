# Deleting an LVMCluster CR by using the web console

You can delete the `LVMCluster` custom resource (CR) using the OpenShift Container Platform web console.

.Prerequisites

- You have access to OpenShift Container Platform as a user with `cluster-admin` permissions.
- You have deleted the persistent volume claims (PVCs), volume snapshots, and volume clones provisioned by LVM Storage. You have also deleted the applications that are using these resources.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Click *Ecosystem* -> *Installed Operators* to view all the installed Operators.
1. Click *LVM Storage* in the `openshift-lvm-storage` namespace.
1. Click the *LVMCluster* tab.
1. From the *Actions*, select *Delete LVMCluster*.
1. Click *Delete*.

.Verification

- On the `LVMCLuster` page, check that the `LVMCluster` CR has been deleted.