# Scheduling a pod using the secondary scheduler

To schedule a pod by using the secondary scheduler, set the `schedulerName` field in the pod definition.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- You have access to the OpenShift Container Platform web console.
- The Secondary Scheduler Operator for Red Hat OpenShift is installed.
- A secondary scheduler is configured.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Navigate to *Workloads* -> *Pods*.
1. Click *Create Pod*.
1. In the YAML editor, enter the desired pod configuration and add the `schedulerName` field:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: default
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: nginx
      image: nginx:1.14.2
      ports:
        - containerPort: 80
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
  schedulerName: secondary-scheduler
```
The `spec.schedulerName` field must match the name that is defined in the config map when you configured the secondary scheduler.

1. Click *Create*.

.Verification

1. Log in to the OpenShift CLI.
1. Describe the pod using the following command:
```bash
$ oc describe pod nginx -n default
```
.Example output
```text
Name:         nginx
Namespace:    default
Priority:     0
Node:         ci-ln-t0w4r1k-72292-xkqs4-worker-b-xqkxp/10.0.128.3
...
Events:
  Type    Reason          Age   From                 Message
  ----    ------          ----  ----                 -------
  Normal  Scheduled       12s   secondary-scheduler  Successfully assigned default/nginx to ci-ln-t0w4r1k-72292-xkqs4-worker-b-xqkxp
...
```

1. In the events table, find the event with a message similar to `Successfully assigned <namespace>/<pod_name> to <node_name>`.
1. In the "From" column, verify that the event was generated from the secondary scheduler and not the default scheduler.
> **NOTE:** You can also check the `secondary-scheduler-*` pod logs in the `openshift-secondary-scheduler-namespace` to verify that the pod was scheduled by the secondary scheduler.

////
Due to a UI bug, can't verify via console. Bug should be fixed in 4.11 hopefully, and if so, update to use the console steps:

.Verification
1. Navigate to the *Events* tab for the pod.
1. Find the event with a message similar to `Successfully assigned <namespace>/<pod_name> to <node_name>`.
1. Verify that the event was generated from the secondary scheduler and not the default scheduler.
////