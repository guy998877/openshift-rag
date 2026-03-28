# Persistent volume formatting

You can use unformatted Cinder volumes as PVs because
OpenShift Container Platform formats them before the first use.

Before OpenShift Container Platform mounts the volume and passes it to a container, the system checks that it contains a file system as specified by the `fsType` parameter in the
PV definition. If the device is not formatted with the file system, all data from the device is erased and the device is automatically formatted with the given file system.