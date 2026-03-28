# Previewing resources before running backup and restore

OADP backs up application resources based on the type, namespace, or label. This means that you can view the resources after the backup is complete. Similarly, you can view the restored objects based on the namespace, persistent volume (PV), or label after a restore operation is complete. To preview the resources in advance, you can do a dry run of the backup and restore operations.

.Prerequisites

- You have installed the OADP Operator.

.Procedure

1. To preview the resources included in the backup before running the actual backup, run the following command:
```bash
$ velero backup create <backup-name> --snapshot-volumes false # <1>
```
<1> Specify the value of `--snapshot-volumes` parameter as `false`.
1. To know more details about the backup resources, run the following command:
```bash
$ velero describe backup <backup_name> --details # <1>
```
<1> Specify the name of the backup.
1. To preview the resources included in the restore before running the actual restore, run the following command:
```bash
$ velero restore create --from-backup <backup-name> # <1>
```
<1> Specify the name of the backup created to review the backup resources.
> **IMPORTANT:** The `velero restore create` command creates restore resources in the cluster. You must delete the resources created as part of the restore, after you review the resources.
1. To know more details about the restore resources, run the following command:
```bash
$ velero describe restore <restore_name> --details # <1>
```
<1> Specify the name of the restore.