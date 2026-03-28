# Accessing the Velero binary in the Velero deployment in the cluster

Use a shell command to access the Velero binary in the Velero deployment in the cluster.

.Prerequisites

- Your `DataProtectionApplication` custom resource has a status of `Reconcile complete`.

.Procedure

- Set the needed alias by using the following command:
```bash
$ alias velero='oc -n openshift-adp exec deployment/velero -c velero -it -- ./velero'
```