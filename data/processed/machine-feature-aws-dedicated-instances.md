# Dedicated Instance configuration options

You can deploy machines that are backed by Dedicated Instances on Amazon Web Services (AWS) clusters. 

Dedicated Instances run in a virtual private cloud (VPC) on hardware that is dedicated to a single customer. 
These Amazon EC2 instances are physically isolated at the host hardware level. 
The isolation of Dedicated Instances occurs even if the instances belong to different AWS accounts that are linked to a single payer account. 
However, other instances that are not dedicated can share hardware with Dedicated Instances if they belong to the same AWS account.

OpenShift Container Platform supports instances with public or dedicated tenancy.

.Sample Dedicated Instances configuration
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
# ...
spec:
  template:
    spec:
      tenancy: dedicated <1>
# ...
```
<1> Specifies using instances with dedicated tenancy that run on single-tenant hardware.
If you do not specify this value, instances with public tenancy that run on shared hardware are used by default.