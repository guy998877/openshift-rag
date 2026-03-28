# Multiple vCenter support for vSphere CSI

Deploying OpenShift Container Platform across multiple vSphere vCenter clusters without shared storage for high availability can be helpful. OpenShift Container Platform v4.17, and later, supports this capability.

> **NOTE:** Multiple vCenters can only be configured *during* installation. Multiple vCenters *cannot* be configured after installation.

The maximum number of supported vCenter clusters is three.