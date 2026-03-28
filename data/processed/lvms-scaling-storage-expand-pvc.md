# Expanding a persistent volume claim

After scaling up the storage of a cluster, you can expand the existing persistent volume claims (PVCs). 

To expand a PVC, you must update the `storage` field in the PVC.

.Prerequisites

- Dynamic provisioning is used.
- The `StorageClass` object associated with the PVC has the `allowVolumeExpansion` field set to `true`.

.Procedure

1. Log in to the OpenShift CLI (`oc`).

1. Update the value of the `spec.resources.requests.storage` field to a value that is greater than the current value by running the following command:
```bash
$ oc patch pvc <pvc_name> -n <application_namespace> \ <1>
  --type=merge -p \ '{ "spec": { "resources": { "requests": { "storage": "<desired_size>" }}}}' <2>
```
<1> Replace `<pvc_name>` with the name of the PVC that you want to expand.
<2> Replace `<desired_size>` with the new size to expand the PVC.

.Verification

- To verify that resizing is completed, run the following command:
```bash
$ oc get pvc <pvc_name> -n <application_namespace> -o=jsonpath={.status.capacity.storage}
```
LVM Storage adds the `Resizing` condition to the PVC during expansion. It deletes the `Resizing` condition after the PVC expansion.