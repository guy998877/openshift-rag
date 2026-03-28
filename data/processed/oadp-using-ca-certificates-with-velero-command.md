// Module included in the following assemblies:
//
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-azure.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-gcp.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-mcg.adoc
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-ocs.adoc

# Using CA certificates with the velero command aliased for Velero deployment

You might want to use the Velero CLI without installing it locally on your system by creating an alias for it.

.Prerequisites

- You must be logged in to the OpenShift Container Platform cluster as a user with the `cluster-admin` role.
- You must have the OpenShift CLI (`oc`) installed.

.Procedure

1. To use an aliased Velero command, run the following command:
```bash
$ alias velero='oc -n openshift-adp exec deployment/velero -c velero -it -- ./velero'
```

1. Check that the alias is working by running the following command:
```bash
$ velero version
```
```bash
Client:
	Version: v1.12.1-OADP
	Git commit: -
Server:
	Version: v1.12.1-OADP
```

1. To use a CA certificate with this command, you can add a certificate to the Velero deployment by running the following commands:
```bash
$ CA_CERT=$(oc -n openshift-adp get dataprotectionapplications.oadp.openshift.io <dpa-name> -o jsonpath='{.spec.backupLocations[0].velero.objectStorage.caCert}')
```
```bash
$ [[ -n $CA_CERT ]] && echo "$CA_CERT" | base64 -d | oc exec -n openshift-adp -i deploy/velero -c velero -- bash -c "cat > /tmp/your-cacert.txt" || echo "DPA BSL has no caCert"
```
```bash
$ velero describe backup <backup_name> --details --cacert /tmp/<your_cacert>.txt
```

1. To fetch the backup logs, run the following command:
```bash
$ velero backup logs  <backup_name>  --cacert /tmp/<your_cacert.txt>
```
You can use these logs to view failures and warnings for the resources that you cannot back up.

1. If the Velero pod restarts, the `/tmp/your-cacert.txt` file disappears, and you must re-create the `/tmp/your-cacert.txt` file by re-running the commands from the previous step.

1. You can check if the `/tmp/your-cacert.txt` file still exists, in the file location where you stored it, by running the following command:
```bash
$ oc exec -n openshift-adp -i deploy/velero -c velero -- bash -c "ls /tmp/your-cacert.txt"
/tmp/your-cacert.txt
```
In a future release of OpenShift API for Data Protection (OADP), we plan to mount the certificate to the Velero pod so that this step is not required.