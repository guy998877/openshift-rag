# Deleting a backup by creating a DeleteBackupRequest CR

You can delete a backup by creating a `DeleteBackupRequest` custom resource (CR).

.Prerequisites

- You have run a backup of your application.

.Procedure

1. Create a `DeleteBackupRequest` CR manifest file:
```yaml
apiVersion: velero.io/v1
kind: DeleteBackupRequest
metadata:
  name: deletebackuprequest
  namespace: openshift-adp
spec:
  backupName: <backup_name> # <1>
```
<1> Specify the name of the backup.

1. Apply the `DeleteBackupRequest` CR to delete the backup:
```bash
$ oc apply -f <deletebackuprequest_cr_filename> 
```