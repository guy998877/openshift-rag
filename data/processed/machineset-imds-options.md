# Machine set options for the Amazon EC2 Instance Metadata Service

You can use machine sets to create machines that use a specific version of the Amazon EC2 Instance Metadata Service (IMDS). Machine sets can create machines that allow the use of both IMDSv1 and [IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) or machines that require the use of IMDSv2.

> **NOTE:** To use IMDSv2 on AWS clusters that were created with OpenShift Container Platform version 4.6 or earlier, you must update your boot image. For more information, see "Boot image management".

> **IMPORTANT:** Before configuring a machine set to create machines that require IMDSv2, ensure that any workloads that interact with the AWS metadata service support IMDSv2.