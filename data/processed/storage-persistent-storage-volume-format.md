# Volume format

Before OpenShift Container Platform mounts the volume and passes it to a container, it checks that the volume contains a file system as specified by the `fsType` arameter in the persistent volume definition. If the device is not formatted with the file system, all data from the device is erased and the device is automatically formatted with the given file system.

This verification enables you to use unformatted {provider} volumes as persistent volumes, because OpenShift Container Platform formats them before the first use.

// Undefined {provider} attribute, so that any mistakes are easily spotted
:!provider: