# Configuring storage throughput for gp3 drives

You can improve performance for high traffic services by increasing the throughput of gp3 storage volumes in an AWS cluster.
You can configure the storage throughput for the root volume, non root volumes, or both.

.Prerequisites

- You use gp3 storage volume(s).

.Procedure

- On the machine template in which you want to configure throughput, add the `throughput` parameter:
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
# ...
spec:
  template:
    spec:
      nonRootVolumes:
      - throughput: <throughput_value>
      rootVolume:
        throughput: <throughput_value>
# ...
```
where:

`<throughput_value>`::
Specifies a value in MiB per second between 125 and 2,000.
You can only edit this value on gp3 volumes.
The default value is `125`.