# Ways to scale up the storage of clusters

OpenShift Container Platform supports additional worker nodes for clusters on bare metal user-provisioned infrastructure. You can scale up the storage of clusters either by adding new worker nodes with available storage or by adding new devices to the existing worker nodes. 

Logical Volume Manager (LVM) Storage detects and uses additional worker nodes when the nodes become active.

To add a new device to the existing worker nodes on a cluster, you must add the path to the new device in the `deviceSelector` field of the `LVMCluster` custom resource (CR).

> **IMPORTANT:** You can add the `deviceSelector` field in the `LVMCluster` CR only while creating the `LVMCluster` CR. If you have not added the `deviceSelector` field while creating the `LVMCluster` CR, you must delete the `LVMCluster` CR and create a new `LVMCluster` CR containing the `deviceSelector` field.

If you do not add the `deviceSelector` field in the `LVMCluster` CR, LVM Storage automatically adds the new devices when the devices are available.
> **NOTE:** LVM Storage adds only the supported devices. For information about unsupported devices, see "Devices not supported by LVM Storage".