# Limitations

Performance plus for Azure Disk has the following limitations:

- Can be enabled only on Standard HDD, Standard SSD, and Premium SSD managed disks that are 513 GiB or larger.
> **IMPORTANT:** If you request a smaller value, the disk size is rounded up to 513GiB.

- Can be enabled only on new disks. For a workaround, see Section _Enabling performance plus by snapshot or cloning_.