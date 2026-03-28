# Uninstalling Run Once Duration Override Operator resources

Optionally, after uninstalling the Run Once Duration Override Operator, you can remove its related resources from your cluster.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.
- You have uninstalled the Run Once Duration Override Operator.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Remove CRDs that were created when the Run Once Duration Override Operator was installed:
.. Navigate to *Administration* -> *CustomResourceDefinitions*.
.. Enter `RunOnceDurationOverride` in the *Name* field to filter the CRDs.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *RunOnceDurationOverride* CRD and select *Delete CustomResourceDefinition*.
.. In the confirmation dialog, click *Delete*.

1. Delete the `openshift-run-once-duration-override-operator` namespace.
.. Navigate to *Administration* -> *Namespaces*.
.. Enter `openshift-run-once-duration-override-operator` into the filter box.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *openshift-run-once-duration-override-operator* entry and select *Delete Namespace*.
.. In the confirmation dialog, enter `openshift-run-once-duration-override-operator` and click *Delete*.

1. Remove the run-once duration override label from the namespaces that it was enabled on.

.. Navigate to *Administration* -> *Namespaces*.
.. Select your namespace.
.. Click *Edit* next to the *Labels* field.
.. Remove the *runoncedurationoverrides.admission.runoncedurationoverride.openshift.io/enabled=true* label and click *Save*.