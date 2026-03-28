# Enabling Azure boot diagnostics

You can enable boot diagnostics on Azure machines that your machine set creates.

.Prerequisites

- Have an existing Microsoft Azure
ifdef::ash[Stack Hub]
cluster.

.Procedure

- Add the `diagnostics` configuration that is applicable to your storage type to the `providerSpec` field in your machine set YAML file:

- For an Azure Managed storage account:
```yaml
providerSpec:
  value:
    diagnostics:
      boot:
        storageAccountType: <azure_managed>
```
Where `<azure_managed>` specifies an Azure Managed storage account.

- For an Azure Unmanaged storage account:
```yaml
providerSpec:
  value: 
    diagnostics:
      boot:
        storageAccountType: <customer_managed>
        customerManaged:
          storageAccountURI: <https://<storage-account>.blob.core.windows.net>
```
Where:
`<customer_managed>`:: Specifies an Azure Unmanaged storage account.
`\https://<storage-account>.blob.core.windows.net`:: Specifies storage account URL. Replace `<storage-account>` with the name of your storage account.
> **NOTE:** Only the Azure Blob Storage data service is supported.

.Verification

- On the Microsoft Azure portal, review the *Boot diagnostics* page for a machine deployed by the machine set, and verify that you can see the serial logs for the machine.