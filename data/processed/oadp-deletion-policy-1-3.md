# Deletion policy for OADP 1.3

The deletion policy determines rules for removing data from a system, specifying when and how deletion occurs based on factors such as retention periods, data sensitivity, and compliance requirements. It manages data removal effectively while meeting regulations and preserving valuable information.

## Deletion policy guidelines for OADP 1.3

Review the following deletion policy guidelines for the OADP 1.3:

- In OADP 1.3.x, when using any type of backup and restore methods, you can set the `deletionPolicy` field to `Retain` or `Delete` in the `VolumeSnapshotClass` custom resource (CR).