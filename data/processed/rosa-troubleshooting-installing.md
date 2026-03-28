# Installation troubleshooting

This procedure describes how to troubleshoot installation issues for OpenShift Container Platform clusters.

.Procedure

- Inspect install or uninstall logs:
- To display install logs, run the following command, replacing `<cluster_name>` with the name of your cluster:
```bash
$ rosa logs install --cluster=<cluster_name>
```
- To watch the logs, include the `--watch` flag:
```bash
$ rosa logs install --cluster=<cluster_name> --watch
```
- To display uninstall logs, run the following command, replacing `<cluster_name>` with the name of your cluster:
```bash
$ rosa logs uninstall --cluster=<cluster_name>
```
- To watch the logs, include the `--watch` flag:
```bash
$ rosa logs uninstall --cluster=<cluster_name> --watch
```

- Verify your AWS account permissions for clusters without STS:
Run the following command to verify if your AWS account has the correct permissions. This command verifies permissions only for clusters that do not use the AWS Security Token Service (STS):
```bash
$ rosa verify permissions
```
If you receive any errors, double check to ensure than an [SCP](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_type-auth.html#orgs_manage_policies_scp) is not applied to your AWS account. If you are required to use an SCP, see [Red Hat Requirements for Customer Cloud Subscriptions](https://www.openshift.com/dedicated/ccs#scp) for details on the minimum required SCP.

- Verify your AWS account and quota:
Run the following command to verify you have the available quota on your AWS account:
```bash
$ rosa verify quota
```
AWS quotas change based on region. Be sure you are verifying your quota for the correct AWS region. If you need to increase your quota, navigate to your [AWS console](https://aws.amazon.com/console/), and request a quota increase for the service that failed.

- AWS notification emails:
When creating a cluster, the OpenShift Container Platform service creates small instances in all supported regions. This check ensures the AWS account being used can deploy to each supported region.
For AWS accounts that are not using all supported regions, AWS may send one or more emails confirming that "Your Request For Accessing AWS Resources Has Been Validated". Typically the sender of this email is aws-verification@amazon.com.
This is expected behavior as the OpenShift Container Platform service is validating your AWS account configuration.