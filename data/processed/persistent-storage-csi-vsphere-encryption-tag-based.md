# Using tag-based placement

.Procedure

To encrypt using tag-based placement:

1. In vCenter create a category for tagging datastores that will be made available to this storage class. Also, ensure that *StoragePod(Datastore clusters)*, *Datastore*, and *Folder* are selected as Associable Entities for the created category.

1. In vCenter, create a tag that uses the category created earlier.

1. Assign the previously created tag to each datastore that will be made available to the storage class. Make sure that datastores are shared with hosts participating in the OpenShift Container Platform cluster.

1. In vCenter, from the main menu, click *Policies and Profiles*.

1. On the *Policies and Profiles* page, in the navigation pane, click *VM Storage Policies*.

1. Click *CREATE*.

1. Type a name for the storage policy.

1. Select *Enable host based rules* and *Enable tag based placement rules*.

1. In the *Next* tab:

.. Select *Encryption* and *Default Encryption Properties*.

.. Select the tag category created earlier, and select tag selected. Verify that the policy is selecting matching datastores.

1. Create the storage policy.

1. Create a storage class that uses the storage policy:
```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
 name:  csi-encrypted  
provisioner: csi.vsphere.vmware.com
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
parameters:
 storagePolicyName: <storage-policy-name> <1>
```
<1> Name of the storage policy that you created for encryption