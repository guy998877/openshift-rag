# Updating the OLM Operators

Software needs to vetted before it is loaded onto a production cluster.
Production clusters are also quite often configured in disconnected network, which means that they are not always directly connected to the internet.
Because the clusters are in a disconnected network, the OpenShift Container Platform Operators are configured for manual update during installation so that new versions can be managed on a cluster-by-cluster basis.
Complete the following procedure to move the Operators to the newer versions.

.Procedure

1. Check to see which Operators need to be updated:
```bash
$ oc get installplan -A | grep -E 'APPROVED|false'
```
.Example output
```bash
NAMESPACE           NAME            CSV                                               APPROVAL   APPROVED
metallb-system      install-nwjnh   metallb-operator.v4.16.0-202409202304             Manual     false
openshift-nmstate   install-5r7wr   kubernetes-nmstate-operator.4.16.0-202409251605   Manual     false
```

1. Patch the `InstallPlan` resources for those Operators:
```bash
$ oc patch installplan -n metallb-system install-nwjnh --type merge --patch \
'{"spec":{"approved":true}}'
```
.Example output
```bash
installplan.operators.coreos.com/install-nwjnh patched
```

1. Monitor the namespace by running the following command:
```bash
$ oc get all -n metallb-system
```
.Example output
```bash
NAME                                                       READY   STATUS              RESTARTS   AGE
pod/metallb-operator-controller-manager-69b5f884c-8bp22    0/1     ContainerCreating   0          4s
pod/metallb-operator-controller-manager-77895bdb46-bqjdx   1/1     Running             0          4m1s
pod/metallb-operator-webhook-server-5d9b968896-vnbhk       0/1     ContainerCreating   0          4s
pod/metallb-operator-webhook-server-d76f9c6c8-57r4w        1/1     Running             0          4m1s

...

NAME                                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/metallb-operator-controller-manager-69b5f884c    1         1         0       4s
replicaset.apps/metallb-operator-controller-manager-77895bdb46   1         1         1       4m1s
replicaset.apps/metallb-operator-controller-manager-99b76f88     0         0         0       4m40s
replicaset.apps/metallb-operator-webhook-server-5d9b968896       1         1         0       4s
replicaset.apps/metallb-operator-webhook-server-6f7dbfdb88       0         0         0       4m40s
replicaset.apps/metallb-operator-webhook-server-d76f9c6c8        1         1         1       4m1s
```
When the update is complete, the required pods should be in a `Running` state, and the required `ReplicaSet` resources should be ready:
```bash
NAME                                                      READY   STATUS    RESTARTS   AGE
pod/metallb-operator-controller-manager-69b5f884c-8bp22   1/1     Running   0          25s
pod/metallb-operator-webhook-server-5d9b968896-vnbhk      1/1     Running   0          25s

...

NAME                                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/metallb-operator-controller-manager-69b5f884c    1         1         1       25s
replicaset.apps/metallb-operator-controller-manager-77895bdb46   0         0         0       4m22s
replicaset.apps/metallb-operator-webhook-server-5d9b968896       1         1         1       25s
replicaset.apps/metallb-operator-webhook-server-d76f9c6c8        0         0         0       4m22s
```

.Verification

- Verify that the Operators do not need to be updated for a second time:
```bash
$ oc get installplan -A | grep -E 'APPROVED|false'
```
There should be no output returned.
> **NOTE:** Sometimes you have to approve an update twice because some Operators have interim z-stream release versions that need to be installed before the final version.