# Uninstalling LVM Storage by using the web console

You can uninstall LVM Storage using the OpenShift Container Platform web console.

.Prerequisites

- You have access to OpenShift Container Platform as a user with `cluster-admin` permissions.
- You have deleted the persistent volume claims (PVCs), volume snapshots, and volume clones provisioned by LVM Storage. You have also deleted the applications that are using these resources.
- You have deleted the `LVMCluster` custom resource (CR).

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Click *Ecosystem* -> *Installed Operators*.
1. Click *LVM Storage* in the `openshift-lvm-storage` namespace.
1. Click the *Details* tab. 
1. From the *Actions* menu, select *Uninstall Operator*.
1. Optional: When prompted, select the *Delete all operand instances for this operator* checkbox to delete the operand instances for LVM Storage. 
1. Click *Uninstall*.