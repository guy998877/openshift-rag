# Installing global Operators in custom namespaces

When installing Operators with the OpenShift Container Platform web console, the default behavior installs Operators that support the *All namespaces* install mode into the default `openshift-operators` global namespace. This can cause issues related to shared install plans and update policies between all Operators in the namespace. For more details on these limitations, see "Multitenancy and Operator colocation".

As a cluster administrator,
you can bypass this default behavior manually by creating a custom global namespace and using that namespace to install your individual or scoped set of Operators and their dependencies.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

// In OSD/ROSA, dedicated-admins can't create namespaces directly but can create projects.
1. Before installing the Operator, create a namespace for the installation of your desired Operator. This installation namespace will become the custom global namespace:

.. Define a `Namespace` resource and save the YAML file, for example, `global-operators.yaml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: global-operators
```

.. Create the namespace by running the following command:
```bash
$ oc create -f global-operators.yaml
```
// Slightly different step for OSD/ROSA since dedicated-admins can't create namespaces directly.

1. Create a custom _global Operator group_, which is an Operator group that watches all namespaces:

.. Define an `OperatorGroup` resource and save the YAML file, for example, `global-operatorgroup.yaml`. Omit both the `spec.selector` and `spec.targetNamespaces` fields to make it a _global Operator group_, which selects all namespaces:
```yaml
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: global-operatorgroup
  namespace: global-operators
```
> **NOTE:** The `status.namespaces` of a created global Operator group contains the empty string (`""`), which signals to a consuming Operator that it should watch all namespaces.

.. Create the Operator group by running the following command:
```bash
$ oc create -f global-operatorgroup.yaml
```