# Static provisioning across subscriptions for Azure File by creating a PV and PVC:

.Prerequisites
- Installed OpenShift Container Platform cluster on Azure with the service principal or managed identity as an Azure identity in one subscription (call it Subscription A)

- Access to another subscription (call it Subscription B) with the storage that is in the same tenant as the cluster

- Logged in to the Azure CLI

.Procedure
1. For your Azure File share, record the resource group, storage account, storage account key, and Azure File name. These values are used for the next steps.

1. Create a secret for the persistent volume parameter `spec.csi.nodeStageSecretRef.name` by running the following command:
```bash
$ oc create secret generic azure-storage-account-<storageaccount-name>-secret --from-literal=azurestorageaccountname="<azure-storage-account-name>" --from-literal azurestorageaccountkey="<azure-storage-account-key>" --type=Opaque
```
Where:
`<azure-storage-account-name>` and `<azure-storage-account-key>` are the Azure storage account name and key respectively that you recorded in Step 1.

1. Create a persistent volume (PV) by using a similar configuration to the following example file:
.Example PV YAML file
```bash
apiVersion: v1
kind: PersistentVolume
metadata:
  annotations:
    pv.kubernetes.io/provisioned-by: file.csi.azure.com
  name: <pv-name> <1>
spec:
  capacity:
    storage: 10Gi <2>
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain  
  storageClassName: <sc-name> <3>
  mountOptions:
    - cache=strict
    - nosharesock
    - actimeo=30
    - nobrl 
  csi:
    driver: file.csi.azure.com
    volumeHandle: "{resource-group-name}#{storage-account-name}#{file-share-name}" <4>
    volumeAttributes:
      shareName: <existing-file-share-name> <5>
    nodeStageSecretRef:
      name: <secret-name>  <6>
      namespace: <secret-namespace>  <7>
```
<1> The name of the PV.
<2> The size of the PV.
<3> The storage class name.
<4> Ensure that `volumeHandle` is unique for every identical share in the cluster.
<5> For `<existing-file-share-name>, use only the file share name and not the full path.
<6> The secret name created in the previous step.
<7> The namespace where the secret resides.

1. Create a persistent value claim (PVC) specifying the existing Azure File share referenced in Step 1 using a similar configuration to the following:
.Example PVC YAML file
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <pvc-name> <1>
spec:
  storageClassName: <sc-name> <2>
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```
<1> The name of the PVC.
<2> The name of the storage class that you specified for the PV in the previous step.

.Recommendation to use a storage class
In the preceding example of static provisioning across subscriptions, the storage class referenced in the PV and PVC is not strictly necessary, as storage classes are not required to accomplish static provisioning. However, it is advisable to use a storage class to avoid cases where a manually created PVC accidentally does not match a manually created PV, and thus potentially triggers dynamic provisioning of a new PV. Other ways to avoid this issue would be to create a storage class with `provisioner: kubernetes.io/no-provisioner` or reference a non-existing storage class, which in both cases ensures that dynamic provisioning does not occur. When using either of these strategies, if a mis-matched PV and PVC occurs, the PVC stays in a pending state, and you can correct the error.