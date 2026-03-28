# Customizing the available cluster roles using the web console

In the *Developer* perspective of the web console, the *Project* -> *Project access* page enables a project administrator to grant roles to users in a project. By default, the available cluster roles that can be granted to users in a project are admin, edit, and view.

As a cluster administrator, you can define which cluster roles are available in the *Project access* page for all projects cluster-wide. You can specify the available roles by customizing the `spec.customization.projectAccess.availableClusterRoles` object in the `Console` configuration resource.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. In the *Administrator* perspective, navigate to *Administration* -> *Cluster settings*.
1. Click the *Configuration* tab.
1. From the *Configuration resource* list, select *Console `operator.openshift.io`*.
1. Navigate to the *YAML* tab to view and edit the YAML code.
1. In the YAML code under `spec`, customize the list of available cluster roles for project access. The following example specifies the default `admin`, `edit`, and `view` roles:
```yaml
apiVersion: operator.openshift.io/v1
kind: Console
metadata:
  name: cluster
# ...
spec:
  customization:
    projectAccess:
      availableClusterRoles:
      - admin
      - edit
      - view
```
1. Click *Save* to save the changes to the `Console` configuration resource.

.Verification

1. In the *Developer* perspective, navigate to the *Project* page.
1. Select a project from the *Project* menu.
1. Select the *Project access* tab.
1. Click the menu in the *Role* column and verify that the available roles match the configuration that you applied to the `Console` resource configuration.