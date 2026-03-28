# Deleting Operators from a cluster using the CLI

Cluster administrators can delete installed Operators from a selected namespace by using the CLI.

.Prerequisites

- You have access to the OpenShift Container Platform cluster using an account with
- The OpenShift CLI (`oc`) is installed on your workstation.

.Procedure

1. Ensure the latest version of the subscribed operator (for example, `serverless-operator`) is identified in the `currentCSV` field.
```bash
$ oc get subscription.operators.coreos.com serverless-operator -n openshift-serverless -o yaml | grep currentCSV
```
.Example output
```bash
  currentCSV: serverless-operator.v1.28.0
```

1. Delete the subscription (for example, `serverless-operator`):
```bash
$ oc delete subscription.operators.coreos.com serverless-operator -n openshift-serverless
```
.Example output
```bash
subscription.operators.coreos.com "serverless-operator" deleted
```

1. Delete the CSV for the Operator in the target namespace using the `currentCSV` value from the previous step:
```bash
$ oc delete clusterserviceversion serverless-operator.v1.28.0 -n openshift-serverless
```
.Example output
```bash
clusterserviceversion.operators.coreos.com "serverless-operator.v1.28.0" deleted
```