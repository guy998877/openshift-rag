# Preparing to install the Google Cloud Filestore CSI Driver Operator with Workload Identity

If you are planning to use GCP Workload Identity with Google Compute Platform Filestore, you must obtain certain parameters that you will use during the installation of the Google Cloud Filestore Container Storage Interface (CSI) Driver Operator.

.Prerequisites
- Access to the cluster as a user with the cluster-admin role.

// Put note in install area of docs to remind users to take note of the identity pool ID and the provider ID

.Procedure

To prepare to install the Google Cloud Filestore CSI Driver Operator with Workload Identity:

1. Obtain the project number:

.. Obtain the project ID by running the following command:
```bash
$ export PROJECT_ID=$(oc get infrastructure/cluster -o jsonpath='{.status.platformStatus.gcp.projectID}')
```

.. Obtain the project number, using the project ID, by running the following command:
```bash
$ gcloud projects describe $PROJECT_ID --format="value(projectNumber)"
```

1. Find the identity pool ID and the provider ID:
During cluster installation, the names of these resources are provided to the Cloud Credential Operator utility (`ccoctl`) with the `--name parameter`. See "Creating Google Cloud resources with the Cloud Credential Operator utility".

1. Create Workload Identity resources for the Google Cloud Filestore Operator:

.. Create a `CredentialsRequest` file using the following example file:
.Example Credentials Request YAML file
```yaml
apiVersion: cloudcredential.openshift.io/v1
kind: CredentialsRequest
metadata:
  name: openshift-gcp-filestore-csi-driver-operator
  namespace: openshift-cloud-credential-operator
  annotations:
    include.release.openshift.io/self-managed-high-availability: "true"
    include.release.openshift.io/single-node-developer: "true"
spec:
  serviceAccountNames:
  - gcp-filestore-csi-driver-operator
  - gcp-filestore-csi-driver-controller-sa
  secretRef:
    name: gcp-filestore-cloud-credentials
    namespace: openshift-cluster-csi-drivers
  providerSpec:
    apiVersion: cloudcredential.openshift.io/v1
	kind: GCPProviderSpec
    predefinedRoles:
    - roles/file.editor
    - roles/resourcemanager.tagUser
    skipServiceCheck: true
```

.. Use the `CredentialsRequest` file to create a Google Cloud service account by running the following command:
```bash
$ ./ccoctl gcp create-service-accounts --name=<filestore-service-account> \// <1>
  --workload-identity-pool=<workload-identity-pool> \// <2> 
  --workload-identity-provider=<workload-identity-provider> \// <3> 
  --project=<project-id> \// <4> 
  --credentials-requests-dir=/tmp/credreq <5>
```
<1> <filestore-service-account> is a user-chosen name. 
<2> <workload-identity-pool> comes from Step 2 above.
<3> <workload-identity-provider> comes from Step 2 above.
<4> <project-id> comes from Step 1.a above.
<5> The name of directory where the `CredentialsRequest` file resides.
.Example output
```bash
2025/02/10 17:47:39 Credentials loaded from gcloud CLI defaults
2025/02/10 17:47:42 IAM service account filestore-service-account-openshift-gcp-filestore-csi-driver-operator created
2025/02/10 17:47:44 Unable to add predefined roles to IAM service account, retrying...
2025/02/10 17:47:59 Updated policy bindings for IAM service account filestore-service-account-openshift-gcp-filestore-csi-driver-operator
2025/02/10 17:47:59 Saved credentials configuration to: /tmp/install-dir/ <1>
openshift-cluster-csi-drivers-gcp-filestore-cloud-credentials-credentials.yaml
```
<1> The current directory.

.. Find the service account email of the newly created service account by running the following command:
```bash
$ cat /tmp/install-dir/manifests/openshift-cluster-csi-drivers-gcp-filestore-cloud-credentials-credentials.yaml | yq '.data["service_account.json"]' | base64 -d | jq '.service_account_impersonation_url'
```
.Example output
```bash
https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/filestore-se-openshift-g-ch8cm@openshift-gce-devel.iam.gserviceaccount.com:generateAccessToken
```
In this example output, the service account email is `filestore-se-openshift-g-ch8cm@openshift-gce-devel.iam.gserviceaccount.com`.

.Results

You now have the following parameters that you need to install the Google Cloud Filestore CSI Driver Operator:

- Project number - from Step 1.b

- Pool ID - from Step 2

- Provider ID - from Step 2

- Service account email - from Step 3.c