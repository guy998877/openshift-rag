# Viewing a project using the CLI

When viewing projects, you are restricted to seeing only the projects you have
access to view based on the authorization policy.

.Procedure

1. To view a list of projects, run:
```bash
$ oc get projects
```

1. You can change from the current project to a different project for CLI
operations. The specified project is then used in all subsequent operations that
manipulate project-scoped content:
```bash
$ oc project <project_name>
```