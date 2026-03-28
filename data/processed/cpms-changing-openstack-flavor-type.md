# Changing the RHOSP compute flavor by using a control plane machine set

You can change the Red Hat OpenStack Platform (RHOSP) compute service (Nova) flavor that your control plane machines use by updating the specification in the control plane machine set custom resource.

In RHOSP, flavors define the compute, memory, and storage capacity of computing instances. By increasing or decreasing the flavor size, you can scale your control plane vertically.

.Prerequisites

- Your RHOSP cluster uses a control plane machine set.

.Procedure

1. Edit the following line under the `providerSpec` field:
```yaml
providerSpec:
  value:
# ...
    flavor: m1.xlarge <1>
```
<1> Specify a RHOSP flavor type that has the same base as the existing selection. For example, you can change `m6i.xlarge` to `m6i.2xlarge` or `m6i.4xlarge`. You can choose larger or smaller flavors depending on your vertical scaling needs.

1. Save your changes.

After you save your changes, machines are replaced with ones that use the flavor you chose.