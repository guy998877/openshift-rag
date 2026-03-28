# Updating the run-once active deadline override value

You can customize the override value that the Run Once Duration Override Operator applies to run-once pods. The predefined value is `3600` seconds, or 1 hour.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have installed the Run Once Duration Override Operator.

.Procedure

1. Log in to the OpenShift CLI.

1. Edit the `RunOnceDurationOverride` resource:
```bash
$ oc edit runoncedurationoverride cluster
```

1. Update the `activeDeadlineSeconds` field:
```yaml
apiVersion: operator.openshift.io/v1
kind: RunOnceDurationOverride
metadata:
# ...
spec:
  runOnceDurationOverride:
    spec:
      activeDeadlineSeconds: 1800 <1>
# ...
```
<1> Set the `activeDeadlineSeconds` field to the desired value, in seconds.

1. Save the file to apply the changes.

Any future run-once pods created in namespaces where the run-once duration override is enabled will have their `activeDeadlineSeconds` field set to this new value. Existing run-once pods in these namespaces will receive this new value when they are updated.