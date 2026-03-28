# Removing Secondary Scheduler Operator resources

Optionally, remove the custom resource definition (CRD) and associated namespace after the Secondary Scheduler Operator for Red Hat OpenShift is uninstalled. This cleans up all remaining secondary scheduler artifacts.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- You have access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Remove the CRD that was installed by the Secondary Scheduler Operator:
.. Navigate to *Administration* -> *CustomResourceDefinitions*.
.. Enter `SecondaryScheduler` in the *Name* field to filter the CRDs.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *SecondaryScheduler* CRD and select *Delete Custom Resource Definition*:

1. Remove the `openshift-secondary-scheduler-operator` namespace.
.. Navigate to *Administration* -> *Namespaces*.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *openshift-secondary-scheduler-operator* and select *Delete Namespace*.
.. In the confirmation dialog, enter `openshift-secondary-scheduler-operator` in the field and click *Delete*.