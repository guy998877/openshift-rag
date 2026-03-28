# Investigating a PVC stuck in the Pending state

A persistent volume claim (PVC) can get stuck in the `Pending` state for the following reasons:

- Insufficient computing resources.
- Network problems.
- Mismatched storage class or node selector.
- No available persistent volumes (PVs).
- The node with the PV is in the `Not Ready` state.

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You have logged in to the pass:quotes[OpenShift CLI (`oc`)] as a user with `cluster-admin` permissions.

.Procedure

1. Retrieve the list of PVCs by running the following command:
```bash
$ oc get pvc
```
.Example output
```bash
NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
lvms-test   Pending                                      lvms-vg1       11s
```

1. Inspect the events associated with a PVC stuck in the `Pending` state by running the following command:
```bash
$ oc describe pvc <pvc_name> <1>
```
<1> Replace `<pvc_name>` with the name of the PVC. For example, `lvms-vg1`.
.Example output
```bash
Type     Reason              Age               From                         Message
----     ------              ----              ----                         -------
Warning  ProvisioningFailed  4s (x2 over 17s)  persistentvolume-controller  storageclass.storage.k8s.io "lvms-vg1" not found
```