# Running a pod with a different service account

You can run a pod with a service account other than the default.

.Procedure

1. Edit the `DeploymentConfig` object:
```bash
$ oc edit dc/<deployment_config>
```

1. Add the `serviceAccount` and `serviceAccountName` parameters to the `spec` field, and specify the service account you want to use:
```yaml
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: example-dc
# ...
spec:
# ...
  securityContext: {}
  serviceAccount: <service_account>
  serviceAccountName: <service_account>
```