# Deleting volume snapshots

You can delete the volume snapshots of the persistent volume claims (PVCs).
> **IMPORTANT:** When you delete a persistent volume claim (PVC), LVM Storage deletes only the PVC, but not the snapshots of the PVC.

.Prerequisites

- You have access to OpenShift Container Platform as a user with `cluster-admin` permissions.
- You have ensured that the volume snpashot that you want to delete is not in use.

.Procedure

1. Log in to the OpenShift CLI (`oc`).

1. Delete the volume snapshot by running the following command:
```bash
$ oc delete volumesnapshot <volume_snapshot_name> -n <namespace>
```

.Verification

- To verify that the volume snapshot is deleted, run the following command:
```bash
$ oc get volumesnapshot -n <namespace>
```
The deleted volume snapshot must not be present in the output of this command.