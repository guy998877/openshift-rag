# Configuring Confidential VM by using machine sets

You create machine sets to scale clusters on Google Cloud. By editing the machine set YAML file, you can configure the Confidential VM options that a machine set uses for machines that it deploys.

For more information about Confidential VM features, functions, and compatibility, see the Google Cloud Compute Engine documentation about [Confidential VM](https://cloud.google.com/confidential-computing/confidential-vm/docs/about-cvm#confidential-vm).

> **NOTE:** Confidential VMs are currently not supported on 64-bit ARM architectures. If you use Confidential VM, you must ensure that you select a supported region. For details on supported regions and configurations, see the Google Cloud Compute Engine documentation about link:https://cloud.google.com/confidential-computing/confidential-vm/docs/supported-configurations#supported-zones[supported zones].

.Procedure

1. In a text editor, open the YAML file for an existing machine set or create a new one.

1. Edit the following section under the `providerSpec` field:
```yaml
# ...
```
where:

.Verification

- On the Google Cloud console, review the details for a machine deployed by the machine set and verify that the Confidential VM options match the values that you configured.