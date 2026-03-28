# Preparing AWS credentials for OADP

An Amazon Web Services account must be prepared and configured to accept an OpenShift API for Data Protection (OADP) installation.

.Procedure

1. Create the following environment variables by running the following commands:
> **IMPORTANT:** Change the cluster name to match your cluster, and ensure you are logged into the cluster as an administrator. Ensure that all fields are outputted correctly before continuing.
```bash
$ export CLUSTER_NAME=my-cluster
```
--
- `my-cluster`: Replace `my-cluster` with your cluster name.
--
```bash
$ export ROSA_CLUSTER_ID=$(rosa describe cluster -c ${CLUSTER_NAME} --output json | jq -r .id)
```
```bash
$ export REGION=$(rosa describe cluster -c ${CLUSTER_NAME} --output json | jq -r .region.id)
```
```bash
$ export OIDC_ENDPOINT=$(oc get authentication.config.openshift.io cluster -o jsonpath='{.spec.serviceAccountIssuer}' | sed 's|^https://||')
```
```bash
$ export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```
```bash
$ export CLUSTER_VERSION=$(rosa describe cluster -c ${CLUSTER_NAME} -o json | jq -r .version.raw_id | cut -f -2 -d '.')
```
```bash
$ export ROLE_NAME="${CLUSTER_NAME}-openshift-oadp-aws-cloud-credentials"
```
```bash
$ export SCRATCH="/tmp/${CLUSTER_NAME}/oadp"
```
```bash
$ mkdir -p ${SCRATCH}
```
```bash
$ echo "Cluster ID: ${ROSA_CLUSTER_ID}, Region: ${REGION}, OIDC Endpoint:
  ${OIDC_ENDPOINT}, AWS Account ID: ${AWS_ACCOUNT_ID}"
```

1. On the AWS account, create an IAM policy to allow access to AWS S3:
.. Check to see if the policy exists by running the following command:
```bash
$ POLICY_ARN=$(aws iam list-policies --query "Policies[?PolicyName=='RosaOadpVer1'].{ARN:Arn}" --output text)
```
--
- `RosaOadp`: Replace `RosaOadp` with your policy name.
--
..  Enter the following command to create the policy JSON file and then create the policy:
> **NOTE:** If the policy ARN is not found, the command creates the policy. If the policy ARN already exists, the `if` statement intentionally skips the policy creation.
```bash
$ if [[ -z "${POLICY_ARN}" ]]; then
  cat << EOF > ${SCRATCH}/policy.json
  {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:PutBucketTagging",
        "s3:GetBucketTagging",
        "s3:PutEncryptionConfiguration",
        "s3:GetEncryptionConfiguration",
        "s3:PutLifecycleConfiguration",
        "s3:GetLifecycleConfiguration",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucketMultipartUploads",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts",
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:DescribeVolumeAttribute",
        "ec2:DescribeVolumesModifications",
        "ec2:DescribeVolumeStatus",
        "ec2:CreateTags",
        "ec2:CreateVolume",
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    }
  ]}
EOF

  POLICY_ARN=$(aws iam create-policy --policy-name "RosaOadpVer1" \
  --policy-document file:///${SCRATCH}/policy.json --query Policy.Arn \
  --tags Key=rosa_openshift_version,Value=${CLUSTER_VERSION} Key=rosa_role_prefix,Value=ManagedOpenShift Key=operator_namespace,Value=openshift-oadp Key=operator_name,Value=openshift-oadp \
  --output text)
  fi
```
--
- `SCRATCH`: `SCRATCH` is a name for a temporary directory created for the environment variables.
--
.. View the policy ARN by running the following command:
```bash
$ echo ${POLICY_ARN}
```

1. Create an IAM role trust policy for the cluster:
.. Create the trust policy file by running the following command:
```bash
$ cat <<EOF > ${SCRATCH}/trust-policy.json
  {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_ENDPOINT}"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": {
            "${OIDC_ENDPOINT}:sub": [
              "system:serviceaccount:openshift-adp:openshift-adp-controller-manager",
              "system:serviceaccount:openshift-adp:velero"]
          }
        }
      }]
  }
EOF
```
.. Create the role by running the following command:
```bash
$ ROLE_ARN=$(aws iam create-role --role-name \
  "${ROLE_NAME}" \
  --assume-role-policy-document file://${SCRATCH}/trust-policy.json \
  --tags Key=rosa_cluster_id,Value=${ROSA_CLUSTER_ID} \
         Key=rosa_openshift_version,Value=${CLUSTER_VERSION} \
         Key=rosa_role_prefix,Value=ManagedOpenShift \
         Key=operator_namespace,Value=openshift-adp \
         Key=operator_name,Value=openshift-oadp \
  --query Role.Arn --output text)
```
.. View the role ARN by running the following command:
```bash
$ echo ${ROLE_ARN}
```

1. Attach the IAM policy to the IAM role by running the following command:
```bash
$ aws iam attach-role-policy --role-name "${ROLE_NAME}" \
  --policy-arn ${POLICY_ARN}
```