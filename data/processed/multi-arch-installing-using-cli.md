# Installing the Multiarch Tuning Operator by using the CLI

You can install the Multiarch Tuning Operator by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed `oc`.
- You have logged in to `oc` as a user with `cluster-admin` privileges.

.Procedure

1. Create a new project named `openshift-multiarch-tuning-operator` by running the following command:
```bash
$ oc create ns openshift-multiarch-tuning-operator
```

1. Create an `OperatorGroup` object:

.. Create a YAML file with the configuration for creating an `OperatorGroup` object.
.Example YAML configuration for creating an `OperatorGroup` object
```yaml
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: openshift-multiarch-tuning-operator
  namespace: openshift-multiarch-tuning-operator
spec: {}
```

.. Create the `OperatorGroup` object by running the following command:
```bash
$ oc create -f <file_name> <1>
```
<1> Replace `<file_name>` with the name of the YAML file that contains the `OperatorGroup` object configuration.

1. Create a `Subscription` object:

.. Create a YAML file with the configuration for creating a `Subscription` object.
.Example YAML configuration for creating a `Subscription` object
```yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-multiarch-tuning-operator
  namespace: openshift-multiarch-tuning-operator
spec:
  channel: stable
  name: multiarch-tuning-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
  installPlanApproval: Automatic
  startingCSV: multiarch-tuning-operator.<version>
```

.. Create the `Subscription` object by running the following command:
```bash
$ oc create -f <file_name> <1>
```
<1> Replace `<file_name>` with the name of the YAML file that contains the `Subscription` object configuration.

> **NOTE:** For more details about configuring the `Subscription` object and `OperatorGroup` object, see "Installing from the software catalog by using the CLI".

.Verification

1. To verify that the Multiarch Tuning Operator is installed, run the following command:
```bash
$ oc get csv -n openshift-multiarch-tuning-operator
```
.Example output
```bash
NAME                                   DISPLAY                     VERSION       REPLACES                            PHASE
multiarch-tuning-operator.<version>   Multiarch Tuning Operator   <version>     multiarch-tuning-operator.1.0.0      Succeeded
```
The installation is successful if the Operator is in `Succeeded` phase.

1. Optional: To verify that the `OperatorGroup` object is created, run the following command:
```bash
$ oc get operatorgroup -n openshift-multiarch-tuning-operator
```
.Example output
```bash
NAME                                        AGE
openshift-multiarch-tuning-operator-q8zbb   133m
```

1. Optional: To verify that the `Subscription` object is created, run the following command:
```bash
$ oc get subscription -n openshift-multiarch-tuning-operator
```
.Example output
```bash
NAME                        PACKAGE                     SOURCE                  CHANNEL
multiarch-tuning-operator   multiarch-tuning-operator   redhat-operators        stable
```