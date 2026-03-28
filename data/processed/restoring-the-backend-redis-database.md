//included in restoring-3scale-api-management-by-using-oadp assembly

# Restoring the back-end Redis database

You can restore the back-end Redis database by deleting the deployment and specifying which resources you do not want to restore.

.Prerequisites

- You restored the Red Hat 3scale API Management operator resources, `Secret`, and APIManager custom resources.
- You restored the MySQL database.

.Procedure

1. Delete the `backend-redis` deployment by running the following command:
```bash
$ oc delete deployment backend-redis -n threescale
```
.Example output
```bash
Warning: apps.openshift.io/v1 deployment is deprecated in v4.14+, unavailable in v4.10000+

deployment.apps.openshift.io "backend-redis" deleted
```

1. Create a YAML file with the following configuration to restore the Redis database:
.Example `restore-backend.yaml` file
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: restore-backend
  namespace: openshift-adp
spec:
  backupName: redis-backup <1>
  excludedResources:
    - nodes
    - events
    - events.events.k8s.io
    - backups.velero.io
    - restores.velero.io
    - resticrepositories.velero.io
    - csinodes.storage.k8s.io
    - volumeattachments.storage.k8s.io
    - backuprepositories.velero.io
  itemOperationTimeout: 1h0m0s
  restorePVs: true
```
<1> Restoring the Redis backup.

1. Restore the Redis database by running the following command:
```bash
$ oc create -f restore-backend.yaml
```
.Example output
```bash
restore.velerio.io/restore-backend created
```

.Verification

- Verify that the `PodVolumeRestore` restore is completed by running the following command:
```bash
$ oc get podvolumerestores.velero.io -n openshift-adp
```
.Example output:
```bash
NAME                    NAMESPACE    POD                     UPLOADER TYPE   VOLUME                  STATUS      TOTALBYTES   BYTESDONE   AGE
restore-backend-jmrwx   threescale   backend-redis-1-bsfmv   kopia           backend-redis-storage   Completed   76123        76123       21m
```