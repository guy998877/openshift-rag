# Enabling feature sets using the CLI

You can use the OpenShift CLI (`oc`) to enable feature sets for all of the nodes in a cluster by editing the `FeatureGate` custom resource (CR). Completing this task enables non-default features in your cluster.

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

- Edit the `FeatureGate` CR named `cluster`:
```bash
$ oc edit featuregate cluster
```
> **WARNING:** Enabling the `TechPreviewNoUpgrade` feature set on your cluster cannot be undone and prevents minor version updates. You should not enable this feature set on production clusters.
.Sample FeatureGate custom resource
```yaml
apiVersion: config.openshift.io/v1
kind: FeatureGate
metadata:
  name: cluster
# ...
spec:
  featureSet: TechPreviewNoUpgrade
```
where:
--
`metadata.name`:: Specifies the name of the `FeatureGate` CR. This must be `cluster`.

`spec.featureSet`:: Specifies the feature set that you want to enable:
- `TechPreviewNoUpgrade` enables specific Technology Preview features.
--
After you save the changes, new machine configs are created, the machine config pools are updated, and scheduling on each node is disabled while the change is being applied.

.Verification