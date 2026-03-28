# Revoking administrator privileges from a user

After you have granted `dedicated-admin` privileges to a user, you can revoke those privileges when they are no longer needed.

.Prerequisites

- You logged in to link:https://console.redhat.com/openshift[OpenShift Cluster Manager].
- You created an OpenShift Container Platform cluster.
- You have configured a GitHub identity provider for your cluster and added an identity provider user.
- You granted `dedicated-admin` privileges to a user.

.Procedure

1. Navigate to link:https://console.redhat.com/openshift[OpenShift Cluster Manager] and select your cluster.

1. Click the *Access control* tab.

1. In the *Cluster Roles and Access* tab, select image:kebab.png[title="Options menu"] next to a user and click *Delete*.

.Verification

- After revoking the privileges, the user is no longer listed as part of the `dedicated-admins` group under *Access control* -> *Cluster Roles and Access* on the OpenShift Cluster Manager page for your cluster.