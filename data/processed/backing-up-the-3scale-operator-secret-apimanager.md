//included in backing-up-3scale-api-management-by-using-oadp.adoc assembly

# Backing up the 3scale API Management operator, secret, and APIManager

Back up the Red Hat 3scale API Management operator resources, including the `Secret` and APIManager custom resources (CRs), by creating backup CRs. This helps you preserve your 3scale operator configuration for recovery scenarios.

.Prerequisites

- You created the Data Protection Application (DPA). 

.Procedure

1. Back up your 3scale operator CRs, such as `operatorgroup`, `namespaces`, and `subscriptions`, by creating a YAML file with the following configuration: 

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: operator-install-backup
  namespace: openshift-adp
spec:
  csiSnapshotTimeout: 10m0s
  defaultVolumesToFsBackup: false
  includedNamespaces:
  - threescale
  includedResources:
  - operatorgroups
  - subscriptions
  - namespaces
  itemOperationTimeout: 1h0m0s
  snapshotMoveData: false
  ttl: 720h0m0s
```
where:
`operator-install-backup`:: Specifies the value of the `metadata.name` parameter in the backup. This is the same value used in the `metadata.backupName` parameter used when restoring the 3scale operator.
`threescale`:: Specifies the namespace where the 3scale operator is installed.
> **NOTE:** You can also back up and restore `ReplicationControllers`, `Deployment`, and `Pod` objects to ensure that all manually set environments are backed up and restored. This does not affect the flow of restoration.

1. Create a backup CR by running the following command:
```bash
$ oc create -f backup.yaml
```
.Example output

```bash
backup.velero.io/operator-install-backup created
```

1. Back up the `Secret` CR by creating a YAML file with the following configuration:

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: operator-resources-secrets
  namespace: openshift-adp
spec:
  csiSnapshotTimeout: 10m0s
  defaultVolumesToFsBackup: false
  includedNamespaces:
  - threescale
  includedResources:
  - secrets
  itemOperationTimeout: 1h0m0s
  labelSelector:
    matchLabels:
      app: 3scale-api-management
  snapshotMoveData: false
  snapshotVolumes: false
  ttl: 720h0m0s
```
`name`:: Specifies the value of the `metadata.name` parameter in the backup. Use this value in the `metadata.backupName` parameter when restoring the `Secret`.

1. Create the `Secret` backup CR by running the following command:
```bash
$ oc create -f backup-secret.yaml
```
.Example output

```bash
backup.velero.io/operator-resources-secrets created
```

1. Back up the APIManager CR by creating a YAML file with the following configuration:

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: operator-resources-apim
  namespace: openshift-adp
spec:
  csiSnapshotTimeout: 10m0s
  defaultVolumesToFsBackup: false
  includedNamespaces:
  - threescale
  includedResources:
  - apimanagers
  itemOperationTimeout: 1h0m0s
  snapshotMoveData: false
  snapshotVolumes: false
  storageLocation: ts-dpa-1
  ttl: 720h0m0s
  volumeSnapshotLocations:
  - ts-dpa-1
```
`name`:: Specifies the value of the `metadata.name` parameter in the backup. Use this value in the `metadata.backupName` parameter when restoring the APIManager.

1. Create the APIManager CR by running the following command:
```bash
$ oc create -f backup-apimanager.yaml
```
.Example output

```bash
backup.velero.io/operator-resources-apim created
```