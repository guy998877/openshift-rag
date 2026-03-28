# Changing the Amazon Web Services instance type by using a control plane machine set

You can change the Amazon Web Services (AWS) instance type that your control plane machines use by updating the specification in the control plane machine set custom resource (CR).

.Prerequisites

- Your AWS cluster uses a control plane machine set.

.Procedure

1. Edit the following line under the `providerSpec` field:
```yaml
providerSpec:
  value:
    ...
    instanceType: <compatible_aws_instance_type>
```
- `<compatible_aws_instance_type>`: Specifies a larger AWS instance type with the same base as the previous selection. For example, you can change `m6i.xlarge` to `m6i.2xlarge` or `m6i.4xlarge`.

1. Save your changes.