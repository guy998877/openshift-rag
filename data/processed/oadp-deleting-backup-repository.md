# Deleting a backup repository

After you delete the backup, and after the Kopia repository maintenance cycles to delete the related artifacts are complete, the backup is no longer referenced by any metadata or manifest objects. You can then delete the `backuprepository` custom resource (CR) to complete the backup deletion process.

.Prerequisites

- You have deleted the backup of your application.
- You have waited up to 72 hours after the backup is deleted. This time frame allows Kopia to run the repository maintenance cycles.

.Procedure

1. To get the name of the backup repository CR for a backup, run the following command:
```bash
$ oc get backuprepositories.velero.io -n openshift-adp
```

1. To delete the backup repository CR, run the following command:
```bash
$ oc delete backuprepository <backup_repository_name> -n openshift-adp <1>
```
<1> Specify the name of the backup repository from the earlier step.