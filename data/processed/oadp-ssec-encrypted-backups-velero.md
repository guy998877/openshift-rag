# Downloading a file with an SSE-C encryption key for files backed up by Velero

When you are verifying an SSE-C encryption key, you can also download the file with the additional encryption key for files that were backed up with Velero.

.Procedure

- Download the file with the additional encryption key for files backed up by Velero by running the following command:
```bash
$ aws s3api get-object \
  --bucket <bucket> \
  --key velero/backups/mysql-persistent-customerkeyencryptionfile4/mysql-persistent-customerkeyencryptionfile4.tar.gz \
  --sse-customer-key fileb://sse.key \
  --sse-customer-algorithm AES256 \
  --debug \
  velero_download.tar.gz
```