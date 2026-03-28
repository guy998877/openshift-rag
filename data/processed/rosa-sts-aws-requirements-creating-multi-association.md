# Associating multiple AWS accounts with your Red Hat organization

You can associate multiple AWS accounts with your Red Hat organization. Associating multiple accounts lets you create OpenShift Container Platform clusters on any of the associated AWS accounts from your Red Hat organization.

With this capability, you can create clusters on different AWS profiles according to characteristics that make sense for your business, for example, by using one AWS profile for each region to create region-bound environments.

.Prerequisites

- You have an AWS account.
- You are using link:https://console.redhat.com/openshift[OpenShift Cluster Manager] to create clusters.
- You have the permissions required to install AWS account-wide roles.
- You have installed and configured the latest AWS CLI (`aws`) and {rosa-cli-first} on your installation host.
- You have created the `ocm-role` and `user-role` IAM roles for OpenShift Container Platform.

.Procedure

- To specify an AWS account profile when creating an OpenShift Cluster Manager role:
```bash
$ rosa create --profile <aws_profile> ocm-role
```

- To specify an AWS account profile when creating a user role:
```bash
$ rosa create --profile <aws_profile> user-role
```

- To specify an AWS account profile when creating the account roles:
```bash
$ rosa create --profile <aws_profile> account-roles
```
> **NOTE:** If you do not specify a profile, the default AWS profile and its associated AWS region are used.