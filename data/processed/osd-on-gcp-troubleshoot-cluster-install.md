# Troubleshooting OpenShift Container Platform on Google Cloud installation error codes

The following table lists OpenShift Container Platform on Google Cloud installation error codes and what you can do to resolve these errors.

.OpenShift Container Platform on Google Cloud installation error codes
[options="header",cols="3"]
|===
| Error code | Description | Resolution

| OCM3022
| Invalid Google Cloud project ID.
| Verify the project ID in the Google cloud console and retry cluster creation.

| OCM3023
| Google Cloud instance type not found.
| Verify the instance type and retry cluster creation.

For more information about OpenShift Container Platform on Google Cloud instance types, see _Google Cloud instance types_ in the _Additional resources_ section.

| OCM3024
| Google Cloud precondition failed.
| Verify the organization policy constraints and retry cluster creation.

For more information about organization policy constraints, see [Organization policy constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints).

| OCM3025
| Google Cloud SSD quota limit exceeded.
| Check your available persistent disk SSD quota either in the Google Cloud console or in the `gcloud` CLI. There must be at least 896 GB of SSD available. Increase the SSD quota limit and retry cluster creation.

For more information about managing persistent disk SSD quota, see [Allocation quotas](https://cloud.google.com/compute/resource-usage).

| OCM3026
| Google Cloud compute quota limit exceeded.
| Increase your CPU compute quota and retry cluster installation.

For more information about the CPU compute quota, see [Compute Engine quota and limits overview](https://cloud.google.com/compute/quotas-limits).

| OCM3027
| Google Cloud service account quota limit exceeded.
| Ensure your quota allows for additional unused service accounts. Check your current usage for quotas in your Google Cloud account and try again.

For more information about managing your quotas, see [Manage your quotas using the console](https://cloud.google.com/docs/quotas/view-manage#managing_your_quota_console).

|===