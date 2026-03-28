# Assigning machines to placement groups for Elastic Fabric Adapter instances by using machine sets

You can configure a machine set to deploy machines on [Elastic Fabric Adapter](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html) (EFA) instances within an existing AWS placement group.

EFA instances do not require placement groups, and you can use placement groups for purposes other than configuring an EFA. This example uses both to demonstrate a configuration that can improve network performance for machines within the specified placement group.

.Prerequisites

- You created a placement group in the AWS console.
> **NOTE:** Ensure that the link:https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html#limitations-placement-groups[rules and limitations] for the type of placement group that you create are compatible with your intended use case.

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following lines under the `providerSpec` field:
```yaml
# ...
spec:
  template:
    spec:
      providerSpec:
        value:
          instanceType: <supported_instance_type> # <1>
          networkInterfaceType: EFA # <2>
          placement:
            availabilityZone: <zone> # <3>
            region: <region> # <4>
          placementGroupName: <placement_group> # <5>
          placementGroupPartition: <placement_group_partition_number> # <6>
# ...
```
<1> Specify an instance type that [supports EFAs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html#efa-instance-types).
<2> Specify the `EFA` network interface type.
<3> Specify the zone, for example, `us-east-1a`.
<4> Specify the region, for example, `us-east-1`.
<5> Specify the name of the existing AWS placement group to deploy machines in.
<6> Optional: Specify the partition number of the existing AWS placement group to deploy machines in.

.Verification

- In the AWS console, find a machine that the machine set created and verify the following in the machine properties:

- The placement group field has the value that you specified for the `placementGroupName` parameter in the machine set.

- The partition number field has the value that you specified for the `placementGroupPartition` parameter in the machine set.

- The interface type field indicates that it uses an EFA.