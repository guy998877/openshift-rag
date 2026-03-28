# Scaling up the storage of clusters by using RHACM

You can scale up the storage capacity of worker nodes on the clusters by using RHACM.

.Prerequisites

- You have access to the RHACM cluster using an account with `cluster-admin` privileges.
- You have created an `LVMCluster` custom resource (CR) by using RHACM.
- You have additional unused devices on each cluster to be used by Logical Volume Manager (LVM) Storage.

.Procedure

1. Log in to the RHACM CLI using your OpenShift Container Platform credentials.
1. Edit the `LVMCluster` CR that you created using RHACM by running the following command:
```bash
$ oc edit -f <file_name> -n <namespace> <1>
```
<1> Replace `<file_name>` with the name of the `LVMCluster` CR.

1. In the `LVMCluster` CR, add the path to the new device in the `deviceSelector` field.
.Example `LVMCluster` CR
```yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: lvms
spec:
  object-templates:
     - complianceType: musthave
       objectDefinition:
         apiVersion: lvm.topolvm.io/v1alpha1
         kind: LVMCluster
         metadata:
           name: my-lvmcluster
           namespace: openshift-lvm-storage
         spec:
           storage:
             deviceClasses:
# ...
               deviceSelector: <1>
                 paths: <2>
                 - /dev/disk/by-path/pci-0000:87:00.0-nvme-1
                 optionalPaths: <3>
                 - /dev/disk/by-path/pci-0000:89:00.0-nvme-1
# ...
```
<1> Contains the configuration to specify the paths to the devices that you want to add to the LVM volume group.
You can specify the device paths in the `paths` field, the `optionalPaths` field, or both. If you do not specify the device paths in both `paths` and `optionalPaths`, Logical Volume Manager (LVM) Storage adds the supported unused devices to the LVM volume group. LVM Storage adds the devices to the LVM volume group only if the following conditions are met:
- The device path exists.
- The device is supported by LVM Storage. For information about unsupported devices, see "Devices not supported by LVM Storage".
<2> Specify the device paths. If the device path specified in this field does not exist, or the device is not supported by LVM Storage, the `LVMCluster` CR moves to the `Failed` state.
<3> Specify the optional device paths. If the device path specified in this field does not exist, or the device is not supported by LVM Storage, LVM Storage ignores the device without causing an error. 
> **IMPORTANT:** After a device is added to the LVM volume group, it cannot be removed.

1. Save the `LVMCluster` CR.