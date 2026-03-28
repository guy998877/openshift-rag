# Disabling project self-provisioning

You can prevent an authenticated user group from self-provisioning new projects.

.Procedure

1. Log in as a user with `cluster-admin` privileges.

1. View the `self-provisioners` cluster role binding usage by running the following command:
```bash
$ oc describe clusterrolebinding.rbac self-provisioners
```
.Example output
```bash
Name:		self-provisioners
Labels:		<none>
Annotations:	rbac.authorization.kubernetes.io/autoupdate=true
Role:
  Kind:	ClusterRole
  Name:	self-provisioner
Subjects:
  Kind	Name				Namespace
  ----	----				---------
  Group	system:authenticated:oauth
```
Review the subjects in the `self-provisioners` section.

1. Remove the `self-provisioner` cluster role from the group `system:authenticated:oauth`.

- If the `self-provisioners` cluster role binding binds only the `self-provisioner` role to the `system:authenticated:oauth` group, run the following command:
```bash
$ oc patch clusterrolebinding.rbac self-provisioners -p '{"subjects": null}'
```

- If the `self-provisioners` cluster role binding binds the `self-provisioner` role to more users, groups, or service accounts than the `system:authenticated:oauth` group, run the following command:
```bash
$ oc adm policy \
    remove-cluster-role-from-group self-provisioner \
    system:authenticated:oauth
```

1. Edit the `self-provisioners` cluster role binding to prevent automatic updates to the role. Automatic updates reset the cluster roles to the default state.

- To update the role binding using the CLI:

... Run the following command:
```bash
$ oc edit clusterrolebinding.rbac self-provisioners
```

... In the displayed role binding, set the `rbac.authorization.kubernetes.io/autoupdate` parameter value to `false`, as shown in the following example:
```yaml
apiVersion: authorization.openshift.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "false"
# ...
```

- To update the role binding by using a single command:
```bash
$ oc patch clusterrolebinding.rbac self-provisioners -p '{ "metadata": { "annotations": { "rbac.authorization.kubernetes.io/autoupdate": "false" } } }'
```

1. Log in as an authenticated user and verify that it can no longer self-provision a project:
```bash
$ oc new-project test
```
.Example output
```bash
Error from server (Forbidden): You may not request a new project via this API.
```
Consider customizing this project request message to provide more helpful instructions specific to your organization.