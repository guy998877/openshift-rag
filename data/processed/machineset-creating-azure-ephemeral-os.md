# Creating machines on Ephemeral OS disks by using compute machine sets

You can launch machines on Ephemeral OS disks on Azure by editing your compute machine set YAML file.

.Prerequisites

- Have an existing Microsoft Azure cluster.

.Procedure

1. Edit the custom resource (CR) by running the following command:
```bash
$ oc edit machineset <machine-set-name>
```
where `<machine-set-name>` is the compute machine set that you want to provision machines on Ephemeral OS disks.

1. Add the following to the `providerSpec` field:
```yaml
providerSpec:
  value:
    ...
    osDisk:
       ...
       diskSettings: <1>
         ephemeralStorageLocation: Local <1>
       cachingType: ReadOnly <1>
       managedDisk:
         storageAccountType: Standard_LRS <2>
       ...
```
<1> These lines enable the use of Ephemeral OS disks.
<2> Ephemeral OS disks are only supported for VMs or scale set instances that use the Standard LRS storage account type.
> **IMPORTANT:** The implementation of Ephemeral OS disk support in OpenShift Container Platform only supports the `CacheDisk` placement type. Do not change the `placement` configuration setting.

1. Create a compute machine set using the updated configuration:
```bash
$ oc create -f <machine-set-config>.yaml
```

.Verification

- On the Microsoft Azure portal, review the *Overview* page for a machine deployed by the compute machine set, and verify that the `Ephemeral OS disk` field is set to `OS cache placement`.