# Checking project status by using the CLI

You can review the status of your project by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You have created a project.

.Procedure

1. Switch to your project:
```bash
$ oc project <project_name> <1>
```
<1> Replace `<project_name>` with the name of your project.

1. Obtain a high-level overview of the project:
```bash
$ oc status
```