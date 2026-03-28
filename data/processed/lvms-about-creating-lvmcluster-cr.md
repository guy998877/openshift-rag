# Ways to create an LVMCluster custom resource

You can create an `LVMCluster` custom resource (CR) by using the OpenShift CLI (`oc`) or the OpenShift Container Platform web console. If you have installed LVM Storage by using Red Hat Advanced Cluster Management (RHACM), you can also create an `LVMCluster` CR by using RHACM. 

> **IMPORTANT:** You must create the `LVMCluster` CR in the same namespace where you installed the LVM Storage Operator, which is `openshift-storage` by default.

Upon creating the `LVMCluster` CR, LVM Storage creates the following system-managed CRs:

- A `storageClass` and `volumeSnapshotClass` for each device class.
> **NOTE:** LVM Storage configures the name of the storage class and volume snapshot class in the format `lvms-<device_class_name>`, where, `<device_class_name>` is the value of the `deviceClasses.name` field in the `LVMCluster` CR. For example, if the `deviceClasses.name` field is set to vg1, the name of the storage class and volume snapshot class is `lvms-vg1`.

- `LVMVolumeGroup`: This CR is a specific type of persistent volume (PV) that is backed by an LVM volume group. It tracks the individual volume groups across multiple nodes.
- `LVMVolumeGroupNodeStatus`: This CR tracks the status of the volume groups on a node.