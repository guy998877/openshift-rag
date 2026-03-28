# Creating a custom-encrypted persistent volume

When you create a `PersistentVolumeClaim` object, OpenShift Container Platform provisions a new persistent volume (PV) and creates a `PersistentVolume` object. You can add a custom encryption key in Google Cloud Platform (GCP) to protect a PV in your cluster by encrypting the newly created PV.

For encryption, the newly attached PV that you create uses customer-managed encryption keys (CMEK) on a cluster by using a new or existing Google Cloud Key Management Service (KMS) key.

.Prerequisites
- You are logged in to a running OpenShift Container Platform cluster.
- You have created a Cloud KMS key ring and key version.

For more information about CMEK and Cloud KMS resources, see [Using customer-managed encryption keys (CMEK)](https://cloud.google.com/kubernetes-engine/docs/how-to/using-cmek).

.Procedure
To create a custom-encrypted PV, complete the following steps:

1. Create a storage class with the Cloud KMS key. The following example enables dynamic provisioning of encrypted volumes:
```yaml
--
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-gce-pd-cmek
provisioner: pd.csi.storage.gke.io
volumeBindingMode: "WaitForFirstConsumer"
allowVolumeExpansion: true
parameters:
  type: pd-standard
  disk-encryption-kms-key: projects/<key-project-id>/locations/<location>/keyRings/<key-ring>/cryptoKeys/<key> <1>
--
<1> This field must be the resource identifier for the key that will be used to encrypt new disks. Values are case-sensitive. For more information about providing key ID values, see link:https://cloud.google.com/kms/docs/resource-hierarchy#retrieve_resource_id[Retrieving a resource's ID] and link:https://cloud.google.com/kms/docs/getting-resource-ids[Getting a Cloud KMS resource ID].
+
[NOTE]
```
You cannot add the `disk-encryption-kms-key` parameter to an existing storage class. However, you can delete the storage class and recreate it with the same name and a different set of parameters. If you do this, the provisioner of the existing class must be `pd.csi.storage.gke.io`.

1. Deploy the storage class on your OpenShift Container Platform cluster using the `oc` command:
```bash
--
$ oc describe storageclass csi-gce-pd-cmek
--
+
.Example output
[source,terminal]
--
Name:                  csi-gce-pd-cmek
IsDefaultClass:        No
Annotations:           None
Provisioner:           pd.csi.storage.gke.io
Parameters:            disk-encryption-kms-key=projects/key-project-id/locations/location/keyRings/ring-name/cryptoKeys/key-name,type=pd-standard
AllowVolumeExpansion:  true
MountOptions:          none
ReclaimPolicy:         Delete
VolumeBindingMode:     WaitForFirstConsumer
Events:                none
--

. Create a file named `pvc.yaml` that matches the name of your storage class object that you created in the previous step:
+
[source,yaml]
--
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: podpvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: csi-gce-pd-cmek
  resources:
    requests:
      storage: 6Gi
--
+
[NOTE]
```
If you marked the new storage class as default, you can omit the `storageClassName` field.

1. Apply the PVC on your cluster:
```bash
--
$ oc apply -f pvc.yaml
--

. Get the status of your PVC and verify that it is created and bound to a newly provisioned PV:
+
[source,terminal]
--
$ oc get pvc
--
+
[source,terminal]
.Example output
--
NAME      STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS     AGE
podpvc    Bound     pvc-e36abf50-84f3-11e8-8538-42010a800002   10Gi       RWO            csi-gce-pd-cmek  9s
--
+
[NOTE]
```
If your storage class has the `volumeBindingMode` field set to `WaitForFirstConsumer`, you must create a pod to use the PVC before you can verify it.

Your CMEK-protected PV is now ready to use with your OpenShift Container Platform cluster.