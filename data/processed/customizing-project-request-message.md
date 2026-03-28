# Customizing the project request message

When a developer or a service account that is unable to self-provision projects
makes a project creation request using the web console or CLI, the following
error message is returned by default:

```bash
You may not request a new project via this API.
```

Cluster administrators can customize this message. Consider updating it to
provide further instructions on how to request a new project specific to your
organization. For example:

- To request a project, contact your system administrator at
[x-]`projectname@example.com`.
- To request a new project, fill out the project request form located at
[x-]`https://internal.example.com/openshift-project-request`.

To customize the project request message:

.Procedure

1. Edit the project configuration resource using the web console or CLI.

- Using the web console:
... Navigate to the *Administration* -> *Cluster Settings* page.
... Click *Configuration* to view all configuration resources.
... Find the entry for *Project* and click *Edit YAML*.

- Using the CLI:
... Log in as a user with `cluster-admin` privileges.
... Edit the `project.config.openshift.io/cluster` resource:
```bash
$ oc edit project.config.openshift.io/cluster
```

1. Update the `spec` section to include the `projectRequestMessage` parameter and
set the value to your custom message:
.Project configuration resource with custom project request message
```yaml
apiVersion: config.openshift.io/v1
kind: Project
metadata:
# ...
spec:
  projectRequestMessage: <message_string>
# ...
```
For example:

```yaml
apiVersion: config.openshift.io/v1
kind: Project
metadata:
# ...
spec:
  projectRequestMessage: To request a project, contact your system administrator at projectname@example.com.
# ...
```

1. After you save your changes, attempt to create a new project as a developer or
service account that is unable to self-provision projects to verify that your
changes were successfully applied.