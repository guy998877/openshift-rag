# Expanding CSI volumes

You can use the Container Storage Interface (CSI) to expand storage volumes after they have already been created.

> **IMPORTANT:** Shrinking persistent volumes (PVs) is _not_ supported.

.Prerequisites

- The underlying CSI driver supports resize. See "CSI drivers supported by OpenShift Container Platform" in the "Additional resources" section.

- Dynamic provisioning is used.

- The controlling `StorageClass` object has `allowVolumeExpansion` set to `true`. For more information, see "Enabling volume expansion support."

.Procedure

1. For the persistent volume claim (PVC), set `.spec.resources.requests.storage` to the desired new size.

1. Watch the `status.conditions` field of the PVC to see if the resize has completed. OpenShift Container Platform adds the `Resizing` condition to the PVC during expansion, which is removed after expansion completes.