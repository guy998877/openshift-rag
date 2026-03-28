# Granting administrator privileges to a user

After you have configured an identity provider for your cluster and added a user to the identity provider, you can grant `dedicated-admin` cluster privileges to the user.

.Prerequisites

- You logged in to link:https://console.redhat.com/openshift[OpenShift Cluster Manager].
- You created an OpenShift Container Platform cluster.
- You configured an identity provider for your cluster.

.Procedure

1. Navigate to link:https://console.redhat.com/openshift[OpenShift Cluster Manager] and select your cluster.

1. Click the *Access control* tab.

1. In the *Cluster Roles and Access* tab, click *Add user*.

1. Enter the user ID of an identity provider user.

1. Click *Add user* to grant `dedicated-admin` cluster privileges to the user.

.Verification

- After granting the privileges, the user is listed as part of the `dedicated-admins` group under *Access control* -> *Cluster Roles and Access* on the OpenShift Cluster Manager page for your cluster.