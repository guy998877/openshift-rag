ifdef::post-install[= Rotating cloud provider credentials manually]
ifndef::post-install[= Maintaining cloud provider credentials]

If your cloud provider credentials are changed for any reason, you must manually update the secret that the Cloud Credential Operator (CCO) uses to manage cloud provider credentials.

The process for rotating cloud credentials depends on the mode that the CCO is configured to use. After you rotate credentials for a cluster that is using mint mode, you must manually remove the component credentials that were created by the removed credential.

////
> **NOTE:** You can also use the command-line interface to complete all parts of this procedure.
////

.Prerequisites

- Your cluster is installed on a platform that supports rotating cloud credentials manually with the CCO mode that you are using:

- You have changed the credentials that are used to interface with your cloud provider.

- The new credentials have sufficient permissions for the mode CCO is configured to use in your cluster.

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

1. Click the Options menu image:kebab.png[title="Options menu"] in the same row as the secret and select *Edit Secret*.

1. Record the contents of the *Value* field or fields. You can use this information to verify that the value is different after updating the credentials.

1. Update the text in the *Value* field or fields with the new authentication information for your cloud provider, and then click *Save*.

.Verification

To verify that the credentials have changed:

1. In the *Administrator* perspective of the web console, navigate to *Workloads* -> *Secrets*.

1. Verify that the contents of the *Value* field or fields have changed.

////
// Provider-side verification also possible, though cluster-side is cleaner process.
1. To verify that the credentials have changed from the console of your cloud provider:

.. Get the `CredentialsRequest` CR names for your platform:
```bash
$ oc -n openshift-cloud-credential-operator get CredentialsRequest -o json | jq -r '.items[] | select (.spec[].kind=="<provider_spec>") | .metadata.name'
```
Where `<provider_spec>` is the corresponding value for your cloud provider: `AWSProviderSpec` for AWS, `AzureProviderSpec` for Azure, or `GCPProviderSpec` for Google Cloud.
.Example output for AWS
```bash
aws-ebs-csi-driver-operator
cloud-credential-operator-iam-ro
openshift-image-registry
openshift-ingress
openshift-machine-api-aws
```

.. Get the IAM username that corresponds to each `CredentialsRequest` CR name:
```bash
$ oc get credentialsrequest <cr_name> -n openshift-cloud-credential-operator -o json | jq -r ".status.providerStatus"
```
Where `<cr_name>` is the name of a `CredentialsRequest` CR.
.Example output for AWS
```json
{
  "apiVersion": "cloudcredential.openshift.io/v1",
  "kind": "AWSProviderStatus",
  "policy": "<example-iam-username-policy>",
  "user": "<example-iam-username>"
}
```
Where `<example-iam-username>` is the name of an IAM user on the cloud provider.

.. For each IAM username, view the details for the user on the cloud provider. The credentials should show that they were created after being rotated on the cluster.
////