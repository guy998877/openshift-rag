# Adding more compute machines to your AWS cluster by using CloudFormation templates

You can add more compute machines to your OpenShift Container Platform cluster on Amazon Web Services (AWS) that you created by using the sample CloudFormation templates.

> **IMPORTANT:** The CloudFormation template creates a stack that represents one compute machine. You must create a stack for each compute machine.

> **NOTE:** If you do not use the provided CloudFormation template to create your compute nodes, you must review the provided information and manually create the infrastructure. If your cluster does not initialize correctly, you might have to contact Red Hat support with your installation logs.

.Prerequisites

- You installed an OpenShift Container Platform cluster by using CloudFormation templates and have access to the JSON file and CloudFormation template that you used to create the compute machines during cluster installation.
- You installed the AWS CLI.

.Procedure

1. Create another compute stack.
.. Launch the template:
```bash
$ aws cloudformation create-stack --stack-name <name> \ <1>
     --template-body file://<template>.yaml \ <2>
     --parameters file://<parameters>.json <3>
```
<1> `<name>` is the name for the CloudFormation stack, such as `cluster-workers`. You must provide the name of this stack if you remove the cluster.
<2> `<template>` is the relative path to and name of the CloudFormation template YAML file that you saved.
<3> `<parameters>` is the relative path to and name of the CloudFormation parameters JSON file.

.. Confirm that the template components exist:
```bash
$ aws cloudformation describe-stacks --stack-name <name>
```

1. Continue to create compute stacks until you have created enough compute machines for your cluster.