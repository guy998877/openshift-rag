# Backing up pod volumes by using the opt-in method

You can use the opt-in method to specify which volumes need to be backed up by File System Backup (FSB). You can do this by using the `backup.velero.io/backup-volumes` command.

.Procedure

- On each pod that contains one or more volumes that you want to back up, enter the following command:
```bash
$ oc -n <your_pod_namespace> annotate pod/<your_pod_name> \
  backup.velero.io/backup-volumes=<your_volume_name_1>, \ <your_volume_name_2>>,...,<your_volume_name_n>
```
where:

`<your_volume_name_x>`:: specifies the name of the xth volume in the pod specification.