# Configuring Shielded VM options by using machine sets

Configure Shielded Virtual Machine (VM) options for your machine sets on Google Cloud to help secure your cluster instances. By editing the `MachineSet` YAML file, you can configure the Shielded VM options that a machine set uses for machines that it deploys.

For more information about Shielded VM features and functionality, see the Google Cloud Compute Engine documentation about [Shielded VM](https://cloud.google.com/compute/shielded-vm/docs/shielded-vm).

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following section under the `providerSpec` field:
```yaml
# ...
spec:
  template:
    spec:
      providerSpec:
        value:
          shieldedInstanceConfig:
            integrityMonitoring: Enabled
            secureBoot: Disabled
            virtualizedTrustedPlatformModule: Enabled
# ...
```
where:
--
`spec.template.spec.providerSpec.value.shieldedInstanceConfig.integrityMonitoring`:: Specifies whether integrity monitoring is enabled. Valid values are `Disabled` or `Enabled`.
> **NOTE:** When integrity monitoring is enabled, you must not disable virtual trusted platform module (vTPM).
`spec.template.spec.providerSpec.value.shieldedInstanceConfig.secureBoot`:: Specifies whether UEFI Secure Boot is enabled. Valid values are `Disabled` or `Enabled`.
`spec.template.spec.providerSpec.value.shieldedInstanceConfig.virtualizedTrustedPlatformModule`:: Specifies whether vTPM is enabled. Valid values are `Disabled` or `Enabled`.
--

.Verification

- Using the Google Cloud console, review the details for a machine deployed by the machine set and verify that the Shielded VM options match the values that you configured.