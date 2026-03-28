# Configuring persistent disk types by using machine sets

Configure the persistent disk type for your machine set on Google Cloud to match your workload requirements. Editing the `MachineSet` YAML file allows you to choose between standard, balanced, or SSD persistent disks.

For more information about persistent disk types, compatibility, regional availability, and limitations, see the Google Cloud Compute Engine documentation about [persistent disks](https://cloud.google.com/compute/docs/disks#pdspecs).

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following line under the `providerSpec` field:
```yaml
...
spec:
  template:
    spec:
      providerSpec:
        value:
          disks:
```

.Verification

- Using the Google Cloud console, review the details for a machine deployed by the machine set and verify that the `Type` field matches the configured disk type.