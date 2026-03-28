# Rotating IBM Cloud credentials

You can rotate API keys for your existing service IDs and update the corresponding secrets.

.Prerequisites

- You have configured the `ccoctl` utility.
- You have existing service IDs in a live OpenShift Container Platform cluster installed.

.Procedure

- Use the `ccoctl` utility to rotate your API keys for the service IDs and update the secrets by running the following command:
```bash
$ ccoctl <provider_name> refresh-keys \// <1>
    --kubeconfig <openshift_kubeconfig_file> \// <2>
    --credentials-requests-dir <path_to_credential_requests_directory> \// <3>
    --name <name> <4>
```
<1> The name of the provider. For example: `ibmcloud` or `powervs`.
<2> The `kubeconfig` file associated with the cluster. For example, `<installation_directory>/auth/kubeconfig`.
<3> The directory where the credential requests are stored.
<4> The name of the OpenShift Container Platform cluster.
--
> **NOTE:** If your cluster uses Technology Preview features that are enabled by the `TechPreviewNoUpgrade` feature set, you must include the `--enable-tech-preview` parameter.
--