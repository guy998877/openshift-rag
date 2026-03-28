# Ensuring that layered products are compatible with the update

Verify that all layered products run on the version of OpenShift Container Platform that you are updating to before you begin the update.
This generally includes all Operators.

.Procedure

1. Verify the currently installed Operators in the cluster.
For example, run the following command:
```bash
$ oc get csv -A
```
.Example output
```bash
NAMESPACE                              NAME            DISPLAY          VERSION   REPLACES                             PHASE
gitlab-operator-kubernetes.v0.17.2     GitLab                           0.17.2    gitlab-operator-kubernetes.v0.17.1   Succeeded
openshift-operator-lifecycle-manager   packageserver   Package Server   0.19.0                                         Succeeded
```

1. Check that Operators that you install with OLM are compatible with the update version.
--
Operators that are installed with the Operator Lifecycle Manager (OLM) are not part of the standard cluster Operators set.

Use the [Operator Update Information Checker](https://access.redhat.com/labs/ocpouic/?upgrade_path=4.14%20to%204.16) to understand if you must update an Operator after each y-stream update or if you can wait until you have fully updated to the next EUS release.

> **TIP:** You can also use the link:https://access.redhat.com/labs/ocpouic/?upgrade_path=4.14%20to%204.16[Operator Update Information Checker] to see what versions of OpenShift Container Platform are compatible with specific releases of an Operator.
--

1. Check that Operators that you install outside of OLM are compatible with the update version.
--
For all OLM-installed Operators that are not directly supported by Red Hat, contact the Operator vendor to ensure release compatibility.

- Some Operators are compatible with several releases of OpenShift Container Platform.
See "Updating the worker nodes" for more information.

- See "Updating all the OLM Operators" for information about updating an Operator after performing the first y-stream control plane update.
--