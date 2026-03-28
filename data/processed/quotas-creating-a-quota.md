# Creating a quota

You can create a quota to constrain resource usage in a given project.

.Procedure

1. Define the quota in a file.

1. Use the file to create the quota and apply it to a project:
```bash
$ oc create -f <file> [-n <project_name>]
```
For example:
```bash
$ oc create -f core-object-counts.yaml -n demoproject
```