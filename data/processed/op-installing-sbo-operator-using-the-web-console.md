# Installing the {servicebinding-title} using the web console

You can install {servicebinding-title} using the OpenShift Container Platform software catalog. When you install the {servicebinding-title}, the custom resources (CRs) required for the service binding configuration are automatically installed along with the Operator.

//[discrete]
//== Prerequisites
//You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

.Procedure

1. In the *Administrator* perspective of the web console, navigate to *Ecosystem* -> *Software Catalog*.

1. Use the *Filter by keyword* box to search for `{servicebinding-title}` in the catalog. Click the *{servicebinding-title}* tile.

1. Read the brief description about the Operator on the *{servicebinding-title}* page. Click *Install*.

1. On the *Install Operator* page:
.. Select *All namespaces on the cluster (default)* for the *Installation Mode*. This mode installs the Operator in the default `openshift-operators` namespace, which enables the Operator to watch and be made available to all namespaces in the cluster.

.. Select *Automatic* for the *Approval Strategy*. This ensures that the future upgrades to the Operator are handled automatically by the Operator Lifecycle Manager (OLM). If you select the *Manual* approval strategy, OLM creates an update request. As a cluster administrator, you must then manually approve the OLM update request to update the Operator to the new version.

.. Select an *Update Channel*.

- By default, the *stable* channel enables installation of the latest stable and supported release of the {servicebinding-title}.

1. Click *Install*.
> **NOTE:** The Operator is installed automatically into the `openshift-operators` namespace.
1. On the **Installed Operator -- ready for use** pane, click *View Operator*. You will see the Operator listed on the *Installed Operators* page.
1. Verify that the *Status* is set to *Succeeded*  to confirm successful installation of {servicebinding-title}.