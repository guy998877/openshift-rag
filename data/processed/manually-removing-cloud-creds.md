# Removing cloud provider credentials

For clusters that use the Cloud Credential Operator (CCO) in mint mode, the administrator-level credential is stored in the `kube-system` namespace. 
The CCO uses the `admin` credential to process the `CredentialsRequest` objects in the cluster and create users for components with limited permissions.

After installing an OpenShift Container Platform cluster with the CCO in mint mode, you can remove the administrator-level credential secret from the `kube-system` namespace in the cluster. 
The CCO only requires the administrator-level credential during changes that require reconciling new or modified `CredentialsRequest` custom resources, such as minor cluster version updates.

> **NOTE:** Before performing a minor version cluster update (for example, updating from OpenShift Container Platform 4.20 to 4.21), you must reinstate the credential secret with the administrator-level credential. If the credential is not present, the update might be blocked.

.Prerequisites

- Your cluster is installed on a platform that supports removing cloud credentials from the CCO. 
Supported platforms are AWS and Google Cloud.

.Procedure

1. In the *Administrator* perspective of the web console, navigate to *Workloads* -> *Secrets*.

1. In the table on the *Secrets* page, find the root secret for your cloud provider.
[cols=2,options=header]
|===
|Platform
|Secret name

|AWS
|`aws-creds`

|Google Cloud
|`gcp-credentials`

|===

1. Click the Options menu image:kebab.png[title="Options menu"] in the same row as the secret and select *Delete Secret*.