# Syncing the LDAP server with OpenShift Container Platform

You can sync all groups from the LDAP server with OpenShift Container Platform.

.Prerequisites

- Create a sync configuration file.
- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

- To sync all groups from the LDAP server with OpenShift Container Platform:
```bash
$ oc adm groups sync --sync-config=config.yaml --confirm
```
> **NOTE:** By default, all group synchronization operations are dry-run, so you must set the `--confirm` flag on the `oc adm groups sync` command to make changes to OpenShift Container Platform group records.