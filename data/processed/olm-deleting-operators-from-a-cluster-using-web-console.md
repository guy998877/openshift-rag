# Deleting Operators from a cluster using the web console

Cluster administrators can delete installed Operators from a selected namespace by using the web console.

.Prerequisites

- You have access to the OpenShift Container Platform cluster web console using an account with

.Procedure

1. Navigate to the *Ecosystem* -> *Installed Operators* page.

1. Scroll or enter a keyword into the *Filter by name* field to find the Operator that you want to remove. Then, click on it.

1. On the right side of the *Operator Details* page, select *Uninstall Operator* from the *Actions* list.
An *Uninstall Operator?* dialog box is displayed.

1. Select *Uninstall* to remove the Operator, Operator deployments, and pods. Following this action, the Operator stops running and no longer receives updates.
> **NOTE:** This action does not remove resources managed by the Operator, including custom resource definitions (CRDs) and custom resources (CRs). Dashboards and navigation items enabled by the web console and off-cluster resources that continue to run might need manual clean up. To remove these after uninstalling the Operator, you might need to manually delete the Operator CRDs.