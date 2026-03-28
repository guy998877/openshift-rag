# About adding devices to a volume group

The `deviceSelector` field in the `LVMCluster` CR contains the configuration to specify the paths to the devices that you want to add to the Logical Volume Manager (LVM) volume group.

You can specify the device paths in the `deviceSelector.paths` field, the `deviceSelector.optionalPaths` field, or both. If you do not specify the device paths in both the `deviceSelector.paths` field and the `deviceSelector.optionalPaths` field, LVM Storage adds the supported unused devices to the volume group (VG). 

> **IMPORTANT:** It is recommended to avoid referencing disks using symbolic naming, such as `/dev/sdX`, as these names may change across reboots within RHCOS. Instead, you must use stable naming schemes, such as `/dev/disk/by-path/` or `/dev/disk/by-id/`, to ensure consistent disk identification. With this change, you might need to adjust existing automation workflows in the cases where monitoring collects information about the install device for each node. For more information, see the link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_file_systems/assembly_overview-of-persistent-naming-attributes_managing-file-systems[RHEL documentation].

You can add the path to the Redundant Array of Independent Disks (RAID) arrays in the `deviceSelector` field to integrate the RAID arrays with LVM Storage. You can create the RAID array by using the `mdadm` utility. LVM Storage does not support creating a software RAID.

> **NOTE:** You can create a RAID array only during an OpenShift Container Platform installation. For information on creating a RAID array, see the following sections: * "Configuring a RAID-enabled data volume" in "Additional resources". * link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_storage_devices/managing-raid_managing-storage-devices#creating-a-software-raid-on-an-installed-system_managing-raid[Creating a software RAID on an installed system] * link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_storage_devices/managing-raid_managing-storage-devices#replacing-a-failed-disk-in-raid_managing-raid[Replacing a failed disk in RAID] * link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_storage_devices/managing-raid_managing-storage-devices#repairing-raid-disks_managing-raid[Repairing RAID disks]

You can also add encrypted devices to the volume group. You can enable disk encryption on the cluster nodes during an OpenShift Container Platform installation. After encrypting a device, you can specify the path to the LUKS encrypted device in the `deviceSelector` field. For information on disk encryption, see "About disk encryption" and "Configuring disk encryption and mirroring".

The devices that you want to add to the VG must be supported by LVM Storage. For information about unsupported devices, see "Devices not supported by LVM Storage".

LVM Storage adds the devices to the VG only if the following conditions are met:

- The device path exists.
- The device is supported by LVM Storage. 

> **IMPORTANT:** After a device is added to the VG, you cannot remove the device. ==== LVM Storage supports dynamic device discovery. If you do not add the `deviceSelector` field in the `LVMCluster` CR, LVM Storage automatically adds the new devices to the VG when the devices are available. [WARNING]
It is not recommended to add the devices to the VG through dynamic device discovery due to the following reasons:

- When you add a new device that you do not intend to add to the VG, LVM Storage automatically adds this device to the VG through dynamic device discovery.
- If LVM Storage adds a device to the VG through dynamic device discovery, LVM Storage does not restrict you from removing the device from the node. Removing or updating the devices that are already added to the VG can disrupt the VG. This can also lead to data loss and necessitate manual node remediation.