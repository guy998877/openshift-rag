[id=storage-class-mapping-oadp_{context}]
# Mapping storage classes with OADP

You can use OpenShift API for Data Protection (OADP)  with the Velero plugin v1.1.0 and later to change the storage class of a persistent volume (PV) during restores, by configuring a storage class mapping in the config map in the Velero namespace.

To deploy ConfigMap with OADP, use the `change-storage-class-config` field. You must change the storage class mapping based on your cloud provider.

.Procedure
1. Change the storage class mapping by running the following command:
```bash
$ cat change-storageclass.yaml
```
1. Create a config map in the Velero namespace as shown in the following example:
.Example
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: change-storage-class-config
  namespace: openshift-adp
  labels:
    velero.io/plugin-config: ""
    velero.io/change-storage-class: RestoreItemAction
data:
  standard-csi: ssd-csi
```
1. Save your storage class mapping preferences by running the following command:
```bash
$ oc create -f change-storage-class-config
```