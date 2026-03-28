# Updating LVM Storage

You can update LVM Storage to ensure compatibility with the OpenShift Container Platform version.

> **NOTE:** The default namespace for the LVM Storage Operator is `openshift-lvm-storage`.

.Prerequisites

- You have updated your OpenShift Container Platform cluster.

- You have installed a previous version of LVM Storage.

- You have installed the OpenShift CLI (`oc`).

- You have access to the cluster using an account with `cluster-admin` permissions.

.Procedure

1. Log in to the OpenShift CLI (`oc`).

1. Update the `Subscription` custom resource (CR) that you created while installing LVM Storage by running the following command:
```bash
$ oc patch subscription lvms-operator -n openshift-lvm-storage --type merge --patch '{"spec":{"channel":"<update_channel>"}}' <1>
```
<1> Replace `<update_channel>` with the version of LVM Storage that you want to install. For example, `stable-4.21`.

1. View the update events to check that the installation is complete by running the following command:
```bash
$ oc get events -n openshift-lvm-storage
```
.Example output
```bash
...
8m13s       Normal    RequirementsUnknown   clusterserviceversion/lvms-operator.v4.21   requirements not yet checked
8m11s       Normal    RequirementsNotMet    clusterserviceversion/lvms-operator.v4.21   one or more requirements couldn't be found
7m50s       Normal    AllRequirementsMet    clusterserviceversion/lvms-operator.v4.21   all requirements found, attempting install
7m50s       Normal    InstallSucceeded      clusterserviceversion/lvms-operator.v4.21   waiting for install components to report healthy
7m49s       Normal    InstallWaiting        clusterserviceversion/lvms-operator.v4.21   installing: waiting for deployment lvms-operator to become ready: deployment "lvms-operator" waiting for 1 outdated replica(s) to be terminated
7m39s       Normal    InstallSucceeded      clusterserviceversion/lvms-operator.v4.21   install strategy completed with no errors
...
```

.Verification

- Verify the LVM Storage version by running the following command:
```bash
$ oc get subscription lvms-operator -n openshift-lvm-storage -o jsonpath='{.status.installedCSV}'
```
.Example output
```bash
lvms-operator.v4.21
---- 
```