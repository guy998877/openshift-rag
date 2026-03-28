# Enabling performance plus by snapshot or cloning

Normally, performance plus can be enabled only on new disks. For a workaround, you can use this procedure.

.Prerequisites

- Access to a Microsoft Azure cluster with cluster-admin privileges.

- Access to an Azure disk with performance plus enabled.

- Have created a storage class to use performance plus enhanced Azure disks.
For more information about creating the storage class, see Section _Creating a storage class to use performance plus enhanced disks_.

.Procedure
To enable performance plus by snapshot or clone:

1. Create a snapshot of the existing volume that does not have performance plus enabled on it.

1. Provision a new disk from that snapshot using a storage class with `enablePerformancePlus` set to "true".

Or

- Clone the persistent volume claim (PVC) using a storage class with `enablePerformancePlus` set to "true" to create a new disk clone.