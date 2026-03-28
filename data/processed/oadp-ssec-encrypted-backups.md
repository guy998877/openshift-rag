// Module included in the following assemblies:
//
// * backup_and_restore/application_backup_and_restore/installing/installing-oadp-aws.adoc

# Creating an OADP SSE-C encryption key for additional data security

Configure server-side encryption with customer-provided keys (SSE-C) to add an additional layer of encryption for backup data stored in Amazon Web Services (AWS) S3. This protects backup data if AWS credentials become exposed.

Amazon Web Services (AWS) S3 applies server-side encryption with AWS S3 managed keys (SSE-S3) as the base level of encryption for every bucket in Amazon S3.

OpenShift API for Data Protection (OADP) encrypts data by using SSL/TLS, HTTPS, and the `velero-repo-credentials` secret when transferring the data from a cluster to storage. To protect backup data in case of lost or stolen AWS credentials, apply an additional layer of encryption.

The velero-plugin-for-aws plugin provides several additional encryption methods. You should review its configuration options and consider implementing additional encryption.

You can store your own encryption keys by using server-side encryption with customer-provided keys (SSE-C). This feature provides additional security if your AWS credentials become exposed.

> **WARNING:** Be sure to store cryptographic keys in a secure and safe manner. Encrypted data and backups cannot be recovered if you do not have the encryption key.

.Prerequisites

- To make OADP mount a secret that contains your SSE-C key to the Velero pod at `/credentials`, use the following default secret name for AWS: `cloud-credentials`, and leave at least one of the following labels empty:

- `dpa.spec.backupLocations[].velero.credential`
- `dpa.spec.snapshotLocations[].velero.credential`
This is a workaround for a known issue: https://issues.redhat.com/browse/OADP-3971.

> **NOTE:** The following procedure contains an example of a `spec:backupLocations` block that does not specify credentials. This example would trigger an OADP secret mounting.

- If you need the backup location to have credentials with a different name than `cloud-credentials`, you must add a snapshot location, such as the one in the following example, that does not contain a credential name. Because the following example does not contain a credential name, the snapshot location will use `cloud-credentials` as its secret for taking snapshots.
```yaml
 snapshotLocations:
  - velero:
      config:
        profile: default
        region: <region>
      provider: aws
# ...
```

.Procedure
1. Create an SSE-C encryption key:

.. Generate a random number and save it as a file named `sse.key` by running the following command:
```bash
$ dd if=/dev/urandom bs=1 count=32 > sse.key
```

1. Create an OpenShift Container Platform secret:
- If you are initially installing and configuring OADP, create the AWS credential and encryption key secret at the same time by running the following command:
```bash
$ oc create secret generic cloud-credentials --namespace openshift-adp --from-file cloud=<path>/openshift_aws_credentials,customer-key=<path>/sse.key
```
- If you are updating an existing installation, edit the values of the `cloud-credential` `secret` block of the `DataProtectionApplication` CR manifest, as in the following example:
```yaml
apiVersion: v1
data:
  cloud: W2Rfa2V5X2lkPSJBS0lBVkJRWUIyRkQ0TlFHRFFPQiIKYXdzX3NlY3JldF9hY2Nlc3Nfa2V5P<snip>rUE1mNWVSbTN5K2FpeWhUTUQyQk1WZHBOIgo=
  customer-key: v+<snip>TFIiq6aaXPbj8dhos=
kind: Secret
# ...
```
1. Edit the value of the `customerKeyEncryptionFile` attribute in the `backupLocations` block of the `DataProtectionApplication` CR manifest, as in the following example:
```yaml
spec:
  backupLocations:
    - velero:
        config:
          customerKeyEncryptionFile: /credentials/customer-key
          profile: default
# ...
```
> **WARNING:** You must restart the Velero pod to remount the secret credentials properly on an existing installation.
The installation is complete, and you can back up and restore OpenShift Container Platform resources. The data saved in AWS S3 storage is encrypted with the new key, and you cannot download it from the AWS S3 console or API without the additional encryption key.

.Verification

To verify that you cannot download the encrypted files without the inclusion of an additional key, create a test file, upload it, and then try to download it.

1. Create a test file by running the following command:
```bash
$ echo "encrypt me please" > test.txt
```
1. Upload the test file by running the following command:
```bash
$ aws s3api put-object \
  --bucket <bucket> \
  --key test.txt \
  --body test.txt \
  --sse-customer-key fileb://sse.key \
  --sse-customer-algorithm AES256
```
1. Try to download the file. In either the Amazon web console or the terminal, run the following command:
```bash
$ s3cmd get s3://<bucket>/test.txt test.txt
```
The download fails because the file is encrypted with an additional key.

1. Download the file with the additional encryption key by running the following command:
```bash
$ aws s3api get-object \
    --bucket <bucket> \
    --key test.txt \
    --sse-customer-key fileb://sse.key \
    --sse-customer-algorithm AES256 \
    downloaded.txt
```

1. Read the file contents by running the following command:
```bash
$ cat downloaded.txt
```
```bash
encrypt me please
```