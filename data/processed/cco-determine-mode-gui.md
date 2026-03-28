# Determining the Cloud Credential Operator mode by using the web console

You can determine what mode the Cloud Credential Operator (CCO) is configured to use by using the web console.

> **NOTE:** Only Amazon Web Services (AWS), global Microsoft Azure, and Google Cloud clusters support multiple CCO modes.

.Prerequisites

- You have access to an OpenShift Container Platform account with cluster administrator permissions.

.Procedure

1. Log in to the OpenShift Container Platform web console as a user with the `cluster-admin` role.

1. Navigate to *Administration* -> *Cluster Settings*.

1. On the *Cluster Settings* page, select the *Configuration* tab.

1. Under *Configuration resource*, select *CloudCredential*.

1. On the *CloudCredential details* page, select the *YAML* tab.

1. In the YAML block, check the value of `spec.credentialsMode`. The following values are possible, though not all are supported on all platforms:
--
- `''`: The CCO is operating in the default mode. In this configuration, the CCO operates in mint or passthrough mode, depending on the credentials provided during installation.
- `Mint`: The CCO is operating in mint mode.
- `Passthrough`: The CCO is operating in passthrough mode.
- `Manual`: The CCO is operating in manual mode.
--
> **IMPORTANT:** To determine the specific configuration of an AWS, Google Cloud, or global Microsoft Azure cluster that has a `spec.credentialsMode` of `''`, `Mint`, or `Manual`, you must investigate further. AWS and Google Cloud clusters support using mint mode with the root secret deleted. An AWS, Google Cloud, or global Microsoft Azure cluster that uses manual mode might be configured to create and manage cloud credentials from outside of the cluster with AWS STS, Google Cloud Workload Identity, or Microsoft Entra Workload ID. You can determine whether your cluster uses this strategy by examining the cluster `Authentication` object.

1. AWS or Google Cloud clusters that use mint mode only: To determine whether the cluster is operating without the root secret, navigate to *Workloads* -> *Secrets* and look for the root secret for your cloud provider.
> **NOTE:** Ensure that the *Project* dropdown is set to *All Projects*.
[cols=2,options=header]
|===
|Platform
|Secret name

|AWS
|`aws-creds`

|Google Cloud
|`gcp-credentials`

|===
--
- If you see one of these values, your cluster is using mint or passthrough mode with the root secret present.
- If you do not see these values, your cluster is using the CCO in mint mode with the root secret removed.
--

1. AWS, Google Cloud, or global Microsoft Azure clusters that use manual mode only: To determine whether the cluster is configured to create and manage cloud credentials from outside of the cluster, you must check the cluster `Authentication` object YAML values.

.. Navigate to *Administration* -> *Cluster Settings*.

.. On the *Cluster Settings* page, select the *Configuration* tab.

.. Under *Configuration resource*, select *Authentication*.

.. On the *Authentication details* page, select the *YAML* tab.

.. In the YAML block, check the value of the `.spec.serviceAccountIssuer` parameter.
--
- A value that contains a URL that is associated with your cloud provider indicates that the CCO is using manual mode with short-term credentials for components. These clusters are configured using the `ccoctl` utility to create and manage cloud credentials from outside of the cluster.

- An empty value (`''`) indicates that the cluster is using the CCO in manual mode but was not configured using the `ccoctl` utility.
--