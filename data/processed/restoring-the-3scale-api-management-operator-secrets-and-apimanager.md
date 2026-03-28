//included in restoring-3scale-api-management-by-using-oadp assembly

# Restoring the 3scale API Management operator, secrets, and APIManager

You can restore the Red Hat 3scale API Management operator resources, and both the `Secret` and APIManager custom resources (CRs) by using the following procedure.

.Prerequisites

- You backed up the 3scale operator.
- You backed up the MySQL and Redis databases.
- You are restoring the database on the same cluster, where it was backed up. 
If you are restoring the operator to a different cluster that you backed up from, install and configure OADP with `nodeAgent` enabled on the destination cluster. Ensure that the OADP configuration is same as it was on the source cluster.

.Procedure

1. Delete the 3scale operator custom resource definitions (CRDs) along with the `threescale` namespace by running the following command:
```bash
$ oc delete project threescale
```
.Example output
```bash
"threescale" project deleted successfully
```

1. Create a YAML file with the following configuration to restore the 3scale operator:
.Example `restore.yaml` file
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: operator-installation-restore
  namespace: openshift-adp
spec:
  backupName: operator-install-backup <1>
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
  itemOperationTimeout: 4h0m0s
```
<1> Restoring the 3scale operator's backup

1. Restore the 3scale operator by running the following command:
```bash
$ oc create -f restore.yaml
```
.Example output
```bash
restore.velerio.io/operator-installation-restore created
```

1. Manually create the `s3-credentials` `Secret` object by running the following command:
```bash
$ oc apply -f - <<EOF
---
apiVersion: v1
kind: Secret
metadata:
      name: s3-credentials
      namespace: threescale
stringData:
  AWS_ACCESS_KEY_ID: <ID_123456> <1>
  AWS_SECRET_ACCESS_KEY: <ID_98765544> <2>
  AWS_BUCKET: <mybucket.example.com> <3>
  AWS_REGION: <us-east-1> <4>
type: Opaque
EOF
```
<1> Replace <ID_123456> with your AWS credentials ID.
<2> Replace <ID_98765544> with your AWS credentials KEY.
<3> Replace <mybucket.example.com> with your target bucket name.
<4> Replace <us-east-1> with the AWS region of your bucket.

1. Scale down the 3scale operator by running the following command:
```bash
$ oc scale deployment threescale-operator-controller-manager-v2 --replicas=0 -n threescale
```
.Example output
```bash
deployment.apps/threescale-operator-controller-manager-v2 scaled
```

1. Create a YAML file with the following configuration to restore the `Secret`:
.Example `restore-secret.yaml` file
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: operator-resources-secrets
  namespace: openshift-adp
spec:
  backupName: operator-resources-secrets <1>
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
  itemOperationTimeout: 4h0m0s
```
<1> Restoring the `Secret` backup.

1. Restore the `Secret` by running the following command:
```bash
$ oc create -f restore-secrets.yaml
```
.Example output
```bash
restore.velerio.io/operator-resources-secrets created
```

1. Create a YAML file with the following configuration to restore APIManager:
.Example `restore-apimanager.yaml` file
```yaml
apiVersion: velero.io/v1
kind: Restore
metadata:
  name: operator-resources-apim
  namespace: openshift-adp
spec:
  backupName: operator-resources-apim <1>
  excludedResources: <2>
  - nodes
  - events
  - events.events.k8s.io
  - backups.velero.io
  - restores.velero.io
  - resticrepositories.velero.io
  - csinodes.storage.k8s.io
  - volumeattachments.storage.k8s.io
  - backuprepositories.velero.io
  itemOperationTimeout: 4h0m0s
```
<1> Restoring the APIManager backup.
<2> The resources that you do not want to restore.

1. Restore the APIManager by running the following command:
```bash
$ oc create -f restore-apimanager.yaml
```
.Example output
```bash
restore.velerio.io/operator-resources-apim created
```

1. Scale up the 3scale operator by running the following command:
```bash
$ oc scale deployment threescale-operator-controller-manager-v2 --replicas=1 -n threescale
```
.Example output
```bash
deployment.apps/threescale-operator-controller-manager-v2 scaled
```