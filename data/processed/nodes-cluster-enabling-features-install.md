# Enabling feature sets at installation

You can enable feature sets for all nodes in the cluster by editing the `install-config.yaml` file before you deploy the cluster. This allows you to use non-default features in your cluster.

.Prerequisites

- You have an `install-config.yaml` file.

.Procedure

1. Use the `featureSet` parameter to specify the name of the feature set you want to enable, such as `TechPreviewNoUpgrade`:
> **WARNING:** Enabling the `TechPreviewNoUpgrade` feature set on your cluster cannot be undone and prevents minor version updates. You should not enable this feature set on production clusters.
.Sample `install-config.yaml` file with an enabled feature set

```yaml
compute:
- hyperthreading: Enabled
  name: worker
  platform:
    aws:
      rootVolume:
        iops: 2000
        size: 500
        type: io1
      metadataService:
        authentication: Optional
      type: c5.4xlarge
      zones:
      - us-west-2c
  replicas: 3
featureSet: TechPreviewNoUpgrade
```

1. Save the file and reference it when using the installation program to deploy the cluster.

.Verification