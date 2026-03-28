# Configuring trusted launch for Azure virtual machines by using machine sets

OpenShift Container Platform 4.21 supports trusted launch for Azure virtual machines (VMs). By editing the machine set YAML file, you can configure the trusted launch options that a machine set uses for machines that it deploys. For example, you can configure these machines to use UEFI security features such as Secure Boot or a dedicated virtual Trusted Platform Module (vTPM) instance.

> **NOTE:** Some feature combinations result in an invalid configuration.

.UEFI feature combination compatibility
|====
|Secure Boot^[1]^ |vTPM^[2]^ |Valid configuration

|Enabled
|Enabled
|Yes

|Enabled
|Disabled
|Yes

|Enabled
|Omitted
|Yes

|Disabled
|Enabled
|Yes

|Omitted
|Enabled
|Yes

|Disabled
|Disabled
|No

|Omitted
|Disabled
|No

|Omitted
|Omitted
|No
|====
[.small]
--
1. Using the `secureBoot` field.
2. Using the `virtualizedTrustedPlatformModule` field.
--

For more information about related features and functionality, see the Microsoft Azure documentation about [Trusted launch for Azure virtual machines](https://learn.microsoft.com/en-us/azure/virtual-machines/trusted-launch).

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following section under the `providerSpec` field to provide a valid configuration:
.Sample valid configuration with UEFI Secure Boot and vTPM enabled
```yaml
# ...
spec:
  template:
    machines_v1beta1_machine_openshift_io:
      spec:
        providerSpec:
          value:
            securityProfile:
              settings:
                securityType: TrustedLaunch # <1>
                trustedLaunch:
                  uefiSettings: # <2>
                    secureBoot: Enabled # <3>
                    virtualizedTrustedPlatformModule: Enabled # <4>
# ...
```
<1> Enables the use of trusted launch for Azure virtual machines. This value is required for all valid configurations.
<2> Specifies which UEFI security features to use. This section is required for all valid configurations.
<3> Enables UEFI Secure Boot.
<4> Enables the use of a vTPM.

.Verification

- On the Azure portal, review the details for a machine deployed by the machine set and verify that the trusted launch options match the values that you configured.