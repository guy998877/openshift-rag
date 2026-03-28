# Dynamic provisioning

Dynamic provisioning of persistent storage depends on the capabilities of
the CSI driver and underlying storage back end. The provider of the CSI
driver should document how to create a storage class in OpenShift Container Platform and
the parameters available for configuration.

The created storage class can be configured to enable dynamic provisioning.

.Procedure

- Create a default storage class that ensures all PVCs that do not require
any special storage class are provisioned by the installed CSI driver.
```shell
# oc create -f - << EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: <storage-class> <1>
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: <provisioner-name> <2>
parameters:
  csi.storage.k8s.io/fstype: xfs  <3>
EOF
```
<1> The name of the storage class that will be created.
<2> The name of the CSI driver that has been installed.
<3> The vSphere CSI driver supports all of the file systems supported by the underlying Red Hat Core operating system release, including XFS and Ext4.