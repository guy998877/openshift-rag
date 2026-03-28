# RBAC overview

Role-based access control (RBAC) objects determine whether a user is allowed to
perform a given action within a project.

can use the cluster roles and bindings to control who has various access levels to the OpenShift Container Platform platform itself and all projects.

Developers can use local roles and bindings to control who has access
to their projects. Note that authorization is a separate step from
authentication, which is more about determining the identity of who is taking the action.

Authorization is managed using:

[cols="1,4",options="header"]
|===

|Authorization object |Description

|Rules |Sets of permitted verbs on a set of objects. For example,
whether a user or service account can `create` pods.

|Roles |Collections of rules. You can associate, or bind, users and groups
to multiple roles.

|Bindings |Associations between users and/or groups with a role.
|===

Be mindful of the difference between local and cluster bindings. For example,
if you bind the `cluster-admin` role to a user by using a local role binding,
it might appear that this user has the privileges of a cluster administrator.
This is not the case. Binding the `cluster-admin` to a user in a project
grants super administrator privileges for only that project to the user. That user has the permissions of the cluster role `admin`, plus a few additional permissions like the ability to edit rate limits, for that project. This binding can be confusing via the web console UI, which does not list cluster role bindings that are bound to true cluster administrators. However, it does list local role bindings that you can use to locally bind `cluster-admin`.

////
If you do, when you upgrade
your cluster, the default roles are updated and
automatically reconciled when the server is started. During reconciliation, any
permissions that are missing from
the default roles are added. If you added more permissions to the role, they are
not removed.

If you customized the default roles and configured them to prevent automatic
role reconciliation, you must manually update policy definitions
when you upgrade OpenShift Container Platform.
////

The relationships between cluster roles, local roles, cluster role bindings,
local role bindings, users, groups and service accounts are illustrated below.

image::rbac.png[OpenShift Container Platform RBAC]

> **WARNING:** The `get pods/exec`, `get pods/*`, and `get *` rules grant execution privileges when they are applied to a role. Apply the principle of least privilege and assign only the minimal RBAC rights required for users and agents. For more information, see link:https://access.redhat.com/solutions/6989997[RBAC rules allow execution privileges].

## Evaluating authorization

OpenShift Container Platform evaluates authorization by using:

Identity:: The user name and list of groups that the user belongs to.

Action:: The action you perform. In most cases, this consists of:
- *Project*: The project you access. A project is a Kubernetes namespace with
additional annotations that allows a community of users to organize and manage
their content in isolation from other communities.
- *Verb* : The action itself:  `get`, `list`, `create`, `update`, `delete`, `deletecollection`, or `watch`.
- *Resource name*: The API endpoint that you access.
Bindings:: The full list of bindings, the associations between users or groups
with a role.

OpenShift Container Platform evaluates authorization by using the following steps:

1. The identity and the project-scoped action is used to find all bindings that
apply to the user or their groups.
1. Bindings are used to locate all the roles that apply.
1. Roles are used to find all the rules that apply.
1. The action is checked against each rule to find a match.
1. If no matching rule is found, the action is then denied by default.

including a matrix of the verbs and resources each are associated with.