# Ways to delete an LVMCluster custom resource

You can delete an `LVMCluster` custom resource (CR) by using the OpenShift CLI (`oc`) or the OpenShift Container Platform web console. If you have installed LVM Storage by using Red Hat Advanced Cluster Management (RHACM), you can also delete an `LVMCluster` CR by using RHACM.

Upon deleting the `LVMCluster` CR, LVM Storage deletes the following CRs:

- `storageClass`
- `volumeSnapshotClass`
- `LVMVolumeGroup`
- `LVMVolumeGroupNodeStatus`