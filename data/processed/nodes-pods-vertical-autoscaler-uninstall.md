# Uninstalling the Vertical Pod Autoscaler Operator

You can remove the Vertical Pod Autoscaler Operator (VPA) from your OpenShift Container Platform cluster. After uninstalling, the resource requests for the pods that are already modified by an existing VPA custom resource (CR) do not change. The resources defined in the workload object, not the previous recommendations made by the VPA, are allocated to any new pods.

> **NOTE:** You can remove a specific VPA CR by using the `oc delete vpa <vpa-name>` command. The same actions apply for resource requests as uninstalling the vertical pod autoscaler.

After removing the VPA, it is recommended that you remove the other components associated with the Operator to avoid potential issues.

.Prerequisites

- You installed the VPA.

.Procedure

1. In the OpenShift Container Platform web console, click *Ecosystem* -> *Installed Operators*.

1. Switch to the *openshift-vertical-pod-autoscaler* project.

1. For the *VerticalPodAutoscaler*  Operator, click the Options menu image:kebab.png[title="Options menu"] and select *Uninstall Operator*.

1. Optional: To remove all operands associated with the Operator, in the dialog box, select *Delete all operand instances for this operator* checkbox.

1. Click *Uninstall*.

1. Optional: Use the OpenShift CLI to remove the VPA components:

.. Delete the VPA namespace:
```bash
$ oc delete namespace openshift-vertical-pod-autoscaler
```

.. Delete the VPA custom resource definition (CRD) objects:
```bash
$ oc delete crd verticalpodautoscalercheckpoints.autoscaling.k8s.io
```
```bash
$ oc delete crd verticalpodautoscalercontrollers.autoscaling.openshift.io
```
```bash
$ oc delete crd verticalpodautoscalers.autoscaling.k8s.io
```
Deleting the CRDs removes the associated roles, cluster roles, and role bindings.
> **NOTE:** This action removes from the cluster all user-created VPA CRs. If you re-install the VPA, you must create these objects again.

.. Delete the `MutatingWebhookConfiguration` object by running the following command:
```bash
$ oc delete MutatingWebhookConfiguration vpa-webhook-config
```

.. Delete the VPA Operator:
```bash
$ oc delete operator/vertical-pod-autoscaler.openshift-vertical-pod-autoscaler
```