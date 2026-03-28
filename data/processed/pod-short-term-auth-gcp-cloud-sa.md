# Creating a federated Google Cloud service account

You can use the Google Cloud console to create a workload identity pool and provider and allow an OpenShift Container Platform service account to impersonate a Google Cloud service account.

.Prerequisites

- Your Google Cloud cluster uses GCP Workload Identity.

- You have access to the Google Cloud console as a user with privileges to manage Identity and Access Management (IAM) and workload identity configurations.

- You have created a Google Cloud project to use with your application.

.Procedure

1. In the IAM configuration for your Google Cloud project, identify the identity pool and provider that the cluster uses for GCP Workload Identity authentication.

1. Grant permission for external identities to impersonate a Google Cloud service account. 
With these permissions, an OpenShift Container Platform service account can work as a federated workload identity.
For more information, see Google Cloud documentation about [allowing your external workload to access Google Cloud resources](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds#service-account-impersonation).