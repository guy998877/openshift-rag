# Configuring Azure confidential virtual machines by using machine sets

OpenShift Container Platform 4.21 supports Azure confidential virtual machines (VMs).

> **NOTE:** Confidential VMs are currently not supported on 64-bit ARM architectures.

By editing the machine set YAML file, you can configure the confidential VM options that a machine set uses for machines that it deploys. For example, you can configure these machines to use UEFI security features such as Secure Boot or a dedicated virtual Trusted Platform Module (vTPM) instance.

For more information about related features and functionality, see the Microsoft Azure documentation about [Confidential virtual machines](https://learn.microsoft.com/en-us/azure/confidential-computing/confidential-vm-overview).

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following section under the `providerSpec` field:
--
.Sample configuration
```yaml
# ...
spec:
  template:
    spec:
      providerSpec:
        value:
          osDisk:
            # ...
            managedDisk:
              securityProfile: # <1>
                securityEncryptionType: VMGuestStateOnly # <2>
            # ...
          securityProfile: # <3>
            settings:
                securityType: ConfidentialVM # <4>
                confidentialVM:
                  uefiSettings: # <5>
                    secureBoot: Disabled # <6>
                    virtualizedTrustedPlatformModule: Enabled # <7>
          vmSize: Standard_DC16ads_v5 # <8>
# ...
```
<1> Specifies security profile settings for the managed disk when using a confidential VM.
<2> Enables encryption of the Azure VM Guest State (VMGS) blob. This setting requires the use of vTPM.
<3> Specifies security profile settings for the confidential VM.
<4> Enables the use of confidential VMs. This value is required for all valid configurations.
<5> Specifies which UEFI security features to use. This section is required for all valid configurations.
<6> Disables UEFI Secure Boot.
<7> Enables the use of a vTPM.
<8> Specifies an instance type that supports confidential VMs.
--

.Verification

- On the Azure portal, review the details for a machine deployed by the machine set and verify that the confidential VM options match the values that you configured.