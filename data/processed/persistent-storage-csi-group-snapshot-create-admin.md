# Creating a volume group snapshot class

Before you can create volume group snapshots, the cluster administrator needs to create a `VolumeGroupSnapshotClass`. 

This object describes how volume group snapshots should be created, including the driver information, the deletion policy, etc.

.Prerequisites
- Logged in to a running OpenShift Container Platform cluster with administrator privileges.

- Enabled this feature using feature gates. For information about how to use feature gates, see _Enabling features sets by using feature gates_.

.Procedure

To create a `VolumeGroupSnapshotClass`:

1. Create a `VolumeGroupSnapshotClass` YAML file using the following example file:
.Example volume group snapshot class YAML file
```yaml
apiVersion: groupsnapshot.storage.k8s.io/v1beta2
kind: VolumeGroupSnapshotClass <1>
metadata:
  name: csi-hostpath-groupsnapclass <2>
deletionPolicy: Delete
driver: hostpath.csi.k8s.io 
     …...
```
<1> Specifies the `VolumeGroupSnapshotClass` object.
<2> Name of the `VolumeGroupSnapshotClass`.

1. Create the 'VolumeGroupSnapshotClass' object by running the following command:
```bash
$ oc create -f <volume-group-snapshot-class-filename>.yaml
```