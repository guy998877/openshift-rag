# Creating service accounts

You can create a service account in a project and grant it permissions by
binding it to a role.

.Procedure

1. Optional: To view the service accounts in the current project:
```bash
$ oc get sa
```
.Example output
```bash
NAME       SECRETS   AGE
builder    1         2d
default    1         2d
deployer   1         2d
```

1. To create a new service account in the current project:
```bash
$ oc create sa <service_account_name> <1>
```
<1> To create a service account in a different project, specify `-n <project_name>`.
.Example output
```bash
serviceaccount "robot" created
```
> **TIP:** You can alternatively apply the following YAML to create the service account: [source,yaml] ---- apiVersion: v1 kind: ServiceAccount metadata: name: <service_account_name> namespace: <current_project> ----

1. Optional: View the secrets for the service account:
```bash
$ oc describe sa robot
```
.Example output
```bash
Name:                robot
Namespace:           project1
Labels:              <none>
Annotations:         openshift.io/internal-registry-pull-secret-ref: robot-dockercfg-qzbhb
Image pull secrets:  robot-dockercfg-qzbhb
Mountable secrets:   robot-dockercfg-qzbhb
Tokens:              <none>
Events:              <none>
```