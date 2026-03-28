# Limitations to configure the size of the devices used in LVM Storage

To ensure your devices are compatible with storage operations, review the size configuration limitations in LVM Storage. Adhering to these constraints prevents provisioning failures by ensuring selected devices meet the required capacity specifications.

When provisioning storage by using LVM Storage, the following factors limit device size:

- The total storage size that you can provision is limited by the size of the underlying Logical Volume Manager (LVM) thin pool and the over-provisioning factor.
- The size of the logical volume depends on the size of the Physical Extent (PE) and the Logical Extent (LE).
- You can define the size of PE and LE during the physical and logical device creation.
- The default PE and LE size is 4 MiB.
- If the size of the PE is increased, the maximum size of the LVM is determined by the kernel limits and your disk space.

The following tables describe the chunk size and volume size limits for static and host configurations:

.Tested configuration
[cols="1,1", width="100%", options="header"]
|====

|Parameter
|Value

|Chunk size
|128 KiB

|Maximum volume size
|32 TiB

|====

.Theoretical size limits for static configuration
[cols="1,1,1", width="100%", options="header"]
|====

|Parameter
|Minimum value
|Maximum value

|Chunk size
|64 KiB
|1 GiB

|Volume size
|Minimum size of the underlying Red Hat Enterprise Linux CoreOS (RHCOS) system.
|Maximum size of the underlying RHCOS system.

|====

.Theoretical size limits for a host configuration
[cols="1,1", width="100%", options="header"]
|====

|Parameter
|Value

|Chunk size
|This value is based on the configuration in the `lvm.conf` file. By default, the configuration sets the value to `128` KiB.

|Maximum volume size
|Equal to the maximum volume size of the underlying RHCOS system.

|Minimum volume size
|Equal to the minimum volume size of the underlying RHCOS system.

|====