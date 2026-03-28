# Uninstalling the Custom Metrics Autoscaler Operator

Use the following procedure to remove the custom metrics autoscaler from your OpenShift Container Platform cluster.

.Prerequisites

- The Custom Metrics Autoscaler Operator must be installed.

.Procedure

1. In the OpenShift Container Platform web console, click *Ecosystem* -> *Installed Operators*.

1. Switch to the *openshift-keda* project.

1. Remove the `KedaController` custom resource.

.. Find the *CustomMetricsAutoscaler*  Operator and click the *KedaController* tab.

.. Find the custom resource, and then click *Delete KedaController*.

.. Click *Uninstall*.

1. Remove the Custom Metrics Autoscaler Operator:

.. Click *Ecosystem* -> *Installed Operators*.

.. Find the *CustomMetricsAutoscaler*  Operator and click the Options menu image:kebab.png[title="Options menu"] and select *Uninstall Operator*.

.. Click *Uninstall*.

1. Optional: Use the OpenShift CLI to remove the custom metrics autoscaler components:

.. Delete the custom metrics autoscaler CRDs:
--
- `clustertriggerauthentications.keda.sh`
- `kedacontrollers.keda.sh`
- `scaledjobs.keda.sh`
- `scaledobjects.keda.sh`
- `triggerauthentications.keda.sh`
--
```bash
$ oc delete crd clustertriggerauthentications.keda.sh kedacontrollers.keda.sh scaledjobs.keda.sh scaledobjects.keda.sh triggerauthentications.keda.sh
```
Deleting the CRDs removes the associated roles, cluster roles, and role bindings. However, there might be a few cluster roles that must be manually deleted.

.. List any custom metrics autoscaler cluster roles:
```bash
$ oc get clusterrole | grep keda.sh
```

.. Delete the listed custom metrics autoscaler cluster roles. For example:
```bash
$ oc delete clusterrole.keda.sh-v1alpha1-admin
```

.. List any custom metrics autoscaler cluster role bindings:
```bash
$ oc get clusterrolebinding | grep keda.sh
```

.. Delete the listed custom metrics autoscaler cluster role bindings. For example:
```bash
$ oc delete clusterrolebinding.keda.sh-v1alpha1-admin
```

1. Delete the custom metrics autoscaler project:
```bash
$ oc delete project openshift-keda
```

1. Delete the Cluster Metric Autoscaler Operator:
```bash
$ oc delete operator/openshift-custom-metrics-autoscaler-operator.openshift-keda
```