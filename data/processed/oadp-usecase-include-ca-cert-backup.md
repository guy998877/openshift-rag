# Backing up an application and its self-signed CA certificate

The `s3.openshift-storage.svc` service, provided by ODF, uses a Transport Layer Security protocol (TLS) certificate that is signed with the self-signed service CA.

To prevent a `certificate signed by unknown authority` error, you must include a self-signed CA certificate in the backup storage location (BSL) section of `DataProtectionApplication` custom resource (CR). For this situation, you must complete the following tasks:

- Request a NooBaa bucket by creating an object bucket claim (OBC).
- Extract the bucket details.
- Include a self-signed CA certificate in the `DataProtectionApplication` CR.
- Back up an application.

.Prerequisites

- You installed the OADP Operator.
- You installed the ODF Operator.
- You have an application with a database running in a separate namespace.

.Procedure

1. Create an OBC manifest to request a NooBaa bucket as shown in the following example:
```yaml
apiVersion: objectbucket.io/v1alpha1
kind: ObjectBucketClaim
metadata:
  name: test-obc
  namespace: openshift-adp
spec:
  storageClassName: openshift-storage.noobaa.io
  generateBucketName: test-backup-bucket
```
where:
`test-obc`:: Specifies the name of the object bucket claim.
`test-backup-bucket`:: Specifies the name of the bucket.

1. Create the OBC by running the following command:
```bash
$ oc create -f <obc_file_name>
```

1. When you create an OBC, ODF creates a `secret` and a `ConfigMap` with the same name as the object bucket claim. The `secret` object contains the bucket credentials, and the `ConfigMap` object contains information to access the bucket. To get the bucket name and bucket host from the generated config map, run the following command:
```bash
$ oc extract --to=- cm/test-obc
```
`test-obc` is the name of the OBC.
.Example output
```bash
# BUCKET_NAME
backup-c20...41fd
# BUCKET_PORT
443
# BUCKET_REGION

# BUCKET_SUBREGION

# BUCKET_HOST
s3.openshift-storage.svc
```

1. To get the bucket credentials from the `secret` object, run the following command:
```bash
$ oc extract --to=- secret/test-obc
```
.Example output
```bash
# AWS_ACCESS_KEY_ID
ebYR....xLNMc
# AWS_SECRET_ACCESS_KEY
YXf...+NaCkdyC3QPym
```

1. Create a `cloud-credentials` file with the object bucket credentials by using the following example configuration:
```bash
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```

1. Create the `cloud-credentials` secret with the `cloud-credentials` file content by running the following command:
```bash
$ oc create secret generic \
  cloud-credentials \
  -n openshift-adp \
  --from-file cloud=cloud-credentials
```

1. Extract the service CA certificate from the `openshift-service-ca.crt` config map by running the following command. Ensure that you encode the certificate in `Base64` format and note the value to use in the next step.
```bash
$ oc get cm/openshift-service-ca.crt \
  -o jsonpath='{.data.service-ca\.crt}' | base64 -w0; echo
```
.Example output
```bash
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0...
....gpwOHMwaG9CRmk5a3....FLS0tLS0K
```

1. Configure the `DataProtectionApplication` CR manifest file with the bucket name and CA certificate as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: oadp-backup
  namespace: openshift-adp
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: kopia
    velero:
      defaultPlugins:
        - aws
        - openshift
        - csi
      defaultSnapshotMoveData: true
  backupLocations:
    - velero:
        config:
          profile: "default"
          region: noobaa
          s3Url: https://s3.openshift-storage.svc
          s3ForcePathStyle: "true"
          insecureSkipTLSVerify: "false"
        provider: aws
        default: true
        credential:
          key: cloud
          name:  cloud-credentials
        objectStorage:
          bucket: <bucket_name>
          prefix: oadp
          caCert: <ca_cert>
```
where:
`insecureSkipTLSVerify`:: Specifies whether SSL/TLS security is enabled. If set to `true`, SSL/TLS security is disabled. If set to `false`, SSL/TLS security is enabled.
`<bucket_name>`:: Specifies the name of the bucket extracted in an earlier step.
`<ca_cert>`:: Specifies the `Base64` encoded certificate from the previous step.

1. Create the `DataProtectionApplication` CR by running the following command:
```bash
$ oc apply -f <dpa_filename>
```

1. Verify that the `DataProtectionApplication` CR is created successfully by running the following command:
```bash
$ oc get dpa -o yaml
```
.Example output
```yaml
apiVersion: v1
items:
- apiVersion: oadp.openshift.io/v1alpha1
  kind: DataProtectionApplication
  metadata:
    namespace: openshift-adp
    #...#
  spec:
    backupLocations:
    - velero:
        config:
          #...#
  status:
    conditions:
    - lastTransitionTime: "20....9:54:02Z"
      message: Reconcile complete
      reason: Complete
      status: "True"
      type: Reconciled
kind: List
metadata:
  resourceVersion: ""
```

1. Verify that the backup storage location (BSL) is available by running the following command:
```bash
$ oc get backupstoragelocations.velero.io -n openshift-adp
```
.Example output
```bash
NAME           PHASE       LAST VALIDATED   AGE   DEFAULT
dpa-sample-1   Available   3s               15s   true
```

1. Configure the `Backup` CR by using the following example:
```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: test-backup
  namespace: openshift-adp
spec:
  includedNamespaces:
  - <application_namespace>
```
where:
`<application_namespace>`:: Specifies the namespace for the application to back up.

1. Create the `Backup` CR by running the following command:
```bash
$ oc apply -f <backup_cr_filename>
```

.Verification

- Verify that the `Backup` object is in the `Completed` phase by running the following command:
```bash
$ oc describe backup test-backup -n openshift-adp
```
.Example output
```bash
Name:         test-backup
Namespace:    openshift-adp
# ....#
Status:
  Backup Item Operations Attempted:  1
  Backup Item Operations Completed:  1
  Completion Timestamp:              2024-09-25T10:17:01Z
  Expiration:                        2024-10-25T10:16:31Z
  Format Version:                    1.1.0
  Hook Status:
  Phase:  Completed
  Progress:
    Items Backed Up:  34
    Total Items:      34
  Start Timestamp:    2024-09-25T10:16:31Z
  Version:            1
Events:               <none>
```