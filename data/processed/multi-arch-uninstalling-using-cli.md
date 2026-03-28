# Uninstalling the Multiarch Tuning Operator by using the CLI

You can uninstall the Multiarch Tuning Operator by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed `oc`.
- You have logged in to `oc` as a user with `cluster-admin` privileges.
- You deleted the `ClusterPodPlacementConfig` object.
> **IMPORTANT:** You must delete the `ClusterPodPlacementConfig` object before uninstalling the Multiarch Tuning Operator. Uninstalling the Operator without deleting the `ClusterPodPlacementConfig` object can lead to unexpected behavior.

.Procedure

1. Get the `Subscription` object name for the Multiarch Tuning Operator by running the following command: 
```bash
$ oc get subscription.operators.coreos.com -n <namespace> <1>
```
<1> Replace `<namespace>` with the name of the namespace where you want to uninstall the Multiarch Tuning Operator.
.Example output
```bash
NAME                                  PACKAGE                     SOURCE             CHANNEL
openshift-multiarch-tuning-operator   multiarch-tuning-operator   redhat-operators   stable
```

1. Get the `currentCSV` value for the Multiarch Tuning Operator by running the following command:
```bash
$ oc get subscription.operators.coreos.com <subscription_name> -n <namespace> -o yaml | grep currentCSV <1>
```
<1> Replace `<subscription_name>` with the `Subscription` object name. For example: `openshift-multiarch-tuning-operator`. Replace `<namespace>` with the name of the namespace where you want to uninstall the Multiarch Tuning Operator.
.Example output
```bash
currentCSV: multiarch-tuning-operator.<version>
```

1. Delete the `Subscription` object by running the following command:
```bash
$ oc delete subscription.operators.coreos.com <subscription_name> -n <namespace> <1>
```
<1> Replace `<subscription_name>` with the `Subscription` object name. Replace `<namespace>` with the name of the namespace where you want to uninstall the Multiarch Tuning Operator.
.Example output
```bash
subscription.operators.coreos.com "openshift-multiarch-tuning-operator" deleted
```

1. Delete the CSV for the Multiarch Tuning Operator in the target namespace using the `currentCSV` value by running the following command:
```bash
$ oc delete clusterserviceversion <currentCSV_value> -n <namespace> <1>
```
<1> Replace `<currentCSV>` with the `currentCSV` value for the Multiarch Tuning Operator. For example: `multiarch-tuning-operator.<version>`. Replace `<namespace>` with the name of the namespace where you want to uninstall the Multiarch Tuning Operator.
.Example output
```bash
clusterserviceversion.operators.coreos.com "multiarch-tuning-operator.<version>" deleted
```

.Verification

- To verify that the Multiarch Tuning Operator is uninstalled, run the following command:
```bash
$ oc get csv -n <namespace> <1>
```
<1> Replace `<namespace>` with the name of the namespace where you have uninstalled the Multiarch Tuning Operator.
.Example output
```bash
No resources found in openshift-multiarch-tuning-operator namespace.
```