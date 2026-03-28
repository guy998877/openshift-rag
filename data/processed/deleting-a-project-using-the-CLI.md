# Deleting a project by using the CLI

// Moved intro paragraph to working-with-projects.adoc

You can delete a project by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You have created a project.
- You have the required permissions to delete the project.

.Procedure

1. Delete your project:
```bash
$ oc delete project <project_name> <1>
```
<1> Replace `<project_name>` with the name of the project that you want to delete.