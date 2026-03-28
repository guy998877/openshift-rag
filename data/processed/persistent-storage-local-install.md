# Installing the Local Storage Operator

The Local Storage Operator is not installed in OpenShift Container Platform by default. Use the following procedure to install and configure this Operator to enable local volumes in your cluster.

.Prerequisites

- Access to the OpenShift Container Platform web console or command-line interface (CLI).

.Procedure

1. Create the `openshift-local-storage` project:
```bash
$ oc adm new-project openshift-local-storage
```

1. Optional: Allow local storage creation on infrastructure nodes.
You might want to use the Local Storage Operator to create volumes on infrastructure nodes in support of components such as logging and monitoring.
You must adjust the default node selector so that the Local Storage Operator includes the infrastructure nodes, and not just worker nodes.
To block the Local Storage Operator from inheriting the cluster-wide default selector, enter the following command:
```bash
$ oc annotate namespace openshift-local-storage openshift.io/node-selector=''
```

1. Optional: Allow local storage to run on the management pool of CPUs in single-node deployment.
Use the Local Storage Operator in single-node deployments and allow the use of CPUs that belong to the `management` pool. Perform this step on single-node installations that use management workload partitioning.
To allow Local Storage Operator to run on the management CPU pool, run following commands:
```bash
$ oc annotate namespace openshift-local-storage workload.openshift.io/allowed='management'
```

.From the UI

To install the Local Storage Operator from the web console, follow these steps:

1. Log in to the OpenShift Container Platform web console.

1. Navigate to *Ecosystem* -> *Software Catalog*.

1. Type *Local Storage* into the filter box to locate the Local Storage Operator.

1. Click *Install*.

1. On the *Install Operator* page, select *A specific namespace on the cluster*. Select *openshift-local-storage* from the drop-down menu.

1. Adjust the values for *Update Channel* and *Approval Strategy* to the values that you want.

1. Click *Install*.

Once finished, the Local Storage Operator will be listed in the *Installed Operators* section of the web console.

.From the CLI
1. Install the Local Storage Operator from the CLI.

.. Create an object YAML file to define an Operator group and subscription for the Local Storage Operator,
such as `openshift-local-storage.yaml`:
.Example openshift-local-storage.yaml
```yaml
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: local-operator-group
  namespace: openshift-local-storage
spec:
  targetNamespaces:
    - openshift-local-storage
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: local-storage-operator
  namespace: openshift-local-storage
spec:
  channel: stable
  installPlanApproval: Automatic <1>
  name: local-storage-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
```
<1> The user approval policy for an install plan.

1. Create the Local Storage Operator object by entering the following command:
```bash
$ oc apply -f openshift-local-storage.yaml
```
At this point, the Operator Lifecycle Manager (OLM) is now aware of the Local Storage Operator. A ClusterServiceVersion (CSV) for the Operator should appear in the target namespace, and APIs provided by the Operator should be available for creation.
1. Verify local storage installation by checking that all pods and the Local Storage Operator have been created:

.. Check that all the required pods have been created:
```bash
$ oc -n openshift-local-storage get pods
```
.Example output
```bash
NAME                                      READY   STATUS    RESTARTS   AGE
local-storage-operator-746bf599c9-vlt5t   1/1     Running   0          19m
```

.. Check the ClusterServiceVersion (CSV) YAML manifest to see that the Local Storage Operator is available in the `openshift-local-storage` project:
```bash
$ oc get csvs -n openshift-local-storage
```
.Example output
```bash
NAME                                         DISPLAY         VERSION               REPLACES   PHASE
local-storage-operator.4.2.26-202003230335   Local Storage   4.2.26-202003230335              Succeeded
```

After all checks have passed, the Local Storage Operator is installed successfully.