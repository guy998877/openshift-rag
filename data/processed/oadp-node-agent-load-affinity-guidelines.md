# Node agent load affinity guidelines

Use the following guidelines to configure the node agent `loadAffinity` object in the `DataProtectionApplication` (DPA) custom resource (CR).

- Use the `spec.nodeagent.podConfig.nodeSelector` object for simple node matching.
- Use the `loadAffinity.nodeSelector` object without the `podConfig.nodeSelector` object for more complex scenarios.
- You can use both `podConfig.nodeSelector` and `loadAffinity.nodeSelector` objects, but the `loadAffinity` object must be equal or more restrictive as compared to the `podConfig` object. In this scenario, the `podConfig.nodeSelector` labels must be a subset of the labels used in the `loadAffinity.nodeSelector` object.
- You cannot use the `matchExpressions` and `matchLabels` fields if you have configured both `podConfig.nodeSelector` and `loadAffinity.nodeSelector` objects in the DPA.
- See the following example to configure both `podConfig.nodeSelector` and `loadAffinity.nodeSelector` objects in the DPA.
```yaml
...
spec:
  configuration:
    nodeAgent:
      enable: true
      uploaderType: kopia
      loadAffinity:
        - nodeSelector:
            matchLabels:
              label.io/location: 'US'
              label.io/gpu: 'no'
      podConfig:
        nodeSelector:
          label.io/gpu: 'no'
```