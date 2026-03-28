# Installing the Secondary Scheduler Operator

You can install the Secondary Scheduler Operator for Red Hat OpenShift through the OpenShift Container Platform web console to configure a secondary scheduler.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- You have access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Create the required namespace for the Secondary Scheduler Operator for Red Hat OpenShift.
.. Navigate to *Administration* -> *Namespaces* and click *Create Namespace*.
.. Enter `openshift-secondary-scheduler-operator` in the *Name* field and click *Create*.
// There are no metrics to collect for the secondary scheduler operator as of now, so no need to add the metrics label

1. Install the Secondary Scheduler Operator for Red Hat OpenShift.
.. Navigate to *Ecosystem* -> *Software Catalog*.
.. Enter *Secondary Scheduler Operator for Red Hat OpenShift* into the filter box.
.. Select the *Secondary Scheduler Operator for Red Hat OpenShift* and click *Install*.
.. On the *Install Operator* page:
... The *Update channel* is set to *stable*, which installs the latest stable release of the Secondary Scheduler Operator for Red Hat OpenShift.
... Select *A specific namespace on the cluster* and select *openshift-secondary-scheduler-operator* from the drop-down menu.
... Select an *Update approval* strategy.
- The *Automatic* strategy allows Operator Lifecycle Manager (OLM) to automatically update the Operator when a new version is available.
- The *Manual* strategy requires a user with appropriate credentials to approve the Operator update.
... Click *Install*.

.Verification

1. Navigate to *Ecosystem* -> *Installed Operators*.
1. Verify that *Secondary Scheduler Operator for Red Hat OpenShift* is listed with a *Status* of *Succeeded*.