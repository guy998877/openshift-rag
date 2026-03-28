# Creating a Cluster API machine template

You can create a provider-specific machine template resource by creating a YAML manifest file and applying it with the OpenShift CLI (`oc`).

.Prerequisites

- You have deployed an OpenShift Container Platform cluster.

- You have enabled the use of the Cluster API.

- You have access to the cluster using an account with `cluster-admin` permissions.

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. Create a YAML file similar to the following. This procedure uses `<machine_template_resource_file>.yaml` as an example file name.
--
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta1
kind: <machine_template_kind> # <1>
metadata:
  name: <template_name> # <2>
  namespace: openshift-cluster-api
spec:
  template:
    spec: # <3>
```
<1> Specify the machine template kind. This value must match the value for your platform.
The following values are valid:
|====
|Cluster infrastructure provider |Value

|Amazon Web Services (AWS)
|`AWSMachineTemplate`

|Google Cloud
|`GCPMachineTemplate`

|Microsoft Azure
|`AzureMachineTemplate`

|Red Hat OpenStack Platform (RHOSP)
|`OpenStackMachineTemplate`

|VMware vSphere
|`VSphereMachineTemplate`

|Bare metal
|`Metal3MachineTemplate`

|====
<2> Specify a name for the machine template.
<3> Specify the details for your environment. These parameters are provider specific. For more information, see the sample Cluster API machine template YAML for your provider.
--

1. Create the machine template CR by running the following command:
```bash
$ oc create -f <machine_template_resource_file>.yaml
```

.Verification

- Confirm that the machine template CR is created by running the following command:
```bash
$ oc get <machine_template_kind> -n openshift-cluster-api
```
where `<machine_template_kind>` is the value that corresponds to your platform.
.Example output
```text
NAME              AGE
<template_name>   77m
```