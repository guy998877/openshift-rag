# Enabling the run-once duration override on a namespace

To apply the run-once duration override from the Run Once Duration Override Operator to run-once pods, you must enable it on each applicable namespace.

.Prerequisites

- The Run Once Duration Override Operator is installed.

.Procedure

1. Log in to the OpenShift CLI.

1. Add the label to enable the run-once duration override to your namespace:
```bash
$ oc label namespace <namespace> \ <1>
    runoncedurationoverrides.admission.runoncedurationoverride.openshift.io/enabled=true
```
<1> Specify the namespace to enable the run-once duration override on.

After you enable the run-once duration override on this namespace, future run-once pods that are created in this namespace will have their `activeDeadlineSeconds` field set to the override value from the Run Once Duration Override Operator. Existing pods in this namespace will also have their `activeDeadlineSeconds` value set when they are updated next.

.Verification

1. Create a test run-once pod in the namespace that you enabled the run-once duration override on:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example
  namespace: <namespace>                 <1>
spec:
  restartPolicy: Never                   <2>
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: busybox
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
      image: busybox:1.25
      command:
        - /bin/sh
        - -ec
        - |
          while sleep 5; do date; done
```
<1> Replace `<namespace>` with the name of your namespace.
<2> The `restartPolicy` must be `Never` or `OnFailure` to be a run-once pod.

1. Verify that the pod has its `activeDeadlineSeconds` field set:
```bash
$ oc get pods -n <namespace> -o yaml | grep activeDeadlineSeconds
```
.Example output
```bash
    activeDeadlineSeconds: 3600
```