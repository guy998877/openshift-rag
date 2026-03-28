# OADP plugins

The OpenShift API for Data Protection (OADP) provides default Velero plugins that are integrated with storage providers to support backup and snapshot operations. You can create [custom plugins](https://velero.io/docs/v1.16/custom-plugins/) based on the Velero plugins.

OADP also provides plugins for OpenShift Container Platform resource backups, OpenShift Virtualization resource backups, and Container Storage Interface (CSI) snapshots.

[cols="3", options="header"]
.OADP plugins
|===
|OADP plugin |Function |Storage location

.2+|`aws` |Backs up and restores Kubernetes objects. |AWS S3
|Backs up and restores volumes with snapshots. |AWS EBS

.2+|`azure` |Backs up and restores Kubernetes objects. |Microsoft Azure Blob storage
|Backs up and restores volumes with snapshots. |Microsoft Azure Managed Disks

.2+|`gcp` |Backs up and restores Kubernetes objects. |Google Cloud Storage
|Backs up and restores volumes with snapshots. |Google Compute Engine Disks

|`openshift` |Backs up and restores OpenShift Container Platform resources. ^[1]^ |Object store

|`kubevirt` |Backs up and restores OpenShift Virtualization resources. ^[2]^ |Object store

|`csi` |Backs up and restores volumes with CSI snapshots. ^[3]^ |Cloud storage that supports CSI snapshots

|`hypershift` |Backs up and restores HyperShift hosted cluster resources. ^[4]^ |Object store
|===
[.small]
--
1. Mandatory.
2. Virtual machine disks are backed up with CSI snapshots or Restic.
3. The `csi` plugin uses the Kubernetes CSI snapshot API.
- OADP 1.1 or later uses `snapshot.storage.k8s.io/v1`
- OADP 1.0 uses `snapshot.storage.k8s.io/v1beta1`
4. Do not add the `hypershift` plugin in the `DataProtectionApplication` custom resource if the cluster is not a HyperShift hosted cluster. 
--