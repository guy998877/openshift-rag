# Modifying the template for new projects

As a cluster administrator, you can modify the default project template so that new projects are created using your custom requirements.

To create your own custom project template:

.Prerequisites
- You have access to an OpenShift Container Platform cluster using an account with `cluster-admin` permissions.

.Procedure

1. Log in as a user with `cluster-admin` privileges.

1. Generate the default project template:
```bash
$ oc adm create-bootstrap-project-template -o yaml > template.yaml
```

1. Use a text editor to modify the generated `template.yaml` file by adding
objects or modifying existing objects.

1. The project template must be created in the `openshift-config` namespace. Load
your modified template:
```bash
$ oc create -f template.yaml -n openshift-config
```

1. Edit the project configuration resource using the web console or CLI.

- Using the web console:
... Navigate to the *Administration* -> *Cluster Settings* page.
... Click *Configuration* to view all configuration resources.
... Find the entry for *Project* and click *Edit YAML*.

- Using the CLI:
... Edit the `project.config.openshift.io/cluster` resource:
```bash
$ oc edit project.config.openshift.io/cluster
```

1. Update the `spec` section to include the `projectRequestTemplate` and `name`
parameters, and set the name of your uploaded project template. The default name
is `project-request`.
.Project configuration resource with custom project template
```yaml
apiVersion: config.openshift.io/v1
kind: Project
metadata:
# ...
spec:
  projectRequestTemplate:
    name: <template_name>
# ...
```

1. After you save your changes, create a new project to verify that your changes
were successfully applied.