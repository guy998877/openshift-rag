# Creating an OpenShift Container Platform service account for Google Cloud

You create an OpenShift Container Platform service account and annotate it to impersonate a Google Cloud service account.

.Prerequisites

- Your Google Cloud cluster uses GCP Workload Identity.

- You have created a federated Google Cloud service account.

- You have access to the pass:quotes[OpenShift CLI (`oc`)] as a user with the `cluster-admin` role.

- You have access to the Google Cloud CLI (`gcloud`) as a user with privileges to manage Identity and Access Management (IAM) and workload identity configurations.

.Procedure

1. Create an OpenShift Container Platform service account to use for GCP Workload Identity pod authentication by running the following command:
```bash
$ oc create serviceaccount <service_account_name>
```

1. Annotate the service account with the identity provider and Google Cloud service account to impersonate by running the following command:
```bash
$ oc patch serviceaccount <service_account_name> -p '{"metadata": {"annotations": {"cloud.google.com/workload-identity-provider": "projects/<project_number>/locations/global/workloadIdentityPools/<identity_pool>/providers/<identity_provider>"}}}'
```
Replace `<project_number>`, `<identity_pool>`, and `<identity_provider>` with the values for your configuration.
> **NOTE:** For `<project_number>`, specify the Google Cloud project number, not the project ID.

1. Annotate the service account with the email address for the Google Cloud service account by running the following command:
```bash
$ oc patch serviceaccount <service_account_name> -p '{"metadata": {"annotations": {"cloud.google.com/service-account-email": "<service_account_email>"}}}'
```
Replace `<service_account_email>` with the email address for the Google Cloud service account.
> **TIP:** Google Cloud service account email addresses typically use the format `<service_account_name>@<project_id>.iam.gserviceaccount.com`

1. Annotate the service account to use the `direct` external credentials configuration injection mode by running the following command:
```bash
$ oc patch serviceaccount <service_account_name> -p '{"metadata": {"annotations": {"cloud.google.com/injection-mode": "direct"}}}'
```
In this mode, the Workload Identity Federation webhook controller directly generates the Google Cloud external credentials configuration and injects them into the pod.

1. Use the Google Cloud CLI (`gcloud`) to specify the permissions for the workload by running the following command:
```bash
$ gcloud projects add-iam-policy-binding <project_id> --member "<service_account_email>" --role "projects/<project_id>/roles/<role_for_workload_permissions>"
```
Replace `<role_for_workload_permissions>` with the role for the workload. 
Specify a role that grants the permissions that your workload requires.

.Verification

- To verify the service account configuration, inspect the `ServiceAccount` manifest by running the following command:
```bash
$ oc get serviceaccount <service_account_name>
```
In the following example, the `service-a/app-x` OpenShift Container Platform service account can impersonate a Google Cloud service account called `app-x`:
.Example output
--
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-x
  namespace: service-a
  annotations: 
    cloud.google.com/workload-identity-provider: "projects/<project_number>/locations/global/workloadIdentityPools/<identity_pool>/providers/<identity_provider>" <1>
    cloud.google.com/service-account-email: "app-x@project.iam.googleapis.com"
    cloud.google.com/audience: "sts.googleapis.com" <2>
    cloud.google.com/token-expiration: "86400" <3>
    cloud.google.com/gcloud-run-as-user: "1000"
    cloud.google.com/injection-mode: "direct" <4>
```
<1> The workload identity provider for the service account of the cluster.
<2> The allowed audience for the workload identity provider.
<3> The token expiration time period in seconds.
<4> The `direct` external credentials configuration injection mode.
--