# Uninstalling the Run Once Duration Override Operator

You can use the web console to uninstall the Run Once Duration Override Operator. Uninstalling the Run Once Duration Override Operator does not unset the `activeDeadlineSeconds` field for run-once pods, but it will no longer apply the override value to future run-once pods.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.
- You have installed the Run Once Duration Override Operator.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Navigate to *Ecosystem* -> *Installed Operators*.

1. Select `openshift-run-once-duration-override-operator` from the *Project* dropdown list.

1. Delete the `RunOnceDurationOverride` instance.
.. Click *Run Once Duration Override Operator* and select the *Run Once Duration Override* tab.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *cluster* entry and select *Delete RunOnceDurationOverride*.
.. In the confirmation dialog, click *Delete*.

1. Uninstall the Run Once Duration Override Operator.
.. Navigate to *Ecosystem* -> *Installed Operators*.
.. Click the Options menu image:kebab.png[title="Options menu"] next to the *Run Once Duration Override Operator* entry and click *Uninstall Operator*.
.. In the confirmation dialog, click *Uninstall*.