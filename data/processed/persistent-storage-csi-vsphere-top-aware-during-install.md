# Creating vSphere storage topology during installation

## Procedure

- Specify the topology during installation. See the _Configuring regions and zones for a VMware vCenter_ section.

No additional action is necessary and the default storage class that is created by OpenShift Container Platform
is topology aware and should allow provisioning of volumes in different failure domains.