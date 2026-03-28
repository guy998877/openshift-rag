# Installing the Multiarch Tuning Operator by using the web console

You can install the Multiarch Tuning Operator by using the OpenShift Container Platform web console.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.

- You have access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Navigate to *Ecosystem* -> *Software Catalog*.
1. Enter *Multiarch Tuning Operator* in the search field.
1. Click *Multiarch Tuning Operator*.
1. Select the *Multiarch Tuning Operator* version from the *Version* list.
1. Click *Install*
1. Set the following options on the *Operator Installation* page:
.. Set *Update Channel* to *stable*.
.. Set *Installation Mode* to *All namespaces on the cluster*.
.. Set *Installed Namespace* to *Operator recommended Namespace* or *Select a Namespace*.
The recommended Operator namespace is `openshift-multiarch-tuning-operator`. If the `openshift-multiarch-tuning-operator` namespace does not exist, it is created during the operator installation.
If you select *Select a namespace*, you must select a namespace for the Operator from the *Select Project* list.
.. *Update approval* as *Automatic* or *Manual*.
If you select *Automatic* updates, Operator Lifecycle Manager (OLM) automatically updates the running instance of the Multiarch Tuning Operator without any intervention.
If you select *Manual* updates, OLM creates an update request.
As a cluster administrator, you must manually approve the update request to update the Multiarch Tuning Operator to a newer version.

1. Optional: Select the *Enable Operator recommended cluster monitoring on this Namespace* checkbox.
1. Click *Install*.

.Verification

1. Navigate to *Ecosystem* -> *Installed Operators*.
1. Verify that the *Multiarch Tuning Operator* is listed with the *Status* field as *Succeeded* in the `openshift-multiarch-tuning-operator` namespace.