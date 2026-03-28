# Recovering from node failure

A persistent volume claim (PVC) can be stuck in the `Pending` state due to a node failure in the cluster. 

To identify the failed node, you can examine the restart count of the `topolvm-node` pod. An increased restart count indicates potential problems with the underlying node, which might require further investigation and troubleshooting.

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You have logged in to the pass:quotes[OpenShift CLI (`oc`)] as a user with `cluster-admin` permissions.

.Procedure

- Examine the restart count of the `topolvm-node` pod instances by running the following command:
```bash
$ oc get pods -n <namespace>
```
.Example output
```bash
NAME                                  READY   STATUS    RESTARTS      AGE
lvms-operator-7b9fb858cb-6nsml        3/3     Running   0             70m
topolvm-controller-5dd9cf78b5-7wwr2   5/5     Running   0             66m
topolvm-node-dr26h                    4/4     Running   0             66m
topolvm-node-54as8                    4/4     Running   0             66m
topolvm-node-78fft                    4/4     Running   17 (8s ago)   66m
vg-manager-r6zdv                      1/1     Running   0             66m
vg-manager-990ut                      1/1     Running   0             66m
vg-manager-an118                      1/1     Running   0             66m
```

.Next steps

- If the PVC is stuck in the `Pending` state even after you have resolved any issues with the node, you must perform a forced clean-up. For more information, see "Performing a forced clean-up".