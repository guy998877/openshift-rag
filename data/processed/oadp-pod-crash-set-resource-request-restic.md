# Setting resource requests for a Restic pod

Use the `configuration.restic.podConfig.resourceAllocations` specification field to set specific resource requests for a `Restic` pod.

.Procedure

- Set the `cpu` and `memory` resource requests as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
...
configuration:
  restic:
    podConfig:
      resourceAllocations:
        requests:
          cpu: 1000m
          memory: 16Gi
```
The `resourceAllocations` listed are for average usage.