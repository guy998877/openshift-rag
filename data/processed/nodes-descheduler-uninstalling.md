# Uninstalling the descheduler

If you no longer need the descheduler in your cluster, you can remove it by deleting the descheduler instance and uninstalling the Kube Descheduler Operator. You can also delete the `KubeDescheduler` CRD and `openshift-kube-descheduler-operator` namespace.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- Access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Delete the descheduler instance.
.. From the *Ecosystem* -> *Installed Operators* page, click *Kube Descheduler Operator*.
.. Select the *Kube Descheduler* tab.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *cluster* entry and select *Delete KubeDescheduler*.
.. In the confirmation dialog, click *Delete*.
1. Uninstall the Kube Descheduler Operator.
.. Navigate to *Ecosystem* -> *Installed Operators*.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *Kube Descheduler Operator* entry and select *Uninstall Operator*.
.. In the confirmation dialog, click *Uninstall*.
1. Delete the `openshift-kube-descheduler-operator` namespace.
.. Navigate to *Administration* -> *Namespaces*.
.. Enter `openshift-kube-descheduler-operator` into the filter box.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *openshift-kube-descheduler-operator* entry and select *Delete Namespace*.
.. In the confirmation dialog, enter `openshift-kube-descheduler-operator` and click *Delete*.
1. Delete the `KubeDescheduler` CRD.
.. Navigate to *Administration* -> *Custom Resource Definitions*.
.. Enter `KubeDescheduler` into the filter box.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *KubeDescheduler* entry and select *Delete CustomResourceDefinition*.
.. In the confirmation dialog, click *Delete*.