# Creating profiles for different credentials

If your backup and snapshot locations use different credentials, you create separate profiles in the `credentials-velero` file.

Then, you create a `Secret` object and specify the profiles in the `DataProtectionApplication` custom resource (CR).

.Procedure

1. Create a `credentials-velero` file with separate profiles for the backup and snapshot locations, as in the following example:
```bash
[backupStorage]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>

[volumeSnapshot]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
```

1. Create a `Secret` object with the `credentials-velero` file:
```bash
$ oc create secret generic {credentials} -n openshift-adp --from-file cloud=credentials-velero <1>
```

1. Add the profiles to the `DataProtectionApplication` CR, as in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: <dpa_sample>
  namespace: openshift-adp
spec:
...
  backupLocations:
    - name: default
      velero:
        provider: {provider}
        default: true
        objectStorage:
          bucket: <bucket_name>
          prefix: <prefix>
        config:
          region: us-east-1
          profile: "backupStorage"
        credential:
          key: cloud
          name: {credentials}
  snapshotLocations:
    - velero:
        provider: {provider}
        config:
          region: us-west-2
          profile: "volumeSnapshot"
```