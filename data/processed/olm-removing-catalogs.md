// The OSD/ROSA version of this procedure is sd-olm-removing-catalogs.adoc.

# Removing custom catalogs

As a cluster administrator, you can remove custom Operator catalogs that have been previously added to your cluster by deleting the related catalog source.

.Prerequisites
- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. In the *Administrator* perspective of the web console, navigate to *Administration* -> *Cluster Settings*.

1. Click the *Configuration* tab, and then click *OperatorHub*.

1. Click the *Sources* tab.

1. Select the Options menu image:kebab.png[title="Options menu"] for the catalog that you want to remove, and then click *Delete CatalogSource*.