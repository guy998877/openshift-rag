# Increasing the maximum allowable volumes per node for vSphere

.Prerequisites
- Access to the OpenShift Container Platform web console.

- Access to the cluster as a user with the cluster-admin role.

- Access to VMware vSphere vCenter.

- In vCenter, ensure that the parameter `pvscsiCtrlr256DiskSupportEnabled` is set to 'True'. 
> **IMPORTANT:** Changing the `pvscsiCtrlr256DiskSupportEnabled` parameter is not fully supported by VMware. Also, the parameter is a cluster-wide option.

.Procedure

Use the following procedure to increase the maximum number of volumes per node for vSphere:

1. Click *Administration* > *CustomResourceDefinitions*.

1. On the *CustomResourceDefinitions* page next to the *Name* dropdown box, type "clustercsidriver".

1. Click *CRD ClusterCSIDriver*.

1. Click the *Instances* tab.

1. Click *csi.vsphere.vmware.com*.

1. Click the *YAML* tab.

1. Set the parameter `spec.driverConfig.driverType` to `vSphere`.

1. Add the parameter `spec.driverConfig.vSphere.maxAllowedBlockVolumesPerNode` to the YAML file, and provide a value for the desired maximum number of volumes per node as in the following sample YAML file:
```yaml
.Sample YAML file for adding the parameter maxAllowedBlockVolumesPerNode
```
...
spec:
  driverConfig:
    driverType: vSphere
    vSphere:
      maxAllowedBlockVolumesPerNode: <1>
...
<1> Enter the desired value here for the maximum number of volumes per node. The default is 59. The minimum value is 1 and the maximum value is 255.

1. Click *Save*.