# Configuring Amazon Web Services

Configure Amazon Web Services (AWS) S3 storage and Identity and Access Management (IAM) credentials for backup storage with Migration Toolkit for Containers (MTC). This provides the necessary permissions and storage infrastructure for data protection operations.
Configure Amazon Web Services (AWS) S3 storage and Identity and Access Management (IAM) credentials for backup storage with OADP. This provides the necessary permissions and storage infrastructure for data protection operations.

.Prerequisites

- You must have the link:https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html[AWS CLI] installed.
- The AWS S3 storage bucket must be accessible to the source and target clusters.
- If you are using the snapshot copy method:
- You must have access to EC2 Elastic Block Storage (EBS).
- The source and target clusters must be in the same region.
- The source and target clusters must have the same storage class.
- The storage class must be compatible with snapshots.

.Procedure

1. Set the `BUCKET` variable:
```bash
$ BUCKET=<your_bucket>
```

1. Set the `REGION` variable:
```bash
$ REGION=<your_region>
```

1. Create an AWS S3 bucket:
```bash
$ aws s3api create-bucket \
    --bucket $BUCKET \
    --region $REGION \
    --create-bucket-configuration LocationConstraint=$REGION
```
where:
`LocationConstraint`:: Specifies the bucket configuration location constraint. `us-east-1` does not support `LocationConstraint`. If your region is `us-east-1`, omit `--create-bucket-configuration LocationConstraint=$REGION`.

1. Create an IAM user:
```bash
$ aws iam create-user --user-name velero
```
where:
`velero`:: Specifies the user name. If you want to use Velero to back up multiple clusters with multiple S3 buckets, create a unique user name for each cluster.

1. Create a `velero-policy.json` file:
```bash
$ cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::${BUCKET}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource": [
                "arn:aws:s3:::${BUCKET}"
            ]
        }
    ]
}
EOF
```

1. Attach the policies to give the `velero` user the minimum necessary permissions:
```bash
$ aws iam put-user-policy \
  --user-name velero \
  --policy-name velero \
  --policy-document file://velero-policy.json
```

1. Create an access key for the `velero` user:
```bash
$ aws iam create-access-key --user-name velero
```
```bash
{
  "AccessKey": {
        "UserName": "velero",
        "Status": "Active",
        "CreateDate": "2017-07-31T22:24:41.576Z",
        "SecretAccessKey": <AWS_SECRET_ACCESS_KEY>,
        "AccessKeyId": <AWS_ACCESS_KEY_ID>
  }
}
```
Record the `AWS_SECRET_ACCESS_KEY` and the `AWS_ACCESS_KEY_ID`. You use the credentials to add AWS as a replication repository.
1. Create a `credentials-velero` file:
```bash
$ cat << EOF > ./credentials-velero
[default]
aws_access_key_id=<AWS_ACCESS_KEY_ID>
aws_secret_access_key=<AWS_SECRET_ACCESS_KEY>
EOF
```
You use the `credentials-velero` file to create a `Secret` object for AWS before you install the Data Protection Application.