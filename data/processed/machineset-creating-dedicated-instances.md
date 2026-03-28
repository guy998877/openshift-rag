# Creating Dedicated Instances by using machine sets

You can run a machine that is backed by a Dedicated Instance by using Machine API integration. Set the `tenancy` field in your machine set YAML file to launch a Dedicated Instance on AWS.

.Procedure

- Specify a dedicated tenancy under the `providerSpec` field:
```yaml
providerSpec:
  placement:
    tenancy: dedicated
```