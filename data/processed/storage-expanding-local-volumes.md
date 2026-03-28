# Expanding local volumes

You can manually expand persistent volumes (PVs) and persistent volume claims (PVCs) created by using the local storage operator (LSO).

.Procedure

1. Expand the underlying devices. Ensure that appropriate capacity is available on these devices.

1. Update the corresponding PV objects to match the new device sizes by editing the `.spec.capacity` field of the PV.

1. For the storage class that is used for binding the PVC to PV, set the `allowVolumeExpansion` field to `true`.

1. For the PVC, set the `.spec.resources.requests.storage` field to match the new size.
Kubelet automatically expands the underlying file system on the volume, if necessary, and updates the status field of the PVC to reflect the new size.