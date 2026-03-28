# Creating a cluster admin

The `cluster-admin` role is required to perform administrator
level tasks on the OpenShift Container Platform cluster, such as modifying
cluster resources.

.Prerequisites

- You must have created a user to define as the cluster admin.

.Procedure

- Define the user as a cluster admin:
```bash
$ oc adm policy add-cluster-role-to-user cluster-admin <user>
```