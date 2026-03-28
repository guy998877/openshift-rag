# Using datastore URL

.Procedure

To encrypt using the datastore URL:

1. Find out the name of the default storage policy in your datastore that supports encryption. 
This is same policy that was used for encrypting your VMs. 

1. Create a storage class that uses this storage policy:
```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
 name: encryption
provisioner: csi.vsphere.vmware.com
parameters:
 storagePolicyName: <storage-policy-name> <1>
 datastoreurl: "ds:///vmfs/volumes/vsan:522e875627d-b090c96b526bb79c/"
```
<1> Name of default storage policy in your datastore that supports encryption