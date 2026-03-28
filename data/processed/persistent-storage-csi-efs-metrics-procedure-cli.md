# Enabling usage metrics using the CLI

To enable Amazon Web Services (AWS) Elastic File Service (EFS) storage Container Storage Interface (CSI) usage metrics using the CLI:

1. Edit ClusterCSIDriver by running the following command:
```bash
$ oc edit clustercsidriver efs.csi.aws.com
```

1. Under `spec.aws.efsVolumeMetrics.state`, set the value to `RecursiveWalk`.
`RecursiveWalk` indicates that volume metrics collection in the AWS EFS CSI Driver is performed by recursively walking through the files in the volume.
.Example ClusterCSIDriver efs.csi.aws.com YAML file
```yaml
spec:
    driverConfig:
        driverType: AWS
        aws:
            efsVolumeMetrics:
              state: RecursiveWalk
              recursiveWalk:
                refreshPeriodMinutes: 100
                fsRateLimit: 10
```

1. Optional: To define how the recursive walk operates, you can also set the following fields:
- `refreshPeriodMinutes`: Specifies the refresh frequency for volume metrics in minutes. If this field is left blank, a reasonable default is chosen, which is subject to change over time. The current default is 240 minutes. The valid range is 1 to 43,200 minutes.
- `fsRateLimit`: Defines the rate limit for processing volume metrics in goroutines per file system. If this field is left blank, a reasonable default is chosen, which is subject to change over time. The current default is 5 goroutines. The valid range is 1 to 100 goroutines.

1. Save the changes to the `efs.csi.aws.com` object.

> **NOTE:** To *disable* AWS EFS CSI usage metrics, use the preceding procedure, but for `spec.aws.efsVolumeMetrics.state`, change the value from `RecursiveWalk` to `Disabled`.