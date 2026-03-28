# Creating an LVMCluster CR by using the web console

You can create an `LVMCluster` CR on a worker node using the OpenShift Container Platform web console.

> **IMPORTANT:** You can only create a single instance of the `LVMCluster` custom resource (CR) on an OpenShift Container Platform cluster.

.Prerequisites

- You have access to the OpenShift Container Platform cluster with `cluster-admin` privileges.

- You have installed LVM Storage.

- You have installed a worker node in the cluster.

- You read the "About the LVMCluster custom resource" section.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Click *Ecosystem* -> *Installed Operators*.
1. In the `openshift-lvm-storage` namespace, click *LVM Storage*.
1. Click *Create LVMCluster* and select either *Form view* or *YAML view*.
1. Configure the required `LVMCluster` CR parameters.
1. Click *Create*.
1. Optional: If you want to edit the `LVMCLuster` CR, perform the following actions:
.. Click the *LVMCluster* tab.
.. From the *Actions* menu, select *Edit LVMCluster*. 
.. Click *YAML* and edit the required `LVMCLuster` CR parameters.  
.. Click *Save*.

.Verification

1. On the *LVMCLuster* page, check that the `LVMCluster` CR is in the `Ready` state. 
1. Optional: To view the available storage classes created by LVM Storage for each device class, click *Storage* -> *StorageClasses*. 
1. Optional: To view the available volume snapshot classes created by LVM Storage for each device class, click *Storage* -> *VolumeSnapshotClasses*.