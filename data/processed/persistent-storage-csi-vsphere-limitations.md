# vSphere CSI limitations

The following limitations apply to the vSphere Container Storage Interface (CSI) Driver Operator:

- The vSphere CSI Driver supports dynamic and static provisioning. However, when using static provisioning in the PV specifications, do not use the key `storage.kubernetes.io/csiProvisionerIdentity` in `csi.volumeAttributes` because this key indicates dynamically provisioned PVs.

- Migrating persistent container volumes between datastores using the vSphere client interface is not supported with OpenShift Container Platform.