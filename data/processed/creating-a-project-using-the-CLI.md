# Creating a project by using the CLI

If allowed by your cluster administrator, you can create a new project.

> **NOTE:** Projects starting with `openshift-` and `kube-` are considered critical by OpenShift Container Platform. As such, OpenShift Container Platform does not allow you to create Projects starting with `openshift-` or `kube-` using the `oc new-project` command. Cluster administrators can create these projects using the `oc adm new-project` command.

.Procedure

- Run:
```bash
$ oc new-project <project_name> \
    --description="<description>" --display-name="<display_name>"
```
For example:
```bash
$ oc new-project hello-openshift \
    --description="This is an example project" \
    --display-name="Hello OpenShift"
```

> **NOTE:** The number of projects you are allowed to create is limited. After your limit is reached, you might have to delete an existing project in order to create a new one.