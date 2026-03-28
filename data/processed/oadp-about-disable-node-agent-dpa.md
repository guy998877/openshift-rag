// Module included in the following assemblies:
//
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-azure.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-gcp.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-mcg.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-ocs.adoc

# Disabling the node agent in DataProtectionApplication

If you are not using `Restic`, `Kopia`, or `DataMover` for your backups, you can disable the `nodeAgent` field in the `DataProtectionApplication` custom resource (CR). Before you disable `nodeAgent`, ensure the OADP Operator is idle and not running any backups.

.Procedure

1. To disable the `nodeAgent`, set the `enable` flag to `false`. See the following example:
.Example `DataProtectionApplication` CR
```yaml
# ...
configuration:
  nodeAgent:
    enable: false
    uploaderType: kopia
# ...
```
where:
`enable`:: Enables the node agent.

1. To enable the `nodeAgent`, set the `enable` flag to `true`. See the following example:
.Example `DataProtectionApplication` CR
```yaml
# ...
configuration:
  nodeAgent:
    enable: true
    uploaderType: kopia
# ...
```
where:
`enable`:: Enables the node agent.
You can set up a job to enable and disable the `nodeAgent` field in the `DataProtectionApplication` CR. For more information, see "Running tasks in pods using jobs".