# Installing the Run Once Duration Override Operator

You can use the web console to install the Run Once Duration Override Operator.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Create the required namespace for the Run Once Duration Override Operator.
.. Navigate to *Administration* -> *Namespaces* and click *Create Namespace*.
.. Enter `openshift-run-once-duration-override-operator` in the *Name* field and click *Create*.

1. Install the Run Once Duration Override Operator.
.. Navigate to *Ecosystem* -> *Software Catalog*.
.. Enter *Run Once Duration Override Operator* into the filter box.
.. Select the *Run Once Duration Override Operator* and click *Install*.
.. On the *Install Operator* page:
... The *Update channel* is set to *stable*, which installs the latest stable release of the Run Once Duration Override Operator.
... Select *A specific namespace on the cluster*.
... Choose *openshift-run-once-duration-override-operator* from the dropdown menu under *Installed namespace*.
... Select an *Update approval* strategy.
- The *Automatic* strategy allows Operator Lifecycle Manager (OLM) to automatically update the Operator when a new version is available.
- The *Manual* strategy requires a user with appropriate credentials to approve the Operator update.
... Click *Install*.

1. Create a `RunOnceDurationOverride` instance.
.. From the *Ecosystem* -> *Installed Operators* page, click *Run Once Duration Override Operator*.
.. Select the *Run Once Duration Override* tab and click *Create RunOnceDurationOverride*.
.. Edit the settings as necessary.
Under the `runOnceDurationOverride` section, you can update the `spec.activeDeadlineSeconds` value, if required. The predefined value is `3600` seconds, or 1 hour.

.. Click *Create*.

.Verification

1. Log in to the OpenShift CLI.

1. Verify all pods are created and running properly.
```bash
$ oc get pods -n openshift-run-once-duration-override-operator
```
.Example output
```bash
NAME                                                   READY   STATUS    RESTARTS   AGE
run-once-duration-override-operator-7b88c676f6-lcxgc   1/1     Running   0          7m46s
runoncedurationoverride-62blp                          1/1     Running   0          41s
runoncedurationoverride-h8h8b                          1/1     Running   0          41s
runoncedurationoverride-tdsqk                          1/1     Running   0          41s
```