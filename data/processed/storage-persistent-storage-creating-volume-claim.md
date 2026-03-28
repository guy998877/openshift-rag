# Creating the persistent volume claim

.Prerequisites

Storage must exist in the underlying infrastructure before it can be mounted as
a volume in OpenShift Container Platform.

.Procedure

1. In the OpenShift Container Platform web console, click *Storage* -> *Persistent Volume Claims*.

1. In the persistent volume claims overview, click *Create Persistent Volume Claim*.

1. Define the desired options on the page that appears.

.. Select the previously-created storage class from the drop-down menu.

.. Enter a unique name for the storage claim.

.. Select the access mode. This selection determines the read and write access for the storage claim.

.. Define the size of the storage claim.

1. Click *Create* to create the persistent volume claim and generate a persistent
volume.