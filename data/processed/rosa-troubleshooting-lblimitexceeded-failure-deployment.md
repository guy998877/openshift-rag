# Troubleshooting cluster creation with an ALoadBalancerLimitExceeded error

If a cluster creation action fails, you might receive the following error message.

.Example output
```bash
Provisioning Error Code:    OCM3036
Provisioning Error Message: AWS Load Balancer quota limit exceeded. Clean unused load balancers or increase quota and try again.
```

This error indicates that you have reached the quota for the number of load balancers.

.Procedure

- To fix this issue, try one of the following methods:
- Request a quota increase from AWS:
.. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
.. Click your user name and select **Service Quotas**.
.. Under **Manage quotas**, select a service to view available quotas.
.. If the quota is adjustable, you can choose the button or the name, and then choose Request quota increase.
.. For **Change quota value**, enter the new value. The new value must be greater than the current value.
.. Choose **Request**.
- Delete a load balancer using the console:
.. If you have a CNAME record for your domain that points to your load balancer, point it to a new location and wait for the DNS change to take effect before deleting your load balancer.
.. Open the [Amazon EC2 console](https://console.aws.amazon.com/ec2/).
.. On the navigation pane, under **LOAD BALANCING**, choose **Load Balancers**.
.. Select the load balancer, and then choose **Actions, Delete**.
.. When prompted for confirmation, choose **Yes, Delete**.