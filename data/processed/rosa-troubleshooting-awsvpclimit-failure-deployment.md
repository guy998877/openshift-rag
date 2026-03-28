# Troubleshooting cluster creation with an AWSVPCLimitExceeded error

If a cluster creation action fails, you might receive the following error message.

.Example OpenShift Cluster Manager output
```bash
Provisioning Error Code:    OCM3013
Provisioning Error Message: VPC limit exceeded. Clean unused VPCs or increase quota and try again.
```

This error indicates that you have reached the quota for the number of VPCs.

.Procedure

- To fix this issue, try one of the following methods:
- Request a quota increase from AWS:
.. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
.. Click your user name and select **Service Quotas**.
.. Under **Manage quotas**, select a service to view available quotas.
.. If the quota is adjustable, you can choose the button or the name, and then choose **Request increase**.
.. For **Increase quota value**, enter the new value. The new value must be greater than the current value.
.. Choose **Request**.
- Clean unused VPCs. Before you can delete a VPC, you must first terminate or delete any resources that created a requester-managed network interface in the VPC. For example, you must terminate your EC2 instances and delete your load balancers, NAT gateways, transit gateways, and interface VPC endpoints before deleting a VPC:
.. Sign in to the [AWS EC2 console](https://console.aws.amazon.com/ec2/).
.. Terminate all instances in the VPC. For more information, see [Terminate Amazon EC2 instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html).
.. Open the [Amazon VPC console](https://console.aws.amazon.com/vpc).
.. In the navigation pane, choose **Your VPCs**.
.. Select the VPC to delete and choose **Actions, Delete VPC**.
.. If you have a Site-to-Site VPN connection, select the option to delete it; otherwise, leave it unselected. Choose **Delete VPC**.