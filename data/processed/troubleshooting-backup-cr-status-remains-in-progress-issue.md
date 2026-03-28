# Troubleshooting issue where backup CR status remains in progress

Resolve the issue where an interrupted backup causes the `Backup` CR status to remain in the `InProgress` phase. This helps you clear stalled backups and create new ones to complete your backup operations.

.Procedure

1. Retrieve the details of the `Backup` CR by running the following command:
```bash
$ oc -n {namespace} exec deployment/velero -c velero -- ./velero \
  backup describe <backup>
```

1. Delete the `Backup` CR by running the following command:
```bash
$ oc delete backups.velero.io <backup> -n openshift-adp
```
You do not need to clean up the backup location because an in progress `Backup` CR has not uploaded files to object storage.

1. Create a new `Backup` CR.

1. View the Velero backup details by running the following command:
```bash
$ velero backup describe <backup_name> --details
```