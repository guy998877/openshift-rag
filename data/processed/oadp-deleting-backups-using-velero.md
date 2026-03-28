# Deleting a backup by using the Velero CLI

You can delete a backup by using the Velero CLI.

.Prerequisites

- You have run a backup of your application.
- You downloaded the Velero CLI and can access the Velero binary in your cluster.

.Procedure

- To delete the backup, run the following Velero command:
```bash
$ velero backup delete <backup_name> -n openshift-adp <1>
```
<1> Specify the name of the backup.