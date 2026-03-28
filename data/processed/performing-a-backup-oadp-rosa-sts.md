# Performing a backup with OADP and OpenShift Container Platform

The following example `hello-world` application has no persistent volumes (PVs) attached. Perform a backup by using OpenShift API for Data Protection (OADP) with OpenShift Container Platform.

Either Data Protection Application (DPA) configuration will work.

.Procedure

1. Create a workload to back up by running the following commands:
```bash
$ oc create namespace hello-world
```
```bash
$ oc new-app -n hello-world --image=docker.io/openshift/hello-openshift
```

1. Expose the route by running the following command:
```bash
$ oc expose service/hello-openshift -n hello-world
```

1. Check that the application is working by running the following command:
```bash
$ curl `oc get route/hello-openshift -n hello-world -o jsonpath='{.spec.host}'`
```
You should see an output similar to the following example:
```bash
Hello OpenShift!
```

1. Back up the workload by running the following command:
```bash
$ cat << EOF | oc create -f -
  apiVersion: velero.io/v1
  kind: Backup
  metadata:
    name: hello-world
    namespace: openshift-adp
  spec:
    includedNamespaces:
    - hello-world
    storageLocation: ${CLUSTER_NAME}-dpa-1
    ttl: 720h0m0s
EOF
```

1. Wait until the backup is complete, and then run the following command:
```bash
$ watch "oc -n openshift-adp get backup hello-world -o json | jq .status"
```
You should see an output similar to the following example:
```json
{
  "completionTimestamp": "2022-09-07T22:20:44Z",
  "expiration": "2022-10-07T22:20:22Z",
  "formatVersion": "1.1.0",
  "phase": "Completed",
  "progress": {
    "itemsBackedUp": 58,
    "totalItems": 58
  },
  "startTimestamp": "2022-09-07T22:20:22Z",
  "version": 1
}
```

1. Delete the demo workload by running the following command:
```bash
$ oc delete ns hello-world
```

1. Restore the workload from the backup by running the following command:
```bash
$ cat << EOF | oc create -f -
  apiVersion: velero.io/v1
  kind: Restore
  metadata:
    name: hello-world
    namespace: openshift-adp
  spec:
    backupName: hello-world
EOF
```

1. Wait for the Restore to finish by running the following command:
```bash
$ watch "oc -n openshift-adp get restore hello-world -o json | jq .status"
```
You should see an output similar to the following example:
```json
{
  "completionTimestamp": "2022-09-07T22:25:47Z",
  "phase": "Completed",
  "progress": {
    "itemsRestored": 38,
    "totalItems": 38
  },
  "startTimestamp": "2022-09-07T22:25:28Z",
  "warnings": 9
}
```

1. Check that the workload is restored by running the following command:
```bash
$ oc -n hello-world get pods
```
You should see an output similar to the following example:
```bash
NAME                              READY   STATUS    RESTARTS   AGE
hello-openshift-9f885f7c6-kdjpj   1/1     Running   0          90s
```
1. Check the JSONPath by running the following command:
```bash
$ curl `oc get route/hello-openshift -n hello-world -o jsonpath='{.spec.host}'`
```
You should see an output similar to the following example:
```bash
Hello OpenShift!
```

> **NOTE:** For troubleshooting tips, see the link:https://access.redhat.com/articles/5456281[troubleshooting documentation].