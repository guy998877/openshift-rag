# Installing LVM Storage by using the CLI

As a cluster administrator, you can install LVM Storage by using the OpenShift CLI.

> **NOTE:** The default namespace for the LVM Storage Operator is `openshift-lvm-storage`.

.Prerequisites

- You have installed the OpenShift CLI (`oc`).
- You have logged in to OpenShift Container Platform as a user with `cluster-admin` and Operator installation permissions.

.Procedure

1. Create a YAML file with the configuration for creating a namespace:
.Example YAML configuration for creating a namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  labels:
    openshift.io/cluster-monitoring: "true"
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
  name: openshift-lvm-storage
```

1. Create the namespace by running the following command:
```bash
$ oc create -f <file_name>
---- 

. Create an `OperatorGroup` CR YAML file:
+
.Example `OperatorGroup` CR
[source,yaml]
```
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: openshift-storage-operatorgroup
  namespace: openshift-lvm-storage
spec:
  targetNamespaces:
  - openshift-storage

1. Create the `OperatorGroup` CR by running the following command:
```bash
$ oc create -f <file_name> 
```

1. Create a `Subscription` CR YAML file:
.Example `Subscription` CR
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: lvms
  namespace: openshift-lvm-storage
spec:
  installPlanApproval: Automatic
  name: lvms-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
```

1. Create the `Subscription` CR by running the following command:
```bash
$ oc create -f <file_name> 
```

.Verification

1. To verify that LVM Storage is installed, run the following command:
```bash
$ oc get csv -n openshift-lvm-storage -o custom-columns=Name:.metadata.name,Phase:.status.phase
```
.Example output
```bash
Name                         Phase
4.13.0-202301261535          Succeeded
```