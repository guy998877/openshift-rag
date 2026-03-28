# Uninstalling LVM Storage by using the CLI

You can uninstall LVM Storage by using the OpenShift CLI (`oc`).

.Prerequisites

- You have logged in to `oc` as a user with `cluster-admin` permissions.
- You deleted the persistent volume claims (PVCs), volume snapshots, and volume clones provisioned by LVM Storage. You have also deleted the applications that are using these resources.
- You deleted the `LVMCluster` custom resource (CR).

.Procedure

1. Get the `currentCSV` value for the LVM Storage Operator by running the following command:
```bash
$ oc get subscription.operators.coreos.com lvms-operator -n <namespace> -o yaml | grep currentCSV
```
.Example output
```bash
currentCSV: lvms-operator.v4.15.3
```

1. Delete the subscription by running the following command:
```bash
$ oc delete subscription.operators.coreos.com lvms-operator -n <namespace>
```
.Example output
```bash
subscription.operators.coreos.com "lvms-operator" deleted
```

1. Delete the CSV for the LVM Storage Operator in the target namespace by running the following command:
```bash
$ oc delete clusterserviceversion <currentCSV> -n <namespace> <1>
```
<1> Replace `<currentCSV>` with the `currentCSV` value for the LVM Storage Operator.
.Example output
```bash
clusterserviceversion.operators.coreos.com "lvms-operator.v4.15.3" deleted
```

.Verification

- To verify that the LVM Storage Operator is uninstalled, run the following command:
```bash
$ oc get csv -n <namespace>
```
If the LVM Storage Operator was successfully uninstalled, it does not appear in the output of this command.