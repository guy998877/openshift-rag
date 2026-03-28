# Setting resource requests for a Velero pod

Use the `configuration.velero.podConfig.resourceAllocations` specification field in the `oadp_v1alpha1_dpa.yaml` file to set specific resource requests for a `Velero` pod.

.Procedure

- Set the `cpu` and `memory` resource requests as shown in the following example:
```yaml
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
...
configuration:
  velero:
    podConfig:
      resourceAllocations:
        requests:
          cpu: 200m
          memory: 256Mi
```
The `resourceAllocations` listed are for average usage.