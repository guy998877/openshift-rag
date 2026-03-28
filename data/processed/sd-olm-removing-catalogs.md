// The OCP version of this procedure is olm-removing-catalogs.adoc.

# Removing custom catalogs

As an administrator with the `dedicated-admin` role, you can remove custom Operator catalogs that have been previously added to your cluster by deleting the related catalog source.

.Prerequisites
- You have access to the cluster as a user with the `dedicated-admin` role.

.Procedure

1. In the *Administrator* perspective of the web console, navigate to *Home* -> *Search*.

1. Select a project from the *Project:* list.

1. Select *CatalogSource* from the *Resources* list.

1. Select the Options menu image:kebab.png[title="Options menu"] for the catalog that you want to remove, and then click *Delete CatalogSource*.