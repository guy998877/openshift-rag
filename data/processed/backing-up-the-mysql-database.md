//included in backing-up-3scale-api-management-by-using-oadp.adoc assembly

# Backing up a MySQL database

Back up a MySQL database by creating a persistent volume claim (PVC) to store the database dump. This helps you preserve your 3scale system database data for recovery scenarios.

.Prerequisites

- You have backed up the Red Hat 3scale API Management operator. 

.Procedure

1. Create a YAML file with the following configuration for adding an additional PVC:

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: example-claim
  namespace: threescale
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: gp3-csi
  volumeMode: Filesystem
```

1. Create the additional PVC by running the following command: 
```bash
$ oc create -f ts_pvc.yml 
```

1. Attach the PVC to the system database pod by editing the `system-mysql` deployment to use the MySQL dump:
```bash
$ oc edit deployment system-mysql -n threescale
----	
+
[source,yaml]
```
  volumeMounts:
    - name: example-claim
      mountPath: /var/lib/mysqldump/data
    - name: mysql-storage
      mountPath: /var/lib/mysql/data
    - name: mysql-extra-conf
      mountPath: /etc/my-extra.d
    - name: mysql-main-conf
      mountPath: /etc/my-extra
    ...
      serviceAccount: amp
  volumes:
        - name: example-claim
          persistentVolumeClaim:
            claimName: example-claim
    ...
`claimName`:: Specifies the PVC that contains the dumped data.

1. Create a YAML file with following configuration to back up the MySQL database:

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: mysql-backup
  namespace: openshift-adp
spec:
  csiSnapshotTimeout: 10m0s
  defaultVolumesToFsBackup: true
  hooks:
    resources:
    - name: dumpdb
      pre:
      - exec:
          command:
          - /bin/sh
          - -c
          - mysqldump -u $MYSQL_USER --password=$MYSQL_PASSWORD system --no-tablespaces
            > /var/lib/mysqldump/data/dump.sql
          container: system-mysql
          onError: Fail
          timeout: 5m
  includedNamespaces:
  - threescale
  includedResources:
  - deployment
  - pods
  - replicationControllers
  - persistentvolumeclaims
  - persistentvolumes
  itemOperationTimeout: 1h0m0s
  labelSelector:
    matchLabels:
      app: 3scale-api-management
      threescale_component_element: mysql
  snapshotMoveData: false
  ttl: 720h0m0s
```
where:
`mysql-backup`:: Specifies the value of the `metadata.name` parameter in the backup. Use this value in the `metadata.backupName` parameter when restoring the MySQL database.
`/var/lib/mysqldump/data/dump.sql`:: Specifies the directory where the data is backed up.
`includedResources`:: Specifies the resources to back up.

1. Back up the MySQL database by running the following command:
```bash
$ oc create -f mysql.yaml
```
.Example output

```bash
backup.velero.io/mysql-backup created
```

.Verification

- Verify that the MySQL backup is completed by running the following command:
```bash
$ oc get backups.velero.io mysql-backup -o yaml
```
.Example output

```bash
status:
completionTimestamp: "2025-04-17T13:25:19Z"
errors: 1
expiration: "2025-05-17T13:25:16Z"
formatVersion: 1.1.0
hookStatus: {}
phase: Completed
progress: {}
startTimestamp: "2025-04-17T13:25:16Z"
version: 1
```