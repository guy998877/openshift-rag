# Granting `dedicated-admin` access

Only the user who created the cluster can grant cluster access to other `cluster-admin` or `dedicated-admin` users. Users with `dedicated-admin` access have fewer privileges. As a best practice, grant `dedicated-admin` access to most of your administrators.

.Prerequisites

- You have added an identity provider (IDP) to your cluster.
- You have the IDP user name for the user you are creating.
- You are logged in to the cluster.

.Procedure

1. Enter the following command to promote your user to a `dedicated-admin`:
```bash
$ rosa grant user dedicated-admin --user=<idp_user_name> --cluster=<cluster_name>
```
1. Enter the following command to verify that your user now has `dedicated-admin` access:
```bash
$ oc get groups dedicated-admins
```
.Example output
```bash
NAME               USERS
dedicated-admins   rh-rosa-test-user
```
> **NOTE:** A `Forbidden` error displays if user without `dedicated-admin` privileges runs this command.