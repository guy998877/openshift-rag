# Installing the custom metrics autoscaler

You can use the following procedure to install the Custom Metrics Autoscaler Operator.

.Prerequisites

- Remove any previously-installed Technology Preview versions of the Cluster Metrics Autoscaler Operator.

- Remove any versions of the community-based KEDA.
Also, remove the KEDA 1.x custom resource definitions by running the following commands:
```bash
$ oc delete crd scaledobjects.keda.k8s.io
```
```bash
$ oc delete crd triggerauthentications.keda.k8s.io
```

- Optional: If you need the Custom Metrics Autoscaler Operator to connect to off-cluster services, such as an external Kafka cluster or an external Prometheus service, put any required service CA certificates into a config map. The config map must exist in the same namespace where the Operator is installed. For example:
```bash
$ oc create configmap -n openshift-keda thanos-cert  --from-file=ca-cert.pem
```

.Procedure

1. In the OpenShift Container Platform web console, click *Ecosystem* -> *Software Catalog*.

1. Choose *Custom Metrics Autoscaler* from the list of available Operators, and click *Install*.

1. On the *Install Operator* page, ensure that the *All namespaces on the cluster (default)* option
is selected for *Installation Mode*. This installs the Operator in all namespaces.

1. Ensure that the *openshift-keda* namespace is selected for *Installed Namespace*. OpenShift Container Platform creates the namespace, if not present in your cluster.

1. Click *Install*.

1. Verify the installation by listing the Custom Metrics Autoscaler Operator components:

.. Navigate to *Workloads* -> *Pods*.

.. Select the `openshift-keda` project from the drop-down menu and verify that the `custom-metrics-autoscaler-operator-*` pod is running.

.. Navigate to *Workloads* -> *Deployments* to verify that the `custom-metrics-autoscaler-operator` deployment is running.

1. Optional: Verify the installation in the OpenShift CLI using the following commands:
```bash
$ oc get all -n openshift-keda
```
The output appears similar to the following:
.Example output
```bash
NAME                                                      READY   STATUS    RESTARTS   AGE
pod/custom-metrics-autoscaler-operator-5fd8d9ffd8-xt4xp   1/1     Running   0          18m

NAME                                                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/custom-metrics-autoscaler-operator   1/1     1            1           18m

NAME                                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/custom-metrics-autoscaler-operator-5fd8d9ffd8   1         1         1       18m
```