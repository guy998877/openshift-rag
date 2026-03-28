# Troubleshooting issue where backup CR cannot retrieve volume

Resolve the `InvalidVolume.NotFound` error that occurs when the persistent volume (PV) and snapshot locations are in different regions. This helps you ensure the `Backup` CR can successfully retrieve volumes.

If the PV and the snapshot locations are in different regions, the `Backup` custom resource (CR) displays the following error message:

```text
InvalidVolume.NotFound: The volume vol-xxxx does not exist.
```

.Procedure

1. Edit the value of the `spec.snapshotLocations.velero.config.region` key in the `DataProtectionApplication` manifest so that the snapshot location is in the same region as the PV.

1. Create a new `Backup` CR.