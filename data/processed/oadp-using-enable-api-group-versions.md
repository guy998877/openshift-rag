# Using Enable API Group Versions

You can use Velero's Enable API Group Versions feature to back up _all_ Kubernetes API group versions that are supported on a cluster, not only the preferred one.

> **NOTE:** Enable API Group Versions is still in beta.

.Procedure

- Configure the `EnableAPIGroupVersions` feature flag:

```yaml
apiVersion: oadp.openshift.io/vialpha1
kind: DataProtectionApplication
...
spec:
  configuration:
    velero:
      featureFlags:
      - EnableAPIGroupVersions
```

.Additional resources
- link:https://velero.io/docs/v1.9/enable-api-group-versions-feature/[Enable API Group Versions Feature]