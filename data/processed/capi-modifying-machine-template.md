# Modifying a Cluster API machine template

You can update the machine template resource for your cluster by modifying the YAML manifest file and applying it with the OpenShift CLI (`oc`).

.Prerequisites

- You have deployed an OpenShift Container Platform cluster that uses the Cluster API.

- You have access to the cluster using an account with `cluster-admin` permissions.

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. List the machine template resource for your cluster by running the following command:
--
```bash
$ oc get <machine_template_kind> <1>
```
<1> Specify the value that corresponds to your platform.
The following values are valid:
|====
|Cluster infrastructure provider |Value

|Amazon Web Services
|`AWSMachineTemplate`

|Google Cloud
|`GCPMachineTemplate`

|Microsoft Azure
|`AzureMachineTemplate`

|RHOSP
|`OpenStackMachineTemplate`

|VMware vSphere
|`VSphereMachineTemplate`

|Bare metal
|`Metal3MachineTemplate`

|====
--
.Example output
```text
NAME              AGE
<template_name>   77m
```

1. Write the machine template resource for your cluster to a file that you can edit by running the following command:
```bash
$ oc get <machine_template_kind> <template_name> -o yaml > <template_name>.yaml
```
where `<template_name>` is the name of the machine template resource for your cluster.

1. Make a copy of the `<template_name>.yaml` file with a different name. This procedure uses `<modified_template_name>.yaml` as an example file name.

1. Use a text editor to make changes to the `<modified_template_name>.yaml` file that defines the updated machine template resource for your cluster.
When editing the machine template resource, observe the following:

- The parameters in the `spec` stanza are provider specific.
For more information, see the sample Cluster API machine template YAML for your provider.

- You must use a value for the `metadata.name` parameter that differs from any existing values.
> **IMPORTANT:** For any Cluster API compute machine sets that reference this template, you must update the `spec.template.spec.infrastructureRef.name` parameter to match the `metadata.name` value in the new machine template resource.

1. Apply the machine template CR by running the following command:
```bash
$ oc apply -f <modified_template_name>.yaml <1>
```
<1> Use the edited YAML file with a new name.

.Next steps

- For any Cluster API compute machine sets that reference this template, update the `spec.template.spec.infrastructureRef.name` parameter to match the `metadata.name` value in the new machine template resource.
For more information, see "Modifying a compute machine set by using the CLI."