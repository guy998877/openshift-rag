# Configuring Velero load affinity

With each OADP deployment, there is one Velero pod and its main purpose is to schedule Velero workloads. To schedule the Velero pod, you can use the `velero.podConfig.nodeSelector` and the `velero.loadAffinity` objects in the `DataProtectionApplication` (DPA) custom resource (CR) spec.

Use the `podConfig.nodeSelector` object to assign the Velero pod to specific nodes. You can also configure the `velero.loadAffinity` object for pod-level affinity and anti-affinity. 

The OpenShift scheduler applies the rules and performs the scheduling of the Velero pod deployment.

.Prerequisites

- You must be logged in as a user with `cluster-admin` privileges.
- You have installed the OADP Operator.
- You have configured the DPA CR.

.Procedure

- Configure the `velero.podConfig.nodeSelector` and the `velero.loadAffinity` objects in the DPA spec as shown in the following examples:
- `velero.podConfig.nodeSelector` object configuration:
```yaml
...
spec:
  configuration:
    velero:
      podConfig:
        nodeSelector:
          some-label.io/custom-node-role: backup-core
```

- `velero.loadAffinity` object configuration:
```yaml
...
spec:
  configuration:
    velero:
      loadAffinity:
        - nodeSelector:
            matchLabels:
              label.io/gpu: 'no'
            matchExpressions:
              - key: label.io/location
                operator: In
                values:
                  - US
                  - EU
```

// end of module. Need to add this comment because the level offset attribute does not get unset at the end of this module due to the continuation plus symbol. Causing the level offset from this module to stack on to the next module. This causes build failures or deeply nested modules.