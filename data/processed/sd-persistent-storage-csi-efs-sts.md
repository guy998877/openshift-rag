# Obtaining a role Amazon Resource Name for Security Token Service

This procedure explains how to obtain a role Amazon Resource Name (ARN) to configure the AWS EFS CSI Driver Operator with OpenShift Container Platform on AWS Security Token Service (STS).

> **IMPORTANT:** Perform this procedure before you install the AWS EFS CSI Driver Operator (see _Installing the AWS EFS CSI Driver Operator_ procedure).

.Prerequisites

- Access to the cluster as a user with the cluster-admin role.
- AWS account credentials

.Procedure

1. Create an IAM policy JSON file with the following content:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:DescribeAccessPoints",
        "elasticfilesystem:DescribeFileSystems",
        "elasticfilesystem:DescribeMountTargets",
        "ec2:DescribeAvailabilityZones",
        "elasticfilesystem:TagResource"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:CreateAccessPoint"
      ],
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:RequestTag/efs.csi.aws.com/cluster": "true"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": "elasticfilesystem:DeleteAccessPoint",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/efs.csi.aws.com/cluster": "true"
        }
      }
    }
  ]
}
```

1. Create an IAM trust JSON file with the following content:
--
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<your_aws_account_ID>:oidc-provider/<openshift_oidc_provider>"  <1>
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<openshift_oidc_provider>:sub": [  <2>
            "system:serviceaccount:openshift-cluster-csi-drivers:aws-efs-csi-driver-operator",
            "system:serviceaccount:openshift-cluster-csi-drivers:aws-efs-csi-driver-controller-sa"
          ]
        }
      }
    }
  ]
}
```
<1> Specify your AWS account ID and the OpenShift OIDC provider endpoint. 
Obtain your AWS account ID by running the following command:
```bash
$ aws sts get-caller-identity --query Account --output text
```

<2> Specify the OpenShift OIDC endpoint again.
--

1. Create the IAM role:
```bash
ROLE_ARN=$(aws iam create-role \
  --role-name "<your_cluster_name>-aws-efs-csi-operator" \
  --assume-role-policy-document file://<your_trust_file_name>.json \
  --query "Role.Arn" --output text); echo $ROLE_ARN
```
Copy the role ARN. You will need it when you install the AWS EFS CSI Driver Operator.

1. Create the IAM policy:
```bash
POLICY_ARN=$(aws iam create-policy \
  --policy-name "<your_cluster_name>-aws-efs-csi" \
  --policy-document file://<your_policy_file_name>.json \
  --query 'Policy.Arn' --output text); echo $POLICY_ARN
```

1. Attach the IAM policy to the IAM role:
```bash
$ aws iam attach-role-policy \
  --role-name "<your_cluster_name>-aws-efs-csi-operator" \
  --policy-arn $POLICY_ARN
```

////
1. Create a `Secret` YAML file for the driver operator:
```yaml
apiVersion: v1
kind: Secret
metadata:
 name: aws-efs-cloud-credentials
 namespace: openshift-cluster-csi-drivers
stringData:
  credentials: |-
    [default]
    sts_regional_endpoints = regional
    role_arn = <role_ARN> <1>
    web_identity_token_file = /var/run/secrets/openshift/serviceaccount/token
```
<1> Replace `role_ARN` with the output you saved while creating the role.

1. Create the secret:
```bash
$ oc apply -f aws-efs-cloud-credentials.yaml
```
You are now ready to install the AWS EFS CSI driver.
////