# Enabling feature sets using the web console

You can use the OpenShift Container Platform web console to enable feature sets for all of the nodes in a cluster by editing the `FeatureGate` custom resource (CR). Completing this task enables non-default features in your cluster.

.Procedure

1. In the OpenShift Container Platform web console, switch to the *Administration* -> *Custom Resource Definitions* page.

1. On the *Custom Resource Definitions* page, click *FeatureGate*.

1. On the *Custom Resource Definition Details* page, click the *Instances* tab.

1. Click the *cluster* feature gate, then click the *YAML* tab.

1. Edit the *cluster* instance to add specific feature sets:
> **WARNING:** Enabling the `TechPreviewNoUpgrade` feature set on your cluster cannot be undone and prevents minor version updates. You should not enable this feature set on production clusters.

.Sample Feature Gate custom resource
```yaml
apiVersion: config.openshift.io/v1
kind: FeatureGate
metadata:
  name: cluster <1>
# ...
spec:
  featureSet: TechPreviewNoUpgrade <2>
```
where:
--
`metadata.name`:: Specifies the name of the `FeatureGate` CR. You must specify `cluster` for the name.

`spec.featureSet`:: Specifies the feature set that you want to enable:
- `TechPreviewNoUpgrade` enables specific Technology Preview features.
--
After you save the changes, new machine configs are created, the machine config pools are updated, and scheduling on each node is disabled while the change is being applied.

.Verification