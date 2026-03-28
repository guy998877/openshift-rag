# Scaling up the storage of clusters by using the web console

You can scale up the storage capacity of the worker nodes on a cluster by using the OpenShift Container Platform web console.

.Prerequisites

- You have additional unused devices on each cluster to be used by Logical Volume Manager (LVM) Storage.
- You have created an `LVMCluster` custom resource (CR).

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Click *Ecosystem* -> *Installed Operators*. 
1. Click *LVM Storage* in the `openshift-lvm-storage` namespace.
1. Click the *LVMCluster* tab to view the `LVMCluster` CR created on the cluster.
1. From the *Actions* menu, select *Edit LVMCluster*.
1. Click the *YAML* tab.
1. Edit the `LVMCluster` CR to add the new device path in the `deviceSelector` field:
1. Click *Save*.