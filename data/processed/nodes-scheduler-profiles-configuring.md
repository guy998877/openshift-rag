# Configuring a scheduler profile

You can configure the scheduler to use a scheduler profile.

.Prerequisites

- Access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. Edit the `Scheduler` object:
```bash
$ oc edit scheduler cluster
```

1. Specify the profile to use in the `spec.profile` field:
```yaml
apiVersion: config.openshift.io/v1
kind: Scheduler
metadata:
  name: cluster
#...
spec:
  mastersSchedulable: false
  profile: HighNodeUtilization <1>
#...
```
<1> Set to `LowNodeUtilization`, `HighNodeUtilization`, or `NoScoring`.

1. Save the file to apply the changes.