# Amazon EC2 Instance Metadata Service configuration options

You can restrict the version of the Amazon EC2 Instance Metadata Service (IMDS) that machines on Amazon Web Services (AWS) clusters use.
Machines can require the use of [IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) (AWS documentation), or allow the use of IMDSv1 in addition to IMDSv2.

////
This is true but does not apply to TP clusters, reassess for Cluster API GA
> **NOTE:** To use IMDSv2 on AWS clusters that were created with OpenShift Container Platform version 4.6 or earlier, you must update your boot image. For more information, see "Boot image management".
////

> **IMPORTANT:** Before creating machines that require IMDSv2, ensure that any workloads that interact with the IMDS support IMDSv2.

.Sample IMDS configuration
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
# ...
spec:
  template:
    spec:
      instanceMetadataOptions:
        httpEndpoint: enabled
        httpPutResponseHopLimit: 1 <1>
        httpTokens: optional <2>
        instanceMetadataTags: disabled
# ...
```
<1> Specifies the number of network hops allowed for IMDSv2 calls.
If no value is specified, this parameter is set to `1` by default.
<2> Specifies whether to require the use of IMDSv2.
If no value is specified, this parameter is set to `optional` by default.
The following values are valid:
`optional`:: Allow the use of both IMDSv1 and IMDSv2.
`required`:: Require IMDSv2.

> **NOTE:** The Machine API does not support the `httpEndpoint`, `httpPutResponseHopLimit`, and `instanceMetadataTags` fields. If you migrate a Cluster API machine template that uses this feature to a Machine API compute machine set, any Machine API machines that it creates will not have these fields and the underlying instances will not use these settings. Any existing machines that the migrated machine set manages will retain these fields and the underlying instances will continue to use these settings.

Requiring the use of IMDSv2 might cause timeouts.
For more information, including mitigation strategies, see [Instance metadata access considerations](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html#imds-considerations) (AWS documentation).