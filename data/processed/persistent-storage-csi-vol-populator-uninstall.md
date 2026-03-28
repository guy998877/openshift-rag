# Uninstalling volume populators

The following procedure explains how to uninstall volume populators.

.Prerequisites

- Access to the OpenShift Container Platform web console.

- Access to the cluster with cluster-admin privileges.

.Procedure

To uninstall volume populators, delete in reverse order all objects installed in the procedures under:

1. Section _Creating prepopulated volumes using volume populators_.

1. Section _Creating CRDs for volume populators_.
Be sure to remove the `VolumePopulator` instance.