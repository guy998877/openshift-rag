# Recovering from failure when expanding volumes

To retry a failed or pending resize request, update the `spec.resources.requests.storage` field in the persistent volume claim (PVC). You must specify a value larger than the original volume size to successfully retrigger the operation.

Entering a smaller resize value in the `.spec.resources.requests.storage` field for the existing PVC does not work. 

.Procedure

1. Mark the persistent volume (PV) that is bound to the PVC with the `Retain` reclaim policy. Change the `persistentVolumeReclaimPolicy` field to `Retain`.

1. Delete the PVC.

1. Manually edit the PV and delete the `claimRef` entry from the PV specification to ensure that the newly created PVC can bind to the PV marked `Retain`. This marks the PV as `Available`.

1. Recreate the PVC in a smaller size, or a size that can be allocated by the underlying storage provider.

1. Set the `volumeName` field of the PVC to the name of the PV. This binds the PVC to the provisioned PV only.

1. Restore the reclaim policy on the PV.