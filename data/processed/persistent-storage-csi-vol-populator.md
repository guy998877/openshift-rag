# Volume populators overview

In OpenShift Container Platform versions 4.12 through 4.19, the `dataSource` field in a persistent volume claim (PVC) spec provides volume populator capability. However, it is limited to using only PVCs and snapshots as the data source for populating volumes. 

Starting with OpenShift Container Platform version 4.20, the `dataSourceRef` field is used instead. With the `dataSourceRef` field, you can use any appropriate custom resource (CR) as the data source to prepopulate a new volume.

> **NOTE:** Volume populator functionality using the `dataSource` field is likely to be deprecated in future versions. If you have created any volume populators using this field, consider re-creating your volume populators to use the `dataSourceRef` field to avoid future issues.

Volume population is enabled by default and OpenShift Container Platform includes the installed `volume-data-source-validator` controller. However, OpenShift Container Platform does not ship with any volume populators.