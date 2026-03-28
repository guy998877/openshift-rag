# Troubleshooting cluster creation with an AWSInsufficientPermissions error

If a cluster creation action fails, you might receive the following error message.

.Example OpenShift Cluster Manager output
```bash
Provisioning Error Code:    OCM3033
Provisioning Error Message: Current credentials insufficient for performing cluster installation.
```

This error indicates that the cluster installation is blocked due to missing or insufficient privileges on the AWS account used to provision the cluster.

.Procedure

1. Ensure that the prerequisites are met by reviewing _Detailed requirements for deploying ROSA (classic architecture) using STS_ or _Deploying ROSA without AWS STS_ in _Additional resources_ depending on your choice of credential mode for installing clusters.
> **TIP:** [role="_abstract"] AWS Security Token Service (STS) is the recommended credential mode for installing and interacting with clusters on OpenShift Container Platform because it provides enhanced security.
1. If needed, you can re-create the permissions and policies by using the `-f` flag:
```bash
$ rosa create ocm-role -f
```
```bash
$ rosa create user-role -f
```
```bash
$ rosa create account-roles -f
```
```bash
$ rosa create operator-roles -c ${CLUSTER} -f
```

1. Validate all the prerequisites and attempt cluster reinstallation.