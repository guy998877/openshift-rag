# Deleting a persistent volume claim

You can delete a persistent volume claim (PVC) by using the OpenShift CLI (`oc`).

.Prerequisites

- You have access to OpenShift Container Platform as a user with `cluster-admin` permissions.

.Procedure

1. Log in to the OpenShift CLI (`oc`).

1. Delete the PVC by running the following command:
```bash
$ oc delete pvc <pvc_name> -n <namespace>
```

.Verification

- To verify that the PVC is deleted, run the following command:
```bash
$ oc get pvc -n <namespace>
```
The deleted PVC must not be present in the output of this command.